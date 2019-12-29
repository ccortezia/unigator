import time
import pytest
from unigator_db import (
    create_process,
    update_process,
    delete_processes_by_ids,
    retrieve_processes_by_ids,
    retrieve_current_active_auth_flow,
    create_auth_flow,
    update_current_active_auth_flow,
    create_location,
    create_vehicle,
    create_contact,
    create_checkpoint,
    terminate_process,
)


def test_create_process(pg_conn):
    pk = create_process(pg_conn)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['proc_id'] == pk


def test_create_process_should_use_auth_flow_setting(pg_conn):
    pk = create_process(pg_conn)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    active_flow = retrieve_current_active_auth_flow(pg_conn)
    assert rs[0]['auth_flow'] == active_flow['auth_flow_id']

    auth_flow_1 = create_auth_flow(pg_conn, 'Flow 1')
    update_current_active_auth_flow(pg_conn, auth_flow_1)
    pk = create_process(pg_conn)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert rs[0]['auth_flow'] == auth_flow_1

    auth_flow_2 = create_auth_flow(pg_conn, 'Flow 2')
    update_current_active_auth_flow(pg_conn, auth_flow_2)
    pk = create_process(pg_conn)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert rs[0]['auth_flow'] == auth_flow_2


def test_retrieve_processes_by_ids(pg_conn):
    pks = [create_process(pg_conn), create_process(pg_conn), create_process(pg_conn), create_process(pg_conn)]
    rs = retrieve_processes_by_ids(pg_conn, tuple(pks))
    assert len(rs) == 4
    assert [r['proc_id'] for r in rs] == pks


def test_update_process(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['proc_id'] == pk
    assert rs[0]['ctc'] == ctc
    assert rs[0]['vhc'] == vhc
    assert rs[0]['ckp'] == ckp
    assert rs[0]['loc_orig'] == orig
    assert rs[0]['loc_dest'] == dest


def test_terminate_process(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)
    terminate_process(pg_conn, pk)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert rs[0]['finished_at']


def test_terminate_process_no_vhc(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, None)
    terminate_process(pg_conn, pk)
    rs = retrieve_processes_by_ids(pg_conn, (pk,))
    assert rs[0]['finished_at']


def test_terminate_process_no_ctc(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, None, orig, dest, ckp, vhc)
    with pytest.raises(Exception):
        terminate_process(pg_conn, pk)


def test_terminate_process_no_orig(pg_conn):
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, None, dest, ckp, vhc)
    with pytest.raises(Exception):
        terminate_process(pg_conn, pk)


def test_terminate_process_no_dest(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, orig, None, ckp, vhc)
    with pytest.raises(Exception):
        terminate_process(pg_conn, pk)


def test_terminate_process_no_ckp(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, orig, dest, None, vhc)
    with pytest.raises(Exception):
        terminate_process(pg_conn, pk)


def test_update_process_finished_err(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    pk = create_process(pg_conn)
    time.sleep(0.01)
    update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)
    terminate_process(pg_conn, pk)
    with pytest.raises(Exception):
        update_process(pg_conn, pk, ctc, orig, dest, ckp, vhc)


def test_delete_processes_by_id(pg_conn):
    pks = [create_process(pg_conn), create_process(pg_conn), create_process(pg_conn), create_process(pg_conn)]
    delete_processes_by_ids(pg_conn, tuple(pks))
    rs = retrieve_processes_by_ids(pg_conn, tuple(pks))
    assert len(rs) == 0
