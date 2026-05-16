.PHONY: help install test lint format clean dev

help:
	@echo "Available commands:"
	@echo "  make install    - Install package in development mode with dev dependencies"
	@echo "  make test       - Run pytest tests with verbose output"
	@echo "  make lint       - Run ruff check on rfuns/ and tests/"
	@echo "  make format     - Format code with ruff"	
	@echo "  make repl       - Launch a UV-powered Python REPL"	
	@echo "  make clean      - Remove build artifacts and cache files"
	@echo "  make dev        - Install dev dependencies"

install:
	uv pip install -e ".[dev]"

test:
	uv run pytest tests/ -v

test-r:
	uv run pytest tests/ -v --r-check

lint:
	uv run ruff check rfuns/ tests/

format:
	uv run ruff format rfuns/ tests/

repl:
	uv run python

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf rfuns.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

dev: install
	@echo "Development environment ready!"
