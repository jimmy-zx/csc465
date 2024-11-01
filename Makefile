all: format

.PHONY: format black isort test pytest

format: black isort

test: pytest

black:
	black fmsd fmsd_impl tests

isort:
	isort fmsd fmsd_impl tests

pytest:
	pytest

