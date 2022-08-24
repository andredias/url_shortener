run:
	@ docker-compose up -d; \
	trap 'docker-compose down' INT; \
	hypercorn --reload --config=hypercorn.toml 'url_shortener.main:app'


test:
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


smoke_test: build
	@ scripts/smoke_test.py



install_hooks:
	@ scripts/install_hooks.sh
