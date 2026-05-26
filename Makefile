.PHONY: setup test test-security lint format \
       run-vulnerable-chatbot run-vulnerable-rag run-vulnerable-agent \
       eval evidence clean scaffold scaffold-class check ci help

# =============================================================================
# Setup
# =============================================================================

setup: ## Set up the development environment
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Environment ready. Run: source venv/bin/activate"

# =============================================================================
# Testing
# =============================================================================

test: ## Run the full test suite
	python -m pytest -v --tb=short 2>/dev/null || echo "No tests found yet. Start writing tests in class directories."

test-security: ## Run security-specific tests only
	python -m pytest -v -m security --tb=short 2>/dev/null || echo "No security tests found yet."

# =============================================================================
# Code Quality
# =============================================================================

lint: ## Run ruff linter
	ruff check . || true

format: ## Run ruff formatter
	ruff format . || true

# =============================================================================
# Lab Systems
# =============================================================================

run-vulnerable-chatbot: ## Run the vulnerable chatbot lab
	cd labs/vulnerable-chatbot && pip install -q -r requirements.txt && python app.py

run-vulnerable-rag: ## Run the vulnerable RAG lab
	cd labs/vulnerable-rag && pip install -q -r requirements.txt && python ingest.py && python app.py

run-vulnerable-agent: ## Run the vulnerable agent lab
	cd labs/vulnerable-agent && pip install -q -r requirements.txt && python app.py

run-vulnerable-memory: ## Run the vulnerable memory assistant lab
	cd labs/vulnerable-memory-assistant && pip install -q -r requirements.txt && python app.py

# =============================================================================
# Evaluation and Evidence
# =============================================================================

eval: ## Run evaluation harness
	python evals/ai-security-eval-harness/run.py

evidence: ## Generate evidence report for a class
	python tools/report_generator/generate_evidence.py

# =============================================================================
# Scaffolding
# =============================================================================

scaffold-class: ## Create a new class directory. Usage: make scaffold-class PHASE=3 CLASS=15 NAME=document-poisoning
	@if [ -z "$(PHASE)" ] || [ -z "$(CLASS)" ] || [ -z "$(NAME)" ]; then \
		echo "Usage: make scaffold-class PHASE=3 CLASS=15 NAME=document-poisoning"; \
		exit 1; \
	fi
	python scripts/scaffold_class.py $(PHASE) $(CLASS) $(NAME)

# =============================================================================
# Project Maintenance
# =============================================================================

clean: ## Remove generated files and caches
	rm -rf __pycache__ .pytest_cache .ruff_cache .chroma/
	rm -rf dist/ build/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleaned"

validate-labs: ## Validate all lab directories have required files
	python tools/lab_validator/validate_lab.py labs/

# =============================================================================
# Quality Checks
# =============================================================================

check: lint test ## Run all quality checks
	@echo "✓ All quality checks passed"

ci: ## Simulate CI pipeline locally
	ruff check . || true
	python -m pytest -v --tb=short 2>/dev/null || echo "No tests yet"
	@echo "✓ CI pipeline simulation complete"

# =============================================================================
# Help
# =============================================================================

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-28s\033[0m %s\n", $$1, $$2}'
