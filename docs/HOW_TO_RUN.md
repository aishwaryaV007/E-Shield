# Application Execution Guide
> Step-by-step execution scripts, model downloads, configuration checks, and verification runs.

*Design / Planned — Not yet implemented*

---

## 1. Installation

To set up ExamShield in local environments:

```bash
# 1. Clone the repository and navigate to the project root
git clone https://github.com/aishwaryaV007/E-Shield.git
cd E-Shield

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install required dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 2. Caching AI Model Weights

Download and cache model weights before running in restricted, offline environments:

```bash
python scripts/cache_models.py
```

This caches `PaddleOCR` models, `all-MiniLM-L6-v2` embeddings, and `nli-deberta-v3-xsmall` weights in local system folders (`~/.cache/`), preparing the system for offline use.

---

## 3. Starting the Services

Startup requires launching both the FastAPI backend and the Streamlit frontend.

### 1. Launch FastAPI Backend
```bash
# Start backend on default port 8000
uvicorn app.api:app --reload --port 8000
```
Confirm the backend is running by opening the Swagger UI at `http://127.0.0.1:8000/docs` in your browser.

### 2. Launch Streamlit UI Dashboard
Open a separate terminal window, activate the virtual environment, and run:
```bash
streamlit run app/dashboard/main.py
```
This starts the dashboard at `http://localhost:8501`.

---

## 4. Verification Check Run

Run the integration test script to verify pipeline functions using the mock dataset:

```bash
python app/test_runner.py
```
This processes the mock 35-script corpus, validates extracted scores, and checks that all planted flags are successfully raised.

---

## 5. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Local DevOps & Startup Scripts](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DEVOPS_PLAN.md)
*   [Testing & Verification Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TESTING_PLAN.md)
