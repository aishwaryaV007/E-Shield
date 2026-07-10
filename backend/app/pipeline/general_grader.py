# 1. FILE PURPOSE: Format-agnostic grader — grade ANY handwritten exam from a plain-text
#    question paper + answer key (no fixed layout, no CSV, any numbering like "Q1." or "21.").
# 2. HOW: OCR every line, then align lines to questions by CONTENT via monotonic DP (answers appear
#    in question order), so it works even when the handwritten question numbers OCR poorly and the
#    text is flush-left. MCQ letters are extracted from the aligned chunk.
# 3. DEPENDS ON: ingestion, segmentation.line_segmenter, ocr, evaluation.similarity/report.
import os
import re

import numpy as np
from sentence_transformers import util

from app.ingestion.pdf_loader import PDFLoader
from app.segmentation.line_segmenter import segment_lines
from app.ocr.handwriting_ocr import get_ocr
from app.models.embedder import get_embedder
from app.evaluation.report import build_report

_QN_SPLIT = re.compile(r"(?im)^\s*Q\s*(\d+)\s*[.)]")
_MARKS = re.compile(r"(?i)marks?\s*[:=]?\s*(\d+(?:\.\d+)?)")
_SECTION_MARKS = re.compile(r"\(?[^)]*?(\d+(?:\.\d+)?)\s*marks?", re.I)
_OPT = re.compile(r"(?i)correct\s*option\s*[:=]?\s*\(?\s*([a-dA-D])")
_LETTER = re.compile(r"\b([a-dA-D])\s*[).]")


def parse_prose_key(answer_path: str, question_path: str | None = None) -> dict[str, dict]:
    """Parse plain-text answer key (+ question paper) -> {qno: {type, correct, max_marks, question}}."""
    keys: dict[str, dict] = {}
    atext = open(answer_path, encoding="utf-8", errors="ignore").read()
    parts = _QN_SPLIT.split(atext)          # [preamble, num, body, num, body, ...]
    for i in range(1, len(parts) - 1, 2):
        qn, body = parts[i], parts[i + 1]
        mk = _MARKS.search(body)
        max_marks = float(mk.group(1)) if mk else 2.0
        opt = _OPT.search(body)
        if opt:
            keys[qn] = {"type": "mcq", "correct": opt.group(1).lower(),
                        "max_marks": max_marks, "question": ""}
        else:
            ans = re.split(r"(?i)rubric points|marks?\s*[:=]", body)[0]
            keys[qn] = {"type": "short", "correct": re.sub(r"\s+", " ", ans).strip(),
                        "max_marks": max_marks, "question": ""}

    if question_path and os.path.exists(question_path):
        qtext = open(question_path, encoding="utf-8", errors="ignore").read()
        qp = _QN_SPLIT.split(qtext)
        for i in range(1, len(qp) - 1, 2):
            qn, body = qp[i], qp[i + 1]
            if qn not in keys:
                continue
            keys[qn]["question"] = re.sub(r"\s+", " ", body).strip()[:400]
            sm = _SECTION_MARKS.search(body)
            if sm:
                keys[qn]["max_marks"] = float(sm.group(1))
    return keys


def _ocr_lines(pdf_path: str) -> list[str]:
    ocr = get_ocr()
    lines = []
    for bgr in PDFLoader.rasterize_pdf(pdf_path, dpi=200):
        rgb = bgr[:, :, ::-1]
        for ln in segment_lines(rgb):
            t = ocr.recognize_text(rgb[ln["y0"]:ln["y1"], ln["x0"]:ln["x1"]])["text"].strip()
            if t:
                lines.append(t)
    return lines


def _align(S: np.ndarray) -> list[int]:
    """Monotonic DP: assign each line (row) to a question (col), non-decreasing, max total score."""
    m, n = S.shape
    dp = np.full((m, n), -1e18)
    back = np.zeros((m, n), int)
    dp[0] = S[0]
    for i in range(1, m):
        run_max, run_arg = -1e18, 0
        pref_max = np.empty(n); pref_arg = np.empty(n, int)
        for j in range(n):
            if dp[i - 1][j] > run_max:
                run_max, run_arg = dp[i - 1][j], j
            pref_max[j], pref_arg[j] = run_max, run_arg
        dp[i] = S[i] + pref_max
        back[i] = pref_arg
    assign = [0] * m
    assign[m - 1] = int(np.argmax(dp[m - 1]))
    for i in range(m - 1, 0, -1):
        assign[i - 1] = int(back[i][assign[i]])
    return assign


def grade_general(pdf_path: str, keys: dict[str, dict], script_id: str,
                  default_max: float = 2.0) -> dict:
    """OCR the script, align lines to questions by content, and grade every question."""
    qns = sorted(keys, key=int)
    lines = _ocr_lines(pdf_path)
    emb = get_embedder()
    # reference text per question = question + expected answer (rich signal, works for MCQ too)
    refs = [(keys[q]["question"] + " " + (keys[q]["correct"] if keys[q]["type"] == "short" else "")).strip()
            or keys[q]["correct"] or keys[q]["question"] for q in qns]

    if lines:
        S = util.cos_sim(emb.encode(lines), emb.encode(refs)).cpu().numpy()
        assign = _align(S)
    else:
        assign = []

    chunks = {q: [] for q in qns}
    for i, a in enumerate(assign):
        chunks[qns[a]].append(lines[i])

    answers = {}
    for q in qns:
        text = re.sub(r"\s+", " ", " ".join(chunks[q])).strip()
        if keys[q]["type"] == "mcq":
            m = _LETTER.search(text)
            answers[q] = {"answer": (m.group(1).lower() if m else ""), "type": "mcq", "ocr_confidence": 0.9}
        else:
            answers[q] = {"answer": text, "type": "short", "ocr_confidence": 0.9}

    typed = {q: {"type": keys[q]["type"], "correct": keys[q]["correct"]} for q in qns}
    mm = {q: float(keys[q].get("max_marks", default_max)) for q in qns}
    return build_report(script_id, answers, typed, max_marks=mm)
