import pytest
from .fixtures import *  # flake8: noqa


def test_create_auth_flow_tr(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    pk = create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')
    rs = retrieve_auth_flow_trs_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_flow_id'] == pk[0]
    assert rs[0]['when_ev'] == pk[1]
    assert rs[0]['curr_st'] == pk[2]
    assert rs[0]['next_st'] == pk[3]


def test_retrieve_auth_flow_trs_by_ids(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    pk1 = create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')

    create_auth_level(db, 'sys/10', auth_grant=False)
    create_auth_level(db, 'sys/20', auth_grant=False)
    create_auth_level(db, 'sys/30', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/10', st_term=False)
    create_auth_flow_st(db, 0, 'sys/20', st_term=False)
    create_auth_flow_st(db, 0, 'sys/30', st_term=False)
    pk2 = create_auth_flow_tr(db, 0, 'sys/10', 'sys/20', 'sys/30')

    rs = retrieve_auth_flow_trs_by_ids(db, [pk1, pk2])
    assert rs[0]['auth_flow_id'] == 0
    assert rs[0]['when_ev'] == 'sys/1'
    assert rs[0]['curr_st'] == 'sys/2'
    assert rs[0]['next_st'] == 'sys/3'
    assert rs[1]['auth_flow_id'] == 0
    assert rs[1]['when_ev'] == 'sys/10'
    assert rs[1]['curr_st'] == 'sys/20'
    assert rs[1]['next_st'] == 'sys/30'


def test_retrieve_auth_flow_trs_by_auth_flow_id(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')

    create_auth_level(db, 'sys/10', auth_grant=False)
    create_auth_level(db, 'sys/20', auth_grant=False)
    create_auth_level(db, 'sys/30', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/10', st_term=False)
    create_auth_flow_st(db, 0, 'sys/20', st_term=False)
    create_auth_flow_st(db, 0, 'sys/30', st_term=False)
    create_auth_flow_tr(db, 0, 'sys/10', 'sys/20', 'sys/30')

    rs = retrieve_auth_flow_trs_by_auth_flow_id(db, 0)
    assert rs[0] == {'auth_flow_id': 0, 'when_ev': 'sys/1', 'curr_st': 'sys/2', 'next_st': 'sys/3'}
    assert rs[1] == {'auth_flow_id': 0, 'when_ev': 'sys/10', 'curr_st': 'sys/20', 'next_st': 'sys/30'}


def test_update_auth_flow_tr(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_level(db, 'sys/10', auth_grant=False)
    create_auth_level(db, 'sys/20', auth_grant=False)
    create_auth_level(db, 'sys/30', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    create_auth_flow_st(db, 0, 'sys/10', st_term=False)
    create_auth_flow_st(db, 0, 'sys/20', st_term=False)
    create_auth_flow_st(db, 0, 'sys/30', st_term=False)
    pk = create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')
    update_auth_flow_tr(db, pk, 'sys/10', 'sys/20', 'sys/30')
    rs = retrieve_auth_flow_trs_by_ids(db, ((0, 'sys/10', 'sys/20', 'sys/30'),))
    assert rs[0]['auth_flow_id'] == 0
    assert rs[0]['when_ev'] == 'sys/10'
    assert rs[0]['curr_st'] == 'sys/20'
    assert rs[0]['next_st'] == 'sys/30'


def test_update_auth_flow_tr_pk_should_err(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')
    flow_id = create_auth_flow(db, auth_flow_desc='Main Flow')
    create_auth_flow_st(db, flow_id, 'sys/1', st_term=False)
    create_auth_flow_st(db, flow_id, 'sys/2', st_term=False)
    create_auth_flow_st(db, flow_id, 'sys/3', st_term=False)
    with pytest.raises(Exception):
        db.execute('update ac_auth_flow_trs set auth_flow_id=%(flow_id)s where auth_flow_id = 0',
                   {'flow_id': flow_id})


def test_delete_auth_flow_trs_by_ids(db):
    create_auth_level(db, 'sys/1', auth_grant=False)
    create_auth_level(db, 'sys/2', auth_grant=False)
    create_auth_level(db, 'sys/3', auth_grant=False)
    create_auth_flow_st(db, 0, 'sys/1', st_term=False)
    create_auth_flow_st(db, 0, 'sys/2', st_term=False)
    create_auth_flow_st(db, 0, 'sys/3', st_term=False)
    pk = create_auth_flow_tr(db, 0, 'sys/1', 'sys/2', 'sys/3')
    delete_auth_flow_trs_by_ids(db, (pk,))
    rs = retrieve_auth_flow_trs_by_ids(db, (pk,))
    assert len(rs) == 0
