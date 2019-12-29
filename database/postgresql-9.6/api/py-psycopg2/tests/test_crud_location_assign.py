# import pytest
from .fixtures import *  # noqa
from unigator_db import (
    # create_location,
    # create_contact,
    create_location_assign_type,
    retrieve_all_location_assign_types,
    update_location_assign_type,
    delete_location_assign_types_by_assign_types,
    assign_contact_to_location,
    retrieve_location_contact_assignments,
    retrieve_location_contact_assignments_by_contact_id,
    delete_contact_location_assignment
)


def test_create_location_assign_type(pg_conn):
    create_location_assign_type(pg_conn, 'caretaker')


def test_retrieve_all_location_assign_types(pg_conn):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    rs = retrieve_all_location_assign_types(pg_conn)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'caretaker'
    assert rs[0]['assign_desc'] == 'Master Caretaker'


def test_update_location_assign_type(pg_conn):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    update_location_assign_type(pg_conn, 'caretaker', 'staff', 'Lesser Caretaker')
    rs = retrieve_all_location_assign_types(pg_conn)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'staff'
    assert rs[0]['assign_desc'] == 'Lesser Caretaker'


def test_delete_location_assign_types_by_assign_types(pg_conn):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    create_location_assign_type(pg_conn, 'freq-guest', 'Frequent Guest')
    delete_location_assign_types_by_assign_types(pg_conn, ('freq-guest',))
    rs = retrieve_all_location_assign_types(pg_conn)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'caretaker'


def test_assign_contact_to_location(pg_conn, ctc_nogrp, loc_nogrp):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    assign_contact_to_location(pg_conn, loc_nogrp, ctc_nogrp, 'caretaker')


def test_retrieve_location_contact_assignments(pg_conn, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    create_location_assign_type(pg_conn, 'houndmaster', 'Kennel Master')
    assign_contact_to_location(pg_conn, loc_a1, ctc_a1, 'caretaker')
    assign_contact_to_location(pg_conn, loc_b1, ctc_a1, 'houndmaster')
    assign_contact_to_location(pg_conn, loc_b1, ctc_b1, 'caretaker')
    rs = retrieve_location_contact_assignments(pg_conn, loc_a1)
    assert rs == [{'contact_id': ctc_a1, 'contact_name': 'ctc_a1', 'assign_type': 'caretaker'}]
    rs = retrieve_location_contact_assignments(pg_conn, loc_b1)
    assert len(rs) == 2
    assert rs[0] == {'contact_id': ctc_a1, 'contact_name': 'ctc_a1', 'assign_type': 'houndmaster'}
    assert rs[1] == {'contact_id': ctc_b1, 'contact_name': 'ctc_b1', 'assign_type': 'caretaker'}


def test_retrieve_location_contact_assignments_by_contact_id(pg_conn, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    create_location_assign_type(pg_conn, 'houndmaster', 'Kennel Master')
    assign_contact_to_location(pg_conn, loc_a1, ctc_a1, 'caretaker')
    assign_contact_to_location(pg_conn, loc_b1, ctc_a1, 'houndmaster')
    assign_contact_to_location(pg_conn, loc_b1, ctc_b1, 'caretaker')
    rs = retrieve_location_contact_assignments_by_contact_id(pg_conn, ctc_a1)
    assert len(rs) == 2
    assert rs[0] == {'location_id': loc_a1, 'addr_1': 'loc_a1', 'addr_2': None, 'addr_3': None, 'addr_4': None, 'addr_5': None, 'addr_6': None, 'assign_type': 'caretaker'}
    assert rs[1] == {'location_id': loc_b1, 'addr_1': 'loc_b1', 'addr_2': None, 'addr_3': None, 'addr_4': None, 'addr_5': None, 'addr_6': None, 'assign_type': 'houndmaster'}
    rs = retrieve_location_contact_assignments_by_contact_id(pg_conn, ctc_b1)
    assert len(rs) == 1
    assert rs[0] == {'location_id': loc_b1, 'addr_1': 'loc_b1', 'addr_2': None, 'addr_3': None, 'addr_4': None, 'addr_5': None, 'addr_6': None, 'assign_type': 'caretaker'}


def test_delete_contact_location_assignment(pg_conn, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(pg_conn, 'caretaker', 'Master Caretaker')
    create_location_assign_type(pg_conn, 'houndmaster', 'Kennel Master')
    assign_contact_to_location(pg_conn, loc_a1, ctc_a1, 'caretaker')
    assign_contact_to_location(pg_conn, loc_b1, ctc_a1, 'houndmaster')
    assign_contact_to_location(pg_conn, loc_b1, ctc_b1, 'caretaker')
    delete_contact_location_assignment(pg_conn, loc_b1, ctc_b1, 'caretaker')
    rs = retrieve_location_contact_assignments(pg_conn, loc_b1)
    assert rs == [{'contact_id': ctc_a1, 'contact_name': 'ctc_a1', 'assign_type': 'houndmaster'}]
