import pytest
from .fixtures import *  # flake8: noqa


def test_create_contact_group(db):
    create_contact_group(db, 'group-1')


def test_update_contact_group(db):
    create_contact_group(db, 'group-1')
    update_contact_group(db,  'group-1', 'group-a')
    rs = retrieve_contact_groups(db)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_contact_groups(db):
    create_contact_group(db, 'group-1')
    create_contact_group(db, 'group-2')
    rs = retrieve_contact_groups(db)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_contact_groups_by_group_names(db):
    create_contact_group(db, 'group-1')
    rs = retrieve_contact_groups(db)
    assert len(rs) == 1
    delete_contact_groups_by_group_names(db, ['group-1'])
    rs = retrieve_contact_groups(db)
    assert rs == []


@pytest.fixture
def ctc_a1(db):
    return create_contact(db, 'ctc_a1')


@pytest.fixture
def ctc_a2(db):
    return create_contact(db, 'ctc_a2')


def test_create_contact_group_membership(db, ctc_a1):
    create_contact_group(db, 'group-1')
    create_contact_group_membership(db, 'group-1', ctc_a1)


def test_retrieve_contact_group_memberships(db, ctc_a1):
    create_contact_group(db, 'group-1')
    create_contact_group_membership(db, 'group-1', ctc_a1)
    rs = retrieve_contact_group_memberships(db, 'group-1')
    assert rs == [{'contact_id': ctc_a1}]


def test_retrieve_contact_groups_by_member_id(db, ctc_a1):
    create_contact_group(db, 'group-1')
    create_contact_group(db, 'group-2')
    create_contact_group_membership(db, 'group-1', ctc_a1)
    create_contact_group_membership(db, 'group-2', ctc_a1)
    rs = retrieve_contact_groups_by_member_id(db, ctc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_delete_contact_group_memberships_by_member_ids(db, ctc_a1, ctc_a2):
    create_contact_group(db, 'group-1')
    create_contact_group_membership(db, 'group-1', ctc_a1)
    create_contact_group_membership(db, 'group-1', ctc_a2)
    delete_contact_group_memberships_by_member_ids(db, 'group-1', [ctc_a1])
    rs = retrieve_contact_group_memberships(db, 'group-1')
    assert rs == [{'contact_id': ctc_a2}]


def test_delete_contact_group_memberships_by_group_names(db, ctc_a1, ctc_a2):
    create_contact_group(db, 'group-1')
    create_contact_group(db, 'group-2')
    create_contact_group(db, 'group-3')
    create_contact_group_membership(db, 'group-1', ctc_a1)
    create_contact_group_membership(db, 'group-2', ctc_a1)
    create_contact_group_membership(db, 'group-3', ctc_a1)
    create_contact_group_membership(db, 'group-1', ctc_a2)
    delete_contact_group_memberships_by_group_names(db, ctc_a1, ['group-1', 'group-3'])
    rs = retrieve_contact_groups_by_member_id(db, ctc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_contact_groups_by_member_id(db, ctc_a2)
    assert rs == [{'group_name': 'group-1'}]


