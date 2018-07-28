from .utils import parsed_result, maybe_default


# --------------------------------------------------------------------------------------------------
# Locations
# --------------------------------------------------------------------------------------------------

def create_location_group(db, group_name):
    return db.create_location_group(group_name=group_name)


def update_location_group(db, group_name, new_group_name):
    return db.update_location_group(group_name=group_name, new_group_name=new_group_name)


def retrieve_location_groups(db):
    return db.retrieve_location_groups()


def delete_location_groups_by_group_names(db, group_names):
    return db.delete_location_groups_by_group_names(group_names=tuple(group_names))


def create_location_group_membership(db, group_name, location_id):
    return db.create_location_group_membership(group_name=group_name, location_id=location_id)


def retrieve_location_group_memberships(db, group_name):
    return db.retrieve_location_group_memberships(group_name=group_name)


def retrieve_location_groups_by_member_id(db, location_id):
    return db.retrieve_location_groups_by_member_id(location_id=location_id)


def delete_location_group_memberships_by_member_ids(db, group_name, location_ids):
    return db.delete_location_group_memberships_by_member_ids(group_name=group_name,
                                                              location_ids=tuple(location_ids))


def delete_location_group_memberships_by_group_names(db, location_id, group_names):
    return db.delete_location_group_memberships_by_group_names(location_id=location_id,
                                                               group_names=tuple(group_names))


def create_location_assign_type(db, assign_type, assign_desc=None):
    return db.create_location_assign_type(assign_type=assign_type, assign_desc=assign_desc)


def retrieve_location_assign_types(db):
    return db.retrieve_location_assign_types()


def update_location_assign_type(db, assign_type, new_assign_type, assign_desc):
    return db.update_location_assign_type(assign_type=assign_type,
                                          new_assign_type=new_assign_type,
                                          assign_desc=assign_desc)


def delete_location_assign_types_by_assign_types(db, assign_types):
    return db.delete_location_assign_types_by_assign_types(assign_types=tuple(assign_types))


def create_contact_location_assignment(db, location_id, contact_id, assign_type):
    return db.create_contact_location_assignment(location_id=location_id,
                                                 contact_id=contact_id,
                                                 assign_type=assign_type)


def retrieve_contact_location_assignments_by_location_id(db, location_id):
    return db.retrieve_contact_location_assignments_by_location_id(location_id=location_id)


def retrieve_contact_location_assignments_by_contact_id(db, contact_id):
    return db.retrieve_contact_location_assignments_by_contact_id(contact_id=contact_id)


def delete_contact_location_assignments_by_ids(db, pks):
    return db.delete_contact_location_assignments_by_ids(pks=tuple(pks))


def create_location(db,
                    addr_1,
                    addr_2=None,
                    addr_3=None,
                    addr_4=None,
                    addr_5=None,
                    addr_6=None):
    return db.create_location(addr_1=addr_1,
                              addr_2=addr_2,
                              addr_3=addr_3,
                              addr_4=addr_4,
                              addr_5=addr_5,
                              addr_6=addr_6)


def retrieve_locations_by_ids(db, location_ids):
    return db.retrieve_locations_by_ids(location_ids=tuple(location_ids))


def update_location(db,
                    location_id,
                    addr_1,
                    addr_2=None,
                    addr_3=None,
                    addr_4=None,
                    addr_5=None,
                    addr_6=None):
    return db.update_location(location_id=location_id,
                              addr_1=addr_1,
                              addr_2=addr_2,
                              addr_3=addr_3,
                              addr_4=addr_4,
                              addr_5=addr_5,
                              addr_6=addr_6)


def delete_locations_by_ids(db, location_ids):
    return db.delete_locations_by_ids(location_ids=tuple(location_ids))


# --------------------------------------------------------------------------------------------------
# Contacts
# --------------------------------------------------------------------------------------------------

def create_contact_group(db, group_name):
    return db.create_contact_group(group_name=group_name)


def update_contact_group(db, group_name, new_group_name):
    return db.update_contact_group(group_name=group_name, new_group_name=new_group_name)


def retrieve_contact_groups(db):
    return db.retrieve_contact_groups()


def delete_contact_groups_by_group_names(db, group_names):
    return db.delete_contact_groups_by_group_names(group_names=tuple(group_names))


def create_contact_group_membership(db, group_name, contact_id):
    return db.create_contact_group_membership(group_name=group_name, contact_id=contact_id)


def retrieve_contact_group_memberships(db, group_name):
    return db.retrieve_contact_group_memberships(group_name=group_name)


def retrieve_contact_groups_by_member_id(db, contact_id):
    return db.retrieve_contact_groups_by_member_id(contact_id=contact_id)


