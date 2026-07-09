# ExamShield — Complete Build Workflow

**Hackathon:** HACK-THE-MATRIX 2026 (TECHNIDHI) — SNIST, 9–11 July
**Track:** 03 — Computer Vision
**Pitch:** *"Upload a batch of answer scripts. ExamShield finds the copying no human can catch, verifies every total, and highlights the evidence a grader needs — in minutes, not weeks."*

---

## 🧭 The One-Line Answer: What Starts First?

> **The shared ingestion pipeline (Scan → Preprocess → OCR) starts first — everything is built on top of it. The first FEATURE built is MarkSafe (guaranteed win), then CopyCatch (headline demo).**

Order of construction:

```
STEP 0          STEP 1        STEP 2       STEP 3        STEP 4      STEP 5      STEP 6       STEP 7
Ingestion  →   MarkSafe  →  CopyCatch → ReEval Guard → ScriptID → BlankCheck → RubricLens → Demo UI
(pipeline)     (trust)      (headline)   (1-hr add)    (quick)    (if time)    (stretch)    + Pitch
```

*(EvaluatorLens = roadmap slide only, not built.)*

---

## 🏗️ System Architecture — The Total Workflow

Every feature runs on ONE shared pipeline. Build the spine once, hang features off it.

```
                        ┌─────────────────────────────┐
                        │   INPUT: Batch of scanned    │
                        │   answer-sheet images/PDFs   │
                        └──────────────┬──────────────┘
                                       │
                        ┌──────────────▼──────────────┐
                        │  STAGE 1 — INGESTION         │
                        │  • Load batch                │
                        │  • Page count per script     │
                        │  • Deskew / denoise /        │
                        │    binarize (preprocess)     │
                        └──────────────┬──────────────┘
                                       │
                        ┌──────────────▼──────────────┐
                        │  STAGE 2 — ZONE CALIBRATION  │
                        │  (one-time, 2 min/format)    │
                        │  • Draw marks column zone    │
                        │  • Draw total box zone       │
                        │  • Draw roll-number box zone │
                        │  • Draw answer regions       │
                        └──────────────┬──────────────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
      ┌──────────▼─────────┐ ┌────────▼────────┐ ┌─────────▼─────────┐
      │ STAGE 3A            │ │ STAGE 3B         │ │ STAGE 3C           │
      │ DIGIT OCR (robust)  │ │ PROSE OCR (fuzzy)│ │ INK-PRESENCE CV    │
      │ marks, totals,      │ │ answer text with │ │ writing detected   │
      │ roll numbers        │ │ confidence scores│ │ per answer region  │
      └──────────┬─────────┘ └────────┬────────┘ └─────────┬─────────┘
                 │                     │                     │
     ┌───────────┼──────────┐          │                     │
     │           │          │          │                     │
┌────▼───┐ ┌────▼─────┐ ┌──▼──────┐ ┌─▼──────────┐ ┌───────▼────────┐
│MarkSafe│ │ ReEval   │ │ ScriptID│ │ CopyCatch  │ │ BlankCheck     │
│ verify │ │ Guard    │ │ roll-no │ │ pairwise   │ │ pages present, │
│ totals │ │borderline│ │ vs      │ │ similarity │ │ attempted vs   │
│        │ │ flags    │ │ register│ │ + clusters │ │ blank          │
└────┬───┘ └────┬─────┘ └──┬──────┘ └─┬──────────┘ └───────┬────────┘
     │          │          │          │        ┌───────────┘
     │          │          │          │        │   ┌────────────┐
     │          │          │          │        │   │ RubricLens │ (stretch)
     │          │          │          │        │   │ NLI rubric │
     │          │          │          │        │   │ highlights │
     │          │          │          │        │   └─────┬──────┘
     └──────────┴────────┬─┴──────────┴────────┴─────────┘
                         │
          ┌──────────────▼──────────────┐
          │  STAGE 4 — REVIEW DASHBOARD │
          │  • Ranked flags (never      │
          │    verdicts) + image-level  │
          │    side-by-side evidence    │
          │  • Human reviews & decides  │
          └─────────────────────────────┘
```

