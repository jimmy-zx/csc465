all: format

.PHONY: format black test pytest

format: black

test: pytest

black:
	black fmsd fmsd_impl tests

pytest:
	pytest

