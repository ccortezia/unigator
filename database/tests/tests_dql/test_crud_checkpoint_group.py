import pytest
from .fixtures import *  # flake8: noqa


def test_create_checkpoint_group(db):
    create_checkpoint_group(db, 'group-1')


def test_update_checkpoint_group(db):
    create_checkpoint_group(db, 'group-1')
    update_checkpoint_group(db,  'group-1', 'group-a')
    rs = retrieve_checkpoint_groups(db)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_checkpoint_groups(db):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group(db, 'group-2')
    rs = retrieve_checkpoint_groups(db)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_checkpoint_groups_by_group_names(db):
    create_checkpoint_group(db, 'group-1')
    rs = retrieve_checkpoint_groups(db)
    assert len(rs) == 1
    delete_checkpoint_groups_by_group_names(db, ['group-1'])
    rs = retrieve_checkpoint_groups(db)
    assert rs == []


@pytest.fixture
def ckp_a1(db):
    return create_checkpoint(db, 'ckp_a1')


@pytest.fixture
def ckp_a2(db):
    return create_checkpoint(db, 'ckp_a2')


def test_create_checkpoint_group_membership(db, ckp_a1):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group_membership(db, 'group-1', ckp_a1)


def test_retrieve_checkpoint_group_memberships(db, ckp_a1):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group_membership(db, 'group-1', ckp_a1)
    rs = retrieve_checkpoint_group_memberships(db, 'group-1')
    assert rs == [{'checkpoint_id': ckp_a1}]


def test_retrieve_checkpoint_groups_by_member_id(db, ckp_a1):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group(db, 'group-2')
    create_checkpoint_group_membership(db, 'group-1', ckp_a1)
    create_checkpoint_group_membership(db, 'group-2', ckp_a1)
    rs = retrieve_checkpoint_groups_by_member_id(db, ckp_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_delete_checkpoint_group_memberships_by_member_ids(db, ckp_a1, ckp_a2):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group_membership(db, 'group-1', ckp_a1)
    create_checkpoint_group_membership(db, 'group-1', ckp_a2)
    delete_checkpoint_group_memberships_by_member_ids(db, 'group-1', [ckp_a1])
    rs = retrieve_checkpoint_group_memberships(db, 'group-1')
    assert rs == [{'checkpoint_id': ckp_a2}]


def test_delete_checkpoint_group_memberships_by_group_names(db, ckp_a1, ckp_a2):
    create_checkpoint_group(db, 'group-1')
    create_checkpoint_group(db, 'group-2')
    create_checkpoint_group(db, 'group-3')
    create_checkpoint_group_membership(db, 'group-1', ckp_a1)
    create_checkpoint_group_membership(db, 'group-2', ckp_a1)
    create_checkpoint_group_membership(db, 'group-3', ckp_a1)
    create_checkpoint_group_membership(db, 'group-1', ckp_a2)
    delete_checkpoint_group_memberships_by_group_names(db, ckp_a1, ['group-1', 'group-3'])
    rs = retrieve_checkpoint_groups_by_member_id(db, ckp_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_checkpoint_groups_by_member_id(db, ckp_a2)
    assert rs == [{'group_name': 'group-1'}]


