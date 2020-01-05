.PHONY: help create-env setup setup-dev run clean lint test

help:
	@echo "  create-env		create python 3 virtual env"
	@echo "  setup			install runtime dependencies"
	@echo "  setup-dev		same as setup except installs dev-only dependencies as well"
	@echo "  run			run the service"
	@echo "  clean			remove unwanted files like .pyc's"
	@echo "  sort-imports	Automatically sort imports in all .py files"
	@echo "  lint			check style with flake8"
	@echo "  test			run all your tests using py.test"

ifeq ($(strip $(VIRTUAL_ENV)),)
export VIRTUAL_ENV := venv
endif
create-env:
	python3.8 -m venv $(VIRTUAL_ENV)

setup:
	$(VIRTUAL_ENV)/bin/pip install -e .

setup-dev:
	$(VIRTUAL_ENV)/bin/pip install -e .[test]

run:
	FLASK_APP=wass/server.py $(VIRTUAL_ENV)/bin/flask run --port 5017 --host 0.0.0.0

clean:
	find . -name "*.pyc" -delete
	rm -rf build dist wheels venv *.egg-info

sort-imports:
	isort --recursive .

lint:
	$(VIRTUAL_ENV)/bin/flake8 .
	$(VIRTUAL_ENV)/bin/pylint wass

test:
	$(VIRTUAL_ENV)/bin/py.test tests
