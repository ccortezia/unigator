import toolz
from .fixtures import *  # noqa
from .fixtures import _create_auth_rule
from .utils import dt
from unigator_db import (
    create_location_assign_type,
    assign_contact_to_location,
    update_auth_rule,
    retrieve_auth_rules_by_ids,
    create_process,
    update_process,
    retrieve_processes_rule_matches,
    retrieve_processes_rule_selections,
)


def test_rule_match_success_ctc_same(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    update_process(pg_conn, proc_2, ctc_b1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_ctc_null(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    update_process(pg_conn, proc_2, ctc_b1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_vhc_same(pg_conn, vhc_a1, vhc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, vhc=vhc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, None, None, vhc_a1)
    update_process(pg_conn, proc_2, None, None, None, None, vhc_b1)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_vhc_null(pg_conn, vhc_a1, vhc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, None, None, vhc_a1)
    update_process(pg_conn, proc_2, None, None, None, None, vhc_b1)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_ckp_same(pg_conn, ckp_a1, ckp_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ckp=ckp_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None,  None, None, ckp_a1, None)
    update_process(pg_conn, proc_2, None,  None, None, ckp_b1, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_ckp_null(pg_conn, ckp_a1, ckp_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, None, ckp_a1, None)
    update_process(pg_conn, proc_2, None, None, None, ckp_b1, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_orig_same(pg_conn, loc_a1, loc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, loc_orig=loc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, loc_a1, None, None, None)
    update_process(pg_conn, proc_2, None, loc_b1, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_orig_null(pg_conn, loc_a1, loc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, loc_a1, None, None, None)
    update_process(pg_conn, proc_2, None, loc_b1, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_dest_same(pg_conn, loc_a1, loc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, loc_dest=loc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, loc_a1, None, None)
    update_process(pg_conn, proc_2, None, None, loc_b1, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_dest_null(pg_conn, loc_a1, loc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, loc_a1, None, None)
    update_process(pg_conn, proc_2, None, None, loc_b1, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_ctc_group_same(pg_conn, ctc_a1, ctc_b1, ctc_nogrp, ctcgrp_a, ctcgrp_b):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc_grp=ctcgrp_a)
    patch_auth_rule(pg_conn, rule_2, ctc_grp=ctcgrp_b)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    proc_3 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    update_process(pg_conn, proc_2, ctc_b1, None, None, None, None)
    update_process(pg_conn, proc_3, ctc_nogrp, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_3]
    assert _proc_matches(grouped, proc_2) == [rule_2, rule_3]
    assert _proc_matches(grouped, proc_3) == [rule_3]


def test_rule_match_success_vhc_group_same(pg_conn, vhc_a1, vhc_b1, vhc_nogrp, vhcgrp_a, vhcgrp_b):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, vhc_grp=vhcgrp_a)
    patch_auth_rule(pg_conn, rule_2, vhc_grp=vhcgrp_b)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    proc_3 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, None, None, vhc_a1)
    update_process(pg_conn, proc_2, None, None, None, None, vhc_b1)
    update_process(pg_conn, proc_3, None, None, None, None, vhc_nogrp)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_3]
    assert _proc_matches(grouped, proc_2) == [rule_2, rule_3]
    assert _proc_matches(grouped, proc_3) == [rule_3]


def test_rule_match_success_ckp_group_same(pg_conn, ckp_a1, ckp_b1, ckp_nogrp, ckpgrp_a, ckpgrp_b):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ckp_grp=ckpgrp_a)
    patch_auth_rule(pg_conn, rule_2, ckp_grp=ckpgrp_b)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    proc_3 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, None, ckp_a1, None)
    update_process(pg_conn, proc_2, None, None, None, ckp_b1, None)
    update_process(pg_conn, proc_3, None, None, None, ckp_nogrp, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_3]
    assert _proc_matches(grouped, proc_2) == [rule_2, rule_3]
    assert _proc_matches(grouped, proc_3) == [rule_3]


def test_rule_match_success_dest_group_same(pg_conn, loc_a1, loc_b1, loc_nogrp, locgrp_a, locgrp_b):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, loc_grp=locgrp_a)
    patch_auth_rule(pg_conn, rule_2, loc_grp=locgrp_b)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    proc_3 = create_process(pg_conn)
    update_process(pg_conn, proc_1, None, None, loc_a1, None, None)
    update_process(pg_conn, proc_2, None, None, loc_b1, None, None)
    update_process(pg_conn, proc_3, None, None, loc_nogrp, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_3]
    assert _proc_matches(grouped, proc_2) == [rule_2, rule_3]
    assert _proc_matches(grouped, proc_3) == [rule_3]


def test_rule_match_success_dest_ctc_assign_same(pg_conn, loc_a1, loc_b1, ctc_a1, ctc_b1):
    create_location_assign_type(pg_conn, 'keeper', 'Keeper')
    create_location_assign_type(pg_conn, 'dweller', 'Dweller')
    assign_contact_to_location(pg_conn, loc_a1, ctc_a1, 'dweller')
    assign_contact_to_location(pg_conn, loc_a1, ctc_b1, 'keeper')
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, loc_ass='dweller')
    patch_auth_rule(pg_conn, rule_2, loc_ass='keeper')
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    proc_3 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, loc_a1, None, None)  # assignee aiming correct loc
    update_process(pg_conn, proc_2, ctc_b1, None, loc_a1, None, None)  # assignee aiming correct loc
    update_process(pg_conn, proc_3, ctc_b1, None, loc_b1, None, None)  # assignee aiming incorrect loc
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_3]
    assert _proc_matches(grouped, proc_2) == [rule_2, rule_3]
    assert _proc_matches(grouped, proc_3) == [rule_3]


