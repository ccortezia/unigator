import time
import pytest
import datetime
import unigator_db as dql_binds
from unigator_db import SQLDefault


# NOTE: these are meant to be voxsql annotation-compliance tests, and not full tests for the
# underlying database model/domain. These are not definitive tests, and are likely to be replaced
# by automatically generated tests aimed at verifying voxsql annotations comply to the annotated
# body expected and input/output. Until voxsql support test case generation these tests will be
# maintained manually.


# ----

def test_create_contact(pg_conn):
    created_id = dql_binds.create_contact(pg_conn, contact_name='Joe Manzana')
    assert(isinstance(created_id, int))


def test_retrieve_contacts_by_ids(pg_conn):
    created_id = dql_binds.create_contact(pg_conn, 'Mary Garcia')
    records = dql_binds.retrieve_contacts_by_ids(pg_conn, (created_id,))
    assert(len(records) == 1)
    assert(records[0]['contact_id'] == created_id)
    assert(records[0]['contact_name'] == 'Mary Garcia')


@pytest.mark.parametrize('contact_name', ['Mary', 'Mary Garcia', 'João Grü Jabé'])
def test_retrieve_contacts_by_name(pg_conn, contact_name):
    created_id = dql_binds.create_contact(pg_conn, contact_name)
    records = dql_binds.retrieve_contacts_by_name(pg_conn,
                                                  contact_name,
                                                  page_pos=(contact_name, 0),
                                                  page_size=100)
    assert(len(records) == 1)
    assert(records[0]['contact_id'] == created_id)
    assert(records[0]['contact_name'] == contact_name)


def test_update_contact(pg_conn):
    created_id = dql_binds.create_contact(pg_conn, 'Mary Garcia')
    result = dql_binds.update_contact(pg_conn, contact_id=created_id, contact_name='Ann Garden')
    assert result is None


def test_delete_contacts_by_ids(pg_conn):
    created_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    result = dql_binds.delete_contacts_by_ids(pg_conn, (created_id,))
    assert result is None


# ----

def test_create_contact_group(pg_conn):
    created_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    assert(isinstance(created_name, str))


def test_retrieve_all_contact_groups(pg_conn):
    dql_binds.create_contact_group(pg_conn, 'Visitors')
    dql_binds.create_contact_group(pg_conn, 'Employees')
    records = dql_binds.retrieve_all_contact_groups(pg_conn)
    assert(len(records) == 2)
    assert(records[0]['group_name'] == 'Employees')
    assert(records[1]['group_name'] == 'Visitors')


def test_update_contact_group(pg_conn):
    created_name = dql_binds.create_contact_group(pg_conn, 'Mary Garcia')
    result = dql_binds.update_contact_group(pg_conn, group_name=created_name, new_group_name='group-2')
    assert result is None


def test_delete_contact_groups_by_group_names(pg_conn):
    created_name = dql_binds.create_contact_group(pg_conn, 'group-1')
    result = dql_binds.delete_contact_groups_by_group_names(pg_conn, (created_name,))
    assert result is None


# ----

def test_add_contact_group_member(pg_conn):
    created_group_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    created_contact_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    result = dql_binds.add_contact_group_member(pg_conn, created_group_name, created_contact_id)
    assert result is None


def test_retrieve_contact_group_members(pg_conn):
    created_group_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    created_contact_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    dql_binds.add_contact_group_member(pg_conn, created_group_name, created_contact_id)
    records = dql_binds.retrieve_contact_group_members(pg_conn, created_group_name)
    assert len(records) == 1
    assert records[0]['contact_name'] == 'Joe Manzana'


def test_retrieve_contact_groups_by_contact_id(pg_conn):
    created_group_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    created_contact_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    dql_binds.add_contact_group_member(pg_conn, created_group_name, created_contact_id)
    records = dql_binds.retrieve_contact_groups_by_contact_id(pg_conn, created_contact_id)
    assert len(records) == 1
    assert records[0]['group_name'] == 'group-1'


