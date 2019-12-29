import os
import pytest
import psycopg2
import logging
from psycopg2.extras import LoggingConnection


LOGGER = logging.getLogger('tests')
LOGGER.setLevel(logging.DEBUG)

HERE = os.path.abspath(os.path.join(__file__, os.path.pardir))
DBROOT = os.path.join(HERE, '../../..')


@pytest.fixture(scope='session')
def sql_schema():
    """Provides the stock database schema SQL"""
    base_path = os.path.normpath(os.path.join(DBROOT, 'ddl'))
    return _concat_files_from_dir(base_path)


@pytest.fixture(scope='session')
def sql_initdb():
    """Provides the stock database initialization SQL"""
    initdb_path = os.path.normpath(os.path.join(DBROOT, 'dml/initdb.sql'))
    with open(initdb_path) as f:
        return f.read()


@pytest.fixture(scope='session')
def unigator_db_conn():
    """Provides a psycopg2 connection object for the 'unigator' database"""
    connection = psycopg2.connect(host='localhost',
                                  dbname='unigator',
                                  user='unigator',
                                  password='123123',
                                  connection_factory=LoggingConnection)
    connection.initialize(LOGGER)
    return connection


@pytest.fixture(scope='session')
def postgres_db_conn():
    """Provides a psycopg2 connection object for the 'postgres' database"""
    connection = psycopg2.connect(host='localhost',
                                  dbname='postgres',
                                  user='postgres',
                                  password='verde3',
                                  connection_factory=LoggingConnection)
    connection.initialize(LOGGER)
    return connection


@pytest.fixture(scope='session')
def setup_db(postgres_db_conn):
    postgres_db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = postgres_db_conn.cursor()
    cursor.execute("drop database if exists unigator")
    cursor.execute("drop user if exists unigator")
    cursor.execute("create user unigator with nosuperuser nocreatedb createrole")
    cursor.execute("create database unigator with owner unigator")
    cursor.execute("alter user unigator with password '123123'")
    cursor.execute('alter role unigator set search_path to "$user", custom, ung, public')
    postgres_db_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_DEFAULT)


@pytest.fixture(scope='session')
def pg_fresh(setup_db, unigator_db_conn, sql_schema, sql_initdb):
    """Ensures the database is reset at the start of each test session execution"""
    cursor = unigator_db_conn.cursor()
    cursor.execute(sql_schema)
    cursor.execute(sql_initdb)
    unigator_db_conn.commit()
    return unigator_db_conn


@pytest.fixture(scope='function')
def pg_conn(pg_fresh, request):
    """Ensures the database is rolled back at the end of each test function execution"""
    request.addfinalizer(pg_fresh.rollback)
    return pg_fresh


# --------------------------------------------------------------------------------------------------
# Local helpers
# --------------------------------------------------------------------------------------------------

def _concat_files_from_dir(dir_path):
    paths = [os.path.join(dir_path, filename) for filename in sorted(os.listdir(dir_path))]
    output = ''
    for fname in paths:
        with open(fname) as infile:
            output += infile.read()
    return output
