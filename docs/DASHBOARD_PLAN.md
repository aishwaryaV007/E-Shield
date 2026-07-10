# Dashboard Interface Development Plan
> Development steps for the Next.js dashboard: training metrics + evaluated sheets.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

A local Next.js dashboard for exam-cell staff: train a model, upload scripts, and review the
auto-graded evaluated sheets.

```
┌────────────────────────────────────────────────────────────┐
│ Next.js App (frontend/src/app)                             │
└──────────────────────┬─────────────────────────────────────┘
         ┌─────────────┼──────────────┬────────────────┐
         ▼             ▼              ▼                ▼
   [ Overview ]  [ Training ]   [ Ingestion ]    [ Results ]
   batches +     metrics +      upload scripts   evaluated
   model status  feature imp.   + answer key     sheets
```

---

## 2. Technical Task Breakdown

### Task 1: App shell + navigation (`app/layout.tsx`, `components/layout/Sidebar.tsx`)
1. Sidebar links: Overview, Training, Ingestion, Results.
2. Batch selector (Zustand `batchStore`); TanStack Query providers.

### Task 2: Training view (`app/training/page.tsx`)
1. Upload the historical corpus + answer key; POST `/train`.
2. Render metrics (RMSE / MAE / R² / ±1-mark accuracy) and feature importance (Recharts).

### Task 3: Ingestion view (`app/ingestion/page.tsx`)
1. Upload scanned scripts + the answer key.
2. Trigger `/evaluate`; poll status.

### Task 4: Results views (`app/results/page.tsx`, `app/scripts/[id]/page.tsx`)
1. List evaluated scripts (total, percentage, low-confidence count).
2. Per-script evaluated sheet: `ScoreSummary` + `AnswerList` (per-question mark, feedback,
   deduction reasons) + `AnswerCompare` (student answer vs key, covered/missing points).

> There is no "override the mark" form in the MVP — the mark is the trained model's output.
> Low-confidence answers are surfaced for human verification before publishing.

---

## 3. Related Documents

*   [Frontend README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/frontend/README.md)
*   [API Contract](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)
*   [System Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)

## To-Do List

- [x] Scaffold Next.js dashboard UI
- [ ] Implement reporting and analytics views
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