def test_remove_contact_group_members(pg_conn):
    created_group_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    created_contact_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    dql_binds.add_contact_group_member(pg_conn, created_group_name, created_contact_id)
    result = dql_binds.remove_contact_group_members(pg_conn, created_group_name, (created_contact_id,))
    assert result is None


def test_remove_contact_from_contact_groups(pg_conn):
    created_group_name = dql_binds.create_contact_group(pg_conn, group_name='group-1')
    created_contact_id = dql_binds.create_contact(pg_conn, 'Joe Manzana')
    dql_binds.add_contact_group_member(pg_conn, created_group_name, created_contact_id)
    result = dql_binds.remove_contact_from_contact_groups(pg_conn, created_contact_id, (created_group_name,))
    assert result is None

# ---

def test_create_location(pg_conn):
    created_id = dql_binds.create_location(pg_conn,
                                           addr_1='Address 1',
                                           addr_2='Address 2',
                                           addr_3='Address 3',
                                           addr_4='Address 4',
                                           addr_5='Address 5',
                                           addr_6='Address 6')
    assert(isinstance(created_id, int))


def test_retrieve_locations_by_ids(pg_conn):
    created_id = dql_binds.create_location(pg_conn, 'Address 1')
    records = dql_binds.retrieve_locations_by_ids(pg_conn, (created_id,))
    assert(len(records) == 1)
    assert(records[0]['location_id'] == created_id)
    assert(records[0]['addr_1'] == 'Address 1')
    assert(records[0]['addr_2'] is None)
    assert(records[0]['addr_3'] is None)
    assert(records[0]['addr_4'] is None)
    assert(records[0]['addr_5'] is None)
    assert(records[0]['addr_6'] is None)


def test_update_location(pg_conn):
    created_id = dql_binds.create_location(pg_conn, 'Address 1')
    result = dql_binds.update_location(pg_conn,
                                       addr_1=created_id,
                                       addr_2=SQLDefault(),
                                       addr_3=SQLDefault(),
                                       addr_4=SQLDefault(),
                                       addr_5=SQLDefault(),
                                       addr_6=SQLDefault())
    assert result is None


def test_delete_locations_by_ids(pg_conn):
    created_id = dql_binds.create_location(pg_conn, 'Address 1')
    result = dql_binds.delete_locations_by_ids(pg_conn, (created_id,))
    assert result is None


# ----

def test_create_location_group(pg_conn):
    created_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    assert(isinstance(created_name, str))


def test_retrieve_all_location_groups(pg_conn):
    dql_binds.create_location_group(pg_conn, 'Area 1')
    dql_binds.create_location_group(pg_conn, 'Area 2')
    records = dql_binds.retrieve_all_location_groups(pg_conn)
    assert(len(records) == 2)
    assert(records[0]['group_name'] == 'Area 1')
    assert(records[1]['group_name'] == 'Area 2')


def test_update_location_group(pg_conn):
    created_name = dql_binds.create_location_group(pg_conn, 'group-1')
    result = dql_binds.update_location_group(pg_conn, group_name=created_name, new_group_name='group-2')
    assert result is None


def test_delete_location_groups_by_group_names(pg_conn):
    created_name = dql_binds.create_location_group(pg_conn, 'group-1')
    result = dql_binds.delete_location_groups_by_group_names(pg_conn, (created_name,))
    assert result is None


# ----

def test_add_location_group_member(pg_conn):
    created_group_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    result = dql_binds.add_location_group_member(pg_conn, created_group_name, created_location_id)
    assert result is None


def test_retrieve_location_group_members(pg_conn):
    created_group_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    dql_binds.add_location_group_member(pg_conn, created_group_name, created_location_id)
    records = dql_binds.retrieve_location_group_members(pg_conn, created_group_name)
    assert len(records) == 1
    assert records[0]['addr_1'] == 'Address 1'
    assert records[0]['addr_2'] is None
    assert records[0]['addr_3'] is None
    assert records[0]['addr_4'] is None
    assert records[0]['addr_5'] is None
    assert records[0]['addr_6'] is None


