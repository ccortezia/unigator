import pytest
from unigator_db import (
    create_location,
    create_location_group,
    retrieve_all_location_groups,
    update_location_group,
    delete_location_groups_by_group_names,
    add_location_group_member,
    retrieve_location_group_members,
    retrieve_location_groups_by_location_id,
    remove_location_group_members,
    remove_location_from_location_groups
)


def test_create_location_group(pg_conn):
    create_location_group(pg_conn, 'group-1')


def test_update_location_group(pg_conn):
    create_location_group(pg_conn, 'group-1')
    update_location_group(pg_conn,  'group-1', 'group-a')
    rs = retrieve_all_location_groups(pg_conn)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_all_location_groups(pg_conn):
    create_location_group(pg_conn, 'group-1')
    create_location_group(pg_conn, 'group-2')
    rs = retrieve_all_location_groups(pg_conn)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_location_groups_by_group_names(pg_conn):
    create_location_group(pg_conn, 'group-1')
    rs = retrieve_all_location_groups(pg_conn)
    assert len(rs) == 1
    delete_location_groups_by_group_names(pg_conn, ('group-1',))
    rs = retrieve_all_location_groups(pg_conn)
    assert rs == []


@pytest.fixture
def loc_a1(pg_conn):
    return create_location(pg_conn, 'loc_a1')


@pytest.fixture
def loc_a2(pg_conn):
    return create_location(pg_conn, 'loc_a2')


def test_add_location_group_member(pg_conn, loc_a1):
    create_location_group(pg_conn, 'group-1')
    add_location_group_member(pg_conn, 'group-1', loc_a1)


def test_retrieve_location_group_members(pg_conn, loc_a1):
    create_location_group(pg_conn, 'group-1')
    add_location_group_member(pg_conn, 'group-1', loc_a1)
    rs = retrieve_location_group_members(pg_conn, 'group-1')
    assert rs == [{'location_id': loc_a1, 'addr_1': 'loc_a1', 'addr_2': None, 'addr_3': None, 'addr_4': None, 'addr_5': None, 'addr_6': None}]


def test_retrieve_location_groups_by_location_id(pg_conn, loc_a1):
    create_location_group(pg_conn, 'group-1')
    create_location_group(pg_conn, 'group-2')
    add_location_group_member(pg_conn, 'group-1', loc_a1)
    add_location_group_member(pg_conn, 'group-2', loc_a1)
    rs = retrieve_location_groups_by_location_id(pg_conn, loc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_remove_location_group_members(pg_conn, loc_a1, loc_a2):
    create_location_group(pg_conn, 'group-1')
    add_location_group_member(pg_conn, 'group-1', loc_a1)
    add_location_group_member(pg_conn, 'group-1', loc_a2)
    remove_location_group_members(pg_conn, 'group-1', (loc_a1,))
    rs = retrieve_location_group_members(pg_conn, 'group-1')
    assert rs == [{'location_id': loc_a2, 'addr_1': 'loc_a2', 'addr_2': None, 'addr_3': None, 'addr_4': None, 'addr_5': None, 'addr_6': None}]


def test_remove_location_from_location_groups(pg_conn, loc_a1, loc_a2):
    create_location_group(pg_conn, 'group-1')
    create_location_group(pg_conn, 'group-2')
    create_location_group(pg_conn, 'group-3')
    add_location_group_member(pg_conn, 'group-1', loc_a1)
    add_location_group_member(pg_conn, 'group-2', loc_a1)
    add_location_group_member(pg_conn, 'group-3', loc_a1)
    add_location_group_member(pg_conn, 'group-1', loc_a2)
    remove_location_from_location_groups(pg_conn, loc_a1, ('group-1', 'group-3'))
    rs = retrieve_location_groups_by_location_id(pg_conn, loc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_location_groups_by_location_id(pg_conn, loc_a2)
    assert rs == [{'group_name': 'group-1'}]
