/* ------------------------------------------------------------------------------------------------
 Locations
------------------------------------------------------------------------------------------------ */

--
create function ung.prevent_delete_exterior_location()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.location_id = 0) then
        raise 'The EXTERIOR location cannot be deleted.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_exterior_location
    before delete on ung.ac_locations
    for each row execute procedure
    ung.prevent_delete_exterior_location();

--
create function ung.prevent_update_exterior_location()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.location_id = 0) then
        raise 'The EXTERIOR location cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_exterior_location
    before update on ung.ac_locations
    for each row execute procedure
    ung.prevent_update_exterior_location();

--
create function ung.prevent_update_locations_pk()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.location_id != OLD.location_id) then
        raise 'The primary key cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_locations_pk
    before update on ung.ac_locations
    for each row execute procedure
    ung.prevent_update_locations_pk();

/* ------------------------------------------------------------------------------------------------
 Contacts
------------------------------------------------------------------------------------------------ */

--
create function ung.prevent_delete_system_contact()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.contact_id = 0) then
        raise 'The SYSTEM contact cannot be deleted.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_system_contact
    before delete on ung.ac_contacts
    for each row execute procedure
    ung.prevent_delete_system_contact();

--
create function ung.prevent_update_system_contact()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.contact_id = 0) then
        raise 'The SYSTEM contact cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_system_contact
    before update on ung.ac_contacts
    for each row execute procedure
    ung.prevent_update_system_contact();

--
create function ung.prevent_update_contacts_pk()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.contact_id != OLD.contact_id) then
        raise 'The primary key cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_contacts_pk
    before update on ung.ac_contacts
    for each row execute procedure
    ung.prevent_update_contacts_pk();

/* ------------------------------------------------------------------------------------------------
 Vehicles
------------------------------------------------------------------------------------------------ */

--
create function ung.prevent_update_vehicles_pk()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.vehicle_id != OLD.vehicle_id) then
        raise 'The primary key cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_vehicles_pk
    before update on ung.ac_vehicles
    for each row execute procedure
    ung.prevent_update_vehicles_pk();

/* ------------------------------------------------------------------------------------------------
 Checkpoints
------------------------------------------------------------------------------------------------ */

--
create function ung.prevent_update_checkpoints_pk()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.checkpoint_id != OLD.checkpoint_id) then
        raise 'The primary key cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_checkpoints_pk
    before update on ung.ac_checkpoints
    for each row execute procedure
    ung.prevent_update_checkpoints_pk();

/* ------------------------------------------------------------------------------------------------
 Access Authorization Flows
------------------------------------------------------------------------------------------------ */

--
create function ung.ensure_default_auth_flow_init_st()
    returns trigger
    language plpgsql
as $$
begin
    set constraints ac_auth_flows_auth_flow_id_fkey deferred;
    set constraints ac_auth_flow_sts_auth_flow_id_fkey deferred;
    insert into ung.ac_auth_flow_sts values (NEW.auth_flow_id, 'sys/none', false);
    NEW.init_st = 'sys/none';
    return NEW;
end;
$$;

create trigger ensure_default_auth_flow_init_st
    before insert on ung.ac_auth_flows
    for each row execute procedure
    ung.ensure_default_auth_flow_init_st();


--
create function ung.prevent_delete_base_auth_level()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.auth_name = 'sys/none') then
        raise 'The authorization level sys/none cannot be deleted.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_base_auth_level
    before delete on ung.ac_auth_levels
    for each row execute procedure
    ung.prevent_delete_base_auth_level();

--
create function ung.prevent_update_base_auth_level()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.auth_name = 'sys/none' or NEW.auth_name = 'sys/none') then
        raise 'The sys/none authorization level cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_base_auth_level
    before update on ung.ac_auth_levels
    for each row execute procedure
    ung.prevent_update_base_auth_level();

--
create function ung.prevent_update_base_auth_flow()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.auth_flow_id = 0 or NEW.auth_flow_id = 0) then
        raise 'The base authorization flow cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_base_auth_flow
    before update on ung.ac_auth_flows
    for each row execute procedure
    ung.prevent_update_base_auth_flow();

