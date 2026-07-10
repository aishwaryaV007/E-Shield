# Application Execution Guide
> Setup, training, and running the auto-grader.

*Design / Planned — Not yet implemented*

---

## 1. Installation

```bash
git clone https://github.com/aishwaryaV007/E-Shield.git
cd E-Shield/backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
cd ../frontend && npm install
```

## 2. Cache models (once, needs internet)

```bash
cd ../backend && source .venv/bin/activate
python ../scripts/download_models.py
```
Caches the handwriting OCR model + `all-MiniLM-L6-v2`. **No LLM is downloaded** — the mark comes
from a trained regressor.

## 3. Phase 1 — train the mark-predictor

```bash
python ../scripts/seed_demo_data.py     # generates historical corpus + answer key + a batch
# then train (via the Training page's POST /train, or the training pipeline entrypoint)
```
Produces `models_cache/mark_predictor.pkl` and a metrics report (RMSE / MAE / R² / ±1-mark accuracy).

## 4. Start the services

```bash
# Backend (from backend/)
uvicorn main:app --reload --port 8000     # http://127.0.0.1:8000/docs

# Frontend (from frontend/)
npm run dev                               # http://localhost:3000
```

## 5. Phase 2 — grade a batch

1. **Training** page → confirm a model is trained (metrics shown).
2. **Ingestion** page → upload scanned scripts + the answer key → run evaluation.
3. **Results** page → open a script → the evaluated sheet: question-wise marks, total, percentage,
   feedback, deduction reasons; low-confidence answers flagged.

## 6. Verify

```bash
cd backend && pytest        # skeleton test suites
```
Compare a few predicted marks against a teacher's marks to sanity-check agreement.

---

## 7. Related Documents

*   [SETUP.md](file:///Users/gaurav/Desktop/MyProjects/E-Shield/SETUP.md)
*   [DevOps Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DEVOPS_PLAN.md)
*   [Testing Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TESTING_PLAN.md)

## To-Do List

- [x] Document backend local setup
- [x] Document frontend local setup
- [ ] Review document for technical accuracy against current implementation.
- [ ] Ensure all referenced internal links are valid and working.
- [ ] Add architectural or workflow diagrams where applicable.
- [ ] Proofread for grammar, consistency, and tone.
- [ ] Cross-reference with SYSTEM_DESIGN.md for alignment.
- [ ] Verify that security considerations are documented if relevant.
- [ ] Add examples or code snippets to clarify complex sections.
- [ ] Check formatting (headers, bolding, lists) for readability.
