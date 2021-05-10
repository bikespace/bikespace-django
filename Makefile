setup-py:
	@# setup a virtualenv for python3
	virtualenv -p python3 venv
	@# note "venv" is now the name of the directory containing the python virtualenv
	@# Use the "venv" you setup earlier for your python3 project buy running the activate script
	( \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
	)

migrate: ## Run database migrations (e.g. when models change)
	@# Run the migrations for the database
	python manage.py migrate

setup-db: migrate
	@# Create a superuser for the admin web page
	python manage.py shell < scripts/create_django_admin.py
	python manage.py collectstatic --no-input

setup-node:
	(cd bicycleparking && npm install)

setup: setup-py setup-node setup-db ## Prepare the environment and database

seed: ## Seed database with test data
	python test/LoadTestDB.py

test: ## Run code coverage tests
	bash scripts/run_tests.sh

start: ## Start the app
	(cd bicycleparking && npm run local)& \
		python manage.py runserver

deploy-staging: ## Deploy app to staging environment
	ENV=staging bash scripts/deploy.sh

deploy-prod:
	ENV=prod bash scripts/deploy.sh

%:
	@true

.PHONY: help test

help:
	@echo 'Usage: make <command>'
	@echo
	@echo 'where <command> is one of the following:'
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
