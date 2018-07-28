import time
import pytest
from .fixtures import *  # flake8: noqa


@pytest.fixture
def basic_flow(db):
    create_auth_level(db, 'sys/acc', auth_grant=True)
    create_auth_flow_st(db, 0, 'sys/acc', st_term=True)
    create_auth_flow_tr(db, 0, 'sys/acc', 'sys/none', 'sys/acc')
    return 0


def test_process_archive_with_unresolved_terminated_process_should_archive_none(db):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, ckp, vhc)
    update_process_terminate(db, pk)
    results = archive_finished_processes(db)
    assert results == []


def test_process_archive_with_resolved_terminated_process_should_archive_one(db, basic_flow):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')
    pk = create_process(db)
    time.sleep(0.01)
    update_process(db, pk, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(db, pk, ctc, 'sys/acc')
    update_process_terminate(db, pk)
    results = archive_finished_processes(db)
    assert results[0]['archived_proc_id'] == pk


def test_process_archive_with_resolved_terminated_process_should_archive_two(db, basic_flow):
    orig = create_location(db, 'Origin')
    dest = create_location(db, 'Dest')
    ctc = create_contact(db, 'Subject')
    ckp = create_checkpoint(db, 'Gate 1')
    vhc = create_vehicle(db, 'UUU0000')

    pk0 = create_process(db)
    time.sleep(0.01)
    update_process(db, pk0, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(db, pk0, ctc, 'sys/acc')
    update_process_terminate(db, pk0)

    pk1 = create_process(db)
    time.sleep(0.01)
    update_process(db, pk1, ctc, orig, dest, ckp, vhc)
    create_process_auth_event(db, pk1, ctc, 'sys/acc')
    update_process_terminate(db, pk1)

    results = archive_finished_processes(db)
    assert results[0]['archived_proc_id'] == pk0
    assert results[1]['archived_proc_id'] == pk1

