close:
	docker-compose down

build:
	ssh-add
	@echo "--> Building Docker Base Image"
	DOCKER_BUILDKIT=1 docker build --ssh default -t facebook -f docker/api/Dockerfile .
	@echo "--> Building Compose"
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build

build-no-cache:
	ssh-add
	@echo "--> Building Docker Base Image"
	DOCKER_BUILDKIT=1 docker build --ssh default -t facebook -f docker/api/Dockerfile . --no-cache
	@echo "--> Building Compose"
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build

bash:
	docker-compose run api bash

run:
	docker-compose up

run-debug:
	docker-compose run --service-ports api

test:
	@echo "--> Testing on Docker."
	docker-compose run api pytest $(path) -s --cov-report term-missing --cov-fail-under 100

test-missing:
	@echo "--> Testing on Docker."
	docker-compose run api pytest $(path) -s --cov-report term-missing

install-requirements:
	pip install -r requirements/base-git.txt --upgrade
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt

delete-requirements:
	@echo "--> Deleting old requirements files"
	rm -f requirements/base-git.txt && \
	rm -f requirements/base.txt && \
	rm -f requirements/dev.txt && \
	rm -f requirements/test.txt
	rm -f the-facebook/chalicelib/requirements.txt

compile-requirements: delete-requirements
	@echo "--> Compiling requirements"
	cd requirements && pip-compile base-git.in
	ssh-add
	DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose run api bash -c	" \
	cd requirements && \
	pip-compile base.in && \
	pip-compile dev.in && \
	pip-compile test.in && \
	cat base.txt > ../the-facebook/requirements.txt && \
	cat base-git.txt >> ../the-facebook/requirements.txt "
