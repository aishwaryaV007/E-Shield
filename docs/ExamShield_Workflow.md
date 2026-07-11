# ExamShield — Complete Build Workflow

**Hackathon:** HACK-THE-MATRIX 2026 (TECHNIDHI) — SNIST, 9–11 July
**Track:** 02 — Predictive Analytics (ML / DL)
**Pitch:** *"Train ExamShield on a few previously corrected answer sheets, and it grades new
handwritten scripts the way your teachers do — question-wise marks, feedback, and a percentage,
in minutes."*

---

## 🧭 What starts first?

> **Phase 1 (train the mark-predictor) proves the core idea. Phase 2 (OCR → segment → score) grades
> new scripts. Build the training + scoring path first; OCR/segmentation feeds it.**

```
STEP 0          STEP 1         STEP 2        STEP 3         STEP 4        STEP 5        STEP 6
Storage/DB  →  Phase-1 train → Ingestion → Handwriting → Segmentation → Scoring →   Results UI
(schema)       (features →     (PDF→img)    OCR           (Q + key)      (model →     + feedback
               XGBoost →                                                marks)       + metrics
               metrics)
```

---

## 🏗️ The two-phase workflow

```
PHASE 1 — TRAINING (learn how teachers grade)
  Historical corrected scripts + teacher marks + answer keys + rubrics
      → dataset_builder → features → trainer (XGBoost, tuned) → evaluate
      → mark_predictor.pkl + metrics (RMSE / MAE / R² / ±1-mark accuracy)

PHASE 2 — EVALUATION (grade new scripts)
  Scanned scripts → ingestion (deskew/binarize) → handwriting OCR (+confidence)
      → segmentation (split questions, match answer key + rubric)
      → similarity + concept coverage → scorer (trained model → marks, % bands)
      → feedback + deduction reasons → report (question-wise marks, total, %)
```

**Design principle (repeat to judges):** *The mark is produced by the trained model — never by
an LLM. Unreadable answers are flagged for human verification, never guessed.*

---

## 📅 24-Hour Battle Plan

### PRE-EVENT (before the clock) — non-negotiable prep
| # | Task | Why it can't wait |
|---|------|-------------------|
| 0.1 | **Collect a small historical corpus:** past answers with teacher-awarded marks (even 100–200 answer/mark pairs) | Phase-1 training needs labels; can't be created at the venue. |
| 0.2 | Prepare a question paper + model answer key + rubric | Phase-2 grading target |
| 0.3 | Scan a fresh batch of student scripts to grade live | Demo input |
| 0.4 | Download + test OCR + `all-MiniLM-L6-v2` offline; install `xgboost` | Venue Wi-Fi will betray you |

### THE 24 HOURS
- **H0–H2 — Storage:** schema (models, answer_keys, questions, scripts, evaluations), DB init.
- **H2–H7 — Phase-1 training:** dataset_builder → features → XGBoost trainer → evaluate. **GATE:
  report RMSE + ±1-mark accuracy vs teacher marks.** Fallback: unsupervised similarity-to-key baseline.
- **H7–H11 — Ingestion + OCR:** PDF→image, deskew/binarize, handwriting OCR + confidence.
- **H11–H14 — Segmentation:** split into questions, match answer key + rubric.
- **H14–H18 — Scoring:** similarity + coverage → trained model → marks; feedback + report. **GATE:
  a scanned script → a full evaluated sheet.**
- **H18–H21 — Results UI:** Training metrics view + evaluated-sheet view; **feature freeze at H21**.
- **H21–H24 — Demo prep:** fallback video, two full rehearsals, pitch.

### If you fall behind — cut order
Cut from the bottom: feedback phrasing → concept-coverage NLI → fancy UI. **Trained model +
similarity scoring + one evaluated sheet is a complete winning demo.** Never sacrifice demo prep.

---

## 🎬 Live Demo Script

1. **Training:** show a model trained on the historical corpus with RMSE + ±1-mark accuracy vs teacher marks.
2. **Upload** a fresh scanned script + answer key; run Phase 2 live.
3. **Evaluated sheet:** question-wise marks, total, percentage, per-answer feedback + deduction reasons.
4. **Agreement:** compare a few predicted marks to a teacher's marks.
5. **Honesty beat:** an unreadable answer flagged *"low confidence — verify"*, never guessed; and
   *"the mark is our trained model's prediction, never an LLM's."*

---

## ⚠️ Rules that keep you safe in Q&A

- **Never let an LLM assign a mark** — Track 02 prohibits it. The mark is the XGBoost regressor's output.
- **Report real metrics** — RMSE / MAE / R² / ±1-mark accuracy on a held-out split.
- **Same features at train + inference** — one feature function, no skew.
- **Flag, don't guess** — low-confidence OCR answers go to a human before publishing.
- **Disclose the corpus honestly** — "trained on N teacher-marked answers; metrics on a held-out split."

---

## ✅ Milestone Checklist

- [ ] Pre-event: historical teacher-marked corpus + answer key + fresh scripts + models downloaded
- [ ] H2: storage schema live
- [ ] H7: Phase-1 model trained, metrics reported ← **core idea proven**
- [ ] H14: script → questions matched to answer key
- [ ] H18: script → full evaluated sheet ← **end-to-end secured**
- [ ] H21: Results + Training UI wired → **FEATURE FREEZE**
- [ ] H24: fallback video + 2 rehearsals + pitch ready

## To-Do List

- [x] Document initial processing workflow
- [x] Complete end-to-end integration
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