--
create function ung.prevent_delete_base_auth_flow()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.auth_flow_id = 0) then
        raise 'The base authorization flow cannot be deleted.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_base_auth_flow
    before delete on ung.ac_auth_flows
    for each row execute procedure
    ung.prevent_delete_base_auth_flow();

--
create function ung.prevent_update_auth_flow_pk()
    returns trigger
    language plpgsql
as $$
begin
    if (OLD.auth_flow_id = 0 and (OLD.auth_flow_id != NEW.auth_flow_id)) then
        raise 'The base authorization flow id cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_auth_flow_pk
    before update on ung.ac_auth_flows
    for each row execute procedure
    ung.prevent_update_auth_flow_pk();


--
create function ung.prevent_update_referenced_flow()
    returns trigger
    language plpgsql
as $$
begin
    if (select count(proc_id) from ung.ac_processes where auth_flow = NEW.auth_flow_id limit 1) > 0 then
        raise 'Invalid attempt to update auth flow referenced by one or more processes.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_referenced_flow
    before update on ung.ac_auth_flows
    for each row execute procedure
    ung.prevent_update_referenced_flow();


--
create function ung.prevent_delete_referenced_flow()
    returns trigger
    language plpgsql
as $$
begin
    if exists (select proc_id from ung.ac_processes where auth_flow = OLD.auth_flow_id limit 1) then
        raise 'Invalid attempt to delete auth flow referenced by one or more processes.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_referenced_flow
    before delete on ung.ac_auth_flows
    for each row execute procedure
    ung.prevent_delete_referenced_flow();


--
create function ung.prevent_delete_auth_flow_settings()
    returns trigger
    language plpgsql
as $$
begin
    raise 'Authorization flow settings cannot be deleted.';
end;
$$;

create trigger prevent_delete_auth_flow_settings
    before delete on ung.ac_settings
    for each row execute procedure
    ung.prevent_delete_auth_flow_settings();


--
create function ung.prevent_update_auth_flow_sts_parent_flow_ref()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.auth_flow_id != OLD.auth_flow_id) then
        raise 'The parent flow for an auth_flow_st cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_auth_flow_sts_parent_flow_ref
    before update on ung.ac_auth_flow_sts
    for each row execute procedure
    ung.prevent_update_auth_flow_sts_parent_flow_ref();

--
create function ung.prevent_update_auth_flow_trs_parent_flow_ref()
    returns trigger
    language plpgsql
as $$
begin
    if (NEW.auth_flow_id != OLD.auth_flow_id) then
        raise 'The parent flow for an auth_flow_tr cannot be updated.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_auth_flow_trs_parent_flow_ref
    before update on ung.ac_auth_flow_trs
    for each row execute procedure
    ung.prevent_update_auth_flow_trs_parent_flow_ref();

--
create function ung.prevent_create_rule_when_running_process()
    returns trigger
    language plpgsql
as $$
begin
    if exists (select proc_id from ung.ac_processes_running limit 1) then
        raise 'Impossible to create authorization rules while processes are running.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_create_rule_when_running_process
    before insert on ung.ac_auth_rules
    for each row execute procedure
    ung.prevent_create_rule_when_running_process();

--
create function ung.prevent_update_rule_when_running_process()
    returns trigger
    language plpgsql
as $$
begin
    if exists (select proc_id from ung.ac_processes_running limit 1) then
        raise 'Impossible to update authorization rules while processes are running.';
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_rule_when_running_process
    before update on ung.ac_auth_rules
    for each row execute procedure
    ung.prevent_update_rule_when_running_process();

--
create function ung.prevent_delete_rule_when_running_process()
    returns trigger
    language plpgsql
as $$
begin
    if exists (select proc_id from ung.ac_processes_running limit 1) then
        raise 'Impossible to delete authorization rules while processes are running.';
    end if;
    return OLD;
