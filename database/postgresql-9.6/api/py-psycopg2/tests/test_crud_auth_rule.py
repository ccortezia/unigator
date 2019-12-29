import pytest
from .fixtures import *  # noqa
from .fixtures import _create_auth_rule
from unigator_db import (
    retrieve_auth_rules_by_ids,
    create_process,
    delete_auth_rules_by_ids,
    update_auth_rule,
)


def test_create_auth_rule(pg_conn):
    _create_auth_rule(pg_conn, 1, 'sys/none')


def test_create_auth_rule_increment_rule_ord(pg_conn, blank_rules):
    blank_rules.append(_create_auth_rule(pg_conn, 3, 'sys/none'))
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[0]['rule_ord'] == 1
    assert rs[1]['rule_ord'] == 2
    assert rs[6]['rule_ord'] == 3
    assert rs[2]['rule_ord'] == 4
    assert rs[3]['rule_ord'] == 5
    assert rs[4]['rule_ord'] == 6
    assert rs[5]['rule_ord'] == 7


def test_create_auth_rule_framing_rule_ord(pg_conn):
    pks = [
        _create_auth_rule(pg_conn, -1, 'sys/none'),  # under lower boundary
        _create_auth_rule(pg_conn, 0, 'sys/none'),   # under lower boundary
        _create_auth_rule(pg_conn, 4, 'sys/none'),   # above current max
        _create_auth_rule(pg_conn, 4, 'sys/none'),   # should not change
    ]
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(pks))
    assert rs[0]['rule_ord'] == 2
    assert rs[1]['rule_ord'] == 1
    assert rs[2]['rule_ord'] == 3
    assert rs[3]['rule_ord'] == 4


def test_create_auth_rule_running_process_err(pg_conn):
    create_process(pg_conn)
    with pytest.raises(Exception):
        _create_auth_rule(pg_conn, 1, 'sys/none')


def test_retrieve_auth_rules_by_ids(pg_conn, blank_rules):
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert len(rs) == len(blank_rules)
    for idx, rule_id in enumerate(blank_rules):
        assert rs[idx]['rule_id'] == rule_id


def test_update_auth_rule(pg_conn):
    pk = _create_auth_rule(pg_conn, 1, 'sys/none')
    rs = retrieve_auth_rules_by_ids(pg_conn, (pk,))
    assert rs[0]['ctc'] is None
    patch_auth_rule(pg_conn, pk, ctc=0)
    rs = retrieve_auth_rules_by_ids(pg_conn, (pk,))
    assert rs[0]['ctc'] == 0


def test_update_auth_rule_move_last_ord_to_middle(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[-1], rule_ord=3)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[0]['rule_ord'] == 1
    assert rs[1]['rule_ord'] == 2
    assert rs[5]['rule_ord'] == 3
    assert rs[2]['rule_ord'] == 4
    assert rs[3]['rule_ord'] == 5
    assert rs[4]['rule_ord'] == 6


def test_update_auth_rule_move_first_ord_to_middle(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[0], rule_ord=3)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[1]['rule_ord'] == 1
    assert rs[2]['rule_ord'] == 2
    assert rs[0]['rule_ord'] == 3
    assert rs[3]['rule_ord'] == 4
    assert rs[4]['rule_ord'] == 5
    assert rs[5]['rule_ord'] == 6


def test_update_auth_rule_move_ord_beyond_last(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[0], rule_ord=10)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[1]['rule_ord'] == 1
    assert rs[2]['rule_ord'] == 2
    assert rs[3]['rule_ord'] == 3
    assert rs[4]['rule_ord'] == 4
    assert rs[5]['rule_ord'] == 5
    assert rs[0]['rule_ord'] == 6


def test_update_auth_rule_move_ord_beyond_first(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[-1], rule_ord=0)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[5]['rule_ord'] == 1
    assert rs[0]['rule_ord'] == 2
    assert rs[1]['rule_ord'] == 3
    assert rs[2]['rule_ord'] == 4
    assert rs[3]['rule_ord'] == 5
    assert rs[4]['rule_ord'] == 6


def test_update_auth_rule_move_middle_ord_down(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[1], rule_ord=5)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[0]['rule_ord'] == 1
    assert rs[2]['rule_ord'] == 2
    assert rs[3]['rule_ord'] == 3
    assert rs[4]['rule_ord'] == 4
    assert rs[1]['rule_ord'] == 5
    assert rs[5]['rule_ord'] == 6


def test_update_auth_rule_move_middle_ord_up(pg_conn, blank_rules):
    patch_auth_rule(pg_conn, blank_rules[4], rule_ord=2)
    rs = retrieve_auth_rules_by_ids(pg_conn, tuple(blank_rules))
    assert rs[0]['rule_ord'] == 1
    assert rs[4]['rule_ord'] == 2
    assert rs[1]['rule_ord'] == 3
    assert rs[2]['rule_ord'] == 4
    assert rs[3]['rule_ord'] == 5
    assert rs[5]['rule_ord'] == 6


def test_update_auth_rule_running_process_err(pg_conn, blank_rules):
    pk = _create_auth_rule(pg_conn, 1, 'sys/none')
    create_process(pg_conn)
    with pytest.raises(Exception):
        patch_auth_rule(pg_conn, pk, ctc=0)


def test_delete_auth_rules_by_ids(pg_conn):
    pk = _create_auth_rule(pg_conn, 1, 'sys/none')
    delete_auth_rules_by_ids(pg_conn, (pk,))
    rs = retrieve_auth_rules_by_ids(pg_conn, (pk,))
    assert len(rs) == 0


def test_delete_auth_rules_by_ids_running_process_err(pg_conn):
    pk = _create_auth_rule(pg_conn, 1, 'sys/none')
    create_process(pg_conn)
    with pytest.raises(Exception):
        delete_auth_rules_by_ids(pg_conn, (pk,))


# --------

def patch_auth_rule(pg_conn, rule_id, **kwargs):
    rs = retrieve_auth_rules_by_ids(pg_conn, (rule_id,))
    _kwargs = dict(rs[0], **kwargs)
    _kwargs.pop('rule_id')
    update_auth_rule(pg_conn, rule_id, **_kwargs)
