.DEFAULT_GOAL := help

PYTHONPATH=
SHELL=/bin/bash
VENV = .venv

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

ifneq ($(TERM),)
    GREEN        := $(shell tput setaf 2)
    RESET        := $(shell tput sgr0)
else
    GREEN        := ""
    RESET        := ""
endif


.PHONY: pre-commit
pre-commit:
	@echo "${GREEN}Formatting with ruff...${RESET}"
	uv run ruff format .
	@echo "${GREEN}Linting with ruff...${RESET}"
	uv run ruff check .
	@echo "${GREEN}Running static type checks...${RESET}"
	uv run pyright .

.PHONY: clean
clean: ## Remove environment and the caches
	@rm -rf .venv/
	@rm -rf .mypy_cache/
	@rm -rf .pytest_cache/
	@rm -rf .ruff_cache/

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort
