# Machine Learning Model Development (Phase 1)

To develop the core Machine Learning model (the **Mark-Predictor**), we engineered a complete Phase 1 Training pipeline. Since Track 02 prohibits just asking an LLM to assign a grade, we built a classic, highly-optimized Supervised Machine Learning pipeline using **XGBoost**.

Here is the step-by-step breakdown of exactly how it was developed (handled by the code in `backend/app/training/`):

### 1. Data Structuring (The Target)
We start with a historical dataset containing the student's answer, the official answer key, and the **actual mark awarded by a human teacher**. 
Instead of predicting raw marks (which change depending on if a question is worth 2, 5, or 10 marks), we normalize the teacher's mark into a **percentage (0.0 to 1.0)**. This allows the model to learn a universal grading scale.

### 2. Feature Engineering (The Inputs)
Machine learning models need numbers, not raw text. In `features.py`, we take every `(Student Answer, Answer Key)` pair and extract **five critical numeric features** that mimic what a teacher looks for:
1.  **Semantic Similarity:** We use the `all-MiniLM-L6-v2` NLP model to convert both answers into dense vectors and compute their Cosine Similarity. This captures the *meaning* (e.g., recognizing that "creates power" is similar to "generates energy").
2.  **Keyword Recall:** The percentage of important vocabulary words from the answer key that the student successfully included.
3.  **Word Overlap:** A mathematical intersection (Jaccard similarity) of the words used.
4.  **Length Ratio:** How long the student's answer is compared to the expected answer.
5.  **Negation Flag:** A binary flag (0 or 1) that triggers if the student uses words like *not, never, cannot, doesn't*. This prevents a student from getting a high similarity score if they write the exact opposite of the correct answer (e.g., "is *not* exothermic").

### 3. Model Training (XGBoost Regressor)
In `trainer.py`, we pass this massive table of 5 features + the teacher's mark percentage into an **XGBoost Regressor** (`XGBRegressor`). 
*   **Why XGBoost?** It is incredibly fast, handles this kind of tabular numerical data better than Deep Learning, and natively provides "Feature Importance" metrics (which is highly favorable for the hackathon judging criteria).

### 4. Hyperparameter Tuning & GroupKFold Validation
We don't just train the model blindly. We use **GroupKFold cross-validation (5 splits)** grouped by `question_id`. 
*   This is a crucial academic ML technique: it hides entire questions from the model during training. When the model is tested, it is forced to grade *questions it has never seen before*. This guarantees the model is actually learning the *rules of grading* rather than just memorizing specific answer keys.
*   We run a Grid Search over parameters like `n_estimators` (200, 400), `max_depth` (3, 4), and `learning_rate` to find the exact combination that produces the lowest Error (RMSE) against the human teachers.

### 5. Final Export (The `.pkl` file)
Once the optimal parameters are found, we train the final model on the entire dataset and export it as `models_cache/mark_predictor.pkl` using `joblib`. 

In Phase 2 (Live Evaluation), when a new student uploads a paper, the FastAPI backend simply loads this `.pkl` file, extracts those same 5 features from the fresh OCR text, and asks the XGBoost model to predict the final mark percentage in milliseconds.
