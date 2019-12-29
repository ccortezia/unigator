import time
import pytest
from unigator_db import (
    create_auth_level,
    create_auth_flow_st,
    create_auth_flow_tr,
    create_process,
    update_process,
    create_location,
    create_vehicle,
    create_contact,
    create_checkpoint,
    terminate_process,
    archive_finished_processes,
    create_process_auth_event,
)


@pytest.fixture
def basic_flow(pg_conn):
    create_auth_level(pg_conn, 'sys/acc', auth_grant=True)
    create_auth_flow_st(pg_conn, 0, 'sys/acc', st_term=True)
    create_auth_flow_tr(pg_conn, 0, 'sys/acc', 'sys/none', 'sys/acc')
    return 0


def test_process_archive_with_unresolved_terminated_process_should_archive_none(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.1)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)
    terminate_process(pg_conn, pk)
    results = archive_finished_processes(pg_conn)
    assert results == []


def test_process_archive_with_resolved_terminated_process_should_archive_one(pg_conn, basic_flow):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.1)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(pg_conn, pk, ctc, 'sys/acc')
    terminate_process(pg_conn, pk)
    results = archive_finished_processes(pg_conn)
    assert results[0]['archived_proc_id'] == pk


def test_process_archive_with_resolved_terminated_process_should_archive_two(pg_conn, basic_flow):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')

    pk0 = create_process(pg_conn)
    time.sleep(0.1)
    update_process(pg_conn, pk0, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(pg_conn, pk0, ctc, 'sys/acc')
    terminate_process(pg_conn, pk0)

    pk1 = create_process(pg_conn)
    time.sleep(0.1)
    update_process(pg_conn, pk1, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(pg_conn, pk1, ctc, 'sys/acc')
    terminate_process(pg_conn, pk1)

    results = archive_finished_processes(pg_conn)
    assert results[0]['archived_proc_id'] == pk0
    assert results[1]['archived_proc_id'] == pk1
