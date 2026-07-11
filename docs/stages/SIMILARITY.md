# Stage: Semantic Similarity & Concept Coverage (Phase 2)

> Measures how close a student's answer is to the official answer key — by **meaning**, not keyword
> overlap — and which rubric concepts are covered. This is the primary signal the scorer uses.

---

## 1. Objective

Turn a (student_answer, answer_key, rubric) unit into interpretable signals: an overall similarity
score and a per-concept coverage map.

## 2. Steps (`backend/app/evaluation/`)

### `similarity.py`
- Embed the student answer and answer key with `all-MiniLM-L6-v2`.
- Compute cosine similarity + sentence-level alignment (which key points are matched).

### `concept_coverage.py`
- For each rubric key-point, classify **covered / partial / missing / contradicted**.
- Handle **negation** ("is not exothermic") so a contradiction is not counted as coverage
  (optionally via a small NLI cross-encoder).

## 3. Output

- `similarity: float` (0–1) and an aligned-points list → features for the mark predictor.
- Per-concept coverage breakdown → used by both the scorer and the feedback generator.

## 4. Why not an LLM

Similarity ranking + concept coverage are deterministic, explainable, and fast on CPU. Using them
(rather than "ask GPT to grade") keeps the system Track-02-compliant and student data private.
