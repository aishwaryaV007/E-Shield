# 1. FILE PURPOSE: Model A — the Reader. PDF answer script -> per-question student answer text,
#    matched to the answer key, with a semantic matching score. Feeds Model B (the marker).
# 2. RESPONSIBILITIES:
#    - rasterize the PDF (ingestion.pdf_loader),
#    - segment each page into lines (segmentation.line_segmenter) and OCR them (ocr.handwriting_ocr),
#    - group lines into answer blocks by indentation, dictionary-correct against the key vocabulary,
#    - assign each block to a question by content (Hungarian match on similarity) — robust to the
#      out-of-order, hard-to-read handwritten question numbers.
# 3. COMPLIANCE: reading only; marks are decided later by the trained model in evaluation/scorer.py.
import os
import re
import csv

import numpy as np
from scipy.optimize import linear_sum_assignment
from rapidfuzz import process, fuzz

from app.ingestion.pdf_loader import PDFLoader
from app.segmentation.line_segmenter import segment_lines
from app.ocr.handwriting_ocr import HandwritingOCR
from app.evaluation.similarity import similarity_matrix

_LEAD = re.compile(r"^\s*[^A-Za-z]*\s*(?:\d{1,2}\s*[.)])?\s*")
_MIN_WORDS = 4
_KEEP_SIM = 0.15


def load_answer_key(path: str) -> dict[str, str]:
    """Read answerkey.txt (Question_Number,Type,Correct_Answer) -> {qno: text} for short answers."""
    rows = list(csv.DictReader(open(path)))
    return {r["Question_Number"]: r["Correct_Answer"] for r in rows if r.get("Type") == "Short_Answer"}


def load_mcq_key(path: str) -> dict[str, str]:
    """-> {qno: correct_letter} for the MCQs (Type=MCQ)."""
    rows = list(csv.DictReader(open(path)))
    return {r["Question_Number"]: r["Correct_Answer"].strip().upper()[:1]
            for r in rows if r.get("Type") == "MCQ"}


# an MCQ answer line looks like "1. D", "20 C" — a number then a single isolated letter A-D
_MCQ_RE = re.compile(r"^(?:[Il|]\s+)?[^\dA-Za-z]*(\d{1,2})\s*[.)]?\s*([A-Da-d])\s*[.)]?\s*$")


_SECTION_MARKS = re.compile(r"\((\d+(?:\.\d+)?)\s*marks?\s*(?:each)?\)", re.I)
# inline marks on a question line: [8], (8), [8m], (4 marks)
_INLINE_MARKS = re.compile(r"[\[(]\s*(\d+(?:\.\d+)?)\s*(?:m|marks?)?\s*[\])]", re.I)
_QLINE = re.compile(r"^\s*(\d{1,2})\s*[.)]")


def parse_max_marks(answer_key_path: str, question_path: str | None,
                    keys: dict[str, str], default: float = 2.0) -> dict[str, float]:
    """Per-question max marks. Priority: answer-key Max_Marks column > question-paper parsing > default.
    Question paper: a section header like '(2 Marks Each)' applies to the questions under it; an inline
    '[8]' / '(4 marks)' on a question line overrides. Best-effort — falls back to `default`."""
    marks = {q: default for q in keys}
    # 1) reliable: Max_Marks column in the answer key, if present
    try:
        for r in csv.DictReader(open(answer_key_path)):
            if r.get("Question_Number") in marks and r.get("Max_Marks"):
                marks[r["Question_Number"]] = float(r["Max_Marks"])
    except Exception:
        pass
    # 2) parse the question paper. Question lines take inline marks (else the current section's
    #    marks); section headers only update `current` on non-question lines (so an inline
    #    "(4 marks)" on one question doesn't leak into the following questions).
    if question_path and os.path.exists(question_path):
        current = None
        for line in open(question_path, encoding="latin-1"):
            m = _QLINE.match(line)
            if m and m.group(1) in marks:
                inline = _INLINE_MARKS.search(line)
                if inline:
                    marks[m.group(1)] = float(inline.group(1))
                elif current is not None:
                    marks[m.group(1)] = current
            else:
                sec = _SECTION_MARKS.search(line)
                if sec:
                    current = float(sec.group(1))
    return marks


