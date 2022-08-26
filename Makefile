SHELL := /bin/bash -O globstar


run: check_env
	@ docker-compose up -d; \
	trap 'docker-compose down' INT; \
	hypercorn --reload --config=hypercorn.toml 'url_shortener.main:app'


test: check_env
	@ scripts/test_project.py


lint:
	@echo
	isort --diff -c .
	@echo
	blue --check --diff --color .
	@echo
	flake8 .
	@echo
	mypy .
	@echo
	bandit -qr url_shortener/
	@echo
	pip-audit


format:
	isort .
	blue .
	pyupgrade --py310-plus **/*.py


build:
	docker build -t url_shortener .


smoke_test: build check_env
	@ scripts/smoke_test.py


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi
