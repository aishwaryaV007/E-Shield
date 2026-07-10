# Models Module

Local model loaders (offline, no external API calls).

- `embedder.py` — sentence-embedding model (all-MiniLM-L6-v2) for semantic similarity.
- `mark_model.py` — loads the **trained mark-predictor** produced by Phase-1 training; falls
  back to the unsupervised similarity baseline if no model has been trained yet.
