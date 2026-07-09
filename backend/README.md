# Backend Application

## Setup & Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Module Map
- `app/api`: HTTP routes.
- `app/pipeline`: End-to-end orchestration.
- `app/engines`: Core AI verification logic.
- `app/ocr` & `app/ingestion`: Data extraction.
- `app/services`: Business logic.
- `app/storage`: SQLite & JSON persistence.
