import pytest
from .fixtures import *  # flake8: noqa


def test_create_auth_level(db):
    pk = create_auth_level(db, 'app/special', auth_grant=True)
    rs = retrieve_auth_levels_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['auth_name'] == pk
    assert rs[0]['auth_grant'] is True


def test_retrieve_auth_levels_by_ids(db):
    infos = [('app/special', True), ('app/special2', False), ('user/custom', False)]
    pks = [create_auth_level(db, *info) for info in infos]
    rs = retrieve_auth_levels_by_ids(db, pks)
    assert [r['auth_name'] for r in rs] == list(list(zip(*infos))[0])
    assert [r['auth_grant'] for r in rs] == list(list(zip(*infos))[1])


def test_update_auth_level(db):
    pk = create_auth_level(db, 'app/special', auth_grant=True)
    update_auth_level(db, pk, auth_name='app/201', auth_grant=False)
    rs = retrieve_auth_levels_by_ids(db, ('app/201',))
    assert rs[0]['auth_name'] == 'app/201'
    assert rs[0]['auth_grant'] is False


def test_update_auth_level_protected_pk_should_err(db):
    with pytest.raises(Exception):
        update_auth_level(db, 'sys/none', auth_name='sys/none', auth_grant=False)
    db.rollback()
    with pytest.raises(Exception):
        update_auth_level(db, 'sys/none', auth_name='sys/app', auth_grant=False)


def test_delete_auth_levels_by_ids(db):
    pk = create_auth_level(db, 'app/special', auth_grant=True)
    delete_auth_levels_by_ids(db, (pk,))
    rs = retrieve_auth_levels_by_ids(db, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(db):
    with pytest.raises(Exception):
        delete_auth_levels_by_ids(db, ('sys/none',))

