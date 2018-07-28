import pytest
from .fixtures import *  # flake8: noqa


def test_create_location_group(db):
    create_location_group(db, 'group-1')


def test_update_location_group(db):
    create_location_group(db, 'group-1')
    update_location_group(db,  'group-1', 'group-a')
    rs = retrieve_location_groups(db)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_location_groups(db):
    create_location_group(db, 'group-1')
    create_location_group(db, 'group-2')
    rs = retrieve_location_groups(db)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_location_groups_by_group_names(db):
    create_location_group(db, 'group-1')
    rs = retrieve_location_groups(db)
    assert len(rs) == 1
    delete_location_groups_by_group_names(db, ['group-1'])
    rs = retrieve_location_groups(db)
    assert rs == []


@pytest.fixture
def loc_a1(db):
    return create_location(db, 'loc_a1')


@pytest.fixture
def loc_a2(db):
    return create_location(db, 'loc_a2')


def test_create_location_group_membership(db, loc_a1):
    create_location_group(db, 'group-1')
    create_location_group_membership(db, 'group-1', loc_a1)


def test_retrieve_location_group_memberships(db, loc_a1):
    create_location_group(db, 'group-1')
    create_location_group_membership(db, 'group-1', loc_a1)
    rs = retrieve_location_group_memberships(db, 'group-1')
    assert rs == [{'location_id': loc_a1}]


def test_retrieve_location_groups_by_member_id(db, loc_a1):
    create_location_group(db, 'group-1')
    create_location_group(db, 'group-2')
    create_location_group_membership(db, 'group-1', loc_a1)
    create_location_group_membership(db, 'group-2', loc_a1)
    rs = retrieve_location_groups_by_member_id(db, loc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_delete_location_group_memberships_by_member_ids(db, loc_a1, loc_a2):
    create_location_group(db, 'group-1')
    create_location_group_membership(db, 'group-1', loc_a1)
    create_location_group_membership(db, 'group-1', loc_a2)
    delete_location_group_memberships_by_member_ids(db, 'group-1', [loc_a1])
    rs = retrieve_location_group_memberships(db, 'group-1')
    assert rs == [{'location_id': loc_a2}]


def test_delete_location_group_memberships_by_group_names(db, loc_a1, loc_a2):
    create_location_group(db, 'group-1')
    create_location_group(db, 'group-2')
    create_location_group(db, 'group-3')
    create_location_group_membership(db, 'group-1', loc_a1)
    create_location_group_membership(db, 'group-2', loc_a1)
    create_location_group_membership(db, 'group-3', loc_a1)
    create_location_group_membership(db, 'group-1', loc_a2)
    delete_location_group_memberships_by_group_names(db, loc_a1, ['group-1', 'group-3'])
    rs = retrieve_location_groups_by_member_id(db, loc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_location_groups_by_member_id(db, loc_a2)
    assert rs == [{'group_name': 'group-1'}]


