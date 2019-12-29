
/**
 * Creates a new authorization level
 *
 * @dialect postgresql
 * @name create_auth_level
 * @param auth_name: str
 * @param auth_grant: str
 * @retmode scalar
 * @retval auth_name: string
 */
{
    insert into ung.ac_auth_levels (auth_name, auth_grant)
    values (%(auth_name)s, %(auth_grant)s)
    returning auth_name
    ;
}

/**
 * Retrieves a list of auth_levels matching the given auth_name's
 *
 * @dialect postgresql
 * @name retrieve_auth_levels_by_auth_name
 * @param auth_names: list
 * @retmode records
 * @retval auth_name: string
 * @retval auth_grant: string
 */
{
    select *
    from ung.ac_auth_levels
    where auth_name in %(auth_names)s
    ;
}

/**
 * Updates an auth_level entry
 *
 * @dialect postgresql
 * @name update_auth_level
 * @param auth_name: string
 * @param new_auth_name: string
 * @param auth_grant: string
 * @retmode none
 */
{
    update ung.ac_auth_levels
    set auth_name=(%(new_auth_name)s), auth_grant=(%(auth_grant)s)
    where auth_name = %(auth_name)s
    ;
}

/**
 * Deletes the auth_level entry
 *
 * @dialect postgresql
 * @name delete_auth_levels_by_auth_names
 * @param auth_names: list
 * @retmode none
 */
{
    delete from ung.ac_auth_levels
    where auth_name in %(auth_names)s
    ;
}

/**
 * Creates a new authorization flow
 *
 * @dialect postgresql
 * @name create_auth_flow
 * @param auth_flow_desc: str
 * @retmode scalar
 * @retval auth_flow_id: number
 */
{
    insert into ung.ac_auth_flows (auth_flow_desc)
    values (%(auth_flow_desc)s)
    returning auth_flow_id
    ;
}

/**
 * Retrieves a list of auth_flows matching the given auth_flow_id's
 *
 * @dialect postgresql
 * @name retrieve_auth_flows_by_ids
 * @param auth_flow_ids: list
 * @retmode records
 * @retval auth_flow_id: number
 * @retval auth_flow_desc: string
 * @retval init_st: string
 * @retval created_at: string
 */
{
    select *
    from ung.ac_auth_flows
    where auth_flow_id in %(auth_flow_ids)s
    ;
}

/**
 * Updates auth_flow entry
 *
 * @dialect postgresql
 * @name update_auth_flow
 * @param auth_flow_id: number
 * @param auth_flow_desc: string
 * @retmode none
 */
{
    update ung.ac_auth_flows
    set auth_flow_desc=(%(auth_flow_desc)s)
    where auth_flow_id = %(auth_flow_id)s
    ;
}

/**
 * Deletes auth_flow entry
 *
 * @dialect postgresql
 * @name delete_auth_flows_by_ids
 * @param auth_flow_ids: list
 * @retmode none
 */
{
    delete from ung.ac_auth_flows
    where auth_flow_id in %(auth_flow_ids)s
    ;
}

/**
 * Creates a new authorization flow state
 *
 * @dialect postgresql
 * @name create_auth_flow_st
 * @param auth_flow_id: number
 * @param st_name: string
 * @param st_term: bool
 * @retmode record
 * @retval auth_flow_id: number
 * @retval st_name: string
 */
{
    insert into ung.ac_auth_flow_sts (auth_flow_id, st_name, st_term)
    values (%(auth_flow_id)s, %(st_name)s, %(st_term)s)
    returning auth_flow_id, st_name
    ;
}

/**
 * Retrieves a list of auth_flow_sts matching the given auth_flow_id's
 *
 * @dialect postgresql
 * @name retrieve_auth_flow_sts_by_auth_flow_id
 * @param auth_flow_id: number
 * @retmode records
 * @retval st_name: string
 * @retval st_term: bool
 */
{
    select st_name, st_term
    from ung.ac_auth_flow_sts
    where auth_flow_id = %(auth_flow_id)s
    order by st_name
    ;
}

/**
 * Updates auth_flow_st entry
 *
 * @dialect postgresql
 * @name update_auth_flow_st
 * @param auth_flow_id: number
 * @param st_name: string
 * @param st_term: bool
 * @retmode none
 */
{
    update ung.ac_auth_flow_sts
    set st_term=(%(st_term)s)
    where auth_flow_id = %(auth_flow_id)s and st_name = %(st_name)s
    ;
}

/**
 * Deletes auth_flow_st entry
 *
 * @dialect postgresql
 * @name delete_auth_flow_st_by_id
 * @param auth_flow_id: number
 * @param st_name: string
 * @retmode none
 */
{
    delete from ung.ac_auth_flow_sts
    where auth_flow_id = %(auth_flow_id)s and st_name = %(st_name)s
    ;
}

/**
 * Creates a new authorization flow transition
 *
 * @dialect postgresql
 * @name create_auth_flow_tr
 * @param auth_flow_id: number
 * @param when_ev: string
 * @param curr_st: string
 * @param next_st: string
 * @retmode record
 * @retval auth_flow_id: number
 * @retval when_ev: string
 * @retval curr_st: string
 * @retval next_st: string
 */
{
    insert into ung.ac_auth_flow_trs (auth_flow_id, when_ev, curr_st, next_st)
    values (%(auth_flow_id)s, %(when_ev)s, %(curr_st)s, %(next_st)s)
    returning auth_flow_id, when_ev, curr_st, next_st
    ;
}

