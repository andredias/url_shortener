SHELL := /bin/bash -O globstar


run_dev: check_env
	@ docker compose up db -d; \
	trap 'docker compose down' INT; \
	ENV=development uv run ./entrypoint.sh


test: check_env
	docker compose up -d;
	uv run pytest -x \
		--cov-report=term-missing --cov-report=html --cov-branch \
		--cov=url_shortener


lint:
	ruff check --diff .
	@echo
	ruff format --diff .
	@echo
	mypy .


format:
	ruff check --silent --exit-zero --fix .
	@echo
	ruff format .


build:
	docker build -t url_shortener .


smoke_test: build check_env
	@ scripts/smoke_test.py


install_hooks:
	@ scripts/install_hooks.sh


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi
