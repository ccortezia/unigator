import pytest
from unigator_db import (
    create_auth_level,
    create_auth_flow,
    create_auth_flow_st,
    create_auth_flow_tr,
    retrieve_auth_flow_trs_by_auth_flow_id,
    update_auth_flow_tr,
    delete_auth_flow_tr_by_id
)


def test_create_auth_flow_tr(pg_conn):
    create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    create_auth_level(pg_conn, 'sys/3', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/1', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/2', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/3', st_term=False)
    create_auth_flow_tr(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3')
    rs = retrieve_auth_flow_trs_by_auth_flow_id(pg_conn, 0)
    assert len(rs) == 1
    assert rs[0]['auth_flow_id'] == 0
    assert rs[0]['curr_st'] == 'sys/1'
    assert rs[0]['when_ev'] == 'sys/2'
    assert rs[0]['next_st'] == 'sys/3'


def test_retrieve_auth_flow_trs_by_auth_flow_id(pg_conn):
    create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    create_auth_level(pg_conn, 'sys/3', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/1', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/2', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/3', st_term=False)
    create_auth_flow_tr(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3')

    create_auth_level(pg_conn, 'sys/10', auth_grant=False)
    create_auth_level(pg_conn, 'sys/20', auth_grant=False)
    create_auth_level(pg_conn, 'sys/30', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/10', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/20', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/30', st_term=False)
    create_auth_flow_tr(pg_conn, 0, 'sys/20', 'sys/10', 'sys/30')

    rs = retrieve_auth_flow_trs_by_auth_flow_id(pg_conn, 0)
    assert rs[0]['auth_flow_id'] == 0
    assert rs[0]['curr_st'] == 'sys/1'
    assert rs[0]['when_ev'] == 'sys/2'
    assert rs[0]['next_st'] == 'sys/3'
    assert rs[1]['auth_flow_id'] == 0
    assert rs[1]['curr_st'] == 'sys/10'
    assert rs[1]['when_ev'] == 'sys/20'
    assert rs[1]['next_st'] == 'sys/30'


def test_update_auth_flow_tr(pg_conn):
    create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    create_auth_level(pg_conn, 'sys/3', auth_grant=False)
    create_auth_level(pg_conn, 'sys/10', auth_grant=False)
    create_auth_level(pg_conn, 'sys/20', auth_grant=False)
    create_auth_level(pg_conn, 'sys/30', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/1', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/2', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/3', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/10', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/20', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/30', st_term=False)
    create_auth_flow_tr(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3')
    update_auth_flow_tr(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3',
                        new_when_ev='sys/20',
                        new_curr_st='sys/10',
                        new_next_st='sys/30')
    rs = retrieve_auth_flow_trs_by_auth_flow_id(pg_conn, 0)
    assert rs[0]['auth_flow_id'] == 0
    assert rs[0]['curr_st'] == 'sys/10'
    assert rs[0]['when_ev'] == 'sys/20'
    assert rs[0]['next_st'] == 'sys/30'


def test_update_auth_flow_tr_pk_should_err(pg_conn):
    # create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    # create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    # create_auth_level(pg_conn, 'sys/3', auth_grant=False)
    # create_auth_flow_st(pg_conn, 0, 'sys/1', st_term=False)
    # create_auth_flow_st(pg_conn, 0, 'sys/2', st_term=False)
    # create_auth_flow_st(pg_conn, 0, 'sys/3', st_term=False)
    # create_auth_flow_tr(pg_conn, 0, 'sys/1', 'sys/2', 'sys/3')
    flow_id = create_auth_flow(pg_conn, auth_flow_desc='Main Flow')
    # create_auth_flow_st(pg_conn, flow_id, 'sys/1', st_term=False)
    # create_auth_flow_st(pg_conn, flow_id, 'sys/2', st_term=False)
    # create_auth_flow_st(pg_conn, flow_id, 'sys/3', st_term=False)
    with pytest.raises(Exception):
        pg_conn.execute(
            'update ac_auth_flow_trs set auth_flow_id=%(flow_id)s where auth_flow_id = 0',
            {'flow_id': flow_id})


def test_delete_auth_flow_tr_by_id(pg_conn):
    create_auth_level(pg_conn, 'sys/1', auth_grant=False)
    create_auth_level(pg_conn, 'sys/2', auth_grant=False)
    create_auth_level(pg_conn, 'sys/3', auth_grant=False)
    create_auth_flow_st(pg_conn, 0, 'sys/1', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/2', st_term=False)
    create_auth_flow_st(pg_conn, 0, 'sys/3', st_term=False)
    create_auth_flow_tr(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3')
    delete_auth_flow_tr_by_id(pg_conn, 0, 'sys/2', 'sys/1', 'sys/3')
    rs = retrieve_auth_flow_trs_by_auth_flow_id(pg_conn, 0)
    assert len(rs) == 0
