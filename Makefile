.PHONY: clean install lint test build

clean:
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +

install:
	pip install poetry --upgrade
	poetry install
  
lint:
	poetry run black globalprogramlib tests
  
test:
	poetry run black --check globalprogramlib tests
	poetry run pytest tests

build:
	poetry build
