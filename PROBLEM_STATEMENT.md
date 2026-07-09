# ExamShield v2 — Problem Statement & Solution

**Hackathon:** HACK-THE-MATRIX 2026 (TECHNIDHI) — SNIST, 9–11 July | 24 Hours
**Track:** 03 — Computer Vision
**Team Repo:** E-Shield

---

## 1. Problem Statement

Every semester, universities manually evaluate lakhs of handwritten answer sheets — and the process fails in three documented, expensive ways:

1. **Undetectable copying.** An evaluator grading 300 sheets cannot remember what sheet #12 said by sheet #200. Collusion between students is practically invisible to a human working sequentially — cross-comparing 300 sheets means **44,850 pairwise comparisons**, which no human performs.
2. **Totaling and transcription errors.** Tired evaluators add marks wrong, skip attempted answers, or transcribe totals incorrectly. Students pay revaluation fees to fix arithmetic mistakes — a publicly documented pain with revaluation fees, withdrawn results, and even court fines on record.
3. **Administrative mix-ups.** Misread or duplicated roll numbers produce "I got someone else's marks" scandals; lost supplements produce unresolvable disputes; borderline totals (39 when pass = 40) flood the system with paid revaluation requests after results are published.

The existing "solution" is more manual labor: moderation committees, second evaluations, and paid revaluation — all *after* the damage is done.

### Phase-1 Validation Checkpoint (per hackathon rules)

| Checkpoint | Our Answer |
|------------|-----------|
| **TARGET_USER** | **Controllers of Examinations, exam-cell staff, and evaluators** at universities/colleges — not "everyone." They own the batch of physical answer scripts and are legally accountable for result accuracy. |
| **PROBLEM_STATE** | Yes — measurably. Cross-comparing 300 scripts for collusion is 44,850 comparisons a human never does (currently ~0% coverage → 100% coverage in minutes). Totaling verification that takes an office days happens in seconds per script. Pre-highlighted rubric evidence targets **~50% reduction in per-sheet grading time**. Borderline-sheet pre-checks happen *before* results are published instead of paid disputes after. |
| **AI_NECESSITY** | Yes — the core tasks are impossible without CV/ML. Handwritten text must be read (OCR — CNN-based recognition), semantic similarity between differently-worded handwritten answers requires sentence embeddings (a human can't compare 44,850 pairs; string matching can't handle handwriting variance), and rubric-contradiction detection requires NLI. Only the final *decision* is human — by design. |

---

## 2. Proposed Solution

**ExamShield v2** — an AI evaluation engine for answer sheets. Upload a batch of scanned answer scripts; ExamShield finds the copying no human can catch, verifies every total, and highlights the evidence a grader needs — in minutes, not weeks.

### Design principle

> **The system never accuses and never finalizes.** Every output is a ranked flag with image-level evidence for human review. Where OCR must be precise (marks), we use digits only. Where OCR is noisy (prose), we only need relative similarity. Where precision is impossible (grading), we highlight evidence instead of deciding.

### Feature suite

| # | Feature | What it does | CV/AI used |
|---|---------|--------------|------------|
| 1 | **MarkSafe** (trust layer) | Verifies every per-question mark and total on graded sheets; ambiguous regions (strikeouts, overwrites) are flagged for human review — a wrong guess is impossible by construction | Digit OCR on calibrated zones + ink-presence detection |
| 2 | **CopyCatch** (headline) | Cross-compares every pair of scripts; flags anomalous-similarity clusters as a copying-network graph with side-by-side image evidence. Two-tier: machine similarity only *ranks*; human eyes on original handwriting *confirm* | Prose OCR → sentence embeddings → pairwise similarity → class-baseline anomaly ranking |
| 3 | **ReEval Guard** | Queues borderline totals (one mark from pass/grade boundary) for pre-emptive recheck *before* results are published | Pure logic on MarkSafe's extracted totals |
| 4 | **ScriptID** | Digit-OCRs the roll-number box and cross-checks the class register: duplicates, absentees-with-sheets, present-without-sheets | Digit OCR + register matching |
| 5 | **BlankCheck** | Pre-grading triage: pages present, attempted vs blank questions, workload per script | Page-count + ink-presence CV |
| 6 | **RubricLens** (assist) | Highlights where each rubric point appears in an answer — entailment in green, contradiction in red. **Never outputs a mark**; the human grades | Retrieval + NLI cross-encoder |

*(Roadmap: EvaluatorLens — grading-consistency statistics across evaluators, pure register data.)*

### Architecture (one shared pipeline)

```
Scanned scripts → Preprocess (deskew/denoise/binarize) → One-time zone calibration
   → OCR branches (digit / prose-with-confidence / ink-presence)
   → Feature analyses (MarkSafe, CopyCatch, ReEval Guard, ScriptID, BlankCheck, RubricLens)
   → Review dashboard: ranked flags + image-level evidence → HUMAN DECIDES
```

---

## 3. Track 03 Compliance — Computer Vision (all requirements met)

