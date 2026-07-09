.PHONY: install dev-backend dev-frontend test lint clean

# ── Installation ─────────────────────────────────────────────────────────────
install: install-backend install-frontend

install-backend:
	@echo "→ Installing backend Python dependencies..."
	cd backend && python -m venv ../.venv && \
		../.venv/bin/pip install --upgrade pip && \
		../.venv/bin/pip install -r requirements.txt -r requirements-dev.txt

install-frontend:
	@echo "→ Installing frontend Node dependencies..."
	cd frontend && npm install

# ── Development servers ──────────────────────────────────────────────────────
dev-backend:
	@echo "→ Starting FastAPI backend on http://127.0.0.1:8000 ..."
	cd backend && ../.venv/bin/uvicorn main:app --reload --host 127.0.0.1 --port 8000

dev-frontend:
	@echo "→ Starting Next.js frontend on http://localhost:3000 ..."
	cd frontend && npm run dev

dev:
	@echo "→ Starting both services (requires tmux or two terminals)..."
	@echo "   Run 'make dev-backend' and 'make dev-frontend' in separate terminals."

# ── Testing ──────────────────────────────────────────────────────────────────
test:
	@echo "→ Running backend test suite..."
	cd backend && ../.venv/bin/pytest ../tests/ -v

test-frontend:
	@echo "→ Running frontend type-check..."
	cd frontend && npx tsc --noEmit

# ── Linting / formatting ─────────────────────────────────────────────────────
lint: lint-backend lint-frontend

lint-backend:
	@echo "→ Linting Python (ruff + black check)..."
	cd backend && ../.venv/bin/ruff check . && ../.venv/bin/black --check .

lint-frontend:
	@echo "→ Linting TypeScript (ESLint)..."
	cd frontend && npm run lint

format:
	cd backend && ../.venv/bin/black . && ../.venv/bin/ruff check --fix .

# ── Model caching ────────────────────────────────────────────────────────────
download-models:
	@echo "→ Pre-downloading ML model weights to models_cache/ ..."
	.venv/bin/python scripts/download_models.py

# ── Demo data ────────────────────────────────────────────────────────────────
seed-demo:
	@echo "→ Seeding demo data into data/ ..."
	.venv/bin/python scripts/seed_demo_data.py

# ── Cleanup ──────────────────────────────────────────────────────────────────
clean:
	@echo "→ Cleaning build artefacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd frontend && rm -rf .next out node_modules 2>/dev/null || true
