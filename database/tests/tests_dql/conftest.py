import os
import pytest
from unigator import UnigatorDataBind

HERE = os.path.abspath(os.path.join(__file__, os.path.pardir))
ROOT = os.path.join(HERE, '../../..')
DBTYPE = 'postgresql-default'


@pytest.fixture(scope='session')
def sql_schema():
    """Provides the stock database schema SQL"""
    base_path = os.path.normpath(os.path.join(ROOT, 'database/{}/ddl'.format(DBTYPE)))
    return _concat_files_from_dir(base_path)


@pytest.fixture(scope='session')
def sql_initdb():
    """Provides the stock database initialization SQL"""
    initdb_path = os.path.normpath(os.path.join(ROOT, 'database/{}/dml/initdb.sql'.format(DBTYPE)))
    with open(initdb_path) as f:
        return f.read()


@pytest.fixture(scope='session')
def dbctl():
    """Provides a plain database access object"""
    sql_path = os.path.normpath(os.path.join(ROOT, 'database/{}/dql/operations.sql'.format(DBTYPE)))
    return UnigatorDataBind('postgresql', sql_path)


@pytest.fixture(scope='session')
def dbfresh(dbctl, sql_schema, sql_initdb):
    """Ensures the database is reset at the start of each test session execution"""
    dbctl.execute(sql_schema)
    dbctl.execute(sql_initdb)
    dbctl.commit()
    return dbctl


@pytest.fixture(scope='function')
def db(dbfresh, request):
    """Ensures the database is rolled back at the end of each test function execution"""
    request.addfinalizer(dbfresh.rollback)
    return dbfresh


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