/**
 * Retrieves a list of auth_flow_trs for the authorization flow
 *
 * @dialect postgresql
 * @name retrieve_auth_flow_trs_by_auth_flow_id
 * @param auth_flow_id: number
 * @retmode records
 * @retval auth_flow_id: number
 * @retval when_ev: string
 * @retval curr_st: string
 * @retval next_st: string
 */
{
    select auth_flow_id, when_ev, curr_st, next_st
    from ung.ac_auth_flow_trs
    where auth_flow_id = %(auth_flow_id)s
    order by when_ev, curr_st, next_st
    ;
}

/**
 * Updates auth_flow_tr entry
 *
 * @dialect postgresql
 * @name update_auth_flow_tr
 * @param auth_flow_id: number
 * @param when_ev: string
 * @param curr_st: string
 * @param next_st: string
 * @param new_when_ev: string
 * @param new_curr_st: string
 * @param new_next_st: string
 * @retmode none
 */
{
    update ung.ac_auth_flow_trs
    set when_ev=%(new_when_ev)s,
        curr_st=%(new_curr_st)s,
        next_st=%(new_next_st)s
    where auth_flow_id=%(auth_flow_id)s and curr_st=%(curr_st)s and next_st=%(next_st)s
    ;
}

/**
 * Deletes auth_flow_tr entry
 *
 * @dialect postgresql
 * @name delete_auth_flow_tr_by_id
 * @param auth_flow_id: number
 * @param when_ev: string
 * @param curr_st: string
 * @param next_st: string
 * @retmode none
 */
{
    delete from ung.ac_auth_flow_trs
    where auth_flow_id=%(auth_flow_id)s and curr_st=%(curr_st)s and next_st=%(next_st)s
    ;
}

/**
 * Retrieves the currently defined Active Authorization Flow
 *
 * @dialect postgresql
 * @name retrieve_current_active_auth_flow
 * @retmode record
 * @retval auth_flow_id: number
 * @retval auth_flow_desc: string
 */
{
    select flows.*
    from ung.ac_settings settings
    join ung.ac_auth_flows flows
      on settings.active_flow = flows.auth_flow_id
    ;
}

/**
 * Defines the current Active Authorization Flow
 *
 * @dialect postgresql
 * @name update_current_active_auth_flow
 * @param auth_flow_id: number
 * @retmode none
 */
{
    update ung.ac_settings
    set active_flow = %(auth_flow_id)s
    ;
}

/**
 * Creates a new authorization automatic effect rule
 *
 * @dialect postgresql
 * @name create_auth_rule
 * @param rule_ord: number
 * @param effect: string
 * @param ctc: number
 * @param loc_orig: number
 * @param loc_dest: number
 * @param ckp: number
 * @param vhc: number
 * @param ctc_grp: number
 * @param vhc_grp: number
 * @param loc_grp: number
 * @param ckp_grp: number
 * @param loc_ass: number
 * @param year0: number
 * @param year1: number
 * @param month0: number
 * @param month1: number
 * @param mday0: number
 * @param mday1: number
 * @param wday0: number
 * @param wday1: number
 * @param hour0: number
 * @param hour1: number
 * @param minute0: number
 * @param minute1: number
 * @retmode scalar
 * @retval rule_id: number
 */
{
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
}

/**
 * Retrieves a list of auth_rules matching the given rule ids
 *
 * @dialect postgresql
 * @name retrieve_auth_rules_by_ids
 * @param rule_ids: list
 * @retmode records
 * @retval rule_id: number
 * @retval rule_ord: number
 * @retval effect: string
 * @retval ctc: number
 * @retval loc_orig: number
 * @retval loc_dest: number
 * @retval ckp: number
 * @retval vhc: number
 * @retval ctc_grp: number
 * @retval vhc_grp: number
 * @retval loc_grp: number
 * @retval ckp_grp: number
 * @retval loc_ass: number
 * @retval year0: number
 * @retval year1: number
 * @retval month0: number
 * @retval month1: number
 * @retval mday0: number
 * @retval mday1: number
 * @retval wday0: number
 * @retval wday1: number
 * @retval hour0: number
 * @retval hour1: number
 * @retval minute0: number
 * @retval minute1: number
 */
{

    select
        rule_id,
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
        minute1
    from ung.ac_auth_rules
    where rule_id in %(rule_ids)s
    order by rule_id, rule_ord
    ;
}

/**
 * Updates an existing authorization automatic effect rule
 *
 * @dialect postgresql
 * @name update_auth_rule
 * @param rule_id: number
 * @param rule_ord: number
 * @param effect: string
 * @param ctc: number
 * @param loc_orig: number
 * @param loc_dest: number
 * @param ckp: number
 * @param vhc: number
 * @param ctc_grp: number
 * @param vhc_grp: number
 * @param loc_grp: number
 * @param ckp_grp: number
 * @param loc_ass: number
 * @param year0: number
 * @param year1: number
 * @param month0: number
 * @param month1: number
 * @param mday0: number
 * @param mday1: number
 * @param wday0: number
 * @param wday1: number
 * @param hour0: number
 * @param hour1: number
 * @param minute0: number
 * @param minute1: number
 * @retmode none
 */
{
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
}

/**
 * Deletes auth_rules entries
 *
 * @dialect postgresql
 * @name delete_auth_rules_by_ids
 * @param rule_ids: list
 * @retmode none
 */
{
    delete from ung.ac_auth_rules
    where rule_id in %(rule_ids)s
    ;
}