end;
$$;

create trigger prevent_delete_rule_when_running_process
    before delete on ung.ac_auth_rules
    for each row execute procedure
    ung.prevent_delete_rule_when_running_process();

--
-- NOTE: this trigger requires isolation level >= Repeatable Read
create function ung.shift_rule_ord_for_new_rule()
    returns trigger
    language plpgsql
as $$
begin
    set constraints ac_auth_rules_rule_ord_key deferred;
    NEW.rule_ord = least(NEW.rule_ord, (select max(rule_ord) + 1 from ung.ac_auth_rules));
    NEW.rule_ord = greatest(NEW.rule_ord, 1);
    update ung.ac_auth_rules
    set rule_ord = rule_ord + 1
    where rule_ord >= NEW.rule_ord;
    return NEW;
end;
$$;

create trigger shift_rule_ord_for_new_rule
    before insert on ung.ac_auth_rules
    for each row execute procedure
    ung.shift_rule_ord_for_new_rule();

--
-- NOTE: this trigger requires isolation level >= Repeatable Read
create function ung.shift_rule_ord_for_changed_rule()
    returns trigger
    language plpgsql
as $$
begin
    set constraints ac_auth_rules_rule_ord_key deferred;
    NEW.rule_ord = least(NEW.rule_ord, (select count(rule_id) from ung.ac_auth_rules));
    NEW.rule_ord = greatest(NEW.rule_ord, 1);
    if NEW.rule_ord > OLD.rule_ord
    then
        update ung.ac_auth_rules
        set rule_ord = rule_ord - 1
        where rule_ord > OLD.rule_ord and rule_ord <= NEW.rule_ord;
    else
        update ung.ac_auth_rules
        set rule_ord = rule_ord + 1
        where rule_ord < OLD.rule_ord and rule_ord >= NEW.rule_ord;
    end if;
    return NEW;
end;
$$;

create trigger shift_rule_ord_for_changed_rule
    before update on ung.ac_auth_rules
    for each row when (pg_trigger_depth() < 1) execute procedure
    ung.shift_rule_ord_for_changed_rule();

/* ------------------------------------------------------------------------------------------------
 Access Processes
------------------------------------------------------------------------------------------------ */

--
create function ung.prevent_update_to_finished_process()
    returns trigger
    language plpgsql
as $$
begin
    if OLD.finished_at is not null then
        raise 'Invalid attempt to update finished process proc_id=(%).', OLD.proc_id;
    end if;
    return NEW;
end;
$$;

create trigger prevent_update_to_finished_process
    before update on ung.ac_processes
    for each row execute procedure
    ung.prevent_update_to_finished_process();

--
create function ung.prevent_auth_events_on_finished_process()
    returns trigger
    language plpgsql
as $$
declare
    proc_fin_dt timestamptz;
begin
    proc_fin_dt := (select finished_at from ung.ac_processes proc where proc_id = NEW.proc_id);
    if proc_fin_dt is null or NEW.auth_at < proc_fin_dt
    then
        return NEW;
    else
        raise 'Invalid attempt to add authorization event happening at % referencing process % finished at %.',
            NEW.auth_at, NEW.proc_id, proc_fin_dt using errcode='check_violation';
    end if;
end;
$$;

create trigger prevent_auth_events_on_finished_process
    before insert on ung.ac_process_auth_events
    for each row execute procedure
    ung.prevent_auth_events_on_finished_process();


--
create function ung.ensure_active_flow_on_new_processes()
    returns trigger
    language plpgsql
as $$
begin
    if NEW.auth_flow is null
    then
        NEW.auth_flow := (select active_flow from ung.ac_settings limit 1);
    end if;
    return NEW;
end;
$$;

create trigger ensure_active_flow_on_new_processes
    before insert on ung.ac_processes
    for each row execute procedure
    ung.ensure_active_flow_on_new_processes();


-- TODO: create trigger to cleanup old zombie dangling processes during creation of new processes,
-- based on settings (time-to-live, max-running-processes).
