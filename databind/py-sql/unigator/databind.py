from .anosql import load_queries
import psycopg2
import psycopg2.sql
import psycopg2.extensions
from .exceptions import UnigatorDataBindError, UnigatorDataBindUnknownQuery


class SQLDefault(object):
    def __conform__(self, proto):
        if proto is psycopg2.extensions.ISQLQuote:
            return self

    def getquoted(self):
        return 'DEFAULT'


class UnigatorDataBind(object):
    class sql:
        default = SQLDefault()

    def __init__(self, db_type, queries_path, db_name=None, db_user=None, db_pass=None):
        if db_type != 'postgresql':
            raise UnigatorDataBindError('unsupported db_type')
        self.db_type = db_type
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass)
        self.queries = load_queries('postgres', queries_path)

    def __getattr__(self, attrname):
        def _query_wrapper(*args, **kwargs):
            return fn(self.conn, *args, **kwargs)
        fn = getattr(self.queries, attrname, None)
        if fn:
            return _query_wrapper
        raise UnigatorDataBindUnknownQuery(attrname)

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def execute(self, sql, *args, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute(sql, *args, **kwargs)
        cursor.close()

    def sql_scalar(self, sql, *args, **kwargs):
        cursor = self.conn.cursor()
        cursor.execute(sql, *args, **kwargs)
        result = cursor.fetchall()
        cursor.close()
        return (result or None) and result[0][0]

