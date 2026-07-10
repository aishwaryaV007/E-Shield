# Local DevOps & Packaging Plan
> Offline deployment setups, local python environments, model weights caching, and application execution scripts.

*Design / Planned — Not yet implemented*

---

## 1. Local Deployment Target

ExamShield is designed to run locally on target client machines (e.g., examination cell computers). It avoids standard cloud services, container registries (like Docker), or remote hosting configurations.

```
┌────────────────────────────────────────────────────────┐
│ Client Desktop PC (Windows / macOS / Linux)            │
├────────────────────────────────────────────────────────┤
│ • Local Python 3.11 Environment                        │
│ • Local cached Model Weights (~180MB)                  │
│ • SQLite Database File (db.sqlite3)                    │
│ • Local media folder (/data/corpus/)                   │
└────────────────────────────────────────────────────────┘
```

---

## 2. Packaging & Environment Automation

### Scripted Installer (`install.sh` / `install.bat`)
To simplify deployment in offline environments, the installation script automates virtual environment setup and packages dependencies:

```bash
#!/bin/bash
# install.sh - Offline installer script for Unix-like environments

set -e

echo "Initializing virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip --no-index --find-links=./wheels/

echo "Installing required Python dependencies..."
# Installs dependencies using local wheel packages in offline environments
pip install -r requirements.txt --no-index --find-links=./wheels/

echo "Caching ML model weights (OCR + embedder; no LLM)..."
python3 scripts/download_models.py

echo "Installation complete! Run './start.sh' to launch ExamShield."
```

### Dependency Packaging
For installations on computers without internet access, dependencies are downloaded as wheel files on an online machine and transferred via USB drive:
```bash
pip download -r requirements.txt -d ./wheels/
```

---

## 3. Execution Coordinator Script (`start.sh`)

A single startup script launches the FastAPI backend and the Next.js dashboard:

```bash
#!/bin/bash
# start.sh - Launch the application stack

echo "Starting FastAPI backend on port 8000..."
(cd backend && source .venv/bin/activate && uvicorn main:app --host 127.0.0.1 --port 8000) &
API_PID=$!

echo "Starting Next.js dashboard on port 3000..."
(cd frontend && npm run start) &
UI_PID=$!

# Clean up on exit
trap "kill $API_PID $UI_PID" EXIT
wait
```

---

## 4. Related Documents

*   [Technology Stack Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/TECH_STACK.md)
*   [Database Specification](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Monitoring and Run Logs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/MONITORING.md)
```
