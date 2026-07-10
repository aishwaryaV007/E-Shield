# 1. FILE PURPOSE: Marks backend/app as the root Python package for the E-Shield backend.
# 2. RESPONSIBILITIES: expose the `app` package; set process-wide env before ML libs load.
# 3. DEPENDS ON / USED BY: imported by all backend submodules and the test suite.
import os

# torch and xgboost both bundle libomp; on macOS the duplicate load segfaults.
# Allow it (safe here — single-process inference) before either library imports.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
os.environ.setdefault("OMP_NUM_THREADS", "1")
