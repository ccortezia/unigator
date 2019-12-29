
/**
 * Creates a blank new process
 *
 * @dialect postgresql
 * @name create_process
 * @param started_at: datetime
 * @retmode scalar
 * @retval proc_id: number
 */
{
    insert into ung.ac_processes (started_at)
    values (coalesce(%(started_at)s, statement_timestamp()))
    returning proc_id
    ;
}

/**
 * Retrieves a list of processes matching the given process_id's
 *
 * @dialect postgresql
 * @name retrieve_processes_by_ids
 * @param proc_ids: list
 * @retmode records
 * @retval proc_id: number
 * @retval ctc: number
 * @retval loc_orig: number
 * @retval loc_dest: number
 * @retval ckp: number
 * @retval vhc: number
 * @retval auth_flow: number
 * @retval started_at: datetime
 * @retval finished_at: datetime
 */
{
    select *
    from ung.ac_processes
    where proc_id in %(proc_ids)s
    ;
}

/**
 * Sets a process details
 *
 * @dialect postgresql
 * @name update_process
 * @param proc_id: number
 * @param ctc: number
 * @param loc_orig: number
 * @param loc_dest: number
 * @param ckp: number
 * @param vhc: number
 * @retmode none
 */
{
    update ung.ac_processes
    set  ctc = %(ctc)s, loc_orig = %(loc_orig)s, loc_dest = %(loc_dest)s, ckp = %(ckp)s, vhc = %(vhc)s
    where proc_id = %(proc_id)s
    ;
}

/**
 * Sets a process active authorization flow
 *
 * @dialect postgresql
 * @name update_process_auth_flow
 * @param proc_id: number
 * @param auth_flow: number
 * @retmode none
 */
{
    update ung.ac_processes
    set  auth_flow = %(auth_flow)s
    where proc_id = %(proc_id)s
    ;
}

/**
 * Terminates an authorization process
 *
 * @dialect postgresql
 * @name terminate_process
 * @param proc_id: number
 * @param finished_at: number
 * @retmode scalar
 * @retval finished_at: datetime
 */
{
    update ung.ac_processes
    set finished_at = coalesce(%(finished_at)s, statement_timestamp())
    where proc_id = %(proc_id)s
    returning finished_at
    ;
}

/**
 * Deletes processes entries matching the given process_id's
 *
 * @dialect postgresql
 * @name delete_processes_by_ids
 * @param proc_ids: list
 * @retmode none
 */
{
    delete from ung.ac_processes
    where proc_id in %(proc_ids)s
    ;
}

/**
 * Creates a new auth event in the process event stream
 *
 * @dialect postgresql
 * @name create_process_auth_event
 * @param proc_id: number
 * @param auth_by: number
 * @param auth_name: string
 * @param auth_at: datetime
 * @retmode scalar
 * @retval auth_at: datetime
 */
{
    insert into ung.ac_process_auth_events (proc_id, auth_by, auth_name, auth_at)
    values (%(proc_id)s,%(auth_by)s,%(auth_name)s,coalesce(%(auth_at)s, statement_timestamp()))
    returning auth_at
    ;
}

/**
 * Turns finished processes into archive entries
 *
 * @dialect postgresql
 * @name archive_finished_processes
 * @retmode records
 * @retval archived_proc_id: number
 * @retval archived_finished_at: datetime
 */
{
    select archived_proc_id, archived_finished_at
    from ung.ac_archive_finished_processes()
    ;
}


/**
 * Retrieves the activity histories for all unarchived processes
 *
 * @dialect postgresql
 * @name retrieve_process_histories_by_ids
 * @param proc_ids: list
 * @retmode records
 * @retval proc_id: number
 * @retval subject_id: number
 * @retval subject_name: string
 * @retval vehicle_id: number
 * @retval vehicle_plate: string
 * @retval location_orig_id: number
 * @retval location_orig_addr1: string
 * @retval location_orig_addr2: string
 * @retval location_orig_addr3: string
 * @retval location_orig_addr4: string
 * @retval location_orig_addr5: string
 * @retval location_orig_addr6: string
 * @retval location_dest_id: number
 * @retval location_dest_addr1: string
 * @retval location_dest_addr2: string
 * @retval location_dest_addr3: string
 * @retval location_dest_addr4: string
 * @retval location_dest_addr5: string
 * @retval location_dest_addr6: string
 * @retval authorizer_id: number
 * @retval authorizer_name: string
 * @retval started_at: datetime
 * @retval finished_at: datetime
 * @retval auth_event_at: datetime
 * @retval auth_event_seq: number
 * @retval curr_auth_flow_st: string
 */
{
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
}

/**
 * Retrieves running process snapshots
 *
 * @dialect postgresql
 * @name retrieve_all_running_process_snapshots
 * @param proc_ids: list
 * @retmode records
 * @retval proc_id: number
 * @retval subject_id: number
 * @retval subject_name: string
 * @retval vehicle_id: number
 * @retval vehicle_plate: string
 * @retval location_orig_id: number
 * @retval location_orig_addr1: string
 * @retval location_orig_addr2: string
 * @retval location_orig_addr3: string
 * @retval location_orig_addr4: string
 * @retval location_orig_addr5: string
 * @retval location_orig_addr6: string
 * @retval location_dest_id: number
 * @retval location_dest_addr1: string
 * @retval location_dest_addr2: string
 * @retval location_dest_addr3: string
 * @retval location_dest_addr4: string
 * @retval location_dest_addr5: string
 * @retval location_dest_addr6: string
 * @retval authorizer_id: number
 * @retval authorizer_name: string
 * @retval started_at: datetime
 * @retval finished_at: datetime
 */
{

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
    ;
}

/**
 * Retrieves processes matched to respective access rules
 *
 * @dialect postgresql
 * @name retrieve_processes_rule_matches
 * @retmode records
 * @retval proc_id: number
 * @retval match_rule_id: number
 * @retval match_rule_ord: number
 * @retval resolved_auth_name: string
 * @retval resolved_auth_grant: string
 */
{
    select * from ung.ac_processes_rule_matches
    ;
}

/**
 * Retrieves processes matched to respective access rules
 *
 * @dialect postgresql
 * @name retrieve_processes_rule_selections
 * @retmode records
 * @retval proc_id: number
 * @retval match_rule_id: number
 * @retval resolved_auth_name: string
 * @retval resolved_auth_grant: string
 */
{
    select * from ung.ac_processes_rule_selections
    ;
}
