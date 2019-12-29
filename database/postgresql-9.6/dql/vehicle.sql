
/**
 * Creates a new vehicle entry
 *
 * @dialect postgresql
 * @name create_vehicle
 * @param plate: str
 * @retmode scalar
 * @retval vehicle_id: number
 */
{
    insert into ung.ac_vehicles (plate)
    values (%(plate)s)
    returning vehicle_id
    ;
}

/**
 * Retrieves a list of vehicles matching the given vehicle_id's
 *
 * @dialect postgresql
 * @name retrieve_vehicles_by_ids
 * @param vehicle_ids: list - list of vehicle ids
 * @retmode records
 * @retval vehicle_id: number
 * @retval plate: string
 */
{
    select *
    from ung.ac_vehicles
    where vehicle_id in %(vehicle_ids)s
    ;
}

/**
 * Updates vehicle entry
 *
 * @dialect postgresql
 * @name update_vehicle
 * @param vehicle_id: integer
 * @param plate: string
 * @retmode none
 */
{
    update ung.ac_vehicles
    set plate=(%(plate)s)
    where vehicle_id = %(vehicle_id)s
    ;
}

/**
 * Deletes vehicle entries
 *
 * @dialect postgresql
 * @name delete_vehicles_by_ids
 * @param vehicle_ids: list - list of vehicle ids
 * @retmode none
 */
{
    delete from ung.ac_vehicles
    where vehicle_id in %(vehicle_ids)s
    ;
}

/**
 * Creates a new vehicle_group
 *
 * @dialect postgresql
 * @name create_vehicle_group
 * @param group_name: str
 * @retmode scalar
 * @retval group_name: string
 */
{
    insert into ung.ac_vehicle_groups (group_name)
    values (%(group_name)s)
    returning group_name
    ;
}

/**
 * Updates vehicle group
 *
 * @dialect postgresql
 * @name update_vehicle_group
 * @param group_name: string
 * @param new_group_name: string
 * @retmode none
 */
{
    update ung.ac_vehicle_groups
    set group_name=(%(new_group_name)s)
    where group_name=%(group_name)s
    ;
}

/**
 * Retrieves a list of all vehicle groups
 *
 * @dialect postgresql
 * @name retrieve_all_vehicle_groups
 * @retmode records
 * @retval group_name: string
 */
{
    select * from ung.ac_vehicle_groups
    order by group_name asc
    ;
}

/**
 * Deletes vehicle group entries
 *
 * @dialect postgresql
 * @name delete_vehicle_groups_by_group_names
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_vehicle_groups
    where group_name in %(group_names)s
    ;
}

/**
 * Associates a vehicle with a vehicle group
 *
 * @dialect postgresql
 * @name add_vehicle_group_member
 * @param group_name: str
 * @param vehicle_id: number
 * @retmode none
 */
{
    insert into ung.ac_vehicle_groups_x_vehicles (group_name, vehicle_id)
    values (%(group_name)s, %(vehicle_id)s)
    ;
}

/**
 * Retrieves the list of vehicles associated with the given group
 *
 * @dialect postgresql
 * @name retrieve_vehicle_group_members
 * @param group_name: str
 * @retmode records
 * @retval vehicle_id: number
 * @retval plate: string
 */
{
    select vehicle_id, plate
    from ung.ac_vehicle_groups_x_vehicles vhcg_vhc
    join ung.ac_vehicles using(vehicle_id)
    where group_name = %(group_name)s
    ;
}

/**
 * Retrieves the list of vehicle groups the given vehicle is associated with
 *
 * @dialect postgresql
 * @name retrieve_vehicle_groups_by_vehicle_id
 * @param vehicle_id: number
 * @retmode records
 * @retval group_name: number
 */
{
    select group_name from ung.ac_vehicle_groups_x_vehicles
    where vehicle_id = %(vehicle_id)s
    ;
}

/**
 * Removes vehicles from the vehicle group
 *
 * @dialect postgresql
 * @name remove_vehicle_group_members
 * @param group_name: string
 * @param vehicle_ids: list
 * @retmode none
 */
{
    delete from ung.ac_vehicle_groups_x_vehicles
    where group_name = %(group_name)s and vehicle_id in %(vehicle_ids)s
    ;
}

/**
 * Removes the vehicle from the vehicle groups
 *
 * @dialect postgresql
 * @name remove_vehicle_from_vehicle_groups
 * @param vehicle_id: number
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_vehicle_groups_x_vehicles
    where vehicle_id = %(vehicle_id)s and group_name in %(group_names)s
    ;
}
