all: build

.PHONY: format black isort test pytest build

build:
	python3 -m pip install --upgrade build
	python3 -m build

install:
	python3 -m pip install -e .

format: black isort

test: pytest

target_files = fmsd fmsd_impl tests setup.py

black:
	black $(target_files)

isort:
	isort $(target_files)

pytest:
	pytest

