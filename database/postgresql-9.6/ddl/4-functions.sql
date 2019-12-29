/* ------------------------------------------------------------------------------------------------
 Access Authorization Flows
------------------------------------------------------------------------------------------------ */

-- Stock predicate hooked into the rule evaluation query: should not affect the evaluation.
create function ung.ac_auth_rule_custom_predicate(ctc integer,
                                                  vhc integer,
                                                  ckp integer,
                                                  loc_orig integer,
                                                  loc_dest integer,
                                                  datetime timestamptz)
    returns boolean
    language plpgsql
as $$
begin
    return true;
end;
$$;

-- Custom user provided function, predicate hooked into the rule evaluation query.
create function custom.ac_auth_rule_custom_predicate(ctc integer,
                                                     vhc integer,
                                                     ckp integer,
                                                     loc_orig integer,
                                                     loc_dest integer,
                                                     datetime timestamptz)
    returns boolean
    language plpgsql
as $$
begin
    return true;
end;
$$;

/* ------------------------------------------------------------------------------------------------
 Access History
------------------------------------------------------------------------------------------------ */

--
create function ung.ac_archive_finished_processes()
    returns table (archived_proc_id bigint, archived_finished_at timestamptz)
    language plpgsql
as $$
begin
    return query
    with moved as (
        insert into ung.ac_history
            (proc_id, ctc, loc_orig, loc_dest, ckp, vhc, auth_name, auth_by, auth_at, started_at, finished_at)
        select proc_id, ctc, loc_orig, loc_dest, ckp, vhc, curr_st, auth_by, auth_at, started_at, finished_at
        from ung.ac_process_snapshots procs
        where procs.finished_at is not null
            and procs.curr_st is not null
            and procs.st_term = true
        returning proc_id, finished_at
    ),
    deleted as (
        delete from ung.ac_processes procs
        where procs.proc_id = any(array(select proc_id from moved))
        returning procs.proc_id, procs.finished_at
    )
    select * from deleted
    order by finished_at asc;
end;
$$;
