.PHONY: test clean
.DELETE_ON_ERROR: unigator_db/dql_api.py

SOURCES := $(shell find ../../dql -name *.sql)

unigator_db/dql_api.py: $(SOURCES)
	pipenv run voxsql $^ > $@

clean:
	rm -rf .pytest_cache __pycache__

test: test.setup test.run

test.run:
	@pipenv run pytest . $(ARGS)

test.setup:
	@pipenv install --dev
