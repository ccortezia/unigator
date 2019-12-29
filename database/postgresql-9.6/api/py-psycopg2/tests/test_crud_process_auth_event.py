import time
import pytest
from .utils import fetch_scalar
from unigator_db import (
    create_process,
    update_process,
    terminate_process,
    create_process_auth_event,
    create_location,
    create_contact,
    create_checkpoint,
    create_vehicle
)


def test_create_process_auth_event(pg_conn):
    proc_id = create_process(pg_conn)
    create_process_auth_event(pg_conn, proc_id, 0, 'sys/none')
    create_process_auth_event(pg_conn, proc_id, 0, 'sys/none')
    create_process_auth_event(pg_conn, proc_id, 0, 'sys/none')
    assert fetch_scalar(pg_conn, 'select count(*) from ac_process_auth_events;') == 3


def test_create_process_auth_events_on_finished_process_err(pg_conn):
    orig = create_location(pg_conn, 'Origin')
    dest = create_location(pg_conn, 'Dest')
    ctc = create_contact(pg_conn, 'Subject')
    ckp = create_checkpoint(pg_conn, 'Gate 1')
    vhc = create_vehicle(pg_conn, 'UUU0000')
    proc_id = create_process(pg_conn)
    time.sleep(0.1)
    update_process(pg_conn, proc_id, ctc, orig, dest, ckp, vhc)
    terminate_process(pg_conn, proc_id)
    with pytest.raises(Exception):
        create_process_auth_event(pg_conn, proc_id, 0, 'sys/none')