def delete_contact_group_memberships_by_member_ids(db, group_name, contact_ids):
    return db.delete_contact_group_memberships_by_member_ids(group_name=group_name,
                                                             contact_ids=tuple(contact_ids))


def delete_contact_group_memberships_by_group_names(db, contact_id, group_names):
    return db.delete_contact_group_memberships_by_group_names(contact_id=contact_id,
                                                              group_names=tuple(group_names))


def create_contact(db, contact_name):
    return db.create_contact(contact_name=contact_name)


def retrieve_contacts_by_ids(db, contact_ids):
    return db.retrieve_contacts_by_ids(contact_ids=tuple(contact_ids))


def retrieve_person_contacts_by_name(db, contact_name_like, page_pos, page_size):
    return db.retrieve_person_contacts_by_name(contact_name=contact_name_like,
                                               page_pos=page_pos,
                                               page_size=page_size)


def update_contact(db, contact_id, contact_name):
    return db.update_contact(contact_id=contact_id, contact_name=contact_name)


def delete_contacts_by_ids(db, contact_ids):
    return db.delete_contacts_by_ids(contact_ids=tuple(contact_ids))


# --------------------------------------------------------------------------------------------------
# Vehicles
# --------------------------------------------------------------------------------------------------

def create_vehicle_group(db, group_name):
    return db.create_vehicle_group(group_name=group_name)


def update_vehicle_group(db, group_name, new_group_name):
    return db.update_vehicle_group(group_name=group_name, new_group_name=new_group_name)


def retrieve_vehicle_groups(db):
    return db.retrieve_vehicle_groups()


def delete_vehicle_groups_by_group_names(db, group_names):
    return db.delete_vehicle_groups_by_group_names(group_names=tuple(group_names))


def create_vehicle_group_membership(db, group_name, vehicle_id):
    return db.create_vehicle_group_membership(group_name=group_name, vehicle_id=vehicle_id)


def retrieve_vehicle_group_memberships(db, group_name):
    return db.retrieve_vehicle_group_memberships(group_name=group_name)


def retrieve_vehicle_groups_by_member_id(db, vehicle_id):
    return db.retrieve_vehicle_groups_by_member_id(vehicle_id=vehicle_id)


def delete_vehicle_group_memberships_by_member_ids(db, group_name, vehicle_ids):
    return db.delete_vehicle_group_memberships_by_member_ids(group_name=group_name,
                                                             vehicle_ids=tuple(vehicle_ids))


def delete_vehicle_group_memberships_by_group_names(db, vehicle_id, group_names):
    return db.delete_vehicle_group_memberships_by_group_names(vehicle_id=vehicle_id,
                                                              group_names=tuple(group_names))


def create_vehicle(db, plate, groups=None):
    return db.create_vehicle(plate=plate)


def retrieve_vehicles_by_ids(db, vehicle_ids):
    return db.retrieve_vehicles_by_ids(vehicle_ids=tuple(vehicle_ids))


def update_vehicle(db, vehicle_id, plate):
    return db.update_vehicle(vehicle_id=vehicle_id, plate=plate)


def delete_vehicles_by_ids(db, vehicle_ids):
    return db.delete_vehicles_by_ids(vehicle_ids=tuple(vehicle_ids))


# --------------------------------------------------------------------------------------------------
# Checkpoints
# --------------------------------------------------------------------------------------------------


def create_checkpoint_group(db, group_name):
    return db.create_checkpoint_group(group_name=group_name)


def update_checkpoint_group(db, group_name, new_group_name):
    return db.update_checkpoint_group(group_name=group_name, new_group_name=new_group_name)


def retrieve_checkpoint_groups(db):
    return db.retrieve_checkpoint_groups()


def delete_checkpoint_groups_by_group_names(db, group_names):
    return db.delete_checkpoint_groups_by_group_names(group_names=tuple(group_names))


def create_checkpoint_group_membership(db, group_name, checkpoint_id):
    return db.create_checkpoint_group_membership(group_name=group_name, checkpoint_id=checkpoint_id)


def retrieve_checkpoint_group_memberships(db, group_name):
    return db.retrieve_checkpoint_group_memberships(group_name=group_name)


def retrieve_checkpoint_groups_by_member_id(db, checkpoint_id):
    return db.retrieve_checkpoint_groups_by_member_id(checkpoint_id=checkpoint_id)


def delete_checkpoint_group_memberships_by_member_ids(db, group_name, checkpoint_ids):
    return db.delete_checkpoint_group_memberships_by_member_ids(
        group_name=group_name, checkpoint_ids=tuple(checkpoint_ids))


