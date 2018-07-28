import time
import pytest
from .fixtures import *  # flake8: noqa


def test_create_process_auth_event(db):
    pk = create_process(db)
    create_process_auth_event(db, pk, 0, 'sys/none')
    create_process_auth_event(db, pk, 0, 'sys/none')
    create_process_auth_event(db, pk, 0, 'sys/none')
    assert db.sql_scalar('select count(*) from ac_process_auth_events;') == 3


def test_create_process_auth_events_on_finished_process_err(db):
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
        create_process_auth_event(db, pk, 0, 'sys/none')
