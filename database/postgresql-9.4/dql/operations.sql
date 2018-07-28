-- name: $create_location<!
-- Creates a new location entry
insert into ung.ac_locations (addr_1, addr_2, addr_3, addr_4, addr_5, addr_6)
values (%(addr_1)s, %(addr_2)s, %(addr_3)s, %(addr_4)s, %(addr_5)s, %(addr_6)s)
returning location_id
;

-- name: $retrieve_locations_by_ids
-- Retrieves a list of locations matching the given location_id's
select *
from ung.ac_locations
where location_id in %(location_ids)s
;

-- name: $update_location!
-- Updates location entry
update ung.ac_locations
set addr_1=(%(addr_1)s),
    addr_2=(%(addr_2)s),
    addr_3=(%(addr_3)s),
    addr_4=(%(addr_4)s),
    addr_5=(%(addr_5)s),
    addr_6=(%(addr_6)s)
where location_id = %(location_id)s
;

-- name: $delete_locations_by_ids!
-- Deletes location entry
delete from ung.ac_locations
where location_id in %(location_ids)s
;

-- name: $create_location_group<!
-- Creates a new location_group
insert into ung.ac_location_groups (group_name)
values (%(group_name)s)
returning group_name
;

-- name: $update_location_group!
-- Updates
update ung.ac_location_groups
set group_name=(%(new_group_name)s)
where group_name=%(group_name)s
returning group_name
;

-- name: $retrieve_location_groups
-- Retrieves
select * from ung.ac_location_groups
;

-- name: $delete_location_groups_by_group_names!
-- Deletes
delete from ung.ac_location_groups
where group_name in %(group_names)s
;

-- name: $create_location_group_membership!
-- Creates
insert into ung.ac_location_groups_x_locations (group_name, location_id)
values (%(group_name)s, %(location_id)s)
;

-- name: $retrieve_location_group_memberships
-- Retrieves
select location_id from ung.ac_location_groups_x_locations
where group_name = %(group_name)s
;

-- name: $retrieve_location_groups_by_member_id
-- Retrieves
select group_name from ung.ac_location_groups_x_locations
where location_id = %(location_id)s
;

-- name: $delete_location_group_memberships_by_member_ids!
-- Deletes
delete from ung.ac_location_groups_x_locations
where group_name = %(group_name)s and location_id in %(location_ids)s
;

-- name: $delete_location_group_memberships_by_group_names!
-- Deletes
delete from ung.ac_location_groups_x_locations
where location_id = %(location_id)s and group_name in %(group_names)s
;

-- name: $create_location_assign_type!
-- Creates a location assignment type.
insert into ung.ac_location_assign_types (assign_type, assign_desc)
values (%(assign_type)s, %(assign_desc)s)
;

-- name: $retrieve_location_assign_types
-- Retrieve
select * from ung.ac_location_assign_types;
;

-- name: $update_location_assign_type!
-- Update
update ung.ac_location_assign_types
set assign_type=%(new_assign_type)s, assign_desc=%(assign_desc)s
where assign_type = %(assign_type)s
;

-- name: $delete_location_assign_types_by_assign_types!
-- Delete
delete from ung.ac_location_assign_types
where assign_type in %(assign_types)s
;


-- name: $create_contact<!
-- Creates a new contact entry
insert into ung.ac_contacts (contact_name)
values (%(contact_name)s)
returning contact_id
;

-- name: $retrieve_contacts_by_ids
-- Retrieves a list of contacts matching the given contact_id's
select *
from ung.ac_contacts
where contact_id in %(contact_ids)s
;

-- name: $retrieve_person_contacts_by_name
-- Retrieves a list of contacts matching on the contact's name expression
select *
from ung.ac_contacts
where contact_name like %(contact_name)s
      and row (contact_name, contact_id) > %(page_pos)s
      and contact_id > 0
order by contact_name, contact_id
fetch first %(page_size)s rows only;
;

-- name: $update_contact!
-- Updates contact entry
update ung.ac_contacts
set contact_name=(%(contact_name)s)
where contact_id = %(contact_id)s
;