def test_retrieve_location_groups_by_location_id(pg_conn):
    created_group_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    dql_binds.add_location_group_member(pg_conn, created_group_name, created_location_id)
    records = dql_binds.retrieve_location_groups_by_location_id(pg_conn, created_location_id)
    assert len(records) == 1
    assert records[0]['group_name'] == 'group-1'


def test_remove_location_group_members(pg_conn):
    created_group_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    dql_binds.add_location_group_member(pg_conn, created_group_name, created_location_id)
    result = dql_binds.remove_location_group_members(pg_conn, created_group_name, (created_location_id,))
    assert result is None


def test_remove_location_from_location_groups(pg_conn):
    created_group_name = dql_binds.create_location_group(pg_conn, group_name='group-1')
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    dql_binds.add_location_group_member(pg_conn, created_group_name, created_location_id)
    result = dql_binds.remove_location_from_location_groups(pg_conn, created_location_id, (created_group_name,))
    assert result is None


# ----

def test_create_location_assign_type(pg_conn):
    created_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    assert(isinstance(created_type, str))


def test_retrieve_all_location_assign_types(pg_conn):
    dql_binds.create_location_assign_type(pg_conn, 'Owner')
    dql_binds.create_location_assign_type(pg_conn, 'Guest')
    records = dql_binds.retrieve_all_location_assign_types(pg_conn)
    assert(len(records) == 2)
    assert(records[0]['assign_type'] == 'Guest')
    assert(records[1]['assign_type'] == 'Owner')


def test_update_location_assign_type(pg_conn):
    created_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    result = dql_binds.update_location_assign_type(pg_conn, created_type, new_assign_type='Maintainer')
    assert result is None


def test_delete_location_assign_types_by_assign_types(pg_conn):
    created_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    result = dql_binds.delete_location_assign_types_by_assign_types(pg_conn, (created_type,))
    assert result is None


# ---

def test_assign_contact_to_location(pg_conn):
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    created_contact_id = dql_binds.create_contact(pg_conn, contact_name='Joe Manzana')
    created_assign_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    result = dql_binds.assign_contact_to_location(pg_conn, created_location_id, created_contact_id, created_assign_type)
    assert result is None


def test_retrieve_location_contact_assignments(pg_conn):
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    created_contact_id = dql_binds.create_contact(pg_conn, contact_name='Joe Manzana')
    created_assign_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    dql_binds.assign_contact_to_location(pg_conn, created_location_id, created_contact_id, created_assign_type)
    records = dql_binds.retrieve_location_contact_assignments(pg_conn, created_location_id)
    assert len(records) == 1
    assert records[0]['contact_id'] == created_contact_id
    assert records[0]['contact_name'] == 'Joe Manzana'
    assert records[0]['assign_type'] == 'Owner'


def test_retrieve_location_contact_assignments_by_contact_id(pg_conn):
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    created_contact_id = dql_binds.create_contact(pg_conn, contact_name='Joe Manzana')
    created_assign_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    dql_binds.assign_contact_to_location(pg_conn, created_location_id, created_contact_id, created_assign_type)
    records = dql_binds.retrieve_location_contact_assignments_by_contact_id(pg_conn, created_contact_id)
    assert len(records) == 1
    assert records[0]['location_id'] == created_location_id
    assert records[0]['addr_1'] == 'Address 1'
    assert records[0]['assign_type'] == 'Owner'


def test_delete_contact_location_assignment(pg_conn):
    created_location_id = dql_binds.create_location(pg_conn, 'Address 1')
    created_contact_id = dql_binds.create_contact(pg_conn, contact_name='Joe Manzana')
    created_assign_type = dql_binds.create_location_assign_type(pg_conn, 'Owner')
    dql_binds.assign_contact_to_location(pg_conn, created_location_id, created_contact_id, created_assign_type)
    result = dql_binds.delete_contact_location_assignment(pg_conn, created_location_id, created_contact_id, created_assign_type)
    assert result is None


# ----

