.DEFAULT_GOAL := help
.PHONY: docs
SRC_DIRS = ./tutorpod_autoscaling
BLACK_OPTS = --exclude templates ${SRC_DIRS}

# Warning: These checks are not necessarily run on every PR.
test: test-lint test-types test-format  # Run some static checks.

test-format: ## Run code formatting tests
	black --check --diff $(BLACK_OPTS)

test-lint: ## Run code linting tests
	pylint --errors-only --enable=unused-import,unused-argument --ignore=templates --ignore=docs/_ext ${SRC_DIRS}

test-types: ## Run type checks.
	mypy --exclude=templates --ignore-missing-imports --implicit-reexport --strict ${SRC_DIRS}

format: ## Format code automatically
	black $(BLACK_OPTS)

isort: ##  Sort imports. This target is not mandatory because the output may be incompatible with black formatting. Provided for convenience purposes.
	isort --skip=templates ${SRC_DIRS}

release: ## release a new version
	@echo "Releasing a new version."
	@echo "This is a remote release, it will push to the remote repository."
	semantic-release --strict version --changelog --push --tag --commit

local-release:
	@echo "Releasing a new version."
	@echo "This is a local release, it will not push to the remote repository."
	@echo "You can push the changes and release manually."
	semantic-release version --changelog --commit --no-push

ESCAPE = 
help: ## Print this help
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
