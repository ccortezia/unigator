import pytest
from .fixtures import *  # flake8: noqa


def test_retrieve_process_snapshots_running_by_ids_blank_procs(db):
    pks = [create_process(db), create_process(db), create_process(db), create_process(db)]
    retrieve_process_snapshots_running_by_ids(db, [0])
    rs = retrieve_processes_by_ids(db, pks)
    assert len(rs) == 4
    assert [r['proc_id'] for r in rs] == pks


def test_retrieve_process_histories_by_ids(db):
    pk = create_process(db)
    create_process_auth_event(db, pk, 0, 'sys/none')
    create_process_auth_event(db, pk, 0, 'sys/none')
    create_process_auth_event(db, pk, 0, 'sys/none')
    rs = retrieve_process_histories_by_ids(db, [pk])
    assert len(rs) == 3


def test_retrieve_process_histories_by_ids_flow(db, basic_flow):
    pk = create_process(db)
    update_process_auth_flow(db, pk, basic_flow)

    create_process_auth_event(db, pk, 0, 'sys/0001')
    rs = retrieve_process_histories_by_ids(db, [pk])
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001']

    create_process_auth_event(db, pk, 0, 'sys/0002')
    rs = retrieve_process_histories_by_ids(db, [pk])
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001', 'sys/0002']

    create_process_auth_event(db, pk, 0, 'sys/0003')
    rs = retrieve_process_histories_by_ids(db, [pk])
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001', 'sys/0002', 'sys/0003']
