-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.8.0
-- PostgreSQL version: 9.3
-- Project Site: pgmodeler.com.br
-- Model Author: ---


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: dsgtools_admindb | type: DATABASE --
-- -- DROP DATABASE IF EXISTS dsgtools_admindb;
-- CREATE DATABASE dsgtools_admindb
-- ;
-- -- ddl-end --
-- 

-- object: topology | type: SCHEMA --
-- DROP SCHEMA IF EXISTS topology CASCADE;
CREATE SCHEMA topology;
-- ddl-end --
ALTER SCHEMA topology OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,topology;
-- ddl-end --

-- object: postgis | type: EXTENSION --
-- DROP EXTENSION IF EXISTS postgis CASCADE;
CREATE EXTENSION postgis
      WITH SCHEMA public;
-- ddl-end --

-- object: postgis_topology | type: EXTENSION --
-- DROP EXTENSION IF EXISTS postgis_topology CASCADE;
CREATE EXTENSION postgis_topology
      WITH SCHEMA topology;
-- ddl-end --

-- object: "uuid-ossp" | type: EXTENSION --
-- DROP EXTENSION IF EXISTS "uuid-ossp" CASCADE;
CREATE EXTENSION "uuid-ossp"
      WITH SCHEMA public;
-- ddl-end --

-- object: public.permission_profile | type: TABLE --
-- DROP TABLE IF EXISTS public.permission_profile CASCADE;
CREATE TABLE public.permission_profile(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT permissions_pk PRIMARY KEY (id),
	CONSTRAINT unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.permission_profile OWNER TO postgres;
-- ddl-end --

-- object: public.product | type: TABLE --
-- DROP TABLE IF EXISTS public.product CASCADE;
CREATE TABLE public.product(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	inom text NOT NULL,
	mi smallint NOT NULL,
	dboid oid,
	CONSTRAINT product_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.product OWNER TO postgres;
-- ddl-end --

-- object: public.metadata | type: TABLE --
-- DROP TABLE IF EXISTS public.metadata CASCADE;
CREATE TABLE public.metadata(
	admindbversion text
);
-- ddl-end --
ALTER TABLE public.metadata OWNER TO postgres;
-- ddl-end --

-- object: public.admin_log_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS public.admin_log_id_seq CASCADE;
CREATE SEQUENCE public.admin_log_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --
ALTER SEQUENCE public.admin_log_id_seq OWNER TO postgres;
-- ddl-end --

-- object: public.admin_log | type: TABLE --
-- DROP TABLE IF EXISTS public.admin_log CASCADE;
CREATE TABLE public.admin_log(
	id integer NOT NULL DEFAULT nextval('admin_log_id_seq'::regclass),
	logtext text,
	time timestamp DEFAULT now(),
	CONSTRAINT admin_log_pk PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.admin_log OWNER TO postgres;
-- ddl-end --

-- object: public.customization | type: TABLE --
-- DROP TABLE IF EXISTS public.customization CASCADE;
CREATE TABLE public.customization(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT customization_pk PRIMARY KEY (id),
	CONSTRAINT customization_unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.customization OWNER TO postgres;
-- ddl-end --

-- object: public.earth_coverage | type: TABLE --
-- DROP TABLE IF EXISTS public.earth_coverage CASCADE;
CREATE TABLE public.earth_coverage(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT earth_coverage_pk PRIMARY KEY (id),
	CONSTRAINT earth_coverage_unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.earth_coverage OWNER TO postgres;
-- ddl-end --

-- object: public.field_toolbox_config | type: TABLE --
-- DROP TABLE IF EXISTS public.field_toolbox_config CASCADE;
CREATE TABLE public.field_toolbox_config(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT field_toolbox_config_pk PRIMARY KEY (id),
	CONSTRAINT field_toolbox_config_unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.field_toolbox_config OWNER TO postgres;
-- ddl-end --

-- object: public.validation_config | type: TABLE --
-- DROP TABLE IF EXISTS public.validation_config CASCADE;
CREATE TABLE public.validation_config(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT validation_config_pk PRIMARY KEY (id),
	CONSTRAINT validation_config_unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.validation_config OWNER TO postgres;
-- ddl-end --

CREATE TABLE public.style(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	name text,
	jsondict text NOT NULL,
	edgvversion text,
	CONSTRAINT style_config_pk PRIMARY KEY (id),
	CONSTRAINT style_config_unique_name_and_version UNIQUE (name,edgvversion)

);
-- ddl-end --
ALTER TABLE public.style OWNER TO postgres;
-- ddl-end --

CREATE TABLE public.applied_customization(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	id_customization uuid NOT NULL,
	dboid oid NOT NULL,
	CONSTRAINT applied_custom_pk PRIMARY KEY (id),
	CONSTRAINT applied_customization_id_customization_fk FOREIGN KEY (id_customization) REFERENCES public.customization (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
-- ddl-end --
ALTER TABLE public.applied_customization OWNER TO postgres;

CREATE TABLE public.applied_field_toolbox_config(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	id_field_toolbox_config uuid NOT NULL,
	dboid oid NOT NULL,
	CONSTRAINT applied_field_toolbox_config_pk PRIMARY KEY (id),
	CONSTRAINT applied_field_toolbox_config_id_field_toolbox_config_fk FOREIGN KEY (id_field_toolbox_config) REFERENCES public.field_toolbox_config (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
-- ddl-end --
ALTER TABLE public.applied_field_toolbox_config OWNER TO postgres;

CREATE TABLE public.applied_earth_coverage(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	id_earth_coverage uuid NOT NULL,
	dboid oid NOT NULL,
	CONSTRAINT applied_earth_coverage_pk PRIMARY KEY (id),
	CONSTRAINT applied_earth_coverage_id_earth_coverage_config_fk FOREIGN KEY (id_earth_coverage) REFERENCES public.earth_coverage (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
-- ddl-end --
ALTER TABLE public.applied_earth_coverage OWNER TO postgres;

CREATE TABLE public.applied_validation_config(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	id_validation_config uuid NOT NULL,
	dboid oid NOT NULL,
	CONSTRAINT applied_validation_config_pk PRIMARY KEY (id),
	CONSTRAINT applied_validation_config_id_validation_config_fk FOREIGN KEY (id_validation_config) REFERENCES public.validation_config (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
-- ddl-end --
ALTER TABLE public.applied_validation_config OWNER TO postgres;

CREATE TABLE public.applied_style(
	id uuid NOT NULL DEFAULT uuid_generate_v4(),
	id_style uuid NOT NULL,
	dboid oid NOT NULL,
	CONSTRAINT applied_style_pk PRIMARY KEY (id),
	CONSTRAINT applied_style_config_id_style_fk FOREIGN KEY (id_style) REFERENCES public.style (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);
-- ddl-end --
ALTER TABLE public.applied_style OWNER TO postgres;