def delete_checkpoint_group_memberships_by_group_names(db, checkpoint_id, group_names):
    return db.delete_checkpoint_group_memberships_by_group_names(checkpoint_id=checkpoint_id,
                                                                 group_names=tuple(group_names))


def create_checkpoint(db, checkpoint_name, groups=None):
    return db.create_checkpoint(checkpoint_name=checkpoint_name)


def retrieve_checkpoints_by_ids(db, checkpoint_ids):
    return db.retrieve_checkpoints_by_ids(checkpoint_ids=tuple(checkpoint_ids))


def update_checkpoint(db, checkpoint_id, checkpoint_name):
    return db.update_checkpoint(checkpoint_id=checkpoint_id, checkpoint_name=checkpoint_name)


def delete_checkpoints_by_ids(db, checkpoint_ids):
    return db.delete_checkpoints_by_ids(checkpoint_ids=tuple(checkpoint_ids))


# --------------------------------------------------------------------------------------------------
# Access Flow
# --------------------------------------------------------------------------------------------------

def create_auth_level(db, auth_name, auth_grant=None):
    return db.create_auth_level(auth_name=auth_name, auth_grant=auth_grant)


def retrieve_auth_levels_by_ids(db, auth_names):
    return db.retrieve_auth_levels_by_ids(auth_names=tuple(auth_names))


def update_auth_level(db, pk, auth_name, auth_grant=None):
    return db.update_auth_level(pk=pk, auth_grant=auth_grant, auth_name=auth_name)


def delete_auth_levels_by_ids(db, auth_names):
    return db.delete_auth_levels_by_ids(auth_names=tuple(auth_names))


# ---

def create_auth_flow(db, auth_flow_desc=None):
    return db.create_auth_flow(auth_flow_desc=auth_flow_desc)


def retrieve_auth_flows_by_ids(db, auth_flow_ids):
    return db.retrieve_auth_flows_by_ids(auth_flow_ids=tuple(auth_flow_ids))


def update_auth_flow(db, auth_flow_id, auth_flow_desc=None):
    return db.update_auth_flow(auth_flow_id=auth_flow_id, auth_flow_desc=auth_flow_desc)


def delete_auth_flows_by_ids(db, auth_flow_ids):
    return db.delete_auth_flows_by_ids(auth_flow_ids=tuple(auth_flow_ids))


# ---

@parsed_result(r'\((\d+),(.*)\)')
def create_auth_flow_st(db, auth_flow_id, st_name, st_term=None):
    return db.create_auth_flow_st(auth_flow_id=auth_flow_id, st_name=st_name, st_term=st_term)


def retrieve_auth_flow_sts_by_ids(db, pks):
    return db.retrieve_auth_flow_sts_by_ids(pks=tuple(pks))


def retrieve_auth_flow_sts_by_auth_flow_id(db, auth_flow_id):
    return db.retrieve_auth_flow_sts_by_auth_flow_id(auth_flow_id=auth_flow_id)


def update_auth_flow_st(db, pk, st_term=None):
    return db.update_auth_flow_st(pk=pk, st_term=st_term)


def delete_auth_flow_sts_by_ids(db, pks):
    return db.delete_auth_flow_sts_by_ids(pks=tuple(pks))


# ---

@parsed_result(r'\((\d+),([^,]*),([^,]*),([^,]*)\)')
def create_auth_flow_tr(db, auth_flow_id, when_ev, curr_st, next_st):
    return db.create_auth_flow_tr(auth_flow_id=auth_flow_id,
                                  when_ev=when_ev,
                                  curr_st=curr_st,
                                  next_st=next_st)


def retrieve_auth_flow_trs_by_ids(db, pks):
    return db.retrieve_auth_flow_trs_by_ids(pks=tuple(pks))


def retrieve_auth_flow_trs_by_auth_flow_id(db, auth_flow_id):
    return db.retrieve_auth_flow_trs_by_auth_flow_id(auth_flow_id=auth_flow_id)


def update_auth_flow_tr(db, pk, when_ev, curr_st, next_st):
    return db.update_auth_flow_tr(pk=pk, when_ev=when_ev, curr_st=curr_st, next_st=next_st)


def delete_auth_flow_trs_by_ids(db, pks):
    return db.delete_auth_flow_trs_by_ids(pks=tuple(pks))


# ---

def retrieve_auth_flow_setting_active_flow(db):
    return db.retrieve_auth_flow_setting_active_flow()[0]['active_flow']


def update_auth_flow_setting_active_flow(db, auth_flow_id):
    db.update_auth_flow_setting_active_flow(auth_flow_id=auth_flow_id)


# ---