**Design principle (repeat in every answer to judges):** *The system never accuses and never finalizes. Every output is a ranked flag with image-level evidence for human review.*

---

## 📅 24-Hour Battle Plan

### PRE-EVENT (before the clock starts) ⚡ NON-NEGOTIABLE PREP

You do NOT have time to create demo data inside the 24 hours. Do this before you walk in:

| # | Task | Why it can't wait |
|---|------|-------------------|
| 0.1 | **Collect 30–40 real handwritten scripts from classmates**, including **2 planted colluder pairs** | CopyCatch's baseline math is only valid at 30+ sheets. Cannot be created at the venue. |
| 0.2 | Scan/photograph all scripts at consistent quality | Dataset ready at hour 0 |
| 0.3 | Register CSV with planted errors: 1 duplicate roll no, 1 absentee-with-sheet, 1 present-without-sheet | ScriptID demo data |
| 0.4 | Grade some scripts with **planted totaling errors** + borderline totals (39 when pass=40) | MarkSafe + ReEval Guard demo data |
| 0.5 | Repo + stack ready; OCR lib (PaddleOCR/Tesseract), sentence-embedding model, NLI model **downloaded and tested offline** on your laptops | Venue Wi-Fi will betray you |

### THE 24 HOURS — hour by hour

**⏱️ H0–H3 — The spine (everything depends on this)**
- H0–H1: Batch image loader + preprocessing (deskew, denoise, binarize)
- H1–H2: Zone calibration tool — draw rectangles for marks column, total box, roll-no box, answer regions → save template JSON
- H2–H3: Digit OCR on calibrated zones with confidence scores

**⏱️ H3–H7 — MarkSafe (Priority 1: the guaranteed win)**
- Parse per-question marks (integers, decimals, evaluable `a+b`)
- Sum vs written total → `OK` / `MISMATCH` / `AMBIGUOUS — human review` (never guess strikeouts)
- Ink-presence check: answer written but marks cell empty → flag
- Minimal results table with image-crop evidence

✅ **H7 GATE:** MarkSafe catches the planted totaling errors on the real corpus. **You now have a demo no matter what happens next.**

**⏱️ H7–H14 — CopyCatch (Priority 2: the shock demo)**
- H7–H9: Prose OCR of answer regions with per-token confidence
- H9–H11: Sentence embeddings (confidence-weighted tokens only) → pairwise similarity (~600 pairs at 35 scripts)
- H11–H12: Class-baseline anomaly ranking (class-wide shared mistakes auto-discounted)
- H12–H14: Copying-network graph + **Tier-2 side-by-side image evidence view**

✅ **H14 GATE:** the 2 planted colluder pairs light up; innocent pairs don't.

**⏱️ H14–H16 — The two quick wins (cheap points)**
- H14–H15: **ReEval Guard** — pure logic on MarkSafe's totals → borderline-sheet recheck queue (the PDF says it "ships in an hour" — hold it to that)
- H15–H16: **ScriptID** — digit-OCR roll-no box vs register CSV → duplicates / absentees-with-sheets / present-without-sheets

**⏱️ H16–H19 — One dashboard + polish**
- Wire all 4 features into a single review dashboard: ranked flags, evidence crops, copying graph front and center
- **H19 = FEATURE FREEZE.** Bug-fix on the real corpus only after this.

**⏱️ H19–H21 — Stretch (ONLY if everything above is stable)**
- **BlankCheck:** page count + attempted-vs-blank per script (ink presence)
- **RubricLens:** retrieval + NLI highlights, never outputs a mark
- If anything upstream is shaky, spend these 2 hours hardening instead. Cut without mercy.

**⏱️ H21–H24 — Demo prep (do not skip to keep coding)**
- H21–H22: Record a **fallback demo video** of the full flow (insurance against live-demo death)
- H22–H23: Rehearse the live-judge demo **twice, full run**, including scanning judges' handwriting on the spot
- H23–H24: Pitch deck / talking points, sleep-deprived sanity check, charge everything

