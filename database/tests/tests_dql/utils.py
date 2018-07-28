import datetime


def dt(y, mo, d, h=0, m=0):
    """Datetime creator, alias"""
    return datetime.datetime(y, mo, d, h, m)
