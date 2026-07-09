# CopyCatch Collusion Engine
> Technical design for prose OCR similarity checks, local vector embeddings, anomaly normalizing, and PyVis graph visualizations.

*Design / Planned — Not yet implemented*

---

## 1. Algorithmic Overview

**CopyCatch** maps collusion networks across handwritten paper submissions. Because human evaluators review pages sequentially, they cannot easily catch student copying networks in large cohorts. CopyCatch automates this audit through local vector modeling:

```mermaid
graph TD
    A[Raw Page Prose Crops] --> B[Tier-2 Prose OCR with Confidence Filter]
    B --> C[Vectorize via local all-MiniLM-L6-v2 Embeddings]
    C --> D[Compute O(N^2) Pairwise Cosine Similarity Matrix]
    D --> E[Normalize scores via class-baseline Anomaly Ranking]
    E --> F[Generate NetworkX Clusters & PyVis HTML Node Graph]
```

---

## 2. Mathematical Modeling & Anomaly Normalizing

To prevent false alarms from common answers (e.g., standard definitions, slide formulas, or copy-pasted questions), CopyCatch applies **Class-Baseline Anomaly Ranking**:

$$\text{Cosine Similarity}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$

If students $A$ and $B$ write a similar answer, the raw cosine similarity score might be high. However, if the entire class scored high similarity due to copying a textbook definition, this is normal class-wide behavior.

To isolate true collusion, the system normalizes similarity metrics against the class baseline using a z-score calculation:

$$Z_{A,B} = \frac{\text{Similarity}(A,B) - \mu_{\text{class}}}{\sigma_{\text{class}}}$$

*   $\mu_{\text{class}}$: Mean similarity score of all student pairs for a question.
*   $\sigma_{\text{class}}$: Standard deviation of similarity scores across the cohort.

An anomaly flag is raised only if the z-score $Z_{A,B}$ exceeds the threshold (e.g., $Z > 3.0$), indicating similarity that deviates significantly from class-wide patterns.

---

## 3. Pairing Engine & Seating Integration (`copycatch.py`)

The pairing calculations combine text similarity metrics with physical exam seating registers:

```python
# Planned implementation pattern
import numpy as np
import networkx as nx

def build_collusion_network(similarity_matrix: np.ndarray, student_ids: list[str], threshold: float = 3.0) -> nx.Graph:
    G = nx.Graph()
    n = len(student_ids)
    
    # Calculate global mean and standard deviation
    triu_indices = np.triu_indices(n, k=1)
    flat_similarities = similarity_matrix[triu_indices]
    
    mean_sim = np.mean(flat_similarities)
    std_sim = np.std(flat_similarities) if np.std(flat_similarities) > 0 else 1.0
    
    # Populate the collusion graph
    for i in range(n):
        for j in range(i + 1, n):
            score = similarity_matrix[i, j]
            z_score = (score - mean_sim) / std_sim
            
            # Link nodes if similarity deviates from class baseline
            if z_score >= threshold:
                G.add_edge(
                    student_ids[i], 
                    student_ids[j], 
                    weight=float(score), 
                    z_score=float(z_score)
                )
    return G
```

### Seating Weights
If exam seating chart data is available, the connection edges are weighted based on distance:
$$\text{Weight}_{\text{final}} = Z_{A,B} \times (1.0 + \text{Seating\_Proximity}(A, B))$$

---

## 4. PyVis Node Graph Visualization

Linked student pairs are rendered in the dashboard as an interactive force-directed graph. 
*   **Nodes:** Represent individual students (clicking a node highlights their seat on the seating chart).
*   **Edges:** Thickness indicates similarity. Clicking an edge opens a side-by-side view comparing original page crops of the two scripts.

---

## 5. Related Documents

*   [System Design Specifications](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SYSTEM_DESIGN.md)
*   [Local Performance & Scalability Specs](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/SCALABILITY.md)
*   [Engines Implementation Plans](file:///Users/gaurav/Desktop/MyProjects/E-Shield/docs/ENGINES_PLAN.md)
