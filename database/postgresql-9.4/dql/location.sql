/**
 * Creates a new location entry
 *
 * @dialect postgresql
 * @name create_location
 * @param addr_1: string - location address line 1
 * @param addr_2: string - location address line 2
 * @param addr_3: string - location address line 3
 * @param addr_4: string - location address line 4
 * @param addr_5: string - location address line 5
 * @param addr_6: string - location address line 6
 * @retmode scalar
 * @retval location_id: number
 */
{
    insert into ung.ac_locations (addr_1, addr_2, addr_3, addr_4, addr_5, addr_6)
    values (%(addr_1)s, %(addr_2)s, %(addr_3)s, %(addr_4)s, %(addr_5)s, %(addr_6)s)
    returning location_id
    ;
}

/**
 * Retrieves a list of locations matching the given location_id
 *
 * @dialect postgresql
 * @name retrieve_locations_by_ids
 * @param location_ids: list - list of location ids
 * @retmode records
 * @retval location_id: number
 * @retval addr_1: string
 * @retval addr_2: string
 * @retval addr_3: string
 * @retval addr_4: string
 * @retval addr_5: string
 * @retval addr_6: string
 */
{
    select *
    from ung.ac_locations
    where location_id in %(location_ids)s
    ;
}

/**
 * Updates location entry
 *
 * @dialect postgresql
 * @name update_location
 * @param location_id: integer - target location id
 * @param addr_1: string - location address line 1
 * @param addr_2: string - location address line 2
 * @param addr_3: string - location address line 3
 * @param addr_4: string - location address line 4
 * @param addr_5: string - location address line 5
 * @param addr_6: string - location address line 6
 * @retmode none
 */
{
    update ung.ac_locations
    set addr_1=%(addr_1)s,
        addr_2=%(addr_2)s,
        addr_3=%(addr_3)s,
        addr_4=%(addr_4)s,
        addr_5=%(addr_5)s,
        addr_6=%(addr_6)s
    where location_id = %(location_id)s
    ;
}


/**
 * Deletes location entries
 *
 * @dialect postgresql
 * @name delete_locations_by_ids
 * @param location_ids: list - list of location ids
 * @retmode none
 */
{
    delete from ung.ac_locations
    where location_id in %(location_ids)s
    ;
}

/**
 * Creates a new location_group
 *
 * @dialect postgresql
 * @name create_location_group
 * @param group_name: str
 * @retmode scalar
 * @retval group_name: string
 */
{
    insert into ung.ac_location_groups (group_name)
    values (%(group_name)s)
    returning group_name
    ;
}

/**
 * Updates location group
 *
 * @dialect postgresql
 * @name update_location_group
 * @param group_name: string
 * @param new_group_name: string
 * @retmode none
 */
{
    update ung.ac_location_groups
    set group_name=(%(new_group_name)s)
    where group_name=%(group_name)s
    ;
}

/**
 * Retrieves a list of all location groups
 *
 * @dialect postgresql
 * @name retrieve_all_location_groups
 * @retmode records
 * @retval group_name: string
 */
{
    select * from ung.ac_location_groups
    order by group_name asc
    ;
}

/**
 * Deletes location group entries
 *
 * @dialect postgresql
 * @name delete_location_groups_by_group_names
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_location_groups
    where group_name in %(group_names)s
    ;
}

/**
 * Associates a location with a location group
 *
 * @dialect postgresql
 * @name add_location_group_member
 * @param group_name: str
 * @param location_id: number
 * @retmode none
 */
{
    insert into ung.ac_location_groups_x_locations (group_name, location_id)
    values (%(group_name)s, %(location_id)s)
    ;
}

/**
 * Retrieves the list of locations associated with the given group
 *
 * @dialect postgresql
 * @name retrieve_location_group_members
 * @param group_name: str
 * @retmode records
 * @retval location_id: number
 * @retval addr_1: string
 * @retval addr_2: string
 * @retval addr_3: string
 * @retval addr_4: string
 * @retval addr_5: string
 * @retval addr_6: string
 */
{
    select loc.*
    from ung.ac_location_groups_x_locations locg_loc
    join ung.ac_locations loc using(location_id)
    where group_name = %(group_name)s
    ;
}

