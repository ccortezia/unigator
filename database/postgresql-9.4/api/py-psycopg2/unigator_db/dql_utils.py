import psycopg2


class SQLDefault(object):
    def __conform__(self, proto):
        if proto is psycopg2.extensions.ISQLQuote:
            return self

    def getquoted(self):
        return 'DEFAULT'
