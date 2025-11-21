.PHONY: help install install-dev test lint format type-check clean coverage pre-commit

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e .
	pip install -r requirements-dev.txt

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=lfas --cov-report=term --cov-report=html

lint:  ## Run linters
	flake8 lfas/ tests/ --max-line-length=100 --extend-ignore=E501,W503
	pylint lfas/ --max-line-length=100

format:  ## Format code with black and isort
	black lfas/ tests/ examples/
	isort lfas/ tests/ examples/

format-check:  ## Check code formatting without making changes
	black --check lfas/ tests/ examples/
	isort --check-only lfas/ tests/ examples/

type-check:  ## Run type checking with mypy
	mypy lfas/ --ignore-missing-imports

quality:  ## Run all quality checks
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) type-check
	$(MAKE) test-cov

pre-commit-install:  ## Install pre-commit hooks
	pip install pre-commit
	pre-commit install

pre-commit:  ## Run pre-commit on all files
	pre-commit run --all-files

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build:  ## Build distribution packages
	python -m build

publish-test:  ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	python -m twine upload dist/*
