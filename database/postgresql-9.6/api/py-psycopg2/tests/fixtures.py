import pytest

from unigator_db import (
    create_contact,
    create_contact_group,
    add_contact_group_member,
    create_location,
    create_location_group,
    add_location_group_member,
    create_checkpoint,
    create_checkpoint_group,
    add_checkpoint_group_member,
    create_vehicle,
    create_vehicle_group,
    add_vehicle_group_member,
    create_auth_level,
    create_auth_flow,
    create_auth_flow_st,
    create_auth_flow_tr,
    create_auth_rule,
    SQLDefault
)


@pytest.fixture
def basic_levels(pg_conn):
    create_auth_level(pg_conn, 'sys/0001', auth_grant=False)
    create_auth_level(pg_conn, 'sys/0002', auth_grant=False)
    create_auth_level(pg_conn, 'sys/0003', auth_grant=False)
    create_auth_level(pg_conn, 'sys/0004', auth_grant=False)
    create_auth_level(pg_conn, 'sys/0005', auth_grant=True)


@pytest.fixture
def basic_flow(pg_conn, basic_levels):
    auth_flow = create_auth_flow(pg_conn)
    create_auth_flow_st(pg_conn, auth_flow, 'sys/0001', st_term=False)
    create_auth_flow_st(pg_conn, auth_flow, 'sys/0002', st_term=False)
    create_auth_flow_st(pg_conn, auth_flow, 'sys/0003', st_term=False)
    create_auth_flow_st(pg_conn, auth_flow, 'sys/0004', st_term=False)
    create_auth_flow_st(pg_conn, auth_flow, 'sys/0005', st_term=False)
    create_auth_flow_tr(pg_conn, auth_flow, when_ev='sys/0001', curr_st='sys/none', next_st='sys/0001')
    create_auth_flow_tr(pg_conn, auth_flow, when_ev='sys/0002', curr_st='sys/0001', next_st='sys/0002')
    create_auth_flow_tr(pg_conn, auth_flow, when_ev='sys/0003', curr_st='sys/0002', next_st='sys/0003')
    create_auth_flow_tr(pg_conn, auth_flow, when_ev='sys/0004', curr_st='sys/0003', next_st='sys/0004')
    create_auth_flow_tr(pg_conn, auth_flow, when_ev='sys/0005', curr_st='sys/0004', next_st='sys/0005')
    return auth_flow


@pytest.fixture
def ctcgrp_a(pg_conn):
    return create_contact_group(pg_conn, 'ctcgrp_a')


@pytest.fixture
def ctcgrp_b(pg_conn):
    return create_contact_group(pg_conn, 'ctcgrp_b')


@pytest.fixture
def ctc_a1(pg_conn, ctcgrp_a):
    ctc = create_contact(pg_conn, 'ctc_a1')
    add_contact_group_member(pg_conn, 'ctcgrp_a', ctc)
    return ctc


@pytest.fixture
def ctc_b1(pg_conn, ctcgrp_b):
    ctc = create_contact(pg_conn, 'ctc_b1')
    add_contact_group_member(pg_conn, 'ctcgrp_b', ctc)
    return ctc


@pytest.fixture
def ctc_nogrp(pg_conn):
    return create_contact(pg_conn, 'ctc_nogrp')


@pytest.fixture
def locgrp_a(pg_conn):
    return create_location_group(pg_conn, 'locgrp_a')


@pytest.fixture
def locgrp_b(pg_conn):
    return create_location_group(pg_conn, 'locgrp_b')


@pytest.fixture
def loc_a1(pg_conn, locgrp_a):
    loc = create_location(pg_conn, 'loc_a1')
    add_location_group_member(pg_conn, 'locgrp_a', loc)
    return loc


@pytest.fixture
def loc_b1(pg_conn, locgrp_b):
    loc = create_location(pg_conn, 'loc_b1')
    add_location_group_member(pg_conn, 'locgrp_b', loc)
    return loc


@pytest.fixture
def loc_nogrp(pg_conn, locgrp_b):
    return create_location(pg_conn, 'loc_nogrp')


@pytest.fixture
def ckpgrp_a(pg_conn):
    return create_checkpoint_group(pg_conn, 'ckpgrp_a')


@pytest.fixture
def ckpgrp_b(pg_conn):
    return create_checkpoint_group(pg_conn, 'ckpgrp_b')


