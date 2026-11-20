.DEFAULT_GOAL := help

UV ?= uv
# a test file to run alone: make test FILE=tests/test_x.py
FILE ?=

.PHONY: help setup format lint typecheck hooks test clean

help: ## List the available commands
	@awk 'BEGIN { FS = ":.*##" } /^[a-zA-Z0-9_-]+:.*##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Install the dependencies and the pre-commit hook
	$(UV) sync
	$(UV) run --with pre-commit pre-commit install

format: ## Fix lint issues and format the code with ruff
	$(UV) run ruff check --fix .
	$(UV) run ruff format .

lint: ## Run every pre-commit hook on all files (ruff, pyright and the rest), as CI does
	$(UV) run --with pre-commit pre-commit run --all-files --show-diff-on-failure

typecheck: ## Check the types with pyright
	$(UV) run pyright

hooks: ## Run every pre-commit hook on all files, as CI does
	$(UV) run --with pre-commit pre-commit run --all-files --show-diff-on-failure

test: ## Run the tests with coverage; make test FILE=tests/test_x.py runs only that file, without it
	QT_QPA_PLATFORM=offscreen $(UV) run pytest -q $(if $(FILE),--no-cov $(FILE))

clean: ## Remove the caches
	rm -rf .pytest_cache .ruff_cache .pyright dist build *.egg-info
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
