import pytest
from .fixtures import *  # flake8: noqa


def test_create_location(db):
    pk = create_location(db, 'Place 1')
    rs = retrieve_locations_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['location_id'] == pk
    assert rs[0]['addr_1'] == 'Place 1'


def test_retrieve_locations_by_ids(db):
    addrs = ['Place 1', 'Place 2', 'Place 3', 'Place 4', 'Place 5']
    pks = [create_location(db, addr) for addr in addrs]
    rs = retrieve_locations_by_ids(db, pks)
    assert [r['location_id'] for r in rs] == pks
    assert [r['addr_1'] for r in rs] == addrs


def test_update_location(db):
    pk = create_location(db, 'Place 1')
    update_location(db, pk, addr_1='Nowhere')
    rs = retrieve_locations_by_ids(db, (pk,))
    assert rs[0]['addr_1'] == 'Nowhere'


def test_update_location_protected_pk_should_err(db):
    with pytest.raises(Exception):
        update_location(db, 0, addr_1='Nowhere')


def test_update_location_pk_should_err(db):
    pk = create_location(db, 'Place 1')
    with pytest.raises(Exception):
        db.execute('update ac_locations set location_id=1088 where location_id = %(pk)s', {'pk': pk})


def test_delete_locations_by_ids(db):
    pk = create_location(db, 'Place 1')
    delete_locations_by_ids(db, (pk,))
    rs = retrieve_locations_by_ids(db, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(db):
    with pytest.raises(Exception):
        delete_locations_by_ids(db, (0,))

