
-- Insert mandatory contacts.
insert into ung.ac_contacts (contact_id, contact_name)
values (0, 'SYSTEM')
;

-- Insert mandatory locations.
insert into ung.ac_locations (location_id, addr_1)
values (0, 'EXTERIOR')
;

-- Insert mandatory authorization levels.
insert into ung.ac_auth_levels (auth_name, auth_grant)
values ('sys/none', false)
;

-- Insert mandatory authorization flows.
insert into ung.ac_auth_flows (auth_flow_id, init_st, auth_flow_desc)
values (0, 'sys/none', 'Base Authorization Flow')
;

-- Initialize authorization flows settings.
insert into ung.ac_settings (active_flow)
values (0)
;
