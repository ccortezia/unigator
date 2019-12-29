
/**
 * Creates a new checkpoint entry
 *
 * @dialect postgresql
 * @name create_checkpoint
 * @param checkpoint_name: str
 * @retmode scalar
 * @retval checkpoint_id: number
 */
{
    insert into ung.ac_checkpoints (checkpoint_name)
    values (%(checkpoint_name)s)
    returning checkpoint_id
    ;
}

/**
 * Retrieves a list of checkpoints matching the given checkpoint_id's
 *
 * @dialect postgresql
 * @name retrieve_checkpoints_by_ids
 * @param checkpoint_ids: list - list of checkpoint ids
 * @retmode records
 * @retval checkpoint_id: number
 * @retval checkpoint_name: string
 */
{
    select *
    from ung.ac_checkpoints
    where checkpoint_id in %(checkpoint_ids)s
    ;
}

/**
 * Updates checkpoint entry
 *
 * @dialect postgresql
 * @name update_checkpoint
 * @param checkpoint_id: integer
 * @param checkpoint_name: string
 * @retmode none
 */
{
    update ung.ac_checkpoints
    set checkpoint_name=(%(checkpoint_name)s)
    where checkpoint_id = %(checkpoint_id)s
    ;
}

/**
 * Deletes checkpoint entries
 *
 * @dialect postgresql
 * @name delete_checkpoints_by_ids
 * @param checkpoint_ids: list - list of checkpoint ids
 * @retmode none
 */
{
    delete from ung.ac_checkpoints
    where checkpoint_id in %(checkpoint_ids)s
    ;
}

/**
 * Creates a new checkpoint_group
 *
 * @dialect postgresql
 * @name create_checkpoint_group
 * @param group_name: str
 * @retmode scalar
 * @retval group_name: string
 */
{
    insert into ung.ac_checkpoint_groups (group_name)
    values (%(group_name)s)
    returning group_name
    ;
}

/**
 * Updates checkpoint group
 *
 * @dialect postgresql
 * @name update_checkpoint_group
 * @param group_name: string
 * @param new_group_name: string
 * @retmode none
 */
{
    update ung.ac_checkpoint_groups
    set group_name=(%(new_group_name)s)
    where group_name=%(group_name)s
    ;
}

/**
 * Retrieves a list of all checkpoint groups
 *
 * @dialect postgresql
 * @name retrieve_all_checkpoint_groups
 * @retmode records
 * @retval group_name: string
 */
{
    select * from ung.ac_checkpoint_groups
    order by group_name asc
    ;
}

/**
 * Deletes checkpoint group entries
 *
 * @dialect postgresql
 * @name delete_checkpoint_groups_by_group_names
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_checkpoint_groups
    where group_name in %(group_names)s
    ;
}

/**
 * Associates a checkpoint with a checkpoint group
 *
 * @dialect postgresql
 * @name add_checkpoint_group_member
 * @param group_name: str
 * @param checkpoint_id: number
 * @retmode none
 */
{
    insert into ung.ac_checkpoint_groups_x_checkpoints (group_name, checkpoint_id)
    values (%(group_name)s, %(checkpoint_id)s)
    ;
}

/**
 * Retrieves the list of checkpoints associated with the given group
 *
 * @dialect postgresql
 * @name retrieve_checkpoint_group_members
 * @param group_name: str
 * @retmode records
 * @retval checkpoint_id: number
 * @retval checkpoint_name: string
 */
{
    select checkpoint_id, checkpoint_name
    from ung.ac_checkpoint_groups_x_checkpoints ckpg_ckp
    join ung.ac_checkpoints using(checkpoint_id)
    where group_name = %(group_name)s
    ;
}

/**
 * Retrieves the list of checkpoint groups the given checkpoint is associated with
 *
 * @dialect postgresql
 * @name retrieve_checkpoint_groups_by_checkpoint_id
 * @param checkpoint_id: number
 * @retmode records
 * @retval group_name: number
 */
{
    select group_name from ung.ac_checkpoint_groups_x_checkpoints
    where checkpoint_id = %(checkpoint_id)s
    ;
}

/**
 * Removes checkpoints from the checkpoint group
 *
 * @dialect postgresql
 * @name remove_checkpoint_group_members
 * @param group_name: string
 * @param checkpoint_ids: list
 * @retmode none
 */
{
    delete from ung.ac_checkpoint_groups_x_checkpoints
    where group_name = %(group_name)s and checkpoint_id in %(checkpoint_ids)s
    ;
}

/**
 * Removes the checkpoint from the checkpoint groups
 *
 * @dialect postgresql
 * @name remove_checkpoint_from_checkpoint_groups
 * @param checkpoint_id: number
 * @param group_names: list
 * @retmode none
 */
{
    delete from ung.ac_checkpoint_groups_x_checkpoints
    where checkpoint_id = %(checkpoint_id)s and group_name in %(group_names)s
    ;
}