-- name: $delete_contacts_by_ids!
-- Deletes contact entry
delete from ung.ac_contacts
where contact_id in %(contact_ids)s
;

-- name: $create_contact_group<!
-- Creates a new contact_group
insert into ung.ac_contact_groups (group_name)
values (%(group_name)s)
returning group_name
;

-- name: $update_contact_group!
-- Updates
update ung.ac_contact_groups
set group_name=(%(new_group_name)s)
where group_name=%(group_name)s
returning group_name
;

-- name: $retrieve_contact_groups
-- Retrieves
select * from ung.ac_contact_groups
;

-- name: $delete_contact_groups_by_group_names!
-- Deletes
delete from ung.ac_contact_groups
where group_name in %(group_names)s
;

-- name: $create_contact_group_membership!
-- Creates
insert into ung.ac_contact_groups_x_contacts (group_name, contact_id)
values (%(group_name)s, %(contact_id)s)
;

-- name: $retrieve_contact_group_memberships
-- Retrieves
select contact_id from ung.ac_contact_groups_x_contacts
where group_name = %(group_name)s
;

-- name: $retrieve_contact_groups_by_member_id
-- Retrieves
select group_name from ung.ac_contact_groups_x_contacts
where contact_id = %(contact_id)s
;

-- name: $delete_contact_group_memberships_by_member_ids!
-- Deletes
delete from ung.ac_contact_groups_x_contacts
where group_name = %(group_name)s and contact_id in %(contact_ids)s
;

-- name: $delete_contact_group_memberships_by_group_names!
-- Deletes
delete from ung.ac_contact_groups_x_contacts
where contact_id = %(contact_id)s and group_name in %(group_names)s
;

-- name: $create_contact_location_assignment!
-- Associates a contact to a location.
insert into ung.ac_contacts_x_locations (location_id, contact_id, assign_type)
values (%(location_id)s, %(contact_id)s, %(assign_type)s)
;

-- name: $retrieve_contact_location_assignments_by_location_id
-- Retrieve
select contact_id, assign_type from ung.ac_contacts_x_locations
where location_id = %(location_id)s
order by assign_type
;

-- name: $retrieve_contact_location_assignments_by_contact_id
-- Retrieve
select location_id, assign_type from ung.ac_contacts_x_locations
where contact_id = %(contact_id)s
order by assign_type
;

-- name: $delete_contact_location_assignments_by_ids!
-- Delete
delete from ung.ac_contacts_x_locations
where (location_id, contact_id, assign_type) in %(pks)s
;

-- name: $create_vehicle<!
-- Creates a new vehicle entry
insert into ung.ac_vehicles (plate)
values (%(plate)s)
returning vehicle_id
;

-- name: $retrieve_vehicles_by_ids
-- Retrieves a list of vehicles matching the given vehicle_id's
select *
from ung.ac_vehicles
where vehicle_id in %(vehicle_ids)s
;

-- name: $update_vehicle!
-- Updates vehicle entry
update ung.ac_vehicles
set plate=(%(plate)s)
where vehicle_id = %(vehicle_id)s
;

-- name: $delete_vehicles_by_ids!
-- Deletes vehicle entry
delete from ung.ac_vehicles
where vehicle_id in %(vehicle_ids)s
;

-- name: $create_vehicle_group<!
-- Creates a new vehicle_group
insert into ung.ac_vehicle_groups (group_name)
values (%(group_name)s)
returning group_name
;

-- name: $update_vehicle_group!
-- Updates
update ung.ac_vehicle_groups
set group_name=(%(new_group_name)s)
where group_name=%(group_name)s
returning group_name
;

-- name: $retrieve_vehicle_groups
-- Retrieves
select * from ung.ac_vehicle_groups
;

-- name: $delete_vehicle_groups_by_group_names!
-- Deletes
delete from ung.ac_vehicle_groups
where group_name in %(group_names)s
;

-- name: $create_vehicle_group_membership!
-- Creates
insert into ung.ac_vehicle_groups_x_vehicles (group_name, vehicle_id)
values (%(group_name)s, %(vehicle_id)s)
;

