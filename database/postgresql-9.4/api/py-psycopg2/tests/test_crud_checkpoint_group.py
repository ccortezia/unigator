import pytest
from unigator_db import (
    create_checkpoint,
    create_checkpoint_group,
    retrieve_all_checkpoint_groups,
    update_checkpoint_group,
    delete_checkpoint_groups_by_group_names,
    add_checkpoint_group_member,
    retrieve_checkpoint_group_members,
    retrieve_checkpoint_groups_by_checkpoint_id,
    remove_checkpoint_group_members,
    remove_checkpoint_from_checkpoint_groups
)


def test_create_checkpoint_group(pg_conn):
    create_checkpoint_group(pg_conn, 'group-1')


def test_update_checkpoint_group(pg_conn):
    create_checkpoint_group(pg_conn, 'group-1')
    update_checkpoint_group(pg_conn,  'group-1', 'group-a')
    rs = retrieve_all_checkpoint_groups(pg_conn)
    assert rs[0]['group_name'] == 'group-a'


def test_retrieve_all_checkpoint_groups(pg_conn):
    create_checkpoint_group(pg_conn, 'group-1')
    create_checkpoint_group(pg_conn, 'group-2')
    rs = retrieve_all_checkpoint_groups(pg_conn)
    assert len(rs) == 2
    assert rs[0]['group_name'] == 'group-1'
    assert rs[1]['group_name'] == 'group-2'


def test_delete_checkpoint_groups_by_group_names(pg_conn):
    create_checkpoint_group(pg_conn, 'group-1')
    rs = retrieve_all_checkpoint_groups(pg_conn)
    assert len(rs) == 1
    delete_checkpoint_groups_by_group_names(pg_conn, ('group-1',))
    rs = retrieve_all_checkpoint_groups(pg_conn)
    assert rs == []


@pytest.fixture
def ckp_a1(pg_conn):
    return create_checkpoint(pg_conn, 'ckp_a1')


@pytest.fixture
def ckp_a2(pg_conn):
    return create_checkpoint(pg_conn, 'ckp_a2')


def test_add_checkpoint_group_member(pg_conn, ckp_a1):
    create_checkpoint_group(pg_conn, 'group-1')
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a1)


def test_retrieve_checkpoint_group_members(pg_conn, ckp_a1):
    create_checkpoint_group(pg_conn, 'group-1')
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a1)
    rs = retrieve_checkpoint_group_members(pg_conn, 'group-1')
    assert rs == [{'checkpoint_id': ckp_a1, 'checkpoint_name': 'ckp_a1'}]


def test_retrieve_checkpoint_groups_by_checkpoint_id(pg_conn, ckp_a1):
    create_checkpoint_group(pg_conn, 'group-1')
    create_checkpoint_group(pg_conn, 'group-2')
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a1)
    add_checkpoint_group_member(pg_conn, 'group-2', ckp_a1)
    rs = retrieve_checkpoint_groups_by_checkpoint_id(pg_conn, ckp_a1)
    assert rs == [{'group_name': 'group-1'}, {'group_name': 'group-2'}]


def test_remove_checkpoint_group_members(pg_conn, ckp_a1, ckp_a2):
    create_checkpoint_group(pg_conn, 'group-1')
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a1)
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a2)
    remove_checkpoint_group_members(pg_conn, 'group-1', (ckp_a1,))
    rs = retrieve_checkpoint_group_members(pg_conn, 'group-1')
    assert rs == [{'checkpoint_id': ckp_a2, 'checkpoint_name': 'ckp_a2'}]


def test_remove_checkpoint_from_checkpoint_groups(pg_conn, ckp_a1, ckp_a2):
    create_checkpoint_group(pg_conn, 'group-1')
    create_checkpoint_group(pg_conn, 'group-2')
    create_checkpoint_group(pg_conn, 'group-3')
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a1)
    add_checkpoint_group_member(pg_conn, 'group-2', ckp_a1)
    add_checkpoint_group_member(pg_conn, 'group-3', ckp_a1)
    add_checkpoint_group_member(pg_conn, 'group-1', ckp_a2)
    remove_checkpoint_from_checkpoint_groups(pg_conn, ckp_a1, ('group-1', 'group-3'))
    rs = retrieve_checkpoint_groups_by_checkpoint_id(pg_conn, ckp_a1)
    assert rs == [{'group_name': 'group-2'}]
    rs = retrieve_checkpoint_groups_by_checkpoint_id(pg_conn, ckp_a2)
    assert rs == [{'group_name': 'group-1'}]
