

/* ------------------------------------------------------------------------------------------------
 Locations
------------------------------------------------------------------------------------------------ */

create table ung.ac_locations (
    location_id serial primary key,
    addr_1 varchar(50) not null,
    addr_2 varchar(50),
    addr_3 varchar(50),
    addr_4 varchar(50),
    addr_5 varchar(50),
    addr_6 varchar(50)
    check(location_id = 0 or (location_id != 0 and addr_1 != 'EXTERIOR'))
);

create table ung.ac_location_groups (
    group_name ung.group_name primary key
);

create table ung.ac_location_groups_x_locations (
    group_name ung.group_name not null references ung.ac_location_groups(group_name) on delete restrict,
    location_id integer not null references ung.ac_locations(location_id) on delete cascade,
    primary key (group_name, location_id)
);

create table ung.ac_location_assign_types (
    assign_type ung.assign_type primary key,
    assign_desc varchar(120)
);

/* ------------------------------------------------------------------------------------------------
 Contacts
------------------------------------------------------------------------------------------------ */

create table ung.ac_contacts (
    contact_id serial primary key,
    contact_name varchar(120) not null,
    created_at timestamptz not null default now()
    check(contact_id = 0 or (contact_id != 0 and contact_name != 'SYSTEM'))
);

create table ung.ac_contact_groups (
    group_name ung.group_name primary key
);

create table ung.ac_contact_groups_x_contacts (
    group_name ung.group_name not null references ung.ac_contact_groups(group_name) on delete restrict,
    contact_id integer not null references ung.ac_contacts(contact_id) on delete cascade,
    primary key (group_name, contact_id)
);

create table ung.ac_contacts_x_locations (
    location_id integer not null references ung.ac_locations(location_id) on delete cascade,
    contact_id integer not null references ung.ac_contacts(contact_id) on delete restrict,
    assign_type ung.assign_type not null references ung.ac_location_assign_types on delete restrict,
    primary key (location_id, contact_id, assign_type)
);

/* ------------------------------------------------------------------------------------------------
 Vehicles
------------------------------------------------------------------------------------------------ */

create table ung.ac_vehicles (
    vehicle_id serial primary key,
    plate varchar(7) not null unique
);

create table ung.ac_vehicle_groups (
    group_name ung.group_name primary key
);

create table ung.ac_vehicle_groups_x_vehicles (
    group_name ung.group_name not null references ung.ac_vehicle_groups(group_name) on delete restrict,
    vehicle_id integer not null references ung.ac_vehicles(vehicle_id) on delete cascade,
    primary key (group_name, vehicle_id)
);

/* ------------------------------------------------------------------------------------------------
 Checkpoints
------------------------------------------------------------------------------------------------ */

create table ung.ac_checkpoints (
    checkpoint_id serial primary key,
    checkpoint_name varchar(50) not null
);

create table ung.ac_checkpoint_groups (
    group_name ung.group_name primary key
);

create table ung.ac_checkpoint_groups_x_checkpoints (
    group_name ung.group_name not null references ung.ac_checkpoint_groups(group_name) on delete restrict,
    checkpoint_id integer not null references ung.ac_checkpoints(checkpoint_id) on delete cascade,
    primary key (group_name, checkpoint_id)
);

/* ------------------------------------------------------------------------------------------------
 Access Authorization Flows
------------------------------------------------------------------------------------------------ */

create table ung.ac_auth_levels (
    auth_name ung.auth_name primary key,
    auth_grant boolean not null default false
);

create table ung.ac_auth_flows (
    auth_flow_id serial primary key,
    auth_flow_desc varchar(100),
    created_at timestamptz not null default now()
);

create table ung.ac_auth_flow_sts (
    auth_flow_id integer references ung.ac_auth_flows (auth_flow_id) on delete cascade on update cascade deferrable,
    st_name ung.auth_name not null references ung.ac_auth_levels (auth_name) on delete restrict on update cascade,
    st_term boolean not null default false,
    primary key (auth_flow_id, st_name)
);

alter table ung.ac_auth_flows
    add column init_st ung.auth_name not null,
    add foreign key (auth_flow_id, init_st) references ung.ac_auth_flow_sts (auth_flow_id, st_name) deferrable
;


create table ung.ac_auth_flow_trs (
    auth_flow_id integer references ung.ac_auth_flows (auth_flow_id) on delete cascade on update cascade,
    when_ev ung.auth_name not null references ung.ac_auth_levels (auth_name) on delete restrict,
    curr_st ung.auth_name not null,
    next_st ung.auth_name not null,
    foreign key (auth_flow_id, curr_st) references ung.ac_auth_flow_sts (auth_flow_id, st_name) on delete restrict on update cascade,
    foreign key (auth_flow_id, next_st) references ung.ac_auth_flow_sts (auth_flow_id, st_name) on delete restrict on update cascade,
    primary key (auth_flow_id, curr_st, when_ev, next_st)
);