def _vocab(key: dict[str, str], question_path: str | None) -> list[str]:
    text = " ".join(key.values())
    if question_path and os.path.exists(question_path):
        text += " " + open(question_path, encoding="latin-1").read()
    return sorted({w.lower() for w in re.findall(r"[A-Za-z]{3,}", text)})


def _correct(text: str, vocab: list[str]) -> str:
    """Snap OCR words very close to a key term (fixes e.g. 'IOR'->'IQR', 'Radical Bass'->'radial basis')."""
    out = []
    for w in text.split():
        core = re.sub(r"[^A-Za-z]", "", w)
        if len(core) >= 3 and core.lower() not in vocab:
            m = process.extractOne(core.lower(), vocab, scorer=fuzz.ratio, score_cutoff=88)
            if m:
                out.append(w.replace(core, m[0])); continue
        out.append(w)
    return " ".join(out)


class ModelAReader:
    """Reads a handwritten answer script into per-question answers matched to the key."""

    def __init__(self, answer_key: dict[str, str], mcq_key: dict[str, str] | None = None,
                 question_path: str | None = None):
        self.key = answer_key
        self.mcq_key = mcq_key or {}
        self.vocab = _vocab(answer_key, question_path)
        self.ocr = HandwritingOCR()

    def read_script(self, pdf_path: str) -> dict[str, dict]:
        pages = PDFLoader.rasterize_pdf(pdf_path, dpi=200)  # BGR arrays
        blocks, cur, mcq = [], None, {}
        for bgr in pages:
            rgb = bgr[:, :, ::-1]
            for ln in segment_lines(rgb):
                crop = rgb[ln["y0"]:ln["y1"], ln["x0"]:ln["x1"]]
                res = self.ocr.recognize_text(crop)
                txt = res["text"].strip()
                if not txt:
                    continue
                # MCQ answer line? ("1. D" etc). Numbers 1-20 separate MCQs from short answers.
                mm = _MCQ_RE.match(txt)
                if mm and mm.group(1) in self.mcq_key:
                    conf = float(np.mean(res["confidences"])) if res["confidences"] else 1.0
                    mcq[mm.group(1)] = (mm.group(2).upper(), conf)
                    cur = None
                    continue
                if ln["is_header"]:
                    cur = {"t": [_LEAD.sub("", txt, 1)], "c": list(res["confidences"])}
                    blocks.append(cur)
                elif cur is not None:
                    cur["t"].append(txt); cur["c"].extend(res["confidences"])

        result: dict[str, dict] = {}
        # --- MCQs: always emit every MCQ question. The narrow stacked letter-column OCRs
        #     unreliably, so undetected ones are left blank (confidence 0) for the operator to
        #     confirm — MCQs are AI-assisted + human-verified, then exact-match graded.
        for qno in self.mcq_key:
            if qno in mcq:
                letter, conf = mcq[qno]
                result[qno] = {"answer": letter, "type": "mcq", "similarity": 0.0,
                               "ocr_confidence": round(conf, 3)}
            else:
                result[qno] = {"answer": "", "type": "mcq", "similarity": 0.0, "ocr_confidence": 0.0}

        # --- short answers: (text, ocr_confidence) per block, matched to key by content ---
        cand = [(_correct(" ".join(b["t"]).strip(), self.vocab),
                 float(np.mean(b["c"])) if b["c"] else 1.0) for b in blocks]
        cand = [c for c in cand if len(c[0].split()) >= _MIN_WORDS]
        if cand:
            qns = sorted(self.key, key=int)
            S = similarity_matrix([c[0] for c in cand], [self.key[q] for q in qns])
            keep = [i for i in range(len(cand)) if S[i].max() >= _KEEP_SIM] or list(range(len(cand)))
            Sk = S[keep]
            bi, ki = linear_sum_assignment(-Sk)
            for b, k in zip(bi, ki):
                result[qns[k]] = {"answer": cand[keep[b]][0], "type": "short",
                                  "similarity": round(float(Sk[b, k]), 3),
                                  "ocr_confidence": round(cand[keep[b]][1], 3)}
        return result