def create_auth_rule(db,
                     rule_ord,
                     effect,
                     ctc=None,
                     loc_orig=None,
                     loc_dest=None,
                     ckp=None,
                     vhc=None,
                     ctc_grp=None,
                     vhc_grp=None,
                     loc_grp=None,
                     ckp_grp=None,
                     loc_ass=None,
                     year0=None,
                     year1=None,
                     month0=None,
                     month1=None,
                     mday0=None,
                     mday1=None,
                     wday0=None,
                     wday1=None,
                     hour0=None,
                     hour1=None,
                     minute0=None,
                     minute1=None):
    return db.create_auth_rule(ctc=maybe_default(db, ctc),
                               loc_orig=maybe_default(db, loc_orig),
                               loc_dest=maybe_default(db, loc_dest),
                               ckp=maybe_default(db, ckp),
                               vhc=maybe_default(db, vhc),
                               ctc_grp=maybe_default(db, ctc_grp),
                               vhc_grp=maybe_default(db, vhc_grp),
                               loc_grp=maybe_default(db, loc_grp),
                               ckp_grp=maybe_default(db, ckp_grp),
                               loc_ass=maybe_default(db, loc_ass),
                               year0=maybe_default(db, year0),
                               year1=maybe_default(db, year1),
                               month0=maybe_default(db, month0),
                               month1=maybe_default(db, month1),
                               mday0=maybe_default(db, mday0),
                               mday1=maybe_default(db, mday1),
                               wday0=maybe_default(db, wday0),
                               wday1=maybe_default(db, wday1),
                               hour0=maybe_default(db, hour0),
                               hour1=maybe_default(db, hour1),
                               minute0=maybe_default(db, minute0),
                               minute1=maybe_default(db, minute1),
                               rule_ord=rule_ord,
                               effect=effect)


def retrieve_auth_rules_by_ids(db, pks):
    return db.retrieve_auth_rules_by_ids(pks=tuple(pks))


def update_auth_rule(db,
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
                     minute1):
    return db.update_auth_rule(rule_id=rule_id,
                               ctc=ctc,
                               loc_orig=loc_orig,
                               loc_dest=loc_dest,
                               ckp=ckp,
                               vhc=vhc,
                               ctc_grp=ctc_grp,
                               vhc_grp=vhc_grp,
                               loc_grp=loc_grp,
                               ckp_grp=ckp_grp,
                               loc_ass=loc_ass,
                               year0=year0,
                               year1=year1,
                               month0=month0,
                               month1=month1,
                               mday0=mday0,
                               mday1=mday1,
                               wday0=wday0,
                               wday1=wday1,
                               hour0=hour0,
                               hour1=hour1,
                               minute0=minute0,
                               minute1=minute1,
                               rule_ord=rule_ord,
                               effect=effect)


def delete_auth_rules_by_ids(db, pks):
    return db.delete_auth_rules_by_ids(pks=tuple(pks))


# --------------------------------------------------------------------------------------------------
# Access Process
# --------------------------------------------------------------------------------------------------

def create_process(db, started_at=None):
    return db.create_process(started_at=started_at)


def retrieve_processes_by_ids(db, proc_ids):
    return db.retrieve_processes_by_ids(proc_ids=tuple(proc_ids))


def update_process(db, proc_id, ctc, loc_orig, loc_dest, ckp, vhc):
    return db.update_process(proc_id=proc_id,
                             ctc=ctc,
                             loc_orig=loc_orig,
                             loc_dest=loc_dest,
                             ckp=ckp,
                             vhc=vhc)


def retrieve_process_snapshots_running_by_ids(db, pks):
    return db.retrieve_process_snapshots_running_by_ids(proc_ids=tuple(pks))


def retrieve_process_histories_by_ids(db, pks):
    return db.retrieve_process_histories_by_ids(proc_ids=tuple(pks))


def update_process_auth_flow(db, proc_id, auth_flow):
    return db.update_process_auth_flow(proc_id=proc_id, auth_flow=auth_flow)


def update_process_terminate(db, proc_id, finished_at=None):
    return db.update_process_terminate(proc_id=proc_id, finished_at=finished_at)


def archive_finished_processes(db):
    return db.archive_finished_processes()


def delete_processes_by_ids(db, pks):
    return db.delete_processes_by_ids(proc_ids=tuple(pks))


def retrieve_processes_rule_matches(db):
    return db.retrieve_processes_rule_matches()


def retrieve_processes_rule_selections(db):
    return db.retrieve_processes_rule_selections()


# ---

def create_process_auth_event(db, proc_id, auth_by, auth_name, auth_at=None):
    return db.create_process_auth_event(db, proc_id=proc_id,
                                        auth_by=auth_by,
                                        auth_name=auth_name,
                                        auth_at=auth_at)
