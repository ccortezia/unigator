import pytest
from unigator_db import (
    create_auth_level,
    create_auth_flow_st,
    retrieve_auth_flow_sts_by_auth_flow_id,
    update_auth_flow_st,
    create_auth_flow,
    delete_auth_flow_st_by_id,
    retrieve_auth_flows_by_ids
)


def test_create_auth_flow_st(pg_conn):
    create_auth_level(pg_conn, 'sys/app', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/app', False)
    rs = retrieve_auth_flow_sts_by_auth_flow_id(pg_conn, 0)
    assert len(rs) == 2
    assert rs[0]['st_name'] == 'sys/app'
    assert rs[0]['st_term'] is False


def test_retrieve_auth_flow_sts_by_auth_flow_id(pg_conn):
    create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/1', False)
    create_auth_flow_st(pg_conn, 0, 'sys/2', True)
    rs = retrieve_auth_flow_sts_by_auth_flow_id(pg_conn, 0)
    assert rs[0] == {'st_name': 'sys/1', 'st_term': False}
    assert rs[1] == {'st_name': 'sys/2', 'st_term': True}
    assert rs[2] == {'st_name': 'sys/none', 'st_term': False}


def test_update_auth_flow_st(pg_conn):
    create_auth_level(pg_conn, 'sys/app', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/app', False)
    update_auth_flow_st(pg_conn, 0, 'sys/app', True)
    rs = retrieve_auth_flow_sts_by_auth_flow_id(pg_conn, 0)
    assert rs[0]['st_term'] is True


def test_update_auth_flow_st_pk_should_err(pg_conn):
    create_auth_level(pg_conn, 'sys/app', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/app', False)
    flow_id = create_auth_flow(pg_conn, auth_flow_desc='Main Flow')
    with pytest.raises(Exception):
        pg_conn.execute('update ac_auth_flow_sts set auth_flow_id=%(flow_id)s where auth_flow_id = %(pk)s', {'pk': 0, 'flow_id': flow_id})


def test_delete_auth_flow_st_by_id(pg_conn):
    create_auth_level(pg_conn, 'sys/app', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/app', False)
    delete_auth_flow_st_by_id(pg_conn, 0, 'sys/app')
    rs = retrieve_auth_flow_sts_by_auth_flow_id(pg_conn, 0)
    assert len(rs) == 1


def test_delete_auth_flow_st_when_init_st_should_err(pg_conn):
    auth_flows = retrieve_auth_flows_by_ids(pg_conn, (0,))
    protected_st_name = auth_flows[0]['init_st']
    with pytest.raises(Exception):
        delete_auth_flow_st_by_id(pg_conn, 0, protected_st_name)
