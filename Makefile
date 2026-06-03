.PHONY: help install run run-agent clean test lint format go-hello bash-hello

help:
	@echo "golang-bash-ai-workspace"
	@echo "========================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make run-agent     - Run the Claude agent"
	@echo "  make go-hello      - Run Go hello world"
	@echo "  make bash-hello    - Run Bash hello world"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean up temporary files"

install:
	pip install -r requirements.txt

run-agent:
	python src/agent.py

go-hello:
	cd golang && go run hello.go

bash-hello:
	cd bash && bash hello.bash

test:
	pytest tests/ -v

lint:
	pylint src/

format:
	black src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
