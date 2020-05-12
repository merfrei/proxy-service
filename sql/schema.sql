CREATE TABLE proxy_types (
       id serial PRIMARY KEY,
       name varchar(20) UNIQUE NOT NULL);

CREATE TABLE proxy_locations (
       id serial PRIMARY KEY,
       name varchar(8) UNIQUE NOT NULL);

CREATE TABLE proxy_providers (
       id serial PRIMARY KEY,
       name varchar(256) UNIQUE NOT NULL,
       url varchar(1024));

CREATE TABLE provider_plans (
       id serial PRIMARY KEY,
       provider_id integer NOT NULL REFERENCES proxy_providers (id) ON DELETE CASCADE,
       name varchar(256) NOT NULL,
       UNIQUE (provider_id, name));

CREATE INDEX provider_plans_provider_id_ix ON provider_plans (provider_id);
CREATE INDEX provider_plans_name_ix ON provider_plans (name);

CREATE TABLE proxies (
       id serial PRIMARY KEY,
       url varchar(1024) UNIQUE NOT NULL,
       active boolean DEFAULT TRUE,
       proxy_type_id integer NOT NULL REFERENCES proxy_types (id) ON DELETE RESTRICT,
       proxy_location_id integer REFERENCES proxy_locations (id) ON DELETE SET NULL,
       proxy_provider_id integer REFERENCES proxy_providers (id) ON DELETE SET NULL,
       provider_plan_id integer REFERENCES provider_plans (id) ON DELETE SET NULL,
       tor_control_port integer,
       tor_control_pswd integer,
       tor_renew_identity boolean DEFAULT FALSE);

CREATE INDEX proxies_proxy_type_id_ix ON proxies (proxy_type_id);
CREATE INDEX proxies_proxy_location_id_ix ON proxies (proxy_location_id) WHERE proxy_location_id IS NOT NULL;
CREATE INDEX proxies_proxy_provider_id_ix ON proxies (proxy_provider_id) WHERE proxy_provider_id IS NOT NULL;
CREATE INDEX proxies_provider_plan_id_ix ON proxies (provider_plan_id) WHERE provider_plan_id IS NOT NULL;

CREATE TABLE targets (
       id serial PRIMARY KEY,
       domain varchar(1024) UNIQUE NOT NULL,
       identifier varchar(1024) UNIQUE,
       blocked_standby integer NOT NULL DEFAULT 720);
