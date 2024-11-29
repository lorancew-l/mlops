#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = mlops
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = ./venv/Scripts/python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies and pre-commit
## Install Python Dependencies and pre-commit
.PHONY: requirements
requirements:
	poetry self update
	poetry install
	poetry run pre-commit install
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	isort --check --diff --profile black mlops
	black --check --config pyproject.toml mlops
	flake8 --config=.flake8 mlops
	
## typecheck using mypy
.PHONY: typecheck
typecheck:
	mypy --config-file=mypy.ini mlops scripts

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml mlops

## Seed s3
.PHONY: seed_s3
seed_s3:
	$(PYTHON_INTERPRETER) ./scripts/seed_s3.py --bucket $(BUCKET) --object $(OBJECT)

## Process dataset
.PHONY: process
process:
	$(PYTHON_INTERPRETER) ./mlops/data/process.py --bucket $(BUCKET) --in-object $(IN_OBJECT) --out-object $(OUT_OBJECT)

## Run experiments
.PHONY: run_experiments
run_experiments:
	$(PYTHON_INTERPRETER) ./scripts/run_experiments.py --dataset-path $(DATASET) --config-path $(CONFIG)

## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	



#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
