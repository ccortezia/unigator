
def parsed_result(regex):
    """Decorator to destructure the result of the returned string into a tuple of elements,
    according to grouping patterns specified in the given regex. Matched tokens are then
    automatically evaluated to literals, falling back to being string literals if no suitable
    alternate type is found.

    @param regex: used as a simple tokenizer
    @return tuple of values from tokens matched in the regex groupings
    """
    import re
    import ast
    import functools

    def try_literal_eval(symbol):
        try:
            return ast.literal_eval(symbol)
        except (ValueError, SyntaxError):
            return symbol

    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            retval = fn(*args, **kwargs)
            match = re.match(regex, retval)
            if match:
                return tuple([try_literal_eval(symbol) for symbol in match.groups()])
            return retval
        return wrapped
    return wrapper


def maybe_default(db, value):
    """Gets a psycopg compliat SQL DEFAULT keyword for a None value, or the value otherwise"""
    return value if value is not None else db.sql.default
