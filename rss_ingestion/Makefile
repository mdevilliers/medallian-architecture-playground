
DAGSTER_VERSION=1.6.1
DAGSTER_LIBS_VERSION=0.22.1
DOCKER_BASE_IMAGE_VERSION=python:3.11-slim

.PHONY: docker_build
docker_build:
	docker build -t rss_ingestion --build-arg BASE_IMAGE=$(DOCKER_BASE_IMAGE_VERSION) --build-arg DAGSTER_VERSION=$(DAGSTER_VERSION) --build-arg DAGSTER_LIBS_VERSION=$(DAGSTER_LIBS_VERSION) .

.PHONY: lint
lint:
	pylama

