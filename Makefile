.PHONY: \
	stack.pg.start \
	stack.pg.stop \
	stack.pg.kill \
	test test.ci \
	test.ci.setup \
	test.ci.run \
	db.pg.setup \
	db.pg.reset \
	db.pg.query

stack.pg.start.d:
	docker-compose -f stack/postgresql-9.6.yaml up -d
	sleep 3

stack.pg.stop:
	docker-compose -f stack/postgresql-9.6.yaml stop

stack.pg.kill:
	docker-compose -f stack/postgresql-9.6.yaml rm -f
	docker volume rm stack_db-data

test:
	make -C database/postgresql-9.6/api/py-psycopg2 test

test.ci: test.ci.setup test.ci.run

test.ci.setup:
	curl -fLSs https://circle.ci/cli | bash

test.ci.run:
	circleci local execute --branch ${BRANCH} --job test-database

db.pg.setup:
	@PGHOST=localhost PGPORT=5432 PGUSER=postgres database/postgresql-9.6/bin/db-setup

db.pg.reset:
	@PGHOST=localhost PGPORT=5432 PGUSER=unigator database/postgresql-9.6/bin/db-reset

db.pg.query:
	@PGHOST=localhost PGPORT=5432 PGPASSWORD=123123 psql -q -h localhost -U unigator -c '${QUERY}'
