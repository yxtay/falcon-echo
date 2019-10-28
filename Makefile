APP_NAME=$(shell python -m src.config APP_NAME)
IMAGE_REGISTRY=$(shell python -m src.config IMAGE_REGISTRY)
DOCKER_FILE=Dockerfile

ENVIRONMENT?=dev
GOOGLE_APPLICATION_CREDENTIALS?=secrets/credentials.json

.PHONY: build
build:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt
	python -m pip freeze

.PHONY: black
black:
	black .

.PHONY: black-check
black-check:
	black --check --diff .

.PHONY: flake8
flake8:
	flake8

.PHONY: pytest
pytest:
	pytest

.PHONY: pre-commit-run
pre-commit-run:
	pre-commit run

.PHONY: gunicorn
gunicorn:
	gunicorn -c src/gunicorn_conf.py src.app:app

### Docker build and register scope
DOCKER_FILE=Dockerfile

.PHONY: docker-build
docker-build:
	docker build \
	-t $(IMAGE_REGISTRY)/$(APP_NAME):latest \
	-f $(DOCKER_FILE) \
	.

.PHONY: docker-run
docker-run:
	docker run --rm \
	-p 80:8080 \
	-e ENVIRONMENT=$(ENVIRONMENT) \
	--mount type=bind,source=$(shell pwd)/secrets,target=/home/appuser/secrets \
	-e GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) \
	$(IMAGE_REGISTRY)/$(APP_NAME):latest \
	$(ARGS)

.PHONY: docker-exec
docker-exec:
	docker exec -it \
	$(shell docker ps -q  --filter ancestor=$(IMAGE_REGISTRY)/$(APP_NAME)) \
	/bin/bash

.PHONY: docker-stop
docker-stop:
	docker stop \
	$(shell docker ps -q  --filter ancestor=$(IMAGE_REGISTRY)/$(APP_NAME))

.PHONY: docker-rmi
docker-rmi:
	docker rmi \
	$(shell docker images -q $(IMAGE_REGISTRY)/$(APP_NAME))

.PHONY: docker-push
docker-push:
	docker push $(IMAGE_REGISTRY)/$(APP_NAME):latest
### End Docker build and register scope
