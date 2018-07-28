import pytest

from unigator.operations import *  # flake8: noqa


@pytest.fixture
def basic_levels(db):
    create_auth_level(db, 'sys/0001', auth_grant=False)
    create_auth_level(db, 'sys/0002', auth_grant=False)
    create_auth_level(db, 'sys/0003', auth_grant=False)
    create_auth_level(db, 'sys/0004', auth_grant=False)
    create_auth_level(db, 'sys/0005', auth_grant=True)


@pytest.fixture
def basic_flow(db, basic_levels):
    auth_flow = create_auth_flow(db)
    create_auth_flow_st(db, auth_flow, 'sys/0001', st_term=False)
    create_auth_flow_st(db, auth_flow, 'sys/0002', st_term=False)
    create_auth_flow_st(db, auth_flow, 'sys/0003', st_term=False)
    create_auth_flow_st(db, auth_flow, 'sys/0004', st_term=False)
    create_auth_flow_st(db, auth_flow, 'sys/0005', st_term=False)
    create_auth_flow_tr(db, auth_flow, when_ev='sys/0001', curr_st='sys/none', next_st='sys/0001')
    create_auth_flow_tr(db, auth_flow, when_ev='sys/0002', curr_st='sys/0001', next_st='sys/0002')
    create_auth_flow_tr(db, auth_flow, when_ev='sys/0003', curr_st='sys/0002', next_st='sys/0003')
    create_auth_flow_tr(db, auth_flow, when_ev='sys/0004', curr_st='sys/0003', next_st='sys/0004')
    create_auth_flow_tr(db, auth_flow, when_ev='sys/0005', curr_st='sys/0004', next_st='sys/0005')
    return auth_flow


@pytest.fixture
def ctcgrp_a(db):
    return create_contact_group(db, 'ctcgrp_a')


@pytest.fixture
def ctcgrp_b(db):
    return create_contact_group(db, 'ctcgrp_b')


@pytest.fixture
def ctc_a1(db, ctcgrp_a):
    ctc = create_contact(db, 'ctc_a1')
    create_contact_group_membership(db, 'ctcgrp_a', ctc)
    return ctc


@pytest.fixture
def ctc_b1(db, ctcgrp_b):
    ctc = create_contact(db, 'ctc_b1')
    create_contact_group_membership(db, 'ctcgrp_b', ctc)
    return ctc


@pytest.fixture
def ctc_nogrp(db):
    return create_contact(db, 'ctc_nogrp')


@pytest.fixture
def locgrp_a(db):
    return create_location_group(db, 'locgrp_a')


@pytest.fixture
def locgrp_b(db):
    return create_location_group(db, 'locgrp_b')


@pytest.fixture
def loc_a1(db, locgrp_a):
    loc = create_location(db, 'loc_a1')
    create_location_group_membership(db, 'locgrp_a', loc)
    return loc


@pytest.fixture
def loc_b1(db, locgrp_b):
    loc = create_location(db, 'loc_b1')
    create_location_group_membership(db, 'locgrp_b', loc)
    return loc


@pytest.fixture
def loc_nogrp(db, locgrp_b):
    return create_location(db, 'loc_nogrp')


@pytest.fixture
def ckpgrp_a(db):
    return create_checkpoint_group(db, 'ckpgrp_a')


@pytest.fixture
def ckpgrp_b(db):
    return create_checkpoint_group(db, 'ckpgrp_b')


@pytest.fixture
def ckp_a1(db, ckpgrp_a):
    ckp = create_checkpoint(db, 'ckp_a1')
    create_checkpoint_group_membership(db, 'ckpgrp_a', ckp)
    return ckp


@pytest.fixture
def ckp_b1(db, ckpgrp_b):
    ckp = create_checkpoint(db, 'ckp_b1')
    create_checkpoint_group_membership(db, 'ckpgrp_b', ckp)
    return ckp


@pytest.fixture
def ckp_nogrp(db):
    return create_checkpoint(db, 'ckp_nogrp')


@pytest.fixture
def vhcgrp_a(db):
    return create_vehicle_group(db, 'vhcgrp_a')


@pytest.fixture
def vhcgrp_b(db):
    return create_vehicle_group(db, 'vhcgrp_b')


@pytest.fixture
def vhc_a1(db, vhcgrp_a):
    vhc = create_vehicle(db, 'UUU0001')
    create_vehicle_group_membership(db, 'vhcgrp_a', vhc)
    return vhc


@pytest.fixture
def vhc_b1(db, vhcgrp_b):
    vhc = create_vehicle(db, 'UUU0002')
    create_vehicle_group_membership(db, 'vhcgrp_b', vhc)
    return vhc


@pytest.fixture
def vhc_nogrp(db):
    return create_vehicle(db, 'UUU0003')


@pytest.fixture
def blank_rules(db):
    return [
        create_auth_rule(db, 1, 'sys/none'),
        create_auth_rule(db, 2, 'sys/none'),
        create_auth_rule(db, 3, 'sys/none'),
        create_auth_rule(db, 4, 'sys/none'),
        create_auth_rule(db, 5, 'sys/none'),
        create_auth_rule(db, 6, 'sys/none'),
    ]
