# Backend Process Security
> Local sandbox guidelines, process isolation, third-party dependency rules, and database file protection.

*Design / Planned — Not yet implemented*

---

## 1. Backend Security Framework

Because ExamShield runs locally, its security model focuses on securing the **Local Python Sandbox** and preventing malicious input files (e.g., corrupted PDFs or images) from causing system failures or unauthorized folder writes.

```
┌────────────────────────────────────────────────────────┐
│ Client Desktop PC (Local Host OS)                      │
├────────────────────────────────────────────────────────┤
│  [ Uploaded Files ]                                    │
│        │                                               │
│        ▼ (Sanitize File Extensions & MIME Types)       │
│  [ Ingestion Subsystem Sandbox ]                       │
│        │                                               │
│        ▼ (Restricted file writes)                      │
│  [ Local storage Folder / SQLite DB ]                  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Backend Security Guidelines

### 1. Upload Sanitization & Mime Filters
*   The upload engine validates file extensions, accepting only `.pdf`, `.png`, `.jpg`, and `.jpeg`.
*   File headers are checked to confirm that uploaded files match supported image and PDF signatures, protecting the binarization engine from executing malicious payloads.

### 2. Sandbox Write Restrictions
*   All file write operations are restricted to the local workspace folder `/data/`.
*   Files are written using sanitized, system-generated UUID filenames rather than the original uploaded filenames, preventing directory traversal vulnerabilities.

### 3. Dependency Verification
*   All third-party library dependencies (e.g., `opencv-python`, `paddleocr`, `sentence-transformers`) are locked to specific versions in `requirements.txt`.
*   Regular dependency audits (`pip-audit`) are performed to identify and address known vulnerabilities in ML packaging modules before deployment.

---

## 3. Related Documents

*   [API Security Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_SECURITY.md)
*   [Database Concepts Reference](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DBMS_CONCEPTS.md)
*   [Secure Development Guidelines](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SECURE_DEVELOPMENT.md)
