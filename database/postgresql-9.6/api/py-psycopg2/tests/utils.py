import datetime


def dt(y, mo, d, h=0, m=0):
    """Datetime creator, alias"""
    return datetime.datetime(y, mo, d, h, m)


def fetch_scalar(conn, sql, *args, **kwargs):
    cursor = conn.cursor()
    cursor.execute(sql, *args, **kwargs)
    result = cursor.fetchall()
    cursor.close()
    return (result or None) and result[0][0]
