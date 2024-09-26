PWD := $(shell pwd)

build-code:
	@poetry run python setup.py build_ext --inplace

run: build-code
	@PYTHONPATH=${PWD} poetry run python perf-cthon.py