-- name: $retrieve_vehicle_group_memberships
-- Retrieves
select vehicle_id from ung.ac_vehicle_groups_x_vehicles
where group_name = %(group_name)s
;

-- name: $retrieve_vehicle_groups_by_member_id
-- Retrieves
select group_name from ung.ac_vehicle_groups_x_vehicles
where vehicle_id = %(vehicle_id)s
;

-- name: $delete_vehicle_group_memberships_by_member_ids!
-- Deletes
delete from ung.ac_vehicle_groups_x_vehicles
where group_name = %(group_name)s and vehicle_id in %(vehicle_ids)s
;

-- name: $delete_vehicle_group_memberships_by_group_names!
-- Deletes
delete from ung.ac_vehicle_groups_x_vehicles
where vehicle_id = %(vehicle_id)s and group_name in %(group_names)s
;

-- name: $create_checkpoint<!
-- Creates a new checkpoint entry
insert into ung.ac_checkpoints (checkpoint_name)
values (%(checkpoint_name)s)
returning checkpoint_id
;

-- name: $retrieve_checkpoints_by_ids
-- Retrieves a list of checkpoints matching the given checkpoint_id's
select *
from ung.ac_checkpoints
where checkpoint_id in %(checkpoint_ids)s
;

-- name: $update_checkpoint!
-- Updates checkpoint entry
update ung.ac_checkpoints
set checkpoint_name=(%(checkpoint_name)s)
where checkpoint_id = %(checkpoint_id)s
;

-- name: $delete_checkpoints_by_ids!
-- Deletes checkpoint entry
delete from ung.ac_checkpoints
where checkpoint_id in %(checkpoint_ids)s
;


-- name: $create_checkpoint_group<!
-- Creates a new checkpoint_group
insert into ung.ac_checkpoint_groups (group_name)
values (%(group_name)s)
returning group_name
;

-- name: $update_checkpoint_group!
-- Updates
update ung.ac_checkpoint_groups
set group_name=(%(new_group_name)s)
where group_name=%(group_name)s
returning group_name
;

-- name: $retrieve_checkpoint_groups
-- Retrieves
select * from ung.ac_checkpoint_groups
;

-- name: $delete_checkpoint_groups_by_group_names!
-- Deletes
delete from ung.ac_checkpoint_groups
where group_name in %(group_names)s
;

-- name: $create_checkpoint_group_membership!
-- Creates
insert into ung.ac_checkpoint_groups_x_checkpoints (group_name, checkpoint_id)
values (%(group_name)s, %(checkpoint_id)s)
;

-- name: $retrieve_checkpoint_group_memberships
-- Retrieves
select checkpoint_id from ung.ac_checkpoint_groups_x_checkpoints
where group_name = %(group_name)s
;

-- name: $retrieve_checkpoint_groups_by_member_id
-- Retrieves
select group_name from ung.ac_checkpoint_groups_x_checkpoints
where checkpoint_id = %(checkpoint_id)s
;

-- name: $delete_checkpoint_group_memberships_by_member_ids!
-- Deletes
delete from ung.ac_checkpoint_groups_x_checkpoints
where group_name = %(group_name)s and checkpoint_id in %(checkpoint_ids)s
;

-- name: $delete_checkpoint_group_memberships_by_group_names!
-- Deletes
delete from ung.ac_checkpoint_groups_x_checkpoints
where checkpoint_id = %(checkpoint_id)s and group_name in %(group_names)s
;


-- name: $create_auth_level<!
-- Creates a new authorization level
insert into ung.ac_auth_levels (auth_name, auth_grant)
values (%(auth_name)s, %(auth_grant)s)
returning auth_name
;

-- name: $retrieve_auth_levels_by_ids
-- Retrieves a list of auth_levels matching the given auth_name's
select *
from ung.ac_auth_levels
where auth_name in %(auth_names)s
;

-- name: $update_auth_level!
-- Updates auth_level entry
update ung.ac_auth_levels
set auth_name=(%(auth_name)s),
    auth_grant=(%(auth_grant)s)
where auth_name = %(pk)s
;

