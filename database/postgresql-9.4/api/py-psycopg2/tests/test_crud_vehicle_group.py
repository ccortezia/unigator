import pytest
from unigator_db import (
    create_vehicle,
    create_vehicle_group,
    update_vehicle_group,
    retrieve_all_vehicle_groups,
    delete_vehicle_groups_by_group_names,
    add_vehicle_group_member,
    retrieve_vehicle_group_members,
    retrieve_vehicle_groups_by_vehicle_id,
    remove_vehicle_group_members,
    remove_vehicle_from_vehicle_groups
)


def test_create_vehicle_group(pg_conn):
    create_vehicle_group(pg_conn, 'group-1')


def test_update_vehicle_group(pg_conn):
    create_vehicle_group(pg_conn, 'group-1')
    update_vehicle_group(pg_conn,  'group-1', 'group-a')
    rs = retrieve_all_vehicle_groups(pg_conn)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_all_vehicle_groups(pg_conn):
    create_vehicle_group(pg_conn, 'group-1')
    create_vehicle_group(pg_conn, 'group-2')
    rs = retrieve_all_vehicle_groups(pg_conn)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_vehicle_groups_by_group_names(pg_conn):
    create_vehicle_group(pg_conn, 'group-1')
    rs = retrieve_all_vehicle_groups(pg_conn)
    assert len(rs) == 1
    delete_vehicle_groups_by_group_names(pg_conn, ('group-1',))
    rs = retrieve_all_vehicle_groups(pg_conn)
    assert rs == []


@pytest.fixture
def vhc_a1(pg_conn):
    return create_vehicle(pg_conn, 'GGG0000')


@pytest.fixture
def vhc_a2(pg_conn):
    return create_vehicle(pg_conn, 'AAA9999')


def test_add_vehicle_group_member(pg_conn, vhc_a1):
    create_vehicle_group(pg_conn, 'group-1')
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a1)


def test_retrieve_vehicle_group_members(pg_conn, vhc_a1):
    create_vehicle_group(pg_conn, 'group-1')
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a1)
    rs = retrieve_vehicle_group_members(pg_conn, 'group-1')
    assert rs == [{'vehicle_id': vhc_a1, 'plate': 'GGG0000'}]


def test_retrieve_vehicle_groups_by_vehicle_id(pg_conn, vhc_a1):
    create_vehicle_group(pg_conn, 'group-1')
    create_vehicle_group(pg_conn, 'group-2')
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a1)
    add_vehicle_group_member(pg_conn, 'group-2', vhc_a1)
    rs = retrieve_vehicle_groups_by_vehicle_id(pg_conn, vhc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_remove_vehicle_group_members(pg_conn, vhc_a1, vhc_a2):
    create_vehicle_group(pg_conn, 'group-1')
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a1)
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a2)
    remove_vehicle_group_members(pg_conn, 'group-1', (vhc_a1,))
    rs = retrieve_vehicle_group_members(pg_conn, 'group-1')
    assert rs == [{'vehicle_id': vhc_a2, 'plate': 'AAA9999'}]


def test_remove_vehicle_from_vehicle_groups(pg_conn, vhc_a1, vhc_a2):
    create_vehicle_group(pg_conn, 'group-1')
    create_vehicle_group(pg_conn, 'group-2')
    create_vehicle_group(pg_conn, 'group-3')
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a1)
    add_vehicle_group_member(pg_conn, 'group-2', vhc_a1)
    add_vehicle_group_member(pg_conn, 'group-3', vhc_a1)
    add_vehicle_group_member(pg_conn, 'group-1', vhc_a2)
    remove_vehicle_from_vehicle_groups(pg_conn, vhc_a1, ('group-1', 'group-3'))
    rs = retrieve_vehicle_groups_by_vehicle_id(pg_conn, vhc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_vehicle_groups_by_vehicle_id(pg_conn, vhc_a2)
    assert rs == [{'group_name': 'group-1'}]
