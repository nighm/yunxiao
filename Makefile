.PHONY: help install test lint format coverage clean

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  coverage     Generate coverage report"
	@echo "  clean        Clean up generated files"

install:
	python -m pip install -e .[dev]

test:
	pytest -v

lint:
	flake8 src tests
	mypy src tests

format:
	black src tests

coverage:
	pytest --cov=src --cov-report=html tests/
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf output/
	find . -type d -name "__pycache__" -exec rm -rf {} + 