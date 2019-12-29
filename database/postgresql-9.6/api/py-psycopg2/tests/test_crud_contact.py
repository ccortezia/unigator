import pytest
# import toolz
# import functools
from unigator_db import (
    create_contact,
    retrieve_contacts_by_ids,
    retrieve_contacts_by_name,
    update_contact,
    delete_contacts_by_ids,
)


def test_create_contact(pg_conn):
    pk = create_contact(pg_conn, 'Adolf')
    rs = retrieve_contacts_by_ids(pg_conn, (pk,))
    assert len(rs) == 1
    assert rs[0]['contact_id'] == pk
    assert rs[0]['contact_name'] == 'Adolf'


def test_create_contact_protected_name_should_err(pg_conn):
    with pytest.raises(Exception):
        create_contact(pg_conn, 'SYSTEM')


def test_retrieve_contacts_by_ids(pg_conn):
    names = ['Adolf', 'Pietro', 'Adam', 'Joan', 'Alex']
    pks = [create_contact(pg_conn, name) for name in names]
    rs = retrieve_contacts_by_ids(pg_conn, tuple(pks))
    assert [r['contact_id'] for r in rs] == pks
    assert [r['contact_name'] for r in rs] == names


@pytest.mark.skip('Re-implement without toolz')
def test_retrieve_contacts_by_name(pg_conn):
    # for name in [
    #     'Gordon', 'Ash', 'Alfred', 'Henry', 'Hannah', 'Paul', 'Richard', 'Tony', 'Cindy',
    #     'Luis', 'Jessica', 'Vincent', 'Heidi', 'Brian', 'Richard', 'Caitlin', 'Kevin',
    #     'Karen', 'Catherine', 'Charles', 'Robin', 'Heather', 'Vernon', 'Kathleen', 'Jared',
    #     'Chelsea', 'Ashley', 'Joseph', 'Jeffrey', 'Tyler', 'Wesley'
    # ]:
    #     create_contact(pg_conn, name)

    # fetch = functools.partial(fetch_pages, db,
    #                           retrieve_contacts_by_name,
    #                           ('contact_name', 'contact_id'))

    # assert fetch('%',   ('', 0),        5) == (5, 5, 5, 5, 5, 5, 1, 0)
    # assert fetch('%',   ('Caitlin', 0), 5) == (5, 5, 5, 5, 5, 2, 0)
    # assert fetch('%',   ('Caitlin', 0), 8) == (8, 8, 8, 3, 0)
    # assert fetch('A%',  ('', 0),        10) == (3, 0)
    # assert fetch('A%',  ('Caitlin', 0), 10) == (0,)
    # assert fetch('C%',  ('', 0),        1) == (1, 1, 1, 1, 1, 0)
    # assert fetch('Ash', ('', 0),        8) == (1, 0)
    # assert fetch('Ash', ('', 0),        0) == (0,)
    # assert fetch('',    ('', 0),        5) == (0,)
    pass


def test_retrieve_contacts_by_name_system_not_listed(pg_conn):
    rs = retrieve_contacts_by_name(pg_conn, 'SYSTEM', ('', 0), 100)
    assert len(rs) == 0


def test_update_contact(pg_conn):
    pk = create_contact(pg_conn, 'Adolf')
    update_contact(pg_conn, pk, contact_name='Joe')
    rs = retrieve_contacts_by_ids(pg_conn, (pk,))
    assert rs[0]['contact_name'] == 'Joe'


def test_update_contact_protected_pk_should_err(pg_conn):
    with pytest.raises(Exception):
        update_contact(pg_conn, 0, contact_name='Joe')


def test_update_contact_pk_should_err(pg_conn):
    pk = create_contact(pg_conn, 'Adolf')
    with pytest.raises(Exception):
        pg_conn.execute('update ac_contacts set contact_id=10 where contact_id = %(pk)s', {'pk': pk})


def test_update_contact_protected_name_should_err(pg_conn):
    pk = create_contact(pg_conn, 'Adolf')
    with pytest.raises(Exception):
        update_contact(pg_conn, pk, contact_name='SYSTEM')


def test_delete_contacts_by_ids(pg_conn):
    pk = create_contact(pg_conn, 'Adolf')
    delete_contacts_by_ids(pg_conn, (pk,))
    rs = retrieve_contacts_by_ids(pg_conn, (pk,))
    assert len(rs) == 0


def test_delete_protected_should_err(pg_conn):
    with pytest.raises(Exception):
        delete_contacts_by_ids(pg_conn, (0,))


# ----------

# def fetch_pages(pg_conn, op, pagekey, query, pgpos, pgsiz):
#     pagelens = []
#     last_count = -1
#     while last_count != 0:
#         results = op(pg_conn, query, pgpos, pgsiz)
#         pgpos = toolz.tail(1, toolz.pluck(list(pagekey), results))
#         last_count = len(results)
#         pagelens.append(last_count)
#     return tuple(pagelens)
