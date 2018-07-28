import time
import pytest
from .fixtures import *  # flake8: noqa


def test_create_process(db):
    pk = create_process(db)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['proc_id'] == pk


def test_create_process_should_use_auth_flow_setting(db):
    pk = create_process(db)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert rs[0]['auth_flow'] == retrieve_auth_flow_setting_active_flow(db)

    auth_flow_1 = create_auth_flow(db, 'Flow 1')
    update_auth_flow_setting_active_flow(db, auth_flow_1)
    pk = create_process(db)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert rs[0]['auth_flow'] == auth_flow_1

    auth_flow_2 = create_auth_flow(db, 'Flow 2')
    update_auth_flow_setting_active_flow(db, auth_flow_2)
    pk = create_process(db)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert rs[0]['auth_flow'] == auth_flow_2


def test_retrieve_processes_by_ids(db):
    pks = [create_process(db), create_process(db), create_process(db), create_process(db)]
    rs = retrieve_processes_by_ids(db, pks)
    assert len(rs) == 4
    assert [r['proc_id'] for r in rs] == pks


def test_update_process(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    update_process(db, pk, ctc, orig, dest, ckp, vhc)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['proc_id'] == pk
    assert rs[0]['ctc'] == ctc
    assert rs[0]['vhc'] == vhc
    assert rs[0]['ckp'] == ckp
    assert rs[0]['loc_orig'] == orig
    assert rs[0]['loc_dest'] == dest


def test_update_process_terminate(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, ckp, vhc)
    update_process_terminate(db, pk)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert rs[0]['finished_at']


def test_update_process_terminate_no_vhc(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, ckp, None)
    update_process_terminate(db, pk)
    rs = retrieve_processes_by_ids(db, (pk,))
    assert rs[0]['finished_at']


def test_update_process_terminate_no_ctc(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, None, orig, dest, ckp, vhc)
    with pytest.raises(Exception):
        update_process_terminate(db, pk)


def test_update_process_terminate(db):
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, None, dest, ckp, vhc)
    with pytest.raises(Exception):
        update_process_terminate(db, pk)


def test_update_process_terminate_no_dest(db):
    orig = create_location(db, 'Origin')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, None, ckp, vhc)
    with pytest.raises(Exception):
        update_process_terminate(db, pk)


def test_update_process_terminate(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, None, vhc)
    with pytest.raises(Exception):
        update_process_terminate(db, pk)


def test_update_process_finished_err(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, ckp, vhc)
    update_process_terminate(db, pk)
    with pytest.raises(Exception):
        update_process(db, pk, ctc, orig, dest, ckp, vhc)


def test_delete_processes_by_id(db):
    pks = [create_process(db), create_process(db), create_process(db), create_process(db)]
    delete_processes_by_ids(db, pks)
    rs = retrieve_processes_by_ids(db, pks)
    assert len(rs) == 0
