import pytest
from .fixtures import *  # flake8: noqa


def test_create_vehicle(db):
    pk = create_vehicle(db, 'IUY5644')
    rs = retrieve_vehicles_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['vehicle_id'] == pk
    assert rs[0]['plate'] == 'IUY5644'


def test_retrieve_vehicles_by_ids(db):
    plates = ['IUY5644', 'Place 2', 'Place 3', 'Place 4', 'Place 5']
    pks = [create_vehicle(db, plate) for plate in plates]
    rs = retrieve_vehicles_by_ids(db, pks)
    assert [r['vehicle_id'] for r in rs] == pks
    assert [r['plate'] for r in rs] == plates


def test_update_vehicle(db):
    pk = create_vehicle(db, 'IUY5644')
    update_vehicle(db, pk, plate='AAA0000')
    rs = retrieve_vehicles_by_ids(db, (pk,))
    assert rs[0]['plate'] == 'AAA0000'


def test_update_vehicle_pk_should_err(db):
    pk = create_vehicle(db, 'IUY5644')
    with pytest.raises(Exception):
        db.execute('update ac_vehicles set vehicle_id=9090 where vehicle_id = %(pk)s', {'pk': pk})


def test_delete_vehicles_by_ids(db):
    pk = create_vehicle(db, 'IUY5644')
    delete_vehicles_by_ids(db, (pk,))
    rs = retrieve_vehicles_by_ids(db, (pk,))
    assert len(rs) == 0
