import pytest
from .fixtures import *  # flake8: noqa


def test_create_checkpoint(db):
    pk = create_checkpoint(db, 'Gate 1')
    rs = retrieve_checkpoints_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['checkpoint_id'] == pk
    assert rs[0]['checkpoint_name'] == 'Gate 1'


def test_retrieve_checkpoints_by_ids(db):
    names = ['Gate 1', 'Place 2', 'Place 3', 'Place 4', 'Place 5']
    pks = [create_checkpoint(db, name) for name in names]
    rs = retrieve_checkpoints_by_ids(db, pks)
    assert [r['checkpoint_id'] for r in rs] == pks
    assert [r['checkpoint_name'] for r in rs] == names


def test_update_checkpoint(db):
    pk = create_checkpoint(db, 'Gate 1')
    update_checkpoint(db, pk, checkpoint_name='Gate 20')
    rs = retrieve_checkpoints_by_ids(db, (pk,))
    assert rs[0]['checkpoint_name'] == 'Gate 20'


def test_update_checkpoint_pk_should_err(db):
    pk = create_checkpoint(db, 'Gate 1')
    with pytest.raises(Exception):
        db.execute('update ac_checkpoints set checkpoint_id=10 where checkpoint_id = %(pk)s', {'pk': pk})


def test_delete_checkpoints_by_ids(db):
    pk = create_checkpoint(db, 'Gate 1')
    delete_checkpoints_by_ids(db, (pk,))
    rs = retrieve_checkpoints_by_ids(db, (pk,))
    assert len(rs) == 0
