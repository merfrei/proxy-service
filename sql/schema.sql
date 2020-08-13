CREATE TABLE users (
       id serial PRIMARY KEY,
       username varchar(32) UNIQUE NOT NULL,
       password varchar(128) NOT NULL);

CREATE TABLE proxy_types (
       id serial PRIMARY KEY,
       name varchar(20) UNIQUE NOT NULL,
       code varchar(4) UNIQUE NOT NULL);

CREATE TABLE proxy_locations (
       id serial PRIMARY KEY,
       name varchar(256) UNIQUE NOT NULL,
       code varchar(4) UNIQUE NOT NULL);

CREATE TABLE providers (
       id serial PRIMARY KEY,
       name varchar(256) UNIQUE NOT NULL,
       url varchar(1024),
       code varchar(8) UNIQUE NOT NULL);

CREATE TABLE provider_plans (
       id serial PRIMARY KEY,
       provider_id integer NOT NULL REFERENCES providers (id) ON DELETE CASCADE,
       name varchar(256) NOT NULL,
       code varchar(8) UNIQUE NOT NULL,
       UNIQUE (provider_id, name));

CREATE INDEX provider_plans_provider_id_ix ON provider_plans (provider_id);
CREATE INDEX provider_plans_name_ix ON provider_plans (name);

CREATE TABLE proxies (
       id serial PRIMARY KEY,
       url varchar(1024) UNIQUE NOT NULL,
       active boolean DEFAULT TRUE,
       proxy_type_id integer NOT NULL REFERENCES proxy_types (id) ON DELETE RESTRICT,
       proxy_location_id integer REFERENCES proxy_locations (id) ON DELETE SET NULL,
       provider_id integer REFERENCES providers (id) ON DELETE SET NULL,
       provider_plan_id integer REFERENCES provider_plans (id) ON DELETE SET NULL,
       tor_control_port integer,
       tor_control_pswd text,
       tor_renew_identity boolean DEFAULT FALSE,
       dont_block boolean DEFAULT FALSE);

CREATE INDEX proxies_proxy_type_id_ix ON proxies (proxy_type_id);
CREATE INDEX proxies_proxy_location_id_ix ON proxies (proxy_location_id) WHERE proxy_location_id IS NOT NULL;
CREATE INDEX proxies_proxy_provider_id_ix ON proxies (provider_id) WHERE provider_id IS NOT NULL;
CREATE INDEX proxies_provider_plan_id_ix ON proxies (provider_plan_id) WHERE provider_plan_id IS NOT NULL;

CREATE TABLE targets (
       id serial PRIMARY KEY,
       domain varchar(1024) UNIQUE NOT NULL,
       identifier varchar(1024) UNIQUE,
       blocked_standby integer NOT NULL DEFAULT 720);

CREATE TABLE target_providers (
       id serial PRIMARY KEY,
       target_id integer NOT NULL REFERENCES targets (id) ON DELETE CASCADE,
       provider_id integer NOT NULL REFERENCES providers (id) ON DELETE CASCADE);

CREATE INDEX target_providers_target_id_ix ON target_providers (target_id);

CREATE TABLE target_provider_plans (
       id serial PRIMARY KEY,
       target_id integer NOT NULL REFERENCES targets (id) ON DELETE CASCADE,
       provider_plan_id integer NOT NULL REFERENCES provider_plans (id) ON DELETE CASCADE);

CREATE INDEX target_provider_plans_target_id_ix ON target_provider_plans (target_id);


-- Views

CREATE VIEW provider_plans_view AS
    SELECT plan.id, plan.code, plan.provider_id, prov.name as "provider_desc", plan.name
    FROM provider_plans plan JOIN providers prov ON (plan.provider_id = prov.id);

CREATE VIEW proxies_view AS
    SELECT
        proxy.id, proxy.url, proxy.active, CASE WHEN proxy.active THEN 'Yes' ELSE 'No' END active_desc,
        proxy.proxy_type_id, ptype.name as "type_desc", proxy.proxy_location_id, ploc.name as "location_desc",
        proxy.provider_id, pprov.name as "provider_name", proxy.provider_plan_id, pplan.name as "plan_desc",
        proxy.dont_block
    FROM
        proxies proxy JOIN proxy_types ptype ON (proxy.proxy_type_id = ptype.id)
                      JOIN proxy_locations ploc ON (proxy.proxy_location_id = ploc.id)
                      JOIN providers pprov ON (proxy.provider_id = pprov.id)
                      JOIN provider_plans pplan ON (proxy.provider_plan_id = pplan.id);
