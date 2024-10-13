PWD := $(shell pwd)

analyze:
	@poetry run python app.py > app.log

parse_log:
	@poetry run python parse_log.py

all: analyze parse_log