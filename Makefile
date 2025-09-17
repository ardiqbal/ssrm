SRC   ?= ssrm_test
SHELL ?= bash
RUN   ?= poetry run
DOCS  ?= docs

NOTEBOOKS ?= $(wildcard notebooks/*.ipynb)

## Meta #######################################################################

.PHONY: help

# note: keep this as first target
help:  ## displays available make targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## Environment ################################################################

.PHONY: pip poetry install install-dev clean clean-pyc clean-notebooks

pip:
	python -m pip install --upgrade pip

poetry:
	pip install poetry==2.2.0

install: pip poetry ## installs dependencies for external users.
	poetry install --no-dev

install-dev: pip poetry ## installs dev dependencies for local development.
	poetry install
	$(RUN) pre-commit install

clean: clean-pyc  ## cleans all generated files.
	-@rm -rf dist build out
	-@find . -name '*.ipynb_checkpoints' -exec rm -rf {} +

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-notebooks:
	$(foreach f,$(NOTEBOOKS),jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace $(f);)

## Build/Release ##############################################################

.PHONY: autoflake black docs flake isort fmt fmt-notebooks release publish publish-test

autoflake:
	$(RUN) autoflake --recursive --in-place --remove-all-unused-imports --remove-duplicate-keys $(SRC)

black:
	$(RUN) pre-commit run black --all-files

docs:  ## builds docs.
	$(MAKE) -C $(DOCS) clean html
	# Copy logo image to fix Sphinx not groking relative paths in the README.
	@mkdir -p $(DOCS)/build/html/logos && cp logos/*.png $(DOCS)/build/html/logos

flake:  ## runs code linter.
	$(RUN) flake8 --exclude venv

isort:
	$(RUN) pre-commit run isort --all-files

fmt: isort black flake  ## runs code auto-formatters (isort, black).

fmt-notebooks:  ## runs notebook auto-formatters (black_nbconvert).
	$(RUN) black_nbconvert $(NOTEBOOKS)

release: clean  ## builds release artifacts into dist directory.
	poetry build

publish: release ## publishes artifacts to PyPi.
	@poetry config pypi-token.pypi ${PYPI_API_TOKEN}
	poetry publish -n

# For some reason, using poetry config pypi-token.pypi does not work for publishing to Test PyPi.
publish-test: release ## publishes artifacts to Test PyPi.
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	@poetry publish --repository testpypi -n -u ${PYPI_USERNAME} -p ${PYPI_TEST_API_TOKEN}

## Testing ####################################################################

.PHONY: check lint flake test

lint: flake

test: PYTEST_ARGS ?= --color=yes --cov-report xml --cov-report term --cov=$(SRC)
test: ## runs the unit tests.
	$(RUN) pytest $(PYTEST_ARGS)

check: lint test  ## runs all checks.
