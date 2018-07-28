
/* ------------------------------------------------------------------------------------------------
 Access Flows
------------------------------------------------------------------------------------------------ */

--
-- This function cannot be declared as `strict`. This is a way to prevent postgresql from storing
-- the first input value for `inc` as the `acc` blindly. Instead, the initial value is retrieved
-- dynamically from ac_auth_flows.init_st.
create function ung.ac_auth_flow_fsm_reducer (acc ung.auth_name, inc ung.auth_name, _auth_flow_id integer)
    returns ung.auth_name
    immutable
    language plpgsql
as $$
begin
    return coalesce (
        (
            select next_st
            from ung.ac_auth_flow_trs tr
            join ung.ac_auth_flows flow using (auth_flow_id)
            where tr.auth_flow_id = _auth_flow_id
                and curr_st = coalesce (acc, flow.init_st)
                and when_ev = inc
        ),
        acc,
        (
            select init_st
            from ung.ac_auth_flows
            where auth_flow_id = _auth_flow_id
        )
    );
end;
$$;


-- This aggregate cannot have an explicit static initcond, since the initial state is gathered
-- from ac_auth_flows.init_st dynamically as the aggregation is run.
create aggregate ung.ac_auth_reduce (ung.auth_name, integer) (
    sfunc = ung.ac_auth_flow_fsm_reducer,
    stype = ung.auth_name
);