| Track Requirement | How ExamShield satisfies it |
|-------------------|------------------------------|
| **Input Stream** — image or video processing | Batch of scanned answer-sheet images/PDFs, preprocessed with OpenCV (deskew, denoise, adaptive binarization) |
| **Vision Pipeline** — CNN, YOLO, ResNet, ViT | CNN-based OCR (PaddleOCR text detection + recognition networks) running locally; transformer embeddings downstream of the vision output |
| **Automated Understanding** — detection, classification, segmentation, or **OCR** | OCR on two tiers: robust digit OCR (marks, totals, roll numbers) and confidence-weighted prose OCR (answer text); ink-presence detection per answer region |
| **Measurable Output** — bounding boxes, labels, masks, or **extracted text** | Extracted marks/totals/roll numbers with confidence scores, bounding-box evidence crops for every flag, similarity scores, anomaly rankings, flagged-region coordinates |
| **Strictly Prohibited** — image-to-GPT upload displaying a text answer | **Fully compliant:** no GPT/LLM anywhere in the pipeline. Local CV models only — PaddleOCR (CNN), MiniLM sentence embeddings, small NLI cross-encoder. Every output is a deterministic, explainable pipeline result |

---

## 4. Quantified Productivity Impact (the 20% "critical focus" metric)

- **Collusion coverage: 0% → 100%.** 44,850 pairwise comparisons on a 300-script batch, done in minutes — a check that currently never happens at all.
- **Totaling verification: days → seconds per batch**, with zero false verdicts by construction (ambiguity is flagged, never guessed).
- **~50% reduction in per-sheet grading time** via pre-highlighted rubric evidence (RubricLens), with the human keeping full marking authority.
- **Revaluation demand reduced at the source:** borderline sheets are re-checked *before* publication (ReEval Guard) instead of paid disputes after; totaling errors caught pre-publication.
- **Result mix-ups prevented:** every roll number verified against the register (ScriptID) — duplicates and mismatches flagged instantly.
- **Batch triage automated:** page counts and attempted-question workload per script (BlankCheck) with a timestamped record that settles "my supplement was lost" disputes.

---

## 5. Evaluation-Rubric Alignment (70% universal + 30% track)

| Rubric criterion | Weight | Our answer |
|------------------|--------|-----------|
| Tech Execution | 25% | Full CV pipeline (preprocess → zone calibration → dual-tier OCR → embeddings → anomaly stats → graph), 6 features on one spine, all local/offline |
| Productivity Impact | 20% | Quantified above — coverage 0→100%, days→seconds, ~50% grading-time cut |
| Innovation | 20% | Collusion detection on *handwritten* scripts via class-baseline anomaly ranking + two-tier (machine ranks / human confirms) evidence design — differentiated from plagiarism checkers (typed text only) and from auto-graders (we refuse to auto-grade; that's the point) |
| Scalability | 15% | Template-based "bring your format" zone calibration (2 min per institution, reuse forever); similarity stage is O(n²) on embeddings — 300 scripts = milliseconds; SQLite/JSON storage, no server dependencies |
| UX & Presentation | 20% | Single review dashboard, ranked flags with image evidence, live judge demo: judges handwrite answers, two secretly copy, the graph lights up the colluding pair |
| Track-specific tech | 30% | See §3 — every Track 03 requirement met with real CV pipelines, banned behavior avoided entirely |

---

## 6. Scope Honesty (what we deliberately do NOT claim)

- **No auto-grading.** RubricLens highlights evidence; it never assigns marks. One wrong grade in a live demo kills all trust — so the fragile promise is removed entirely.
- **No accusation.** CopyCatch outputs "abnormal similarity cluster — review with seating data," never "cheater."
- **No guessing on ambiguity.** Strikeouts/overwrites → "ambiguous, human review." The failure mode is an extra review flag, never a wrong verdict.
- **VivaFair (viva-fairness audio analysis) was cut** — the adaptive-questioning confound is unfixable at hackathon scale. It stays on the roadmap slide only.
- **Demo corpus disclosed honestly:** 30–40 volunteer-written real scripts with 2 planted colluder pairs; baseline statistics are valid at 30+.

---

## 7. Demo Plan

1. Four judges handwrite a short answer; two secretly copy each other.
2. Scripts are scanned live → CopyCatch's graph lights up exactly the colluding pair, matching handwriting regions side-by-side. **The judges are the demo.**
3. On the 35-script corpus: MarkSafe surfaces the planted totaling errors — "these would have become paid revaluation cases."
4. Rapid-fire: ReEval Guard's borderline queue, ScriptID's register mismatches, BlankCheck triage.
5. Honesty beat: a strikeout flagged "ambiguous — human review" — *a wrong guess is impossible by construction.*

> **Closing:** "120 answer sheets are waiting for you after judging this hackathon. ExamShield would have them integrity-checked, error-verified, and evidence-highlighted before dinner — and every flag it raises is reviewed by a human, never decided by a machine."
