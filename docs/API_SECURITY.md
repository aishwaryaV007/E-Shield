# API Security & Loopback Bounds
> API security guidelines, local loopback bindings, input validation, and parameter sanitization rules.

*Design / Planned — Not yet implemented*

---

## 1. Local Network Isolation

Although ExamShield runs locally, the FastAPI backend must be secured to prevent unauthorized access from other devices on the same local network (e.g., college Wi-Fi).

```
[ Local Streamlit Dashboard UI ]
        │
        ▼ (Restricted loopback connection: localhost / 127.0.0.1)
[ Local FastAPI server (port 8000) ]
        ▲
        ✕ (BLOCKED: External requests from other network devices)
```

### Loopback Binding Rules
The FastAPI server must be bound to the local loopback address (`127.0.0.1` or `localhost`) rather than the public interface (`0.0.0.0`):

```python
# Planned server configuration
if __name__ == "__main__":
    import uvicorn
    # Bind to 127.0.0.1 to restrict access to local processes
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000)
```

This prevents other computers on the same network from accessing the API endpoints or querying the local database.

---

## 2. Input Validation & Parameter Sanitization

To protect the local database from injection attacks and ensure stable file processing:

*   **Pydantic Input Validation:** All API inputs use Pydantic schemas to validate data types (e.g., checking that `resolved_value` is a float and coordinates are integers).
*   **File Path Sanitization:** The file upload handler strips directory traversal characters (e.g., `../`, `..\\`) from filenames, preventing files from being written outside the target `/data/corpus/` directory.
*   **SQL Parameterization:** SQLite queries use parameterized placeholders (`?`) to prevent SQL injection vulnerabilities.

---

## 3. Related Documents

*   [API Specifications Guide](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/API_CONTRACT.md)
*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Backend Security Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/BACKEND_SECURITY.md)