@pytest.fixture
def ckp_a1(pg_conn, ckpgrp_a):
    ckp = create_checkpoint(pg_conn, 'ckp_a1')
    add_checkpoint_group_member(pg_conn, 'ckpgrp_a', ckp)
    return ckp


@pytest.fixture
def ckp_b1(pg_conn, ckpgrp_b):
    ckp = create_checkpoint(pg_conn, 'ckp_b1')
    add_checkpoint_group_member(pg_conn, 'ckpgrp_b', ckp)
    return ckp


@pytest.fixture
def ckp_nogrp(pg_conn):
    return create_checkpoint(pg_conn, 'ckp_nogrp')


@pytest.fixture
def vhcgrp_a(pg_conn):
    return create_vehicle_group(pg_conn, 'vhcgrp_a')


@pytest.fixture
def vhcgrp_b(pg_conn):
    return create_vehicle_group(pg_conn, 'vhcgrp_b')


@pytest.fixture
def vhc_a1(pg_conn, vhcgrp_a):
    vhc = create_vehicle(pg_conn, 'UUU0001')
    add_vehicle_group_member(pg_conn, 'vhcgrp_a', vhc)
    return vhc


@pytest.fixture
def vhc_b1(pg_conn, vhcgrp_b):
    vhc = create_vehicle(pg_conn, 'UUU0002')
    add_vehicle_group_member(pg_conn, 'vhcgrp_b', vhc)
    return vhc


@pytest.fixture
def vhc_nogrp(pg_conn):
    return create_vehicle(pg_conn, 'UUU0003')


@pytest.fixture
def blank_rules(pg_conn):
    return [
        _create_auth_rule(pg_conn, 1, 'sys/none'),
        _create_auth_rule(pg_conn, 2, 'sys/none'),
        _create_auth_rule(pg_conn, 3, 'sys/none'),
        _create_auth_rule(pg_conn, 4, 'sys/none'),
        _create_auth_rule(pg_conn, 5, 'sys/none'),
        _create_auth_rule(pg_conn, 6, 'sys/none'),
    ]


# ---

def _create_auth_rule(pg_conn,
                      rule_ord=None,
                      effect=None,
                      ctc=None,
                      loc_orig=None,
                      loc_dest=None,
                      ckp=None,
                      vhc=None,
                      ctc_grp=None,
                      vhc_grp=None,
                      loc_grp=None,
                      ckp_grp=None,
                      loc_ass=None,
                      year0=None,
                      year1=None,
                      month0=None,
                      month1=None,
                      mday0=None,
                      mday1=None,
                      wday0=None,
                      wday1=None,
                      hour0=None,
                      hour1=None,
                      minute0=None,
                      minute1=None):
    return create_auth_rule(pg_conn,
                            rule_ord=rule_ord if rule_ord is not None else SQLDefault(),
                            effect=effect if effect is not None else SQLDefault(),
                            ctc=ctc if ctc is not None else SQLDefault(),
                            loc_orig=loc_orig if loc_orig is not None else SQLDefault(),
                            loc_dest=loc_dest if loc_dest is not None else SQLDefault(),
                            ckp=ckp if ckp is not None else SQLDefault(),
                            vhc=vhc if vhc is not None else SQLDefault(),
                            ctc_grp=ctc_grp if ctc_grp is not None else SQLDefault(),
                            vhc_grp=vhc_grp if vhc_grp is not None else SQLDefault(),
                            loc_grp=loc_grp if loc_grp is not None else SQLDefault(),
                            ckp_grp=ckp_grp if ckp_grp is not None else SQLDefault(),
                            loc_ass=loc_ass if loc_ass is not None else SQLDefault(),
                            year0=year0 if year0 is not None else SQLDefault(),
                            year1=year1 if year1 is not None else SQLDefault(),
                            month0=month0 if month0 is not None else SQLDefault(),
                            month1=month1 if month1 is not None else SQLDefault(),
                            mday0=mday0 if mday0 is not None else SQLDefault(),
                            mday1=mday1 if mday1 is not None else SQLDefault(),
                            wday0=wday0 if wday0 is not None else SQLDefault(),
                            wday1=wday1 if wday1 is not None else SQLDefault(),
                            hour0=hour0 if hour0 is not None else SQLDefault(),
                            hour1=hour1 if hour1 is not None else SQLDefault(),
                            minute0=minute0 if minute0 is not None else SQLDefault(),
                            minute1=minute1 if minute1 is not None else SQLDefault())
