
/**
 * Creates a new contact entry
 *
 * @dialect postgresql
 * @name create_contact
 * @param contact_name: str
 * @retmode scalar
 * @retval contact_id: number
 */
{
    insert into ung.ac_contacts (contact_name)
    values (%(contact_name)s)
    returning contact_id
    ;
}

/**
 * Retrieves a list of contacts matching the given contact_id's
 *
 * @dialect postgresql
 * @name retrieve_contacts_by_ids
 * @param contact_ids: list - list of contact ids
 * @retmode records
 * @retval contact_id: number
 * @retval contact_name: string
 */
{
    select *
    from ung.ac_contacts
    where contact_id in %(contact_ids)s
    ;
}

/**
 * Retrieves a list of contacts matching on the contact's name expression
 *
 * @dialect postgresql
 * @name retrieve_contacts_by_name
 * @param contact_name: string
 * @param page_pos: tuple
 * @param page_size: number
 * @retmode records
 * @retval contact_id: number
 * @retval contact_name: string
 */
{
    select *
    from ung.ac_contacts
    where contact_name like %(contact_name)s
        and row (contact_name, contact_id) > %(page_pos)s
        and contact_id > 0
    order by contact_name, contact_id
    fetch first %(page_size)s rows only;
    ;
}

/**
 * Updates contact entry
 *
 * @dialect postgresql
 * @name update_contact
 * @param contact_id: integer
 * @param contact_name: string
 * @retmode none
 */
{
    update ung.ac_contacts
    set contact_name=(%(contact_name)s)
    where contact_id = %(contact_id)s
    ;
}

/**
 * Deletes contact entries
 *
 * @dialect postgresql
 * @name delete_contacts_by_ids
 * @param contact_ids: list - list of contact ids
 * @retmode none
 */
{
    delete from ung.ac_contacts
    where contact_id in %(contact_ids)s
    ;
}

/**
 * Creates a new contact_group
 *
 * @dialect postgresql
 * @name create_contact_group
 * @param group_name: str
 * @retmode scalar
 * @retval group_name: string
 */
{
    insert into ung.ac_contact_groups (group_name)
    values (%(group_name)s)
    returning group_name
    ;
}

/**
 * Updates contact group
 *
 * @dialect postgresql
 * @name update_contact_group
 * @param group_name: string
 * @param new_group_name: string
 * @retmode none
 */
{
    update ung.ac_contact_groups
    set group_name=(%(new_group_name)s)
    where group_name=%(group_name)s
    ;
}

/**
 * Retrieves a list of all contact groups
 *
 * @dialect postgresql
 * @name retrieve_all_contact_groups
 * @retmode records
 * @retval group_name: string
 */
{
    select * from ung.ac_contact_groups
    order by group_name asc
    ;
}

/**
 * Deletes contact group entries
 *
 * @dialect postgresql
 * @name delete_contact_groups_by_group_names
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_contact_groups
    where group_name in %(group_names)s
    ;
}

/**
 * Associates a contact with a contact group
 *
 * @dialect postgresql
 * @name add_contact_group_member
 * @param group_name: str
 * @param contact_id: number
 * @retmode none
 */
{
    insert into ung.ac_contact_groups_x_contacts (group_name, contact_id)
    values (%(group_name)s, %(contact_id)s)
    ;
}

/**
 * Retrieves the list of contacts associated with the given group
 *
 * @dialect postgresql
 * @name retrieve_contact_group_members
 * @param group_name: str
 * @retmode records
 * @retval contact_id: number
 * @retval contact_name: string
 */
{
    select contact_id, contact_name
    from ung.ac_contact_groups_x_contacts ctcg_ctc
    join ung.ac_contacts using(contact_id)
    where group_name = %(group_name)s
    ;
}

/**
 * Retrieves the list of contact groups the given contact is associated with
 *
 * @dialect postgresql
 * @name retrieve_contact_groups_by_contact_id
 * @param contact_id: number
 * @retmode records
 * @retval group_name: number
 */
{
    select group_name from ung.ac_contact_groups_x_contacts
    where contact_id = %(contact_id)s
    ;
}

/**
 * Removes contacts from the contact group
 *
 * @dialect postgresql
 * @name remove_contact_group_members
 * @param group_name: string
 * @param contact_ids: list
 * @retmode none
 */
{
    delete from ung.ac_contact_groups_x_contacts
    where group_name = %(group_name)s and contact_id in %(contact_ids)s
    ;
}

/**
 * Removes the contact from the contact groups
 *
 * @dialect postgresql
 * @name remove_contact_from_contact_groups
 * @param contact_id: number
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_contact_groups_x_contacts
    where contact_id = %(contact_id)s and group_name in %(group_names)s
    ;
}
