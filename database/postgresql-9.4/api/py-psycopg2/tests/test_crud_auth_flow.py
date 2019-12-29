import pytest
from unigator_db import (
    create_process,
    create_auth_flow,
    retrieve_auth_flows_by_ids,
    update_auth_flow,
    update_process_auth_flow,
    delete_auth_flows_by_ids
)


def test_create_auth_flow(pg_conn):
    pk = create_auth_flow(pg_conn, 'Flow 1')
    rs = retrieve_auth_flows_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_flow_id'] == pk
    assert rs[0]['auth_flow_desc'] == 'Flow 1'


def test_retrieve_auth_flows_by_ids(pg_conn):
    infos = ['Flow 1', 'Flow 12', 'Flow 10']
    pks = [create_auth_flow(pg_conn, info) for info in infos]
    rs = retrieve_auth_flows_by_ids(pg_conn, tuple(pks))
    assert [r['auth_flow_id'] for r in rs] == pks
    assert [r['auth_flow_desc'] for r in rs] == infos


def test_update_auth_flow(pg_conn):
    pk = create_auth_flow(pg_conn, 'Flow 1')
    update_auth_flow(pg_conn, pk, auth_flow_desc='Flow 30')
    rs = retrieve_auth_flows_by_ids(pg_conn, (pk,))
    assert rs[0]['auth_flow_desc'] == 'Flow 30'


def test_update_auth_flow_protected_pk_should_err(pg_conn):
    with pytest.raises(Exception):
        update_auth_flow(pg_conn, 0, auth_flow_desc='Flow 120')


def test_update_auth_flow_referenced_should_err(pg_conn):
    auth_flow = create_auth_flow(pg_conn, 'Flow 1')
    proc_id = create_process(pg_conn)
    update_process_auth_flow(pg_conn, proc_id, auth_flow)
    with pytest.raises(Exception):
        update_auth_flow(pg_conn, auth_flow, auth_flow_desc='Flow 120')


def test_delete_auth_flows_by_ids(pg_conn):
    pk = create_auth_flow(pg_conn, auth_flow_desc='Main Flow')
    delete_auth_flows_by_ids(pg_conn, (pk,))
    rs = retrieve_auth_flows_by_ids(pg_conn, (pk,))
    assert len(rs) == 0


def test_delete_auth_flow_protected_pk_should_err(pg_conn):
    with pytest.raises(Exception):
        delete_auth_flows_by_ids(pg_conn, (0,))


def test_delete_auth_flow_referenced_should_err(pg_conn):
    auth_flow = create_auth_flow(pg_conn, 'Flow 1')
    proc_id = create_process(pg_conn)
    update_process_auth_flow(pg_conn, proc_id, auth_flow)
    with pytest.raises(Exception):
        delete_auth_flows_by_ids(pg_conn, (auth_flow,))