-- name: $delete_auth_levels_by_ids!
-- Deletes auth_level entry
delete from ung.ac_auth_levels
where auth_name in %(auth_names)s
;

-- name: $create_auth_flow<!
-- Creates a new authorization flow
insert into ung.ac_auth_flows (auth_flow_desc)
values (%(auth_flow_desc)s)
returning auth_flow_id
;

-- name: $retrieve_auth_flows_by_ids
-- Retrieves a list of auth_flows matching the given auth_flow_id's
select *
from ung.ac_auth_flows
where auth_flow_id in %(auth_flow_ids)s
;

-- name: $update_auth_flow!
-- Updates auth_flow entry
update ung.ac_auth_flows
set auth_flow_desc=(%(auth_flow_desc)s)
where auth_flow_id = %(auth_flow_id)s
;

-- name: $delete_auth_flows_by_ids!
-- Deletes auth_flow entry
delete from ung.ac_auth_flows
where auth_flow_id in %(auth_flow_ids)s
;

-- name: $create_auth_flow_st<!
-- Creates a new authorization flow state
insert into ung.ac_auth_flow_sts (auth_flow_id, st_name, st_term)
values (%(auth_flow_id)s, %(st_name)s, %(st_term)s)
returning (auth_flow_id, st_name)
;

-- name: $retrieve_auth_flow_sts_by_ids
-- Retrieves a list of auth_flow_sts matching the given auth_flow_id's
select *
from ung.ac_auth_flow_sts
where (auth_flow_id, st_name) in %(pks)s
;

-- name: $retrieve_auth_flow_sts_by_auth_flow_id
-- Retrieves a list of auth_flow_sts matching the given auth_flow_id's
select *
from ung.ac_auth_flow_sts
where auth_flow_id = %(auth_flow_id)s
order by st_name
;

-- name: $update_auth_flow_st!
-- Updates auth_flow_st entry
update ung.ac_auth_flow_sts
set st_term=(%(st_term)s)
where (auth_flow_id, st_name) = %(pk)s
;

-- name: $delete_auth_flow_sts_by_ids!
-- Deletes auth_flow_st entry
delete from ung.ac_auth_flow_sts
where (auth_flow_id, st_name) in %(pks)s
;

-- name: $create_auth_flow_tr<!
-- Creates a new authorization flow state
insert into ung.ac_auth_flow_trs (auth_flow_id, when_ev, curr_st, next_st)
values (%(auth_flow_id)s, %(when_ev)s, %(curr_st)s, %(next_st)s)
returning (auth_flow_id, when_ev, curr_st, next_st)
;

-- name: $retrieve_auth_flow_trs_by_ids
-- Retrieves a list of auth_flow_trs matching the given primary keys
select *
from ung.ac_auth_flow_trs
where (auth_flow_id, when_ev, curr_st, next_st) in %(pks)s
;

-- name: $retrieve_auth_flow_trs_by_auth_flow_id
-- Retrieves a list of auth_flow_trs matching the given auth_flow_id
select *
from ung.ac_auth_flow_trs
where auth_flow_id = %(auth_flow_id)s
order by curr_st, when_ev, next_st
;

-- name: $update_auth_flow_tr!
-- Updates auth_flow_tr entry
update ung.ac_auth_flow_trs
set when_ev=%(when_ev)s,
    curr_st=%(curr_st)s,
    next_st=%(next_st)s
where (auth_flow_id, when_ev, curr_st, next_st) = %(pk)s
;

-- name: $delete_auth_flow_trs_by_ids!
-- Deletes auth_flow_tr entry
delete from ung.ac_auth_flow_trs
where (auth_flow_id, when_ev, curr_st, next_st) in %(pks)s
;

-- name: $retrieve_auth_flow_setting_active_flow
-- Sets auth flow setting: active_flow
select active_flow from ung.ac_settings
;

-- name: $update_auth_flow_setting_active_flow!
-- Sets auth flow setting: active_flow
update ung.ac_settings
set active_flow = %(auth_flow_id)s
;