def test_rule_match_success_year_range_min(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, year0=2018)
    patch_auth_rule(pg_conn, rule_2, year0=2010)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_year_range_max(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, year1=2018)
    patch_auth_rule(pg_conn, rule_2, year1=2010)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_month_range_min(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, month0=1)
    patch_auth_rule(pg_conn, rule_2, month0=12)
    proc_1 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 12, 1))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_month_range_max(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, month1=1)
    patch_auth_rule(pg_conn, rule_2, month1=12)
    proc_1 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 12, 1))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_monthday_range_min(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, mday0=1)
    patch_auth_rule(pg_conn, rule_2, mday0=31)
    proc_1 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 1, 31))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_monthday_range_max(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, mday1=1)
    patch_auth_rule(pg_conn, rule_2, mday1=31)
    proc_1 = create_process(pg_conn, started_at=dt(2010, 1, 1))
    proc_2 = create_process(pg_conn, started_at=dt(2010, 1, 31))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_weekday_range_min(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, wday0=0)
    patch_auth_rule(pg_conn, rule_2, wday0=6)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15))  # 0, monday
    proc_2 = create_process(pg_conn, started_at=dt(2018, 7, 14))  # 6, sunday
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_weekday_range_max(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, wday1=0)
    patch_auth_rule(pg_conn, rule_2, wday1=6)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15))  # 0, monday
    proc_2 = create_process(pg_conn, started_at=dt(2018, 7, 14))  # 6, sunday
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_daytime_range_min(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour0=0, minute0=0)
    patch_auth_rule(pg_conn, rule_2, hour0=23, minute0=59)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 0, 0))
    proc_2 = create_process(pg_conn, started_at=dt(2018, 7, 15, 23, 59))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_2]


def test_rule_match_success_daytime_range_max(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour1=0, minute1=0)
    patch_auth_rule(pg_conn, rule_2, hour1=23, minute1=59)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 0, 0))
    proc_2 = create_process(pg_conn, started_at=dt(2018, 7, 15, 23, 59))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_2]


def test_rule_match_success_daytime_above_max_minute_within_daytime_range(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour0=0, minute0=0, hour1=3, minute1=20)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 1, 35))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]


def test_rule_match_success_daytime_equal_max_hour_within_daytime_range(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour0=0, minute0=0, hour1=3, minute1=20)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 3, 15))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]


def test_rule_match_failure_daytime_above_max_hour_below_max_minute(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour0=0, minute0=0, hour1=3, minute1=20)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 4, 1))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == []


def test_rule_match_success_daytime_below_min_minute_within_daytime_range(pg_conn):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, hour0=0, minute0=10, hour1=3, minute1=20)
    proc_1 = create_process(pg_conn, started_at=dt(2018, 7, 15, 2, 5))
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]


def test_processes_rule_matches_single_process_matches_one_rule(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_2, ctc=ctc_b1)
    patch_auth_rule(pg_conn, rule_3, ctc=ctc_b1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == []


def test_processes_rule_matches_single_process_matches_multiple_rules(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_2, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_3, ctc=ctc_b1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == []


def test_processes_rule_matches_single_process_matches_no_rule(pg_conn, ctc_a1, ctc_b1):
    proc_1 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == []


def test_processes_rule_matches_no_processes_match_no_rule(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_2, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_3, ctc=ctc_b1)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    assert processes_matches == []


def test_processes_rule_matches_multiple_processes_match_single_rule(pg_conn, ctc_a1, ctc_b1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    update_process(pg_conn, proc_2, ctc_a1, None, None, None, None)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1]
    assert _proc_matches(grouped, proc_2) == [rule_1]


def test_processes_rule_matches_multiple_processes_match_different_rules(pg_conn, ctc_a1, ctc_b1, vhc_a1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, vhc=vhc_a1)
    patch_auth_rule(pg_conn, rule_2, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_3, ctc=ctc_b1, vhc=vhc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, vhc_a1)
    update_process(pg_conn, proc_2, ctc_b1, None, None, None, vhc_a1)
    processes_matches = retrieve_processes_rule_matches(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_1, rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1, rule_3]


def test_processes_rule_selections_highest_order_rule_selected_from_multiple_matches(pg_conn, ctc_a1, ctc_b1, vhc_a1):
    rule_1 = _create_auth_rule(pg_conn, 1, 'sys/none')
    rule_2 = _create_auth_rule(pg_conn, 2, 'sys/none')
    rule_3 = _create_auth_rule(pg_conn, 3, 'sys/none')
    patch_auth_rule(pg_conn, rule_1, ctc=ctc_b1)
    patch_auth_rule(pg_conn, rule_2, ctc=ctc_a1)
    patch_auth_rule(pg_conn, rule_3, ctc=ctc_b1, vhc=vhc_a1)
    proc_1 = create_process(pg_conn)
    proc_2 = create_process(pg_conn)
    update_process(pg_conn, proc_1, ctc_a1, None, None, None, None)
    update_process(pg_conn, proc_2, ctc_b1, None, None, None, vhc_a1)
    processes_matches = retrieve_processes_rule_selections(pg_conn)
    grouped = toolz.groupby('proc_id', processes_matches)
    assert _proc_matches(grouped, proc_1) == [rule_2]
    assert _proc_matches(grouped, proc_2) == [rule_1]


# --------

def patch_auth_rule(pg_conn, rule_id, **kwargs):
    rs = retrieve_auth_rules_by_ids(pg_conn, (rule_id,))
    _kwargs = dict(rs[0], **kwargs)
    _kwargs.pop('rule_id')
    update_auth_rule(pg_conn, rule_id, **_kwargs)


def _proc_matches(grouped, proc_id):
    return [_ for _ in toolz.pluck('match_rule_id', grouped[proc_id]) if _]
