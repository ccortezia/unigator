#!/bin/bash

set -e

export PGUSER=postgres
export PGPASSWORD=verde3
export PGHOST=stack_db_1
export PGDATABASE=unigator
/opt/proj/database/postgresql-common/db-setup

export PGUSER=unigator
export PGPASSWORD=123123
export PGHOST=stack_db_1
export PGDATABASE=unigator
/opt/proj/database/postgresql-common/db-reset default

export PGUSER=unigator
export PGPASSWORD=123123
export PGHOST=stack_db_1
export PGDATABASE=unigator
source /opt/venvs/database-tests/bin/activate
pushd /opt/proj/database/tests/tests_dql
PYTHONPATH=/opt/proj/databind/py-sql/ py.test
