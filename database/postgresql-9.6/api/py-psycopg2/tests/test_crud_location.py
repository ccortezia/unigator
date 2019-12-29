import pytest
from unigator_db import (
    create_location,
    retrieve_locations_by_ids,
    update_location,
    delete_locations_by_ids
)


def test_create_location(pg_conn):
    pk = create_location(pg_conn, 'Place 1')
    rs = retrieve_locations_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['location_id'] == pk
    assert rs[0]['addr_1'] == 'Place 1'


def test_retrieve_locations_by_ids(pg_conn):
    addrs = ['Place 1', 'Place 2', 'Place 3', 'Place 4', 'Place 5']
    pks = [create_location(pg_conn, addr) for addr in addrs]
    rs = retrieve_locations_by_ids(pg_conn, tuple(pks))
    assert [r['location_id'] for r in rs] == pks
    assert [r['addr_1'] for r in rs] == addrs


def test_update_location(pg_conn):
    pk = create_location(pg_conn, 'Place 1')
    update_location(pg_conn, pk, addr_1='Nowhere')
    rs = retrieve_locations_by_ids(pg_conn, (pk,))
    assert rs[0]['addr_1'] == 'Nowhere'


def test_update_location_protected_pk_should_err(pg_conn):
    with pytest.raises(Exception):
        update_location(pg_conn, 0, addr_1='Nowhere')


def test_update_location_pk_should_err(pg_conn):
    pk = create_location(pg_conn, 'Place 1')
    with pytest.raises(Exception):
        pg_conn.execute('update ac_locations set location_id=1088 where location_id = %(pk)s', {'pk': pk})


def test_delete_locations_by_ids(pg_conn):
    pk = create_location(pg_conn, 'Place 1')
    delete_locations_by_ids(pg_conn, (pk,))
    rs = retrieve_locations_by_ids(pg_conn, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(pg_conn):
    with pytest.raises(Exception):
        delete_locations_by_ids(pg_conn, (0,))
