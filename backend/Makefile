PYTHON ?= ../.venv/Scripts/python.exe

.PHONY: test test-unit test-integration test-cov-html

test:
	$(PYTHON) -m pytest

test-unit:
	$(PYTHON) -m pytest -m unit --no-cov

test-integration:
	$(PYTHON) -m pytest -m integration --no-cov

test-cov-html:
	$(PYTHON) -m pytest --cov-report=html