create table ung.ac_auth_rules (
    rule_id serial primary key,
    rule_ord integer not null default 0 unique deferrable initially immediate,
    effect ung.auth_name not null references ung.ac_auth_levels (auth_name) on update cascade,
    ctc integer references ung.ac_contacts (contact_id),
    loc_orig integer references ung.ac_locations (location_id),
    loc_dest integer references ung.ac_locations (location_id),
    ckp integer references ung.ac_checkpoints (checkpoint_id),
    vhc integer references ung.ac_vehicles (vehicle_id),
    ctc_grp ung.group_name references ung.ac_contact_groups (group_name),
    vhc_grp ung.group_name references ung.ac_vehicle_groups (group_name),
    loc_grp ung.group_name references ung.ac_location_groups (group_name),
    ckp_grp ung.group_name references ung.ac_checkpoint_groups (group_name),
    loc_ass ung.assign_type references ung.ac_location_assign_types (assign_type),
    year0 smallint not null default 1970 check (year0 >= 1970 and year0 <= 3000),
    year1 smallint not null default 3000 check (year1 >= 1970 and year1 <= 3000),
    month0 smallint not null default 1 check (month0 >= 1 and month0 <= 12),
    month1 smallint not null default 12 check (month1 >= 1 and month1 <= 12),
    mday0 smallint not null default 1 check (mday0 >= 1 and mday0 <= 31),
    mday1 smallint not null default 31 check (mday1 >= 1 and mday1 <= 31),
    wday0 smallint not null default 0 check (wday0 >= 0 and wday0 <= 6),
    wday1 smallint not null default 6 check (wday1 >= 0 and wday1 <= 6),
    hour0 smallint not null default 0 check (hour0 >= 0 and hour0 <= 23),
    hour1 smallint not null default 23 check (hour1 >= 0 and hour1 <= 23),
    minute0 smallint not null default 0 check (minute0 >= 0 and minute0 <= 59),
    minute1 smallint not null default 59 check (minute1 >= 0 and minute1 <= 59),
    check (rule_ord > 0),
    check (year0 <= year1),
    check (month0 <= month1),
    check (mday0 <= mday1),
    check (wday0 <= wday1),
    check (timestamp '1970-01-01' + interval '1 hour' * hour0 + interval '1 minute' * minute0 <=
           timestamp '1970-01-01' + interval '1 hour' * hour1 + interval '1 minute' * minute1)
);

/* ------------------------------------------------------------------------------------------------
 Access Processes
------------------------------------------------------------------------------------------------ */

create table ung.ac_processes (
    proc_id bigserial primary key,
    ctc integer references ung.ac_contacts(contact_id) on delete cascade,
    loc_orig integer references ung.ac_locations(location_id) on delete cascade,
    loc_dest integer references ung.ac_locations(location_id) on delete cascade,
    ckp integer references ung.ac_checkpoints(checkpoint_id) on delete cascade,
    vhc integer references ung.ac_vehicles(vehicle_id) on delete restrict,
    auth_flow integer not null references ung.ac_auth_flows (auth_flow_id) on delete cascade on update cascade,
    started_at timestamptz not null default now(),
    finished_at timestamptz,
    constraint movement check (loc_orig != loc_dest),
    constraint elapsed_time check (started_at < finished_at),
    constraint ac_filled check (
        finished_at is null or
           (ctc is not null
            and loc_orig is not null
            and loc_dest is not null
            and ckp is not null))
);

create table ung.ac_process_auth_events (
    proc_id bigint not null references ung.ac_processes (proc_id) on delete cascade,
    auth_by integer not null references ung.ac_contacts (contact_id) on delete restrict,
    auth_name ung.auth_name not null references ung.ac_auth_levels (auth_name) on delete restrict,
    auth_at timestamptz not null default now(),
    primary key (proc_id, auth_at)
);

/* ------------------------------------------------------------------------------------------------
 Access History
------------------------------------------------------------------------------------------------ */

create table ung.ac_history (
    proc_id bigserial primary key,
    ctc integer not null references ung.ac_contacts(contact_id) on delete cascade,
    loc_orig integer not null references ung.ac_locations(location_id) on delete cascade,
    loc_dest integer not null references ung.ac_locations(location_id) on delete cascade,
    ckp integer not null references ung.ac_checkpoints(checkpoint_id) on delete cascade,
    vhc integer null references ung.ac_vehicles(vehicle_id) on delete restrict,
    auth_name ung.auth_name not null references ung.ac_auth_levels (auth_name) on delete restrict,
    auth_by integer not null references ung.ac_contacts (contact_id) on delete restrict,
    auth_at timestamptz not null default now(),
    started_at timestamptz not null,
    finished_at timestamptz not null,
    check (loc_orig != loc_dest),
    check (started_at < finished_at)
);

/* ------------------------------------------------------------------------------------------------
 Settings
------------------------------------------------------------------------------------------------ */

create table ung.ac_settings (
    lock boolean primary key default true check (lock = true),

    /* -------------------------------------------------------------------------------
     * Determines which auth flow new access processes should use.
     * ------------------------------------------------------------------------------- */
    active_flow integer not null
        references ung.ac_auth_flows (auth_flow_id)
        on delete restrict
        on update cascade,

    /* -------------------------------------------------------------------------------
     * Determines the maximum number of acess processes at any point in time.
     * Once the threshold is reached, processes are deleted starting from the oldest.
     * ------------------------------------------------------------------------------- */
    proc_max_cnt integer not null check(proc_max_cnt > 0) default 10,

    /* -------------------------------------------------------------------------------
     * Determines the maximum number of seconds an access process can exist before it
     * is dropped. Processes time-to-live are evaluated when new processes are created.
     * ------------------------------------------------------------------------------- */
    proc_ttl_sec integer not null check(proc_ttl_sec > 0) default 60 * 5
);
