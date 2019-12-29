import pytest
from unigator_db import (
    create_contact_group,
    update_contact_group,
    retrieve_all_contact_groups,
    delete_contact_groups_by_group_names,
    create_contact,
    add_contact_group_member,
    retrieve_contact_group_members,
    retrieve_contact_groups_by_contact_id,
    remove_contact_from_contact_groups
)


def test_create_contact_group(pg_conn):
    create_contact_group(pg_conn, 'group-1')


def test_update_contact_group(pg_conn):
    create_contact_group(pg_conn, 'group-1')
    update_contact_group(pg_conn,  'group-1', 'group-a')
    rs = retrieve_all_contact_groups(pg_conn)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_all_contact_groups(pg_conn):
    create_contact_group(pg_conn, 'group-1')
    create_contact_group(pg_conn, 'group-2')
    rs = retrieve_all_contact_groups(pg_conn)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_contact_groups_by_group_names(pg_conn):
    create_contact_group(pg_conn, 'group-1')
    rs = retrieve_all_contact_groups(pg_conn)
    assert len(rs) == 1
    delete_contact_groups_by_group_names(pg_conn, ('group-1',))
    rs = retrieve_all_contact_groups(pg_conn)
    assert rs == []


@pytest.fixture
def ctc_a1(pg_conn):
    return create_contact(pg_conn, 'ctc_a1')


@pytest.fixture
def ctc_a2(pg_conn):
    return create_contact(pg_conn, 'ctc_a2')


def test_add_contact_group_member(pg_conn, ctc_a1):
    create_contact_group(pg_conn, 'group-1')
    add_contact_group_member(pg_conn, 'group-1', ctc_a1)


def test_retrieve_contact_group_members(pg_conn, ctc_a1):
    create_contact_group(pg_conn, 'group-1')
    add_contact_group_member(pg_conn, 'group-1', ctc_a1)
    rs = retrieve_contact_group_members(pg_conn, 'group-1')
    assert rs == [{'contact_id': ctc_a1, 'contact_name': 'ctc_a1'}]


def test_retrieve_contact_groups_by_contact_id(pg_conn, ctc_a1):
    create_contact_group(pg_conn, 'group-1')
    create_contact_group(pg_conn, 'group-2')
    add_contact_group_member(pg_conn, 'group-1', ctc_a1)
    add_contact_group_member(pg_conn, 'group-2', ctc_a1)
    rs = retrieve_contact_groups_by_contact_id(pg_conn, ctc_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_remove_contact_from_contact_groups(pg_conn, ctc_a1, ctc_a2):
    create_contact_group(pg_conn, 'group-1')
    create_contact_group(pg_conn, 'group-2')
    create_contact_group(pg_conn, 'group-3')
    add_contact_group_member(pg_conn, 'group-1', ctc_a1)
    add_contact_group_member(pg_conn, 'group-2', ctc_a1)
    add_contact_group_member(pg_conn, 'group-3', ctc_a1)
    add_contact_group_member(pg_conn, 'group-1', ctc_a2)
    remove_contact_from_contact_groups(pg_conn, ctc_a1, ('group-1', 'group-3'))
    rs = retrieve_contact_groups_by_contact_id(pg_conn, ctc_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_contact_groups_by_contact_id(pg_conn, ctc_a2)
    assert rs == [{'group_name': 'group-1'}]
