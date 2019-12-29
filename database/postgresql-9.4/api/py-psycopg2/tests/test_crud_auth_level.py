import pytest
from unigator_db import (
    create_auth_level,
    retrieve_auth_levels_by_auth_name,
    update_auth_level,
    delete_auth_levels_by_auth_names,
)


def test_create_auth_level(pg_conn):
    pk = create_auth_level(pg_conn, 'app/special', auth_grant=True)
    rs = retrieve_auth_levels_by_auth_name(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_name'] == pk
    assert rs[0]['auth_grant'] is True


def test_retrieve_auth_levels_by_auth_name(pg_conn):
    infos = [('app/special', True), ('app/special2', False), ('user/custom', False)]
    pks = [create_auth_level(pg_conn, *info) for info in infos]
    rs = retrieve_auth_levels_by_auth_name(pg_conn, tuple(pks))
    assert [r['auth_name'] for r in rs] == list(list(zip(*infos))[0])
    assert [r['auth_grant'] for r in rs] == list(list(zip(*infos))[1])


def test_update_auth_level(pg_conn):
    pk = create_auth_level(pg_conn, 'app/special', auth_grant=True)
    update_auth_level(pg_conn, pk, new_auth_name='app/201', auth_grant=False)
    rs = retrieve_auth_levels_by_auth_name(pg_conn, ('app/201',))
    assert rs[0]['auth_name'] == 'app/201'
    assert rs[0]['auth_grant'] is False


def test_update_auth_level_protected_pk_should_err(pg_conn):
    with pytest.raises(Exception):
        update_auth_level(pg_conn, 'sys/none', auth_name='sys/none', auth_grant=False)
    pg_conn.rollback()
    with pytest.raises(Exception):
        update_auth_level(pg_conn, 'sys/none', auth_name='sys/app', auth_grant=False)


def test_delete_auth_levels_by_auth_names(pg_conn):
    pk = create_auth_level(pg_conn, 'app/special', auth_grant=True)
    delete_auth_levels_by_auth_names(pg_conn, (pk,))
    rs = retrieve_auth_levels_by_auth_name(pg_conn, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(pg_conn):
    with pytest.raises(Exception):
        delete_auth_levels_by_auth_names(pg_conn, ('sys/none',))
