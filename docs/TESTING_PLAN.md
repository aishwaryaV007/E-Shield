# ExamShield Testing Specification
> Test architecture, mock registry configurations, integration validations, and demo runner setups.

*Design / Planned — Not yet implemented*

---

## 1. Test Architecture

The testing framework uses `pytest` to run automated unit checks on pre-processing pipelines, math summation parsers, and registry matching functions:

```
┌────────────────────────────────────────────────────────┐
│ PyTest Test Runner                                     │
└───────────────────────┬────────────────────────────────┘
                        │
         ┌──────────────┼────────────────────────┐
         ▼              ▼                        ▼
   [ Unit Tests ] [ Integration Tests ]    [ Demo Validation ]
   • preprocess   • Ingestion -> SQLite    • Run on 35 scripts
   • regex sum    • End-to-end flow        • Check planted flags
   • CSV roster   • Thread pool locks      • Render local HTML
```

---

## 2. Test Suites Breakdown

### 1. Subsystem Unit Tests (`tests/unit/`)
*   `test_preprocess.py`: Verifies OpenCV binarization and deskewing functions on synthetic skewed images.
*   `test_marksafe_math.py`: Checks regex parsing of digits, fractions, addition formulas, and strikeouts.
*   `test_roster_matcher.py`: Validates ScriptID enrollment matching and duplicate flag generation.

### 2. Integration Pipelines Verification (`tests/integration/`)
*   `test_pipeline_flow.py`: Verifies the end-to-end processing pipeline, checking data flow from raw scanned PDFs to SQLite DB records.
*   `test_concurrent_writes.py`: Checks SQLite WAL settings and lock timeout behaviors under concurrent write loads from multiple threads.

### 3. Demo Validation Runner (`app/test_runner.py`)
Runs automated integration checks on a mock dataset before live demonstrations:
*   **Verification Dataset:** A test batch of **35 scanned scripts** containing planted errors (2 copying student pairs, 3 arithmetic summation discrepancies, 1 registration error).
*   **Success Verification Rules:**
    ```python
    # Planned implementation pattern
    def verify_mock_batch_results(batch_id: str):
        # Query results from local SQLite DB
        mismatches = query_db("SELECT count(*) FROM audit_flags WHERE flag_type='SUM_MISMATCH'")
        duplicates = query_db("SELECT count(*) FROM audit_flags WHERE flag_type='DUPLICATE_ID'")
        collusions = query_db("SELECT count(*) FROM similarity_matrix WHERE similarity_score > 0.85")
        
        # Verify that all planted errors are detected
        assert mismatches == 3, f"Expected 3 arithmetic errors, found {mismatches}"
        assert duplicates == 1, f"Expected 1 duplicate ID error, found {duplicates}"
        assert collusions >= 2, f"Expected at least 2 collusion pairs, found {collusions}"
        print("Integration test passed: all planted errors successfully detected!")
    ```

---

## 3. Related Documents

*   [Overall Implementation Plan](file:///Users/gaurav/Desktop/MyProjects/E-Shield/implementation_plan.md)
*   [Local Storage specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/storage/README.md)
*   [Database Concepts Reference](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/DBMS_CONCEPTS.md)
