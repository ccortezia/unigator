
## A minimal SQL driven Setup + Physical Access use case

_NOTE: This sample was tested only against the postgresql-4.9 component._

```sql
begin;

-- Creates some basic landscape setup.
insert into ac_checkpoints (checkpoint_name) values ('Main Gate');
insert into ac_locations (addr_1) values ('441 Sungarden Blvd.');
insert into ac_contacts (contact_name) values ('Visitor');
insert into ac_contacts (contact_name) values ('Gatekeeper');

-- Inserts a new authorization level named sys/allow.
insert into ac_auth_levels (auth_name, auth_grant) values ('sys/allow', true);

-- Adds a valid transition from sys/none to sys/allow into the default access flow.
insert into ac_auth_flow_sts (auth_flow_id, st_name, st_term) values (0, 'sys/allow', true);
insert into ac_auth_flow_trs (auth_flow_id, when_ev, curr_st, next_st) values
                             (0, 'sys/allow', 'sys/none', 'sys/allow');

-- Creates an automation rule to generate a sys/allow event for any evaluated process.
insert into ac_auth_rules (effect) values ('sys/allow');

-- Creates an access process to track some physical access attempt.
insert into ac_processes (ctc, ckp, loc_orig, loc_dest) values (
    (select contact_id from ac_contacts where contact_name = 'Visitor'),
    (select checkpoint_id from ac_checkpoints where checkpoint_name = 'Main Gate'),
    (select location_id from ac_locations where addr_1 = 'EXTERIOR'),
    (select location_id from ac_locations where addr_1 = '441 Sungarden Blvd.')
);

-- Creates authorization event to evolve process flow.
insert into ac_process_auth_events (proc_id, auth_by, auth_name) values (
    (select proc_id from ac_processes order by started_at desc limit 1),
    (select contact_id from ac_contacts where contact_name = 'Gatekeeper'),
    (select resolved_auth_name from ac_processes_rule_selections where proc_id = (
        select proc_id from ac_processes order by started_at desc limit 1
    ))
);

-- Terminates process.
update ac_processes set finished_at = statement_timestamp() where proc_id = (
    select proc_id from ac_processes order by started_at desc limit 1
);

-- Archive terminated process in history.
select * from ac_archive_finished_processes();

-- List archived access history.
select * from ac_history;

rollback;
```
