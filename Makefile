# Architected AI Starter — standard developer entry points.
.DEFAULT_GOAL := help
SHELL := /bin/bash

UV ?= uv
COMPOSE ?= docker compose
WEB_DIR := apps/web
PY_SOURCES := packages scripts apps/api/src apps/agent-gateway/src

.PHONY: help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install Python workspace and frontend dependencies
	$(UV) sync
	cd $(WEB_DIR) && npm install

.PHONY: env
env: ## Create .env from .env.example if missing
	@test -f .env || (cp .env.example .env && echo "Created .env")

.PHONY: lint
lint: ## Lint Python
	$(UV) run ruff check .
	$(UV) run ruff format --check .

.PHONY: format
format: ## Auto-format Python
	$(UV) run ruff format .
	$(UV) run ruff check --fix .

.PHONY: typecheck
typecheck: ## Strict type checking
	$(UV) run mypy $(PY_SOURCES)
	$(UV) run mypy --platform linux $(PY_SOURCES)

.PHONY: test
test: ## Unit + architecture tests only
	$(UV) run pytest -m "not integration and not e2e"

.PHONY: test-integration
test-integration: ## Infrastructure-backed integration tests
	$(UV) run pytest -m integration

.PHONY: test-e2e
test-e2e: ## Full-stack tests
	$(UV) run pytest -m e2e

.PHONY: check
check: lint typecheck test ## Python quality gate

.PHONY: web-check
web-check: ## Frontend typecheck + lint + build
	cd $(WEB_DIR) && npm run typecheck && npm run lint && npm run build

.PHONY: up
up: env ## Start the local stack
	$(COMPOSE) up -d --build
	@echo "API:       http://localhost:8000"
	@echo "Gateway:   http://localhost:8100"
	@echo "Web:       http://localhost:3000"
	@echo "Couchbase: http://localhost:8091"

.PHONY: down
down: ## Stop local stack, preserving data
	$(COMPOSE) down

.PHONY: clean
clean: ## Stop local stack and delete volumes
	$(COMPOSE) down -v

.PHONY: logs
logs: ## Follow application logs
	$(COMPOSE) logs -f api agent-gateway web

.PHONY: repo-check
repo-check: ## Validate project-template conventions
	$(UV) run python scripts/check_project.py

.PHONY: security
security: ## Run local security checks when tools are available
	@command -v gitleaks >/dev/null && gitleaks detect --source . || echo "gitleaks not installed; CI runs it"
	$(UV) export --no-emit-workspace --format requirements-txt --no-hashes -o requirements.audit.txt
	$(UV) run --with pip-audit pip-audit --requirement requirements.audit.txt --desc
	cd $(WEB_DIR) && npm audit --audit-level=high
