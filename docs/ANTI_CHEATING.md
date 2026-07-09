# Post-Exam Collusion Analysis
> Specifications for post-hoc copying detection, seating chart correlation, and the "Human Decides" verification rule.

*Design / Planned — Not yet implemented*

---

## 1. Post-Exam Integrity Approach

ExamShield does not track live students or monitor exam rooms during test execution. Instead, it uses **Post-Exam Collusion Analysis** to audit physical scripts after they are submitted.

```
                  ┌──────────────────────────────┐
                  │ Batch of physical booklets   │
                  └──────────────┬───────────────┘
                                 │
                  ┌──────────────▼───────────────┐
                  │ Prose OCR & Vector Embeds    │
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
        [ Path A: Similarity ]         [ Path B: Seating Map ]
        • Pairwise Cosine              • seat coords register
        • Class average z-score        • distance weights
                 │                               │
                 ▼                               ▼
        [ Graph Link: Final Weight = Z-score * Proximity ]
                                 │
                                 ▼
        [ Visual Evidence Crops -> Human Decides ]
```

---

## 2. CopyCatch & Seating Chart Correlation

Copying between students usually occurs when they are seated close to each other in the exam hall. To identify these links, CopyCatch combines text similarity scores with physical seating coordinates:

1.  **Extract Similarity:** The system calculates the z-score similarity metric $Z_{A,B}$ between two student answers, highlighting pairs with similarity that deviates from the class average.
2.  **Lookup Seating Distance:** The system looks up student seating locations in the exam register:
    $$\text{Distance} = \sqrt{(X_A - X_B)^2 + (Y_A - Y_B)^2}$$
3.  **Adjust Weighting:** The system adjusts the collusion connection weight based on seating proximity:
    $$\text{Final Weight} = Z_{A,B} \times (1.0 + \frac{1}{\text{Distance}})$$
    
This increases the weight of links between students seated next to each other, highlighting likely copying pairs while ignoring high similarity scores between students seated far apart (which are more likely to be coincidental similarities).

---

## 3. The "Human Decides" Rule

The system never accuses students of cheating. The output is framed as a **Ranked Similarity Link** rather than a final verdict:

*   **No Auto-Accusations:** The dashboard highlights pairs with high similarity scores as *"Anomalous similarity detected — Review seating map and handwriting"* instead of *"Cheating detected"*.
*   **Graders Confirm Copying:** Graders can click on a link in the collusion graph to display the two student booklets side-by-side. The human grader makes the final decision on whether copying occurred based on handwriting style, crossed-out errors, and prose alignment.

---

## 4. Related Documents

*   [CopyCatch Detailed Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/engines/COPYCATCH.md)
*   [Exam Integrity Framework](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/EXAM_INTEGRITY.md)
*   [Product Features List](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/FEATURES.md)