-- name: $create_auth_rule<!
-- Creates a new authorization automatic effect rule
insert into ung.ac_auth_rules (
    rule_ord,
    effect,
    ctc,
    loc_orig,
    loc_dest,
    ckp,
    vhc,
    ctc_grp,
    vhc_grp,
    loc_grp,
    ckp_grp,
    loc_ass,
    year0,
    year1,
    month0,
    month1,
    mday0,
    mday1,
    wday0,
    wday1,
    hour0,
    hour1,
    minute0,
    minute1)
values (
    %(rule_ord)s,
    %(effect)s,
    %(ctc)s,
    %(loc_orig)s,
    %(loc_dest)s,
    %(ckp)s,
    %(vhc)s,
    %(ctc_grp)s,
    %(vhc_grp)s,
    %(loc_grp)s,
    %(ckp_grp)s,
    %(loc_ass)s,
    %(year0)s,
    %(year1)s,
    %(month0)s,
    %(month1)s,
    %(mday0)s,
    %(mday1)s,
    %(wday0)s,
    %(wday1)s,
    %(hour0)s,
    %(hour1)s,
    %(minute0)s,
    %(minute1)s)
returning rule_id
;

-- name: $retrieve_auth_rules_by_ids
-- Retrieves a list of auth_rules matching the given primary keys
select *
from ung.ac_auth_rules
where rule_id in %(pks)s
order by rule_id, rule_ord
;

-- name: $update_auth_rule!
-- Creates a new authorization automatic effect rule
update ung.ac_auth_rules
set rule_ord=%(rule_ord)s,
    effect=%(effect)s,
    ctc=%(ctc)s,
    loc_orig=%(loc_orig)s,
    loc_dest=%(loc_dest)s,
    ckp=%(ckp)s,
    vhc=%(vhc)s,
    ctc_grp=%(ctc_grp)s,
    vhc_grp=%(vhc_grp)s,
    loc_grp=%(loc_grp)s,
    ckp_grp=%(ckp_grp)s,
    loc_ass=%(loc_ass)s,
    year0=%(year0)s,
    year1=%(year1)s,
    month0=%(month0)s,
    month1=%(month1)s,
    mday0=%(mday0)s,
    mday1=%(mday1)s,
    wday0=%(wday0)s,
    wday1=%(wday1)s,
    hour0=%(hour0)s,
    hour1=%(hour1)s,
    minute0=%(minute0)s,
    minute1=%(minute1)s
where rule_id=%(rule_id)s
;

-- name: $delete_auth_rules_by_ids!
-- Deletes auth_rules entries
delete from ung.ac_auth_rules
where rule_id in %(pks)s
;

-- name: create_process<!
-- Creates a blank new process
insert into ung.ac_processes (started_at)
values (coalesce(%(started_at)s, statement_timestamp()))
returning proc_id
;

-- name: $retrieve_processes_by_ids
-- Retrieves a list of processes matching the given process_id's
select *
from ung.ac_processes
where proc_id in %(proc_ids)s
;

-- name: update_process!
-- Sets a process details
update ung.ac_processes
set  ctc = %(ctc)s, loc_orig = %(loc_orig)s, loc_dest = %(loc_dest)s, ckp = %(ckp)s, vhc = %(vhc)s
where proc_id = %(proc_id)s
;

-- name: update_process_auth_flow!
-- Sets a process details
update ung.ac_processes
set  auth_flow = %(auth_flow)s
where proc_id = %(proc_id)s
;

-- name: update_process_terminate<!
-- Sets a process finish date
update ung.ac_processes
set finished_at = coalesce(%(finished_at)s, statement_timestamp())
where proc_id = %(proc_id)s
returning finished_at
;

-- name: $delete_processes_by_ids!
-- Deletes processes entries matching the given process_id's
delete from ung.ac_processes
where proc_id in %(proc_ids)s
;

-- name: create_process_auth_event<!
-- Creates a new auth event in the process event stream
insert into ung.ac_process_auth_events (proc_id, auth_by, auth_name, auth_at)
values (%(proc_id)s,%(auth_by)s,%(auth_name)s,coalesce(%(auth_at)s, statement_timestamp()))
returning auth_at
;

