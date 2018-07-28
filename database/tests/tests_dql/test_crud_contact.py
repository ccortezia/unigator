import pytest
import toolz
import functools
from .fixtures import *  # flake8: noqa


def test_create_contact(db):
    pk = create_contact(db, 'Adolf')
    rs = retrieve_contacts_by_ids(db, (pk,))
    assert len(rs) == 1
    assert rs[0]['contact_id'] == pk
    assert rs[0]['contact_name'] == 'Adolf'


def test_create_contact_protected_name_should_err(db):
    with pytest.raises(Exception):
        create_contact(db, 'SYSTEM')


def test_retrieve_contacts_by_ids(db):
    names = ['Adolf', 'Pietro', 'Adam', 'Joan', 'Alex']
    pks = [create_contact(db, name) for name in names]
    rs = retrieve_contacts_by_ids(db, pks)
    assert [r['contact_id'] for r in rs] == pks
    assert [r['contact_name'] for r in rs] == names


def test_retrieve_person_contacts_by_name(db):
    for name in [
        'Gordon', 'Ash', 'Alfred', 'Henry', 'Hannah', 'Paul', 'Richard', 'Tony', 'Cindy',
        'Luis', 'Jessica', 'Vincent', 'Heidi', 'Brian', 'Richard', 'Caitlin', 'Kevin',
        'Karen', 'Catherine', 'Charles', 'Robin', 'Heather', 'Vernon', 'Kathleen', 'Jared',
        'Chelsea', 'Ashley', 'Joseph', 'Jeffrey', 'Tyler', 'Wesley'
    ]:
        create_contact(db, name)

    fetch = functools.partial(fetch_pages, db,
                              retrieve_person_contacts_by_name,
                              ('contact_name', 'contact_id'))

    assert fetch('%',   ('', 0),        5) == (5, 5, 5, 5, 5, 5, 1, 0)
    assert fetch('%',   ('Caitlin', 0), 5) == (5, 5, 5, 5, 5, 2, 0)
    assert fetch('%',   ('Caitlin', 0), 8) == (8, 8, 8, 3, 0)
    assert fetch('A%',  ('', 0),        10) == (3, 0)
    assert fetch('A%',  ('Caitlin', 0), 10) == (0,)
    assert fetch('C%',  ('', 0),        1) == (1, 1, 1, 1, 1, 0)
    assert fetch('Ash', ('', 0),        8) == (1, 0)
    assert fetch('Ash', ('', 0),        0) == (0,)
    assert fetch('',    ('', 0),        5) == (0,)


def test_retrieve_person_contacts_by_name_system_not_listed(db):
    rs = retrieve_person_contacts_by_name(db, 'SYSTEM', ('', 0), 100)
    assert len(rs) == 0


def test_update_contact(db):
    pk = create_contact(db, 'Adolf')
    update_contact(db, pk, contact_name='Joe')
    rs = retrieve_contacts_by_ids(db, (pk,))
    assert rs[0]['contact_name'] == 'Joe'


def test_update_contact_protected_pk_should_err(db):
    with pytest.raises(Exception):
        update_contact(db, 0, contact_name='Joe')


def test_update_contact_pk_should_err(db):
    pk = create_contact(db, 'Adolf')
    with pytest.raises(Exception):
        db.execute('update ac_contacts set contact_id=10 where contact_id = %(pk)s', {'pk': pk})


def test_update_contact_protected_name_should_err(db):
    pk = create_contact(db, 'Adolf')
    with pytest.raises(Exception):
        update_contact(db, pk, contact_name='SYSTEM')


def test_delete_contacts_by_ids(db):
    pk = create_contact(db, 'Adolf')
    delete_contacts_by_ids(db, (pk,))
    rs = retrieve_contacts_by_ids(db, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(db):
    with pytest.raises(Exception):
        delete_contacts_by_ids(db, (0,))


# ----------

def fetch_pages(db, op, pagekey, query, pgpos, pgsiz):
    pagelens = []
    last_count = -1
    while last_count != 0:
        results = op(db, query, pgpos, pgsiz)
        pgpos = toolz.tail(1, toolz.pluck(list(pagekey), results))
        last_count = len(results)
        pagelens.append(last_count)
    return tuple(pagelens)
