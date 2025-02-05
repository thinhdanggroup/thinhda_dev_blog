GITHUB_URL ?= ""

review:
	@poetry run python app.py review $(GITHUB_URL)

improve:
	@poetry run python app.py improve $(GITHUB_URL)

all: review improve
	@echo "All done"