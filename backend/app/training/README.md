# Model Training & Evaluation — Phase 1 Pipeline

This directory contains the core training pipeline for **Model B (The Mark-Predictor)**, complying strictly with the Track 02 (ML/DL Predictive Analytics) requirements by learning directly from historical evaluations instead of calling LLM grading prompts.

---

## 1. Pipeline Overview

The training workflow follows a structured sequence:
1. **`dataset_builder.py`**: Reads raw student scripts, question papers, and answer keys, then assembles tabular training rows mapping student answers, keys, and actual human-awarded marks.
2. **`features.py`**: Extracts high-quality numerical features from text matches.
3. **`trainer.py`**: Executes hyperparameter tuning via Grid Search combined with GroupKFold cross-validation, fits the final XGBoost Regressor, and serializes the model.
4. **`evaluate.py`**: Validates prediction performance using robust metrics (RMSE, MAE, R², and $\pm$1-mark accuracy) against a held-out test split of unseen questions.

---

## 2. Dataset & Target Normalization

- **Source Dataset**: Mohler ASAG dataset (`dataset/external/mohler_asag.csv`), consisting of 2,442 short answers graded by human computer science instructors.
- **Target Normalization**: Rather than predicting raw points directly (since questions have different maximum scales like 2, 5, or 10 marks), the target variable is normalized as a percentage ($0.0$ to $1.0$):
$$\text{mark\_percentage} = \frac{\text{Human Awarded Mark}}{\text{Max Marks}}$$
During inference, this percentage is scaled up to the question's specific maximum marks and rounded to the nearest half-mark ($0.5$).

---

## 3. Feature Engineering (`features.py`)

To convert raw textual answers into numerical inputs, `features.py` extracts **5 core metrics** comparing the student's answer to the official key:

| Feature Name | Type | Description |
| :--- | :--- | :--- |
| **`similarity`** | `float` | Cosine similarity computed over semantic dense embeddings generated using the `all-MiniLM-L6-v2` transformer model. |
| **`keyword_recall`** | `float` | The fraction of non-stopwords in the answer key that appear in the student's answer: $\frac{|\text{Student} \cap \text{Key}|}{|\text{Key}|}$. |
| **`word_overlap`** | `float` | Jaccard similarity coefficient representing word intersection over union: $\frac{|\text{Student} \cap \text{Key}|}{|\text{Student} \cup \text{Key}|}$. |
| **`length_ratio`** | `float` | Ratio of student answer word count to expected answer word count, capped at $3.0$. |
| **`negation_flag`** | `int` | Binary flag ($1$ if present, $0$ otherwise) indicating whether negation tokens (e.g. *not, never, don't, doesn't, cannot*) appear in the student answer. Prevents awarding high marks to statement contradictions. |

---

## 4. Validation & Training Strategy

- **Algorithm**: **XGBoost Regressor** (`XGBRegressor`). tabular gradient boosted decision trees excel on small, structured numeric datasets and avoid the high overhead of deep networks.
- **GroupKFold Validation**: Splitting is grouped by `question_id` (5 splits). This guarantees that during validation, entire questions (along with their associated student answers) are hidden from the training partition. The model is tested exclusively on questions it has never seen, verifying true generalization to new exam criteria.
- **Hyperparameter Grid Search**: Tunes combinations of:
  - `n_estimators`: `[200, 400]`
  - `max_depth`: `[3, 4]`
  - `learning_rate`: `[0.03, 0.05]`

---

## 5. Execution Commands

From the `backend/` directory, activate your virtual environment:

### Step 1: Run Training Pipeline
Trains the XGBoost regressor, runs cross-validation, saves the serialized model, and logs performance metrics.
```bash
PYTHONPATH=. python -m app.training.trainer
```

**Artifacts Generated:**
- **Model Binary**: `models_cache/mark_predictor.pkl` (contains the trained XGBoost model, feature list, and hyperparameters).
- **Performance Logs**: `dataset/processed/model_b_metrics.json` (stores RMSE, MAE, R², and feature importances).

### Step 2: View Training Metrics
Prints serialized metrics output such as training split counts, cross-validation root-mean-squared error, and feature importances.
```bash
PYTHONPATH=. python -c "import json; print(json.dumps(json.load(open('../dataset/processed/model_b_metrics.json')), indent=2))"
```