-- name: $archive_finished_processes
-- Turns finished processes into archive entries
select * from ung.ac_archive_finished_processes()
;


-- name: $retrieve_process_histories_by_ids
-- Retrieves resolved process snapshots
select
    proc_id,
    ctc.contact_id as subject_id,
    ctc.contact_name as subject_name,
    vhc.vehicle_id as vehicle_id,
    vhc.plate as vehicle_plate,
    loc_orig.location_id as location_orig_id,
    loc_orig.addr_1 as location_orig_addr_1,
    loc_orig.addr_2 as location_orig_addr_2,
    loc_orig.addr_3 as location_orig_addr_3,
    loc_orig.addr_4 as location_orig_addr_4,
    loc_orig.addr_5 as location_orig_addr_5,
    loc_orig.addr_6 as location_orig_addr_6,
    loc_dest.location_id as location_dest_id,
    loc_dest.addr_1 as location_dest_addr_1,
    loc_dest.addr_2 as location_dest_addr_2,
    loc_dest.addr_3 as location_dest_addr_3,
    loc_dest.addr_4 as location_dest_addr_4,
    loc_dest.addr_5 as location_dest_addr_5,
    loc_dest.addr_6 as location_dest_addr_6,
    auth_by.contact_id as authorizer_id,
    auth_by.contact_name as authorizer_name,
    started_at,
    finished_at,
    auth_at as auth_event_at,
    ev_seq as auth_event_seq,
    curr_st as curr_auth_flow_st
from ung.ac_process_histories proc
    left join ung.ac_contacts ctc on ctc.contact_id = proc.ctc
    left join ung.ac_vehicles vhc on vhc.vehicle_id = proc.vhc
    left join ung.ac_locations loc_orig on loc_orig.location_id = proc.loc_orig
    left join ung.ac_locations loc_dest on loc_dest.location_id = proc.loc_dest
    left join ung.ac_contacts auth_by on auth_by.contact_id = proc.auth_by
where proc_id in %(proc_ids)s
;


-- name: $retrieve_process_snapshots_running_by_ids
-- Retrieves resolved process snapshots
select
    proc_id,
    ctc.contact_id as subject_id,
    ctc.contact_name as subject_name,
    vhc.vehicle_id as vehicle_id,
    vhc.plate as vehicle_plate,
    loc_orig.location_id as location_orig_id,
    loc_orig.addr_1 as location_orig_addr_1,
    loc_orig.addr_2 as location_orig_addr_2,
    loc_orig.addr_3 as location_orig_addr_3,
    loc_orig.addr_4 as location_orig_addr_4,
    loc_orig.addr_5 as location_orig_addr_5,
    loc_orig.addr_6 as location_orig_addr_6,
    loc_dest.location_id as location_dest_id,
    loc_dest.addr_1 as location_dest_addr_1,
    loc_dest.addr_2 as location_dest_addr_2,
    loc_dest.addr_3 as location_dest_addr_3,
    loc_dest.addr_4 as location_dest_addr_4,
    loc_dest.addr_5 as location_dest_addr_5,
    loc_dest.addr_6 as location_dest_addr_6,
    auth_by.contact_id as authorizer_id,
    auth_by.contact_name as authorizer_name,
    started_at,
    finished_at
from ung.ac_process_snapshots_running proc
    left join ung.ac_contacts ctc on ctc.contact_id = proc.ctc
    left join ung.ac_vehicles vhc on vhc.vehicle_id = proc.vhc
    left join ung.ac_locations loc_orig on loc_orig.location_id = proc.loc_orig
    left join ung.ac_locations loc_dest on loc_dest.location_id = proc.loc_dest
    left join ung.ac_contacts auth_by on auth_by.contact_id = proc.auth_by
where proc_id in %(proc_ids)s
;

-- name: $retrieve_processes_rule_matches
-- Retrieves processes matched to respective access rules
select * from ung.ac_processes_rule_matches
;


-- name: $retrieve_processes_rule_selections
-- Retrieves processes matched to respective access rules
select * from ung.ac_processes_rule_selections
;
