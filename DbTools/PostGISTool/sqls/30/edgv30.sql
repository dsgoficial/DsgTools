SET check_function_bodies = false;
CREATE SCHEMA IF NOT EXISTS topology;
ALTER SCHEMA topology OWNER TO postgres;
CREATE SCHEMA dominios;
CREATE SCHEMA complexos;
ALTER SCHEMA complexos OWNER TO postgres;
CREATE SCHEMA cb;
CREATE SCHEMA cc;
CREATE SCHEMA ct;
SET search_path TO pg_catalog,public,topology,dominios,complexos,cb,cc,ct;
CREATE EXTENSION IF NOT EXISTS postgis
      WITH SCHEMA public
      VERSION '2.0.4';
COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';
CREATE EXTENSION IF NOT EXISTS postgis_topology
      WITH SCHEMA topology
      VERSION '2.0.4';
COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';
CREATE TABLE cb.hid_area_umida_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipoareaumida smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_area_umida_a_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_area_umida_a_geom_1408997021488 ON cb.hid_area_umida_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_area_umida_a OWNER TO postgres;
CREATE TABLE cb.hid_banco_areia(
	id serial NOT NULL,
	tipobanco smallint,
	nome varchar(80),
	geometriaaproximada smallint,
	situacaoemagua smallint,
	materialpredominante smallint,
	CONSTRAINT hid_banco_areia_l_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_banco_areia OWNER TO postgres;
CREATE TABLE cb.hid_recife(
	tiporecife smallint NOT NULL DEFAULT 0,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	situacaoemagua smallint NOT NULL DEFAULT 0,
	situacaocosta smallint NOT NULL DEFAULT 0,
	id serial NOT NULL,
	CONSTRAINT hid_recife_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_recife OWNER TO postgres;
CREATE TABLE cb.hid_barragem(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	matconstr smallint NOT NULL DEFAULT 0,
	usoprincipal smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 1,
	situacaofisica smallint NOT NULL DEFAULT 5,
	id_enc_complexo_gerad_energ_eletr uuid,
	CONSTRAINT hid_barragem_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_barragem OWNER TO postgres;
CREATE TABLE cb.hid_comporta(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint,
	operacional smallint,
	situacaofisica smallint,
	CONSTRAINT hid_comporta_p_pkey PRIMARY KEY (id)
)WITH ( OIDS = TRUE );
ALTER TABLE cb.hid_comporta OWNER TO postgres;
CREATE TABLE cb.hid_queda_dagua(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipoqueda smallint NOT NULL DEFAULT 0,
	alturaaproximada real,
	CONSTRAINT hid_queda_dagua_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_queda_dagua OWNER TO postgres;
CREATE TABLE cb.hid_corredeira(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	CONSTRAINT hid_corredeira_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_corredeira OWNER TO postgres;
CREATE TABLE cb.hid_dique(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	matconstr smallint NOT NULL DEFAULT 0,
	CONSTRAINT hid_dique_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_dique OWNER TO postgres;
CREATE TABLE cb.hid_dique_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_dique_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_dique)
;
CREATE INDEX hid_dique_a_geom_1408997017153 ON cb.hid_dique_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_dique_a OWNER TO postgres;
CREATE TABLE cb.hid_fonte_dagua_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipofontedagua smallint NOT NULL,
	qualidagua smallint NOT NULL,
	regime smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_fonte_dagua_p_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_fonte_dagua_p_geom_1408997017228 ON cb.hid_fonte_dagua_p
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_fonte_dagua_p OWNER TO postgres;
CREATE TABLE cb.hid_foz_maritima(
	id serial NOT NULL,
	nome character(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	CONSTRAINT hid_foz_maritima_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_foz_maritima OWNER TO postgres;
CREATE TABLE cb.rel_elemento_fisiografico(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	CONSTRAINT rel_elemento_fisiografico_pk PRIMARY KEY (id)
);
CREATE TABLE cb.hid_limite_massa_dagua_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipolimmassa smallint NOT NULL,
	materialpredominante smallint NOT NULL DEFAULT 0,
	revestida smallint NOT NULL DEFAULT 0,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_limite_massa_dagua_l_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_limite_massa_dagua_l_geom_140899701845 ON cb.hid_limite_massa_dagua_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_limite_massa_dagua_l OWNER TO postgres;
CREATE TABLE cb.hid_massa_dagua_a(
	id serial NOT NULL,
	nome character(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipomassadagua smallint NOT NULL,
	regime smallint,
	salinidade smallint NOT NULL,
	dominialidade smallint,
	artificial smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_massa_dagua_a_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_massa_dagua_a_geom_1408997018171 ON cb.hid_massa_dagua_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_massa_dagua_a OWNER TO postgres;
CREATE TABLE cb.hid_ponto_drenagem_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint,
	relacionado smallint,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_ponto_drenagem_p_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_ponto_drenagem_p_geom_1408997018772 ON cb.hid_ponto_drenagem_p
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_ponto_drenagem_p OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe(
	id serial NOT NULL,
	tipoquebramolhe smallint NOT NULL DEFAULT 0,
	nome character(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	matconstr smallint NOT NULL DEFAULT 0,
	situacaoemagua smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT hid_quebramar_molhe_a_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_quebramar_molhe OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_quebramar_molhe_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_quebramar_molhe)
;
CREATE INDEX hid_quebramar_molhe_l_geom_1408997019419 ON cb.hid_quebramar_molhe_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_quebramar_molhe_l OWNER TO postgres;
CREATE TABLE cb.hid_queda_dagua_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_queda_dagua_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE INDEX hid_queda_dagua_p_gist ON cb.hid_queda_dagua_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_recife_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_recife_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
CREATE INDEX hid_recife_p_gist ON cb.hid_recife_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_rocha_em_agua(
	id serial NOT NULL,
	nome varchar(80) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	situacaoemagua smallint NOT NULL DEFAULT 0,
	alturalamina real,
	CONSTRAINT hid_rocha_em_agua_p_pkey PRIMARY KEY (id)
);
ALTER TABLE cb.hid_rocha_em_agua OWNER TO postgres;
CREATE TABLE cb.hid_rocha_em_agua_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_rocha_em_agua_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_rocha_em_agua)
;
CREATE INDEX hid_rocha_em_agua_p_1 ON cb.hid_rocha_em_agua_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_reservatorio_hidrico_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint,
	usoprincipal smallint,
	volumeutil smallint,
	namaximomaximorum smallint,
	namaximooperacional smallint,
	id_enc_complexo_gerad_energ_eletr uuid NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_reservatorio_hidrico_a_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_reservatorio_hidrico_a_geom_1408997020482 ON cb.hid_reservatorio_hidrico_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_reservatorio_hidrico_a OWNER TO postgres;
CREATE TABLE cb.hid_trecho_massa_dagua_a(
	tipotrechomassadagua smallint NOT NULL DEFAULT 1,
	CONSTRAINT hid_trecho_massa_dagua_a_check_tipomassadagua_8 CHECK (tipomassadagua = 8),
	CONSTRAINT hid_trecho_massa_dagua_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_massa_dagua_a)
;
ALTER TABLE cb.hid_trecho_massa_dagua_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_barragem_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE INDEX hid_barragem_p_gist ON cb.hid_barragem_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_sumidouro_vertedouro_p(
	id serial NOT NULL,
	nome varchar(80) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tiposumvert smallint NOT NULL,
	causa smallint NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_sumidouro_vertedouro_p_pkey PRIMARY KEY (id)
)WITH ( OIDS = TRUE );
CREATE INDEX hid_sumidouro_vertedouro_p_geom_1408997020972 ON cb.hid_sumidouro_vertedouro_p
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_sumidouro_vertedouro_p OWNER TO postgres;
CREATE TABLE cb.hid_terreno_suj_inundacao_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	periodicidadeinunda character(20),
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_terreno_sujeito_inundacao_a_pkey PRIMARY KEY (id),
	CONSTRAINT hid_terreno_sujeito_inundacao_a_check_geomaprox_sim CHECK (geometriaaproximada = 1)
);
CREATE INDEX hid_terreno_sujeito_inundacao_a_geom_140899702189 ON cb.hid_terreno_suj_inundacao_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_terreno_suj_inundacao_a OWNER TO postgres;
CREATE TABLE cb.hid_trecho_drenagem_l(
	id serial NOT NULL,
	nome character(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipotrechodrenagem smallint NOT NULL DEFAULT 1,
	navegavel smallint NOT NULL DEFAULT 0,
	regime smallint NOT NULL DEFAULT 0,
	larguramedia real,
	encoberto smallint NOT NULL DEFAULT 2,
	geom geometry(LINESTRING, 4326) NOT NULL,
	dentrodepoligono smallint NOT NULL DEFAULT 2,
	CONSTRAINT hid_trecho_drenagem_l_pkey PRIMARY KEY (id)
);
CREATE INDEX hid_trecho_drenagem_l_geom_1408997021361 ON cb.hid_trecho_drenagem_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_trecho_drenagem_l OWNER TO postgres;
CREATE TABLE cb.hid_dique_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_dique_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_dique)
;
CREATE INDEX hid_dique_l_geom_1408997017169 ON cb.hid_dique_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_dique_l OWNER TO postgres;
CREATE TABLE cb.hid_dique_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_dique_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_dique)
;
CREATE INDEX hid_dique_p_geom_1408997017188 ON cb.hid_dique_p
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_dique_p OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_quebramar_molhe_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_quebramar_molhe)
;
CREATE INDEX hid_quebramar_molhe_a_geom_1408997019255 ON cb.hid_quebramar_molhe_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_quebramar_molhe_a OWNER TO postgres;
CREATE TABLE cb.hid_banco_areia_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_banco_areia_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_banco_areia)
;
CREATE INDEX hid_banco_areia_l_gist ON cb.hid_banco_areia_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_banco_areia_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_banco_areia_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_banco_areia)
;
CREATE INDEX hid_banco_areia_a_geom_1408997016227 ON cb.hid_banco_areia_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_banco_areia_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_barragem_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE INDEX hid_barragem_l_gist ON cb.hid_barragem_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_recife_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_recife_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
CREATE INDEX hid_recife_l_gist ON cb.hid_recife_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_recife_l OWNER TO postgres;
CREATE TABLE cb.hid_recife_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_recife_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
CREATE INDEX hid_recife_a_gist ON cb.hid_recife_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_recife_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_barragem_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE INDEX hid_barragem_a_gist ON cb.hid_barragem_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_rocha_em_agua_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_rocha_em_agua_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_rocha_em_agua)
;
CREATE INDEX hid_rocha_em_agua_a_gist ON cb.hid_rocha_em_agua_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_rocha_em_agua_a OWNER TO postgres;
CREATE TABLE cb.rel_elemento_fisiog_natural(
	tipoelemnat smallint NOT NULL DEFAULT 99,
	CONSTRAINT rel_elemento_fisiog_natural_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiografico)
;
CREATE TABLE cb.rel_elemento_fisiog_natural_p(
	geom geometry(POINT, 4326) NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE INDEX rel_elemento_fisiog_natural_p_gist ON cb.rel_elemento_fisiog_natural_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_comporta_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_comporta_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_comporta)
;
CREATE INDEX hid_comporta_p_gist ON cb.hid_comporta_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_queda_dagua_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_queda_dagua_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE INDEX hid_queda_dagua_l_gist ON cb.hid_queda_dagua_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_queda_dagua_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_queda_dagua_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE INDEX hid_queda_dagua_a_gist ON cb.hid_queda_dagua_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_corredeira_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_corredeira_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE INDEX hid_corredeira_p_gist ON cb.hid_corredeira_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_corredeira_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_corredeira_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE INDEX hid_corredeira_l_gist ON cb.hid_corredeira_l
	USING btree
	(
	  geom
	);
CREATE TABLE cb.hid_comporta_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_comporta_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_comporta)
;
CREATE INDEX hid_comporta_l_geom_1408997016713 ON cb.hid_comporta_l
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_comporta_l OWNER TO postgres;
CREATE TABLE cb.hid_corredeira_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_corredeira_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE INDEX hid_corredeira_a_gist ON cb.hid_corredeira_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_ponto_inicio_drenagem_p(
	nascente smallint NOT NULL DEFAULT 0,
	CONSTRAINT hid_ponto_inicio_drenagem_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_ponto_drenagem_p)
;
CREATE TABLE cb.hid_confluencia_p(
	a smallint,
	CONSTRAINT hid_confluencia_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_ponto_drenagem_p)
;
CREATE TABLE cb.hid_foz_maritima_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hid_foz_maritima_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE INDEX hid_foz_maritima_p_gist ON cb.hid_foz_maritima_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_foz_maritima_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hid_foz_maritima_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE INDEX hid_foz_maritima_l_gist ON cb.hid_foz_maritima_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hid_foz_maritima_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hid_foz_maritima_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE INDEX hid_foz_maritima_a_gist ON cb.hid_foz_maritima_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.veg_vegetacao_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipoveg smallint NOT NULL DEFAULT 0,
	classificacaoporte smallint NOT NULL DEFAULT 0,
	densidade smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_area_verde uuid,
	CONSTRAINT veg_vegetacao_a_pk PRIMARY KEY (id)
);
CREATE INDEX veg_vegetacao_a_gist ON cb.veg_vegetacao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.veg_veg_cultivada_a(
	tipolavoura smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL DEFAULT 0,
	terreno smallint NOT NULL,
	cultivopredominante smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_veg_cultivada_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_reflorestamento_a(
	espacamentoindividuos float,
	espessura float,
	alturamediaindividuos float,
	CONSTRAINT veg_reflorestamento_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_cultivada_a)
;
CREATE TABLE cb.veg_veg_natural_a(
	antropizada smallint NOT NULL DEFAULT 0,
	secundaria smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_veg_natural_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_veg_area_contato(
	a smallint,
	CONSTRAINT veg_veg_area_contato_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_campo_a(
	tipocampo smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_campo_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_cerrado_a(
	vereda smallint NOT NULL,
	CONSTRAINT veg_cerrado_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_caatinga_a(
	a smallint,
	CONSTRAINT veg_caatinga_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_campinarana_a(
	a smallint,
	CONSTRAINT veg_campinarana_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_veg_restinga_a(
	a smallint,
	CONSTRAINT veg_veg_restinga_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_mangue_a(
	tipomanguezal smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_mangue_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_natural_a)
;
CREATE TABLE cb.veg_brejo_pantano_a(
	predominanciapalmeiras smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_brejo_pantano_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_floresta_a(
	especiepredominante smallint NOT NULL DEFAULT 0,
	CONSTRAINT veg_floresta_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.rel_isolinha_hipsometrica(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	CONSTRAINT rel_isolinha_hipsometrica_pk PRIMARY KEY (id)
);
CREATE TABLE cb.rel_curva_nivel_l(
	cota integer NOT NULL,
	depressao smallint NOT NULL DEFAULT 2,
	tipocurvanivel smallint NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rel_curva_nivel_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_isolinha_hipsometrica)
;
CREATE INDEX rel_curva_nivel_l_gist ON cb.rel_curva_nivel_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_curva_batimetrica_l(
	profundidade integer,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rel_curva_batimetrica_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_isolinha_hipsometrica)
;
CREATE TABLE cb.rel_terreno_exposto_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipoterrexp smallint NOT NULL DEFAULT 0,
	causaexposicao smallint NOT NULL DEFAULT 0
);
CREATE TABLE cb.rel_terreno_erodido(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	situacaoterreno smallint NOT NULL DEFAULT 0,
	tipoerosao smallint NOT NULL DEFAULT 0,
	CONSTRAINT rel_terreno_erodido_1 PRIMARY KEY (id)
);
CREATE TABLE cb.rel_terreno_erodido_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT rel_terreno_erodido_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_terreno_erodido)
;
CREATE INDEX rel_terreno_erodido_p_gist ON cb.rel_terreno_erodido_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_terreno_erodido_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rel_terreno_erodido_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_terreno_erodido)
;
CREATE INDEX rel_terreno_erodido_l_gist ON cb.rel_terreno_erodido_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_terreno_erodido_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT rel_terreno_erodido_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_terreno_erodido)
;
CREATE INDEX rel_terreno_erodido_a_gist ON cb.rel_terreno_erodido_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_ponto_hipsometrico(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	CONSTRAINT rel_ponto_hipsometrico_pk PRIMARY KEY (id)
);
CREATE TABLE cb.rel_ponto_cotado_batimetrico_p(
	profundidade float,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT rel_ponto_cotado_batimetrico_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_ponto_hipsometrico)
;
CREATE INDEX rel_ponto_cotado_batimetrico_p_gist ON cb.rel_ponto_cotado_batimetrico_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_ponto_cotado_altimetrico_p(
	cotacomprovada smallint NOT NULL DEFAULT 2,
	cota float,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT rel_ponto_cotado_altimetrico_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_ponto_hipsometrico)
;
CREATE INDEX rel_ponto_cotado_altimetrico_p_gist ON cb.rel_ponto_cotado_altimetrico_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_alter_fisiog_antropica(
	tipoalterantrop smallint NOT NULL DEFAULT 0,
	CONSTRAINT rel_alter_fisiog_antropica_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiografico)
;
CREATE TABLE cb.rel_elemento_fisiog_natural_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rel_elemento_fisiog_natural_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE INDEX rel_elemento_fisiog_natural_l_gist ON cb.rel_elemento_fisiog_natural_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_elemento_fisiog_natural_a(
	geom geometry(POLYGON, 4326) NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE INDEX rel_elemento_fisiog_natural_a_gist ON cb.rel_elemento_fisiog_natural_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_alter_fisiog_antropica_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT rel_alter_fisiog_antropica_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica)
;
CREATE INDEX rel_alter_fisiog_antropica_p_gist ON cb.rel_alter_fisiog_antropica_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_alter_fisiog_antropica_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rel_alter_fisiog_antropica_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica)
;
CREATE INDEX rel_alter_fisiog_antropica_l_gist ON cb.rel_alter_fisiog_antropica_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rel_alter_fisiog_antropica_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT rel_alter_fisiog_antropica_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica)
;
CREATE INDEX rel_alter_fisiog_antropica_a_gist ON cb.rel_alter_fisiog_antropica_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_ext_mineral_p(
	secaoativecon smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipoextmin smallint NOT NULL,
	tipoproduto smallint NOT NULL,
	tipopocomina smallint NOT NULL,
	procextracao smallint NOT NULL,
	atividade smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_p)
;
CREATE TABLE cb.eco_ext_mineral_l(
	secaoativecon smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipoextmin smallint NOT NULL,
	tipoproduto smallint NOT NULL,
	tipopocomina smallint NOT NULL,
	procextracao smallint NOT NULL,
	atividade smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_l)
;
CREATE TABLE cb.eco_ext_mineral_a(
	secaoativecon smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipoextmin smallint NOT NULL,
	tipoproduto smallint NOT NULL,
	tipopocomina smallint NOT NULL,
	procextracao smallint NOT NULL,
	atividade smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_a)
;
CREATE TABLE cb.rel_corte_p(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_corte_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_p)
;
CREATE TABLE cb.rel_duna_p(
	fixa smallint NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.rel_corte_l(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_corte_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_l)
;
CREATE TABLE cb.rel_gruta_caverna_p(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.rel_corte_a(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_corte_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_a)
;
CREATE TABLE cb.rel_aterro_p(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_aterro_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_p)
;
CREATE TABLE cb.rel_aterro_l(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_aterro_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_l)
;
CREATE TABLE cb.rel_aterro_a(
	matconstr smallint NOT NULL,
	CONSTRAINT rel_aterro_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_a)
;
CREATE TABLE cb.hid_canal_l(
	usoprincipal smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL,
	CONSTRAINT hid_canal_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_l)
;
CREATE TABLE cb.hid_canal_a(
	usoprincipal smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL,
	CONSTRAINT hid_canal_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_a)
;
CREATE TABLE cb.hid_vala_l(
	usoprincipal smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL,
	CONSTRAINT hid_vala_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_l)
;
CREATE TABLE cb.hid_vala_a(
	usoprincipal smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL,
	CONSTRAINT hid_vala_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica_a)
;
CREATE TABLE complexos.hid_arquipelago(
	id uuid NOT NULL,
	nome varchar(80),
	jurisdicao smallint NOT NULL,
	CONSTRAINT hid_arquipelago_pk PRIMARY KEY (id)
);
CREATE TABLE cc.edf_edificacao(
	id serial NOT NULL,
	nome varchar(80),
	numero integer,
	bloco varchar(80),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	matconstr smallint NOT NULL,
	numeropavimentos integer,
	alturaaproximada float,
	turistica smallint NOT NULL,
	cultura smallint NOT NULL,
	id_complexo_habitacional uuid,
	id_area_subnormal uuid,
	CONSTRAINT "EDF_Edificacao_pk" PRIMARY KEY (id)
);
CREATE TABLE cc.edf_edificacao_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT edf_edificacao_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao)
;
CREATE INDEX edf_edificacao_p_gist ON cc.edf_edificacao_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.edf_edificacao_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT edf_edificacao_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao)
;
CREATE INDEX edf_edificacao_a_1 ON cc.edf_edificacao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.edf_hab_indigena_p(
	coletiva smallint NOT NULL DEFAULT 0,
	isolada smallint NOT NULL DEFAULT 0,
	CONSTRAINT edf_hab_indigena_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_residencial_p(
	a smallint
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_abast_agua_p(
	tipoedifabast smallint NOT NULL DEFAULT 0,
	id_complexo_abast_agua uuid
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_saneamento_p(
	tipoedifsaneam smallint NOT NULL DEFAULT 0,
	id_complexo_saneamento uuid
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_ensino_p(
	classeativecon smallint NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT edf_edif_ensino_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_saude_p(
	classeativecon smallint NOT NULL,
	nivelatencao smallint NOT NULL,
	id_org_saude uuid,
	CONSTRAINT edf_edif_saude_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_servico_social_p(
	classeativecon smallint NOT NULL,
	id_org_servico_social uuid,
	CONSTRAINT edf_edif_servico_social_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cb.rel_gruta_caverna_l(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
CREATE TABLE cc.edf_edif_residencial_a(
	a smallint,
	CONSTRAINT edf_edif_residencial_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cb.rel_gruta_caverna_a(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cb.rel_rocha_l(
	formarocha smallint NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
CREATE TABLE cc.edf_edif_abast_agua_a(
	tipoedifabast smallint NOT NULL DEFAULT 0,
	id_complexo_abast_agua uuid NOT NULL,
	CONSTRAINT edf_edif_abast_agua_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cb.rel_pico_p(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.hid_ilha_p(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
ALTER TABLE cb.hid_ilha_p OWNER TO postgres;
CREATE TABLE cb.hid_ilha_l(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
ALTER TABLE cb.hid_ilha_l OWNER TO postgres;
CREATE TABLE cb.hid_ilha_a(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
ALTER TABLE cb.hid_ilha_a OWNER TO postgres;
CREATE TABLE cb.rel_rocha_a(
	formarocha smallint NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cc.edf_edif_saneamento_a(
	tipoedifsaneam smallint NOT NULL DEFAULT 0,
	id_complexo_saneamento uuid,
	CONSTRAINT edf_edif_saneamento_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cb.rel_rocha_p(
	formarocha smallint NOT NULL DEFAULT 0
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.rel_dolina_a(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cc.edf_hab_indigena_a(
	coletiva smallint NOT NULL DEFAULT 0,
	isolada smallint NOT NULL DEFAULT 0,
	CONSTRAINT edf_hab_indigena_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_ensino_a(
	classeativecon smallint NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT edf_edif_ensino_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_saude_a(
	classeativecon smallint NOT NULL,
	nivelatencao smallint NOT NULL,
	id_org_saude uuid,
	CONSTRAINT edf_edif_saude_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cb.rel_duna_l(
	fixa smallint NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
CREATE TABLE cc.edf_edif_servico_social_a(
	classeativecon smallint NOT NULL,
	id_org_servico_social uuid,
	CONSTRAINT edf_edif_servico_social_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cb.rel_duna_a(
	fixa smallint NOT NULL
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cb.rel_dolina_l(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
CREATE TABLE cb.rel_dolina_p(
	a smallint
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cc.edf_edif_pub_militar_p(
	tipousoedif smallint NOT NULL DEFAULT 0,
	jurisdicao smallint NOT NULL,
	tipoinstalmilitar smallint NOT NULL DEFAULT 0,
	organizacao varchar(80),
	CONSTRAINT edf_edif_pub_militar_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_pub_militar_a(
	tipousoedif smallint NOT NULL DEFAULT 0,
	jurisdicao smallint NOT NULL,
	tipoinstalmilitar smallint NOT NULL DEFAULT 0,
	organizacao varchar(80),
	CONSTRAINT edf_edif_pub_militar_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_posto_policia_militar_p(
	a smallint,
	CONSTRAINT edf_posto_policia_militar_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edif_pub_militar_p)
;
CREATE TABLE cc.edf_posto_policia_militar_a(
	a smallint,
	CONSTRAINT edf_posto_policia_militar_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edif_pub_militar_a)
;
CREATE TABLE cc.edf_representacao_diplomatica_p(
	tiporepdiplomatica smallint NOT NULL,
	CONSTRAINT edf_representacao_diplomatica_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_representacao_diplomatica_a(
	tiporepdiplomatica smallint NOT NULL,
	CONSTRAINT edf_representacao_diplomatica_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_pub_civil_p(
	tipousoedif smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	organizacao varchar(80) NOT NULL,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_pub_civil_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_pub_civil_a(
	tipousoedif smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	organizacao varchar(80) NOT NULL,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_pub_civil_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_posto_policia_rod_federal_p(
	a smallint,
	CONSTRAINT edf_posto_policia_rod_federal_p_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_p)
;
CREATE TABLE cc.edf_posto_policia_rod_federal_a(
	a smallint,
	CONSTRAINT edf_posto_policia_rod_federal_a_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_a)
;
CREATE TABLE cc.edf_edif_policia_p(
	a smallint,
	CONSTRAINT edf_edif_policia_p_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_p)
;
CREATE TABLE cc.edf_edif_policia_a(
	a smallint,
	CONSTRAINT edf_edif_policia_a_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_a)
;
CREATE TABLE cc.edf_posto_guarda_municipal_p(
	a smallint,
	CONSTRAINT edf_posto_guarda_municipal_p_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_p)
;
CREATE TABLE cc.edf_posto_guarda_municipal_a(
	a smallint,
	CONSTRAINT edf_posto_guarda_municipal_a_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_a)
;
CREATE TABLE cc.edf_posto_fiscal_p(
	tipopostofisc smallint NOT NULL,
	administracao smallint NOT NULL,
	concessionaria varchar(80),
	id_estrut_transporte uuid,
	CONSTRAINT edf_posto_fiscal_p_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_p)
;
CREATE TABLE cc.edf_posto_fiscal_a(
	tipopostofisc smallint NOT NULL,
	administracao smallint NOT NULL,
	concessionaria varchar(80),
	id_estrut_transp uuid,
	CONSTRAINT edf_posto_fiscal_a_pk PRIMARY KEY (geom)
) INHERITS(cc.edf_edif_pub_civil_a)
;
CREATE TABLE cc.edf_edif_religiosa_p(
	tipoedifrelig smallint NOT NULL DEFAULT 0,
	ensino smallint NOT NULL DEFAULT 0,
	religiao varchar(80),
	id_org_religiosa uuid,
	CONSTRAINT edf_edif_religiosa_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_religiosa_a(
	tipoedifrelig smallint NOT NULL DEFAULT 0,
	ensino smallint NOT NULL DEFAULT 0,
	religiao varchar(80),
	id_org_religiosa uuid,
	CONSTRAINT edf_edif_religiosa_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_constr_lazer_p(
	tipoediflazer smallint NOT NULL DEFAULT 0,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_constr_lazer_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_lazer_a(
	tipoediflazer smallint NOT NULL DEFAULT 0,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_constr_lazer_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_constr_turistica_p(
	tipoedifturist smallint NOT NULL DEFAULT 0,
	ovgd smallint NOT NULL DEFAULT 0,
	tombada smallint NOT NULL DEFAULT 2,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_constr_turistica_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_turistica_a(
	tipoedifturist smallint NOT NULL DEFAULT 0,
	ovgd smallint NOT NULL DEFAULT 0,
	tombada smallint NOT NULL DEFAULT 2,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT edf_edif_constr_turistica_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_constr_est_med_fen_p(
	a smallint,
	CONSTRAINT edf_edif_constr_est_med_fen_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_est_med_fen_a(
	a smallint,
	CONSTRAINT edf_edif_constr_est_med_fen_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_energia_p(
	tipoedifenergia smallint NOT NULL DEFAULT 0,
	CONSTRAINT edf_edif_energia_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_energia_a(
	tipoedifenergia smallint NOT NULL DEFAULT 0,
	CONSTRAINT edf_edif_energia_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_comunic_p(
	modalidade smallint NOT NULL DEFAULT 0,
	tipoedifcomunic smallint NOT NULL DEFAULT 0,
	id_complexo_comunicacao uuid,
	CONSTRAINT edf_edif_comunic_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_comunic_a(
	modalidade smallint NOT NULL DEFAULT 0,
	tipoedifcomunic smallint NOT NULL DEFAULT 0,
	id_complexo_comunicacao uuid,
	CONSTRAINT edf_edif_comunic_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_constr_aeroportuaria_p(
	tipoedifaero smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL DEFAULT 0,
	id_complexo_aeroportuario uuid,
	CONSTRAINT edf_edif_constr_aeroportuaria_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_portuaria_a(
	tipoedifport smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	CONSTRAINT edf_edif_constr_portuaria_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_metro_ferroviaria_p(
	tipoedifmetroferrov smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	CONSTRAINT edf_edif_metro_ferroviaria_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_portuaria_p(
	tipoedifport smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80) NOT NULL,
	CONSTRAINT edf_edif_constr_portuaria_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_constr_aeroportuaria_a(
	tipoedifaero smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	id_complexo_aeroportuario uuid,
	CONSTRAINT edf_edif_constr_aeroportuaria_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_metro_ferroviaria_a(
	tipoedifmetroferrov smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	CONSTRAINT edf_edif_metro_ferroviaria_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_rodoviaria_p(
	tipoedifrod smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	CONSTRAINT edf_edif_rodoviaria_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_rodoviaria_a(
	tipoedifrod smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	concessionaria varchar(80),
	CONSTRAINT edf_edif_rodoviaria_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_ext_mineral_p(
	divisaoativecon smallint NOT NULL,
	CONSTRAINT edf_edif_ext_mineral_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_ext_mineral_a(
	divisaoativecon smallint NOT NULL,
	CONSTRAINT edf_edif_ext_mineral_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_agrop_ext_veg_pesca_p(
	tipoedifagropec smallint NOT NULL,
	CONSTRAINT edf_edif_agrop_ext_veg_pesca_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_agrop_ext_veg_pesca_a(
	tipoedifagropec smallint NOT NULL DEFAULT 0,
	CONSTRAINT edf_edif_agrop_ext_veg_pesca_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_industrial_p(
	chamine smallint NOT NULL DEFAULT 0,
	divisaoativecon smallint NOT NULL DEFAULT 0,
	id_org_industrial uuid,
	CONSTRAINT edf_edif_industrial_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_edif_industrial_a(
	chamine smallint NOT NULL DEFAULT 0,
	divisaoativecon smallint NOT NULL DEFAULT 0,
	id_org_industrial uuid,
	CONSTRAINT edf_edif_industrial_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_edif_comerc_serv_p(
	tipoedifcomercserv smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL DEFAULT 0,
	id_estrut_transporte uuid,
	id_org_comerc_serv uuid,
	CONSTRAINT edf_edif_comerc_serv_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_posto_combustivel_p(
	a smallint,
	CONSTRAINT edf_posto_combustivel_p_pk PRIMARY KEY (id_org_comerc_serv)
) INHERITS(cc.edf_edif_comerc_serv_p)
;
CREATE TABLE cc.edf_edif_comerc_serv_a(
	tipoedifcomercserv smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL DEFAULT 0,
	id_estrut_transporte uuid,
	id_org_comerc_serv uuid,
	CONSTRAINT edf_edif_comerc_serv_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE cc.edf_posto_combustivel_a(
	a smallint,
	CONSTRAINT edf_posto_combustivel_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edif_comerc_serv_a)
;
CREATE TABLE cc.edf_banheiro_publico_p(
	a smallint,
	CONSTRAINT edf_banheiro_publico_p_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_p)
;
CREATE TABLE cc.edf_banheiro_publico_a(
	a smallint,
	CONSTRAINT edf_banheiro_publico_a_pk PRIMARY KEY (id)
) INHERITS(cc.edf_edificacao_a)
;
CREATE TABLE complexos.asb_complexo_saneamento(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	classeativecon smallint NOT NULL,
	administracao smallint NOT NULL,
	id_org_comerc_serv uuid,
	id_org_pub_civil uuid,
	CONSTRAINT asb_complexo_saneamento_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.asb_complexo_abast_agua(
	id uuid NOT NULL,
	nome varchar(80),
	classeativecon smallint NOT NULL,
	administracao smallint NOT NULL,
	id_org_comerc_serv uuid,
	id_org_pub_civil uuid,
	CONSTRAINT asb_complexo_abast_agua_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_dep_abast_agua(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipodep smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	tipoexposicao smallint NOT NULL DEFAULT 0,
	unidadevolume smallint NOT NULL,
	valorvolume float,
	tratamento smallint NOT NULL DEFAULT 0,
	finalidadedep smallint NOT NULL DEFAULT 0,
	situacaoagua smallint NOT NULL DEFAULT 0,
	id_complexo_abast_agua uuid,
	CONSTRAINT asb_dep_abast_agua_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_dep_abast_agua_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT asb_dep_abast_agua_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_abast_agua)
;
CREATE INDEX asb_dep_abast_agua_p_gist ON cb.asb_dep_abast_agua_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.asb_dep_abast_agua_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT asb_dep_abast_agua_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_abast_agua)
;
CREATE INDEX "äsb_dep_abast_agua_a_gist" ON cb.asb_dep_abast_agua_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.asb_area_abast_agua_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	"ïd_complexo_abast_agua" uuid,
	CONSTRAINT asb_area_abast_agua_a_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.adm_org_comerc_serv(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	divisaoativecon smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL DEFAULT 0,
	id_org_pub_civil uuid,
	CONSTRAINT adm_org_comerc_serv_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_dep_saneamento(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipodep smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	tipoexposicao smallint NOT NULL DEFAULT 0,
	tipoprodutoresiduo smallint NOT NULL DEFAULT 0,
	tipoconteudo smallint NOT NULL DEFAULT 0,
	unidadevolume smallint,
	valorvolume float,
	estadofisico smallint NOT NULL,
	finalidadedep smallint NOT NULL DEFAULT 0,
	tratamento smallint NOT NULL DEFAULT 0,
	id_complexo_saneamento uuid,
	CONSTRAINT asb_dep_saneamento_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_dep_saneamento_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT asb_dep_saneamento_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_saneamento)
;
CREATE INDEX asb_dep_saneamento_p_gist ON cb.asb_dep_saneamento_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.asb_dep_saneamento_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT asb_dep_saneamento_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_saneamento)
;
CREATE INDEX asb_dep_saneamento_a_gist ON cb.asb_dep_saneamento_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.asb_area_saneamento_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_complexo_saneamento uuid,
	CONSTRAINT asb_area_saneamento_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.eco_deposito_geral(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipodepgeral smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	tipoexposicao smallint NOT NULL DEFAULT 0,
	tipoprodutoresiduo smallint NOT NULL DEFAULT 0,
	tipoconteudo smallint NOT NULL DEFAULT 0,
	unidadevolume smallint,
	valorvolume float,
	id_org_comerc_serv uuid,
	id_org_ext_mineral uuid,
	id_eco_org_agrop_ext_veg_pesca uuid,
	id_enc_complexo_gerad_energ_eletr uuid,
	id_estrut_transporte uuid,
	CONSTRAINT eco_deposito_geral_pk PRIMARY KEY (id)
);
CREATE TABLE cb.eco_deposito_geral_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT eco_deposito_geral_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_deposito_geral)
;
CREATE INDEX eco_deposito_geral_p_gist ON cb.eco_deposito_geral_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_deposito_geral_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT eco_deposito_geral_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_deposito_geral)
;
CREATE INDEX eco_deposito_geral_a_gist ON cb.eco_deposito_geral_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.adm_org_ext_mineral(
	id uuid NOT NULL,
	nome varchar(80),
	secaoativecon smallint NOT NULL DEFAULT 0,
	CONSTRAINT eco_org_ext_mineral_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.adm_org_agrop_ext_veg_pesca(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	divisaoativecon smallint NOT NULL DEFAULT 0,
	id_org_industrial uuid,
	CONSTRAINT org_agropec_ext_vegetal_pesca_pk PRIMARY KEY (id)
);
CREATE TABLE cb.eco_area_agrop_ext_veg_pesca_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	destinadoa smallint NOT NULL DEFAULT 0,
	id_org_agropec_ext_vegetal_pesca uuid,
	CONSTRAINT eco_area_agropec_ext_vegetal_pesca_a_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.adm_org_industrial(
	id uuid NOT NULL,
	nome varchar(80),
	secaoativecon smallint NOT NULL DEFAULT 0,
	id_org_pub_civil uuid,
	id_org_pub_militar uuid,
	CONSTRAINT eco_org_industrial_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.eco_frigorifico_matadouro(
	frigorifico smallint NOT NULL DEFAULT 0,
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_frigorifico_matadouro_pk PRIMARY KEY (id)
) INHERITS(complexos.adm_org_industrial)
;
CREATE TABLE complexos.eco_madeireira(
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_madeireira_pk PRIMARY KEY (id)
) INHERITS(complexos.adm_org_industrial)
;
CREATE TABLE cb.eco_area_industrial_a(
	id serial NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_org_industrial uuid,
	CONSTRAINT eco_area_industrial_a_pk PRIMARY KEY (id)
);
CREATE INDEX eco_area_industrial_a_gist ON cb.eco_area_industrial_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_equip_agropec(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipoequipagropec smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	id_org_agropec_ext_veg uuid,
	CONSTRAINT eco_equip_agropec_pk PRIMARY KEY (id)
);
CREATE TABLE cb.eco_equip_agropec_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT eco_equip_agropec_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE INDEX eco_equip_agropec_p_gist ON cb.eco_equip_agropec_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_equip_agropec_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT eco_equip_agropec_l_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE INDEX eco_equip_agropec_l_gist ON cb.eco_equip_agropec_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_equip_agropec_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT eco_equip_agropec_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE INDEX eco_equip_agropec_a_1 ON cb.eco_equip_agropec_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_plataforma(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoplataforma smallint NOT NULL DEFAULT 0,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_plataforma_pk PRIMARY KEY (id)
);
CREATE TABLE cb.eco_plataforma_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT eco_plataforma_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_plataforma)
;
CREATE INDEX eco_plataforma_p_gist ON cb.eco_plataforma_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_plataforma_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT eco_plataforma_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_plataforma)
;
CREATE INDEX eco_plataforma_a_gist ON cb.eco_plataforma_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_area_ext_mineral_a(
	id serial NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_a_pk_1 PRIMARY KEY (id)
);
CREATE INDEX eco_area_ext_mineral_a_gist ON cb.eco_area_ext_mineral_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.edu_org_ensino(
	id uuid NOT NULL,
	nome varchar(80),
	administracao smallint NOT NULL DEFAULT 0,
	grupoativecon smallint NOT NULL DEFAULT 0,
	CONSTRAINT edu_org_ensino_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.edu_org_ensino_privada(
	id_org_comerc_serv uuid,
	CONSTRAINT edu_org_ensino_privada_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino)
;
CREATE TABLE complexos.edu_org_ensino_militar(
	id_org_pub_militar uuid,
	CONSTRAINT edu_org_ensino_militar_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino)
;
CREATE TABLE complexos.edu_org_ensino_pub(
	id_org_pub_militar uuid,
	id_org_pub_civil uuid,
	CONSTRAINT edu_org_ensino_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino)
;
CREATE TABLE complexos.edu_org_ensino_religiosa(
	id_org_religiosa uuid,
	CONSTRAINT edu_org_ensino_religiosa_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino)
;
CREATE TABLE complexos.enc_complexo_gerad_energ_eletr(
	id uuid NOT NULL,
	nome varchar(80),
	classeativecon smallint NOT NULL DEFAULT 0,
	id_org_comerc_serv uuid,
	CONSTRAINT enc_comp_gerad_energ_ele_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.enc_subestacao_ener_eletro(
	id uuid NOT NULL,
	nome varchar(80),
	classeativecon smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	id_complexo_gerador_energia_eletrica uuid,
	CONSTRAINT enc_subest_transm_distrib_energia_eletrica_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.enc_complexo_comunicacao(
	id uuid NOT NULL,
	nome varchar(80),
	classeativecon smallint NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT enc_complexo_comunicacao_pk PRIMARY KEY (id)
);
CREATE TABLE cb.enc_grupo_transformadores(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipooperativo smallint NOT NULL DEFAULT 0,
	id_subest_transf uuid,
	CONSTRAINT enc_grupo_transformadores_pk PRIMARY KEY (id)
);
CREATE TABLE cb.enc_grupo_transformadores_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT enc_grupo_transformadores_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_grupo_transformadores)
;
CREATE INDEX enc_grupo_transformadores_p_gist ON cb.enc_grupo_transformadores_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_grupo_transformadores_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT enc_grupo_transformadores_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_grupo_transformadores)
;
CREATE INDEX enc_grupo_transformadores_a_gist ON cb.enc_grupo_transformadores_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_area_energia_eletrica_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_subest_transf uuid,
	CONSTRAINT enc_area_energia_eletrica_a_pk PRIMARY KEY (id)
);
CREATE INDEX enc_area_energia_eletrica_a_gist ON cb.enc_area_energia_eletrica_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_zona_linhas_energia_com_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT enc_zona_lin_energ_comunic_a_pk PRIMARY KEY (id)
);
CREATE INDEX enc_zona_lin_energ_comunic_a_gist ON cb.enc_zona_linhas_energia_com_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_area_comunicacao_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_complexo_comunicacao uuid,
	CONSTRAINT enc_area_energia_eletrica_a_pk_1 PRIMARY KEY (id)
);
CREATE INDEX enc_area_comunicacao_a_gist ON cb.enc_area_comunicacao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_torre_energia_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	ovgd smallint NOT NULL DEFAULT 0,
	alturaestimada float,
	tipotorre smallint NOT NULL DEFAULT 0,
	arranjofases varchar(80),
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT enc_torre_energia_p_pk PRIMARY KEY (id)
);
CREATE INDEX enc_torre_energia_p_gist ON cb.enc_torre_energia_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_antena_comunic_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	posicaoreledific smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	id_complexo_comunicacao uuid,
	CONSTRAINT enc_antena_comunic_p_pk PRIMARY KEY (id)
);
CREATE INDEX enc_antena_comunic_p_gist ON cb.enc_antena_comunic_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_torre_comunic_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	posicaoreledific smallint NOT NULL DEFAULT 0,
	ovgd smallint NOT NULL DEFAULT 0,
	alturaestimada float,
	modalidade smallint NOT NULL DEFAULT 0,
	id_complexo_comunicacao uuid,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT enc_torre_comunic_p_pk PRIMARY KEY (id)
);
CREATE INDEX enc_torre_comunic_p_gist ON cb.enc_torre_comunic_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_trecho_energia_l(
	id serial NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	especie smallint NOT NULL DEFAULT 0,
	posicaorelativa smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	emduto smallint NOT NULL DEFAULT 0,
	tensaoeletrica float,
	numcircuitos integer,
	operadora varchar(80),
	id_org_comerc_serv uuid,
	CONSTRAINT enc_trecho_comunic_l_pk PRIMARY KEY (id)
);
CREATE INDEX enc_trecho_energia_l_gist ON cb.enc_trecho_energia_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_trecho_comunic_l(
	id serial NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipotrechocomunic smallint NOT NULL DEFAULT 0,
	posicaorelativa smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	emduto smallint NOT NULL DEFAULT 0,
	id_org_comerc_serv uuid,
	CONSTRAINT enc_trecho_comunic_l_pk_1 PRIMARY KEY (id)
);
CREATE INDEX enc_trecho_comunic_l_gist ON cb.enc_trecho_comunic_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_est_gerad_energia_eletr(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoestgerad smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	destenergelet smallint NOT NULL DEFAULT 0,
	codigoestacao varchar(80),
	potenciaoutorgada float,
	potenciafiscalizada float,
	geracao smallint NOT NULL DEFAULT 0,
	id_enc_complexo_gerad_energ_eletr uuid,
	CONSTRAINT enc_est_gerad_energia_eletrica_fk PRIMARY KEY (id)
);
CREATE TABLE cb.enc_est_gerad_energia_eletr_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE INDEX enc_est_gerad_energia_eletrica_p_gist ON cb.enc_est_gerad_energia_eletr_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_est_gerad_energia_eletr_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_l_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE INDEX enc_est_gerad_energia_eletrica_l_gist ON cb.enc_est_gerad_energia_eletr_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_est_gerad_energia_eletr_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE INDEX enc_est_gerad_energia_eletrica_a_gist ON cb.enc_est_gerad_energia_eletr_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_termeletrica_p(
	tipocombustivel smallint NOT NULL DEFAULT 0,
	combrenovavel smallint NOT NULL DEFAULT 0,
	tipomaqtermica smallint NOT NULL DEFAULT 0,
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_termeletrica_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_p)
;
CREATE TABLE cb.enc_termeletrica_l(
	tipocombustivel smallint NOT NULL DEFAULT 0,
	combrenovavel smallint NOT NULL DEFAULT 0,
	tipomaqtermica smallint NOT NULL DEFAULT 0,
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_termeletrica_l_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_l)
;
CREATE TABLE cb.enc_termeletrica_a(
	tipocombustivel smallint NOT NULL DEFAULT 0,
	combrenovavel smallint NOT NULL DEFAULT 0,
	tipomaqtermica smallint NOT NULL DEFAULT 0,
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_termeletrica_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_a)
;
CREATE TABLE cb.enc_hidreletrica_p(
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_hidreletrica_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_p)
;
CREATE TABLE cb.enc_hidreletrica_l(
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_hidreletrica_l_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_l)
;
CREATE TABLE cb.enc_hidreletrica_a(
	tipoestgerad smallint NOT NULL DEFAULT 0,
	CONSTRAINT enc_hidreletrica_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_a)
;
CREATE TABLE cb.pto_geod_topo_controle_p(
	id serial NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tiporef smallint NOT NULL,
	latitude varchar(80),
	longitude varchar(80),
	altitudeortometrica float,
	sistemageodesico smallint NOT NULL DEFAULT 99,
	outrarefalt varchar(80),
	orgaoenteresp varchar(80),
	codponto varchar(80),
	obs varchar(80),
	CONSTRAINT pto_pto_geod_topo_controle_p_pk PRIMARY KEY (id)
);
CREATE INDEX pto_pto_geod_topo_controle_p_gist ON cb.pto_geod_topo_controle_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.pto_pto_ref_geod_topo_p(
	nome varchar(80),
	proximidade smallint NOT NULL DEFAULT 0,
	tipoptorefgeodtopo smallint NOT NULL DEFAULT 0,
	redereferencia smallint NOT NULL DEFAULT 0,
	referencialgrav smallint NOT NULL DEFAULT 0,
	situacaomarco smallint NOT NULL DEFAULT 0,
	datavisita varchar(80),
	CONSTRAINT pto_pto_ref_geod_topo_p_pk PRIMARY KEY (id)
) INHERITS(cb.pto_geod_topo_controle_p)
;
CREATE TABLE cb.pto_pto_controle_p(
	tipoptocontrole smallint NOT NULL,
	materializado smallint NOT NULL DEFAULT 0,
	codprojeto varchar(80),
	CONSTRAINT pto_pto_controle_p_pk PRIMARY KEY (id)
) INHERITS(cb.pto_geod_topo_controle_p)
;
CREATE TABLE complexos.pto_est_med_fenomenos(
	id uuid,
	nome varchar(80),
	orgaoenteresp varchar(80),
	id_est_med_fenomenos uuid,
	CONSTRAINT pto_est_med_fenomenos_pk PRIMARY KEY (id)
);
CREATE TABLE cb.pto_est_med_fenomenos_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoptoestmed smallint NOT NULL DEFAULT 0,
	codestacao varchar(80),
	id_est_med_fenomenos uuid,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT pto_est_med_fenomenos_p_fk PRIMARY KEY (id)
);
CREATE INDEX pto_est_med_fenomenos_p_gist ON cb.pto_est_med_fenomenos_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.pto_area_est_med_fenomenos_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_est_med_fenomenos uuid,
	CONSTRAINT pto_area_est_med_fenomenos_a_pk PRIMARY KEY (id)
);
CREATE INDEX pto_area_est_med_fenomenos_a_gist ON cb.pto_area_est_med_fenomenos_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.tra_estrut_transporte(
	id uuid NOT NULL,
	nome varchar(80),
	modaluso smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL DEFAULT 0,
	jurisdicao smallint NOT NULL DEFAULT 0,
	concessionaria varchar(80),
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_estrut_transporte_pk PRIMARY KEY (id)
);
CREATE TABLE cb.aer_pista_ponto_pouso(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipopista smallint NOT NULL,
	revestimento smallint NOT NULL DEFAULT 0,
	usopista smallint NOT NULL DEFAULT 0,
	homologacao smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	largura float,
	extensao float,
	id_complexo_aeroportuario uuid,
	CONSTRAINT aer_pista_ponto_pouso_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.aer_complexo_aeroportuario(
	indicador varchar(80),
	siglaaero varchar(80),
	tipocomplexoaeroportuario smallint NOT NULL DEFAULT 0,
	classificacao smallint NOT NULL DEFAULT 0,
	latoficial varchar(80),
	altitude integer,
	CONSTRAINT aer_complexo_aeroportuario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE cb.aer_pista_ponto_pouso_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT aer_pista_ponto_pouso_p_pk PRIMARY KEY (id)
) INHERITS(cb.aer_pista_ponto_pouso)
;
CREATE INDEX aer_pista_ponto_pouso_p_gist ON cb.aer_pista_ponto_pouso_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.aer_pista_ponto_pouso_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT aer_pista_ponto_pouso_l_pk PRIMARY KEY (id)
) INHERITS(cb.aer_pista_ponto_pouso)
;
CREATE INDEX aer_pista_ponto_pouso_l_gist ON cb.aer_pista_ponto_pouso_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.aer_pista_ponto_pouso_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT aer_pista_ponto_pouso_a_pk PRIMARY KEY (id)
) INHERITS(cb.aer_pista_ponto_pouso)
;
CREATE INDEX aer_pista_ponto_pouso_a_gist ON cb.aer_pista_ponto_pouso_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.dut_trecho_duto_l(
	id serial NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipotrechoduto smallint NOT NULL DEFAULT 0,
	mattransp smallint NOT NULL DEFAULT 0,
	setor smallint NOT NULL DEFAULT 0,
	posicaorelativa smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	ndutos integer,
	situacaoespacial smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	id_duto uuid,
	CONSTRAINT dut_trecho_duto_l_pk PRIMARY KEY (id)
);
CREATE INDEX dut_trecho_duto_l_gist ON cb.dut_trecho_duto_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.aer_faixa_seg_aeroportuaria_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	largura float,
	extensao float,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT aer_faixa_seg_aeroportuaria_a_pk PRIMARY KEY (id)
);
CREATE INDEX aer_faixa_seg_aeroportuaria_a_gist ON cb.aer_faixa_seg_aeroportuaria_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.dut_duto(
	id uuid NOT NULL,
	nome varchar(80),
	CONSTRAINT dut_duto_pk PRIMARY KEY (id)
);
CREATE TABLE cb.dut_condutor_hidrico_l(
	mattransp smallint NOT NULL,
	CONSTRAINT dut_condutor_hidrico_l_pk PRIMARY KEY (id)
) INHERITS(cb.dut_trecho_duto_l)
;
CREATE TABLE cb.dut_ponto_duto_p(
	id serial NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_duto uuid,
	relacionado smallint NOT NULL,
	CONSTRAINT dut_ponto_duto_p_pk PRIMARY KEY (id)
);
CREATE INDEX dut_ponto_duto_p_gist ON cb.dut_ponto_duto_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.dut_faixa_dominial_duto_a(
	id serial NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL,
	largura float,
	CONSTRAINT dut_faixa_dominial_duto_a_pk PRIMARY KEY (id)
);
CREATE INDEX dut_faixa_dominial_duto_a_gist ON cb.dut_faixa_dominial_duto_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.hdv_complexo_portuario(
	tipotransporte smallint NOT NULL DEFAULT 0,
	tipocomplexoportuario smallint NOT NULL,
	portosempapel smallint NOT NULL DEFAULT 0,
	CONSTRAINT hdv_complexo_portuario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE complexos.tra_estrut_apoio(
	tipoestrut smallint NOT NULL,
	tipoexposicao smallint NOT NULL,
	CONSTRAINT tra_estrut_apoio_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE complexos.fer_estacao_ferroviaria(
	tipoestrut smallint NOT NULL,
	modaluso smallint NOT NULL,
	CONSTRAINT fer_estacao_ferroviaria_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE complexos.fer_estacao_metroviaria(
	tipoestrut smallint NOT NULL,
	modaluso smallint NOT NULL,
	CONSTRAINT fer_estacao_metroviaria_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE complexos.rod_estacao_rodoviaria(
	tipoestrut smallint NOT NULL,
	modaluso smallint NOT NULL,
	CONSTRAINT rod_estacao_rodoviaria_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE cb.tra_patio(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	modaluso smallint NOT NULL,
	administracao smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	finalidadepatio smallint NOT NULL,
	id_estrut_transporte uuid,
	CONSTRAINT tra_patio_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_patio_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_patio_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio)
;
CREATE INDEX tra_patio_p_gist ON cb.tra_patio_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_patio_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT tra_patio_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio)
;
CREATE INDEX tra_patio_a_gist ON cb.tra_patio_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_estacionamento_p(
	publico smallint NOT NULL,
	finalidadepatio smallint NOT NULL,
	modaluso smallint NOT NULL,
	CONSTRAINT cbc_estacionamento_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio_p)
;
CREATE TABLE cc.cbc_estacionamento_a(
	publico smallint NOT NULL,
	finalidadepatio smallint NOT NULL,
	modaluso smallint NOT NULL,
	CONSTRAINT cbc_estacionamento_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio_a)
;
CREATE TABLE cb.tra_funicular(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_funicular_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_funicular_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_funicular_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_funicular)
;
CREATE INDEX tra_funicular_p_gist ON cb.tra_funicular_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_funicular_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_funicular_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_funicular)
;
CREATE INDEX tra_funicular_l_1 ON cb.tra_funicular_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_caminho_aereo_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipocaminhoaer smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	geom geometry(LINESTRING, 4326) NOT NULL
);
CREATE INDEX tra_caminho_aereo_l_gist ON cb.tra_caminho_aereo_l
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.tra_entroncamento(
	id uuid NOT NULL,
	nome varchar(80),
	tipoentroncamento smallint NOT NULL,
	CONSTRAINT tra_entroncamento_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_entroncamento_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoentroncamento smallint NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	id_entroncamento uuid,
	CONSTRAINT tra_entroncamento_p_pk PRIMARY KEY (id)
);
CREATE INDEX tra_entroncamento_p_gist ON cb.tra_entroncamento_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_entroncamento_l(
	id serial NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_entroncamento uuid,
	CONSTRAINT tra_entroncamento_l_pk PRIMARY KEY (id)
);
CREATE INDEX tra_entroncamento_l_gist ON cb.tra_entroncamento_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_obra_de_arte_viaria(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	modaluso smallint NOT NULL,
	matconstr smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	necessitamanutencao smallint NOT NULL DEFAULT 0,
	largura float,
	entensao float,
	nrfaixas integer,
	nrpistas integer,
	posicaopista smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_obra_de_arte_viaria_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_passagem_elevada_viaduto(
	tipopassagviad smallint NOT NULL,
	vaolivrehoriz float,
	vaovertical float,
	gabhorizsup float,
	cargasuportmaxima float,
	CONSTRAINT tra_passagem_elevada_viaduto_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obra_de_arte_viaria)
;
CREATE TABLE cb.tra_passagem_elevada_viaduto_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_passagem_elevada_viaduto_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_passagem_elevada_viaduto)
;
CREATE INDEX tra_passagem_elevada_viaduto_p_gist ON cb.tra_passagem_elevada_viaduto_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_passagem_elevada_viaduto_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_passagem_elevada_viaduto_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_passagem_elevada_viaduto)
;
CREATE INDEX tra_passagem_elevada_viaduto_l_gist ON cb.tra_passagem_elevada_viaduto_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ponte(
	tipoponte smallint NOT NULL,
	vaolivrehoriz float,
	vaovertical float,
	cargasuportmaxima float,
	CONSTRAINT tra_ponte_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obra_de_arte_viaria)
;
CREATE TABLE cb.tra_ponte_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_ponte_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponte)
;
CREATE INDEX tra_ponte_p_gist ON cb.tra_ponte_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ponte_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_ponte_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponte)
;
CREATE INDEX tra_ponte_l_gist ON cb.tra_ponte_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_tunel(
	altura float,
	CONSTRAINT tra_tunel_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obra_de_arte_viaria)
;
CREATE TABLE cb.tra_tunel_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_tunel_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_tunel)
;
CREATE INDEX tra_tunel_p_gist ON cb.tra_tunel_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_tunel_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_tunel_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_tunel)
;
CREATE INDEX tra_tunel_l_gist ON cb.tra_tunel_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.emu_acesso(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	matconstr smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaoespacial smallint NOT NULL DEFAULT 0,
	CONSTRAINT emu_acesso_pk PRIMARY KEY (id)
);
CREATE TABLE cc.emu_acesso_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT emu_acesso_p_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso)
;
CREATE INDEX emu_acesso_p_gist ON cc.emu_acesso_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.emu_acesso_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT emu_acesso_l_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso)
;
CREATE INDEX emu_acesso_l_1 ON cc.emu_acesso_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.emu_acesso_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT emu_acesso_a_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso)
;
CREATE INDEX emu_acesso_a_gist ON cc.emu_acesso_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_travessia_pedestre(
	tipotravessiaped smallint NOT NULL,
	largura float,
	extensao float,
	matconstr smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_travessia_pedestre_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso)
;
CREATE TABLE cb.tra_travessia_pedestre_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_travessia_pedestre_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia_pedestre)
;
CREATE INDEX tra_travesssia_pedestre_p_gist ON cb.tra_travessia_pedestre_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_travessia_pedestre_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_travessia_pedestre_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia_pedestre)
;
CREATE INDEX tra_travessia_pedestre_l_gist ON cb.tra_travessia_pedestre_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_caminho_carrocavel_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_caminho_carrocavel_l_pk PRIMARY KEY (id)
);
CREATE INDEX tra_caminho_carrocavel_l_gist ON cb.tra_caminho_carrocavel_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_trilha_picada_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(LINESTRING, 4326) NOT NULL
);
CREATE INDEX tra_trilha_picada_l_gist ON cb.tra_trilha_picada_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_travessia(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipotravessia smallint NOT NULL DEFAULT 0,
	tipouso smallint NOT NULL,
	tipoembarcacao smallint NOT NULL,
	CONSTRAINT tra_travessia_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_travessia_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT tra_travessia_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia)
;
CREATE INDEX tra_travessia_p_gist ON cb.tra_travessia_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_travessia_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT tra_travessia_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia)
;
CREATE INDEX tra_travessia_l_gist ON cb.tra_travessia_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ponto_rodoviario_ferrov_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POINT, 4326) NOT NULL
);
CREATE INDEX tra_ponto_rodoviario_ferrov_p_gist ON cb.tra_ponto_rodoviario_ferrov_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rod_trecho_rodoviario(
	id serial NOT NULL,
	nome varchar(80),
	codtrechorodov varchar(80) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipotrechorod smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	administracao smallint NOT NULL,
	concessionaria smallint NOT NULL,
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	nrpistas integer,
	nrfaixas integer,
	trafego smallint NOT NULL DEFAULT 0,
	velocidademedia float,
	velocidademaxima float,
	trechoemperimetrourbano smallint NOT NULL,
	acostamento smallint NOT NULL,
	tipopavimentacao smallint NOT NULL,
	canteirodivisorio smallint NOT NULL DEFAULT 0,
	sigla varchar(80),
	CONSTRAINT rod_trecho_rodoviario_pk PRIMARY KEY (id)
);
CREATE TABLE cb.rod_trecho_rodoviario_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT rod_trecho_rodoviario_l_pk PRIMARY KEY (id)
) INHERITS(cb.rod_trecho_rodoviario)
;
CREATE INDEX rod_trecho_rodoviario_l_gist ON cb.rod_trecho_rodoviario_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.rod_passagem_nivel_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POINT, 4326) NOT NULL
);
CREATE INDEX rod_passagem_nivel_p_gist ON cb.rod_passagem_nivel_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.fer_girador_ferroviario_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	administracao smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	id_estacao_ferroviaria uuid,
	id_estacao_metroviaria uuid,
	CONSTRAINT fer_girador_ferroviario_p_pk PRIMARY KEY (id)
);
CREATE INDEX fer_girador_ferroviario_p_gist ON cb.fer_girador_ferroviario_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.fer_trecho_ferroviario_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	codtrechoferrov varchar(80),
	posicaorelativa smallint NOT NULL,
	bitola smallint NOT NULL,
	eletrificada smallint NOT NULL DEFAULT 0,
	nrlinhas smallint NOT NULL,
	jurisdicao smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL DEFAULT 0,
	concessionaria varchar(80),
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL,
	cargasuportmaxima float,
	tipotrechoferrov smallint NOT NULL,
	id_via_ferrea uuid,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT fer_trecho_ferroviario_l_pk PRIMARY KEY (id)
);
CREATE INDEX fer_trecho_ferroviario_l_gist ON cb.fer_trecho_ferroviario_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.fer_cremalheira(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT fer_cremalheira_pk PRIMARY KEY (id)
);
CREATE TABLE cb.fer_cremalheira_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT fer_cremalheira_p_pk PRIMARY KEY (id)
) INHERITS(cb.fer_cremalheira)
;
CREATE INDEX fer_cremalheira_p_gist ON cb.fer_cremalheira_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.fer_cremalheira_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT fer_cremalheira_l_pk PRIMARY KEY (id)
) INHERITS(cb.fer_cremalheira)
;
CREATE INDEX fer_cremalheira_l_gist ON cb.fer_cremalheira_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_atracadouro_terminal(
	id serial NOT NULL,
	nome varchar(80),
	geometriaproximada smallint NOT NULL DEFAULT 2,
	tipoatracad smallint NOT NULL,
	administracao smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	aptidaooperacional smallint NOT NULL,
	id_complexo_portuario uuid,
	CONSTRAINT hdv_atracadouro_terminal_pk PRIMARY KEY (id)
);
CREATE TABLE cb.hdv_atracadouro_terminal_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hdv_atracadouro_terminal_p_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_atracadouro_terminal)
;
CREATE INDEX hdv_atracadouro_p_gist ON cb.hdv_atracadouro_terminal_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_atracadouro_terminal_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hdv_atracadouro_terminal_l_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_atracadouro_terminal)
;
CREATE INDEX hdv_atracadouro_l_1 ON cb.hdv_atracadouro_terminal_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_atracadouro_terminal_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hdv_atracadouro_terminal_a_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_atracadouro_terminal)
;
CREATE INDEX hdv_atracadouro_a_gist ON cb.hdv_atracadouro_terminal_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_fundeadouro(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipofundeadouro smallint NOT NULL,
	administracao smallint NOT NULL DEFAULT 0,
	CONSTRAINT hdv_fundeadouro_pk PRIMARY KEY (id)
);
CREATE TABLE cb.hdv_fundeadouro_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hdv_fundeadouro_p_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_fundeadouro)
;
CREATE INDEX hdv_fundeadouro_p_gist ON cb.hdv_fundeadouro_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_fundeadouro_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hdv_fundeadouro_l_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_fundeadouro)
;
CREATE INDEX hdv_fundeadouro_l_gist ON cb.hdv_fundeadouro_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_fundeadouro_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hdv_fundeadouro_a_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_fundeadouro)
;
CREATE INDEX hdv_fundeadouro_a_gist ON cb.hdv_fundeadouro_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_sinalizacao_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tiposinal smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hdv_sinalizacao_p_pk PRIMARY KEY (id)
);
CREATE INDEX hdv_sinalizacao_p_gist ON cb.hdv_sinalizacao_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_obstaculo_navegacao(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoobst smallint NOT NULL,
	situacaoemagua smallint NOT NULL DEFAULT 0,
	CONSTRAINT hdv_obstaculo_navegacao_pk PRIMARY KEY (id)
);
CREATE TABLE cb.hdv_obstaculo_navegacao_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hdv_obstaculo_navegacao_p_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_obstaculo_navegacao)
;
CREATE INDEX hdv_obstaculo_navegacao_p_gist ON cb.hdv_obstaculo_navegacao_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_obstaculo_navegacao_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hdv_obstaculo_navegacao_l_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_obstaculo_navegacao)
;
CREATE INDEX hdv_obstaculo_navegacao_l_gist ON cb.hdv_obstaculo_navegacao_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_obstaculo_navegacao_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hdv_obstaculo_navegacao_a_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_obstaculo_navegacao)
;
CREATE INDEX hdv_obstaculo_navegacao_a_gist ON cb.hdv_obstaculo_navegacao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_eclusa(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	desnivel float,
	largura float,
	extensao float,
	calado float,
	matconstr smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT hdv_eclusa_pk PRIMARY KEY (id)
);
CREATE TABLE cb.hdv_eclusa_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT hdv_eclusa_p_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_eclusa)
;
CREATE INDEX hdv_eclusa_p_gist ON cb.hdv_eclusa_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_eclusa_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT hdv_eclusa_l_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_eclusa)
;
CREATE INDEX hdv_eclusa_l_gist ON cb.hdv_eclusa_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.hdv_eclusa_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT hdv_eclusa_a_pk PRIMARY KEY (id)
) INHERITS(cb.hdv_eclusa)
;
CREATE INDEX hdv_eclusa_a_gist ON cb.hdv_eclusa_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_linha_de_limite_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	referenciallegal smallint NOT NULL,
	obssituacao varchar(80),
	extensao float,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT lim_linha_de_limite_l_pk PRIMARY KEY (id)
);
CREATE INDEX lim_linha_de_limite_l_gist ON cb.lim_linha_de_limite_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_limite_politico_adm_l(
	tipolimpol smallint NOT NULL,
	CONSTRAINT lim_limite_politico_adm_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_intra_munic_adm_l(
	tipolimintramun smallint NOT NULL,
	CONSTRAINT lim_limite_intra_munic_adm_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_operacional_l(
	tipolimoper smallint NOT NULL,
	CONSTRAINT lim_limite_operacional_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_outros_limites_oficiais_l(
	tipooutlimofic smallint NOT NULL,
	CONSTRAINT lim_outros_limites_oficiais_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_particular_l(
	a smallint,
	CONSTRAINT lim_limite_particular_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_area_especial_l(
	tipolimareaesp smallint NOT NULL,
	CONSTRAINT lim_limite_area_especial_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_delimitacao_fisica_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipodelimfis smallint NOT NULL,
	matconstr smallint NOT NULL,
	eletrificada smallint NOT NULL DEFAULT 0,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT lim_delimitacao_fisica_l_pk PRIMARY KEY (id)
);
CREATE INDEX lim_delimitacao_fisica_l_gist ON cb.lim_delimitacao_fisica_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_marco_de_limite_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	codigo varchar(80),
	tipomarcolim smallint NOT NULL,
	latitude_gms float,
	latitude varchar(80),
	longitude_gms float,
	longitude smallint,
	altitudeortometrica float,
	sistemageodesico smallint NOT NULL,
	outrarefplan varchar(80),
	referencialaltim smallint NOT NULL,
	outrarefalt varchar(80),
	orgresp varchar(80),
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT lim_marco_de_limite_p_pk PRIMARY KEY (id)
);
CREATE INDEX lim_marco_de_limite_p_gist ON cb.lim_marco_de_limite_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_area_de_litigio_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	descricao varchar(80),
	geom geometry(POLYGON, 4326) NOT NULL
);
CREATE INDEX lim_area_de_litigio_a_gist ON cb.lim_area_de_litigio_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_area_politico_adm_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT lim_area_politico_adm_a_pk PRIMARY KEY (id)
);
CREATE INDEX lim_area_politico_adm_a_gist ON cb.lim_area_politico_adm_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_pais_a(
	sigla varchar(80),
	codiso3166 varchar(80) NOT NULL DEFAULT 'BRA',
	CONSTRAINT lim_pais_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_unidade_federacao_a(
	sigla smallint NOT NULL,
	geocodigo varchar(80),
	CONSTRAINT lim_unidade_federacao_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_municipio_a(
	geocodigo varchar(80),
	anodereferencia integer,
	CONSTRAINT lim_municipio_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_regiao_administrativa_a(
	anodereferencia integer,
	CONSTRAINT lim_regiao_administrativa_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_bairro_a(
	anodereferencia integer,
	CONSTRAINT lim_bairro_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_distrito_a(
	geocodigo varchar(80),
	anodereferencia varchar(80),
	CONSTRAINT lim_distrito_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_sub_distrito_a(
	geocodigo varchar(80),
	anodereferencia varchar(80),
	CONSTRAINT lim_sub_distrito_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.lim_area_especial_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	numerosequencial integer,
	numerometrico integer,
	numerokilometrico float,
	codidentificadorunico varchar(80),
	arealegal float,
	cep integer,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT lim_area_especial_a_pk PRIMARY KEY (id)
);
CREATE INDEX lim_area_especial_a_gist ON cb.lim_area_especial_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_area_desenv_controle_a(
	classificacao varchar(80),
	CONSTRAINT lim_area_desenv_controle_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
CREATE TABLE cb.lim_area_uso_comunitario_a(
	tipoareausocomun smallint NOT NULL,
	CONSTRAINT lim_area_uso_comunitario_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
CREATE TABLE cb.loc_localidade_p(
	id uuid NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	geocodigo varchar(80),
	identificador varchar(80),
	latitude smallint,
	latitude_gms real,
	longitude varchar(80),
	longitude_gms real,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT loc_localidade_p_pk PRIMARY KEY (id)
);
CREATE INDEX loc_localidade_p_gist ON cb.loc_localidade_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.loc_aglomerado_rural_p(
	tipoaglomrurisol smallint,
	CONSTRAINT loc_aglomerado_rural_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.loc_vila_p(
	a smallint,
	CONSTRAINT loc_vila_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.loc_cidade_p(
	a smallint,
	CONSTRAINT loc_cidade_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.loc_capital_p(
	tipocapital smallint NOT NULL,
	CONSTRAINT loc_capital_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_cidade_p)
;
CREATE TABLE cb.loc_area_construida_a(
	id serial NOT NULL,
	nome varchar(80),
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT loc_area_construida_a_pk PRIMARY KEY (id)
);
CREATE INDEX loc_area_construida_a_1 ON cb.loc_area_construida_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.loc_nome_local_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT loc_nome_local_p_pk PRIMARY KEY (id)
);
CREATE INDEX loc_nome_local_p_gist ON cb.loc_nome_local_p
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.cbc_complexo_habitacional(
	id uuid NOT NULL,
	nome varchar(80),
	id_localidade uuid,
	CONSTRAINT cbc_complexo_habitacional_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.loc_aldeia_indigena(
	codigofunai varchar(80),
	terraindigena varchar(80),
	etnia varchar(80),
	CONSTRAINT loc_aldeia_indigena_pk PRIMARY KEY (id)
) INHERITS(complexos.cbc_complexo_habitacional)
;
CREATE TABLE cc.ver_jardim_a(
	finalidade smallint NOT NULL,
	CONSTRAINT ver_jardim_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_veg_cultivada_a)
;
CREATE TABLE complexos.ver_area_verde(
	id uuid NOT NULL,
	nome varchar(80),
	paisagismo smallint NOT NULL,
	administracao smallint NOT NULL DEFAULT 0,
	id_area_verde_urbana uuid,
	id_complexo_desportivo_lazer uuid,
	id_parcela uuid,
	CONSTRAINT ver_area_verde_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.ver_area_verde_urbana(
	id uuid NOT NULL,
	nome varchar(80),
	CONSTRAINT ver_area_verde_urbana_pk PRIMARY KEY (id)
);
CREATE TABLE cc.ver_arvore_isolada_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POINT, 4326) NOT NULL,
	id_area_verde uuid,
	CONSTRAINT ver_arvore_isolada_p_pk PRIMARY KEY (id)
);
CREATE INDEX ver_arvore_isolada_p_gist ON cc.ver_arvore_isolada_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.ppb_terra_publica_a(
	classificacao varchar(80),
	CONSTRAINT ppb_terra_publica_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
CREATE TABLE cc.ppb_terra_indigena_a(
	situacaojuridica smallint NOT NULL,
	datasituacaojuridica varchar(80),
	grupoetnico varchar(80),
	perimetrooficial float,
	CONSTRAINT ppb_terra_indigena_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_terra_publica_a)
;
CREATE TABLE cc.ppb_area_dominial_a(
	a smallint,
	CONSTRAINT ppb_area_dominial_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_terra_publica_a)
;
CREATE TABLE cc.ppb_faixa_dominio_curso_massa_dagua_a(
	largura float,
	terrenomarinha smallint NOT NULL DEFAULT 0,
	CONSTRAINT ppb_faixa_dominio_curso_massa_dagua_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_area_dominial_a)
;
CREATE TABLE cc.ppb_faixa_dominio_rodovia_a(
	largurapartireixo float,
	CONSTRAINT ppb_faixa_dominio_rodovia_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_area_dominial_a)
;
CREATE TABLE cc.ppb_faixa_dominio_arruamento_a(
	largurapartireixo float,
	CONSTRAINT ppb_faixa_dominio_arruamento_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_area_dominial_a)
;
CREATE TABLE cc.ppb_faixa_dominio_ferrovia_a(
	largurapartireixo float,
	CONSTRAINT ppb_faixa_dominio_ferrovia_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_area_dominial_a)
;
CREATE TABLE complexos.laz_complexo_desportivo_lazer(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	divisaoativecon smallint NOT NULL,
	administracao smallint NOT NULL,
	turistico smallint NOT NULL,
	cultura smallint NOT NULL,
	id_org_religiosa uuid,
	id_org_pub_civil uuid,
	id_org_ensino uuid,
	id_comerc_serv uuid,
	id_org_pub_militar uuid,
	CONSTRAINT laz_complexo_desportivo_lazer_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.laz_complexo_desportivo(
	a smallint,
	CONSTRAINT laz_complexo_desportivo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo_lazer)
;
CREATE TABLE complexos.laz_campo_aeromodelismo(
	a smallint,
	CONSTRAINT laz_campo_aeromodelismo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_autodromo(
	a smallint,
	CONSTRAINT laz_autodromo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_velodromo(
	a smallint,
	CONSTRAINT laz_velodromo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_kartodromo(
	a smallint,
	CONSTRAINT laz_kartodromo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_hipica(
	a smallint,
	CONSTRAINT laz_hipica_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_hipodromo(
	a smallint,
	CONSTRAINT laz_hipodromo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_campo_de_golfe(
	a smallint,
	CONSTRAINT laz_campo_de_golfe_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_estande_de_tiro(
	a smallint,
	CONSTRAINT laz_estande_de_tiro_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo)
;
CREATE TABLE complexos.laz_complexo_recreativo(
	tipocomplexorecreativo smallint NOT NULL,
	CONSTRAINT laz_complexo_recreativo_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_desportivo_lazer)
;
CREATE TABLE complexos.laz_clube_social(
	tipocomplexorecreativo smallint NOT NULL,
	CONSTRAINT laz_clube_social_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_jardim_botanico(
	a smallint,
	CONSTRAINT laz_jardim_botanico_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_parque_aquatico(
	a smallint,
	CONSTRAINT laz_parque_aquatico_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_jardim_zoologico(
	a smallint,
	CONSTRAINT laz_jardim_zoologico_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_parque_tematico(
	a smallint,
	CONSTRAINT laz_parque_tematico_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_marina(
	a smallint,
	CONSTRAINT laz_marina_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_pesque_pague(
	a smallint,
	CONSTRAINT laz_pesque_pague_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE complexos.laz_parque_urbano(
	a smallint,
	CONSTRAINT laz_parque_urbano_pk PRIMARY KEY (id)
) INHERITS(complexos.laz_complexo_recreativo)
;
CREATE TABLE cc.laz_arquibancada(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT laz_arquibancada_pk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_arquibancada_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT laz_arquibancada_p_pk PRIMARY KEY (id)
) INHERITS(cc.laz_arquibancada)
;
CREATE INDEX laz_arquibancada_p_gist ON cc.laz_arquibancada_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_arquibancada_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT laz_arquibancada_l_pk PRIMARY KEY (id)
) INHERITS(cc.laz_arquibancada)
;
CREATE INDEX laz_arquibancada_l_gist ON cc.laz_arquibancada_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_arquibancada_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_arquibancada_a_pk PRIMARY KEY (id)
) INHERITS(cc.laz_arquibancada)
;
CREATE INDEX laz_arquibancada_a_gist ON cc.laz_arquibancada_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_praca_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	turistica smallint NOT NULL DEFAULT 1,
	id_complexo_desportivo_lazer uuid,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_praca_a_pk PRIMARY KEY (id)
);
CREATE INDEX laz_praca_a_gist ON cc.laz_praca_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_largo_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_complexo_desportivo_lazer uuid,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_largo_a_pk PRIMARY KEY (id)
);
CREATE INDEX laz_largo_a_gist ON cc.laz_largo_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_campo_quadra(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	tipocampoquadra smallint NOT NULL,
	situacaofisica smallint NOT NULL DEFAULT 0,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT laz_campo_quadra_pk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_campo_quadra_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT laz_campo_quadra_p_pk PRIMARY KEY (id)
) INHERITS(cc.laz_campo_quadra)
;
CREATE INDEX laz_campo_quadra_p_gist ON cc.laz_campo_quadra_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_campo_quadra_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_campo_quadra_a_pk PRIMARY KEY (id)
) INHERITS(cc.laz_campo_quadra)
;
CREATE INDEX laz_campo_quadra_a_gist ON cc.laz_campo_quadra_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_pista_competicao(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	tipofistacomp smallint NOT NULL DEFAULT 0,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT laz_pista_competicao_fk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_pista_competicao_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT laz_pista_competicao_p_pk PRIMARY KEY (id)
) INHERITS(cc.laz_pista_competicao)
;
CREATE INDEX laz_pista_competicao_p_gist ON cc.laz_pista_competicao_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_pista_competicao_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT laz_pista_competicao_l_pk PRIMARY KEY (id)
) INHERITS(cc.laz_pista_competicao)
;
CREATE INDEX laz_pista_competicao_l_gist ON cc.laz_pista_competicao_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_pista_competicao_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_pista_competicao_a_pk PRIMARY KEY (id)
) INHERITS(cc.laz_pista_competicao)
;
CREATE INDEX laz_pista_competicao_a_gist ON cc.laz_pista_competicao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_piscina_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_complexo_desportivo uuid,
	CONSTRAINT laz_piscina_a_pk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_ruina(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	turistica smallint NOT NULL DEFAULT 0,
	cutura smallint NOT NULL DEFAULT 1,
	id_complexo_desportivo_lazer uuid,
	CONSTRAINT laz_ruina_pk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_ruina_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT laz_ruina_p_pk PRIMARY KEY (id)
) INHERITS(cc.laz_ruina)
;
CREATE INDEX laz_ruina_p_gist ON cc.laz_ruina_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_ruina_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_ruina_a_pk PRIMARY KEY (id)
) INHERITS(cc.laz_ruina)
;
CREATE INDEX laz_ruina_a_gist ON cc.laz_ruina_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_sitio_arqueologico(
	id serial NOT NULL,
	nome varchar(80),
	turistica smallint NOT NULL DEFAULT 95,
	cultura smallint NOT NULL DEFAULT 1,
	CONSTRAINT laz_sitio_arqueologico_pk PRIMARY KEY (id)
);
CREATE TABLE cc.laz_sitio_arqueologico_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT laz_sitio_arqueologico_p_pk PRIMARY KEY (id)
) INHERITS(cc.laz_sitio_arqueologico)
;
CREATE INDEX laz_sitio_arqueologico_p_gist ON cc.laz_sitio_arqueologico_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.laz_sitio_arqueologico_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT laz_sitio_arqueologico_a_pk PRIMARY KEY (id)
) INHERITS(cc.laz_sitio_arqueologico)
;
CREATE INDEX laz_sitio_arqueologico_a_1 ON cc.laz_sitio_arqueologico_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.emu_rampa_p(
	a smallint,
	CONSTRAINT emu_rampa_p_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_p)
;
CREATE TABLE cc.emu_rampa_l(
	a smallint,
	CONSTRAINT emu_rampa_l_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_l)
;
CREATE TABLE cc.emu_rampa_a(
	a smallint,
	CONSTRAINT emu_rampa_a_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_a)
;
CREATE TABLE cc.emu_escadaria_p(
	a smallint,
	CONSTRAINT emu_escadaria_p_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_p)
;
CREATE TABLE cc.emu_escadaria_a(
	a smallint,
	CONSTRAINT emu_escadaria_a_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_a)
;
CREATE TABLE cc.emu_escadaria_l(
	a smallint,
	CONSTRAINT emu_escadaria_l_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_l)
;
CREATE TABLE cc.emu_elevador_p(
	tipoelevador smallint NOT NULL,
	CONSTRAINT emu_elevador_p_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_p)
;
CREATE TABLE cc.emu_elevador_l(
	tipoelevador smallint NOT NULL,
	CONSTRAINT emu_elevador_l_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_l)
;
CREATE TABLE cc.emu_elevador_a(
	tipoelevador smallint NOT NULL,
	CONSTRAINT emu_elevador_a_pk PRIMARY KEY (id)
) INHERITS(cc.emu_acesso_a)
;
CREATE TABLE cc.emu_ciclovia_l(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 95,
	situacaofisica smallint NOT NULL,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT emu_ciclovia_l_pk PRIMARY KEY (id)
);
CREATE INDEX emu_ciclovia_l_gist ON cc.emu_ciclovia_l
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.emu_terminal_rodoviario(
	tipoestrut smallint NOT NULL,
	CONSTRAINT emu_terminal_rodoviario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE complexos.emu_terminal_ferroviario(
	tipoestrut smallint NOT NULL,
	CONSTRAINT emu_terminal_ferroviario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE complexos.emu_terminal_hidroviario(
	tipoestrut smallint NOT NULL,
	CONSTRAINT emu_terminal_hidroviario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_apoio)
;
CREATE TABLE ct.imb_lote(
	codlogradouro integer,
	bairro varchar(80),
	tipolote smallint NOT NULL
);
CREATE TABLE ct.imb_parcela(
	id uuid NOT NULL,
	geometriaaproximada smallint NOT NULL,
	numerosequencial integer,
	numerometrico integer,
	numerokilometrico float,
	codidentificadorunico varchar(80),
	arealegal float,
	cep integer,
	CONSTRAINT imb_parcela_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.cbc_condominio(
	a smallint,
	CONSTRAINT cbc_condominio_pk PRIMARY KEY (id)
) INHERITS(complexos.cbc_complexo_habitacional)
;
CREATE TABLE complexos.cbc_conjunto_habitacional(
	a smallint,
	CONSTRAINT cbc_conjunto_habitacional_pk PRIMARY KEY (id)
) INHERITS(complexos.cbc_complexo_habitacional)
;
CREATE TABLE complexos.cbc_area_subnormal(
	id uuid NOT NULL,
	nome varchar(80),
	CONSTRAINT cbc_area_subnormal_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.cbc_palafitas(
	a smallint,
	CONSTRAINT cbc_palafitas_pk PRIMARY KEY (id)
) INHERITS(complexos.cbc_area_subnormal)
;
CREATE TABLE complexos.cbc_favela(
	a smallint,
	CONSTRAINT cbc_favela_pk PRIMARY KEY (id)
) INHERITS(complexos.cbc_area_subnormal)
;
CREATE TABLE cc.cbc_area_habitacional_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_habitacional_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_habitacional_a_gist ON cc.cbc_area_habitacional_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_comunicacao_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_comunicacao_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_comunicacao_a_gist ON cc.cbc_area_comunicacao_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_abast_agua_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_abast_agua_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_abast_agua_a_gist ON cc.cbc_area_abast_agua_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_saneamento_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_saneamento_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_saneamento_a_gist ON cc.cbc_area_saneamento_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_duto_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_duto_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_duto_a_gist ON cc.cbc_area_duto_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_de_prop_particular_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_de_prop_particular_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_de_prop_particular_a_gist ON cc.cbc_area_de_prop_particular_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_servico_social_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_org_servico_social uuid
);
CREATE INDEX cbc_area_servico_social_a_gist ON cc.cbc_area_servico_social_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_saude_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_org_saude uuid,
	CONSTRAINT cbc_area_saude_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_saude_a_gist ON cc.cbc_area_saude_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_ruinas_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_compl_desportivo_laz uuid,
	CONSTRAINT cbc_area_ruinas_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_ruinas_a_gist ON cc.cbc_area_ruinas_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_lazer_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_compl_desportivo_laz uuid,
	CONSTRAINT cbc_area_lazer_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_lazer_a_gist ON cc.cbc_area_lazer_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_comerc_serv_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT cbc_area_comerc_serv_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_comerc_serv_a_gist ON cc.cbc_area_comerc_serv_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_ensino_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT cbc_area_ensino_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_ensino_a_gist ON cc.cbc_area_ensino_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_religiosa_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_religiosa_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_religiosa_a_gist ON cc.cbc_area_religiosa_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_urbana_isolada_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	tipoassociado smallint NOT NULL,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_urbana_isolada_a_ok PRIMARY KEY (id)
);
CREATE INDEX cbc_area_urbana_isolada_a_gist ON cc.cbc_area_urbana_isolada_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_trecho_rodoviario_a(
	a smallint,
	CONSTRAINT cbc_trecho_rodoviario_a_pk PRIMARY KEY (id)
) INHERITS(cb.rod_trecho_rodoviario)
;
CREATE TABLE cc.cbc_retorno(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	CONSTRAINT cbc_retorno_pk PRIMARY KEY (id)
);
CREATE TABLE cc.cbc_retorno_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT cbc_retorno_p_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_retorno)
;
CREATE INDEX cbc_retorno_p_gist ON cc.cbc_retorno_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_retorno_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT cbc_retorno_l_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_retorno)
;
CREATE INDEX cbc_retorno_l_gist ON cc.cbc_retorno_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_retorno_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_retorno_a_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_retorno)
;
CREATE INDEX cbc_retorno_a_gist ON cc.cbc_retorno_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_canteiro_central(
	id serial NOT NULL,
	gemetriaaproximada smallint NOT NULL,
	situacaoespacial smallint NOT NULL,
	CONSTRAINT cbc_canteiro_central_pk PRIMARY KEY (id)
);
CREATE TABLE cc.cbc_canteiro_central_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT cbc_canteiro_central_l_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_canteiro_central)
;
CREATE INDEX cbc_canteiro_central_l_gist ON cc.cbc_canteiro_central_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_canteiro_central_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_canteiro_central_a_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_canteiro_central)
;
CREATE INDEX cbc_canteiro_central_a_gist ON cc.cbc_canteiro_central_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_meio_fio_l(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	comsargeta smallint NOT NULL DEFAULT 95,
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT cbc_meio_fio_l_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_meio_fio_l_gist ON cc.cbc_meio_fio_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_passeio(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	largura float,
	calcada smallint NOT NULL DEFAULT 95,
	pavimentacao smallint NOT NULL
);
CREATE TABLE cc.cbc_passeio_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_passeio_a_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_passeio)
;
CREATE INDEX cbc_passeio_a_gist ON cc.cbc_passeio_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_passeio_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT cbc_passeio_l_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_passeio)
;
CREATE INDEX cbc_passeio_l_gist ON cc.cbc_passeio_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_trecho_arruamento(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	nrfaixas integer,
	nrpistas integer,
	trafego smallint NOT NULL,
	canteirodivisorio smallint NOT NULL,
	acostamento smallint NOT NULL,
	tipoarruamento smallint NOT NULL,
	tipopavimentacao smallint NOT NULL,
	id_arruamento uuid,
	CONSTRAINT cbc_trecho_arruamento_pk PRIMARY KEY (id)
);
CREATE TABLE cc.cbc_trecho_arruamento_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT cbc_trecho_arruamento_l_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_trecho_arruamento)
;
CREATE INDEX cbc_trecho_arruamento_l_gist ON cc.cbc_trecho_arruamento_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_trecho_arruamento_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_trecho_arruamento_a_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_trecho_arruamento)
;
CREATE INDEX cbc_trecho_arruamento_a_gist ON cc.cbc_trecho_arruamento_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.cbc_arruamento(
	id uuid NOT NULL,
	CONSTRAINT cbc_arruamento_pk PRIMARY KEY (id)
);
CREATE TABLE cc.cbc_entroncamento_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON) NOT NULL,
	id_arruamento uuid,
	CONSTRAINT cbc_entroncamento_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_entroncamento_a_gist ON cc.cbc_entroncamento_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_ponte_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_ponte_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponte)
;
CREATE INDEX cbc_ponte_a_gist ON cc.cbc_ponte_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_area_pub_civil_a(
	a smallint,
	CONSTRAINT cbc_area_pub_civil_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_terra_publica_a)
;
CREATE TABLE cc.cbc_area_pub_militar_a(
	a smallint,
	CONSTRAINT cbc_area_pub_militar_a_pk PRIMARY KEY (id)
) INHERITS(cc.ppb_terra_publica_a)
;
CREATE TABLE cc.cbc_quadra_a(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	id_bairro uuid,
	CONSTRAINT cbc_quadra_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_quadra_a_gist ON cc.cbc_quadra_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_tunel_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_tunel_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_tunel)
;
CREATE INDEX cbc_tunel_a_gist ON cc.cbc_tunel_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_passagem_elevada_viaduto_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_passagem_elevada_viaduto_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_passagem_elevada_viaduto)
;
CREATE INDEX cbc_passagem_elevada_viaduto_a_gist ON cc.cbc_passagem_elevada_viaduto_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_travessia_pedrestre_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_travessia_pedrestre_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia_pedestre)
;
CREATE INDEX cbc_travessia_pedrestre_a_gist ON cc.cbc_travessia_pedrestre_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_perimetro_legal_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL
);
CREATE INDEX cbc_perimetro_legal_a_gist ON cc.cbc_perimetro_legal_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.cbc_perimetro_urbano_a(
	a smallint,
	CONSTRAINT cbc_perimetro_urbano_a_pk PRIMARY KEY (id)
) INHERITS(cc.cbc_perimetro_legal_a)
;
CREATE TABLE cc.mub_bebedouro_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_bebedouro_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_bebedouro_p_gist ON cc.mub_bebedouro_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_banco_praca(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	CONSTRAINT mub_banco_praca_pk PRIMARY KEY (id)
);
CREATE TABLE cc.mub_banco_praca_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT mub_banco_praca_l_pk PRIMARY KEY (id)
) INHERITS(cc.mub_banco_praca)
;
CREATE INDEX mub_banco_praca_l_gist ON cc.mub_banco_praca_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_banco_praca_p(
	geom geometry(POINT, 4326) NOT NULL
) INHERITS(cc.mub_banco_praca)
;
CREATE INDEX mub_banco_praca_p_gist ON cc.mub_banco_praca_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_vaso_jardineira_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_vaso_jardineira_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_vaso_jardineira_p_gist ON cc.mub_vaso_jardineira_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_espelho_dagua_a(
	id serial NOT NULL,
	nome varchar(80),
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT mub_espelho_dagua_a_pk PRIMARY KEY (id)
);
CREATE INDEX mub_espelho_dagua_a_gist ON cc.mub_espelho_dagua_a
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_fonte_p(
	id serial NOT NULL,
	nome varchar(80),
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_fonte_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_fonte_p_gist ON cc.mub_fonte_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_academia_esporte_publico_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_academia_esporte_publico_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_academia_esporte_publico_p_gist ON cc.mub_academia_esporte_publico_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_parquinho_infantil_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL
);
CREATE INDEX mub_parquinho_infantil_p_gist ON cc.mub_parquinho_infantil_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_relogio_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_relogio_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_relogio_p_gist ON cc.mub_relogio_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_lixeira_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_lixeira_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_lixeira_p_gist ON cc.mub_lixeira_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_hidrante_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_hidrante_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_hidrante_p_gist ON cc.mub_hidrante_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_caixa_coleta_correios_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL
);
CREATE INDEX mub_caixa_coleta_correios_p_gist ON cc.mub_caixa_coleta_correios_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_armario_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	matconstr smallint NOT NULL,
	tipoarmario smallint NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_armario_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_armario_p_gist ON cc.mub_armario_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_poste_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	codident varchar(80),
	matconstr smallint NOT NULL,
	tipoposte smallint NOT NULL,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_poste_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_poste_p_gist ON cc.mub_poste_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_poste_sinalizacao_p(
	tipoposte smallint NOT NULL,
	CONSTRAINT mub_poste_sinalizacao_p_pk PRIMARY KEY (id)
) INHERITS(cc.mub_poste_p)
;
CREATE TABLE cc.mub_cabine_telefonica_publica_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_cabine_telefonica_publica_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_cabine_telefonica_publica_p_gist ON cc.mub_cabine_telefonica_publica_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_engenho_publicicade_p(
	id serial NOT NULL,
	codident varchar(80),
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_engenho_publicicade_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_engenho_publicicade_p_gist ON cc.mub_engenho_publicicade_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_parada_onibus(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	nome varchar(80),
	codident varchar(80),
	id_estrut_apoio uuid,
	CONSTRAINT mub_parada_onibus_pk PRIMARY KEY (id)
);
CREATE TABLE cc.mub_parada_onibus_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT mub_parada_onibus_p_pk PRIMARY KEY (id)
) INHERITS(cc.mub_parada_onibus)
;
CREATE INDEX mub_parada_onibus_p_gist ON cc.mub_parada_onibus_p
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_parada_onibus_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT mub_parada_onibus_l_pk PRIMARY KEY (id)
) INHERITS(cc.mub_parada_onibus)
;
CREATE INDEX mub_parada_onibus_l_gist ON cc.mub_parada_onibus_l
	USING gist
	(
	  geom
	);
CREATE TABLE cc.mub_parada_taxi_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	nome varchar(80),
	codident varchar(80),
	geom geometry(POINT, 4326) NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT mub_parada_taxi_p_pk PRIMARY KEY (id)
);
CREATE INDEX mub_parada_taxi_p_gist ON cc.mub_parada_taxi_p
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.adm_org_pub_militar(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	classeativecon smallint NOT NULL,
	tipoorgmilitar smallint NOT NULL,
	administracao smallint NOT NULL,
	id_org_pub_militar uuid,
	id_instituicao_publica uuid,
	CONSTRAINT adm_org_pub_militar_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.adm_org_pub_civil(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	classeativecon smallint NOT NULL,
	administracao smallint NOT NULL,
	tipoorgcivil smallint NOT NULL,
	poderpublico smallint NOT NULL,
	administracaodireta smallint NOT NULL,
	id_org_pub_civil uuid,
	CONSTRAINT adm_org_pub_civil_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_cemiterio(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	tipocemiterio smallint NOT NULL,
	denominacaoassociada smallint NOT NULL,
	destinacaocemiterio smallint NOT NULL,
	id_org_comerc_serv uuid,
	id_org_pub_civil uuid,
	CONSTRAINT asb_cemiterio_pk PRIMARY KEY (id)
);
CREATE TABLE cb.asb_cemiterio_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT asb_cemiterio_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_cemiterio)
;
CREATE INDEX asb_cemiterio_p_gist ON cb.asb_cemiterio_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.asb_cemiterio_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT asb_cemiterio_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_cemiterio)
;
CREATE INDEX abs_cemiterio_a_gist ON cb.asb_cemiterio_a
	USING gist
	(
	  geom
	);
CREATE TABLE ct.rdr_galeria_bueiro_l(
	finalidade smallint NOT NULL,
	pesosuportmaximo smallint,
	tipotrechoduto smallint NOT NULL,
	CONSTRAINT rdr_galeria_bueiro_l_pk PRIMARY KEY (id)
) INHERITS(cb.dut_trecho_duto_l)
;
CREATE TABLE ct.rdr_galeria_l(
	largura float,
	CONSTRAINT rdr_galeria_l_pk PRIMARY KEY (id)
) INHERITS(ct.rdr_galeria_bueiro_l)
;
CREATE TABLE ct.dci_local_risco(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	tiporisco smallint NOT NULL,
	CONSTRAINT dci_local_risco_pk PRIMARY KEY (id)
);
CREATE TABLE ct.dci_local_critico(
	tiporisco smallint NOT NULL,
	tipolocalcrit smallint NOT NULL,
	CONSTRAINT dci_local_critico_pk PRIMARY KEY (id)
) INHERITS(ct.dci_local_risco)
;
CREATE TABLE ct.dci_local_critico_p(
	geom geometry(POINT, 4326) NOT NULL,
	CONSTRAINT dci_local_critico_p_pk PRIMARY KEY (id)
) INHERITS(ct.dci_local_critico)
;
CREATE INDEX dci_local_critico_p_gist ON ct.dci_local_critico_p
	USING gist
	(
	  geom
	);
CREATE TABLE ct.dci_local_critico_l(
	geom geometry(LINESTRING, 4326) NOT NULL,
	CONSTRAINT dci_local_critico_l_pk PRIMARY KEY (id)
) INHERITS(ct.dci_local_critico)
;
CREATE INDEX dci_local_critico_l_gist ON ct.dci_local_critico_l
	USING gist
	(
	  geom
	);
CREATE TABLE ct.dci_local_critico_a(
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT dci_local_critico_a_pk PRIMARY KEY (id)
) INHERITS(ct.dci_local_critico)
;
CREATE INDEX dci_local_critico_a_gist ON ct.dci_local_critico_a
	USING gist
	(
	  geom
	);
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"
      WITH SCHEMA public;
CREATE TABLE complexos.adm_org_religiosa(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	classeativecon smallint NOT NULL,
	cultura smallint NOT NULL,
	CONSTRAINT adm_org_religiosa_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.adm_instituicao_publica(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	grupoativecon smallint NOT NULL,
	administracao smallint NOT NULL,
	poderpublico smallint NOT NULL,
	id_instituicao_publica uuid,
	id_org_pub_civil uuid,
	CONSTRAINT adm_instituicao_publica_fk PRIMARY KEY (id)
);
CREATE TABLE complexos.sau_org_saude(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	administracao smallint NOT NULL,
	grupoativecon smallint NOT NULL,
	classeativecon smallint NOT NULL,
	numeroleitos integer,
	numeroleitosuti integer,
	CONSTRAINT sau_org_saude_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.sau_org_saude_militar(
	id_org_pub_militar uuid,
	CONSTRAINT sau_org_saude_militar_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_saude)
;
CREATE TABLE complexos.sau_org_saude_privada(
	id_org_comerc_serv uuid,
	CONSTRAINT sau_org_saude_privada_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_saude)
;
CREATE TABLE complexos.sau_org_saude_pub(
	id_org_pub_civil uuid,
	CONSTRAINT sau_org_saude_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_saude)
;
CREATE TABLE complexos.sau_especialidade_medica(
	id serial NOT NULL,
	nome smallint NOT NULL,
	numeromedicos integer,
	id_org_saude uuid
);
CREATE TABLE complexos.sau_org_servico_social(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	administracao smallint NOT NULL,
	grupoativecon smallint NOT NULL,
	classeativecon smallint NOT NULL,
	tipoorgsvsocial smallint NOT NULL,
	CONSTRAINT sau_org_servico_social_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.sau_org_servico_social_pub(
	id_org_pub_civil uuid,
	CONSTRAINT sau_org_servico_social_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_servico_social)
;
CREATE TABLE cc.cbc_area_industrial_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_org_industrial uuid,
	geom geometry(POLYGON, 4326) NOT NULL,
	CONSTRAINT cbc_area_industrial_a_pk PRIMARY KEY (id)
);
CREATE INDEX cbc_area_industrial_a_gist ON cc.cbc_area_industrial_a
	USING gist
	(
	  geom
	);
ALTER TABLE cb.hid_barragem ADD CONSTRAINT hid_barragem_id_complexo_gerad_fk FOREIGN KEY (id_enc_complexo_gerad_energ_eletr)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.hid_reservatorio_hidrico_a ADD CONSTRAINT hid_reservatorio_hidrico_id_compl_fk FOREIGN KEY (id_enc_complexo_gerad_energ_eletr)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.veg_vegetacao_a ADD CONSTRAINT veg_vege_id_area_verde_fk FOREIGN KEY (id_area_verde)
REFERENCES complexos.ver_area_verde (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_ext_mineral_p ADD CONSTRAINT eco_ext_mineral_p_id_org_ext_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_ext_mineral_l ADD CONSTRAINT eco_ext_mineral_l_id_org_ext_min_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_ext_mineral_a ADD CONSTRAINT eco_ext_mineral_a_id_org_ext_min_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edificacao ADD CONSTRAINT edf_edificacao_id_area_subn_fk FOREIGN KEY (id_area_subnormal)
REFERENCES complexos.cbc_area_subnormal (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edificacao ADD CONSTRAINT edf_edificacao_id_compl_hab_fk FOREIGN KEY (id_complexo_habitacional)
REFERENCES complexos.cbc_complexo_habitacional (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_abast_agua_p ADD CONSTRAINT edf_edif_abast_agua_p_id_complexo_abast_agua_fk FOREIGN KEY (id_complexo_abast_agua)
REFERENCES complexos.asb_complexo_abast_agua (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_saneamento_p ADD CONSTRAINT edf_saneam_id_complexo_saneamento_fk FOREIGN KEY (id_complexo_saneamento)
REFERENCES complexos.asb_complexo_saneamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_ensino_p ADD CONSTRAINT edf_eep_id_ensino_fk FOREIGN KEY (id_org_ensino)
REFERENCES complexos.edu_org_ensino (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_saude_p ADD CONSTRAINT eesp_id_org_saude_fk FOREIGN KEY (id_org_saude)
REFERENCES complexos.sau_org_saude (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_servico_social_p ADD CONSTRAINT eesp_id_org_servico_social_fk FOREIGN KEY (id_org_servico_social)
REFERENCES complexos.sau_org_servico_social (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_abast_agua_a ADD CONSTRAINT edf_edif_abast_agua_a_id_complexo_abast_agua_fk FOREIGN KEY (id_complexo_abast_agua)
REFERENCES complexos.asb_complexo_abast_agua (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.hid_ilha_p ADD CONSTRAINT id_complexo_hid_arquipelago_fk FOREIGN KEY (id_complexo_hid_arquipelago)
REFERENCES complexos.hid_arquipelago (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.hid_ilha_l ADD CONSTRAINT id_complexo_hid_arquipelago_fk FOREIGN KEY (id_complexo_hid_arquipelago)
REFERENCES complexos.hid_arquipelago (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.hid_ilha_a ADD CONSTRAINT id_complexo_hid_arquipelago_fk FOREIGN KEY (id_complexo_hid_arquipelago)
REFERENCES complexos.hid_arquipelago (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_saneamento_a ADD CONSTRAINT edf_saneam_id_complexo_saneamento_fk FOREIGN KEY (id_complexo_saneamento)
REFERENCES complexos.asb_complexo_saneamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_ensino_a ADD CONSTRAINT edf_eea_id_ensino_fk FOREIGN KEY (id_org_ensino)
REFERENCES complexos.edu_org_ensino (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_saude_a ADD CONSTRAINT eesa_id_org_saude_fk FOREIGN KEY (id_org_saude)
REFERENCES complexos.sau_org_saude (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_servico_social_a ADD CONSTRAINT eesa_id_org_servico_social_fk FOREIGN KEY (id_org_servico_social)
REFERENCES complexos.sau_org_servico_social (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_pub_civil_p ADD CONSTRAINT edf_dpca_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_pub_civil_a ADD CONSTRAINT edf_dpcp_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_posto_fiscal_p ADD CONSTRAINT epfp_estr_trans_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_posto_fiscal_a ADD CONSTRAINT epfa_estr_trans_fk FOREIGN KEY (id_estrut_transp)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_religiosa_p ADD CONSTRAINT edf_religp_org_rel_fk FOREIGN KEY (id_org_religiosa)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_religiosa_a ADD CONSTRAINT edf_religa_org_rel_fk FOREIGN KEY (id_org_religiosa)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_constr_lazer_p ADD CONSTRAINT edf_eclp_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_constr_lazer_a ADD CONSTRAINT edf_ecla_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_constr_turistica_p ADD CONSTRAINT edf_ect_id_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_constr_turistica_a ADD CONSTRAINT edf_ecta_id_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comunic_p ADD CONSTRAINT eecp_id_complexo_comunicacao_fk FOREIGN KEY (id_complexo_comunicacao)
REFERENCES complexos.enc_complexo_comunicacao (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comunic_a ADD CONSTRAINT eeca_id_compl_com_fk FOREIGN KEY (id_complexo_comunicacao)
REFERENCES complexos.enc_complexo_comunicacao (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_industrial_p ADD CONSTRAINT edf_industr_p_id_org_industrial_fk FOREIGN KEY (id_org_industrial)
REFERENCES complexos.adm_org_industrial (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_industrial_a ADD CONSTRAINT edf_industr_a_id_org_industrial_fk FOREIGN KEY (id_org_industrial)
REFERENCES complexos.adm_org_industrial (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comerc_serv_p ADD CONSTRAINT eecsp_id_est_transp_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comerc_serv_p ADD CONSTRAINT eecsp_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comerc_serv_a ADD CONSTRAINT eecsa_id_est_transp_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.edf_edif_comerc_serv_a ADD CONSTRAINT eecsa_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.asb_complexo_saneamento ADD CONSTRAINT asb_compl_sanem_id_org_comerc_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.asb_complexo_saneamento ADD CONSTRAINT asb_cs_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.asb_complexo_abast_agua ADD CONSTRAINT asb_complexo_abast_agua_id_org_com_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.asb_complexo_abast_agua ADD CONSTRAINT asb_caa_org_pub_civ_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.asb_area_abast_agua_a ADD CONSTRAINT asb_area_abast_agua_a_complexo_fk FOREIGN KEY ("ïd_complexo_abast_agua")
REFERENCES complexos.asb_complexo_abast_agua (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_comerc_serv ADD CONSTRAINT aocsv_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.asb_area_saneamento_a ADD CONSTRAINT asb_area_saneamento_id_compl_saneam_fk FOREIGN KEY (id_complexo_saneamento)
REFERENCES complexos.asb_complexo_saneamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_p ADD CONSTRAINT edgp_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_p ADD CONSTRAINT edgp_id_org_ext_mineral FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_p ADD CONSTRAINT edgp_id_eoaevp_fk FOREIGN KEY (id_eco_org_agrop_ext_veg_pesca)
REFERENCES complexos.adm_org_agrop_ext_veg_pesca (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_p ADD CONSTRAINT edgp_id_ecgee_fk FOREIGN KEY (id_enc_complexo_gerad_energ_eletr)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_p ADD CONSTRAINT edgp_id_estr_trans_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_a ADD CONSTRAINT edga_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_a ADD CONSTRAINT edga_id_org_ext_min_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_a ADD CONSTRAINT edga_id_eoaevp_fk FOREIGN KEY (id_eco_org_agrop_ext_veg_pesca)
REFERENCES complexos.adm_org_agrop_ext_veg_pesca (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_a ADD CONSTRAINT edga_id_ecgee_fk FOREIGN KEY (id_enc_complexo_gerad_energ_eletr)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_deposito_geral_a ADD CONSTRAINT edga_id_estr_transp_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_agrop_ext_veg_pesca ADD CONSTRAINT org_agropec_id_org_industrial_fk FOREIGN KEY (id_org_industrial)
REFERENCES complexos.adm_org_industrial (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_area_agrop_ext_veg_pesca_a ADD CONSTRAINT eco_org_agropec_ext_vegetal_pesca_fk FOREIGN KEY (id_org_agropec_ext_vegetal_pesca)
REFERENCES complexos.adm_org_agrop_ext_veg_pesca (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_industrial ADD CONSTRAINT aoi_id_org_pub_civil FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_industrial ADD CONSTRAINT aoi_id_org_pub_militar_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.eco_frigorifico_matadouro ADD CONSTRAINT efm_id_oaevp_fk FOREIGN KEY (id_org_agrop_ext_veg_pesca)
REFERENCES complexos.adm_org_agrop_ext_veg_pesca (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.eco_frigorifico_matadouro ADD CONSTRAINT efm_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.eco_frigorifico_matadouro ADD CONSTRAINT efm_id_org_pub_militar_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_area_industrial_a ADD CONSTRAINT eco_area_industrial_a_org_ind_fk FOREIGN KEY (id_org_industrial)
REFERENCES complexos.adm_org_industrial (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_equip_agropec ADD CONSTRAINT eco_equip_agropec_id_org_agro_fk FOREIGN KEY (id_org_agropec_ext_veg)
REFERENCES complexos.adm_org_agrop_ext_veg_pesca (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_plataforma ADD CONSTRAINT eco_plataforma_id_org_ext_min_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.eco_area_ext_mineral_a ADD CONSTRAINT eco_area_ext_mineral_a_org_ext_fk FOREIGN KEY (id_org_ext_mineral)
REFERENCES complexos.adm_org_ext_mineral (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.edu_org_ensino_privada ADD CONSTRAINT edu_org_ensino_privada_id_org_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.edu_org_ensino_militar ADD CONSTRAINT eoem_id_org_pub_militar FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.edu_org_ensino_pub ADD CONSTRAINT eoep_id_org_pub_militar_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.edu_org_ensino_pub ADD CONSTRAINT eoep_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.edu_org_ensino_religiosa ADD CONSTRAINT eoer_id_org_religiosa_fk FOREIGN KEY (id_org_religiosa)
REFERENCES complexos.adm_org_religiosa (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.enc_complexo_gerad_energ_eletr ADD CONSTRAINT enc_comp_gerad_energ_ele_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.enc_subestacao_ener_eletro ADD CONSTRAINT sub_trans_distr_ener_ele_comp_gerad_fk FOREIGN KEY (id_complexo_gerador_energia_eletrica)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.enc_complexo_comunicacao ADD CONSTRAINT enc_complexo_comunic_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_grupo_transformadores ADD CONSTRAINT enc_gt_id_subest_transf_fk FOREIGN KEY (id_subest_transf)
REFERENCES complexos.enc_subestacao_ener_eletro (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_area_energia_eletrica_a ADD CONSTRAINT enc_aee_id_subest_transffk FOREIGN KEY (id_subest_transf)
REFERENCES complexos.enc_subestacao_ener_eletro (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_area_comunicacao_a ADD CONSTRAINT enc_ac_id_compl_comunic_fk FOREIGN KEY (id_complexo_comunicacao)
REFERENCES complexos.enc_complexo_comunicacao (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_antena_comunic_p ADD CONSTRAINT enc_acp_id_compl_com_fk FOREIGN KEY (id_complexo_comunicacao)
REFERENCES complexos.enc_complexo_comunicacao (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_torre_comunic_p ADD CONSTRAINT enc_tcp_id_compl_com_fk FOREIGN KEY (id_complexo_comunicacao)
REFERENCES complexos.enc_complexo_comunicacao (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_trecho_energia_l ADD CONSTRAINT enc_trecho_comunic_l_id_org_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_trecho_comunic_l ADD CONSTRAINT enc_tcl_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.enc_est_gerad_energia_eletr ADD CONSTRAINT enc_egee_id_compl_gee_fk FOREIGN KEY (id_enc_complexo_gerad_energ_eletr)
REFERENCES complexos.enc_complexo_gerad_energ_eletr (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.pto_est_med_fenomenos ADD CONSTRAINT pto_est_med_fenomenos_fk FOREIGN KEY (id)
REFERENCES complexos.pto_est_med_fenomenos (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.pto_est_med_fenomenos_p ADD CONSTRAINT pto_est_med_fenomenos_p_id_fk FOREIGN KEY (id_est_med_fenomenos)
REFERENCES complexos.pto_est_med_fenomenos (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.pto_area_est_med_fenomenos_a ADD CONSTRAINT pto_area_est_med_fenomenos_a_fk FOREIGN KEY (id_est_med_fenomenos)
REFERENCES complexos.pto_est_med_fenomenos (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.aer_pista_ponto_pouso ADD CONSTRAINT aerppp_id_compl_aer_fk FOREIGN KEY (id_complexo_aeroportuario)
REFERENCES complexos.aer_complexo_aeroportuario (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.dut_trecho_duto_l ADD CONSTRAINT dut_trecho_duto_l_id_duto_fk FOREIGN KEY (id_duto)
REFERENCES complexos.dut_duto (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.dut_ponto_duto_p ADD CONSTRAINT dut_pdp_id_duto_fk FOREIGN KEY (id_duto)
REFERENCES complexos.dut_duto (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.tra_patio ADD CONSTRAINT tra_patio_id_est_tra_fk FOREIGN KEY (id_estrut_transporte)
REFERENCES complexos.tra_estrut_transporte (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.tra_entroncamento_p ADD CONSTRAINT tra_entr_p_id_entr_fk FOREIGN KEY (id_entroncamento)
REFERENCES complexos.tra_entroncamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.tra_entroncamento_l ADD CONSTRAINT tel_id_entr_fk FOREIGN KEY (id_entroncamento)
REFERENCES complexos.tra_entroncamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.fer_girador_ferroviario_p ADD CONSTRAINT fer_gf_ef_fk FOREIGN KEY (id_estacao_ferroviaria)
REFERENCES complexos.fer_estacao_ferroviaria (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.fer_girador_ferroviario_p ADD CONSTRAINT fer_gf_em_fk FOREIGN KEY (id_estacao_metroviaria)
REFERENCES complexos.fer_estacao_metroviaria (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cb.hdv_atracadouro_terminal ADD CONSTRAINT hdv_at_compl_port_fk FOREIGN KEY (id_complexo_portuario)
REFERENCES complexos.hdv_complexo_portuario (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.cbc_complexo_habitacional ADD CONSTRAINT cbc_ch_id_loc_fk FOREIGN KEY (id_localidade)
REFERENCES cb.loc_localidade_p (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.ver_area_verde ADD CONSTRAINT ver_av_id_avu_fk FOREIGN KEY (id_area_verde_urbana)
REFERENCES complexos.ver_area_verde_urbana (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.ver_area_verde ADD CONSTRAINT ver_av_id_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.ver_area_verde ADD CONSTRAINT ver_av_parcela_fk FOREIGN KEY (id_parcela)
REFERENCES complexos.ver_area_verde (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.ver_arvore_isolada_p ADD CONSTRAINT ver_ai_av_fk FOREIGN KEY (id_area_verde)
REFERENCES complexos.ver_area_verde (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_campo_aeromodelismo ADD CONSTRAINT laz_ca_id_org_religiosa_fk FOREIGN KEY (id_org_religiosa)
REFERENCES complexos.adm_org_religiosa (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_campo_aeromodelismo ADD CONSTRAINT laz_ca_id_org_pub_civil FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_campo_aeromodelismo ADD CONSTRAINT laz_ca_id_org_ensino_fk FOREIGN KEY (id_org_ensino)
REFERENCES complexos.edu_org_ensino (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_campo_aeromodelismo ADD CONSTRAINT laz_ca_id_comerc_serv_fk FOREIGN KEY (id_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_campo_aeromodelismo ADD CONSTRAINT laz_ca_id_org_pub_militar FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_autodromo ADD CONSTRAINT laz_auto_id_org_religiosa_fk FOREIGN KEY (id_org_religiosa)
REFERENCES complexos.adm_org_religiosa (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_autodromo ADD CONSTRAINT laz_auto_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_autodromo ADD CONSTRAINT laz_auto_id_org_ensino_fk FOREIGN KEY (id_org_ensino)
REFERENCES complexos.edu_org_ensino (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_autodromo ADD CONSTRAINT laz_auto_id_comerc_serv_fk FOREIGN KEY (id_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.laz_autodromo ADD CONSTRAINT laz_auto_id_org_pub_mil_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_praca_a ADD CONSTRAINT laz_praca_id_comp_dl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_largo_a ADD CONSTRAINT laz_largo_a_id_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_campo_quadra ADD CONSTRAINT laz_cq_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_pista_competicao ADD CONSTRAINT laz_pc_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_piscina_a ADD CONSTRAINT laz_piscina_a_fk FOREIGN KEY (id_complexo_desportivo)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.laz_ruina ADD CONSTRAINT laz_ruina_cdl_fk FOREIGN KEY (id_complexo_desportivo_lazer)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_servico_social_a ADD CONSTRAINT cbc_assa_id_org_sv_soc_fk FOREIGN KEY (id_org_servico_social)
REFERENCES complexos.sau_org_servico_social (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_saude_a ADD CONSTRAINT cbc_as_id_org_saude_fk FOREIGN KEY (id_org_saude)
REFERENCES complexos.sau_org_saude (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_ruinas_a ADD CONSTRAINT cbc_a_ruina_id_compl_des_laz_fk FOREIGN KEY (id_compl_desportivo_laz)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_lazer_a ADD CONSTRAINT cbc_a_laz_a_id_compl_desp_laz_fk FOREIGN KEY (id_compl_desportivo_laz)
REFERENCES complexos.laz_complexo_desportivo_lazer (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_comerc_serv_a ADD CONSTRAINT cbc_acsa_org_comerc_sv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_ensino_a ADD CONSTRAINT cbc_aea_id_org_ensino_fk FOREIGN KEY (id_org_ensino)
REFERENCES complexos.edu_org_ensino (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_trecho_arruamento ADD CONSTRAINT cbc_trecho_arruam_fk FOREIGN KEY (id_arruamento)
REFERENCES complexos.cbc_arruamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_entroncamento_a ADD CONSTRAINT cbc_entronc_fk FOREIGN KEY (id_arruamento)
REFERENCES complexos.cbc_arruamento (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.mub_parada_onibus ADD CONSTRAINT mub_parada_onibus_id_estrut_apoio_fk FOREIGN KEY (id_estrut_apoio)
REFERENCES complexos.tra_estrut_apoio (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.mub_parada_taxi_p ADD CONSTRAINT mub_parada_taxi_id_estrut_apoio_fk FOREIGN KEY (id_estrut_apoio)
REFERENCES complexos.tra_estrut_apoio (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_pub_militar ADD CONSTRAINT adm_org_pub_militar_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_pub_militar ADD CONSTRAINT aopm_id_inst_publ_fk FOREIGN KEY (id_instituicao_publica)
REFERENCES complexos.adm_instituicao_publica (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_org_pub_civil ADD CONSTRAINT adm_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_instituicao_publica ADD CONSTRAINT adm_aip_aip_fk FOREIGN KEY (id_instituicao_publica)
REFERENCES complexos.adm_instituicao_publica (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.adm_instituicao_publica ADD CONSTRAINT adm_aip_id_org_pc_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.sau_org_saude_militar ADD CONSTRAINT sau_osm_id_org_pub_mil_fk FOREIGN KEY (id_org_pub_militar)
REFERENCES complexos.adm_org_pub_militar (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.sau_org_saude_privada ADD CONSTRAINT sau_osp_id_org_comerc_serv_fk FOREIGN KEY (id_org_comerc_serv)
REFERENCES complexos.adm_org_comerc_serv (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.sau_org_saude_pub ADD CONSTRAINT sau_osp_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.sau_especialidade_medica ADD CONSTRAINT sau_em_id_org_saude_fk FOREIGN KEY (id_org_saude)
REFERENCES complexos.sau_org_saude (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE complexos.sau_org_servico_social_pub ADD CONSTRAINT sau_ossp_id_org_pub_civil_fk FOREIGN KEY (id_org_pub_civil)
REFERENCES complexos.adm_org_pub_civil (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
ALTER TABLE cc.cbc_area_industrial_a ADD CONSTRAINT caia_id_org_industrial_fk FOREIGN KEY (id_org_industrial)
REFERENCES complexos.adm_org_industrial (id) MATCH FULL
ON DELETE NO ACTION ON UPDATE NO ACTION NOT DEFERRABLE;
create view public.complex_schema as
select nsp.nspname as complex_schema, COALESCE(inheritancetree.child,t2.relname) as complex, npsagreg.nspname as aggregated_schema, t.relname as aggregated_class, at1.attname as column_name from pg_constraint c
	left join pg_class t on c.conrelid = t.oid left join pg_class t2 on c.confrelid = t2.oid
	join pg_namespace nsp on t2.relnamespace = nsp.oid 
	left join 
		(SELECT tier1.*,c.relname AS child, c.oid as childoid, p.relname AS parent, tier2p.relname as grandpa, tier3p.relname as grandgrandpa, tier4p.relname as gggpa, COALESCE(tier4p.relname,tier3p.relname,tier2p.relname,p.relname) as ancestral,COALESCE(tier4p.oid,tier3p.oid,tier2p.oid,p.oid) as ancestralOid
		FROM
		    pg_inherits as tier1
		    left JOIN pg_class AS c ON (inhrelid=c.oid)
		    left JOIN pg_class as p ON (inhparent=p.oid)
		    left join pg_inherits as tier2 on tier2.inhrelid=tier1.inhparent
		    left JOIN pg_class as tier2p ON (tier2.inhparent=tier2p.oid)
		    left join pg_inherits as tier3 on tier3.inhrelid=tier2.inhparent
		    left JOIN pg_class as tier3p ON (tier3.inhparent=tier3p.oid)
		    left join pg_inherits as tier4 on tier4.inhrelid=tier3.inhparent
		    left JOIN pg_class as tier4p ON (tier4.inhparent=tier4p.oid) 
		    ) as inheritancetree
		on t2.oid=ancestralOid
	left join pg_attribute as at1 on (at1.attnum=c.conkey[1]) and (at1.attrelid=c.conrelid)
	left join pg_namespace npsagreg on t.relnamespace = npsagreg.oid
	where contype = 'f' and (nsp.nspname = 'complexos')
	order by t2.relname;
CREATE TABLE dominios.administracao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
administracao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.app_curso_massa_dagua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
app_curso_massa_dagua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.aptidao_operacional_atracadouro( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
aptidao_operacional_atracadouro_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.atividade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
atividade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.bitola( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
bitola_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.booleano( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
booleano_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.booleano_estendido( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
booleano_estendido_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.causa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
causa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.causa_exposicao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
causa_exposicao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.classe_ativ_econ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
classe_ativ_econ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.classificacao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
classificacao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.classificacao_porte( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
classificacao_porte_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.condicao_terreno( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
condicao_terreno_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.cultivo_predominante( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
cultivo_predominante_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.denominacao_associada( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
denominacao_associada_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.densidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
densidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.dentro_de( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
dentro_de_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.dest_energ_elet( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
dest_energ_elet_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.destinacao_cemiterio( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
destinacao_cemiterio_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.destinado_a( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
destinado_a_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.divisao_ativ_econ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
divisao_ativ_econ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.especie( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
especie_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.especie_trecho_energia( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
especie_trecho_energia_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.espess_algas( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
espess_algas_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.estado_fisico( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
estado_fisico_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.estagio_processo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
estagio_processo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.finalidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
finalidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.finalidade_cultura( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
finalidade_cultura_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.finalidade_deposito( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
finalidade_deposito_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.finalidade_galeria_bueiro( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
finalidade_galeria_bueiro_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.finalidade_patio( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
finalidade_patio_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.forma_extracao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
forma_extracao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.forma_rocha( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
forma_rocha_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.geracao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
geracao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.grupo_ativ_econ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
grupo_ativ_econ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.jurisdicao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
jurisdicao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.mat_condutor( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
mat_condutor_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.mat_constr( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
mat_constr_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.mat_transp( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
mat_transp_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.material_predominante( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
material_predominante_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.modal_uso( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
modal_uso_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.modalidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
modalidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.motivo_retencao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
motivo_retencao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.nivel_atencao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
nivel_atencao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.nome_especialidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
nome_especialidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.nr_linhas( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
nr_linhas_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.poder_publico( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
poder_publico_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.posicao_placa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
posicao_placa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.posicao_rel_edific( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
posicao_rel_edific_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.posicao_relativa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
posicao_relativa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.preposicao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
preposicao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.proc_extracao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
proc_extracao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.proximidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
proximidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.qualid_agua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
qualid_agua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.rede_referencia( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
rede_referencia_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.referencia_legal( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
referencia_legal_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.referencial_altim( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
referencial_altim_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.referencial_grav( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
referencial_grav_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.regime( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
regime_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.relacionado( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
relacionado_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.revestimento( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
revestimento_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.secao_ativ_econ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
secao_ativ_econ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.setor( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
setor_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.sigla_uf( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
sigla_uf_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.sistema_geodesico( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
sistema_geodesico_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_agua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_agua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_costa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_costa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_em_agua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_em_agua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_espacial( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_espacial_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_fisica( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_fisica_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_juridica( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_juridica_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_logradouro( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_logradouro_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_marco( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_marco_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.situacao_terreno( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
situacao_terreno_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_aglom_rur_isol( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_aglom_rur_isol_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_alter_antrop( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_alter_antrop_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_area_umida( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_area_umida_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_area_uso_comun( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_area_uso_comun_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_armario( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_armario_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_arruamento( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_arruamento_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_associado( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_associado_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_atracad( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_atracad_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_banco( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_banco_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_caminho_aereo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_caminho_aereo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_campo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_campo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_campo_quadra( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_campo_quadra_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_capital( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_capital_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_cemiterio( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_cemiterio_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_circ_rod( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_circ_rod_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_cmplxdesport_lazer( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_cmplxdesport_lazer_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_cmplxrecreativo_lazer( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_cmplxrecreativo_lazer_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_combustivel( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_combustivel_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_complexo_aeroportuario( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_complexo_aeroportuario_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_complexo_lazer( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_complexo_lazer_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_complexo_portuario( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_complexo_portuario_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_conteudo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_conteudo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_curva_nivel( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_curva_nivel_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_delim_fis( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_delim_fis_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_dep_geral( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_dep_geral_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_divisoria( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_divisoria_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_abast( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_abast_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_aero( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_aero_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_agropec( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_agropec_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_comerc_serv( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_comerc_serv_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_comunic( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_comunic_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_energia( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_energia_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_lazer( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_lazer_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_metro_ferrov( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_metro_ferrov_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_port( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_port_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_relig( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_relig_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_rod( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_rod_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_saneam( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_saneam_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_edif_turist( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_edif_turist_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_elem_nat( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_elem_nat_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_elevador( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_elevador_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_embarcacao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_embarcacao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_entroncamento( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_entroncamento_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_equip_agropec( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_equip_agropec_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_erosao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_erosao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_est_gerad( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_est_gerad_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_estrut( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_estrut_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_exposicao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_exposicao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_ext_min( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_ext_min_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_fonte_dagua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_fonte_dagua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_fundeadouro( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_fundeadouro_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_gleba( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_gleba_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_hierarquia( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_hierarquia_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_ilha( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_ilha_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_instal_militar( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_instal_militar_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lavoura( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lavoura_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lim_area_esp( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lim_area_esp_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lim_intra_mun( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lim_intra_mun_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lim_massa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lim_massa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lim_oper( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lim_oper_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_lim_pol( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_lim_pol_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_local_critico( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_local_critico_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_local_risco( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_local_risco_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_logradouro( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_logradouro_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_manguezal( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_manguezal_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_maq_termica( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_maq_termica_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_massa_dagua( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_massa_dagua_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_obst( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_obst_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_operativo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_operativo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_org_civil( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_org_civil_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_org_militar( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_org_militar_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_org_sv_social( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_org_sv_social_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_out_lim_ofic( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_out_lim_ofic_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_out_unid_prot( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_out_unid_prot_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_passag_viad( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_passag_viad_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pavimentacao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pavimentacao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pavimento( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pavimento_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pista( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pista_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pista_comp( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pista_comp_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_placa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_placa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_plataforma( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_plataforma_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_poco_mina( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_poco_mina_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_ponte( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_ponte_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_poste( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_poste_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_posto_fisc( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_posto_fisc_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_produto_residuo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_produto_residuo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pto_controle( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pto_controle_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pto_est_med( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pto_est_med_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_pto_ref_geod_topo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_pto_ref_geod_topo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_quebra_molhe( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_quebra_molhe_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_queda( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_queda_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_recife( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_recife_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_ref( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_ref_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_rep_diplomatica( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_rep_diplomatica_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_restricao_circ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_restricao_circ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_sinal( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_sinal_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_subunidade( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_subunidade_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_sum_vert( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_sum_vert_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_terreno_exposto( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_terreno_exposto_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_torre( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_torre_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_transporte( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_transporte_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_travessia( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_travessia_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_travessia_ped( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_travessia_ped_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_comunic( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_comunic_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_drenagem( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_drenagem_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_duto( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_duto_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_ferrov( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_ferrov_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_massa( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_massa_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_trecho_rod( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_trecho_rod_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_unid_prot_integ( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_unid_prot_integ_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_unid_protegida( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_unid_protegida_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_unid_uso_sust( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_unid_uso_sust_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_uso_edif( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_uso_edif_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_vegetacao( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_vegetacao_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_via_rod( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_via_rod_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.titulo( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
titulo_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.trafego( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
trafego_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.unidade_volume( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
unidade_volume_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.uso_pista( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
uso_pista_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.uso_principal( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
uso_principal_pk PRIMARY KEY (code)
);
CREATE TABLE dominios.tipo_tunel( 
code smallint NOT NULL, 
code_name text NOT NULL, CONSTRAINT
tipo_tunel_pk PRIMARY KEY (code)
);
INSERT INTO dominios.administracao (code,code_name) VALUES (1, 'Federal');  
INSERT INTO dominios.administracao (code,code_name) VALUES (2, 'Estadual/Distrital');  
INSERT INTO dominios.administracao (code,code_name) VALUES (3, 'Municipal');  
INSERT INTO dominios.administracao (code,code_name) VALUES (4, 'Concessionada');  
INSERT INTO dominios.administracao (code,code_name) VALUES (5, 'Privada');  
INSERT INTO dominios.administracao (code,code_name) VALUES (6, 'Não aplicável');  
INSERT INTO dominios.administracao (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.app_curso_massa_dagua (code,code_name) VALUES (5, '5 m');  
INSERT INTO dominios.app_curso_massa_dagua (code,code_name) VALUES (8, '8 m');  
INSERT INTO dominios.app_curso_massa_dagua (code,code_name) VALUES (15, '15 m');  
INSERT INTO dominios.app_curso_massa_dagua (code,code_name) VALUES (30, '30 m');  
INSERT INTO dominios.app_curso_massa_dagua (code,code_name) VALUES (50, '50 m');  
INSERT INTO dominios.aptidao_operacional_atracadouro (code,code_name) VALUES (1, 'Transporte de cabotagem');  
INSERT INTO dominios.aptidao_operacional_atracadouro (code,code_name) VALUES (2, 'Transporte oceânico');  
INSERT INTO dominios.atividade (code,code_name) VALUES (9, 'Prospecção');  
INSERT INTO dominios.atividade (code,code_name) VALUES (10, 'Produção');  
INSERT INTO dominios.atividade (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.bitola (code,code_name) VALUES (1, 'Métrica');  
INSERT INTO dominios.bitola (code,code_name) VALUES (2, 'Internacional');  
INSERT INTO dominios.bitola (code,code_name) VALUES (3, 'Larga');  
INSERT INTO dominios.bitola (code,code_name) VALUES (4, 'Mista métrica internacional');  
INSERT INTO dominios.bitola (code,code_name) VALUES (5, 'Mista métrica  larga');  
INSERT INTO dominios.bitola (code,code_name) VALUES (6, 'Mista internacional larga');  
INSERT INTO dominios.bitola (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.booleano (code,code_name) VALUES (0, 'Não');  
INSERT INTO dominios.booleano (code,code_name) VALUES (1, 'Sim');  
INSERT INTO dominios.booleano_estendido (code,code_name) VALUES (0, 'Não');  
INSERT INTO dominios.booleano_estendido (code,code_name) VALUES (1, 'Sim');  
INSERT INTO dominios.booleano_estendido (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.causa (code,code_name) VALUES (2, 'Absorção');  
INSERT INTO dominios.causa (code,code_name) VALUES (4, 'Gruta ou fenda');  
INSERT INTO dominios.causa (code,code_name) VALUES (5, 'Canalização');  
INSERT INTO dominios.causa (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (1, 'Natural');  
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (2, 'Artificial');  
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (2, 'Produção de energia elétrica');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (3, 'Transmissão de energia elétrica');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (4, 'Distribuição de energia elétrica');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (5, 'Captação, tratamento e distribuição de água');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (6, 'Telecomunicações');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (7, 'Administração pública em geral');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (8, 'Seguridade social');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (9, 'Regulação das atividades econômicas');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (10, 'Atividades de apoio à administração pública');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (11, 'Relações exteriores');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (12, 'Defesa');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (13, 'Justiça');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (14, 'Segurança e ordem pública');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (15, 'Defesa civil');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (16, 'Regulação das atividades sociais e culturais');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (17, 'Educação infantil - creche');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (18, 'Educação infantil-pré-escola');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (19, 'Ensino fundamental');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (20, 'Ensino médio');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (21, 'Educação superior-graduação');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (22, 'Educação superior-graduação e pós-graduação');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (23, 'Educação superior-pós-graduação e extensão');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (24, 'Educação profissional de nível técnico');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (25, 'Educação profissional de nível tecnológico');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (26, 'Outras atividades de ensino');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (27, 'Atendimento hospitalar (hospital)');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (28, 'Atendimento às urgências e emergências (pronto-socorro)');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (29, 'Atenção ambulatorial (posto e centro de saúde)');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (30, 'Serviços de complementação diagnóstica ou terapêutica');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (31, 'Atividades de organizações religiosas');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (32, 'Outras atividades relacionadas com atenção à saúde (instituto de pesquisa)');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (33, 'Serviços sociais com alojamento');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (34, 'Serviços sociais sem alojamento');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (35, 'Limpeza urbana e atividades relacionadas');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (36, 'Serviços veterinários');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (97, 'Misto');  
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.classificacao (code,code_name) VALUES (2, 'Internacional');  
INSERT INTO dominios.classificacao (code,code_name) VALUES (9, 'Doméstico');  
INSERT INTO dominios.classificacao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (2, 'Rasteira');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (3, 'Herbácea');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (4, 'Arbórea');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (5, 'Arbustiva');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (97, 'Mista');  
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (1, 'Inundado');  
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (2, 'Seco');  
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (3, 'Irrigado');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (2, 'Cultura rotativa');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (3, 'Milho');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (4, 'Banana');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (5, 'Laranja');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (6, 'Trigo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (7, 'Abacate');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (8, 'Algodão herbáceo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (9, 'Cana de açúcar');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (10, 'Fumo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (11, 'Soja');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (12, 'Batata inglesa');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (13, 'Mandioca');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (14, 'Feijão');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (15, 'Arroz');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (16, 'Café');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (17, 'Cacau');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (18, 'Erva-mate');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (19, 'Palmeira');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (20, 'Açaí');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (21, 'Seringueira');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (22, 'Eucalipto');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (23, 'Acácia');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (24, 'Algaroba');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (25, 'Pinus');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (26, 'Pastagem cultivada');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (27, 'Hortaliças');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (28, 'Abacaxi ou ananás');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (29, 'Araucária');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (30, 'Carnaúba');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (31, 'Alfafa');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (32, 'Maçã');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (33, 'Pêssego');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (34, 'Juta');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (35, 'Cebola');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (36, 'Algodão arbóreo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (37, 'Alho');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (38, 'Amendoim');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (39, 'Aveia');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (40, 'Azeitona');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (41, 'Batata-doce');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (42, 'Caju');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (43, 'Centeio');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (44, 'Videira');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (45, 'Cevada');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (46, 'Chá-da-índia');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (47, 'Coco-da-baía');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (48, 'Cravo da índia');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (49, 'Dendê');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (50, 'Ervilha');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (51, 'Fava');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (52, 'Figo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (53, 'Flores');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (54, 'Girassol');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (55, 'Goiaba');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (56, 'Guaraná');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (57, 'Inhame');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (58, 'Limão');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (59, 'Linho');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (60, 'Malva');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (61, 'Mamão');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (62, 'Mamona');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (63, 'Mandioca, aipim ou macaxeira');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (64, 'Manga');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (65, 'Maracujá');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (66, 'Marmelo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (67, 'Melancia');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (68, 'Melão');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (96, 'Não identificado');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (70, 'Noz');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (71, 'Palmito');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (72, 'Pera');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (73, 'Piaçava');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (74, 'Plantas ornamentais');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (75, 'Policultura');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (76, 'Rami');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (77, 'Sisal ou agave');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (78, 'Sorgo');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (79, 'Tangerina');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (80, 'Tomate');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (81, 'Triticale');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (82, 'Tungue');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (83, 'Urucum');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (84, 'Uva');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (85, 'Pimenta do reino');  
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (5, 'Israelita');  
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (6, 'Muçulmana');  
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (7, 'Cristã');  
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (99, 'Outras');  
INSERT INTO dominios.densidade (code,code_name) VALUES (1, 'Alta');  
INSERT INTO dominios.densidade (code,code_name) VALUES (2, 'Baixa');  
INSERT INTO dominios.densidade (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (3, 'Trecho de massa dágua');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (4, 'Canal');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (5, 'Vala');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (11, 'Galeria');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (12, 'Bueiro');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (13, 'Área úmida');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (14, 'Queda dágua');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (17, 'Corredeira');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (18, 'Eclusa');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (19, 'Foz marítima');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (20, 'Barragem');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (21, 'Laguna');  
INSERT INTO dominios.dentro_de (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (1, 'Serviço público (SP)');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (2, 'Auto-produção de energia (APE)');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (3, 'Auto-produção com comercialização de excedente (APE-COM)');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (4, 'Comercialização de energia (COM)');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (5, 'Produção independente de energia (PIE)');  
INSERT INTO dominios.dest_energ_elet (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.destinacao_cemiterio (code,code_name) VALUES (5, 'Humanos');  
INSERT INTO dominios.destinacao_cemiterio (code,code_name) VALUES (6, 'Animais');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (2, 'Pesca');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (18, 'Madeira');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (33, 'Açaí');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (34, 'Planta ornamental');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (35, 'Turfa');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (36, 'Látex');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (37, 'Castanha');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (38, 'Carnaúba');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (39, 'Coco');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (40, 'Jaborandi');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (41, 'Palmito');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (42, 'Babaçu');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (43, 'Marisco');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (44, 'Pecuária');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.destinado_a (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (3, 'Agricultura, pecuário e serviços relacionados');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (4, 'Silvicultura, exploração florestal e serviços relacionados');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (5, 'Fabricação de produtos de minerais não metálicos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (6, 'Atividades recreativas, culturais e desportivas');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (7, 'Serviços prestados principalmente a empresas (organizações)');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (10, 'Fabricação de produtos de madeira e celulose');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (11, 'Pesca, aquicultura e serviços relacionados');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (13, 'Extração de carvão mineral');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (14, 'Extração de petróleo e serviços relacionados');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (15, 'Extração de minerais metálicos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (16, 'Extração de minerais não-metálicos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (17, 'Fabricação alimentícia e bebidas');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (18, 'Fabricação de produtos do fumo');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (20, 'Fabricação de produtos têxteis');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (21, 'Confecção de artigos do vestuário e acessórios');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (22, 'Preparação de couros e fabricação de artefatos de couro, artigos de viagens e calçados');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (23, 'Fabricação de celulose, papel e produtos de papel');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (24, 'Edição, impressão e reprodução de gravações');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (25, 'Fabricação de coque, refino de petróleo, elaboração de combustíveis nucleares e produção de álcool');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (27, 'Fabricação de produtos químicos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (28, 'Fabricação de artigos de borracha e material plástico');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (29, 'Metalurgia básica');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (30, 'Fabricação de produtos de metal, exclusive máquinas e equipamentos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (31, 'Fabricação de máquinas e equipamentos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (32, 'Fabricação de máquinas de escritório e equipamentos de informática');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (33, 'Fabricação de máquinas, aparelhos e materiais elétricos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (34, 'Fabricação de material eletrônico, e equipamentos de comunicações');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (35, 'Fabricação de equipamentos de instrumentação médico-hospitalares, instrumentos de precisão e ópticos, equipamentos pa automação instrustrial, cronômetros e relógios');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (36, 'Fabricação e montagem de veículos automotores, reboques e carrocerias');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (37, 'Fabricação de outros equipamentos de transporte');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (45, 'Fabricação de móveis e indústrias diversas');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (50, 'Reciclagem');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (51, 'Construção');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (52, 'Comércio e reparação de veiculos automotores e motocicletas e comércio a varejo de combustíveis');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (55, 'Comércio por atacado e representantes comerciais e agentes do comércio');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (74, 'Comércio varejista e reparação de objetos pessoais e domésticos');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (92, 'Alojamento e alimentação');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.divisao_ativ_econ (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.especie (code,code_name) VALUES (11, 'Cipó');  
INSERT INTO dominios.especie (code,code_name) VALUES (12, 'Bambu');  
INSERT INTO dominios.especie (code,code_name) VALUES (13, 'Araucária');  
INSERT INTO dominios.especie (code,code_name) VALUES (17, 'Sororoca');  
INSERT INTO dominios.especie (code,code_name) VALUES (27, 'Palmeira');  
INSERT INTO dominios.especie (code,code_name) VALUES (37, 'Sem predominância');  
INSERT INTO dominios.especie (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.especie (code,code_name) VALUES (96, 'Não identificado');  
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (1, 'Distribuição');  
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (2, 'Transmissão');  
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.espess_algas (code,code_name) VALUES (2, 'Finas');  
INSERT INTO dominios.espess_algas (code,code_name) VALUES (3, 'Médias');  
INSERT INTO dominios.espess_algas (code,code_name) VALUES (4, 'Grossas');  
INSERT INTO dominios.espess_algas (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (0, 'Sólido');  
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (1, 'Misto');  
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (2, 'Gasoso');  
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (4, 'Líquido');  
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.estagio_processo (code,code_name) VALUES (1, 'Avançado');  
INSERT INTO dominios.estagio_processo (code,code_name) VALUES (2, 'Médio');  
INSERT INTO dominios.estagio_processo (code,code_name) VALUES (3, 'Inicial');  
INSERT INTO dominios.estagio_processo (code,code_name) VALUES (96, 'Não identificado');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (2, 'Uso restrito');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (3, 'Residencial');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (4, 'Comercial');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (5, 'Serviço');  
INSERT INTO dominios.finalidade (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (2, 'Ornamental');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (3, 'Exploração econômica');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (4, 'Subsistência');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (5, 'Conservação ambiental');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (2, 'Armazenamento');  
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (4, 'Distribuição');  
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (5, 'Recalque');  
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (8, 'Tratamento');  
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (1, 'Canalização de efluentes industriais');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (2, 'Canalização de águas pluviais');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (3, 'Irrigaçao');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (4, 'Abastecimento animal');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (5, 'Abastecimento humano');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (6, 'Abastecimento industrial');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (7, 'Canalização de curso dágua');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (8, 'Canalização de efluentes domésticos');  
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (2, 'Deposito temporário de cargas e contêineres');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (3, 'Estacionamento de veículos ');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (4, 'Estacionamento de locomotivas');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (5, 'Estacionamento de aeronaves');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (6, 'Manobra de cargas');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (7, 'Manobra de veículos em geral');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (8, 'Manutenção');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (21, 'Subterrânea');  
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (22, 'A céu aberto');  
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (2, 'Área rochosa - lajedo');  
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (3, 'Penedo isolado');  
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (4, 'Matacão - pedra');  
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.geracao (code,code_name) VALUES (1, 'Eletricidade - GER 0');  
INSERT INTO dominios.geracao (code,code_name) VALUES (2, 'Cogeração');  
INSERT INTO dominios.geracao (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (1, 'Ensino médio');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (2, 'Educação infantil e ensino fundamental');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (3, 'Serviços veterinários ');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (4, 'Ensino superior');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (5, 'Educação profissional e outras atividades de ensino');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (6, 'Administração do estado e da política econômica e social');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (7, 'Serviços coletivos prestados pela administração');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (9, 'Seguridade social');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (10, 'Atividades de atenção à saúde');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (19, 'Serviço social');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.grupo_ativ_econ (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (1, 'Internacional');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (2, 'Propriedade particular');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (3, 'Federal');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (4, 'Estadual/Distrital');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (5, 'Municipal');  
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (1, 'Fibra ótica');  
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (2, 'Fio metálico');  
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (2, 'Alvenaria');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (3, 'Concreto');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (4, 'Metal');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (5, 'Rocha');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (6, 'Madeira');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (7, 'Terra');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (8, 'Fibra');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.mat_constr (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (1, 'Querosene');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (2, 'Álcool');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (3, 'Nafta');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (4, 'Minério');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (5, 'Grãos');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (6, 'Gasolina');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (7, 'Gás');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (8, 'Óleo');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (9, 'Efluentes');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (29, 'Esgoto');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (30, 'Água');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (31, 'Petróleo');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.mat_transp (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (13, 'Rocha');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (14, 'Areia');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (15, 'Areia fina');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (16, 'Lama');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (17, 'Concha');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (18, 'Argila');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (19, 'Lodo');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (20, 'Cascalho');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (21, 'Seixo');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (22, 'Ervas marinhas');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (23, 'Pedra');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (24, 'Coral');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.material_predominante (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (5, 'Portuário');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (6, 'Rodoviário');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (7, 'Ferroviário');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (8, 'Metroviário');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (9, 'Dutos');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (10, 'Hidroviário');  
INSERT INTO dominios.modal_uso (code,code_name) VALUES (11, 'Aeroportuário');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (1, 'Imagem');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (2, 'Radiocomunicação');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (3, 'Som');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (4, 'Telefonia');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (5, 'Dados');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.modalidade (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (1, 'Entroncamento');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (2, 'Entrada de escola');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (3, 'Lombada');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (4, 'Lombada eletrônica');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (5, 'Parada de ônibus');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (6, 'Passagem de nível');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (7, 'Pico de fluxo veículos ');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (8, 'Pista defeituosa');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (9, 'Posto fiscal');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (10, 'Posto policial');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (11, 'Praça de pedágio');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (12, 'Redutor de velocidade ');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (13, 'Redução de número de faixas');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (14, 'Retorno');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (15, 'Saída de veíiculos ');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (16, 'Semáfaro');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (17, 'Entrada  de estacionamento');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (18, 'Entrada de centro comercial');  
INSERT INTO dominios.motivo_retencao (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (1, 'Secundário');  
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (2, 'Terciário');  
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (7, 'Primário');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (3, 'Acupuntura');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (4, 'Alergia e Imunologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (5, 'Anestesiologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (6, 'Angiologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (7, 'Cancerologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (8, 'Cardiologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (9, 'Cirurgia Cardiovascular');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (10, 'Cirurgia Geral');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (11, 'Cirurgia Pediátrica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (12, 'Cirurgia Plástica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (13, 'Cirurgia Torácica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (14, 'Cirurgia Vascular');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (15, 'Cirurgia da Mão');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (16, 'Cirurgia de Cabeça e Pescoço');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (17, 'Cirurgia do Aparelho Digestivo');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (18, 'Clínica Médica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (19, 'Coloproctologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (20, 'Dermatologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (21, 'Endocrinologia e Metabologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (22, 'Endoscopia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (23, 'Gastroenterologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (24, 'Genética Médica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (25, 'Geriatria');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (26, 'Ginecologia e Obstetrícia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (27, 'Hematologia e Hemoterapia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (28, 'Homeopatia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (29, 'Infectologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (30, 'Mastologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (31, 'Medicina Esportiva');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (32, 'Medicina Física e Reabilitação');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (33, 'Medicina Intensiva');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (34, 'Medicina Legal e Perícia Médica');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (35, 'Medicina Nuclear');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (36, 'Medicina Preventiva e Social');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (37, 'Medicina de Família e Comunidade');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (38, 'Medicina de Tráfego');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (39, 'Medicina do Trabalho');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (40, 'Nefrologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (41, 'Neurocirurgia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (42, 'Neurologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (43, 'Nutrologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (44, 'Oftalmologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (45, 'Ortopedia e Traumatologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (46, 'Otorrinolaringologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (47, 'Patologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (48, 'Patologia Clínica/Medicina Laboratorial');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (49, 'Pediatria');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (50, 'Pneumologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (51, 'Psiquiatria');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (52, 'Radiologia e Diagnóstico por Imagem');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (53, 'Radioterapia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (54, 'Reumatologia');  
INSERT INTO dominios.nome_especialidade (code,code_name) VALUES (55, 'Urologia');  
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (1, 'Múltipla');  
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (2, 'Simples');  
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (3, 'Dupla');  
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.poder_publico (code,code_name) VALUES (1, 'Legislativo');  
INSERT INTO dominios.poder_publico (code,code_name) VALUES (2, 'Judiciário');  
INSERT INTO dominios.poder_publico (code,code_name) VALUES (3, 'Executivo');  
INSERT INTO dominios.poder_publico (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.posicao_placa (code,code_name) VALUES (1, 'Aérea sobre via');  
INSERT INTO dominios.posicao_placa (code,code_name) VALUES (2, 'Parede');  
INSERT INTO dominios.posicao_placa (code,code_name) VALUES (3, 'Poste');  
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (1, 'Adjacente à edificação');  
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (2, 'Isolada');  
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (3, 'Sobre edificação');  
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (1, 'Emersa');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (2, 'Subterrânea');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (3, 'Desconhecida');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (4, 'Elevada');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (5, 'Superfície');  
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (6, 'Submersa');  
INSERT INTO dominios.preposicao (code,code_name) VALUES (1, 'Do');  
INSERT INTO dominios.preposicao (code,code_name) VALUES (2, 'Dos');  
INSERT INTO dominios.preposicao (code,code_name) VALUES (3, 'Da');  
INSERT INTO dominios.preposicao (code,code_name) VALUES (4, 'Das');  
INSERT INTO dominios.preposicao (code,code_name) VALUES (5, 'De');  
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (1, 'Manual');  
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (2, 'Mecanizado');  
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.proximidade (code,code_name) VALUES (3, 'Isolada');  
INSERT INTO dominios.proximidade (code,code_name) VALUES (14, 'Adjacente');  
INSERT INTO dominios.proximidade (code,code_name) VALUES (15, 'Coincidente');  
INSERT INTO dominios.proximidade (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (1, 'Mineral');  
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (2, 'Salobra');  
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (3, 'Potável');  
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (4, 'Não potável');  
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (1, 'Nacional');  
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (2, 'Privada');  
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (14, 'Estadual');  
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (15, 'Municipal');  
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (1, 'Arruamento');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (2, 'Limite de massa dágua');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (3, 'Trecho de drenagem');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (4, 'Massa dágua');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (5, 'Cumeada');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (6, 'Linha seca');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (7, 'Costa visível da carta');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (8, 'Trecho rodoviário');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (9, 'Trecho ferroviário');  
INSERT INTO dominios.referencia_legal (code,code_name) VALUES (96, 'Não identificado');  
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (1, 'Imbituba');  
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (3, 'Torres');  
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (5, 'Santana');  
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (99, 'Outra referência');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (2, 'Potsdam1930');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (3, 'IGSN71');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (4, 'Absoluto');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (5, 'Local');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.regime (code,code_name) VALUES (1, 'Temporário com leito permanente');  
INSERT INTO dominios.regime (code,code_name) VALUES (2, 'Permanente');  
INSERT INTO dominios.regime (code,code_name) VALUES (3, 'Permanente com grande variação');  
INSERT INTO dominios.regime (code,code_name) VALUES (4, 'Temporário');  
INSERT INTO dominios.regime (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (2, 'Eclusa');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (3, 'Passagem elevada ou viaduto');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (4, 'Comporta');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (5, 'Queda dágua');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (6, 'Corredeira');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (7, 'Foz marítima');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (8, 'Sumidouro');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (9, 'Meandro abandonado');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (10, 'Lago');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (11, 'Lagoa');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (12, 'Laguna');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (13, 'Represa/açude');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (14, 'Entre trechos de drenagem');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (15, 'Ponte');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (16, 'Confluência');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (17, 'Vertedouro');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (18, 'Pátio');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (19, 'Passagem de nível');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (20, 'Túnel');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (21, 'Barragem');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (22, 'Local crítico');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (23, 'Depósito geral');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (24, 'Travessia');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (25, 'Canal ou vala');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (26, 'Contato com localidade');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (27, 'Edificação rodoviária');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (28, 'Entrocamento');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (29, 'Galeria ou bueiro');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (30, 'Início/fim de trecho');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (31, 'Mudança de UF');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (32, 'Mudança de administração');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (33, 'Mudança de declividade');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (34, 'Mudança de número de faixas');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (35, 'Mudança de revestimento');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (36, 'Mudança de tipo de rodovia');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (37, 'Ramificação');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (38, 'Mudança do número de pistas');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (39, 'Ponto de início de drenagem');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (40, 'Outra mudança de atributo');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (41, 'Desvio Ferroviário');  
INSERT INTO dominios.relacionado (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (1, 'Revestimento primário (solto)');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (2, 'Pavimentado');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (3, 'Madeira');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (4, 'Sem revestimento (leito natural)');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.revestimento (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (1, 'Indústrias de transformação');  
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (2, 'Construção');  
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (3, 'Indústrias extrativas');  
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.setor (code,code_name) VALUES (1, 'Econômico');  
INSERT INTO dominios.setor (code,code_name) VALUES (2, 'Abastecimento de água');  
INSERT INTO dominios.setor (code,code_name) VALUES (3, 'Saneamento básico');  
INSERT INTO dominios.setor (code,code_name) VALUES (4, 'Energético');  
INSERT INTO dominios.setor (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (1, 'SP');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (2, 'TO');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (3, 'AC');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (4, 'AL');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (5, 'AM');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (6, 'AP');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (7, 'BA');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (8, 'CE');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (9, 'DF');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (10, 'ES');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (11, 'GO');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (12, 'MA');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (13, 'MG');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (14, 'MS');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (15, 'MT');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (16, 'PA');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (17, 'PB');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (18, 'PE');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (19, 'PI');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (20, 'PR');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (21, 'RJ');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (22, 'RN');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (23, 'RO');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (24, 'RR');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (25, 'RS');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (26, 'SC');  
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (27, 'SE');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (1, 'Astro Chuá');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (2, 'Córrego Alegre');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (3, 'SAD-69');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (5, 'WGS-84');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (6, 'SIRGAS2000');  
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (99, 'Outra referência');  
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (10, 'Tratada');  
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (11, 'Não tratada');  
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.situacao_costa (code,code_name) VALUES (4, 'Contígua');  
INSERT INTO dominios.situacao_costa (code,code_name) VALUES (5, 'Afastada');  
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (5, 'Emerso');  
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (6, 'Cobre e descobre');  
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (7, 'Submerso');  
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (1, 'Subterrânea');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (2, 'Superposta nivel 1');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (3, 'Superposta nivel 2');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (4, 'Nivel do solo');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (5, 'Adjacente');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (6, 'Superposta nivel 3');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (99, 'Outra');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (1, 'Planejada');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (2, 'Construída');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (3, 'Abandonada');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (4, 'Destruída');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (5, 'Em construção');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (6, 'Construída, mas em obras');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (1, 'Regularizada');  
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (2, 'Homologada ou demarcada');  
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (3, 'Declarada');  
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (4, 'Delimitada');  
INSERT INTO dominios.situacao_logradouro (code,code_name) VALUES (1, 'Em uso');  
INSERT INTO dominios.situacao_logradouro (code,code_name) VALUES (2, 'Cancelado');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (1, 'Não construído');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (2, 'Não visitado');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (3, 'Bom');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (4, 'Destruído');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (5, 'Destruído sem chapa');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (6, 'Destruído com chapa danificada');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (7, 'Não encontrado');  
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.situacao_terreno (code,code_name) VALUES (1, 'Em progressão');  
INSERT INTO dominios.situacao_terreno (code,code_name) VALUES (2, 'Estabilizada');  
INSERT INTO dominios.situacao_terreno (code,code_name) VALUES (3, 'Em regressão');  
INSERT INTO dominios.situacao_terreno (code,code_name) VALUES (95, 'Desconhecida');  
INSERT INTO dominios.tipo_aglom_rur_isol (code,code_name) VALUES (4, 'Núcleo');  
INSERT INTO dominios.tipo_aglom_rur_isol (code,code_name) VALUES (5, 'Povoado');  
INSERT INTO dominios.tipo_aglom_rur_isol (code,code_name) VALUES (22, 'Outros aglomerados rurais isolados');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (24, 'Vala');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (25, 'Canal');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (26, 'Caixa de empréstimo');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (27, 'Extrativismo mineral');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (28, 'Corte');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (29, 'Aterro');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (30, 'Resíduo sólido em geral');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (31, 'Resíduo de bota-fora');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (1, 'Lamacento');  
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (2, 'Arenoso');  
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_area_uso_comun (code,code_name) VALUES (2, 'Terra de remasnecentes quilombolas');  
INSERT INTO dominios.tipo_area_uso_comun (code,code_name) VALUES (3, 'Assentamento rural');  
INSERT INTO dominios.tipo_area_uso_comun (code,code_name) VALUES (99, 'Outras comunidades');  
INSERT INTO dominios.tipo_armario (code,code_name) VALUES (2, 'Rede Eletrica');  
INSERT INTO dominios.tipo_armario (code,code_name) VALUES (3, 'Telefonico');  
INSERT INTO dominios.tipo_armario (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_armario (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_arruamento (code,code_name) VALUES (1, 'Beco');  
INSERT INTO dominios.tipo_arruamento (code,code_name) VALUES (2, 'Logradouro');  
INSERT INTO dominios.tipo_arruamento (code,code_name) VALUES (3, 'Servidão');  
INSERT INTO dominios.tipo_arruamento (code,code_name) VALUES (4, 'Entroncamento');  
INSERT INTO dominios.tipo_arruamento (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_associado (code,code_name) VALUES (37, 'Cidade');  
INSERT INTO dominios.tipo_associado (code,code_name) VALUES (38, 'Vila');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (1, 'Desembarcadouro');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (4, 'Dolfim');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (40, 'Cais');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (41, 'Cais flutuante');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (42, 'Trapiche');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (43, 'Molhe de atracação');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (44, 'Píer');  
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (2, 'Fluvial');  
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (3, 'Cordão arenoso');  
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (4, 'Marítimo');  
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (12, 'Lacustre');  
INSERT INTO dominios.tipo_caminho_aereo (code,code_name) VALUES (1, 'Teleférico');  
INSERT INTO dominios.tipo_caminho_aereo (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (1, 'Sujo');  
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (2, 'Limpo');  
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (3, 'Rupestre');  
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (2, 'Tênis');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (3, 'Futebol');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (4, 'Basquetebol');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (5, 'Voleibol');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (6, 'Pólo');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (7, 'Hipismo');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (8, 'Poliesportiva');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_capital (code,code_name) VALUES (1, 'Capital federal');  
INSERT INTO dominios.tipo_capital (code,code_name) VALUES (2, 'Capital estadual');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (1, 'Horizontal/Vertical');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (2, 'Túmulo  isolado');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (3, 'Comum');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (4, 'Crematório');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (5, 'Parque');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (6, 'Vertical');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_circ_rod (code,code_name) VALUES (1, 'Faixa veiculos lentos');  
INSERT INTO dominios.tipo_circ_rod (code,code_name) VALUES (2, 'Faixa exclusiva onibus');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (5, 'Autodromo');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (6, 'Velódromo');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (7, 'Kartódromo');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (22, 'Estande de Tiro');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (23, 'Hipódromo');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (24, 'Hípica');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (25, 'Campo de Golfe');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (33, 'Campo Aeromodelismo');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_cmplxdesport_lazer (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (3, 'Clube Social');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (4, 'Jardim Botânico');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (5, 'Parque Aquático');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (6, 'Jardim Zoológico');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (7, 'Parque Temático');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (8, 'Marina');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (9, 'Pesque e Pague');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (10, 'Parque Urbano');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_cmplxrecreativo_lazer (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (14, 'Nuclear');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (15, 'Diesel');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (16, 'Gás');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (17, 'Carvão');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_complexo_aeroportuario (code,code_name) VALUES (19, 'Aeroporto');  
INSERT INTO dominios.tipo_complexo_aeroportuario (code,code_name) VALUES (20, 'Aeródromo');  
INSERT INTO dominios.tipo_complexo_aeroportuario (code,code_name) VALUES (21, 'Heliporto');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (1, 'Complexo recreativo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (2, 'Clube social');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (3, 'Autódromo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (4, 'Parque de diversões');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (5, 'Parque urbano');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (6, 'Parque aquático');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (7, 'Parque temático');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (8, 'Hipódromo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (9, 'Hípica');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (10, 'Estande de tiro');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (11, 'Campo de golfe');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (12, 'Kartódromo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (13, 'Camping');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (14, 'Complexo desportivo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (15, 'Pesque-pague');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (16, 'Jardim botânico');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (17, 'Jardim zoológico');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (18, 'Praça');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (19, 'Parque de eventos');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (20, 'Velódromo');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_complexo_lazer (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_complexo_portuario (code,code_name) VALUES (8, 'Instalação portuária');  
INSERT INTO dominios.tipo_complexo_portuario (code,code_name) VALUES (9, 'Porto organizado');  
INSERT INTO dominios.tipo_complexo_portuario (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (11, 'Insumo');  
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (12, 'Produto');  
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (32, 'Resíduo');  
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (1, 'Mestra');  
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (2, 'Normal');  
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (3, 'Auxiliar');  
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (4, 'Cerca');  
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (5, 'Gradil');  
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (6, 'Mureta');  
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (7, 'Muro');  
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (1, 'Tanque');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (2, 'Cisterna');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (3, 'Composteira');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (4, 'Aterro controlado');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (5, 'Depósito de lixo');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (6, 'Reservatório');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (7, 'Depósito frigorífico');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (12, 'Armazém');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (15, 'Caixa dágua');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (26, 'Barracão industrial');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (27, 'Galpão');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (28, 'Silo');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (29, 'Aterro sanitário');  
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (14, 'Muro');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (15, 'Defensa metálica (guard-rail)');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (16, 'Barreira New Jersey');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (17, 'Tacha refletiva (olho de gato)');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (18, 'Tachão refletivo (tartaruga)');  
INSERT INTO dominios.tipo_divisoria (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (2, 'Captação');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (3, 'Tratamento');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (4, 'Recalque');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (7, 'Administrativa');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (8, 'Terminal de passageiros');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (9, 'Terminal de cargas');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (10, 'Torre de controle');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (11, 'Hangar');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (14, 'Sede operacional de fazenda');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (15, 'Aviário');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (16, 'Apiário');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (17, 'Viveiro de plantas');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (18, 'Viveiro para aquicultura');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (19, 'Pocilga');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (20, 'Curral');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (21, 'Moinho');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (1, 'Farmácia');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (2, 'Oficina mecânica');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (3, 'Loja de materiais de construção e/ou ferragem');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (4, 'Centro comercial');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (5, 'Loja de conveniência');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (6, 'Centro de convenções');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (7, 'Motel');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (8, 'Loja de móveis');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (9, 'Supermercado');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (10, 'Centro de exposições');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (11, 'Posto de combustível');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (12, 'Loja de roupas e/ou tecidos');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (13, 'Mercado público');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (14, 'Quiosque');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (15, 'Quitanda');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (16, 'Comércio de carnes');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (17, 'Hotel');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (18, 'Banca de jornal');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (19, 'Venda de veículos');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (20, 'Banco');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (21, 'Pousada');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (22, 'Outros comércios');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (23, 'Outros serviços');  
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (11, 'Centro de operações');  
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (14, 'Central comutação e transmissão');  
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (15, 'Estação rádio base');  
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (20, 'Estação repetidora');  
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (15, 'Oficinas');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (16, 'Segurança');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (17, 'Depósito');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (18, 'Chaminé');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (19, 'Administrativa');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (10, 'Coreto ou tribuna');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (11, 'Espaço de eventos e/ ou cultural');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (12, 'Museu');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (13, 'Concha acústica');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (14, 'Teatro');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (15, 'Anfiteatro');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (19, 'Estádio');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (20, 'Ginásio');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (26, 'Cinema');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (27, 'Centro cultural');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (32, 'Plataforma de pesca');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (33, 'Arquivo');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (34, 'Biblioteca');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (35, 'Conservatório');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (36, 'Galeria');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (37, 'Quiosque');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (4, 'Administrativa');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (5, 'Estação ferroviária de passageiros');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (6, 'Estação metroviária');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (7, 'Terminal ferroviário de cargas');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (8, 'Terminal ferroviário de passageiros e cargas');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (9, 'Oficina de manutenção');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (6, 'Terminal de uso  privativo');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (7, 'Rampa transportadora');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (8, 'Administrativa');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (9, 'Terminal de passageiros');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (10, 'Terminal de cargas');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (11, 'Estaleiro');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (12, 'Carreira');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (13, 'Armazém');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (14, 'Dique de estaleiro');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (6, 'Templo');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (7, 'Igreja');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (8, 'Centro');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (9, 'Mosteiro');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (10, 'Convento');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (11, 'Mesquita');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (12, 'Sinagoga');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (13, 'Capela mortuária');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (14, 'Terreiro ');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (1, 'Posto de pedágio');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (2, 'Administrativa');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (3, 'Garagem');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (17, 'Terminal interestadual');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (18, 'Terminal urbano');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (19, 'Parada interestadual');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (6, 'Recalque');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (7, 'Tratamento de esgoto');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (8, 'Usina de reciclagem');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (9, 'Incinerador');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (12, 'Cruzeiro');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (13, 'Estátua');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (14, 'Mirante');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (15, 'Monumento');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (16, 'Panteão');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (17, 'Chafariz');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (18, 'Chaminé');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (19, 'Escultura');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (20, 'Obelisco');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (21, 'Torre');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (1, 'Chapada');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (2, 'Planalto');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (3, 'Cabo');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (4, 'Falésia');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (5, 'Ilha');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (6, 'Montanha');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (7, 'Planície');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (8, 'Praia');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (9, 'Pico');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (10, 'Dolina');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (11, 'Duna');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (12, 'Rocha');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (13, 'Península');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (14, 'Falha');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (15, 'Fenda');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (16, 'Maciço');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (17, 'Talude');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (18, 'Caverna');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (19, 'Ponta');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (20, 'Morro');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (21, 'Escarpa');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (22, 'Gruta');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (23, 'Serra');  
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_elevador (code,code_name) VALUES (1, 'Inclinado');  
INSERT INTO dominios.tipo_elevador (code,code_name) VALUES (2, 'Vertical');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (1, 'Balsa');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (2, 'Lancha');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (6, 'Empurrador-balsa');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (7, 'Embarcação de pequeno porte');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (1, 'Círculo ');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (2, 'Trevo');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (3, 'Rótula');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (4, 'Entroncamento ferroviário');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (5, 'Outros tipos de entroncamento em nivel');  
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (6, 'Cruzamento ou junção simples');  
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (7, 'Pivô central');  
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (2, 'Voçoroca');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (3, 'Deslizamento');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (4, 'Ravina');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (5, 'Sulco');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_erosao (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (2, 'Termelétrica');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (3, 'Eólica');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (4, 'Hidrelétrica');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (5, 'Maré-motriz');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (6, 'Solar');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (1, 'Terminal');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (2, 'Estação');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (3, 'Comércio e serviços');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (4, 'Parada');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (5, 'Fiscalização');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (10, 'Integração');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (12, 'Porto seco');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_estrut (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (1, 'Coberto');  
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (2, 'Céu aberto');  
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (3, 'Fechado');  
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (1, 'Poço de petróleo');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (2, 'Mina');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (3, 'Poço para água subterrânea');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (4, 'Salina');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (5, 'Garimpo');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (14, 'Poço');  
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (15, 'Poço artesiano');  
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (16, 'Olho dágua');  
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (18, 'Com limite definido');  
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (19, 'Sem limite definido');  
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_gleba (code,code_name) VALUES (20, 'Chácara');  
INSERT INTO dominios.tipo_gleba (code,code_name) VALUES (21, 'Fazenda');  
INSERT INTO dominios.tipo_gleba (code,code_name) VALUES (22, 'Sítio');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (3, 'Municipal');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (23, 'Estadual');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (24, 'Internacional secundário');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (25, 'Internacional de referência');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (26, 'Internacional principal');  
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (1, 'Fluvial');  
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (2, 'Mista');  
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (3, 'Marítima');  
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (4, 'Lacustre');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (5, 'Aquartelamento');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (6, 'Campo de instruçao');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (7, 'Campo de tiro');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (8, 'Base aérea');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (9, 'Distrito naval');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (10, 'Hotel de trânsito');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (11, 'Delegacia de  serviço militar');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (12, 'Quartel general');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (13, 'Posto de vigilância');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (14, 'Posto de policiamento urbano');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (15, 'Posto de policiamento rodoviário');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (16, 'Capitânia dos portos');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (17, 'Base naval');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (20, 'Anual');  
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (21, 'Perene');  
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (22, 'Semi-perene');  
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (3, 'Estação biológica');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (4, 'Área de relevante  interesse ecológico - ARIE');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (5, 'Estrada parque');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (6, 'Reserva de desenvolvimento sustentável - RDS');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (7, 'Reserva extrativista - RESEX');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (8, 'Zoneamento');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (9, 'Reserva particular do patrimônio natural -  RPPN');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (10, 'Reserva ecológica');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (11, 'Reserva florestal');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (12, 'Floresta de rendimento sustentável');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (13, 'Floresta extrativista');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (14, 'Estação ecológica - ESEC ');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (15, 'Área de proteção  ambiental - APA');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (16, 'Parque - PAR');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (17, 'Horto florestal');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (18, 'Monumento natural - MONA');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (19, 'Floresta - FLO');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (20, 'Reserva biológica - REBIO');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (21, 'Refúgio da vida silvestre - RVS');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (22, 'Área militar');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (23, 'Terra pública');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (24, 'Terra indígena');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (25, 'Terra de remanescentes quilombolas');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (26, 'Assentamento rural');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (27, 'Amazônia  legal');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (28, 'Faixa de fronteira');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (29, 'Polígono da seca');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (30, 'Área de preservação permanente');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (31, 'Reserva  legal');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (32, 'Mosaico');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (33, 'Distrito florestal sustentável');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (34, 'Corredor ecológico');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (35, 'Floresta pública');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (36, 'Sitios RAMSAR');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (37, 'Sítios do patrimônio');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (38, 'Reserva de fauna - REFAU');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (39, 'Reserva da biosfera');  
INSERT INTO dominios.tipo_lim_area_esp (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_lim_intra_mun (code,code_name) VALUES (1, 'Distrital');  
INSERT INTO dominios.tipo_lim_intra_mun (code,code_name) VALUES (2, 'Perímetro urbano legal');  
INSERT INTO dominios.tipo_lim_intra_mun (code,code_name) VALUES (3, 'Sub-distrital');  
INSERT INTO dominios.tipo_lim_intra_mun (code,code_name) VALUES (4, 'Bairro');  
INSERT INTO dominios.tipo_lim_intra_mun (code,code_name) VALUES (5, 'Região administrativa');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (1, 'Limite interno entre massas e/ou trechos');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (2, 'Margem direita de trechos de massas dágua');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (3, 'Costa visível da carta');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (4, 'Limite com elemento artificial');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (5, 'Margem esquerda de trechos de massas dágua');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (6, 'Margem de massa dágua');  
INSERT INTO dominios.tipo_lim_massa (code,code_name) VALUES (7, 'Limite interno com foz marítima');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (1, 'Linha limite de terrenos de Marinha (LLTM oceano)');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (2, 'Linha limite de terrenos marginais (LLTM rios)');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (3, 'Linha média de enchentes ordinárias (LMEO)');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (4, 'Setor censitário');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (5, 'Linha de base normal');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (6, 'Linha de base reta');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (7, 'Costa visível da carta (interpretada)');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (8, 'Linha preamar média  - 1831');  
INSERT INTO dominios.tipo_lim_oper (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_lim_pol (code,code_name) VALUES (4, 'Estadual');  
INSERT INTO dominios.tipo_lim_pol (code,code_name) VALUES (5, 'Internacional');  
INSERT INTO dominios.tipo_lim_pol (code,code_name) VALUES (6, 'Municipal');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (1, 'Interferência com localidades');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (2, 'Interferência com vias');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (3, 'Interferência com áreas especiais');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (4, 'Subestação de válvulas e/ou bombas');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (5, 'Interferência com hidrografia');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (6, 'Risco geotécnico');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (8, 'Outras interferências');  
INSERT INTO dominios.tipo_local_critico (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (1, 'Sujeito a deslisamento');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (2, 'Sujeito a explosões');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (3, 'Sujeito a alagamento');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (4, 'Local crítico para dutos');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (5, 'Elevado indice  de acidentes de transito');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (6, 'Criminalidade geral elevada');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (7, 'Criminalidade relacionada ao tráfico de drogas');  
INSERT INTO dominios.tipo_local_risco (code,code_name) VALUES (8, 'Sujeito a incêndio');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (1, 'Beco');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (2, 'Vila');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (3, 'Travessa');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (4, 'Praça');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (5, 'Viaduto');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (7, 'Largo');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (8, 'Rua');  
INSERT INTO dominios.tipo_logradouro (code,code_name) VALUES (9, 'Túnel');  
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (1, 'Manguezal');  
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (2, 'Manguezal tipo apicum');  
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (3, 'Manguezal tipo salguado');  
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_maq_termica (code,code_name) VALUES (5, 'Ciclo combinado (CLCB)');  
INSERT INTO dominios.tipo_maq_termica (code,code_name) VALUES (6, 'Motor de combustão interna (MCIA)');  
INSERT INTO dominios.tipo_maq_termica (code,code_name) VALUES (7, 'Turbina a gás (TBGS)');  
INSERT INTO dominios.tipo_maq_termica (code,code_name) VALUES (8, 'Turbina a vapor (TBVP)');  
INSERT INTO dominios.tipo_maq_termica (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (10, 'Enseada');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (11, 'Meandro abandonado');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (12, 'Lagoa/Lagoa');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (13, 'Trecho massa dágua');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (14, 'Represa/açude');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (15, 'Oceano');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (22, 'Baía');  
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_obst (code,code_name) VALUES (8, 'Natural');  
INSERT INTO dominios.tipo_obst (code,code_name) VALUES (9, 'Artificial');  
INSERT INTO dominios.tipo_operativo (code,code_name) VALUES (4, 'Elevadora');  
INSERT INTO dominios.tipo_operativo (code,code_name) VALUES (5, 'Abaixadora');  
INSERT INTO dominios.tipo_operativo (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (1, 'Cartorial');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (2, 'Gestão');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (3, 'Eleitoral');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (4, 'Produção e/ou pesquisa');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (5, 'Prefeitura');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (6, 'Autarquia');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (7, 'Fundação');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (8, 'Secretaria');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (9, 'Procuradoria');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (10, 'Fórum');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (11, 'Assembleia legislativa');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (12, 'Prisional');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (13, 'Câmara municipal');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (14, 'Policial');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (15, 'Seguridade social');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (16, 'Delegacia de Polícia Civil');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (11, 'Corpo de bombeiros');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (12, 'Exército');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (13, 'Força Aérea');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (14, 'Marinha');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (15, 'Polícia militar');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_org_militar (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (1, 'Asilo');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (2, 'Casa de repouso');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (5, 'Albergue');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (6, 'Orfanato');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_org_sv_social (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (1, 'Zona contígua');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (2, 'Zona econômica exclusiva');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (3, 'Plataforma continental jurídica');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (4, 'Mar territorial');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (5, 'Lateral marítima');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_out_lim_ofic (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (1, 'Sítios do patrimônio');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (2, 'Reserva da biofera');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (3, 'Sítios RAMSAR');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (4, 'Área de preservação permanente - APP');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (5, 'Reserva legal');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (6, 'Mosaico');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (9, 'Corredor ecológico');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (10, 'Floresta pública');  
INSERT INTO dominios.tipo_out_unid_prot (code,code_name) VALUES (11, 'Distrito florestal sustentável');  
INSERT INTO dominios.tipo_passag_viad (code,code_name) VALUES (3, 'Passagem elevada');  
INSERT INTO dominios.tipo_passag_viad (code,code_name) VALUES (4, 'Viaduto');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (2, 'Asfalto');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (3, 'Placa de concreto');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (4, 'Pedra regular');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (5, 'Ladrilho de concreto');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (6, 'Paralelepípedo');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (7, 'Pedra irregular');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (4, 'Térreo');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (5, 'Mesanino');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (6, 'Sobreloja');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (7, 'Subsolo');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (8, 'Andar');  
INSERT INTO dominios.tipo_pavimento (code,code_name) VALUES (9, 'Torre');  
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (3, 'Pista de taxiamento');  
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (4, 'Pista de Pouso');  
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (5, 'Heliponto');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (1, 'Bicicross');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (2, 'Motocross');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (3, 'Ciclismo');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (4, 'Automobilismo');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (5, 'Atletismo');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (6, 'Motociclismo');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (7, 'Corrida de cavalos');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (1, 'Ponto de ônibus');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (2, 'Logradouro');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (3, 'Ponto de táxi');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (4, 'Trânsito');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (5, 'Bairro');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (6, 'Painel eletrônico');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (7, 'Turística');  
INSERT INTO dominios.tipo_placa (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (1, 'Petróleo');  
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (2, 'Gás');  
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (3, 'Horizontal');  
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (4, 'Vertical');  
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (7, 'Estaíada');  
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (8, 'Fixa');  
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (9, 'Móvel');  
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (10, 'Pênsil');  
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (12, 'Iluminação');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (13, 'Ornamental');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (14, 'Rede Eletrica');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (15, 'Sinalização');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (19, 'Fiscalização sanitária');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (20, 'Posto de pesagem');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (21, 'Tributação');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (1, 'Sal-gema');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (2, 'Terras raras');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (3, 'Titânio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (4, 'Topázio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (5, 'Tungstênio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (6, 'Turmalina');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (7, 'Tório');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (8, 'Urânio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (9, 'Opala');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (10, 'Zinco');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (11, 'Zircônio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (12, 'Níquel');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (13, 'Querosene');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (14, 'Água mineral');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (15, 'Óleo diesel');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (16, 'Vermiculita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (17, 'Ágata');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (18, 'Água');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (19, 'Nióbio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (20, 'Rocha ornamental');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (24, 'Ouro');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (25, 'Petróleo');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (26, 'Pedra preciosa');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (27, 'Gás');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (28, 'Grão');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (29, 'Alexandrita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (30, 'Ametista');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (31, 'Amianto');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (32, 'Argila');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (33, 'Barita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (34, 'Bentonita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (35, 'Calcário');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (36, 'Carvão vegetal');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (37, 'Caulim');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (38, 'Vinhoto');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (39, 'Estrume');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (40, 'Cascalho');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (41, 'Chumbo');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (42, 'Inseticida');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (43, 'Folhagem');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (44, 'Água marinha');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (45, 'Pedra (brita)');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (46, 'Granito');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (47, 'Mármore');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (48, 'Bauxita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (49, 'Manganês');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (50, 'Talco');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (51, 'Chorume');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (52, 'Gasolina');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (53, 'Álcool');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (54, 'Citrino');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (55, 'Cobre');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (56, 'Carvão mineral');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (57, 'Sal');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (58, 'Turfa');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (59, 'Escória');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (60, 'Ferro');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (61, 'Crisoberilo');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (62, 'Prata');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (63, 'Cristal de rocha');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (64, 'Forragem');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (65, 'Saibro/piçarra');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (66, 'Areia');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (67, 'Cromo');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (68, 'Diamante');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (69, 'Diatomita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (70, 'Dolomito');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (71, 'Esgoto');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (72, 'Esmeralda');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (73, 'Estanho');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (74, 'Feldspato');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (75, 'Fosfato');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (76, 'Gipsita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (77, 'Grafita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (78, 'Granada');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (79, 'Lixo domiciliar e comercial');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (80, 'Lixo séptico');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (81, 'Lixo tóxico');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (82, 'Lítio');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (83, 'Magnesita');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (84, 'Mica');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_pto_controle (code,code_name) VALUES (4, 'Centro perspectivo');  
INSERT INTO dominios.tipo_pto_controle (code,code_name) VALUES (5, 'Ponto de controle');  
INSERT INTO dominios.tipo_pto_controle (code,code_name) VALUES (6, 'Ponto fotogramétrico');  
INSERT INTO dominios.tipo_pto_controle (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (1, 'Eólica - EO');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (2, 'Solarimétrica - SL');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (3, 'Maregráfica - MA');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (4, 'Pluviométrica - PL');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (5, 'Radiossonda - RS');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (6, 'Metero-maregráfica');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (7, 'Agroclimatológica - AC');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (8, 'Radar metereológico - RD');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (9, 'Marés terrestres-crosta');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (10, 'Climatológica auxiliar- CA');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (11, 'Evaporimétrica - EV');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (12, 'Fluviométrica - FL');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (13, 'Climatológica principal - CP');  
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (1, 'Ponto astronômico - PA');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (2, 'Estação gravimétrica - EG');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (3, 'Referência de nível - RN');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (4, 'Vértice de triangulação - VT');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (5, 'Ponto barométrico - B');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (6, 'Estação de poligonal - EP');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (7, 'Ponto de satélite - SAT');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (8, 'Ponto trigonométrico - RV');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (2, 'Quebramar');  
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (4, 'Espigão');  
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (6, 'Molhe');  
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (1, 'Catarata');  
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (2, 'Salto');  
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (3, 'Cachoeira');  
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (4, 'Arenito');  
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (12, 'Coral');  
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (18, 'Rochoso');  
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (1, 'Planimétrico');  
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (22, 'Planialtimétrico');  
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (23, 'Altimétrico');  
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (24, 'Gravimétrico');  
INSERT INTO dominios.tipo_rep_diplomatica (code,code_name) VALUES (1, 'Embaixada');  
INSERT INTO dominios.tipo_rep_diplomatica (code,code_name) VALUES (2, 'Consulado');  
INSERT INTO dominios.tipo_restricao_circ (code,code_name) VALUES (22, 'Faixa exclusiva para onibus');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (2, 'Sinalização de margem');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (3, 'Farol ou farolete');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (4, 'Bóia de amarração');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (20, 'Bóia cega');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (21, 'Bóia luminosa');  
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_subunidade (code,code_name) VALUES (1, 'Apartamento');  
INSERT INTO dominios.tipo_subunidade (code,code_name) VALUES (5, 'Casa');  
INSERT INTO dominios.tipo_subunidade (code,code_name) VALUES (7, 'Loja');  
INSERT INTO dominios.tipo_sum_vert (code,code_name) VALUES (8, 'Sumidouro');  
INSERT INTO dominios.tipo_sum_vert (code,code_name) VALUES (10, 'Vertedouro');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (2, 'Areia');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (4, 'Terra');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (7, 'Cascalho');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (8, 'Saibro');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (9, 'Pedregoso');  
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_torre (code,code_name) VALUES (1, 'Autoportante');  
INSERT INTO dominios.tipo_torre (code,code_name) VALUES (2, 'Estaiada');  
INSERT INTO dominios.tipo_torre (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (1, 'Passageiro');  
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (3, 'Carga');  
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (98, 'Misto');  
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (4, 'Balsa');  
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (5, 'Vau construída');  
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (6, 'Bote transportador');  
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (8, 'Vau natural');  
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (1, 'Passarela em Área Úmida');  
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (8, 'Pinguela');  
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (9, 'Passagem subterrânea');  
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (10, 'Passarela');  
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (1, 'Telefônica');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (2, 'Sinal de TV');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (3, 'Dados');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (98, 'Mista');  
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (4, 'Curso dágua');  
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (5, 'Pluvial');  
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (1, 'Calha');  
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (2, 'Duto');  
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (3, 'Correia transportadora');  
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (5, 'Galeria ou bueiro');  
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (1, 'Trecho para aeromóvel');  
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (2, 'Trecho para bonde');  
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (3, 'Trecho para metrô');  
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (4, 'Trecho para trem');  
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_trecho_massa (code,code_name) VALUES (5, 'Laguna');  
INSERT INTO dominios.tipo_trecho_massa (code,code_name) VALUES (6, 'Represa/açude');  
INSERT INTO dominios.tipo_trecho_massa (code,code_name) VALUES (7, 'Rio');  
INSERT INTO dominios.tipo_trecho_massa (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_trecho_rod (code,code_name) VALUES (1, 'Auto-estrada');  
INSERT INTO dominios.tipo_trecho_rod (code,code_name) VALUES (3, 'Rodovia');  
INSERT INTO dominios.tipo_trecho_rod (code,code_name) VALUES (4, 'Entroncamento');  
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (2, 'Estação ecológica - ESEC');  
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (4, 'Monumento natural - MONA');  
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (5, 'Parque - PAR');  
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (6, 'Refúgio de vida silvestre - RVS');  
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (7, 'Reserva biológica - REBIO');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (8, 'Unidade de conservação');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (9, 'Unidade de conservação SNUC');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (10, 'Unidade de conservação não SNUC');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (11, 'Unidade de proteção integral');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (12, 'Unidade de uso sustentável');  
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (99, 'Outras unidades protegidas');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (1, 'Área de relevante interesse ecológico - ARIE');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (2, 'Floresta - FLO');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (3, 'Reserva de desenvolvimento sustentável - RDS');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (4, 'Reserva extrativita - RESEX');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (5, 'Reserva de fauna - REFAU');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (6, 'Reserva particular de patrimônio - RPPN');  
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (14, 'Área de proteção ambiental - APA');  
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (4, 'Próprio nacional');  
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (5, 'Uso  do município');  
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (6, 'Uso da UF');  
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (7, 'Uso da União');  
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (1, 'Vegetação cultivada');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (2, 'Floresta');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (3, 'Vegetação de mangue');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (4, 'Refúgio ecológico');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (5, 'Campinarana');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (6, 'Cerrado');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (7, 'Vegetação de restinga');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (8, 'Estepe');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (9, 'Vegetação de brejo ou pântano');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (10, 'Caatinga');  
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.tipo_via_rod (code,code_name) VALUES (6, 'Via expressa');  
INSERT INTO dominios.tipo_via_rod (code,code_name) VALUES (10, 'Via arterial');  
INSERT INTO dominios.tipo_via_rod (code,code_name) VALUES (11, 'Via marginal');  
INSERT INTO dominios.tipo_via_rod (code,code_name) VALUES (12, 'Via coletora');  
INSERT INTO dominios.titulo (code,code_name) VALUES (0, 'Padre');  
INSERT INTO dominios.titulo (code,code_name) VALUES (1, 'Almirante');  
INSERT INTO dominios.titulo (code,code_name) VALUES (2, 'Professor');  
INSERT INTO dominios.titulo (code,code_name) VALUES (3, 'Brigadeiro');  
INSERT INTO dominios.titulo (code,code_name) VALUES (4, 'Marechal');  
INSERT INTO dominios.titulo (code,code_name) VALUES (5, 'Irmã');  
INSERT INTO dominios.titulo (code,code_name) VALUES (6, 'Coronel');  
INSERT INTO dominios.titulo (code,code_name) VALUES (10, 'Frei');  
INSERT INTO dominios.titulo (code,code_name) VALUES (11, 'Prefeito');  
INSERT INTO dominios.titulo (code,code_name) VALUES (12, 'Governador');  
INSERT INTO dominios.titulo (code,code_name) VALUES (13, 'Presidente');  
INSERT INTO dominios.trafego (code,code_name) VALUES (2, 'Periódico');  
INSERT INTO dominios.trafego (code,code_name) VALUES (3, 'Permanente');  
INSERT INTO dominios.trafego (code,code_name) VALUES (4, 'Temporário');  
INSERT INTO dominios.trafego (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (6, 'Litro');  
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (7, 'Metro cúbico');  
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (1, 'Particular');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (2, 'Público/militar');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (3, 'Militar');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (4, 'Público');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (5, 'Público e Militar');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (6, 'Público e Civil');  
INSERT INTO dominios.uso_pista (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (0, 'Lazer');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (1, 'Irrigação');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (5, 'Energia');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (6, 'Abastecimento');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (7, 'Dessedentação animal');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (8, 'Drenagem');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (95, 'Desconhecido');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (97, 'Não aplicável');  
INSERT INTO dominios.uso_principal (code,code_name) VALUES (99, 'Outros');  
INSERT INTO dominios.tipo_tunel (code,code_name) VALUES (1, 'Passagem Subterrânea');  
INSERT INTO dominios.tipo_tunel (code,code_name) VALUES (2, 'Túnel')  
