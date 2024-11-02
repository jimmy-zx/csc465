all: build

.PHONY: format black isort test pytest build

build:
	python3 -m pip install --upgrade build
	python3 -m build

install:
	python3 -m pip install -e .

format: black isort

test: pytest

target_files = fmsd fmsd_impl tests setup.py build_isolated.py

black:
	python3 -m black $(target_files)

isort:
	python3 -m isort $(target_files)

pytest:
	python3 -m pytest

