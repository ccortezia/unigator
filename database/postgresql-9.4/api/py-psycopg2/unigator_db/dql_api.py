def create_location(conn, addr_1=None, addr_2=None, addr_3=None, addr_4=None, addr_5=None, addr_6=None):
    import psycopg2
    sql_query = "insert into ung.ac_locations (addr_1, addr_2, addr_3, addr_4, addr_5, addr_6) values (%(addr_1)s, %(addr_2)s, %(addr_3)s, %(addr_4)s, %(addr_5)s, %(addr_6)s) returning location_id ;"
    sql_params = dict(addr_1=addr_1, addr_2=addr_2, addr_3=addr_3, addr_4=addr_4, addr_5=addr_5, addr_6=addr_6)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_locations_by_ids(conn, location_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_locations where location_id in %(location_ids)s ;"
    sql_params = dict(location_ids=location_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(location_id=row[0], addr_1=row[1], addr_2=row[2], addr_3=row[3], addr_4=row[4], addr_5=row[5], addr_6=row[6]) for row in fetched]


def update_location(conn, location_id=None, addr_1=None, addr_2=None, addr_3=None, addr_4=None, addr_5=None, addr_6=None):
    import psycopg2
    sql_query = "update ung.ac_locations set addr_1=%(addr_1)s,     addr_2=%(addr_2)s,     addr_3=%(addr_3)s,     addr_4=%(addr_4)s,     addr_5=%(addr_5)s,     addr_6=%(addr_6)s where location_id = %(location_id)s ;"
    sql_params = dict(location_id=location_id, addr_1=addr_1, addr_2=addr_2, addr_3=addr_3, addr_4=addr_4, addr_5=addr_5, addr_6=addr_6)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_locations_by_ids(conn, location_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_locations where location_id in %(location_ids)s ;"
    sql_params = dict(location_ids=location_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_location_group(conn, group_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_location_groups (group_name) values (%(group_name)s) returning group_name ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def update_location_group(conn, group_name=None, new_group_name=None):
    import psycopg2
    sql_query = "update ung.ac_location_groups set group_name=(%(new_group_name)s) where group_name=%(group_name)s ;"
    sql_params = dict(group_name=group_name, new_group_name=new_group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_all_location_groups(conn):
    import psycopg2
    sql_query = "select * from ung.ac_location_groups order by group_name asc ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def delete_location_groups_by_group_names(conn, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_location_groups where group_name in %(group_names)s ;"
    sql_params = dict(group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def add_location_group_member(conn, group_name=None, location_id=None):
    import psycopg2
    sql_query = "insert into ung.ac_location_groups_x_locations (group_name, location_id) values (%(group_name)s, %(location_id)s) ;"
    sql_params = dict(group_name=group_name, location_id=location_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_location_group_members(conn, group_name=None):
    import psycopg2
    sql_query = "select loc.* from ung.ac_location_groups_x_locations locg_loc join ung.ac_locations loc using(location_id) where group_name = %(group_name)s ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(location_id=row[0], addr_1=row[1], addr_2=row[2], addr_3=row[3], addr_4=row[4], addr_5=row[5], addr_6=row[6]) for row in fetched]


def retrieve_location_groups_by_location_id(conn, location_id=None):
    import psycopg2
    sql_query = "select group_name from ung.ac_location_groups_x_locations where location_id = %(location_id)s ;"
    sql_params = dict(location_id=location_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def remove_location_group_members(conn, group_name=None, location_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_location_groups_x_locations where group_name = %(group_name)s and location_id in %(location_ids)s ;"
    sql_params = dict(group_name=group_name, location_ids=location_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def remove_location_from_location_groups(conn, location_id=None, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_location_groups_x_locations where location_id = %(location_id)s and group_name in %(group_names)s ;"
    sql_params = dict(location_id=location_id, group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_location_assign_type(conn, assign_type=None, assign_desc=None):
    import psycopg2
    sql_query = "insert into ung.ac_location_assign_types (assign_type, assign_desc) values (%(assign_type)s, %(assign_desc)s) returning assign_type ;"
    sql_params = dict(assign_type=assign_type, assign_desc=assign_desc)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_all_location_assign_types(conn):
    import psycopg2
    sql_query = "select * from ung.ac_location_assign_types order by assign_type asc ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(assign_type=row[0], assign_desc=row[1]) for row in fetched]


def update_location_assign_type(conn, assign_type=None, new_assign_type=None, assign_desc=None):
    import psycopg2
    sql_query = "update ung.ac_location_assign_types set assign_type=%(new_assign_type)s, assign_desc=%(assign_desc)s where assign_type = %(assign_type)s ;"
    sql_params = dict(assign_type=assign_type, new_assign_type=new_assign_type, assign_desc=assign_desc)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_location_assign_types_by_assign_types(conn, assign_types=None):
    import psycopg2
    sql_query = "delete from ung.ac_location_assign_types where assign_type in %(assign_types)s ;"
    sql_params = dict(assign_types=assign_types)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def assign_contact_to_location(conn, location_id=None, contact_id=None, assign_type=None):
    import psycopg2
    sql_query = "insert into ung.ac_contacts_x_locations (location_id, contact_id, assign_type) values (%(location_id)s, %(contact_id)s, %(assign_type)s) ;"
    sql_params = dict(location_id=location_id, contact_id=contact_id, assign_type=assign_type)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_location_contact_assignments(conn, location_id=None):
    import psycopg2
    sql_query = "select contact_id, contact_name, assign_type from ung.ac_contacts_x_locations join ung.ac_contacts using(contact_id) where location_id = %(location_id)s order by contact_name, assign_type ;"
    sql_params = dict(location_id=location_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(contact_id=row[0], contact_name=row[1], assign_type=row[2]) for row in fetched]


def retrieve_location_contact_assignments_by_contact_id(conn, contact_id=None):
    import psycopg2
    sql_query = "select loc.*, assign_type from ung.ac_contacts_x_locations join ung.ac_locations loc using (location_id) where contact_id = %(contact_id)s order by assign_type ;"
    sql_params = dict(contact_id=contact_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(location_id=row[0], addr_1=row[1], addr_2=row[2], addr_3=row[3], addr_4=row[4], addr_5=row[5], addr_6=row[6], assign_type=row[7]) for row in fetched]


def delete_contact_location_assignment(conn, location_id=None, contact_id=None, assign_type=None):
    import psycopg2
    sql_query = "delete from ung.ac_contacts_x_locations where location_id=%(location_id)s and contact_id=%(contact_id)s and assign_type=%(assign_type)s ;"
    sql_params = dict(location_id=location_id, contact_id=contact_id, assign_type=assign_type)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_vehicle(conn, plate=None):
    import psycopg2
    sql_query = "insert into ung.ac_vehicles (plate) values (%(plate)s) returning vehicle_id ;"
    sql_params = dict(plate=plate)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_vehicles_by_ids(conn, vehicle_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_vehicles where vehicle_id in %(vehicle_ids)s ;"
    sql_params = dict(vehicle_ids=vehicle_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(vehicle_id=row[0], plate=row[1]) for row in fetched]


def update_vehicle(conn, vehicle_id=None, plate=None):
    import psycopg2
    sql_query = "update ung.ac_vehicles set plate=(%(plate)s) where vehicle_id = %(vehicle_id)s ;"
    sql_params = dict(vehicle_id=vehicle_id, plate=plate)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_vehicles_by_ids(conn, vehicle_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_vehicles where vehicle_id in %(vehicle_ids)s ;"
    sql_params = dict(vehicle_ids=vehicle_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_vehicle_group(conn, group_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_vehicle_groups (group_name) values (%(group_name)s) returning group_name ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def update_vehicle_group(conn, group_name=None, new_group_name=None):
    import psycopg2
    sql_query = "update ung.ac_vehicle_groups set group_name=(%(new_group_name)s) where group_name=%(group_name)s ;"
    sql_params = dict(group_name=group_name, new_group_name=new_group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_all_vehicle_groups(conn):
    import psycopg2
    sql_query = "select * from ung.ac_vehicle_groups order by group_name asc ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def delete_vehicle_groups_by_group_names(conn, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_vehicle_groups where group_name in %(group_names)s ;"
    sql_params = dict(group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def add_vehicle_group_member(conn, group_name=None, vehicle_id=None):
    import psycopg2
    sql_query = "insert into ung.ac_vehicle_groups_x_vehicles (group_name, vehicle_id) values (%(group_name)s, %(vehicle_id)s) ;"
    sql_params = dict(group_name=group_name, vehicle_id=vehicle_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_vehicle_group_members(conn, group_name=None):
    import psycopg2
    sql_query = "select vehicle_id, plate from ung.ac_vehicle_groups_x_vehicles vhcg_vhc join ung.ac_vehicles using(vehicle_id) where group_name = %(group_name)s ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(vehicle_id=row[0], plate=row[1]) for row in fetched]


def retrieve_vehicle_groups_by_vehicle_id(conn, vehicle_id=None):
    import psycopg2
    sql_query = "select group_name from ung.ac_vehicle_groups_x_vehicles where vehicle_id = %(vehicle_id)s ;"
    sql_params = dict(vehicle_id=vehicle_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def remove_vehicle_group_members(conn, group_name=None, vehicle_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_vehicle_groups_x_vehicles where group_name = %(group_name)s and vehicle_id in %(vehicle_ids)s ;"
    sql_params = dict(group_name=group_name, vehicle_ids=vehicle_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def remove_vehicle_from_vehicle_groups(conn, vehicle_id=None, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_vehicle_groups_x_vehicles where vehicle_id = %(vehicle_id)s and group_name in %(group_names)s ;"
    sql_params = dict(vehicle_id=vehicle_id, group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_process(conn, started_at=None):
    import psycopg2
    sql_query = "insert into ung.ac_processes (started_at) values (coalesce(%(started_at)s, statement_timestamp())) returning proc_id ;"
    sql_params = dict(started_at=started_at)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_processes_by_ids(conn, proc_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_processes where proc_id in %(proc_ids)s ;"
    sql_params = dict(proc_ids=proc_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(proc_id=row[0], ctc=row[1], loc_orig=row[2], loc_dest=row[3], ckp=row[4], vhc=row[5], auth_flow=row[6], started_at=row[7], finished_at=row[8]) for row in fetched]


def update_process(conn, proc_id=None, ctc=None, loc_orig=None, loc_dest=None, ckp=None, vhc=None):
    import psycopg2
    sql_query = "update ung.ac_processes set  ctc = %(ctc)s, loc_orig = %(loc_orig)s, loc_dest = %(loc_dest)s, ckp = %(ckp)s, vhc = %(vhc)s where proc_id = %(proc_id)s ;"
    sql_params = dict(proc_id=proc_id, ctc=ctc, loc_orig=loc_orig, loc_dest=loc_dest, ckp=ckp, vhc=vhc)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def update_process_auth_flow(conn, proc_id=None, auth_flow=None):
    import psycopg2
    sql_query = "update ung.ac_processes set  auth_flow = %(auth_flow)s where proc_id = %(proc_id)s ;"
    sql_params = dict(proc_id=proc_id, auth_flow=auth_flow)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def terminate_process(conn, proc_id=None, finished_at=None):
    import psycopg2
    sql_query = "update ung.ac_processes set finished_at = coalesce(%(finished_at)s, statement_timestamp()) where proc_id = %(proc_id)s returning finished_at ;"
    sql_params = dict(proc_id=proc_id, finished_at=finished_at)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def delete_processes_by_ids(conn, proc_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_processes where proc_id in %(proc_ids)s ;"
    sql_params = dict(proc_ids=proc_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_process_auth_event(conn, proc_id=None, auth_by=None, auth_name=None, auth_at=None):
    import psycopg2
    sql_query = "insert into ung.ac_process_auth_events (proc_id, auth_by, auth_name, auth_at) values (%(proc_id)s,%(auth_by)s,%(auth_name)s,coalesce(%(auth_at)s, statement_timestamp())) returning auth_at ;"
    sql_params = dict(proc_id=proc_id, auth_by=auth_by, auth_name=auth_name, auth_at=auth_at)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def archive_finished_processes(conn):
    import psycopg2
    sql_query = "select archived_proc_id, archived_finished_at from ung.ac_archive_finished_processes() ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(archived_proc_id=row[0], archived_finished_at=row[1]) for row in fetched]


def retrieve_process_histories_by_ids(conn, proc_ids=None):
    import psycopg2
    sql_query = "select     proc_id,     ctc.contact_id as subject_id,     ctc.contact_name as subject_name,     vhc.vehicle_id as vehicle_id,     vhc.plate as vehicle_plate,     loc_orig.location_id as location_orig_id,     loc_orig.addr_1 as location_orig_addr_1,     loc_orig.addr_2 as location_orig_addr_2,     loc_orig.addr_3 as location_orig_addr_3,     loc_orig.addr_4 as location_orig_addr_4,     loc_orig.addr_5 as location_orig_addr_5,     loc_orig.addr_6 as location_orig_addr_6,     loc_dest.location_id as location_dest_id,     loc_dest.addr_1 as location_dest_addr_1,     loc_dest.addr_2 as location_dest_addr_2,     loc_dest.addr_3 as location_dest_addr_3,     loc_dest.addr_4 as location_dest_addr_4,     loc_dest.addr_5 as location_dest_addr_5,     loc_dest.addr_6 as location_dest_addr_6,     auth_by.contact_id as authorizer_id,     auth_by.contact_name as authorizer_name,     started_at,     finished_at,     auth_at as auth_event_at,     ev_seq as auth_event_seq,     curr_st as curr_auth_flow_st from ung.ac_process_histories proc     left join ung.ac_contacts ctc on ctc.contact_id = proc.ctc     left join ung.ac_vehicles vhc on vhc.vehicle_id = proc.vhc     left join ung.ac_locations loc_orig on loc_orig.location_id = proc.loc_orig     left join ung.ac_locations loc_dest on loc_dest.location_id = proc.loc_dest     left join ung.ac_contacts auth_by on auth_by.contact_id = proc.auth_by where proc_id in %(proc_ids)s ;"
    sql_params = dict(proc_ids=proc_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(proc_id=row[0], subject_id=row[1], subject_name=row[2], vehicle_id=row[3], vehicle_plate=row[4], location_orig_id=row[5], location_orig_addr1=row[6], location_orig_addr2=row[7], location_orig_addr3=row[8], location_orig_addr4=row[9], location_orig_addr5=row[10], location_orig_addr6=row[11], location_dest_id=row[12], location_dest_addr1=row[13], location_dest_addr2=row[14], location_dest_addr3=row[15], location_dest_addr4=row[16], location_dest_addr5=row[17], location_dest_addr6=row[18], authorizer_id=row[19], authorizer_name=row[20], started_at=row[21], finished_at=row[22], auth_event_at=row[23], auth_event_seq=row[24], curr_auth_flow_st=row[25]) for row in fetched]


def retrieve_all_running_process_snapshots(conn, proc_ids=None):
    import psycopg2
    sql_query = "select     proc_id,     ctc.contact_id as subject_id,     ctc.contact_name as subject_name,     vhc.vehicle_id as vehicle_id,     vhc.plate as vehicle_plate,     loc_orig.location_id as location_orig_id,     loc_orig.addr_1 as location_orig_addr_1,     loc_orig.addr_2 as location_orig_addr_2,     loc_orig.addr_3 as location_orig_addr_3,     loc_orig.addr_4 as location_orig_addr_4,     loc_orig.addr_5 as location_orig_addr_5,     loc_orig.addr_6 as location_orig_addr_6,     loc_dest.location_id as location_dest_id,     loc_dest.addr_1 as location_dest_addr_1,     loc_dest.addr_2 as location_dest_addr_2,     loc_dest.addr_3 as location_dest_addr_3,     loc_dest.addr_4 as location_dest_addr_4,     loc_dest.addr_5 as location_dest_addr_5,     loc_dest.addr_6 as location_dest_addr_6,     auth_by.contact_id as authorizer_id,     auth_by.contact_name as authorizer_name,     started_at,     finished_at from ung.ac_process_snapshots_running proc     left join ung.ac_contacts ctc on ctc.contact_id = proc.ctc     left join ung.ac_vehicles vhc on vhc.vehicle_id = proc.vhc     left join ung.ac_locations loc_orig on loc_orig.location_id = proc.loc_orig     left join ung.ac_locations loc_dest on loc_dest.location_id = proc.loc_dest     left join ung.ac_contacts auth_by on auth_by.contact_id = proc.auth_by ;"
    sql_params = dict(proc_ids=proc_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(proc_id=row[0], subject_id=row[1], subject_name=row[2], vehicle_id=row[3], vehicle_plate=row[4], location_orig_id=row[5], location_orig_addr1=row[6], location_orig_addr2=row[7], location_orig_addr3=row[8], location_orig_addr4=row[9], location_orig_addr5=row[10], location_orig_addr6=row[11], location_dest_id=row[12], location_dest_addr1=row[13], location_dest_addr2=row[14], location_dest_addr3=row[15], location_dest_addr4=row[16], location_dest_addr5=row[17], location_dest_addr6=row[18], authorizer_id=row[19], authorizer_name=row[20], started_at=row[21], finished_at=row[22]) for row in fetched]


def retrieve_processes_rule_matches(conn):
    import psycopg2
    sql_query = "select * from ung.ac_processes_rule_matches ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(proc_id=row[0], match_rule_id=row[1], match_rule_ord=row[2], resolved_auth_name=row[3], resolved_auth_grant=row[4]) for row in fetched]


def retrieve_processes_rule_selections(conn):
    import psycopg2
    sql_query = "select * from ung.ac_processes_rule_selections ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(proc_id=row[0], match_rule_id=row[1], resolved_auth_name=row[2], resolved_auth_grant=row[3]) for row in fetched]


def create_auth_level(conn, auth_name=None, auth_grant=None):
    import psycopg2
    sql_query = "insert into ung.ac_auth_levels (auth_name, auth_grant) values (%(auth_name)s, %(auth_grant)s) returning auth_name ;"
    sql_params = dict(auth_name=auth_name, auth_grant=auth_grant)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_auth_levels_by_auth_name(conn, auth_names=None):
    import psycopg2
    sql_query = "select * from ung.ac_auth_levels where auth_name in %(auth_names)s ;"
    sql_params = dict(auth_names=auth_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(auth_name=row[0], auth_grant=row[1]) for row in fetched]


def update_auth_level(conn, auth_name=None, new_auth_name=None, auth_grant=None):
    import psycopg2
    sql_query = "update ung.ac_auth_levels set auth_name=(%(new_auth_name)s), auth_grant=(%(auth_grant)s) where auth_name = %(auth_name)s ;"
    sql_params = dict(auth_name=auth_name, new_auth_name=new_auth_name, auth_grant=auth_grant)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_auth_levels_by_auth_names(conn, auth_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_auth_levels where auth_name in %(auth_names)s ;"
    sql_params = dict(auth_names=auth_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_auth_flow(conn, auth_flow_desc=None):
    import psycopg2
    sql_query = "insert into ung.ac_auth_flows (auth_flow_desc) values (%(auth_flow_desc)s) returning auth_flow_id ;"
    sql_params = dict(auth_flow_desc=auth_flow_desc)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_auth_flows_by_ids(conn, auth_flow_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_auth_flows where auth_flow_id in %(auth_flow_ids)s ;"
    sql_params = dict(auth_flow_ids=auth_flow_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(auth_flow_id=row[0], auth_flow_desc=row[1], init_st=row[2], created_at=row[3]) for row in fetched]


def update_auth_flow(conn, auth_flow_id=None, auth_flow_desc=None):
    import psycopg2
    sql_query = "update ung.ac_auth_flows set auth_flow_desc=(%(auth_flow_desc)s) where auth_flow_id = %(auth_flow_id)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id, auth_flow_desc=auth_flow_desc)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_auth_flows_by_ids(conn, auth_flow_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_auth_flows where auth_flow_id in %(auth_flow_ids)s ;"
    sql_params = dict(auth_flow_ids=auth_flow_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_auth_flow_st(conn, auth_flow_id=None, st_name=None, st_term=None):
    import psycopg2
    sql_query = "insert into ung.ac_auth_flow_sts (auth_flow_id, st_name, st_term) values (%(auth_flow_id)s, %(st_name)s, %(st_term)s) returning auth_flow_id, st_name ;"
    sql_params = dict(auth_flow_id=auth_flow_id, st_name=st_name, st_term=st_term)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return dict(auth_flow_id=fetched[0][0], st_name=fetched[0][1])


def retrieve_auth_flow_sts_by_auth_flow_id(conn, auth_flow_id=None):
    import psycopg2
    sql_query = "select st_name, st_term from ung.ac_auth_flow_sts where auth_flow_id = %(auth_flow_id)s order by st_name ;"
    sql_params = dict(auth_flow_id=auth_flow_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(st_name=row[0], st_term=row[1]) for row in fetched]


def update_auth_flow_st(conn, auth_flow_id=None, st_name=None, st_term=None):
    import psycopg2
    sql_query = "update ung.ac_auth_flow_sts set st_term=(%(st_term)s) where auth_flow_id = %(auth_flow_id)s and st_name = %(st_name)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id, st_name=st_name, st_term=st_term)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_auth_flow_st_by_id(conn, auth_flow_id=None, st_name=None):
    import psycopg2
    sql_query = "delete from ung.ac_auth_flow_sts where auth_flow_id = %(auth_flow_id)s and st_name = %(st_name)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id, st_name=st_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_auth_flow_tr(conn, auth_flow_id=None, when_ev=None, curr_st=None, next_st=None):
    import psycopg2
    sql_query = "insert into ung.ac_auth_flow_trs (auth_flow_id, when_ev, curr_st, next_st) values (%(auth_flow_id)s, %(when_ev)s, %(curr_st)s, %(next_st)s) returning auth_flow_id, when_ev, curr_st, next_st ;"
    sql_params = dict(auth_flow_id=auth_flow_id, when_ev=when_ev, curr_st=curr_st, next_st=next_st)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return dict(auth_flow_id=fetched[0][0], when_ev=fetched[0][1], curr_st=fetched[0][2], next_st=fetched[0][3])


def retrieve_auth_flow_trs_by_auth_flow_id(conn, auth_flow_id=None):
    import psycopg2
    sql_query = "select auth_flow_id, when_ev, curr_st, next_st from ung.ac_auth_flow_trs where auth_flow_id = %(auth_flow_id)s order by when_ev, curr_st, next_st ;"
    sql_params = dict(auth_flow_id=auth_flow_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(auth_flow_id=row[0], when_ev=row[1], curr_st=row[2], next_st=row[3]) for row in fetched]


def update_auth_flow_tr(conn, auth_flow_id=None, when_ev=None, curr_st=None, next_st=None, new_when_ev=None, new_curr_st=None, new_next_st=None):
    import psycopg2
    sql_query = "update ung.ac_auth_flow_trs set when_ev=%(new_when_ev)s,     curr_st=%(new_curr_st)s,     next_st=%(new_next_st)s where auth_flow_id=%(auth_flow_id)s and curr_st=%(curr_st)s and next_st=%(next_st)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id, when_ev=when_ev, curr_st=curr_st, next_st=next_st, new_when_ev=new_when_ev, new_curr_st=new_curr_st, new_next_st=new_next_st)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_auth_flow_tr_by_id(conn, auth_flow_id=None, when_ev=None, curr_st=None, next_st=None):
    import psycopg2
    sql_query = "delete from ung.ac_auth_flow_trs where auth_flow_id=%(auth_flow_id)s and curr_st=%(curr_st)s and next_st=%(next_st)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id, when_ev=when_ev, curr_st=curr_st, next_st=next_st)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_current_active_auth_flow(conn):
    import psycopg2
    sql_query = "select flows.* from ung.ac_settings settings join ung.ac_auth_flows flows   on settings.active_flow = flows.auth_flow_id ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return dict(auth_flow_id=fetched[0][0], auth_flow_desc=fetched[0][1])


def update_current_active_auth_flow(conn, auth_flow_id=None):
    import psycopg2
    sql_query = "update ung.ac_settings set active_flow = %(auth_flow_id)s ;"
    sql_params = dict(auth_flow_id=auth_flow_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_auth_rule(conn, rule_ord=None, effect=None, ctc=None, loc_orig=None, loc_dest=None, ckp=None, vhc=None, ctc_grp=None, vhc_grp=None, loc_grp=None, ckp_grp=None, loc_ass=None, year0=None, year1=None, month0=None, month1=None, mday0=None, mday1=None, wday0=None, wday1=None, hour0=None, hour1=None, minute0=None, minute1=None):
    import psycopg2
    sql_query = "insert into ung.ac_auth_rules (     rule_ord,     effect,     ctc,     loc_orig,     loc_dest,     ckp,     vhc,     ctc_grp,     vhc_grp,     loc_grp,     ckp_grp,     loc_ass,     year0,     year1,     month0,     month1,     mday0,     mday1,     wday0,     wday1,     hour0,     hour1,     minute0,     minute1) values (     %(rule_ord)s,     %(effect)s,     %(ctc)s,     %(loc_orig)s,     %(loc_dest)s,     %(ckp)s,     %(vhc)s,     %(ctc_grp)s,     %(vhc_grp)s,     %(loc_grp)s,     %(ckp_grp)s,     %(loc_ass)s,     %(year0)s,     %(year1)s,     %(month0)s,     %(month1)s,     %(mday0)s,     %(mday1)s,     %(wday0)s,     %(wday1)s,     %(hour0)s,     %(hour1)s,     %(minute0)s,     %(minute1)s) returning rule_id ;"
    sql_params = dict(rule_ord=rule_ord, effect=effect, ctc=ctc, loc_orig=loc_orig, loc_dest=loc_dest, ckp=ckp, vhc=vhc, ctc_grp=ctc_grp, vhc_grp=vhc_grp, loc_grp=loc_grp, ckp_grp=ckp_grp, loc_ass=loc_ass, year0=year0, year1=year1, month0=month0, month1=month1, mday0=mday0, mday1=mday1, wday0=wday0, wday1=wday1, hour0=hour0, hour1=hour1, minute0=minute0, minute1=minute1)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_auth_rules_by_ids(conn, rule_ids=None):
    import psycopg2
    sql_query = "select     rule_id,     rule_ord,     effect,     ctc,     loc_orig,     loc_dest,     ckp,     vhc,     ctc_grp,     vhc_grp,     loc_grp,     ckp_grp,     loc_ass,     year0,     year1,     month0,     month1,     mday0,     mday1,     wday0,     wday1,     hour0,     hour1,     minute0,     minute1 from ung.ac_auth_rules where rule_id in %(rule_ids)s order by rule_id, rule_ord ;"
    sql_params = dict(rule_ids=rule_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(rule_id=row[0], rule_ord=row[1], effect=row[2], ctc=row[3], loc_orig=row[4], loc_dest=row[5], ckp=row[6], vhc=row[7], ctc_grp=row[8], vhc_grp=row[9], loc_grp=row[10], ckp_grp=row[11], loc_ass=row[12], year0=row[13], year1=row[14], month0=row[15], month1=row[16], mday0=row[17], mday1=row[18], wday0=row[19], wday1=row[20], hour0=row[21], hour1=row[22], minute0=row[23], minute1=row[24]) for row in fetched]


def update_auth_rule(conn, rule_id=None, rule_ord=None, effect=None, ctc=None, loc_orig=None, loc_dest=None, ckp=None, vhc=None, ctc_grp=None, vhc_grp=None, loc_grp=None, ckp_grp=None, loc_ass=None, year0=None, year1=None, month0=None, month1=None, mday0=None, mday1=None, wday0=None, wday1=None, hour0=None, hour1=None, minute0=None, minute1=None):
    import psycopg2
    sql_query = "update ung.ac_auth_rules set rule_ord=%(rule_ord)s,     effect=%(effect)s,     ctc=%(ctc)s,     loc_orig=%(loc_orig)s,     loc_dest=%(loc_dest)s,     ckp=%(ckp)s,     vhc=%(vhc)s,     ctc_grp=%(ctc_grp)s,     vhc_grp=%(vhc_grp)s,     loc_grp=%(loc_grp)s,     ckp_grp=%(ckp_grp)s,     loc_ass=%(loc_ass)s,     year0=%(year0)s,     year1=%(year1)s,     month0=%(month0)s,     month1=%(month1)s,     mday0=%(mday0)s,     mday1=%(mday1)s,     wday0=%(wday0)s,     wday1=%(wday1)s,     hour0=%(hour0)s,     hour1=%(hour1)s,     minute0=%(minute0)s,     minute1=%(minute1)s where rule_id=%(rule_id)s ;"
    sql_params = dict(rule_id=rule_id, rule_ord=rule_ord, effect=effect, ctc=ctc, loc_orig=loc_orig, loc_dest=loc_dest, ckp=ckp, vhc=vhc, ctc_grp=ctc_grp, vhc_grp=vhc_grp, loc_grp=loc_grp, ckp_grp=ckp_grp, loc_ass=loc_ass, year0=year0, year1=year1, month0=month0, month1=month1, mday0=mday0, mday1=mday1, wday0=wday0, wday1=wday1, hour0=hour0, hour1=hour1, minute0=minute0, minute1=minute1)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_auth_rules_by_ids(conn, rule_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_auth_rules where rule_id in %(rule_ids)s ;"
    sql_params = dict(rule_ids=rule_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_checkpoint(conn, checkpoint_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_checkpoints (checkpoint_name) values (%(checkpoint_name)s) returning checkpoint_id ;"
    sql_params = dict(checkpoint_name=checkpoint_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_checkpoints_by_ids(conn, checkpoint_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_checkpoints where checkpoint_id in %(checkpoint_ids)s ;"
    sql_params = dict(checkpoint_ids=checkpoint_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(checkpoint_id=row[0], checkpoint_name=row[1]) for row in fetched]


def update_checkpoint(conn, checkpoint_id=None, checkpoint_name=None):
    import psycopg2
    sql_query = "update ung.ac_checkpoints set checkpoint_name=(%(checkpoint_name)s) where checkpoint_id = %(checkpoint_id)s ;"
    sql_params = dict(checkpoint_id=checkpoint_id, checkpoint_name=checkpoint_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_checkpoints_by_ids(conn, checkpoint_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_checkpoints where checkpoint_id in %(checkpoint_ids)s ;"
    sql_params = dict(checkpoint_ids=checkpoint_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_checkpoint_group(conn, group_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_checkpoint_groups (group_name) values (%(group_name)s) returning group_name ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def update_checkpoint_group(conn, group_name=None, new_group_name=None):
    import psycopg2
    sql_query = "update ung.ac_checkpoint_groups set group_name=(%(new_group_name)s) where group_name=%(group_name)s ;"
    sql_params = dict(group_name=group_name, new_group_name=new_group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_all_checkpoint_groups(conn):
    import psycopg2
    sql_query = "select * from ung.ac_checkpoint_groups order by group_name asc ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def delete_checkpoint_groups_by_group_names(conn, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_checkpoint_groups where group_name in %(group_names)s ;"
    sql_params = dict(group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def add_checkpoint_group_member(conn, group_name=None, checkpoint_id=None):
    import psycopg2
    sql_query = "insert into ung.ac_checkpoint_groups_x_checkpoints (group_name, checkpoint_id) values (%(group_name)s, %(checkpoint_id)s) ;"
    sql_params = dict(group_name=group_name, checkpoint_id=checkpoint_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_checkpoint_group_members(conn, group_name=None):
    import psycopg2
    sql_query = "select checkpoint_id, checkpoint_name from ung.ac_checkpoint_groups_x_checkpoints ckpg_ckp join ung.ac_checkpoints using(checkpoint_id) where group_name = %(group_name)s ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(checkpoint_id=row[0], checkpoint_name=row[1]) for row in fetched]


def retrieve_checkpoint_groups_by_checkpoint_id(conn, checkpoint_id=None):
    import psycopg2
    sql_query = "select group_name from ung.ac_checkpoint_groups_x_checkpoints where checkpoint_id = %(checkpoint_id)s ;"
    sql_params = dict(checkpoint_id=checkpoint_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def remove_checkpoint_group_members(conn, group_name=None, checkpoint_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_checkpoint_groups_x_checkpoints where group_name = %(group_name)s and checkpoint_id in %(checkpoint_ids)s ;"
    sql_params = dict(group_name=group_name, checkpoint_ids=checkpoint_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def remove_checkpoint_from_checkpoint_groups(conn, checkpoint_id=None, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_checkpoint_groups_x_checkpoints where checkpoint_id = %(checkpoint_id)s and group_name in %(group_names)s ;"
    sql_params = dict(checkpoint_id=checkpoint_id, group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_contact(conn, contact_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_contacts (contact_name) values (%(contact_name)s) returning contact_id ;"
    sql_params = dict(contact_name=contact_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def retrieve_contacts_by_ids(conn, contact_ids=None):
    import psycopg2
    sql_query = "select * from ung.ac_contacts where contact_id in %(contact_ids)s ;"
    sql_params = dict(contact_ids=contact_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(contact_id=row[0], contact_name=row[1]) for row in fetched]


def retrieve_contacts_by_name(conn, contact_name=None, page_pos=None, page_size=None):
    import psycopg2
    sql_query = "select * from ung.ac_contacts where contact_name like %(contact_name)s     and row (contact_name, contact_id) > %(page_pos)s     and contact_id > 0 order by contact_name, contact_id fetch first %(page_size)s rows only; ;"
    sql_params = dict(contact_name=contact_name, page_pos=page_pos, page_size=page_size)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(contact_id=row[0], contact_name=row[1]) for row in fetched]


def update_contact(conn, contact_id=None, contact_name=None):
    import psycopg2
    sql_query = "update ung.ac_contacts set contact_name=(%(contact_name)s) where contact_id = %(contact_id)s ;"
    sql_params = dict(contact_id=contact_id, contact_name=contact_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def delete_contacts_by_ids(conn, contact_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_contacts where contact_id in %(contact_ids)s ;"
    sql_params = dict(contact_ids=contact_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def create_contact_group(conn, group_name=None):
    import psycopg2
    sql_query = "insert into ung.ac_contact_groups (group_name) values (%(group_name)s) returning group_name ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return fetched[0][0]


def update_contact_group(conn, group_name=None, new_group_name=None):
    import psycopg2
    sql_query = "update ung.ac_contact_groups set group_name=(%(new_group_name)s) where group_name=%(group_name)s ;"
    sql_params = dict(group_name=group_name, new_group_name=new_group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_all_contact_groups(conn):
    import psycopg2
    sql_query = "select * from ung.ac_contact_groups order by group_name asc ;"
    sql_params = dict()
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def delete_contact_groups_by_group_names(conn, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_contact_groups where group_name in %(group_names)s ;"
    sql_params = dict(group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def add_contact_group_member(conn, group_name=None, contact_id=None):
    import psycopg2
    sql_query = "insert into ung.ac_contact_groups_x_contacts (group_name, contact_id) values (%(group_name)s, %(contact_id)s) ;"
    sql_params = dict(group_name=group_name, contact_id=contact_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def retrieve_contact_group_members(conn, group_name=None):
    import psycopg2
    sql_query = "select contact_id, contact_name from ung.ac_contact_groups_x_contacts ctcg_ctc join ung.ac_contacts using(contact_id) where group_name = %(group_name)s ;"
    sql_params = dict(group_name=group_name)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(contact_id=row[0], contact_name=row[1]) for row in fetched]


def retrieve_contact_groups_by_contact_id(conn, contact_id=None):
    import psycopg2
    sql_query = "select group_name from ung.ac_contact_groups_x_contacts where contact_id = %(contact_id)s ;"
    sql_params = dict(contact_id=contact_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return [dict(group_name=row[0]) for row in fetched]


def remove_contact_group_members(conn, group_name=None, contact_ids=None):
    import psycopg2
    sql_query = "delete from ung.ac_contact_groups_x_contacts where group_name = %(group_name)s and contact_id in %(contact_ids)s ;"
    sql_params = dict(group_name=group_name, contact_ids=contact_ids)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None


def remove_contact_from_contact_groups(conn, contact_id=None, group_names=None):
    import psycopg2
    sql_query = "delete from ung.ac_contact_groups_x_contacts where contact_id = %(contact_id)s and group_name in %(group_names)s ;"
    sql_params = dict(contact_id=contact_id, group_names=group_names)
    cursor = conn.cursor()
    cursor.execute(sql_query, sql_params)
    try:
        fetched = cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        if str(e) == "no results to fetch":
            fetched = []
    cursor.close()
    return None

