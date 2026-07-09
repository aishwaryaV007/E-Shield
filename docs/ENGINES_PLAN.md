# Verification Engines Development Plan
> Development steps, tasks, algorithm configurations, and testing timelines for the five core evaluation engines.

*Design / Planned — Not yet implemented*

---

## 1. Development Focus

The **Verification Engines** analyze digitized data structures from the OCR pipeline to flag discrepancies and collusion networks.

```
                         ┌────────────────────────────────┐
                         │      Core OCR Output Data      │
                         └───────────────┬────────────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 │                       │                       │
      ┌──────────▼──────────┐ ┌──────────▼──────────┐ ┌──────────▼──────────┐
      │ Task 1: MarkSafe    │ │ Task 2: CopyCatch   │ │ Task 3: ScriptID    │
      │ Grader sum check    │ │ Embedding matrix    │ │ ID register match   │
      └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                 │                       │                       │
                 └───────────────┬───────┴───────────────┬───────┘
                                 │                       │
                      ┌──────────▼──────────┐ ┌──────────▼──────────┐
                      │ Task 4: ReEval Guard│ │ Task 5: RubricLens  │
                      │ Borderline sorting  │ │ Semantic highlights │
                      └─────────────────────┘ └─────────────────────┘
```

---

## 2. Technical Task Breakdown

### Task 1: MarkSafe Sum Engine (`app/engines/marksafe.py`)
*   **Objectives:** Verify individual page score calculations against the overall written totals.
*   **Implementation Steps:**
    1.  Parse numeric grid values using fraction and addition regex patterns.
    2.  Sum the question scores on a script and compare the sum against the extracted total.
    3.  Flag arithmetic discrepancies as `SUM_MISMATCH`.

### Task 2: CopyCatch Collusion Engine (`app/engines/copycatch.py`)
*   **Objectives:** Identify student copying networks using semantic similarity.
*   **Implementation Steps:**
    1.  Integrate local sentence-transformer models (`all-MiniLM-L6-v2`) to vectorize text.
    2.  Calculate pairwise cosine similarity matrices using optimized NumPy tensor operations.
    3.  Apply z-score calculations to normalize similarity scores against the class baseline.
    4.  Generate interactive community cluster graphs using NetworkX and PyVis.

### Task 3: ScriptID Roster Matcher (`app/engines/scriptid.py`)
*   **Objectives:** Validate student identity details and flag roster discrepancies.
*   **Implementation Steps:**
    1.  Load the roster CSV using pandas.
    2.  Crosscheck OCR-extracted roll numbers against the roster database.
    3.  Flag duplicated roll numbers, missing IDs, or registration discrepancies.

### Task 4: ReEval Guard Sort (`app/engines/reeval_guard.py`)
*   **Objectives:** Identify and prioritize scripts with borderline passing scores or grade boundaries.
*   **Implementation Steps:**
    1.  Parse final script scores from MarkSafe.
    2.  Compare scores against grade boundaries in the configuration.
    3.  Add scripts falling within the borderline margin (e.g., 39/40) to the priority review queue.

### Task 5: RubricLens Cross-Encoder (`app/engines/rubriclens.py`)
*   **Objectives:** Align extracted student answers with grading rubric targets.
*   **Implementation Steps:**
    1.  Set up local NLI cross-encoder models (`nli-deberta-v3-xsmall`).
    2.  Classify student sentences against rubric guidelines into `Entailment`, `Contradiction`, or `Neutral`.
    3.  Write classification states to SQLite to display color-coded highlights in the dashboard.

---

## 3. Related Documents

*   [Engines Module specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/app/engines/README.md)
*   [CopyCatch Detailed Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [MarkSafe Detailed Design](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/MARKSAFE.md)