def test_create_vehicle(pg_conn):
    created_id = dql_binds.create_vehicle(pg_conn, plate='CCC1010')
    assert(isinstance(created_id, int))


def test_retrieve_vehicles_by_ids(pg_conn):
    created_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    records = dql_binds.retrieve_vehicles_by_ids(pg_conn, (created_id,))
    assert(len(records) == 1)
    assert(records[0]['vehicle_id'] == created_id)
    assert(records[0]['plate'] == 'CCC1010')


def test_update_vehicle(pg_conn):
    created_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    result = dql_binds.update_vehicle(pg_conn, vehicle_id=created_id, plate='CCC1020')
    assert result is None


def test_delete_vehicles_by_ids(pg_conn):
    created_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    result = dql_binds.delete_vehicles_by_ids(pg_conn, (created_id,))
    assert result is None


# ----

def test_create_vehicle_group(pg_conn):
    created_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    assert(isinstance(created_name, str))


def test_retrieve_all_vehicle_groups(pg_conn):
    dql_binds.create_vehicle_group(pg_conn, 'group-2')
    dql_binds.create_vehicle_group(pg_conn, 'group-1')
    records = dql_binds.retrieve_all_vehicle_groups(pg_conn)
    assert(len(records) == 2)
    assert(records[0]['group_name'] == 'group-1')
    assert(records[1]['group_name'] == 'group-2')


def test_update_vehicle_group(pg_conn):
    created_name = dql_binds.create_vehicle_group(pg_conn, 'group-1')
    result = dql_binds.update_vehicle_group(pg_conn, group_name=created_name, new_group_name='group-2')
    assert result is None


def test_delete_vehicle_groups_by_group_names(pg_conn):
    created_name = dql_binds.create_vehicle_group(pg_conn, 'group-1')
    result = dql_binds.delete_vehicle_groups_by_group_names(pg_conn, (created_name,))
    assert result is None


# ----

def test_add_vehicle_group_member(pg_conn):
    created_group_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    created_vehicle_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    result = dql_binds.add_vehicle_group_member(pg_conn, created_group_name, created_vehicle_id)
    assert result is None


def test_retrieve_vehicle_group_members(pg_conn):
    created_group_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    created_vehicle_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    dql_binds.add_vehicle_group_member(pg_conn, created_group_name, created_vehicle_id)
    records = dql_binds.retrieve_vehicle_group_members(pg_conn, created_group_name)
    assert len(records) == 1
    assert records[0]['plate'] == 'CCC1010'


def test_retrieve_vehicle_groups_by_vehicle_id(pg_conn):
    created_group_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    created_vehicle_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    dql_binds.add_vehicle_group_member(pg_conn, created_group_name, created_vehicle_id)
    records = dql_binds.retrieve_vehicle_groups_by_vehicle_id(pg_conn, created_vehicle_id)
    assert len(records) == 1
    assert records[0]['group_name'] == 'group-1'


def test_remove_vehicle_group_members(pg_conn):
    created_group_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    created_vehicle_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    dql_binds.add_vehicle_group_member(pg_conn, created_group_name, created_vehicle_id)
    result = dql_binds.remove_vehicle_group_members(pg_conn, created_group_name, (created_vehicle_id,))
    assert result is None


def test_remove_vehicle_from_vehicle_groups(pg_conn):
    created_group_name = dql_binds.create_vehicle_group(pg_conn, group_name='group-1')
    created_vehicle_id = dql_binds.create_vehicle(pg_conn, 'CCC1010')
    dql_binds.add_vehicle_group_member(pg_conn, created_group_name, created_vehicle_id)
    result = dql_binds.remove_vehicle_from_vehicle_groups(pg_conn, created_vehicle_id, (created_group_name,))
    assert result is None


# ----

def test_create_checkpoint(pg_conn):
    created_id = dql_binds.create_checkpoint(pg_conn, checkpoint_name='Entrance A')
    assert(isinstance(created_id, int))


