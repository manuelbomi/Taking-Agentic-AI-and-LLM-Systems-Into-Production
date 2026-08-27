.PHONY: install test run docker-build

install:
	python -m pip install -r requirements.txt

test:
	pytest -q

run:
	uvicorn agentic_production.api:app --app-dir src --host 0.0.0.0 --port 8000

docker-build:
	docker build -f deploy/Dockerfile -t agentic-production:local .