### If you fall behind — the cut order

Cut from the bottom, never the top: RubricLens → BlankCheck → ScriptID → ReEval Guard. **MarkSafe + CopyCatch + dashboard is a complete winning demo by itself.** Never sacrifice the H21–H24 demo-prep block to build one more feature.

---

## 🎬 Live Demo Script (the judging flow)

1. **Hook (30 s):** "An evaluator grading 300 sheets can't remember what sheet #12 said by sheet #200."
2. **The shock moment — CopyCatch live:** 4 judges each handwrite a short answer; 2 secretly copy each other → scan → the graph lights up exactly the colluding pair, matching regions side-by-side. **The judges are the demo.**
3. **The trust layer — MarkSafe on the 35-script corpus:** "…and while checking copying, it also caught 3 totaling errors that would have become paid revaluation cases."
4. **Rapid-fire utility:** ReEval Guard borderline queue → ScriptID register mismatches → (BlankCheck triage if built)
5. **Honesty beat:** show a strikeout flagged "ambiguous — human review" — *a wrong guess is impossible by construction.*
6. **Closing pitch:** *"120 answer sheets are waiting for you after judging this hackathon. ExamShield would have them integrity-checked, error-verified, and evidence-highlighted before dinner — and every flag it raises is reviewed by a human, never decided by a machine."*

---

## 📋 Feature Reference Table

| Priority | Feature | Role | OCR need | When built |
|----------|---------|------|----------|------------|
| 1 | **MarkSafe** | Trust layer — totaling verification | Digits only (robust) | H3–H7 |
| 2 | **CopyCatch** | Headline — collusion graph | Fuzzy prose (tolerant) | H7–H14 |
| 3 | **ReEval Guard** | Borderline-sheet pre-check | None (reuses MarkSafe) | H14–H15 |
| 4 | **ScriptID** | Roll-number vs register | Digits only (robust) | H15–H16 |
| 5 | **BlankCheck** | Pre-grading triage | Ink presence only | H19–H21, if time |
| 6 | **RubricLens** | Grader evidence assist (never grades) | Prose (assist-only, safe) | H19–H21, stretch |
| — | **EvaluatorLens** | Marks-consistency stats | None (register data) | Roadmap slide only |
| ✂️ | ~~VivaFair~~ | Dropped — confound unfixable | — | One-line roadmap note |

---

## ⚠️ Rules That Keep You Safe in Q&A

- **Never say "detects cheating"** — say *"ranks anomalous similarity for human review with seating data."*
- **Never let OCR convict** — machine similarity only *ranks* pairs (Tier 1); confirmation is always human eyes on original images (Tier 2).
- **Never guess ambiguous marks** — strikeouts/overwrites → "ambiguous, human review" flag. Failure mode = extra flag, never a wrong verdict.
- **RubricLens never outputs a mark** — a missed highlight is a shrug, not a scandal.
- **Disclose the corpus honestly** — "volunteer-written corpus of 30–40 real scripts with 2 planted colluder pairs."
- **Template dependence is a feature** — "2-minute one-time zone calibration per institution: bring your format."

---

## ✅ Milestone Checklist

- [ ] Pre-event: 30–40 script corpus scanned (2 colluder pairs, planted total errors, register CSV with errors)
- [ ] Pre-event: OCR + embedding + NLI models downloaded and verified running offline
- [ ] H3: shared pipeline — ingest → preprocess → calibrate → digit OCR
- [ ] H7: MarkSafe catches planted totaling errors ← **guaranteed win secured**
- [ ] H14: CopyCatch graph lights up planted colluder pairs ← **shock demo secured**
- [ ] H16: ReEval Guard + ScriptID wired in
- [ ] H19: everything in one dashboard → **FEATURE FREEZE**
- [ ] H21: stretch features only if stable — otherwise harden
- [ ] H24: fallback video recorded + 2 full demo rehearsals done + pitch ready