def test_retrieve_checkpoints_by_ids(pg_conn):
    created_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    records = dql_binds.retrieve_checkpoints_by_ids(pg_conn, (created_id,))
    assert(len(records) == 1)
    assert(records[0]['checkpoint_id'] == created_id)
    assert(records[0]['checkpoint_name'] == 'Entrance A')


def test_update_checkpoint(pg_conn):
    created_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    result = dql_binds.update_checkpoint(pg_conn, checkpoint_id=created_id, checkpoint_name='CCC1020')
    assert result is None


def test_delete_checkpoints_by_ids(pg_conn):
    created_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    result = dql_binds.delete_checkpoints_by_ids(pg_conn, (created_id,))
    assert result is None


# ----

def test_create_checkpoint_group(pg_conn):
    created_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    assert(isinstance(created_name, str))


def test_retrieve_all_checkpoint_groups(pg_conn):
    dql_binds.create_checkpoint_group(pg_conn, 'group-2')
    dql_binds.create_checkpoint_group(pg_conn, 'group-1')
    records = dql_binds.retrieve_all_checkpoint_groups(pg_conn)
    assert(len(records) == 2)
    assert(records[0]['group_name'] == 'group-1')
    assert(records[1]['group_name'] == 'group-2')


def test_update_checkpoint_group(pg_conn):
    created_name = dql_binds.create_checkpoint_group(pg_conn, 'group-1')
    result = dql_binds.update_checkpoint_group(pg_conn, group_name=created_name, new_group_name='group-2')
    assert result is None


def test_delete_checkpoint_groups_by_group_names(pg_conn):
    created_name = dql_binds.create_checkpoint_group(pg_conn, 'group-1')
    result = dql_binds.delete_checkpoint_groups_by_group_names(pg_conn, (created_name,))
    assert result is None


# ----

def test_add_checkpoint_group_member(pg_conn):
    created_group_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    created_checkpoint_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    result = dql_binds.add_checkpoint_group_member(pg_conn, created_group_name, created_checkpoint_id)
    assert result is None


def test_retrieve_checkpoint_group_members(pg_conn):
    created_group_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    created_checkpoint_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    dql_binds.add_checkpoint_group_member(pg_conn, created_group_name, created_checkpoint_id)
    records = dql_binds.retrieve_checkpoint_group_members(pg_conn, created_group_name)
    assert len(records) == 1
    assert records[0]['checkpoint_name'] == 'Entrance A'


def test_retrieve_checkpoint_groups_by_checkpoint_id(pg_conn):
    created_group_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    created_checkpoint_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    dql_binds.add_checkpoint_group_member(pg_conn, created_group_name, created_checkpoint_id)
    records = dql_binds.retrieve_checkpoint_groups_by_checkpoint_id(pg_conn, created_checkpoint_id)
    assert len(records) == 1
    assert records[0]['group_name'] == 'group-1'


def test_remove_checkpoint_group_members(pg_conn):
    created_group_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    created_checkpoint_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    dql_binds.add_checkpoint_group_member(pg_conn, created_group_name, created_checkpoint_id)
    result = dql_binds.remove_checkpoint_group_members(pg_conn, created_group_name, (created_checkpoint_id,))
    assert result is None


def test_remove_checkpoint_from_checkpoint_groups(pg_conn):
    created_group_name = dql_binds.create_checkpoint_group(pg_conn, group_name='group-1')
    created_checkpoint_id = dql_binds.create_checkpoint(pg_conn, 'Entrance A')
    dql_binds.add_checkpoint_group_member(pg_conn, created_group_name, created_checkpoint_id)
    result = dql_binds.remove_checkpoint_from_checkpoint_groups(pg_conn, created_checkpoint_id, (created_group_name,))
    assert result is None


# ---

def test_create_auth_level(pg_conn):
    created_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    assert isinstance(created_name, str)


def test_retrieve_auth_levels_by_auth_name(pg_conn):
    created_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    records = dql_binds.retrieve_auth_levels_by_auth_name(pg_conn, (created_name,))
    assert len(records) == 1
    assert records[0]['auth_name'] == 'sys/1'


