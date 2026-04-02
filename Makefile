.PHONY: install test lint format build publish clean

# Install dependencies
install:
	pip install -e ".[dev]"

# Run tests
test:
	pytest tests/ -v --cov=src/life

# Lint code
lint:
	mypy src/life/
	flake8 src/life/

# Format code
format:
	black src/life/ tests/ examples/
	isort src/life/ tests/ examples/

# Build package
build:
	python -m build

# Publish to PyPI
publish:
	twine upload dist/*

# Clean build artifacts
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

# Run quickstart
quickstart:
	python scripts/quickstart.py

# Run examples
examples:
	python examples/basic_usage.py

# All checks before commit
check: lint test
	@echo "All checks passed!"