/**
 * Retrieves the list of location groups the given location is associated with
 *
 * @dialect postgresql
 * @name retrieve_location_groups_by_location_id
 * @param location_id: number
 * @retmode records
 * @retval group_name: number
 */
{
    select group_name from ung.ac_location_groups_x_locations
    where location_id = %(location_id)s
    ;
}

/**
 * Removes locations from the location group
 *
 * @dialect postgresql
 * @name remove_location_group_members
 * @param group_name: string
 * @param location_ids: list
 * @retmode none
 */
{
    delete from ung.ac_location_groups_x_locations
    where group_name = %(group_name)s and location_id in %(location_ids)s
    ;
}

/**
 * Removes the location from the location groups
 *
 * @dialect postgresql
 * @name remove_location_from_location_groups
 * @param location_id: number
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_location_groups_x_locations
    where location_id = %(location_id)s and group_name in %(group_names)s
    ;
}

/**
 * Creates a location assignment type
 *
 * @dialect postgresql
 * @name create_location_assign_type
 * @param assign_type: string - location assignment type
 * @param assign_desc: string - location assignment description
 * @retmode scalar
 * @retval assign_type: string
 */
{
    insert into ung.ac_location_assign_types (assign_type, assign_desc)
    values (%(assign_type)s, %(assign_desc)s)
    returning assign_type
    ;
}

/**
 * Retrieves the list of all location assignment types
 *
 * @dialect postgresql
 * @name retrieve_all_location_assign_types
 * @retmode records
 * @retval assign_type: string
 * @retval assign_desc: string
 */
{
    select *
    from ung.ac_location_assign_types
    order by assign_type asc
    ;
}

/**
 * Updates location assignment type entry
 *
 * @dialect postgresql
 * @name update_location_assign_type
 * @param assign_type: string
 * @param new_assign_type: string
 * @param assign_desc: string
 * @retmode none
 */
{
    update ung.ac_location_assign_types
    set assign_type=%(new_assign_type)s, assign_desc=%(assign_desc)s
    where assign_type = %(assign_type)s
    ;
}

/**
 * Deletes location assignment type entries
 *
 * @dialect postgresql
 * @name delete_location_assign_types_by_assign_types
 * @param assign_types: list
 * @retmode none
 */
{
    delete from ung.ac_location_assign_types
    where assign_type in %(assign_types)s
    ;
}


/**
 * Assigns a contact to a location
 *
 * @dialect postgresql
 * @name assign_contact_to_location
 * @param location_id: number
 * @param contact_id: number
 * @param assign_type: string
 * @retmode none
 */
{
    insert into ung.ac_contacts_x_locations (location_id, contact_id, assign_type)
    values (%(location_id)s, %(contact_id)s, %(assign_type)s)
    ;
}

/**
 * Retrieves the list of contacts assigned to the location
 *
 * @dialect postgresql
 * @name retrieve_location_contact_assignments
 * @param location_id: number
 * @retmode records
 * @retval contact_id: number
 * @retval contact_name: string
 * @retval assign_type: string
 */
{
    select contact_id, contact_name, assign_type
    from ung.ac_contacts_x_locations
    join ung.ac_contacts using(contact_id)
    where location_id = %(location_id)s
    order by contact_name, assign_type
    ;
}

/**
 * Retrieves the list of location assignments for the contact
 *
 * @dialect postgresql
 * @name retrieve_location_contact_assignments_by_contact_id
 * @param contact_id: number
 * @retmode records
 * @retval location_id: number
 * @retval addr_1: string
 * @retval addr_2: string
 * @retval addr_3: string
 * @retval addr_4: string
 * @retval addr_5: string
 * @retval addr_6: string
 * @retval assign_type: string
 */
{
    select loc.*, assign_type
    from ung.ac_contacts_x_locations
    join ung.ac_locations loc using (location_id)
    where contact_id = %(contact_id)s
    order by assign_type
    ;
}

/**
 * Removes a contact location assignment by assignment type
 *
 * @dialect postgresql
 * @name delete_contact_location_assignment
 * @param location_id: number
 * @param contact_id: number
 * @param assign_type: string
 * @retmode none
 */
{
    delete from ung.ac_contacts_x_locations
    where location_id=%(location_id)s and contact_id=%(contact_id)s and assign_type=%(assign_type)s
    ;
}
