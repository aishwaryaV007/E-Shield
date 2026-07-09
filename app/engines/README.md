# ExamShield Verification Engines Module
> Overview of the five core analysis engines that evaluate OCR outputs and raise validation flags.

*Design / Planned — Not yet implemented*

---

## 1. Engine Architecture

The `app/engines/` folder contains the core logic of ExamShield. After images are deskewed and text is digitized by the OCR module, these five engines analyze the data.

```
                         ┌────────────────────────────────┐
                         │   Digit & Prose OCR Results    │
                         └───────────────┬────────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
      ┌──────────▼─────────┐ ┌───────────▼──────────┐ ┌──────────▼─────────┐
      │  MARKSAFE ENGINE   │ │   COPYCATCH ENGINE   │ │  SCRIPTID ENGINE   │
      │ Verify page sums   │ │ Pairwise similarity  │ │ Cross-check roster │
      │ vs written totals  │ │ & network clusters   │ │ duplicates/absent  │
      └──────────┬─────────┘ └───────────┬──────────┘ └──────────┬─────────┘
                 │                       │                       │
                 └───────────────┬───────┴───────────────┬───────┘
                                 │                       │
                      ┌──────────▼─────────┐   ┌─────────▼─────────┐
                      │ REEVAL GUARD ENGINE│   │ RUBRICLENS ENGINE │
                      │ Borderline score   │   │ Match student text│
                      │ priority review    │   │ to grading rubric │
                      └──────────┬─────────┘   └─────────┬─────────┘
                                 │                       │
                                 └───────────┬───────────┘
                                             │
                                  ┌──────────▼──────────┐
                                  │   SQLite / JSON     │
                                  │   Audit Database    │
                                  └─────────────────────┘
```

---

## 2. Verification Engines Matrix

| Engine | Inputs | Algorithmic Approach | Outputs & Flags |
| :--- | :--- | :--- | :--- |
| **MarkSafe** | Digit crops (marks column & totals). | Regular expression validation & mathematical summation. | `SUM_MISMATCH`, `PAGE_MISSING_GRADE`, `AMBIGUOUS_MARK`. |
| **CopyCatch** | Prose OCR texts. | Cosine similarity matrices & NetworkX community clustering. | `SIMILARITY_CLUSTER`, `HIGHEST_SIMILARITY_PAIRS`. |
| **ScriptID** | Roll number digit crops & register CSV. | pandas dictionary lookups & key validation. | `DUPLICATE_ID`, `UNREGISTERED_ID`, `ABSENTEE_WITH_SCRIPT`. |
| **ReEval Guard** | MarkSafe outputs. | Threshold comparison filters. | `BORDERLINE_FAIL`, `BORDERLINE_GRADE_CUTOFF`. |
| **RubricLens** | Prose OCR texts & rubric schemas. | Semantic search + DeBERTa NLI categorization. | `RUBRIC_ENTAILED` (green), `RUBRIC_CONTRADICTED` (red). |

---

## 3. Local Library Policies

To maintain the system's offline functionality and execution speed during hackathons and local college deployments, engines must strictly adhere to local compute constraints:

*   **MiniLM Embeddings (`copycatch.py`):** Uses Hugging Face's local sentence-transformer loader. Downloads are cached locally (`HF_HOME`).
*   **Graph Computing (`copycatch.py`):** Graph computation runs locally in NetworkX. Graph exports compile into standard interactive JavaScript templates served by Python.
*   **Database Writes:** Results are queued and committed to a local SQLite schema via transactional connections in a thread-safe wrapper.

---

## 4. Related Documents

*   [MarkSafe Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/MARKSAFE.md)
*   [CopyCatch Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [ScriptID Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/SCRIPTID.md)
*   [ReEval Guard Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/REEVAL_GUARD.md)
*   [RubricLens Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/RUBRICLENS.md)
