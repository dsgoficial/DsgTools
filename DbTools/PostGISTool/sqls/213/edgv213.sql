CREATE SCHEMA topology;
ALTER SCHEMA topology OWNER TO postgres;
CREATE SCHEMA dominios;
CREATE SCHEMA complexos;
ALTER SCHEMA complexos OWNER TO postgres;
CREATE SCHEMA cb;
CREATE EXTENSION IF NOT EXISTS postgis;
COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';
CREATE EXTENSION IF NOT EXISTS postgis_topology;
COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';
SET search_path TO pg_catalog,public,topology,dominios,complexos,cb;
CREATE TABLE cb.hid_area_umida_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoareaumida smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_area_umida_a_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_area_umida_a OWNER TO postgres;
CREATE TABLE cb.hid_banco_areia(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint,
	tipobanco smallint,
	situacaoemagua smallint,
	materialpredominante smallint,
	CONSTRAINT hid_banco_areia_l_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_banco_areia OWNER TO postgres;
CREATE TABLE cb.hid_recife(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tiporecife smallint NOT NULL DEFAULT 0,
	situamare smallint NOT NULL,
	situacaocosta smallint NOT NULL DEFAULT 0,
	CONSTRAINT hid_recife_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_recife OWNER TO postgres;
CREATE TABLE cb.hid_barragem(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	matconstr smallint NOT NULL,
	usoprincipal smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_complexo_gerad_energ_eletr uuid,
	CONSTRAINT hid_barragem_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_barragem OWNER TO postgres;
CREATE TABLE cb.hid_comporta(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint,
	operacional smallint,
	situacaofisica smallint,
	CONSTRAINT hid_comporta_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
)WITH ( OIDS = TRUE );
ALTER TABLE cb.hid_comporta OWNER TO postgres;
CREATE TABLE cb.hid_queda_dagua(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoqueda smallint NOT NULL,
	altura real,
	CONSTRAINT hid_queda_dagua_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_queda_dagua OWNER TO postgres;
CREATE TABLE cb.hid_corredeira(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	CONSTRAINT hid_corredeira_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_corredeira OWNER TO postgres;
CREATE TABLE cb.hid_fonte_dagua_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipofontedagua smallint NOT NULL,
	qualidagua smallint NOT NULL,
	regime smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_fonte_dagua_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_fonte_dagua_p OWNER TO postgres;
CREATE TABLE cb.hid_foz_maritima(
	id serial NOT NULL,
	nome character(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	CONSTRAINT hid_foz_maritima_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_foz_maritima OWNER TO postgres;
CREATE TABLE cb.rel_elemento_fisiografico(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	CONSTRAINT rel_elemento_fisiografico_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.hid_limite_massa_dagua_l(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	tipolimmassa smallint NOT NULL,
	materialpredominante smallint NOT NULL,
	alturamediamargem real,
	nomeabrev varchar(50),
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_limite_massa_dagua_l_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_limite_massa_dagua_l OWNER TO postgres;
CREATE TABLE cb.hid_massa_dagua_a(
	id serial NOT NULL,
	nome character(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipomassadagua smallint NOT NULL,
	regime smallint NOT NULL,
	salinidade smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_massa_dagua_a_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_massa_dagua_a OWNER TO postgres;
CREATE TABLE cb.hid_ponto_drenagem_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint,
	relacionado smallint,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_ponto_drenagem_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_ponto_drenagem_p OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe(
	id serial NOT NULL,
	nome character(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoquebramolhe smallint NOT NULL,
	matconstr smallint NOT NULL,
	situamare smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	CONSTRAINT hid_quebramar_molhe_a_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_quebramar_molhe OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_quebramar_molhe_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_quebramar_molhe)
;
ALTER TABLE cb.hid_quebramar_molhe_l OWNER TO postgres;
CREATE TABLE cb.hid_queda_dagua_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_queda_dagua_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE TABLE cb.hid_recife_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_recife_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
CREATE TABLE cb.rel_elemento_fisiog_natural(
	tipoelemnat smallint NOT NULL DEFAULT 99,
	CONSTRAINT rel_elemento_fisiog_natural_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiografico)
;
CREATE TABLE cb.hid_reservatorio_hidrico_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint,
	usoprincipal smallint,
	volumeutil integer,
	namaximomaximorum integer,
	namaximooperacional integer,
	id_complexo_gerad_energ_eletr uuid NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_reservatorio_hidrico_a_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_reservatorio_hidrico_a OWNER TO postgres;
CREATE TABLE cb.hid_trecho_massa_dagua_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipotrechomassa smallint NOT NULL,
	regime smallint NOT NULL,
	salinidade smallint NOT NULL,
	id_trecho_curso_dagua uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_trecho_massa_dagua_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.hid_trecho_massa_dagua_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_barragem_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE TABLE cb.hid_sumidouro_vertedouro_p(
	id serial NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tiposumvert smallint NOT NULL,
	causa smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_sumidouro_vertedouro_p_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
)WITH ( OIDS = TRUE );
ALTER TABLE cb.hid_sumidouro_vertedouro_p OWNER TO postgres;
CREATE TABLE cb.hid_terreno_suj_inundacao_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	periodicidadeinunda character(20),
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_terreno_sujeito_inundacao_a_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_terreno_suj_inundacao_a OWNER TO postgres;
CREATE TABLE cb.hid_trecho_drenagem_l(
	id serial NOT NULL,
	nome character(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	coincidecomdentrode smallint NOT NULL,
	dentrodepoligono smallint NOT NULL,
	compartilhado smallint NOT NULL,
	eixoprincipal smallint NOT NULL,
	navegabilidade smallint NOT NULL DEFAULT 0,
	caladomax real,
	regime smallint NOT NULL DEFAULT 0,
	larguramedia real,
	velocidademedcorrente real,
	profundidademedia real,
	id_trecho_curso_dagua uuid,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_trecho_drenagem_l_pkey PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
ALTER TABLE cb.hid_trecho_drenagem_l OWNER TO postgres;
CREATE TABLE cb.hid_quebramar_molhe_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_quebramar_molhe_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_quebramar_molhe)
;
ALTER TABLE cb.hid_quebramar_molhe_a OWNER TO postgres;
CREATE TABLE cb.hid_banco_areia_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_banco_areia_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_banco_areia)
;
CREATE TABLE cb.hid_banco_areia_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_banco_areia_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_banco_areia)
;
ALTER TABLE cb.hid_banco_areia_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_barragem_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE TABLE cb.hid_recife_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_recife_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
ALTER TABLE cb.hid_recife_l OWNER TO postgres;
CREATE TABLE cb.hid_recife_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_recife_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_recife)
;
ALTER TABLE cb.hid_recife_a OWNER TO postgres;
CREATE TABLE cb.hid_barragem_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_barragem_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_barragem)
;
CREATE TABLE cb.rel_alter_fisiog_antropica(
	tipoalterantrop smallint NOT NULL DEFAULT 0,
	CONSTRAINT rel_alter_fisiog_antropica_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiografico)
;
CREATE TABLE cb.rel_elemento_fisiog_natural_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT rel_elemento_fisiog_natural_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE TABLE cb.hid_comporta_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_comporta_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_comporta)
WITH ( OIDS = TRUE );
CREATE TABLE cb.hid_queda_dagua_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_queda_dagua_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE TABLE cb.hid_queda_dagua_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_queda_dagua_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_queda_dagua)
;
CREATE TABLE cb.hid_corredeira_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_corredeira_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE TABLE cb.hid_corredeira_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_corredeira_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE TABLE cb.hid_comporta_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_comporta_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_comporta)
WITH ( OIDS = TRUE );
ALTER TABLE cb.hid_comporta_l OWNER TO postgres;
CREATE TABLE cb.hid_corredeira_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_corredeira_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_corredeira)
;
CREATE TABLE cb.hid_ponto_inicio_drenagem_p(
	nascente smallint NOT NULL DEFAULT 0,
	CONSTRAINT hid_ponto_inicio_drenagem_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_ponto_drenagem_p)
;
CREATE TABLE cb.hid_confluencia_p(
	CONSTRAINT hid_confluencia_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_ponto_drenagem_p)
;
CREATE TABLE cb.hid_foz_maritima_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_foz_maritima_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE TABLE cb.hid_foz_maritima_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_foz_maritima_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE TABLE cb.hid_foz_maritima_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_foz_maritima_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_foz_maritima)
;
CREATE TABLE cb.veg_vegetacao_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	denso smallint NOT NULL,
	antropizada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT veg_vegetacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.veg_veg_cultivada_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipolavoura smallint NOT NULL DEFAULT 0,
	finalidade smallint NOT NULL DEFAULT 0,
	terreno smallint NOT NULL,
	classificacaoporte smallint NOT NULL,
	espacamentoindividuos real,
	espessuradap real,
	denso smallint NOT NULL,
	alturamediaindividuos real,
	cultivopredominante smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT veg_veg_cultivada_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.veg_veg_area_contato_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	classificacaoporte smallint NOT NULL,
	denso smallint NOT NULL,
	alturamediaindividuos real,
	antropizada smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT veg_veg_area_contato_pk PRIMARY KEY (id)
);
CREATE TABLE cb.veg_campo_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipocampo smallint NOT NULL,
	ocorrenciaem smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT veg_campo_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.veg_cerrado_cerradao_a(
	tipocerr smallint NOT NULL,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_cerrado_cerradao_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_caatinga_a(
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_caatinga_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_campinarana_a(
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_campinarana_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_veg_restinga_a(
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_veg_restinga_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_mangue_a(
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_mangue_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_brejo_pantano_a(
	tipobrejopantano smallint NOT NULL DEFAULT 0,
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_brejo_pantano_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.veg_floresta_a(
	especiepredominante smallint NOT NULL,
	caracteristicafloresta smallint NOT NULL,
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_floresta_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
CREATE TABLE cb.rel_isolinha_hipsometrica(
	id serial NOT NULL,
	CONSTRAINT rel_isolinha_hipsometrica_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.rel_curva_nivel_l(
	geometriaaproximada smallint NOT NULL,
	cota integer NOT NULL,
	depressao smallint NOT NULL,
	indice smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT rel_curva_nivel_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_isolinha_hipsometrica)
;
CREATE TABLE cb.rel_curva_batimetrica_l(
	profundidade integer,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT rel_curva_batimetrica_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_isolinha_hipsometrica)
;
CREATE TABLE cb.rel_terreno_exposto_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 1,
	tipoterrexp smallint NOT NULL DEFAULT 0,
	causaexposicao smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT rel_terreno_exposto_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.rel_ponto_hipsometrico(
	id serial NOT NULL,
	CONSTRAINT rel_ponto_hipsometrico_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.rel_ponto_cotado_batimetrico_p(
	profundidade float,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT rel_ponto_cotado_batimetrico_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_ponto_hipsometrico)
;
CREATE TABLE cb.rel_ponto_cotado_altimetrico_p(
	geometriaaproximada smallint NOT NULL,
	cotacomprovada smallint NOT NULL,
	cota float,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT rel_ponto_cotado_altimetrico_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_ponto_hipsometrico)
;
CREATE TABLE cb.rel_elemento_fisiog_natural_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT rel_elemento_fisiog_natural_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE TABLE cb.rel_rocha_p(
	tiporocha smallint NOT NULL,
	CONSTRAINT rel_rocha_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.loc_edificacao(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	matconstr smallint NOT NULL,
	CONSTRAINT edificacao_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.rel_alter_fisiog_antropica_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT rel_alter_fisiog_antropica_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica)
;
CREATE TABLE cb.rel_alter_fisiog_antropica_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT rel_alter_fisiog_antropica_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_alter_fisiog_antropica)
;
CREATE TABLE cb.eco_ext_mineral(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tiposecaocnae smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipoextmin smallint NOT NULL,
	tipoprodutoresiduo smallint NOT NULL,
	tipopocomina smallint NOT NULL,
	procextracao smallint NOT NULL,
	formaextracao smallint NOT NULL,
	atividade smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_pk PRIMARY KEY (id)
);
CREATE TABLE cb.loc_edificacao_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT loc_edificacao_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao)
;
CREATE TABLE cb.rel_duna_p(
	fixa smallint NOT NULL,
	CONSTRAINT rel_duna_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.loc_edificacao_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_edificacao_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao)
;
CREATE TABLE cb.rel_elemento_fisiog_natural_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT rel_elemento_fisiog_natural_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural)
;
CREATE TABLE cb.rel_gruta_caverna_p(
	tipogrutacaverna smallint NOT NULL,
	CONSTRAINT rel_gruta_caverna_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.asb_edif_abast_agua_p(
	tipoedifabast smallint NOT NULL,
	id_complexo_abast_agua uuid,
	CONSTRAINT asb_edif_abast_agua_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.asb_edif_saneamento_p(
	tipoedifsaneam smallint NOT NULL,
	id_complexo_saneamento uuid,
	CONSTRAINT asb_edif_saneamento_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.rel_duna_a(
	fixa smallint NOT NULL,
	CONSTRAINT rel_duna_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cb.hid_ilha_l(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid,
	CONSTRAINT hid_ilha_l_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_l)
;
ALTER TABLE cb.hid_ilha_l OWNER TO postgres;
CREATE TABLE cb.hid_ilha_a(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid,
	CONSTRAINT hid_ilha_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
ALTER TABLE cb.hid_ilha_a OWNER TO postgres;
CREATE TABLE cb.rel_dolina_a(
	CONSTRAINT rel_dolina_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cb.rel_rocha_a(
	tiporocha smallint NOT NULL,
	CONSTRAINT rel_rocha_a_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_a)
;
CREATE TABLE cb.rel_pico_p(
	CONSTRAINT rel_pico_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.sau_edif_saude_p(
	tipoclassecnae smallint NOT NULL,
	nivelatencao smallint NOT NULL,
	id_org_saude uuid,
	CONSTRAINT sau_edif_saude_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.sau_edif_servico_social_p(
	tipoclassecnae smallint NOT NULL,
	id_org_servico_social uuid,
	CONSTRAINT sau_edif_servico_social_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.hid_ilha_p(
	tipoilha smallint NOT NULL DEFAULT 1,
	id_complexo_hid_arquipelago uuid,
	CONSTRAINT hid_ilha_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
ALTER TABLE cb.hid_ilha_p OWNER TO postgres;
CREATE TABLE cb.rel_dolina_p(
	CONSTRAINT rel_dolina_p_pk PRIMARY KEY (id)
) INHERITS(cb.rel_elemento_fisiog_natural_p)
;
CREATE TABLE cb.asb_edif_abast_agua_a(
	tipoedifabast smallint NOT NULL,
	id_complexo_abast_agua uuid NOT NULL,
	CONSTRAINT asb_edif_abast_agua_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.asb_edif_saneamento_a(
	tipoedifsaneam smallint NOT NULL,
	id_complexo_saneamento uuid,
	CONSTRAINT asb_edif_saneamento_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.adm_edif_pub_militar_p(
	tipousoedif smallint NOT NULL,
	tipoedifmil smallint NOT NULL,
	id_org_pub_militar uuid,
	CONSTRAINT adm_edif_pub_militar_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.adm_edif_pub_militar_a(
	tipoedifmil smallint NOT NULL,
	tipousoedif smallint NOT NULL,
	id_org_pub_militar uuid,
	CONSTRAINT adm_edif_pub_militar_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.sau_edif_servico_social_a(
	tipoclassecnae smallint NOT NULL,
	id_org_servico_social uuid,
	CONSTRAINT sau_edif_servico_social_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.edu_edif_ensino_a(
	tipoclassecnae smallint NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT edu_edif_ensino_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.adm_edif_pub_civil_p(
	tipoedifcivil smallint NOT NULL,
	tipousoedif smallint NOT NULL,
	id_org_pub_civil uuid,
	CONSTRAINT adm_edif_pub_civil_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.adm_edif_pub_civil_a(
	tipoedifcivil smallint NOT NULL,
	tipousoedif smallint NOT NULL,
	id_org_pub_civil uuid,
	CONSTRAINT adm_edif_pub_civil_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.edu_edif_religiosa_p(
	tipoedifrelig smallint NOT NULL,
	ensino smallint NOT NULL,
	religiao varchar(80),
	id_org_religiosa uuid,
	CONSTRAINT edu_edif_religiosa_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.sau_edif_saude_a(
	tipoclassecnae smallint NOT NULL,
	nivelatencao smallint NOT NULL,
	id_org_saude uuid,
	CONSTRAINT sau_edif_saude_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.edu_edif_religiosa_a(
	tipoedifrelig smallint NOT NULL,
	ensino smallint NOT NULL,
	religiao varchar(80),
	id_org_religiosa uuid,
	CONSTRAINT edu_edif_religiosa_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.edu_edif_const_lazer_p(
	tipoediflazer smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_edif_const_lazer_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.edu_edif_const_lazer_a(
	tipoediflazer smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_edif_const_lazer_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.hid_rocha_em_agua(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	situacaoemagua smallint NOT NULL,
	alturalamina real,
	CONSTRAINT hid_rocha_em_agua_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.hid_rocha_em_agua_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_rocha_em_agua_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_rocha_em_agua)
;
ALTER TABLE cb.hid_rocha_em_agua_a OWNER TO postgres;
CREATE TABLE cb.edu_edif_const_turistica_p(
	tipoedifturist smallint NOT NULL,
	ovgd smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_edif_const_turistica_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.edu_edif_const_turistica_a(
	tipoedifturist smallint NOT NULL,
	ovgd smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_edif_const_turistica_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.eco_edif_comerc_serv_p(
	tipoedifcomercserv smallint NOT NULL,
	finalidade smallint NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT eco_edif_comerc_serv_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.eco_edif_comerc_serv_a(
	tipoedifcomercserv smallint NOT NULL,
	finalidade smallint NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT eco_edif_comerc_serv_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.pto_edif_constr_est_med_fen_p(
	CONSTRAINT pto_edif_constr_est_med_fen_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.pto_edif_constr_est_med_fen_a(
	CONSTRAINT pto_edif_constr_est_med_fen_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.asb_dep_abast_agua(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipodepabast smallint NOT NULL,
	situacaoagua smallint NOT NULL,
	construcao smallint NOT NULL,
	matconstr smallint NOT NULL,
	finalidade smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	operacional smallint NOT NULL,
	id_complexo_abast_agua uuid,
	CONSTRAINT asb_dep_abast_agua_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.asb_dep_abast_agua_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT asb_dep_abast_agua_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_abast_agua)
;
CREATE TABLE cb.asb_dep_saneamento(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipodepsaneam smallint NOT NULL,
	construcao smallint NOT NULL,
	matconstr smallint NOT NULL,
	finalidade smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	residuo smallint NOT NULL,
	tiporesiduo smallint NOT NULL,
	id_complexo_saneamento uuid,
	CONSTRAINT asb_dep_saneamento_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.asb_dep_saneamento_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT asb_dep_saneamento_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_saneamento)
;
CREATE TABLE cb.eco_deposito_geral(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipodepgeral smallint NOT NULL,
	matconstr smallint NOT NULL,
	tipoexposicao smallint NOT NULL,
	tipoprodutoresiduo smallint NOT NULL,
	tipoconteudo smallint NOT NULL,
	unidadevolume smallint,
	valorvolume float,
	tratamento smallint NOT NULL,
	id_org_comerc_serv uuid,
	id_org_ext_mineral uuid,
	id_org_agrop_ext_veg_pesca uuid,
	id_complexo_gerad_energ_eletr uuid,
	id_estrut_transporte uuid,
	CONSTRAINT eco_deposito_geral_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_deposito_geral_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_deposito_geral_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_deposito_geral)
;
CREATE TABLE complexos.eco_org_industrial(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tiposecaocnae smallint NOT NULL,
	id_org_pub_civil uuid,
	id_org_pub_militar uuid,
	CONSTRAINT eco_org_industrial_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.eco_madeireira(
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_madeireira_pk PRIMARY KEY (id)
) INHERITS(complexos.eco_org_industrial)
;
CREATE TABLE cb.eco_equip_agropec(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipoequipagropec smallint NOT NULL,
	matconstr smallint NOT NULL,
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_equip_agropec_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_equip_agropec_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT eco_equip_agropec_l_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE TABLE cb.eco_equip_agropec_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_equip_agropec_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE TABLE cb.eco_plataforma(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoplataforma smallint NOT NULL,
	CONSTRAINT eco_plataforma_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_plataforma_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_plataforma_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_plataforma)
;
CREATE TABLE complexos.edu_org_ensino(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	administracao smallint NOT NULL,
	tipogrupocnae smallint NOT NULL,
	CONSTRAINT edu_org_ensino_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.adm_org_pub_militar(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipoclassecnae smallint NOT NULL,
	administracao smallint NOT NULL,
	id_org_pub_militar uuid,
	id_instituicao_publica uuid,
	instituicao smallint NOT NULL,
	classficsigiloso smallint NOT NULL,
	CONSTRAINT adm_org_pub_militar_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.adm_org_pub_civil(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipoclassecnae smallint NOT NULL,
	administracao smallint NOT NULL,
	poderpublico smallint NOT NULL,
	id_instituicao_publica uuid,
	id_org_pub_civil uuid,
	CONSTRAINT adm_org_pub_civil_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.edu_org_religiosa(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipoclassecnae smallint NOT NULL,
	CONSTRAINT adm_org_religiosa_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_grupo_transformadores(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	id_subestacao_ener_eletr uuid,
	CONSTRAINT enc_grupo_transformadores_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_grupo_transformadores_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT enc_grupo_transformadores_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_grupo_transformadores)
;
CREATE TABLE cb.enc_est_gerad_energia_eletr(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoestgerad smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	destenergelet smallint NOT NULL,
	codigoestacao varchar(80),
	potenciaoutorgada float,
	potenciafiscalizada float,
	id_complexo_gerad_energ_eletr uuid,
	CONSTRAINT enc_est_gerad_energia_eletrica_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_est_gerad_energia_eletr_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_l_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE TABLE cb.enc_est_gerad_energia_eletr_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE TABLE cb.enc_termeletrica_a(
	tipocombustivel smallint NOT NULL,
	combrenovavel smallint NOT NULL,
	tipomaqtermica smallint NOT NULL,
	geracao smallint NOT NULL,
	CONSTRAINT enc_termeletrica_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_a)
;
CREATE TABLE cb.enc_est_gerad_energia_eletr_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT enc_est_gerad_energia_eletr_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr)
;
CREATE TABLE cb.enc_hidreletrica_p(
	codigohidreletrica varchar(30),
	CONSTRAINT enc_hidreletrica_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_p)
;
CREATE TABLE cb.enc_hidreletrica_l(
	codigohidreletrica varchar(30),
	CONSTRAINT enc_hidreletrica_l_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_l)
;
CREATE TABLE cb.enc_hidreletrica_a(
	codigohidreletrica varchar(30),
	CONSTRAINT enc_hidreletrica_a_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_a)
;
CREATE TABLE cb.enc_edif_energia_p(
	tipoedifenergia smallint NOT NULL DEFAULT 0,
	id_complexo_gerad_energ_eletr uuid,
	id_subestacao_ener_eletr uuid,
	CONSTRAINT enc_edif_energia_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.pto_pto_geod_topo_controle_p(
	id serial NOT NULL,
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tiporef smallint NOT NULL,
	latitude varchar(80),
	longitude varchar(80),
	altitudeortometrica float,
	sistemageodesico smallint NOT NULL,
	referencialaltim smallint NOT NULL,
	outrarefalt varchar(80),
	orgaoenteresp varchar(80),
	codponto varchar(80),
	obs varchar(255),
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT pto_pto_geod_topo_controle_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_edif_energia_a(
	tipoedifenergia smallint NOT NULL,
	id_complexo_gerad_energ_eletr uuid,
	id_subestacao_ener_eletr uuid,
	CONSTRAINT enc_edif_energia_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.pto_pto_controle_p(
	tipoptocontrole smallint NOT NULL,
	materializado smallint NOT NULL DEFAULT 0,
	codprojeto varchar(80),
	CONSTRAINT pto_pto_controle_p_pk PRIMARY KEY (id)
) INHERITS(cb.pto_pto_geod_topo_controle_p)
;
CREATE TABLE cb.enc_edif_comunic_p(
	modalidade smallint NOT NULL,
	tipoedifcomunic smallint NOT NULL,
	id_complexo_comunicacao uuid,
	CONSTRAINT enc_edif_comunic_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.tra_pista_ponto_pouso(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
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
	CONSTRAINT tra_pista_ponto_pouso_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_edif_comunic_a(
	modalidade smallint NOT NULL DEFAULT 0,
	tipoedifcomunic smallint NOT NULL DEFAULT 0,
	id_complexo_comunicacao uuid,
	CONSTRAINT enc_edif_comunic_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.tra_pista_ponto_pouso_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_pista_ponto_pouso_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_pista_ponto_pouso)
;
CREATE TABLE cb.tra_edif_constr_aeroportuaria_p(
	tipoedifaero smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL DEFAULT 0,
	id_complexo_aeroportuario uuid,
	CONSTRAINT tra_edif_constr_aeroportuaria_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.tra_pista_ponto_pouso_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_pista_ponto_pouso_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_pista_ponto_pouso)
;
CREATE TABLE cb.tra_edif_constr_portuaria_a(
	tipoedifport smallint NOT NULL,
	administracao smallint NOT NULL,
	id_complexo_portuario uuid,
	CONSTRAINT tra_edif_constr_portuaria_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.tra_trecho_duto_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
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
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_trecho_duto_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_edif_metro_ferroviaria_p(
	funcaoedifmetroferrov smallint,
	multimodal smallint NOT NULL,
	administracao smallint NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT tra_edif_metro_ferroviaria_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE complexos.tra_estrut_transporte(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	CONSTRAINT tra_estrut_transporte_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_edif_constr_portuaria_p(
	tipoedifport smallint NOT NULL,
	administracao smallint NOT NULL,
	id_complexo_portuario uuid,
	CONSTRAINT tra_edif_constr_portuaria_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE complexos.tra_estrut_apoio(
	tipoestrut smallint NOT NULL,
	CONSTRAINT tra_estrut_apoio_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE cb.tra_edif_constr_aeroportuaria_a(
	tipoedifaero smallint NOT NULL,
	administracao smallint NOT NULL,
	id_complexo_aeroportuario uuid,
	CONSTRAINT tra_edif_constr_aeroportuaria_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.tra_edif_metro_ferroviaria_a(
	funcaoedifmetroferrov smallint NOT NULL,
	multimodal smallint NOT NULL,
	administracao smallint NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT tra_edif_metro_ferroviaria_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.tra_edif_rodoviaria_p(
	tipoedifrod smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT tra_edif_rodoviaria_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.tra_edif_rodoviaria_a(
	tipoedifrod smallint NOT NULL DEFAULT 0,
	administracao smallint NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT tra_edif_rodoviaria_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.eco_edif_ext_mineral_p(
	tipodivisaocnae smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_edif_ext_mineral_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.eco_edif_ext_mineral_a(
	tipodivisaocnae smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_edif_ext_mineral_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE complexos.tra_complexo_aeroportuario(
	indicador varchar(4) NOT NULL,
	siglaaero varchar(3),
	tipocomplexoaero smallint NOT NULL,
	classificacao smallint NOT NULL,
	latoficial varchar(80),
	longoficial varchar(80),
	altitude integer,
	CONSTRAINT tra_complexo_aeroportuario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE cb.eco_edif_agrop_ext_veg_pesca_p(
	tipoedifagropec smallint NOT NULL,
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.asb_dep_abast_agua_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT asb_dep_abast_agua_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_abast_agua)
;
CREATE TABLE cb.eco_edif_agrop_ext_veg_pesca_a(
	tipoedifagropec smallint NOT NULL,
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.eco_edif_industrial_p(
	chamine smallint NOT NULL,
	tipodivisaocnae smallint NOT NULL,
	id_org_industrial uuid,
	CONSTRAINT eco_edif_industrial_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE cb.asb_dep_saneamento_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT asb_dep_saneamento_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_dep_saneamento)
;
CREATE TABLE cb.eco_edif_industrial_a(
	chamine smallint NOT NULL,
	tipodivisaocnae smallint NOT NULL,
	id_org_industrial uuid,
	CONSTRAINT eco_edif_industrial_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
CREATE TABLE cb.eco_deposito_geral_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT eco_deposito_geral_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_deposito_geral)
;
CREATE TABLE cb.tra_patio(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	modaluso smallint NOT NULL,
	administracao smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	id_estrut_transporte uuid,
	id_org_ext_mineral uuid,
	id_org_comerc_serv uuid,
	id_org_industrial uuid,
	id_org_ensino uuid,
	CONSTRAINT tra_patio_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.eco_frigorifico_matadouro(
	frigorifico smallint NOT NULL,
	id_org_agrop_ext_veg_pesca uuid,
	CONSTRAINT eco_frigorifico_matadouro_pk PRIMARY KEY (id)
) INHERITS(complexos.eco_org_industrial)
;
CREATE TABLE cb.tra_patio_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_patio_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio)
;
CREATE TABLE cb.eco_equip_agropec_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT eco_equip_agropec_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_equip_agropec)
;
CREATE TABLE cb.tra_patio_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_patio_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_patio)
;
CREATE TABLE complexos.asb_complexo_saneamento(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	tipoclassecnae smallint NOT NULL,
	administracao smallint NOT NULL,
	organizacao smallint NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT asb_complexo_saneamento_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.asb_complexo_abast_agua(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipoclassecnae smallint NOT NULL,
	organizacao varchar(50),
	id_org_comerc_serv uuid,
	CONSTRAINT asb_complexo_abast_agua_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_plataforma_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT eco_plataforma_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_plataforma)
;
CREATE TABLE cb.tra_funicular(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	id_org_ext_mineral uuid,
	CONSTRAINT tra_funicular_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.adm_org_comerc_serv(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipodivisaocnae smallint NOT NULL,
	finalidade smallint NOT NULL,
	CONSTRAINT adm_org_comerc_serv_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_funicular_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_funicular_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_funicular)
;
CREATE TABLE complexos.edu_org_ensino_militar(
	CONSTRAINT edu_org_ensino_militar_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino,complexos.adm_org_pub_militar)
;
CREATE TABLE complexos.edu_org_ensino_pub(
	CONSTRAINT edu_org_ensino_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino,complexos.adm_org_pub_civil)
;
CREATE TABLE cb.tra_passag_elevada_viaduto(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipopassagviad smallint NOT NULL,
	modaluso smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	vaolivrehoriz real,
	vaovertical real,
	gabhorizsup real,
	gabvertsup real,
	cargasuportmaxima real,
	nrpistas integer,
	nrfaixas integer,
	posicaopista smallint NOT NULL,
	extensao float,
	largura float,
	CONSTRAINT tra_passag_elevada_viaduto_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.adm_org_ext_mineral(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tiposecaocnae smallint NOT NULL,
	CONSTRAINT eco_org_ext_mineral_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.eco_org_agrop_ext_veg_pesca(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	tipodivisaocnae smallint NOT NULL,
	CONSTRAINT org_agropec_ext_vegetal_pesca_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_area_agrop_ext_veg_pesca_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	destinadoa smallint NOT NULL,
	id_org_agropec_ext_veg_pesca uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_area_agropec_ext_vegetal_pesca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.edu_org_ensino_religioso(
	CONSTRAINT edu_org_ensino_religioso_pk PRIMARY KEY (id)
) INHERITS(complexos.edu_org_ensino,complexos.edu_org_religiosa)
;
CREATE TABLE cb.enc_grupo_transformadores_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT enc_grupo_transformadores_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_grupo_transformadores)
;
CREATE TABLE cb.tra_ponte(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoponte smallint NOT NULL,
	modaluso smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	vaolivrehoriz real,
	vaolivrevertical real,
	cargasuportmaxima real,
	nrfaixas integer,
	nrpistas integer,
	posicaopista smallint NOT NULL,
	largura float,
	extensao float,
	CONSTRAINT tra_ponte_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_ponte_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_ponte_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponte)
;
CREATE TABLE cb.tra_tunel(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipotunel smallint NOT NULL,
	modaluso smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint,
	nrpistas integer,
	nrfaixas integer,
	posicaopista smallint NOT NULL,
	altura float,
	extensao real,
	CONSTRAINT tra_tunel_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_tunel_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_tunel_p_pk PRIMARY KEY (nome)
) INHERITS(cb.tra_tunel)
;
CREATE TABLE cb.tra_tunel_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_tunel_l_pk PRIMARY KEY (nome)
) INHERITS(cb.tra_tunel)
;
CREATE TABLE cb.eco_area_ext_mineral_a(
	id serial NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT eco_ext_mineral_a_pk_1 PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_termeletrica_p(
	tipocombustivel smallint NOT NULL DEFAULT 0,
	combrenovavel smallint NOT NULL DEFAULT 0,
	tipomaqtermica smallint NOT NULL DEFAULT 0,
	geracao smallint NOT NULL,
	CONSTRAINT enc_termeletrica_p_pk PRIMARY KEY (id)
) INHERITS(cb.enc_est_gerad_energia_eletr_p)
;
CREATE TABLE cb.tra_travessia_pedestre(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipotravessiaped smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	largura float,
	extensao float,
	CONSTRAINT tra_travessia_pedestre_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_travessia_pedestre_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_travessia_pedestre_p_pk PRIMARY KEY (tipotravessiaped)
) INHERITS(cb.tra_travessia_pedestre)
;
CREATE TABLE complexos.enc_complexo_gerad_energ_eletr(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipoclassecnae smallint NOT NULL DEFAULT 0,
	id_org_comerc_serv uuid,
	CONSTRAINT enc_comp_gerad_energ_ele_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.enc_subestacao_ener_eletr(
	id uuid NOT NULL,
	nome varchar(80),
	tipoclassecnae smallint NOT NULL,
	tipooperativo smallint NOT NULL,
	operacional smallint NOT NULL DEFAULT 0,
	id_complexo_gerad_energ_eletr uuid,
	CONSTRAINT enc_subest_transm_distrib_energia_eletrica_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.enc_complexo_comunicacao(
	id uuid NOT NULL,
	nome varchar(80),
	tipoclassecnae smallint NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT enc_complexo_comunicacao_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_travessia_pedestre_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_travessia_pedestre_l_pk PRIMARY KEY (tipotravessiaped)
) INHERITS(cb.tra_travessia_pedestre)
;
CREATE TABLE cb.pto_pto_ref_geod_topo_p(
	nome varchar(80),
	proximidade smallint NOT NULL,
	tipoptorefgeodtopo smallint NOT NULL,
	rede smallint NOT NULL,
	referencialgrav smallint NOT NULL,
	situacaomarco smallint NOT NULL,
	datavisita varchar(80),
	CONSTRAINT pto_pto_ref_geod_topo_p_pk PRIMARY KEY (id)
) INHERITS(cb.pto_pto_geod_topo_controle_p)
;
CREATE TABLE cb.tra_travessia(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipotravessia smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_travessia_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.enc_area_energia_eletrica_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_subestacao_ener_eletr uuid,
	id_complexo_gerador_energia_eletrica uuid,
	CONSTRAINT enc_area_energia_eletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_zona_linhas_energia_com_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT enc_zona_lin_energ_comunic_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_torre_energia_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	ovgd smallint NOT NULL,
	alturaestimada float,
	tipotorre smallint NOT NULL,
	arranjofases varchar(80),
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT enc_torre_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_antena_comunic_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	id_complexo_comunicacao uuid,
	CONSTRAINT enc_antena_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_torre_comunic_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	posicaoreledific smallint NOT NULL,
	ovgd smallint NOT NULL,
	alturaestimada float,
	id_complexo_comunicacao uuid,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT enc_torre_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_trecho_energia_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	especie smallint NOT NULL,
	posicaorelativa smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	emduto smallint NOT NULL,
	tensaoeletrica float,
	numcircuitos integer,
	id_org_comerc_serv uuid,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT enc_trecho_comunic_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.enc_trecho_comunic_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipotrechocomunic smallint NOT NULL,
	posicaorelativa smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	emduto smallint NOT NULL,
	id_org_comerc_serv uuid,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT enc_trecho_comunic_l_pk_1 PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_travessia_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_travessia_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia)
;
CREATE TABLE cb.tra_pista_ponto_pouso_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_pista_ponto_pouso_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_pista_ponto_pouso)
;
CREATE TABLE cb.tra_trecho_rodoviario_l(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	codtrechorodov varchar(80) NOT NULL,
	tipotrechorod smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	administracao smallint NOT NULL,
	concessionaria varchar(100),
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	nrpistas integer,
	nrfaixas integer,
	trafego smallint NOT NULL,
	canteirodivisorio smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	id_via_rodoviaria uuid,
	CONSTRAINT tra_trecho_rodoviario_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_cremalheira(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	CONSTRAINT tra_cremalheira_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_cremalheira_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_cremalheira_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_cremalheira)
;
CREATE TABLE cb.tra_atracadouro(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoatracad smallint NOT NULL,
	administracao smallint NOT NULL,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_complexo_portuario uuid,
	CONSTRAINT tra_atracadouro_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_condutor_hidrico_l(
	tipocondutor smallint NOT NULL,
	id_complexo_gerad_energ_eletr uuid,
	CONSTRAINT tra_condutor_hidrico_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_trecho_duto_l)
;
CREATE TABLE complexos.tra_complexo_portuario(
	tipotransporte smallint NOT NULL DEFAULT 0,
	tipocomplexoportuario smallint NOT NULL,
	CONSTRAINT tra_complexo_portuario_pk PRIMARY KEY (id)
) INHERITS(complexos.tra_estrut_transporte)
;
CREATE TABLE cb.tra_atracadouro_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_atracadouro_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_atracadouro)
;
CREATE TABLE cb.tra_atracadouro_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_atracadouro_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_atracadouro)
;
CREATE TABLE cb.tra_fundeadouro(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	destinacaofundeadouro smallint NOT NULL,
	administracao smallint NOT NULL DEFAULT 0,
	id_complexo_portuario uuid,
	CONSTRAINT tra_fundeadouro_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_fundeadouro_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_fundeadouro_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_fundeadouro)
;
CREATE TABLE cb.tra_fundeadouro_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_fundeadouro_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_fundeadouro)
;
CREATE TABLE cb.tra_obstaculo_navegacao(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipoobst smallint NOT NULL,
	situacaoemagua smallint NOT NULL,
	CONSTRAINT tra_obstaculo_navegacao_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.pto_est_med_fenomenos(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipoestmed smallint,
	codigoest varchar(50),
	orgaoenteresp varchar(80),
	id_est_med_fenomenos uuid,
	CONSTRAINT pto_est_med_fenomenos_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.pto_pto_est_med_fenomenos_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	tipoptoestmed smallint NOT NULL,
	codestacao varchar(80),
	orgaoenteresp varchar(15),
	id_est_med_fenomenos uuid,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT pto_est_med_fenomenos_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_obstaculo_navegacao_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_obstaculo_navegacao_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obstaculo_navegacao)
;
CREATE TABLE cb.tra_obstaculo_navegacao_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_obstaculo_navegacao_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obstaculo_navegacao)
;
CREATE TABLE cb.tra_eclusa(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	desnivel float,
	largura float,
	extensao float,
	calado float,
	matconstr smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	CONSTRAINT tra_eclusa_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_eclusa_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_eclusa_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_eclusa)
;
CREATE TABLE cb.tra_faixa_seguranca_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	largura float,
	extensao float,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_faixa_seguranca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE complexos.tra_duto(
	id uuid NOT NULL,
	nome varchar(80),
	CONSTRAINT dut_duto_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_eclusa_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_eclusa_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_eclusa)
;
CREATE TABLE cb.tra_funicular_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_funicular_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_funicular)
;
CREATE TABLE cb.tra_ponto_duto_p(
	id serial NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	relacionado smallint NOT NULL,
	CONSTRAINT tra_ponto_duto_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.lim_linha_de_limite_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	coincidecomdentrode smallint NOT NULL,
	geometriaaproximada smallint NOT NULL,
	extensao float,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT lim_linha_de_limite_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.lim_limite_intra_munic_adm_l(
	tipolimintramun smallint NOT NULL,
	obssituacao varchar(100),
	CONSTRAINT lim_limite_intra_munic_adm_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_operacional_l(
	tipolimoper smallint NOT NULL,
	obssituacao varchar(100),
	CONSTRAINT lim_limite_operacional_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.tra_passag_elevada_viaduto_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_passag_elevada_viaduto_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_passag_elevada_viaduto)
;
CREATE TABLE cb.lim_outros_limites_oficiais_l(
	tipooutlimofic smallint NOT NULL,
	obssituacao varchar(100),
	CONSTRAINT lim_outros_limites_oficiais_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_particular_l(
	obssituacao varchar(100),
	CONSTRAINT lim_limite_particular_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_limite_area_especial_l(
	tipolimareaesp smallint NOT NULL,
	obssituacao varchar(100),
	CONSTRAINT lim_limite_area_especial_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.lim_area_politico_adm_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_area_politico_adm_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
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
CREATE TABLE cb.tra_caminho_aereo_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipocaminhoaereo smallint NOT NULL,
	tipousocaminhoaer smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	id_org_ext_mineral uuid,
	CONSTRAINT tra_caminho_aereo_l_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_entroncamento_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	tipoentroncamento smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_entroncamento_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
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
CREATE TABLE cb.lim_area_especial(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	CONSTRAINT lim_area_especial_pk PRIMARY KEY (id)
);
ALTER TABLE cb.lim_area_especial OWNER TO postgres;
CREATE TABLE cb.lim_area_especial_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_area_especial_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial)
;
CREATE TABLE cb.loc_localidade_p(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geocodigo varchar(80),
	identificador varchar(80),
	latitude varchar(15),
	latitude_gms real,
	longitude varchar(15),
	longitude_gms real,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT loc_localidade_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_travessia_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_travessia_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_travessia)
;
CREATE TABLE cb.loc_vila_p(
	CONSTRAINT loc_vila_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.loc_cidade_p(
	CONSTRAINT loc_cidade_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.loc_capital_p(
	tipocapital smallint NOT NULL,
	CONSTRAINT loc_capital_p_pk PRIMARY KEY (nome)
) INHERITS(cb.loc_cidade_p)
;
CREATE TABLE cb.tra_cremalheira_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_cremalheira_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_cremalheira)
;
CREATE TABLE cb.tra_atracadouro_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_atracadouro_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_atracadouro)
;
CREATE TABLE cb.tra_fundeadouro_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_fundeadouro_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_fundeadouro)
;
CREATE TABLE cb.tra_obstaculo_navegacao_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_obstaculo_navegacao_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_obstaculo_navegacao)
;
CREATE TABLE cb.tra_ponto_rodoviario_ferrov(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	relacionado smallint NOT NULL,
	CONSTRAINT tra_ponto_rodoviario_ferrov_pk PRIMARY KEY (id)
);
CREATE TABLE complexos.edu_complexo_lazer(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipocomplexolazer smallint NOT NULL,
	tipodivisaocnae smallint NOT NULL,
	administracao smallint NOT NULL,
	id_org_religiosa uuid,
	id_org_pub_civil uuid,
	id_org_ensino uuid,
	id_org_pub_militar uuid,
	CONSTRAINT laz_complexo_lazer_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_passagem_nivel_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_passagem_nivel_p_pk PRIMARY KEY (id)
);
CREATE TABLE cb.tra_girador_ferroviario_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	administracao smallint NOT NULL DEFAULT 0,
	operacional smallint NOT NULL DEFAULT 0,
	situacaofisica smallint NOT NULL DEFAULT 0,
	geom geometry(POINT, [epsg]) NOT NULL,
	id_estrut_apoio uuid,
	CONSTRAINT tra_girador_ferroviario_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_trecho_ferroviario_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	codtrechoferrov varchar(80),
	posicaorelativa smallint NOT NULL,
	tipotrechoferrov smallint NOT NULL,
	bitola smallint NOT NULL,
	eletrificada smallint NOT NULL,
	nrlinhas smallint NOT NULL,
	emarruamento smallint NOT NULL,
	jurisdicao smallint NOT NULL,
	administracao smallint NOT NULL,
	concessionaria varchar(80),
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	cargasuportmaxima float,
	id_via_ferrea uuid,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_trecho_ferroviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_eclusa_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_eclusa_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_eclusa)
;
CREATE TABLE cb.lim_limite_politico_adm_l(
	tipolimpol smallint NOT NULL,
	obssituacao varchar(100),
	CONSTRAINT lim_limite_politico_adm_l_pk PRIMARY KEY (id)
) INHERITS(cb.lim_linha_de_limite_l)
;
CREATE TABLE cb.tra_sinalizacao_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tiposinal smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_sinalizacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.lim_pais_a(
	sigla varchar(80),
	codiso3166 varchar(80) NOT NULL DEFAULT 'BRA',
	CONSTRAINT lim_pais_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_politico_adm_a)
;
CREATE TABLE cb.edu_arquibancada(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_arquibancada_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.lim_area_desenv_controle_a(
	classificacao varchar(80),
	CONSTRAINT lim_area_desenv_controle_a_pk PRIMARY KEY (geom)
) INHERITS(cb.lim_area_especial_a)
;
CREATE TABLE cb.lim_area_uso_comunitario_a(
	tipoareausocomun smallint NOT NULL,
	CONSTRAINT lim_area_uso_comunitario_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
CREATE TABLE cb.edu_arquibancada_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT edu_arquibancada_a_pk PRIMARY KEY (id)
) INHERITS(cb.edu_arquibancada)
;
CREATE TABLE cb.loc_aglomerado_rural_p(
	CONSTRAINT loc_aglomerado_rural_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_localidade_p)
;
CREATE TABLE cb.edu_campo_quadra(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipocampoquadra smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_campo_quadra_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.lim_delimitacao_fisica_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipodelimfis smallint NOT NULL,
	matconstr smallint NOT NULL,
	eletrificada smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT lim_delimitacao_fisica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.lim_marco_de_limite_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipomarcolim smallint NOT NULL,
	latitude_gms float,
	latitude varchar(15),
	longitude_gms float,
	longitude varchar(15),
	altitudeortometrica float,
	sistemageodesico smallint NOT NULL,
	outrarefplan varchar(80),
	referencialaltim smallint NOT NULL,
	outrarefalt varchar(80),
	orgresp varchar(80),
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT lim_marco_de_limite_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.lim_area_de_litigio_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL DEFAULT 2,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_area_de_litigio_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.edu_campo_quadra_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT edu_campo_quadra_a_pk PRIMARY KEY (id)
) INHERITS(cb.edu_campo_quadra)
;
CREATE TABLE cb.edu_pista_competicao_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipopista smallint NOT NULL,
	id_complexo_lazer uuid,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT edu_pista_competicao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_ruina(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT laz_ruina_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_ruina_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT edu_ruina_a_pk PRIMARY KEY (id)
) INHERITS(cb.edu_ruina)
;
CREATE TABLE cb.loc_area_construida_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_area_construida_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.loc_nome_local_p(
	id serial NOT NULL,
	nome varchar(80),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT loc_nome_local_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_arquibancada_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT edu_arquibancada_p_pk PRIMARY KEY (id)
) INHERITS(cb.edu_arquibancada)
;
CREATE TABLE cb.edu_campo_quadra_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT edu_campo_quadra_p_pk PRIMARY KEY (id)
) INHERITS(cb.edu_campo_quadra)
;
CREATE TABLE cb.tra_arruamento_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	nrfaixas integer,
	trafego smallint NOT NULL,
	canteirodivisorio smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_arruamento_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_ruina_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT edu_ruina_p_pk PRIMARY KEY (id)
) INHERITS(cb.edu_ruina)
;
CREATE TABLE cb.asb_cemiterio(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipocemiterio smallint NOT NULL,
	denominacaoassociada smallint NOT NULL,
	CONSTRAINT asb_cemiterio_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.asb_cemiterio_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT asb_cemiterio_a_pk PRIMARY KEY (id)
) INHERITS(cb.asb_cemiterio)
;
CREATE TABLE complexos.sau_org_saude(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	administracao smallint NOT NULL,
	tipogrupocnae smallint NOT NULL,
	CONSTRAINT sau_org_saude_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.sau_org_saude_pub(
	CONSTRAINT sau_org_saude_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_saude,complexos.adm_org_pub_civil)
;
CREATE TABLE complexos.sau_org_servico_social(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	administracao smallint NOT NULL,
	tipogrupocnae smallint NOT NULL,
	CONSTRAINT sau_org_servico_social_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.enc_area_comunicacao_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_complexo_comunicacao uuid,
	CONSTRAINT cbc_area_comunicacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.asb_area_abast_agua_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_complexo_abast_agua uuid,
	CONSTRAINT cbc_area_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.asb_area_saneamento_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_complexo_saneamento uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT cbc_area_saneamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_area_duto_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_area_duto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.sau_area_servico_social_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_org_servico_social uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT sau_area_servico_social_a_pk PRIMARY KEY (id)
);
CREATE TABLE cb.sau_area_saude_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_saude uuid,
	CONSTRAINT sau_area_saude_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_area_ruinas_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT cbc_area_ruinas_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_area_lazer_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_area_lazer_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_area_comerc_serv_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_comerc_serv uuid,
	CONSTRAINT eco_area_comerc_serv_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_area_ensino_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL DEFAULT 0,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT cbc_area_ensino_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.edu_area_religiosa_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_religiosa uuid,
	CONSTRAINT cbc_area_religiosa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.tra_ponto_ferroviario_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_ponto_ferroviario_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponto_rodoviario_ferrov)
;
CREATE TABLE cb.tra_ponto_rodoviario_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_ponto_rodoviario_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponto_rodoviario_ferrov)
;
CREATE TABLE cb.asb_cemiterio_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT asb_cemiterio_p_pk PRIMARY KEY (id)
) INHERITS(cb.asb_cemiterio)
;
CREATE TABLE cb.edu_edif_ensino_p(
	tipoclassecnae smallint NOT NULL,
	id_org_ensino uuid,
	CONSTRAINT edu_edif_ensino_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
CREATE TABLE complexos.sau_org_saude_militar(
	CONSTRAINT sau_org_saude_militar_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_saude,complexos.adm_org_pub_militar)
;
CREATE TABLE complexos.sau_org_servico_social_pub(
	CONSTRAINT sau_org_servico_social_pub_pk PRIMARY KEY (id)
) INHERITS(complexos.sau_org_servico_social,complexos.adm_org_pub_civil)
;
CREATE EXTENSION "uuid-ossp"
      WITH SCHEMA public;
CREATE TABLE complexos.adm_instituicao_publica(
	id uuid NOT NULL,
	nome varchar(80) NOT NULL,
	nomeabrev varchar(50),
	tipogrupocnae smallint NOT NULL,
	id_instituicao_publica uuid,
	CONSTRAINT adm_instituicao_publica_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.eco_area_industrial_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_org_industrial uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_area_industrial_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.tra_area_estrut_transporte_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_estrut_transporte uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT cbc_area_estrut_transporte_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE cb.loc_aglomerado_rural_isolado_p(
	tipoaglomrurisol smallint NOT NULL,
	CONSTRAINT loc_aglomerado_rural_isolado_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_aglomerado_rural_p)
;
CREATE TABLE cb.loc_aglom_rural_de_ext_urbana_p(
	CONSTRAINT loc_aglom_rural_de_ext_urbana_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_aglomerado_rural_p)
;
CREATE TABLE cb.pto_area_est_med_fenom_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	id_est_med_fenomenos uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT cbc_area_est_med_fenom_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE public.aux_geometria(
	id serial NOT NULL,
	classe varchar(80),
	CONSTRAINT aux_geometria_1 PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE public.aux_objeto_desconhecido(
	id serial NOT NULL,
	classe varchar(80),
	descricao varchar(80),
	CONSTRAINT aux_objeto_desconhecido_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE public.aux_objeto_desconhecido_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT aux_objeto_desconhecido_l_pk PRIMARY KEY (id)
) INHERITS(public.aux_objeto_desconhecido)
;
CREATE TABLE public.aux_ponto_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT aux_ponto_p_pk PRIMARY KEY (id)
) INHERITS(public.aux_geometria)
;
CREATE TABLE public.aux_linha_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT aux_linha_l_pk PRIMARY KEY (id)
) INHERITS(public.aux_geometria)
;
CREATE TABLE public.aux_area_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT aux_area_a_pk PRIMARY KEY (id)
) INHERITS(public.aux_geometria)
;
CREATE TABLE public.aux_objeto_desconhecido_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT aux_objeto_desconhecido_p_pk PRIMARY KEY (id)
) INHERITS(public.aux_objeto_desconhecido)
;
CREATE TABLE public.aux_objeto_desconhecido_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT aux_objeto_desconhecido_a_pk PRIMARY KEY (id)
) INHERITS(public.aux_objeto_desconhecido)
;
CREATE TABLE public.aux_moldura_a(
	id serial NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	mi varchar(80),
	inom varchar(80),
	escala varchar(80),
	nomecarta varchar(80),
	anoaquisicao varchar(80),
	engrespaquisicao varchar(80),
	opaquisicao varchar(80),
	datainicioaquisicao date,
	datafimaquisicao date,
	engresprevisaoaquisicao varchar(80),
	oprevisaoaquisicao varchar(80),
	datainiciorevaquisicao date,
	datafimrevaquisicao date,
	engrespreambulacao varchar(80),
	opreambulacao varchar(80),
	datainicioreambulacao date,
	datafimreambulacao date,
	oprevisaoreambulacao varchar(80),
	engrespvalidacaoedicao varchar(80),
	opvalidacao varchar(80),
	datainiciovalidacao date,
	datafimvalidacao date,
	opedicao1 varchar(80),
	datainicioedicao1 date,
	datafimedicao1 date,
	oprevedicao1 varchar(80),
	datainiciorevedicao1 date,
	datafimrevedicao1 date,
	opedicao2 varchar(80),
	datainicioedicao2 date,
	datafimedicao2 date,
	CONSTRAINT aux_moldura_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 10)
);
CREATE TABLE public.db_metadata(
	edgvversion varchar(6) NOT NULL DEFAULT '2.1.3',
	CONSTRAINT edgvversioncheck CHECK (edgvversion = '2.1.3')
);
INSERT INTO public.db_metadata (edgvversion) VALUES ('2.1.3');
CREATE TABLE complexos.hid_curso_dagua(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	CONSTRAINT hid_curso_dagua_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE complexos.hid_trecho_curso_dagua(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	id_curso_dagua uuid,
	CONSTRAINT hid_trecho_curso_dagua_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.hid_natureza_fundo(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	materialpredominante smallint,
	espessalgas smallint NOT NULL,
	CONSTRAINT hid_natureza_fundo_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE TABLE cb.hid_natureza_fundo_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_natureza_fundo_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_natureza_fundo)
;
CREATE TABLE cb.hid_natureza_fundo_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT hid_natureza_fundo_l_pk PRIMARY KEY (id)
) INHERITS(cb.hid_natureza_fundo)
;
CREATE TABLE cb.hid_natureza_fundo_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_natureza_fundo_a_pk PRIMARY KEY (id)
) INHERITS(cb.hid_natureza_fundo)
;
CREATE TABLE cb.hid_rocha_em_agua_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT hid_rocha_em_agua_p_pk PRIMARY KEY (id)
) INHERITS(cb.hid_rocha_em_agua)
;
ALTER TABLE cb.hid_rocha_em_agua_p OWNER TO postgres;
CREATE TABLE cb.hid_bacia_hidrografica_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	codigootto integer NOT NULL,
	nivelotto integer NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT hid_bacia_hidrografica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 100)
);
CREATE INDEX hid_area_umida_a_geom_1408997021488 ON cb.hid_area_umida_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_fonte_dagua_p_geom_1408997017228 ON cb.hid_fonte_dagua_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_limite_massa_dagua_l_geom_140899701845 ON cb.hid_limite_massa_dagua_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_massa_dagua_a_geom_1408997018171 ON cb.hid_massa_dagua_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_ponto_drenagem_p_geom_1408997018772 ON cb.hid_ponto_drenagem_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_quebramar_molhe_l_geom_1408997019419 ON cb.hid_quebramar_molhe_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_queda_dagua_p_gist ON cb.hid_queda_dagua_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_recife_p_gist ON cb.hid_recife_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_reservatorio_hidrico_a_geom_1408997020482 ON cb.hid_reservatorio_hidrico_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_barragem_p_gist ON cb.hid_barragem_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_sumidouro_vertedouro_p_geom_1408997020972 ON cb.hid_sumidouro_vertedouro_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_terreno_sujeito_inundacao_a_geom_140899702189 ON cb.hid_terreno_suj_inundacao_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_trecho_drenagem_l_geom_1408997021361 ON cb.hid_trecho_drenagem_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_quebramar_molhe_a_geom_1408997019255 ON cb.hid_quebramar_molhe_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_banco_areia_l_gist ON cb.hid_banco_areia_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_banco_areia_a_geom_1408997016227 ON cb.hid_banco_areia_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_barragem_l_gist ON cb.hid_barragem_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_recife_l_gist ON cb.hid_recife_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_recife_a_gist ON cb.hid_recife_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_barragem_a_gist ON cb.hid_barragem_a
	USING gist
	(
	  geom
	);
CREATE INDEX rel_elemento_fisiog_natural_p_gist ON cb.rel_elemento_fisiog_natural_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_comporta_p_gist ON cb.hid_comporta_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_queda_dagua_l_gist ON cb.hid_queda_dagua_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_queda_dagua_a_gist ON cb.hid_queda_dagua_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_corredeira_p_gist ON cb.hid_corredeira_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_corredeira_l_gist ON cb.hid_corredeira_l
	USING btree
	(
	  geom
	);
CREATE INDEX hid_comporta_l_geom_1408997016713 ON cb.hid_comporta_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_corredeira_a_gist ON cb.hid_corredeira_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_foz_maritima_p_gist ON cb.hid_foz_maritima_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_foz_maritima_l_gist ON cb.hid_foz_maritima_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_foz_maritima_a_gist ON cb.hid_foz_maritima_a
	USING gist
	(
	  geom
	);
CREATE INDEX veg_vegetacao_a_gist ON cb.veg_vegetacao_a
	USING gist
	(
	  geom
	);
CREATE INDEX rel_curva_nivel_l_gist ON cb.rel_curva_nivel_l
	USING gist
	(
	  geom
	);
CREATE INDEX rel_curva_batimetrica_l_gist ON cb.rel_curva_batimetrica_l
	USING gist
	(
	  geom
	);
CREATE INDEX rel_ponto_cotado_batimetrico_p_gist ON cb.rel_ponto_cotado_batimetrico_p
	USING gist
	(
	  geom
	);
CREATE INDEX rel_ponto_cotado_altimetrico_p_gist ON cb.rel_ponto_cotado_altimetrico_p
	USING gist
	(
	  geom
	);
CREATE INDEX rel_elemento_fisiog_natural_l_gist ON cb.rel_elemento_fisiog_natural_l
	USING gist
	(
	  geom
	);
CREATE INDEX rel_alter_fisiog_antropica_l_gist ON cb.rel_alter_fisiog_antropica_l
	USING gist
	(
	  geom
	);
CREATE INDEX rel_alter_fisiog_antropica_a_gist ON cb.rel_alter_fisiog_antropica_a
	USING gist
	(
	  geom
	);
CREATE INDEX loc_edificacao_p_gist ON cb.loc_edificacao_p
	USING gist
	(
	  geom
	);
CREATE INDEX loc_edificacao_a_gist ON cb.loc_edificacao_a
	USING gist
	(
	  geom
	);
CREATE INDEX rel_elemento_fisiog_natural_a_gist ON cb.rel_elemento_fisiog_natural_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_rocha_em_agua_p_gist ON cb.hid_rocha_em_agua_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_rocha_em_agua_a_gist ON cb.hid_rocha_em_agua_a
	USING gist
	(
	  geom
	);
CREATE INDEX "äsb_dep_abast_agua_a_gist" ON cb.asb_dep_abast_agua_a
	USING gist
	(
	  geom
	);
CREATE INDEX asb_dep_saneamento_a_gist ON cb.asb_dep_saneamento_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_deposito_geral_a_gist ON cb.eco_deposito_geral_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_equip_agropec_l_gist ON cb.eco_equip_agropec_l
	USING gist
	(
	  geom
	);
CREATE INDEX eco_equip_agropec_a_1 ON cb.eco_equip_agropec_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_plataforma_a_gist ON cb.eco_plataforma_a
	USING gist
	(
	  geom
	);
CREATE INDEX enc_grupo_transformadores_a_gist ON cb.enc_grupo_transformadores_a
	USING gist
	(
	  geom
	);
CREATE INDEX enc_est_gerad_energia_eletrica_l_gist ON cb.enc_est_gerad_energia_eletr_l
	USING gist
	(
	  geom
	);
CREATE INDEX enc_est_gerad_energia_eletrica_a_gist ON cb.enc_est_gerad_energia_eletr_a
	USING gist
	(
	  geom
	);
CREATE INDEX enc_est_gerad_energia_eletrica_p_gist ON cb.enc_est_gerad_energia_eletr_p
	USING gist
	(
	  geom
	);
CREATE INDEX pto_pto_geod_topo_controle_p_gist ON cb.pto_pto_geod_topo_controle_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_pista_ponto_pouso_l_gist ON cb.tra_pista_ponto_pouso_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_pista_ponto_pouso_a_gist ON cb.tra_pista_ponto_pouso_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_trecho_duto_l_gist ON cb.tra_trecho_duto_l
	USING gist
	(
	  geom
	);
CREATE INDEX asb_dep_abast_agua_p_gist ON cb.asb_dep_abast_agua_p
	USING gist
	(
	  geom
	);
CREATE INDEX asb_dep_saneamento_p_gist ON cb.asb_dep_saneamento_p
	USING gist
	(
	  geom
	);
CREATE INDEX eco_deposito_geral_p_gist ON cb.eco_deposito_geral_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_patio_a_gist ON cb.tra_patio_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_equip_agropec_p_gist ON cb.eco_equip_agropec_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_patio_p_gist ON cb.tra_patio_p
	USING gist
	(
	  geom
	);
CREATE INDEX eco_plataforma_p_gist ON cb.eco_plataforma_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_funicular_l_gist ON cb.tra_funicular_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_passagem_elevada_viaduto_l_gist ON cb.tra_passag_elevada_viaduto_l
	USING gist
	(
	  geom
	);
CREATE INDEX enc_grupo_transformadores_p_gist ON cb.enc_grupo_transformadores_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_ponte_l_gist ON cb.tra_ponte_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_tunel_p_gist ON cb.tra_tunel_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_tunel_l_gist ON cb.tra_tunel_l
	USING gist
	(
	  geom
	);
CREATE INDEX eco_area_ext_mineral_a_gist ON cb.eco_area_ext_mineral_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_travesssia_pedestre_p_gist ON cb.tra_travessia_pedestre_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_travessia_pedestre_l_gist ON cb.tra_travessia_pedestre_l
	USING gist
	(
	  geom
	);
CREATE INDEX enc_area_energia_eletrica_a_gist ON cb.enc_area_energia_eletrica_a
	USING gist
	(
	  geom
	);
CREATE INDEX enc_zona_lin_energ_comunic_a_gist ON cb.enc_zona_linhas_energia_com_a
	USING gist
	(
	  geom
	);
CREATE INDEX enc_torre_energia_p_gist ON cb.enc_torre_energia_p
	USING gist
	(
	  geom
	);
CREATE INDEX enc_antena_comunic_p_gist ON cb.enc_antena_comunic_p
	USING gist
	(
	  geom
	);
CREATE INDEX enc_torre_comunic_p_gist ON cb.enc_torre_comunic_p
	USING gist
	(
	  geom
	);
CREATE INDEX enc_trecho_energia_l_gist ON cb.enc_trecho_energia_l
	USING gist
	(
	  geom
	);
CREATE INDEX enc_trecho_comunic_l_gist ON cb.enc_trecho_comunic_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_travessia_l_gist ON cb.tra_travessia_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_pista_ponto_pouso_p_gist ON cb.tra_pista_ponto_pouso_p
	USING gist
	(
	  geom
	);
CREATE INDEX fer_cremalheira_l_gist ON cb.tra_cremalheira_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_atracadouro_l_gist ON cb.tra_atracadouro_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_atracadouro_a_gist ON cb.tra_atracadouro_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_fundeadouro_l_gist ON cb.tra_fundeadouro_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_fundeadouro_a_gist ON cb.tra_fundeadouro_a
	USING gist
	(
	  geom
	);
CREATE INDEX pto_est_med_fenomenos_p_gist ON cb.pto_pto_est_med_fenomenos_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_obstaculo_navegacao_l_gist ON cb.tra_obstaculo_navegacao_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_obstaculo_navegacao_a_gist ON cb.tra_obstaculo_navegacao_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_eclusa_l_gist ON cb.tra_eclusa_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_faixa_seguranca_a_gist ON cb.tra_faixa_seguranca_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_eclusa_a_gist ON cb.tra_eclusa_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_funicular_p_gist ON cb.tra_funicular_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_ponto_duto_p_gist ON cb.tra_ponto_duto_p
	USING gist
	(
	  geom
	);
CREATE INDEX lim_linha_de_limite_l_gist ON cb.lim_linha_de_limite_l
	USING gist
	(
	  geom
	);
CREATE INDEX lim_area_politico_adm_a_gist ON cb.lim_area_politico_adm_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_caminho_aereo_l_gist ON cb.tra_caminho_aereo_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_entroncamento_p_gist ON cb.tra_entroncamento_p
	USING gist
	(
	  geom
	);
CREATE INDEX loc_localidade_p_gist ON cb.loc_localidade_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_travessia_p_gist ON cb.tra_travessia_p
	USING gist
	(
	  geom
	);
CREATE INDEX fer_cremalheira_p_gist ON cb.tra_cremalheira_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_atracadouro_p_gist ON cb.tra_atracadouro_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_fundeadouro_p_gist ON cb.tra_fundeadouro_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_obstaculo_navegacao_p_gist ON cb.tra_obstaculo_navegacao_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_passagem_nivel_p_gist ON cb.tra_passagem_nivel_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_girador_ferroviario_p_gist ON cb.tra_girador_ferroviario_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_trecho_ferroviario_l_gist ON cb.tra_trecho_ferroviario_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_eclusa_p_gist ON cb.tra_eclusa_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_sinalizacao_p_gist ON cb.tra_sinalizacao_p
	USING gist
	(
	  geom
	);
CREATE INDEX edu_arquibancada_a_gist ON cb.edu_arquibancada_a
	USING gist
	(
	  geom
	);
CREATE INDEX lim_delimitacao_fisica_l_gist ON cb.lim_delimitacao_fisica_l
	USING gist
	(
	  geom
	);
CREATE INDEX lim_marco_de_limite_p_gist ON cb.lim_marco_de_limite_p
	USING gist
	(
	  geom
	);
CREATE INDEX lim_area_de_litigio_a_gist ON cb.lim_area_de_litigio_a
	USING gist
	(
	  geom
	);
CREATE INDEX edu_campo_quadra_a_gist ON cb.edu_campo_quadra_a
	USING gist
	(
	  geom
	);
CREATE INDEX edu_ruina_a_gist ON cb.edu_ruina_a
	USING gist
	(
	  geom
	);
CREATE INDEX loc_area_construida_a_1 ON cb.loc_area_construida_a
	USING gist
	(
	  geom
	);
CREATE INDEX loc_nome_local_p_gist ON cb.loc_nome_local_p
	USING gist
	(
	  geom
	);
CREATE INDEX edu_arquibancada_p_gist ON cb.edu_arquibancada_p
	USING gist
	(
	  geom
	);
CREATE INDEX edu_campo_quadra_p_gist ON cb.edu_campo_quadra_p
	USING gist
	(
	  geom
	);
CREATE INDEX edu_ruina_p_gist ON cb.edu_ruina_p
	USING gist
	(
	  geom
	);
CREATE INDEX abs_cemiterio_a_gist ON cb.asb_cemiterio_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_comunicacao_a_gist ON cb.enc_area_comunicacao_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_abast_agua_a_gist ON cb.asb_area_abast_agua_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_saneamento_a_gist ON cb.asb_area_saneamento_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_area_duto_a_gist ON cb.tra_area_duto_a
	USING gist
	(
	  geom
	);
CREATE INDEX sau_area_servico_social_a_gist ON cb.sau_area_servico_social_a
	USING gist
	(
	  geom
	);
CREATE INDEX sau_area_saude_a_gist ON cb.sau_area_saude_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_ruinas_a_gist ON cb.edu_area_ruinas_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_lazer_a_gist ON cb.edu_area_lazer_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_area_comerc_serv_a_gist ON cb.eco_area_comerc_serv_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_ensino_a_gist ON cb.edu_area_ensino_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_religiosa_a_gist ON cb.edu_area_religiosa_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_ponto_ferroviario_p_gist ON cb.tra_ponto_ferroviario_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_ponto_rodoviario_p_gist ON cb.tra_ponto_rodoviario_p
	USING gist
	(
	  geom
	);
CREATE INDEX asb_cemiterio_p_gist ON cb.asb_cemiterio_p
	USING gist
	(
	  geom
	);
CREATE INDEX eco_area_industrial_a_gist ON cb.eco_area_industrial_a
	USING gist
	(
	  geom
	);
CREATE INDEX cbc_area_est_med_fenom_a_gist ON cb.pto_area_est_med_fenom_a
	USING gist
	(
	  geom
	);
CREATE INDEX aux_objeto_desconhecido_l_gist ON public.aux_objeto_desconhecido_l
	USING gist
	(
	  geom
	);
CREATE INDEX aux_ponto_p_gist ON public.aux_ponto_p
	USING gist
	(
	  geom
	);
CREATE INDEX aux_linha_l_gist ON public.aux_linha_l
	USING gist
	(
	  geom
	);
CREATE INDEX aux_area_a_gist ON public.aux_area_a
	USING gist
	(
	  geom
	);
CREATE INDEX aux_objeto_desconhecido_p_gist ON public.aux_objeto_desconhecido_p
	USING gist
	(
	  geom
	);
CREATE INDEX aux_objeto_desconhecido_a_gist ON public.aux_objeto_desconhecido_a
	USING gist
	(
	  geom
	);
CREATE INDEX aux_moldura_a_gist ON public.aux_moldura_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_natureza_fundo_p_gist ON cb.hid_natureza_fundo_p
	USING gist
	(
	  geom
	);
CREATE INDEX hid_natureza_fundo_l_gist ON cb.hid_natureza_fundo_l
	USING gist
	(
	  geom
	);
CREATE INDEX hid_natureza_fundo_a_gist ON cb.hid_natureza_fundo_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_bacia_hidrografica_a_gist ON cb.hid_bacia_hidrografica_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_ext_mineral_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT eco_ext_mineral_p_pk PRIMARY KEY (id)
) INHERITS(cb.eco_ext_mineral)
;
ALTER TABLE cb.eco_ext_mineral_p OWNER TO postgres;
CREATE INDEX eco_ext_mineral_p_gist ON cb.eco_ext_mineral_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.eco_ext_mineral_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT eco_ext_mineral_a_pk PRIMARY KEY (id)
) INHERITS(cb.eco_ext_mineral)
;
ALTER TABLE cb.eco_ext_mineral_a OWNER TO postgres;
CREATE INDEX eco_ext_mineral_a_gist ON cb.eco_ext_mineral_a
	USING gist
	(
	  geom
	);
CREATE INDEX rel_terreno_exposto_a_gist ON cb.rel_terreno_exposto_a
	USING gist
	(
	  geom
	);
CREATE INDEX veg_veg_area_contato_gist ON cb.veg_veg_area_contato_a
	USING gist
	(
	  geom
	);
CREATE INDEX veg_veg_cultivada_a_gist ON cb.veg_veg_cultivada_a
	USING gist
	(
	  geom
	);
CREATE INDEX veg_campo_a_gist ON cb.veg_campo_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.veg_macega_chavascal_a(
	tipomacchav smallint NOT NULL,
	alturamediaindividuos real,
	classificacaoporte smallint NOT NULL,
	CONSTRAINT veg_macega_chavascal_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
ALTER TABLE cb.veg_macega_chavascal_a OWNER TO postgres;
CREATE TABLE cb.veg_estepe_a(
	alturamediaindividuos real,
	CONSTRAINT veg_estepe_a_pk PRIMARY KEY (id)
) INHERITS(cb.veg_vegetacao_a)
;
ALTER TABLE cb.veg_estepe_a OWNER TO postgres;
CREATE TABLE complexos.tra_via_rodoviaria(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	sigla varchar(6) NOT NULL,
	CONSTRAINT tra_via_rodoviaria_pk PRIMARY KEY (id)
);
ALTER TABLE complexos.tra_via_rodoviaria OWNER TO postgres;
CREATE INDEX tra_trecho_rodoviario_l_gist ON cb.tra_trecho_rodoviario_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_identific_trecho_rod_p(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	sigla varchar(6) NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	id_via_rodoviaria uuid,
	CONSTRAINT tra_identific_trecho_rod_p_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_identific_trecho_rod_p OWNER TO postgres;
CREATE INDEX tra_identific_trecho_rod_p_gist ON cb.tra_identific_trecho_rod_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_galeria_bueiro(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	matconstr smallint NOT NULL,
	pesosuportmaximo real,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	CONSTRAINT tra_galeria_bueiro_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_galeria_bueiro OWNER TO postgres;
CREATE TABLE cb.tra_galeria_bueiro_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_galeria_bueiro_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_galeria_bueiro)
;
ALTER TABLE cb.tra_galeria_bueiro_p OWNER TO postgres;
CREATE INDEX tra_galeria_bueiro_p_gist ON cb.tra_galeria_bueiro_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_galeria_bueiro_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_galeria_bueiro_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_galeria_bueiro)
;
ALTER TABLE cb.tra_galeria_bueiro_l OWNER TO postgres;
CREATE INDEX tra_galeria_bueiro_l_gist ON cb.tra_galeria_bueiro_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ponte_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_ponte_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_ponte)
;
CREATE TABLE cb.tra_passag_elevada_viaduto_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_passag_elevada_viaduto_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_passag_elevada_viaduto)
;
CREATE TABLE cb.tra_trilha_picada_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_trilha_picada_l_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_trilha_picada_l OWNER TO postgres;
CREATE INDEX tra_trilha_picada_l_gist ON cb.tra_trilha_picada_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ciclovia_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	administracao smallint NOT NULL,
	revestimento smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	trafego smallint NOT NULL,
	geom geometry(LINESTRING, [epsg]) NOT NULL
);
ALTER TABLE cb.tra_ciclovia_l OWNER TO postgres;
CREATE INDEX tra_ciclovia_l_gist ON cb.tra_ciclovia_l
	USING gist
	(
	  geom
	);
CREATE INDEX tra_arruamento_l_gist ON cb.tra_arruamento_l
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.tra_via_ferrea(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	CONSTRAINT tra_via_ferrea_pk PRIMARY KEY (id)
);
ALTER TABLE complexos.tra_via_ferrea OWNER TO postgres;
CREATE TABLE cb.tra_local_critico(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	tipolocalcrit smallint NOT NULL,
	CONSTRAINT tra_local_critico_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_local_critico OWNER TO postgres;
CREATE TABLE cb.tra_local_critico_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_local_critico_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_local_critico)
;
ALTER TABLE cb.tra_local_critico_p OWNER TO postgres;
CREATE INDEX tra_local_critico_p_gist ON cb.tra_local_critico_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_local_critico_l(
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	CONSTRAINT tra_local_critico_l_pk PRIMARY KEY (id)
) INHERITS(cb.tra_local_critico)
;
ALTER TABLE cb.tra_local_critico_l OWNER TO postgres;
CREATE INDEX tra_local_critico_l_gist ON cb.tra_local_critico_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_local_critico_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_local_critico_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_local_critico)
;
ALTER TABLE cb.tra_local_critico_a OWNER TO postgres;
CREATE INDEX tra_local_critico_a_gist ON cb.tra_local_critico_a
	USING gist
	(
	  geom
	);
CREATE TABLE complexos.tra_hidrovia(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	administracao smallint NOT NULL,
	extensaototal real,
	CONSTRAINT tra_hidrovia_pk PRIMARY KEY (id)
);
ALTER TABLE complexos.tra_hidrovia OWNER TO postgres;
CREATE TABLE cb.tra_trecho_hidroviario_l(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	regime smallint NOT NULL,
	extensaotrecho real,
	caladomaxseca real,
	geom geometry(LINESTRING, [epsg]) NOT NULL,
	id_hidrovia uuid,
	CONSTRAINT tra_trecho_hidroviario_l_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_trecho_hidroviario_l OWNER TO postgres;
CREATE INDEX tra_trecho_hidroviario_l_gist ON cb.tra_trecho_hidroviario_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_ponto_hidroviario_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	relacionado smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL
);
ALTER TABLE cb.tra_ponto_hidroviario_p OWNER TO postgres;
CREATE INDEX tra_ponto_hidroviario_p_gist ON cb.tra_ponto_hidroviario_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_ponte_p_gist ON cb.tra_ponte_p
	USING gist
	(
	  geom
	);
CREATE INDEX tra_passagem_elevada_viaduto_p_gist ON cb.tra_passag_elevada_viaduto_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_posto_combustivel(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	administracao smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	matconstr smallint NOT NULL,
	CONSTRAINT tra_posto_combustivel_pk PRIMARY KEY (id)
);
ALTER TABLE cb.tra_posto_combustivel OWNER TO postgres;
CREATE TABLE cb.tra_posto_combustivel_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT tra_posto_combustivel_p_pk PRIMARY KEY (id)
) INHERITS(cb.tra_posto_combustivel)
;
ALTER TABLE cb.tra_posto_combustivel_p OWNER TO postgres;
CREATE INDEX tra_posto_combustivel_p_gist ON cb.tra_posto_combustivel_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.tra_posto_combustivel_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT tra_posto_combustivel_a_pk PRIMARY KEY (id)
) INHERITS(cb.tra_posto_combustivel)
;
ALTER TABLE cb.tra_posto_combustivel_a OWNER TO postgres;
CREATE INDEX tra_posto_combustivel_a_gist ON cb.tra_posto_combustivel_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.enc_ponto_trecho_energia_p(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	tipoptoenergia smallint NOT NULL,
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT enc_ponto_trecho_energia_p_pk PRIMARY KEY (id)
);
ALTER TABLE cb.enc_ponto_trecho_energia_p OWNER TO postgres;
CREATE INDEX enc_ponto_trecho_energia_p_gist ON cb.enc_ponto_trecho_energia_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.edu_piscina_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_complexo_lazer uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT edu_piscina_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.edu_piscina_a OWNER TO postgres;
CREATE INDEX edu_piscina_a_gist ON cb.edu_piscina_a
	USING gist
	(
	  geom
	);
CREATE INDEX edu_pista_competicao_l_gist ON cb.edu_pista_competicao_l
	USING gist
	(
	  geom
	);
CREATE TABLE cb.edu_coreto_tribuna(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_complexo_lazer uuid,
	CONSTRAINT edu_coreto_tribuna_pk PRIMARY KEY (id)
);
ALTER TABLE cb.edu_coreto_tribuna OWNER TO postgres;
CREATE TABLE cb.edu_coreto_tribuna_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT edu_coreto_tribuna_p_pk PRIMARY KEY (id)
) INHERITS(cb.edu_coreto_tribuna)
;
ALTER TABLE cb.edu_coreto_tribuna_p OWNER TO postgres;
CREATE INDEX edu_coreto_tribuna_p_gist ON cb.edu_coreto_tribuna_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.edu_coreto_tribuna_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT edu_coreto_tribuna_a_pk PRIMARY KEY (id)
) INHERITS(cb.edu_coreto_tribuna)
;
ALTER TABLE cb.edu_coreto_tribuna_a OWNER TO postgres;
CREATE INDEX edu_coreto_tribuna_a_gist ON cb.edu_coreto_tribuna_a
	USING gist
	(
	  geom
	);
CREATE INDEX eco_area_agrop_ext_veg_pesca_a_gist ON cb.eco_area_agrop_ext_veg_pesca_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.adm_area_pub_civil_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_pub_civil uuid,
	CONSTRAINT adm_area_pub_civil_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.adm_area_pub_civil_a OWNER TO postgres;
CREATE TABLE cb.adm_posto_fiscal(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	tipopostofisc smallint NOT NULL,
	id_org_pub_civil uuid,
	CONSTRAINT adm_posto_fiscal_pk PRIMARY KEY (id)
);
ALTER TABLE cb.adm_posto_fiscal OWNER TO postgres;
CREATE TABLE cb.adm_posto_fiscal_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT adm_posto_fiscal_p_pk PRIMARY KEY (id)
) INHERITS(cb.adm_posto_fiscal)
;
ALTER TABLE cb.adm_posto_fiscal_p OWNER TO postgres;
CREATE TABLE cb.adm_area_pub_militar_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	id_org_pub_militar uuid,
	CONSTRAINT adm_area_pub_militar_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.adm_area_pub_militar_a OWNER TO postgres;
CREATE TABLE cb.adm_posto_pol_rod(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipopostopol smallint NOT NULL,
	geometriaaproximada smallint NOT NULL,
	operacional smallint NOT NULL,
	situacaofisica smallint NOT NULL,
	id_org_pub_militar uuid,
	id_org_pub_civil uuid,
	CONSTRAINT adm_posto_pol_rod_pk PRIMARY KEY (id)
);
ALTER TABLE cb.adm_posto_pol_rod OWNER TO postgres;
CREATE TABLE cb.adm_posto_pol_rod_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT adm_posto_pol_rod_p_pk PRIMARY KEY (id)
) INHERITS(cb.adm_posto_pol_rod)
;
ALTER TABLE cb.adm_posto_pol_rod_p OWNER TO postgres;
CREATE TABLE complexos.loc_complexo_habitacional(
	id uuid NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	CONSTRAINT loc_complexo_habitacional_pk PRIMARY KEY (id)
);
ALTER TABLE complexos.loc_complexo_habitacional OWNER TO postgres;
CREATE TABLE complexos.loc_aldeia_indigena(
	codigofunai varchar(12),
	terraindigena varchar(100),
	etnia varchar(100),
	CONSTRAINT loc_aldeia_indigena_pk PRIMARY KEY (id)
) INHERITS(complexos.loc_complexo_habitacional)
;
ALTER TABLE complexos.loc_aldeia_indigena OWNER TO postgres;
CREATE TABLE cb.loc_edif_habitacional_p(
	id_complexo_habitacional uuid,
	CONSTRAINT loc_edif_habitacional_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_p)
;
ALTER TABLE cb.loc_edif_habitacional_p OWNER TO postgres;
CREATE TABLE cb.loc_hab_indigena(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	coletiva smallint NOT NULL,
	isolada smallint NOT NULL,
	id_aldeia_indigena uuid,
	CONSTRAINT loc_hab_indigena_pk PRIMARY KEY (id)
);
ALTER TABLE cb.loc_hab_indigena OWNER TO postgres;
CREATE TABLE cb.loc_edif_habitacional_a(
	id_complexo_habitacional uuid,
	CONSTRAINT loc_edif_habitacional_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_edificacao_a)
;
ALTER TABLE cb.loc_edif_habitacional_a OWNER TO postgres;
CREATE TABLE cb.loc_hab_indigena_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_hab_indigena_a_pk PRIMARY KEY (id)
) INHERITS(cb.loc_hab_indigena)
;
ALTER TABLE cb.loc_hab_indigena_a OWNER TO postgres;
CREATE TABLE cb.loc_area_habitacional_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	id_complexo_habitacional uuid,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_area_habitacional_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.loc_area_habitacional_a OWNER TO postgres;
CREATE INDEX loc_area_habitacional_a_gist ON cb.loc_area_habitacional_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.loc_area_edificada_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_area_edificada_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.loc_area_edificada_a OWNER TO postgres;
CREATE TABLE cb.lim_terra_publica_a(
	classificacao varchar(100),
	CONSTRAINT lim_terra_publica_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
ALTER TABLE cb.lim_terra_publica_a OWNER TO postgres;
CREATE TABLE cb.lim_terra_indigena(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	"nomeTi" varchar(100),
	situacaojuridica smallint NOT NULL,
	datasituacaojuridica date,
	grupoetnico varchar(100),
	areaoficialha real,
	perimetrooficial real,
	CONSTRAINT lim_terra_indigena_pk PRIMARY KEY (id)
);
ALTER TABLE cb.lim_terra_indigena OWNER TO postgres;
CREATE TABLE cb.lim_terra_indigena_p(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_terra_indigena_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_terra_indigena)
;
ALTER TABLE cb.lim_terra_indigena_p OWNER TO postgres;
CREATE INDEX lim_terra_indigena_p_gist ON cb.lim_terra_indigena_p
	USING gist
	(
	  geom
	);
CREATE INDEX adm_area_pub_civil_a_gist ON cb.adm_area_pub_civil_a
	USING gist
	(
	  geom
	);
CREATE INDEX adm_area_pub_militar_a_gist ON cb.adm_area_pub_militar_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_terra_indigena_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_terra_indigena_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_terra_indigena)
;
ALTER TABLE cb.lim_terra_indigena_a OWNER TO postgres;
CREATE INDEX lim_terra_indigena_a_gist ON cb.lim_terra_indigena_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_outras_unid_protegidas_a(
	tipooutunidprot smallint NOT NULL,
	anocriacao varchar(4),
	historicomodificacao varchar(255),
	sigla varchar(6),
	areaoficial varchar(15),
	administracao smallint NOT NULL,
	CONSTRAINT lim_outras_unid_protegidas_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
ALTER TABLE cb.lim_outras_unid_protegidas_a OWNER TO postgres;
CREATE TABLE cb.lim_unidade_conserv_nao_snuc_a(
	atolegal varchar(100),
	administracao smallint NOT NULL,
	classificacao varchar(100),
	anocriacao varchar(4),
	sigla varchar(6),
	areaoficial varchar(15),
	CONSTRAINT lim_unidade_conserv_nao_snuc_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a OWNER TO postgres;
CREATE TABLE cb.lim_unidade_protecao_integral_a(
	anocriacao integer,
	areaoficial varchar(15),
	atolegal varchar(100),
	administracao smallint NOT NULL,
	tipounidprotinteg smallint NOT NULL,
	CONSTRAINT lim_unidade_protecao_integral_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
ALTER TABLE cb.lim_unidade_protecao_integral_a OWNER TO postgres;
CREATE TABLE cb.lim_unidade_uso_sustentavel_a(
	anocriacao integer,
	sigla varchar(6),
	areaoficialha float,
	atolegal varchar(100),
	administracao smallint NOT NULL,
	tipounidusosust smallint NOT NULL,
	CONSTRAINT lim_unidade_uso_sustentavel_a_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_a)
;
ALTER TABLE cb.lim_unidade_uso_sustentavel_a OWNER TO postgres;
CREATE TABLE cb.lim_area_especial_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT lim_area_especial_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial)
;
CREATE TABLE cb.lim_area_uso_comunitario_p(
	tipoareausocomun smallint NOT NULL,
	CONSTRAINT lim_area_uso_comunitario_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
CREATE TABLE cb.lim_area_desenv_controle_p(
	classificacao varchar(80),
	CONSTRAINT lim_area_desenv_controle_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
CREATE TABLE cb.lim_terra_publica_p(
	classificacao varchar(100),
	CONSTRAINT lim_terra_publica_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
ALTER TABLE cb.lim_terra_publica_p OWNER TO postgres;
CREATE TABLE cb.lim_outras_unid_protegidas_p(
	tipooutunidprot smallint NOT NULL,
	anocriacao varchar(4),
	historicomodificacao varchar(255),
	sigla varchar(6),
	areaoficial varchar(15),
	administracao smallint NOT NULL,
	CONSTRAINT lim_outras_unid_protegidas_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
ALTER TABLE cb.lim_outras_unid_protegidas_p OWNER TO postgres;
CREATE TABLE cb.lim_unidade_conserv_nao_snuc_p(
	atolegal varchar(100),
	administracao smallint NOT NULL,
	classificacao varchar(100),
	anocriacao varchar(4),
	sigla varchar(6),
	areaoficial varchar(15),
	CONSTRAINT lim_unidade_conserv_nao_snuc_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p OWNER TO postgres;
CREATE TABLE cb.lim_unidade_protecao_integral_p(
	anocriacao integer,
	areaoficial varchar(15),
	atolegal varchar(100),
	administracao smallint NOT NULL,
	tipounidprotinteg smallint NOT NULL,
	CONSTRAINT lim_unidade_protecao_integral_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
ALTER TABLE cb.lim_unidade_protecao_integral_p OWNER TO postgres;
CREATE TABLE cb.lim_unidade_uso_sustentavel_p(
	anocriacao integer,
	sigla varchar(6),
	areaoficialha float,
	atolegal varchar(100),
	administracao smallint NOT NULL,
	tipounidusosust smallint NOT NULL,
	CONSTRAINT lim_unidade_uso_sustentavel_p_pk PRIMARY KEY (id)
) INHERITS(cb.lim_area_especial_p)
;
ALTER TABLE cb.lim_unidade_uso_sustentavel_p OWNER TO postgres;
CREATE INDEX lim_area_especial_p_gist ON cb.lim_area_especial_p
	USING gist
	(
	  geom
	);
CREATE INDEX lim_area_especial_a_gist ON cb.lim_area_especial_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.lim_area_particular_a(
	id serial NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	geometriaaproximada smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT lim_area_particular_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.lim_area_particular_a OWNER TO postgres;
CREATE INDEX lim_area_particular_a_gist ON cb.lim_area_particular_a
	USING gist
	(
	  geom
	);
CREATE INDEX adm_posto_pol_rod_p_gist ON cb.adm_posto_pol_rod_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.adm_posto_pol_rod_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT adm_posto_pol_rod_a_pk PRIMARY KEY (id)
) INHERITS(cb.adm_posto_pol_rod)
;
ALTER TABLE cb.adm_posto_pol_rod_a OWNER TO postgres;
CREATE INDEX adm_posto_pol_rod_a_gist ON cb.adm_posto_pol_rod_a
	USING gist
	(
	  geom
	);
CREATE INDEX adm_posto_fiscal_p_gist ON cb.adm_posto_fiscal_p
	USING gist
	(
	  geom
	);
CREATE TABLE cb.adm_posto_fiscal_a(
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT adm_posto_fiscal_a_pk PRIMARY KEY (id)
) INHERITS(cb.adm_posto_fiscal)
;
ALTER TABLE cb.adm_posto_fiscal_a OWNER TO postgres;
CREATE INDEX adm_posto_fiscal_a_gist ON cb.adm_posto_fiscal_a
	USING gist
	(
	  geom
	);
CREATE INDEX tra_area_estrut_transporte_a_gist ON cb.tra_area_estrut_transporte_a
	USING gist
	(
	  geom
	);
CREATE INDEX loc_area_edificada_a_gist ON cb.loc_area_edificada_a
	USING gist
	(
	  geom
	);
CREATE INDEX hid_trecho_massa_dagua_a_gist ON cb.hid_trecho_massa_dagua_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.loc_hab_indigena_p(
	geom geometry(POINT, [epsg]) NOT NULL,
	CONSTRAINT loc_hab_indigena_p_pk PRIMARY KEY (id)
) INHERITS(cb.loc_hab_indigena)
;
ALTER TABLE cb.loc_hab_indigena_p OWNER TO postgres;
CREATE INDEX loc_hab_indigena_p_gist ON cb.loc_hab_indigena_p
	USING gist
	(
	  geom
	);
CREATE INDEX loc_hab_indigena_a_gist ON cb.loc_hab_indigena_a
	USING gist
	(
	  geom
	);
CREATE TABLE cb.loc_area_urbana_isolada_a(
	id serial NOT NULL,
	geometriaaproximada smallint NOT NULL,
	nome varchar(80),
	nomeabrev varchar(50),
	tipoassociado smallint NOT NULL,
	geom geometry(POLYGON, [epsg]) NOT NULL,
	CONSTRAINT loc_area_urbana_isolada_a_pk PRIMARY KEY (id)
);
ALTER TABLE cb.loc_area_urbana_isolada_a OWNER TO postgres;
CREATE INDEX loc_area_urbana_isolada_a_gist ON cb.loc_area_urbana_isolada_a
	USING gist
	(
	  geom
	);
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
	order by t2.relname