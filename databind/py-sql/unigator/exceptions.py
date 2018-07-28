
class UnigatorDataBindError(Exception):
    """Base exception class for the unigator datasources"""


class UnigatorDataBindUnknownQuery(UnigatorDataBindError):
    """Raised when an unknown query is requested"""
