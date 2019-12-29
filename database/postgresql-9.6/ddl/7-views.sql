/* ------------------------------------------------------------------------------------------------
 Access Processes
------------------------------------------------------------------------------------------------ */

--
create view ung.ac_process_histories as
    select
        procs.proc_id,
        procs.ctc,
        procs.vhc,
        procs.ckp,
        procs.loc_orig,
        procs.loc_dest,
        procs.auth_flow,
        procs.started_at,
        procs.finished_at,
        proc_evs.auth_by,
        proc_evs.auth_at,
        rank() over(latest_first_window) as ev_seq,
        ung.ac_auth_reduce(proc_evs.auth_name, procs.auth_flow) over(event_stream_window) as curr_st
    from ung.ac_processes procs
    left join ung.ac_process_auth_events proc_evs using (proc_id)
    window
        latest_first_window as (partition by procs.proc_id order by proc_evs.auth_at desc),
        event_stream_window as (partition by procs.proc_id order by proc_evs.auth_at asc)
;


--
create view ung.ac_process_snapshots as
    select proc_id, ctc, vhc, ckp, loc_orig, loc_dest, auth_flow, auth_by, auth_at, curr_st, sts.st_term, auth_levels.auth_grant, started_at, finished_at
    from ung.ac_process_histories joined
    left join ung.ac_auth_flow_sts sts on joined.auth_flow = sts.auth_flow_id and joined.curr_st = sts.st_name
    left join ung.ac_auth_levels auth_levels on auth_levels.auth_name = sts.st_name
    where joined.ev_seq = 1
;


--
create view ung.ac_process_snapshots_running as
    select * from ung.ac_process_snapshots
    where finished_at is null
;


--
create view ung.ac_processes_running as
    select * from ung.ac_processes
    where finished_at is null
;


