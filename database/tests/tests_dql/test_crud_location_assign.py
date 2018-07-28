import pytest
from .fixtures import *  # flake8: noqa


def test_create_location_assign_type(db):
    create_location_assign_type(db, 'caretaker')


def test_retrieve_location_assign_types(db):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    rs = retrieve_location_assign_types(db)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'caretaker'
    assert rs[0]['assign_desc'] == 'Master Caretaker'


def test_update_location_assign_type(db):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    update_location_assign_type(db, 'caretaker', 'staff', 'Lesser Caretaker')
    rs = retrieve_location_assign_types(db)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'staff'
    assert rs[0]['assign_desc'] == 'Lesser Caretaker'


def test_delete_location_assign_types_by_assign_types(db):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    create_location_assign_type(db, 'freq-guest', 'Frequent Guest')
    delete_location_assign_types_by_assign_types(db, ['freq-guest'])
    rs = retrieve_location_assign_types(db)
    assert len(rs) == 1
    assert rs[0]['assign_type'] == 'caretaker'


def test_create_contact_location_assignment(db, ctc_nogrp, loc_nogrp):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    create_contact_location_assignment(db, loc_nogrp, ctc_nogrp, 'caretaker')


def test_retrieve_contact_location_assignments_by_location_id(db, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    create_location_assign_type(db, 'houndmaster', 'Kennel Master')
    create_contact_location_assignment(db, loc_a1, ctc_a1, 'caretaker')
    create_contact_location_assignment(db, loc_b1, ctc_a1, 'houndmaster')
    create_contact_location_assignment(db, loc_b1, ctc_b1, 'caretaker')
    rs = retrieve_contact_location_assignments_by_location_id(db, loc_a1)
    assert rs == [{'contact_id': ctc_a1, 'assign_type': 'caretaker'}]
    rs = retrieve_contact_location_assignments_by_location_id(db, loc_b1)
    assert len(rs) == 2
    assert rs[0] == {'contact_id': ctc_b1, 'assign_type': 'caretaker'}
    assert rs[1] == {'contact_id': ctc_a1, 'assign_type': 'houndmaster'}


def test_retrieve_contact_location_assignments_by_contact_id(db, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    create_location_assign_type(db, 'houndmaster', 'Kennel Master')
    create_contact_location_assignment(db, loc_a1, ctc_a1, 'caretaker')
    create_contact_location_assignment(db, loc_b1, ctc_a1, 'houndmaster')
    create_contact_location_assignment(db, loc_b1, ctc_b1, 'caretaker')
    rs = retrieve_contact_location_assignments_by_contact_id(db, ctc_a1)
    assert len(rs) == 2
    assert rs[0] == {'location_id': loc_a1, 'assign_type': 'caretaker'}
    assert rs[1] == {'location_id': loc_b1, 'assign_type': 'houndmaster'}
    rs = retrieve_contact_location_assignments_by_contact_id(db, ctc_b1)
    assert len(rs) == 1
    assert rs[0] == {'location_id': loc_b1, 'assign_type': 'caretaker'}


def test_delete_contact_location_assignments_by_ids(db, ctc_a1, ctc_b1, loc_a1, loc_b1):
    create_location_assign_type(db, 'caretaker', 'Master Caretaker')
    create_location_assign_type(db, 'houndmaster', 'Kennel Master')
    create_contact_location_assignment(db, loc_a1, ctc_a1, 'caretaker')
    create_contact_location_assignment(db, loc_b1, ctc_a1, 'houndmaster')
    create_contact_location_assignment(db, loc_b1, ctc_b1, 'caretaker')
    delete_contact_location_assignments_by_ids(db, [(loc_b1, ctc_b1, 'caretaker')])
    rs = retrieve_contact_location_assignments_by_location_id(db, loc_b1)
    assert rs == [{'contact_id': ctc_a1, 'assign_type': 'houndmaster'}]