def test_update_auth_level(pg_conn):
    created_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    result = dql_binds.update_auth_level(pg_conn, created_name, new_auth_name='level-2', auth_grant=False)
    assert result is None


def test_delete_auth_levels_by_auth_names(pg_conn):
    created_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    result = dql_binds.delete_auth_levels_by_auth_names(pg_conn, (created_name,))
    assert result is None


# ---

def test_create_auth_flow(pg_conn):
    created_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    assert isinstance(created_id, int)


def test_retrieve_auth_flows_by_ids(pg_conn):
    created_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    records = dql_binds.retrieve_auth_flows_by_ids(pg_conn, (created_id,))
    assert len(records) == 1
    assert records[0]['auth_flow_desc'] == 'primary'


def test_update_auth_flow(pg_conn):
    created_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    result = dql_binds.update_auth_flow(pg_conn, created_id, 'secondary')
    assert result is None


def test_delete_auth_flows_by_ids(pg_conn):
    created_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    result = dql_binds.delete_auth_flows_by_ids(pg_conn, (created_id,))
    assert result is None


def test_create_auth_flow_st(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    created_auth_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    created_record = dql_binds.create_auth_flow_st(pg_conn, created_flow_id, created_auth_name, st_term=False)
    assert created_record['auth_flow_id'] == created_flow_id
    assert created_record['st_name'] == created_auth_name


def test_retrieve_auth_flow_sts_by_auth_flow_id(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    created_auth_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, created_auth_name, st_term=False)
    records = dql_binds.retrieve_auth_flow_sts_by_auth_flow_id(pg_conn, created_flow_id)
    assert len(records) != 0


def test_update_auth_flow_st(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    created_auth_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, created_auth_name, st_term=False)
    result = dql_binds.update_auth_flow_st(pg_conn, created_flow_id, created_auth_name, st_term=True)
    assert result is None


def test_delete_auth_flow_st_by_id(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    created_auth_name = dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, created_auth_name, st_term=False)
    result = dql_binds.delete_auth_flow_st_by_id(pg_conn, created_flow_id, created_auth_name)
    assert result is None


def test_create_auth_flow_tr(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/2', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/3', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/1', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/2', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/3', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, created_flow_id, 'sys/2', 'sys/1', 'sys/3')


def test_retrieve_auth_flow_trs_by_auth_flow_id(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/2', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/3', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/1', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/2', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/3', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, created_flow_id, 'sys/2', 'sys/1', 'sys/3')
    records = dql_binds.retrieve_auth_flow_trs_by_auth_flow_id(pg_conn, created_flow_id)
    assert len(records) == 1


def test_update_auth_flow_tr(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/2', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/3', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/1', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/2', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/3', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, created_flow_id, 'sys/1', 'sys/2', 'sys/3')
    result = dql_binds.update_auth_flow_tr(pg_conn, created_flow_id, 'sys/2', 'sys/1', 'sys/3',
                                           new_curr_st='sys/1',
                                           new_when_ev='sys/2',
                                           new_next_st='sys/3')
    assert result is None


def test_delete_auth_flow_tr_by_id(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    dql_binds.create_auth_level(pg_conn, 'sys/1', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/2', auth_grant=True)
    dql_binds.create_auth_level(pg_conn, 'sys/3', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/1', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/2', st_term=True)
    dql_binds.create_auth_flow_st(pg_conn, created_flow_id, 'sys/3', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, created_flow_id, 'sys/2', 'sys/1', 'sys/3')
    result = dql_binds.delete_auth_flow_tr_by_id(pg_conn, created_flow_id, 'sys/2', 'sys/1', 'sys/3')
    assert result is None


# ---

def test_retrieve_current_active_auth_flow(pg_conn):
    record = dql_binds.retrieve_current_active_auth_flow(pg_conn)
    assert record['auth_flow_id'] == 0


def test_update_current_active_auth_flow(pg_conn):
    created_flow_id = dql_binds.create_auth_flow(pg_conn, 'primary')
    result = dql_binds.update_current_active_auth_flow(pg_conn, created_flow_id)
    assert result is None


# ---

def test_create_auth_rule(pg_conn):
    created_id = dql_binds.create_auth_rule(pg_conn,
                                            effect='sys/none',
                                            rule_ord=SQLDefault(),
                                            year0=SQLDefault(),
                                            year1=SQLDefault(),
                                            month0=SQLDefault(),
                                            month1=SQLDefault(),
                                            mday0=SQLDefault(),
                                            mday1=SQLDefault(),
                                            wday0=SQLDefault(),
                                            wday1=SQLDefault(),
                                            hour0=SQLDefault(),
                                            hour1=SQLDefault(),
                                            minute0=SQLDefault(),
                                            minute1=SQLDefault())
    assert isinstance(created_id, int)


def test_retrieve_auth_rules_by_ids(pg_conn):
    created_id = dql_binds.create_auth_rule(pg_conn,
                                            effect='sys/none',
                                            rule_ord=SQLDefault(),
                                            year0=SQLDefault(),
                                            year1=SQLDefault(),
                                            month0=SQLDefault(),
                                            month1=SQLDefault(),
                                            mday0=SQLDefault(),
                                            mday1=SQLDefault(),
                                            wday0=SQLDefault(),
                                            wday1=SQLDefault(),
                                            hour0=SQLDefault(),
                                            hour1=SQLDefault(),
                                            minute0=SQLDefault(),
                                            minute1=SQLDefault())
    records = dql_binds.retrieve_auth_rules_by_ids(pg_conn, (created_id,))
    assert len(records) == 1


def test_update_auth_rule(pg_conn):
    created_id = dql_binds.create_auth_rule(pg_conn,
                                            effect='sys/none',
                                            rule_ord=SQLDefault(),
                                            year0=SQLDefault(),
                                            year1=SQLDefault(),
                                            month0=SQLDefault(),
                                            month1=SQLDefault(),
                                            mday0=SQLDefault(),
                                            mday1=SQLDefault(),
                                            wday0=SQLDefault(),
                                            wday1=SQLDefault(),
                                            hour0=SQLDefault(),
                                            hour1=SQLDefault(),
                                            minute0=SQLDefault(),
                                            minute1=SQLDefault())

    result = dql_binds.update_auth_rule(pg_conn,
                                        rule_id=created_id,
                                        effect='sys/none',
                                        rule_ord=SQLDefault(),
                                        year0=SQLDefault(),
                                        year1=SQLDefault(),
                                        month0=SQLDefault(),
                                        month1=SQLDefault(),
                                        mday0=SQLDefault(),
                                        mday1=SQLDefault(),
                                        wday0=SQLDefault(),
                                        wday1=SQLDefault(),
                                        hour0=SQLDefault(),
                                        hour1=SQLDefault(),
                                        minute0=SQLDefault(),
                                        minute1=SQLDefault())
    assert result is None


def test_delete_auth_rules_by_ids(pg_conn):
    created_id = dql_binds.create_auth_rule(pg_conn,
                                            effect='sys/none',
                                            rule_ord=SQLDefault(),
                                            year0=SQLDefault(),
                                            year1=SQLDefault(),
                                            month0=SQLDefault(),
                                            month1=SQLDefault(),
                                            mday0=SQLDefault(),
                                            mday1=SQLDefault(),
                                            wday0=SQLDefault(),
                                            wday1=SQLDefault(),
                                            hour0=SQLDefault(),
                                            hour1=SQLDefault(),
                                            minute0=SQLDefault(),
                                            minute1=SQLDefault())
    result = dql_binds.delete_auth_rules_by_ids(pg_conn, (created_id,))
    assert result is None


# ---

def test_create_process(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    assert isinstance(created_proc_id, int)


def test_retrieve_processes_by_ids(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    records = dql_binds.retrieve_processes_by_ids(pg_conn, (created_proc_id,))
    assert len(records) == 1


def test_update_process(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    result = dql_binds.update_process(pg_conn, created_proc_id, ctc=0)
    assert result is None


def test_update_process_auth_flow(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    result = dql_binds.update_process_auth_flow(pg_conn, created_proc_id, auth_flow=0)
    assert result is None


def test_terminate_process(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    created_ctc_id = dql_binds.create_contact(pg_conn, 'Joe')
    created_orig_id = dql_binds.create_location(pg_conn, 'Addr 1')
    created_dest_id = dql_binds.create_location(pg_conn, 'Addr 2')
    created_ckp_id = dql_binds.create_checkpoint(pg_conn, 'Gate 1')
    result = dql_binds.update_process(pg_conn, created_proc_id,
                                      ctc=created_ctc_id,
                                      loc_orig=created_orig_id,
                                      loc_dest=created_dest_id,
                                      ckp=created_ckp_id)
    result = dql_binds.terminate_process(pg_conn, created_proc_id)
    assert isinstance(result, datetime.datetime)


def test_delete_processes_by_ids(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    result = dql_binds.delete_processes_by_ids(pg_conn, (created_proc_id,))
    assert result is None


def test_create_process_auth_event(pg_conn):
    created_proc_id = dql_binds.create_process(pg_conn)
    result = dql_binds.create_process_auth_event(pg_conn, created_proc_id, 0, 'sys/none')
    assert isinstance(result, datetime.datetime)


def test_archive_finished_processes(pg_conn):
    dql_binds.create_auth_level(pg_conn, 'sys/acc', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, 0, 'sys/acc', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, 0, 'sys/acc', 'sys/none', 'sys/acc')

    created_proc_id = dql_binds.create_process(pg_conn)
    ctc = dql_binds.create_contact(pg_conn, 'Joe')
    loc_orig = dql_binds.create_location(pg_conn, 'Addr 1')
    loc_dest = dql_binds.create_location(pg_conn, 'Addr 2')
    ckp = dql_binds.create_checkpoint(pg_conn, 'Gate 1')
    dql_binds.update_process(pg_conn, created_proc_id, ctc=ctc, loc_orig=loc_orig, loc_dest=loc_dest, ckp=ckp)

    dql_binds.create_process_auth_event(pg_conn, created_proc_id, ctc, 'sys/acc')
    time.sleep(0.1)
    dql_binds.terminate_process(pg_conn, created_proc_id)
    result = dql_binds.archive_finished_processes(pg_conn)
    assert result


def test_retrieve_process_histories_by_ids(pg_conn):
    dql_binds.create_auth_level(pg_conn, 'sys/acc', auth_grant=True)
    dql_binds.create_auth_flow_st(pg_conn, 0, 'sys/acc', st_term=True)
    dql_binds.create_auth_flow_tr(pg_conn, 0, 'sys/acc', 'sys/none', 'sys/acc')

    created_proc_id = dql_binds.create_process(pg_conn)
    ctc = dql_binds.create_contact(pg_conn, 'Joe')
    loc_orig = dql_binds.create_location(pg_conn, 'Addr 1')
    loc_dest = dql_binds.create_location(pg_conn, 'Addr 2')
    ckp = dql_binds.create_checkpoint(pg_conn, 'Gate 1')
    dql_binds.update_process(pg_conn, created_proc_id, ctc=ctc, loc_orig=loc_orig, loc_dest=loc_dest, ckp=ckp)
    dql_binds.create_process_auth_event(pg_conn, created_proc_id, ctc, 'sys/acc')
    result = dql_binds.retrieve_process_histories_by_ids(pg_conn, (created_proc_id,))
    assert result


def test_retrieve_all_running_process_snapshots(pg_conn):
    dql_binds.create_process(pg_conn)
    result = dql_binds.retrieve_all_running_process_snapshots(pg_conn)
    assert result


def test_retrieve_processes_rule_matches(pg_conn):
    dql_binds.create_process(pg_conn)
    result = dql_binds.retrieve_processes_rule_matches(pg_conn)
    assert result


def test_retrieve_processes_rule_selections(pg_conn):
    dql_binds.create_process(pg_conn)
    result = dql_binds.retrieve_processes_rule_selections(pg_conn)
    assert result
