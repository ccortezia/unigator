from .fixtures import *  # noqa
from unigator_db import (
    create_process,
    retrieve_all_running_process_snapshots,
    retrieve_processes_by_ids,
    create_process_auth_event,
    retrieve_process_histories_by_ids,
    update_process_auth_flow
)


def test_retrieve_all_running_process_snapshots_blank_procs(pg_conn):
    pks = [create_process(pg_conn), create_process(pg_conn), create_process(pg_conn), create_process(pg_conn)]
    retrieve_all_running_process_snapshots(pg_conn)
    rs = retrieve_processes_by_ids(pg_conn, tuple(pks))
    assert len(rs) == 4
    assert [r['proc_id'] for r in rs] == pks


def test_retrieve_process_histories_by_ids(pg_conn):
    pk = create_process(pg_conn)
    create_process_auth_event(pg_conn, pk, 0, 'sys/none')
    create_process_auth_event(pg_conn, pk, 0, 'sys/none')
    create_process_auth_event(pg_conn, pk, 0, 'sys/none')
    rs = retrieve_process_histories_by_ids(pg_conn, (pk,))
    assert len(rs) == 3


def test_retrieve_process_histories_by_ids_flow(pg_conn, basic_flow):
    pk = create_process(pg_conn)
    update_process_auth_flow(pg_conn, pk, basic_flow)

    create_process_auth_event(pg_conn, pk, 0, 'sys/0001')
    rs = retrieve_process_histories_by_ids(pg_conn, (pk,))
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001']

    create_process_auth_event(pg_conn, pk, 0, 'sys/0002')
    rs = retrieve_process_histories_by_ids(pg_conn, (pk,))
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001', 'sys/0002']

    create_process_auth_event(pg_conn, pk, 0, 'sys/0003')
    rs = retrieve_process_histories_by_ids(pg_conn, (pk,))
    assert [r['curr_auth_flow_st'] for r in rs] == ['sys/0001', 'sys/0002', 'sys/0003']
