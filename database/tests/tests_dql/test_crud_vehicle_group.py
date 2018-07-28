import pytest
from .fixtures import *  # flake8: noqa


def test_create_vehicle_group(db):
    create_vehicle_group(db, 'group-1')


def test_update_vehicle_group(db):
    create_vehicle_group(db, 'group-1')
    update_vehicle_group(db,  'group-1', 'group-a')
    rs = retrieve_vehicle_groups(db)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_vehicle_groups(db):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group(db, 'group-2')
    rs = retrieve_vehicle_groups(db)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_vehicle_groups_by_group_names(db):
    create_vehicle_group(db, 'group-1')
    rs = retrieve_vehicle_groups(db)
    assert len(rs) == 1
    delete_vehicle_groups_by_group_names(db, ['group-1'])
    rs = retrieve_vehicle_groups(db)
    assert rs == []


@pytest.fixture
def vhc_a1(db):
    return create_vehicle(db, 'GGG0000')


@pytest.fixture
def vhc_a2(db):
    return create_vehicle(db, 'AAA9999')


def test_create_vehicle_group_membership(db, vhc_a1):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group_membership(db, 'group-1', vhc_a1)


def test_retrieve_vehicle_group_memberships(db, vhc_a1):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group_membership(db, 'group-1', vhc_a1)
    rs = retrieve_vehicle_group_memberships(db, 'group-1')
    assert rs == [{'vehicle_id': vhc_a1}]


def test_retrieve_vehicle_groups_by_member_id(db, vhc_a1):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group(db, 'group-2')
    create_vehicle_group_membership(db, 'group-1', vhc_a1)
    create_vehicle_group_membership(db, 'group-2', vhc_a1)
    rs = retrieve_vehicle_groups_by_member_id(db, vhc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_delete_vehicle_group_memberships_by_member_ids(db, vhc_a1, vhc_a2):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group_membership(db, 'group-1', vhc_a1)
    create_vehicle_group_membership(db, 'group-1', vhc_a2)
    delete_vehicle_group_memberships_by_member_ids(db, 'group-1', [vhc_a1])
    rs = retrieve_vehicle_group_memberships(db, 'group-1')
    assert rs == [{'vehicle_id': vhc_a2}]


def test_delete_vehicle_group_memberships_by_group_names(db, vhc_a1, vhc_a2):
    create_vehicle_group(db, 'group-1')
    create_vehicle_group(db, 'group-2')
    create_vehicle_group(db, 'group-3')
    create_vehicle_group_membership(db, 'group-1', vhc_a1)
    create_vehicle_group_membership(db, 'group-2', vhc_a1)
    create_vehicle_group_membership(db, 'group-3', vhc_a1)
    create_vehicle_group_membership(db, 'group-1', vhc_a2)
    delete_vehicle_group_memberships_by_group_names(db, vhc_a1, ['group-1', 'group-3'])
    rs = retrieve_vehicle_groups_by_member_id(db, vhc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_vehicle_groups_by_member_id(db, vhc_a2)
    assert rs == [{'group_name': 'group-1'}]


