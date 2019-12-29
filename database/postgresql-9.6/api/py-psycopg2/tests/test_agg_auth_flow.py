import pytest
from .utils import fetch_scalar
from .fixtures import *  # noqa

# -------------------------------------------------------------------------------------------------

AUTH_FLOW_REDUCTION_TEST_CASES = [
    # Expected   Event Stream
    (None,       []),
    ('sys/none', ['sys/none']),
    ('sys/0001', ['sys/0001']),
    ('sys/0002', ['sys/0001', 'sys/0002']),
    ('sys/0003', ['sys/0001', 'sys/0002', 'sys/0003']),
    ('sys/0004', ['sys/0001', 'sys/0002', 'sys/0003', 'sys/0004']),
    ('sys/0005', ['sys/0001', 'sys/0002', 'sys/0003', 'sys/0004', 'sys/0005']),
    ('sys/none', ['sys/0002']),
    ('sys/none', ['sys/????']),
    ('sys/0001', ['sys/????', 'sys/0001']),
    ('sys/0001', ['sys/0001', 'sys/0005']),
    ('sys/0002', ['sys/0001', 'sys/0001', 'sys/0001', 'sys/0002']),
    ('sys/0002', ['sys/0001', 'sys/0001', 'sys/0001', 'sys/0002', 'sys/0001']),
]


# -------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("reduced, events", AUTH_FLOW_REDUCTION_TEST_CASES)
def test_auth_flow_fsm_reduce(pg_conn, basic_flow, reduced, events):
    assert reduced == _reduce_evs(pg_conn, basic_flow, events)


def _reduce_evs(pg_conn, auth_flow_id, evs):
    return fetch_scalar(pg_conn, '''
        with ev_stream (auth_name) as (select unnest(%(evs)s::varchar[]))
        select ac_auth_reduce(ev_stream.auth_name, %(auth_flow_id)s)
        from ev_stream;
        ''', {'evs': list(evs), 'auth_flow_id': auth_flow_id})
