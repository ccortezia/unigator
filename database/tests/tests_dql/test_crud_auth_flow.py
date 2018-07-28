import pytest
from .fixtures import *  # flake8: noqa


def test_create_auth_flow(db):
    pk = create_auth_flow(db, 'Flow 1')
    rs = retrieve_auth_flows_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_flow_id'] == pk
    assert rs[0]['auth_flow_desc'] == 'Flow 1'


def test_retrieve_auth_flows_by_ids(db):
    infos = ['Flow 1', 'Flow 12', 'Flow 10']
    pks = [create_auth_flow(db, info) for info in infos]
    rs = retrieve_auth_flows_by_ids(db, pks)
    assert [r['auth_flow_id'] for r in rs] == pks
    assert [r['auth_flow_desc'] for r in rs] == infos


def test_update_auth_flow(db):
    pk = create_auth_flow(db, 'Flow 1')
    update_auth_flow(db, pk, auth_flow_desc='Flow 30')
    rs = retrieve_auth_flows_by_ids(db, (pk,))
    assert rs[0]['auth_flow_desc'] == 'Flow 30'


def test_update_auth_flow_protected_pk_should_err(db):
    with pytest.raises(Exception):
        update_auth_flow(db, 0, auth_flow_desc='Flow 120')


def test_update_auth_flow_referenced_should_err(db):
    auth_flow = create_auth_flow(db, 'Flow 1')
    proc_id = create_process(db)
    update_process_auth_flow(db, proc_id, auth_flow)
    with pytest.raises(Exception):
        update_auth_flow(db, auth_flow, auth_flow_desc='Flow 120')


def test_delete_auth_flows_by_ids(db):
    pk = create_auth_flow(db, auth_flow_desc='Main Flow')
    delete_auth_flows_by_ids(db, (pk,))
    rs = retrieve_auth_flows_by_ids(db, (pk,))
    assert len(rs) == 0


def test_delete_auth_flow_protected_pk_should_err(db):
    with pytest.raises(Exception):
        delete_auth_flows_by_ids(db, (0,))


def test_delete_auth_flow_referenced_should_err(db):
    auth_flow = create_auth_flow(db, 'Flow 1')
    proc_id = create_process(db)
    update_process_auth_flow(db, proc_id, auth_flow)
    with pytest.raises(Exception):
        delete_auth_flows_by_ids(db, (auth_flow,))