--
create view ung.ac_processes_rule_matches as
    select
        proc.proc_id as proc_id,
        matched_rule.*

    from ung.ac_processes proc

    -- Matches running process to access rules.
    left join lateral (

        select
            rule.rule_id as match_rule_id,
            rule.rule_ord as match_rule_ord,
            resolved_auth.auth_name as resolved_auth_name,
            resolved_auth.auth_grant as resolved_auth_grant

        from ung.ac_auth_rules rule

        -- Brings in auth_levels data to compute the most restrictive rule (if multiple matches)
        join ung.ac_auth_levels resolved_auth on rule.effect = resolved_auth.auth_name

        -- Joins to allow matching on contact group.
        left join ung.ac_contact_groups ctcg on (rule.ctc_grp is null or ctcg.group_name = rule.ctc_grp)
        left join ung.ac_contact_groups_x_contacts ctcgxctc on
            ctcgxctc.group_name = ctcg.group_name
            and ctcgxctc.contact_id = proc.ctc

        -- Joins to allow matching on destination location group.
        left join ung.ac_location_groups locg on (rule.loc_grp is null or locg.group_name = rule.loc_grp)
        left join ung.ac_location_groups_x_locations locgxloc on
            locgxloc.group_name = locg.group_name
            and locgxloc.location_id = proc.loc_dest

        -- Joins to allow matching on checkpoint group.
        left join ung.ac_checkpoint_groups ckpg on (rule.ckp_grp is null or ckpg.group_name = rule.ckp_grp)
        left join ung.ac_checkpoint_groups_x_checkpoints ckpgxckp on
            ckpgxckp.group_name = ckpg.group_name
            and ckpgxckp.checkpoint_id = proc.ckp

        -- Joins to allow matching on vehicle group.
        left join ung.ac_vehicle_groups vhcg on (rule.vhc_grp is null or vhcg.group_name = rule.vhc_grp)
        left join ung.ac_vehicle_groups_x_vehicles vhcgxvhc on
            vhcgxvhc.group_name = vhcg.group_name
            and vhcgxvhc.vehicle_id = proc.vhc

        -- Joins to allow matching on contact x location assign.
        left join ung.ac_location_assign_types locass on (rule.loc_ass is null or locass.assign_type = rule.loc_ass)
        left join ung.ac_contacts_x_locations ctcxloc on
            ctcxloc.assign_type = locass.assign_type
            and ctcxloc.location_id = proc.loc_dest
            and ctcxloc.contact_id = proc.ctc

        where
            -- Matches if the process started within the rule's year range.
                extract(year from proc.started_at) between rule.year0 and rule.year1

            -- Matches if the process started within the rule's month range.
            and extract(month from proc.started_at) between rule.month0 and rule.month1

            -- Matches if the process started within the rule's month day range.
            and extract(day from proc.started_at) between rule.mday0 and rule.mday1

            -- Matches if the process started within the rule's weekday range.
            and extract(dow from proc.started_at) between rule.wday0 and rule.wday1

            -- Matches if the process started within the rule's hour/minute range.
            and (proc.started_at between
                (date_trunc('day', proc.started_at) + interval '1 hour' * rule.hour0 + interval '1 minute' * rule.minute0) and
                (date_trunc('day', proc.started_at) + interval '1 hour' * rule.hour1 + interval '1 minute' * rule.minute1))

            -- Matches if the process subject is the one optionally defined by the rule.
            and (rule.ctc is null or rule.ctc = proc.ctc)

            -- Matches if the process destination is the one optionally defined by the rule.
            and (rule.loc_dest is null or rule.loc_dest = proc.loc_dest)

            -- Matches if the process origin is the one optionally defined by the rule.
            and (rule.loc_orig is null or rule.loc_orig = proc.loc_orig)

            -- Matches if the process checkpoint is the one optionally defined by the rule.
            and (rule.ckp is null or rule.ckp = proc.ckp)

            -- Matches if the process vehicle is the one optionally defined by the rule.
            and (rule.vhc is null or rule.vhc = proc.vhc)

            -- Matches if the process destination is associated to the rule's optional location group.
            and (rule.ctc_grp is null or ctcgxctc.contact_id = proc.ctc)

            -- Matches if the process destination is associated to the rule's optional location group.
            and (rule.loc_grp is null or locgxloc.location_id = proc.loc_dest)

            -- Matches if the process checkpoint is associated to the rule's optional checkpoint group.
            and (rule.ckp_grp is null or ckpgxckp.checkpoint_id = proc.ckp)

            -- Matches if the process vehicle is associated to the rule's optional vehicle group.
            and (rule.vhc_grp is null or vhcgxvhc.vehicle_id = proc.vhc)

            -- Matches if the process subject is assigned to the destination as optionally defined by the rule.
            and (rule.loc_ass is null or (ctcxloc.location_id = proc.loc_dest and ctcxloc.contact_id = proc.ctc))

            -- Matches according to custom rules, in case an optional custom predicate is injected.
            and ac_auth_rule_custom_predicate(proc.ctc, proc.loc_orig, proc.loc_dest, proc.vhc, proc.ckp, proc.started_at)

        group by rule.rule_id, resolved_auth.auth_name, resolved_auth.auth_grant

        order by rule.rule_ord asc

    ) matched_rule on true
;

--
create view ung.ac_processes_rule_selections as
    with matches_ranked as (
        select *, row_number() over(matches_pr) as order_mark
        from ung.ac_processes_rule_matches matches
        window matches_pr as (partition by proc_id order by matches.match_rule_ord asc)
    )
    select proc_id, match_rule_id, resolved_auth_name, resolved_auth_grant
    from matches_ranked
    where order_mark = 1
;

/* ------------------------------------------------------------------------------------------------
 System
------------------------------------------------------------------------------------------------ */

--
create view ung.ac_stats as
    select schemaname,relname,n_live_tup
    from pg_stat_user_tables
    order by n_live_tup desc
;
