import pytest
from unigator_db import (
    create_vehicle,
    retrieve_vehicles_by_ids,
    update_vehicle,
    delete_vehicles_by_ids
)


def test_create_vehicle(pg_conn):
    pk = create_vehicle(pg_conn, 'IUY5644')
    rs = retrieve_vehicles_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['vehicle_id'] == pk
    assert rs[0]['plate'] == 'IUY5644'


def test_retrieve_vehicles_by_ids(pg_conn):
    plates = ['IUY5644', 'Place 2', 'Place 3', 'Place 4', 'Place 5']
    pks = [create_vehicle(pg_conn, plate) for plate in plates]
    rs = retrieve_vehicles_by_ids(pg_conn, tuple(pks))
    assert [r['vehicle_id'] for r in rs] == pks
    assert [r['plate'] for r in rs] == plates


def test_update_vehicle(pg_conn):
    pk = create_vehicle(pg_conn, 'IUY5644')
    update_vehicle(pg_conn, pk, plate='AAA0000')
    rs = retrieve_vehicles_by_ids(pg_conn, (pk,))
    assert rs[0]['plate'] == 'AAA0000'


def test_update_vehicle_pk_should_err(pg_conn):
    pk = create_vehicle(pg_conn, 'IUY5644')
    with pytest.raises(Exception):
        pg_conn.execute('update ac_vehicles set vehicle_id=9090 where vehicle_id = %(pk)s', {'pk': pk})


def test_delete_vehicles_by_ids(pg_conn):
    pk = create_vehicle(pg_conn, 'IUY5644')
    delete_vehicles_by_ids(pg_conn, (pk,))
    rs = retrieve_vehicles_by_ids(pg_conn, (pk,))
    assert len(rs) == 0
