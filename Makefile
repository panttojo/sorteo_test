.DEFAULT_GOAL := help
SHELL := bash
.ONESHELL:

PROJECT_NAME=apps
DB_NAME=$(PROJECT_NAME)
INVENTORY=provisioner/hosts
PLAYBOOK=provisioner/site.yml
PYTHON_PATH=venv/bin/

run_all:  ## Run all the servers in parallel, requires GNU Make
	make -j django docs celery redis
.PHONY: run_all

venv:  ## Create python virtualenv at `./venv/`
	python3 -m venv venv

regenerate:  ## Delete and create new database.
	-dropdb $(DB_NAME)
	createdb $(DB_NAME)
	${PYTHON_PATH}python manage.py migrate
.PHONY: regenerate

install: venv  ## Install and setup project dependencies
	${PYTHON_PATH}python -m pip install -r requirements/development.txt
	${PYTHON_PATH}pre-commit install
ifneq ($(CI),True)
	-createdb $(DB_NAME)
	${PYTHON_PATH}python manage.py migrate
endif
.PHONY: install

clean:  ## Remove all temporary files like pycache
	find . -name \*.rdb -type f -ls -delete
	find . -name \*.pyc -type f -ls -delete
	find . -name __pycache__ -ls -delete
.PHONY: clean

# == Django Helpers
# ===================================================
djrun: install  ## Start Django server locally
	${PYTHON_PATH}python manage.py runserver

check:  ## Check the project for code-style related errors
	${PYTHON_PATH}black ${PROJECT_NAME} tests/ settings/
	${PYTHON_PATH}flake8 .
.PHONY: check

test: ARGS=--pdb --cov  ## Run all the tests
test: check
	${PYTHON_PATH}pytest $(ARGS)

djmm:  ## Create Django migrations
	${PYTHON_PATH}python manage.py makemigrations

djmigrate:  # Run Django migrations
	${PYTHON_PATH}python manage.py migrate

djurls:  ## Displays all the django urls
	${PYTHON_PATH}python manage.py show_urls

shell:  ## Enter the django shell
	${PYTHON_PATH}python manage.py shell_plus

docs: venv  ## Start documentation server locally
	${PYTHON_PATH}python -m pip install -r requirements/docs.txt
	${PYTHON_PATH}mkdocs serve
celery: install  ## Start celery worker
	${PYTHON_PATH}celery -A $(PROJECT_NAME) worker -B -l INFO

redis:  ## Start redis server
	redis-server

help:  ## Display this help
	# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'
.PHONY: help
