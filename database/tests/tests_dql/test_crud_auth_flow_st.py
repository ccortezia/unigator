import pytest
from .fixtures import *  # flake8: noqa


def test_create_auth_flow_st(db):
    create_auth_level(db, 'sys/app', auth_grant=False)
    pk = create_auth_flow_st(db, 0, 'sys/app', False)
    rs = retrieve_auth_flow_sts_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_flow_id'] == pk[0]
    assert rs[0]['st_name'] == pk[1]
    assert rs[0]['st_term'] is False


def test_retrieve_auth_flow_sts_by_ids(db):
    create_auth_level(db, 'sys/app', auth_grant=False)
    infos = [(0, 'sys/app', True)]
    pks = [create_auth_flow_st(db, *info) for info in infos]
    rs = retrieve_auth_flow_sts_by_ids(db, pks)
    assert [r['auth_flow_id'] for r in rs] == list(list(zip(*infos))[0])
    assert [r['st_name'] for r in rs] == list(list(zip(*infos))[1])
    assert [r['st_term'] for r in rs] == list(list(zip(*infos))[2])


def test_retrieve_auth_flow_sts_by_auth_flow_id(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', False)
    create_auth_flow_st(db, 0, 'sys/2', True)
    rs = retrieve_auth_flow_sts_by_auth_flow_id(db, 0)
    assert rs[0] == {'auth_flow_id': 0, 'st_name': 'sys/1', 'st_term': False}
    assert rs[1] == {'auth_flow_id': 0, 'st_name': 'sys/2', 'st_term': True}
    assert rs[2] == {'auth_flow_id': 0, 'st_name': 'sys/none', 'st_term': False}


def test_update_auth_flow_st(db):
    create_auth_level(db, 'sys/app', auth_grant=False)
    pk = create_auth_flow_st(db, 0, 'sys/app', False)
    update_auth_flow_st(db, pk, True)
    rs = retrieve_auth_flow_sts_by_ids(db, (pk,))
    assert rs[0]['st_term'] is True


def test_update_auth_flow_st_pk_should_err(db):
    create_auth_level(db, 'sys/app', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/app', False)
    flow_id = create_auth_flow(db, auth_flow_desc='Main Flow')
    with pytest.raises(Exception):
        db.execute('update ac_auth_flow_sts set auth_flow_id=%(flow_id)s where auth_flow_id = %(pk)s', {'pk': 0, 'flow_id': flow_id})


def test_delete_auth_flow_sts_by_ids(db):
    create_auth_level(db, 'sys/app', auth_grant=False)
    pk = create_auth_flow_st(db, 0, 'sys/app', False)
    delete_auth_flow_sts_by_ids(db, (pk,))
    rs = retrieve_auth_flow_sts_by_ids(db, (pk,))
    assert len(rs) == 0


def test_delete_auth_flow_st_when_init_st_should_err(db):
    auth_flows = retrieve_auth_flows_by_ids(db, [0])
    pk = (0, auth_flows[0]['init_st'])
    with pytest.raises(Exception):
        delete_auth_flow_sts_by_ids(db, [pk])
