.DEFAULT_GOAL := help
.PHONY: help

quality: ## Run linters
	uv run ruff check
	uv run ruff format --diff
	uv run ty   check

quality-fix: ## Run automatic linter fixes
	uv run ruff format
	uv run ruff check --fix

changelog-entry: ## Run scriv to create a changelog entry
	uv run scriv create

changelog-collect: ## Collect all the changelog entries and rebuild CHANGELOG.md
	uv run scriv collect

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
