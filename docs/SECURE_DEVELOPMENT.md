# Secure Development Guidelines
> Codebase audit practices, input validation standards, static analysis, and comments preservation.

*Design / Planned — Not yet implemented*

---

## 1. Development Principles

Developers working on ExamShield must follow these **Secure Development Principles** to maintain database stability and prevent data leaks:

1.  **Local Isolation:** Do not implement features that upload data to external cloud servers.
2.  **No Automatic Decision-Making:** Keep the user in control. Highlight discrepancies and display flags, but leave all grading changes and cheating decisions to the human auditor.
3.  **Strict OCR Fallbacks:** Ambiguous characters, crossed-out numbers, and low-confidence OCR predictions must fail safely, flagging the script as `AMBIGUOUS_MARK` and routing it to the manual override queue.

---

## 2. Secure Coding Standards

### Input Validation
All parameters passed to core python functions must be validated:
*   Use Pydantic models for REST endpoints.
*   Enforce numeric limits (e.g., checking that marks are positive values and coordinate crops fall within the page's boundaries).

### SQL Injection Prevention
All SQLite interactions must use parameterized queries:
*   Avoid using string formatting (`f"SELECT ... WHERE id = '{id}'"`) to construct SQL queries.
*   Use standard SQL parameter syntax (`"SELECT ... WHERE id = ?"`, `(id,)`) to protect against injection vulnerabilities.

### Preserving Comments and Documentation
*   Developers must preserve inline comments that document calibration rules and OCR threshold settings.
*   Ensure that all functions are documented with clear docstrings explaining input arguments, return types, and validation logic.

---

## 3. Pre-Commit Checklist

Before merging new code into the main branch:
*   [ ] Run `black` to check code formatting.
*   [ ] Run `flake8` to audit syntax errors and potential bugs.
*   [ ] Run `pytest` to verify that all unit and integration tests pass.
*   [ ] Run `pip-audit` to scan for vulnerabilities in local package dependencies.

---

## 4. Related Documents

*   [Overall README](file:///Users/gaurav/Desktop/MyProjects/E-Shield/README.md)
*   [Backend Security Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/BACKEND_SECURITY.md)
*   [DevOps Deployment Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DEVOPS_PLAN.md)
