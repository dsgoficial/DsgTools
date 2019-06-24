CREATE SCHEMA cb#
CREATE SCHEMA dominios#

CREATE EXTENSION postgis#
SET search_path TO pg_catalog,public,cb,dominios#

CREATE TABLE public.db_metadata(
	 edgvversion varchar(50) NOT NULL DEFAULT '2.1.3',
	 dbimplversion varchar(50) NOT NULL DEFAULT '3.00',
	 CONSTRAINT edgvversioncheck CHECK (edgvversion = '2.1.3')
)#
INSERT INTO public.db_metadata (edgvversion, dbimplversion) VALUES ('2.1.3','3.00')#

CREATE TABLE dominios.tipounidusosust (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipounidusosust_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (1,'Área de Proteção Ambiental - APA')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (2,'Área de Relevante Interesse Ecológico - ARIE')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (3,'Floresta - FLO')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (4,'Reserva de Desenvolvimento Sustentável - RDS')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (5,'Reserva Extrativista - RESEX')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (6,'Reserva de Fauna - REFAU')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (7,'Reserva Particular do Patrimônio Natural - RPPN')#
INSERT INTO dominios.tipounidusosust (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.isolada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT isolada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.isolada (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.isolada (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.isolada (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.isolada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.frigorifico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT frigorifico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.frigorifico (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.frigorifico (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.frigorifico (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.frigorifico (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.espessalgas (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT espessalgas_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.espessalgas (code,code_name) VALUES (1,'Finas')#
INSERT INTO dominios.espessalgas (code,code_name) VALUES (2,'Médias')#
INSERT INTO dominios.espessalgas (code,code_name) VALUES (3,'Grossas')#
INSERT INTO dominios.espessalgas (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.trafego (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT trafego_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.trafego (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.trafego (code,code_name) VALUES (1,'Permanente')#
INSERT INTO dominios.trafego (code,code_name) VALUES (2,'Periódico')#
INSERT INTO dominios.trafego (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.bitola (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT bitola_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.bitola (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.bitola (code,code_name) VALUES (1,'Métrica')#
INSERT INTO dominios.bitola (code,code_name) VALUES (2,'Internacional')#
INSERT INTO dominios.bitola (code,code_name) VALUES (3,'Larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (4,'Mista Métrica Internacional')#
INSERT INTO dominios.bitola (code,code_name) VALUES (5,'Mista Métrica Larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (6,'Mista Internacional Larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.emduto (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT emduto_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.emduto (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.emduto (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.emduto (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipomarcolim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipomarcolim_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipomarcolim (code,code_name) VALUES (1,'Internacional')#
INSERT INTO dominios.tipomarcolim (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.tipomarcolim (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.tipomarcolim (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipomarcolim (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipopassagviad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipopassagviad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipopassagviad (code,code_name) VALUES (5,'Passagem elevada')#
INSERT INTO dominios.tipopassagviad (code,code_name) VALUES (6,'Viaduto')#
INSERT INTO dominios.tipopassagviad (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_asb (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_asb_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (2,'Tratamento')#
INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (4,'Distribuição')#
INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (8,'Armazenamento')#
INSERT INTO dominios.finalidade_asb (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.mattransp (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT mattransp_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.mattransp (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (1,'Água')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (2,'Óleo')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (4,'Nafta')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (6,'Grãos')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (7,'Minério')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (8,'Efluentes')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (9,'Esgoto')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (29,'Gasolina')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (30,'Álcool')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (31,'Querosene')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.mattransp (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoediflazer (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoediflazer_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (1,'Estádio')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (2,'Ginásio')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (3,'Museu')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (4,'Teatro')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (5,'Anfiteatro')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (6,'Cinema')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (7,'Centro cultural')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (8,'Plataforma de pesca')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (9,'Chaminé')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoediflazer (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipopostofisc (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipopostofisc_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (10,'Tributação')#
INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (11,'Fiscalização')#
INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipopostofisc (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.referencialgrav (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencialgrav_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.referencialgrav (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (1,'Postdam 1930')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (2,'IGSN71')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (3,'Absoluto')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (4,'Local')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (97,'Não Aplicável')#
INSERT INTO dominios.referencialgrav (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoobst (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoobst_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoobst (code,code_name) VALUES (4,'Natural')#
INSERT INTO dominios.tipoobst (code,code_name) VALUES (5,'Artificial')#
INSERT INTO dominios.tipoobst (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoelemnat (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoelemnat_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (1,'Serra')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (2,'Morro')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (3,'Montanha')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (4,'Chapada')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (5,'Maciço')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (6,'Planalto')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (7,'Planície')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (8,'Escarpa')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (9,'Península')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (10,'Ponta')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (11,'Cabo')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (12,'Praia')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (13,'Falésia')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (14,'Talude')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoelemnat (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.residuo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT residuo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.residuo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.residuo (code,code_name) VALUES (1,'Líquido')#
INSERT INTO dominios.residuo (code,code_name) VALUES (2,'Sólido')#
INSERT INTO dominios.residuo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotorre (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotorre_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotorre (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipotorre (code,code_name) VALUES (1,'Autoportante')#
INSERT INTO dominios.tipotorre (code,code_name) VALUES (2,'Estaiada')#
INSERT INTO dominios.tipotorre (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifmil (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifmil_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (12,'Aquartelamento')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (13,'Campo de instrução')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (14,'Campo de tiro')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (15,'Base aérea')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (16,'Distrito naval')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (17,'Hotel de trânsito')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (18,'Delegacia serviço militar')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (19,'Posto')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifmil (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.modaluso (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT modaluso_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.modaluso (code,code_name) VALUES (4,'Rodoviário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (5,'Ferroviário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (6,'Metroviário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (7,'Dutos')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (8,'Rodoferroviário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (9,'Aeroportuário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (14,'Portuário')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.modaluso (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.matconstr (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT matconstr_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.matconstr (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (1,'Alvenaria')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (2,'Concreto')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (3,'Metal')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (4,'Rocha')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (5,'Madeira')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (6,'Arame')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (7,'Tela ou Alambrado')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (8,'Cerca viva')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (23,'Terra')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (25,'Fibra ótica')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (26,'Fio Metálico')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (97,'Não Aplicável')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.matconstr (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaoespacial (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaoespacial_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaoespacial (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.situacaoespacial (code,code_name) VALUES (12,'Adjacentes')#
INSERT INTO dominios.situacaoespacial (code,code_name) VALUES (13,'Superpostos')#
INSERT INTO dominios.situacaoespacial (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.situacaoespacial (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipodepsaneam (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipodepsaneam_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (1,'Tanque')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (4,'Depósito de lixo')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (5,'Aterro sanitário')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (6,'Aterro controlado')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipodepsaneam (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.terreno (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT terreno_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.terreno (code,code_name) VALUES (1,'Seco')#
INSERT INTO dominios.terreno (code,code_name) VALUES (2,'Irrigado')#
INSERT INTO dominios.terreno (code,code_name) VALUES (3,'Inundado')#
INSERT INTO dominios.terreno (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotrechoferrov (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotrechoferrov_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (5,'Bonde')#
INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (6,'Aeromóvel')#
INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (7,'Ferrovia')#
INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (8,'Metrovia')#
INSERT INTO dominios.tipotrechoferrov (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.depressao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT depressao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.depressao (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.depressao (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.depressao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocomplexoportuario (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocomplexoportuario_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocomplexoportuario (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocomplexoportuario (code,code_name) VALUES (30,'Porto organizado')#
INSERT INTO dominios.tipocomplexoportuario (code,code_name) VALUES (31,'Instalação portuária')#
INSERT INTO dominios.tipocomplexoportuario (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipobrejopantano (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipobrejopantano_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipobrejopantano (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipobrejopantano (code,code_name) VALUES (1,'Brejo')#
INSERT INTO dominios.tipobrejopantano (code,code_name) VALUES (2,'Pântano')#
INSERT INTO dominios.tipobrejopantano (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipodelimfis (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipodelimfis_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipodelimfis (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipodelimfis (code,code_name) VALUES (1,'Cerca')#
INSERT INTO dominios.tipodelimfis (code,code_name) VALUES (2,'Muro')#
INSERT INTO dominios.tipodelimfis (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.materialpredominante (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT materialpredominante_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.materialpredominante (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (4,'Rocha')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (12,'Areia')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (13,'Areia Fina')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (14,'Lama')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (15,'Argila')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (16,'Lodo')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (19,'Seixo')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (20,'Coral')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (21,'Concha')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (22,'Ervas Marinhas')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (24,'Saibro')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (50,'Pedra')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (97,'Não Aplicável')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.materialpredominante (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocomplexoaero (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocomplexoaero_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocomplexoaero (code,code_name) VALUES (23,'Aeródromo')#
INSERT INTO dominios.tipocomplexoaero (code,code_name) VALUES (24,'Aeroporto')#
INSERT INTO dominios.tipocomplexoaero (code,code_name) VALUES (25,'Heliporto')#
INSERT INTO dominios.tipocomplexoaero (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.poderpublico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT poderpublico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.poderpublico (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.poderpublico (code,code_name) VALUES (1,'Executivo')#
INSERT INTO dominios.poderpublico (code,code_name) VALUES (2,'Legislativo')#
INSERT INTO dominios.poderpublico (code,code_name) VALUES (3,'Judiciário')#
INSERT INTO dominios.poderpublico (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoassociado (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoassociado_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoassociado (code,code_name) VALUES (1,'Cidade')#
INSERT INTO dominios.tipoassociado (code,code_name) VALUES (4,'Vila')#
INSERT INTO dominios.tipoassociado (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipodivisaocnae (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipodivisaocnae_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (1,'Agricultura Pecuária e Serviços Relacionados')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (2,'Silvicultura Exploração Florestal e Serviços Relacionados')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (5,'Pesca Aquicultura e Serviços Relacionados')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (10,'Extração de Carvão Mineral')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (11,'Extração de Petróleo e Serviços Relacionados')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (13,'Extração de Minerais Metálicos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (14,'Extração de Minerais Não-Metálicos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (15,'Fabricação Alimentícia e Bebidas')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (16,'Fabricação de Produtos do Fumo')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (17,'Fabricação de Produtos Têxteis')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (18,'Confecção de Artigos do Vestuário e Acessórios')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (19,'Preparação de couros e Fabricação de Artefatos de Couro Artigos de Viagem e Calçados')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (20,'Fabricação de produtos de Madeira e Celulose')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (21,'Fabricação de Celulose Papel e Produtos de Papel')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (22,'Edição Impressão e Reprodução de Gravações')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (23,'Fabricação de Coque Refino de Petróleo Elaboração de Combustíveis Nucleares e Produção de Álcool')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (24,'Fabricação de Produtos Químicos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (25,'Fabricação de Artigos de Borracha e Material Plástico')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (26,'Fabricação de Produtos de Minerais Não-Metálicos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (27,'Metalurgia Básica')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (28,'Fabricação de Produtos de Metal Exclusive Máquinas e Equipamentos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (29,'Fabricação de Máquinas e Equipamentos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (30,'Fabricação de Máquinas de Escritório e Equipamentos de Informática')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (31,'Fabricação de Máquinas Aparelhos e Materiais Elétricos')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (32,'Fabricação de Material Eletrônicode Aparelhos e Equipamentos de Comunicações')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (33,'Fabricação de Equipamentos de Instrumentação Médico-Hospitalares Instumentos de Precisão e Ópticos Equipamentos para Automação Industrial Cronômetros e Relógios')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (34,'Fabricação e Montagem de Veículos Automotores Reboques e Carrocerias')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (35,'Fabricação de Outros Equipamentos de Transporte')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (36,'Fabricação de Móveis e Industrias Diversas')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (37,'Reciclagem')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (45,'Construção')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (50,'Comércio e Reparação de Veículos Automotores e Motocicletas e Comércio a Varejo de Combustíveis.')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (51,'Comércio por Atacado e Representantes Comerciais. E agentes do comércio')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (52,'Comércio Varejista e Reparação de Objetos Pessoais e Domésticos.')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (55,'Alojamento e Alimentação')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (74,'Serviços Prestados Principalmente às Empresas (organizações).')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (92,'Atividades Recreativas Culturais e Desportivas')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipodivisaocnae (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipooutlimofic (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipooutlimofic_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (1,'Mar territorial')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (2,'Zona contígua')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (3,'Zona econômica exclusiva')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (4,'Lateral marítima')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (5,'Faixa de fronteira')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (6,'Plataforma continental jurídica')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipooutlimofic (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoquebramolhe (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoquebramolhe_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoquebramolhe (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoquebramolhe (code,code_name) VALUES (1,'Quebramar')#
INSERT INTO dominios.tipoquebramolhe (code,code_name) VALUES (2,'Molhe')#
INSERT INTO dominios.tipoquebramolhe (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifsaneam (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifsaneam_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (5,'Tratamento de esgoto')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (6,'Usina de reciclagem')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (7,'Incinerador')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifsaneam (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocomplexolazer (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocomplexolazer_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (1,'Complexo recreativo')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (2,'Clube')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (3,'Autódromo')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (4,'Parque de diversões')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (5,'Parque urbano')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (6,'Parque aquático')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (7,'Parque temático')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (8,'Hipódromo')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (9,'Hípica')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (10,'Estande de tiro')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (11,'Campo de golfe')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (12,'Parque de eventos culturais')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (13,'Camping')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (14,'Complexo desportivo')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (15,'Zoológico')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (16,'Jardim botânico')#
INSERT INTO dominios.tipocomplexolazer (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiposinal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiposinal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiposinal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (1,'Bóia luminosa')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (2,'Bóia cega')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (3,'Bóia de amarração')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (4,'Farol ou farolete')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (5,'Barca farol')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (6,'Sinalização de margem')#
INSERT INTO dominios.tiposinal (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.classificacaoporte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT classificacaoporte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (1,'Arbórea')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (2,'Arbustiva')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (3,'Herbácea')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (4,'Rasteira')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.classificacaoporte (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.navegabilidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT navegabilidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.navegabilidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.navegabilidade (code,code_name) VALUES (1,'Navegável')#
INSERT INTO dominios.navegabilidade (code,code_name) VALUES (2,'Não navegável')#
INSERT INTO dominios.navegabilidade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.qualidagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT qualidagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.qualidagua (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.qualidagua (code,code_name) VALUES (1,'Potável')#
INSERT INTO dominios.qualidagua (code,code_name) VALUES (2,'Não potável')#
INSERT INTO dominios.qualidagua (code,code_name) VALUES (3,'Mineral')#
INSERT INTO dominios.qualidagua (code,code_name) VALUES (4,'Salobra')#
INSERT INTO dominios.qualidagua (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaoemagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaoemagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaoemagua (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.situacaoemagua (code,code_name) VALUES (4,'Emerso')#
INSERT INTO dominios.situacaoemagua (code,code_name) VALUES (5,'Submerso')#
INSERT INTO dominios.situacaoemagua (code,code_name) VALUES (7,'Cobre e Descobre')#
INSERT INTO dominios.situacaoemagua (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.ocorrenciaem (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT ocorrenciaem_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (5,'Brejo ou Pântano')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (6,'Caatinga')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (7,'Estepe')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (8,'Pastagem')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (13,'Cerrado ou cerradão')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (14,'Macega ou chavascal')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (15,'Floresta')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (19,'Campinarana')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (96,'Não Identificado')#
INSERT INTO dominios.ocorrenciaem (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.modalidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT modalidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.modalidade (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (1,'Radiocomunicação')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (2,'Radiodifusão/som e imagem')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (3,'Telefonia')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (4,'Dados')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (5,'Radiodifusão/som')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (99,'Outras')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifagropec (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifagropec_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (12,'Sede operacional de fazenda')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (13,'Aviário')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (14,'Apiário')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (15,'Viveiro de plantas')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (16,'Viveiro para aquicultura')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (17,'Pocilga')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (18,'Curral')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifagropec (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolimintramun (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolimintramun_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (1,'Distrital')#
INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (2,'Sub-distrital')#
INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (3,'Perímetro urbano legal')#
INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (4,'Região administrativa')#
INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (5,'Bairro')#
INSERT INTO dominios.tipolimintramun (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipousocaminhoaer (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipousocaminhoaer_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipousocaminhoaer (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipousocaminhoaer (code,code_name) VALUES (21,'Passageiros')#
INSERT INTO dominios.tipousocaminhoaer (code,code_name) VALUES (22,'Cargas')#
INSERT INTO dominios.tipousocaminhoaer (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipousocaminhoaer (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoareaumida (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoareaumida_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoareaumida (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoareaumida (code,code_name) VALUES (3,'Lamacento')#
INSERT INTO dominios.tipoareaumida (code,code_name) VALUES (4,'Arenoso')#
INSERT INTO dominios.tipoareaumida (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.destenergelet (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT destenergelet_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.destenergelet (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (1,'Auto-Produção de Energia (APE)')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (2,'Auto-Produção com Comercialização de Excedente (APE-COM)')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (3,'Comercialização de Energia (COM)')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (4,'Produção Independente de Energia (PIE)')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (5,'Serviço Público (SP)')#
INSERT INTO dominios.destenergelet (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.relacionado_hid (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT relacionado_hid_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (1,'Eclusa')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (2,'Barragem')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (3,'Comporta')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (4,'Queda d’água')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (5,'Corredeira')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (6,'Foz marítima')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (7,'Sumidouro')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (8,'Meandro abandonado')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (9,'Lago')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (10,'Lagoa')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (11,'Laguna')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (12,'Represa/ açude')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (13,'Entre trechos de drenagem')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (16,'Vertedouro')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (17,'Interrupção à Jusante')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (18,'Interrupção à Montante')#
INSERT INTO dominios.relacionado_hid (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.procextracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT procextracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.procextracao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.procextracao (code,code_name) VALUES (1,'Mecanizado')#
INSERT INTO dominios.procextracao (code,code_name) VALUES (2,'Manual')#
INSERT INTO dominios.procextracao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipooutunidprot (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipooutunidprot_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (1,'Área de preservação permanente')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (2,'Reserva legal')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (3,'Mosaico')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (4,'Distrito florestal')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (5,'Corredor ecológico')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (6,'Floresta pública')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (7,'Sítios RAMSAR')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (8,'Sítios do patrimônio')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (9,'Reserva da biosfera')#
INSERT INTO dominios.tipooutunidprot (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoconteudo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoconteudo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoconteudo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoconteudo (code,code_name) VALUES (1,'Insumo')#
INSERT INTO dominios.tipoconteudo (code,code_name) VALUES (2,'Produto')#
INSERT INTO dominios.tipoconteudo (code,code_name) VALUES (3,'Resíduo')#
INSERT INTO dominios.tipoconteudo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoextmin (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoextmin_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoextmin (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (1,'Poço')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (4,'Mina')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (5,'Garimpo')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (6,'Salina')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (7,'Pedreira')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (8,'Ponto de Prospecção')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoextmin (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiporef (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiporef_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiporef (code,code_name) VALUES (1,'Altimétrico')#
INSERT INTO dominios.tiporef (code,code_name) VALUES (2,'Planimétrico')#
INSERT INTO dominios.tiporef (code,code_name) VALUES (3,'Planialtimétrico')#
INSERT INTO dominios.tiporef (code,code_name) VALUES (4,'Gravimétrico')#
INSERT INTO dominios.tiporef (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifcivil (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifcivil_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (1,'Policial')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (2,'Prisional')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (3,'Cartorial')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (4,'Gestão')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (5,'Eleitoral')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (6,'Produção e/ou pesquisa')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (7,'Seguridade Social')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (8,'Câmara Municipal')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (9,'Assembléia Legislativa')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (22,'Prefeitura')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifcivil (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifport (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifport_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifport (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (15,'Administrativa')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (26,'Terminal de passageiros')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (27,'Terminal de cargas')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (32,'Armazém')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (33,'Estaleiro')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (34,'Dique de estaleiro')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (35,'Rampa')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (36,'Carreira')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (37,'Terminal privativo')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifport (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoclassecnae (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoclassecnae_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (1,'40.11-8 - Produção de Energia Elétrica')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (2,'40.12-6 - Transmissão de Energia Elétrica')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (3,'40.14-2 - Distribuição de Energia Elétrica')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (4,'41.00-9 - Captação Tratamento e Distribuição de Água')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (5,'64.20-3 - Telecomunicações')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (6,'75.11-6 - Administração Pública em Geral')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (7,'75.12-4 - Regulação das Atividades Sociais e Culturais')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (8,'75.13-2 - Regulação das Atividades Econômicas')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (9,'75.14-0 - Atividades de Apoio à Administração Pública')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (10,'75.21-3 - Relações Exteriores')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (11,'75.22-1 - Defesa')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (12,'75.23-0 - Justiça')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (13,'75.24-8 - Segurança e Ordem Pública')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (14,'75.25-6 - Defesa Civil')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (15,'75.30-2 - Seguridade Social')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (16,'80.13-6 - Educação Infantil - Creche')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (17,'80.14-4 - Educação Infantil - Pré-Escola')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (18,'80.15-2 - Ensino Fundamental')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (19,'80.20-9 - Ensino Médio')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (20,'80.31-4 - Educação Superior - Graduação')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (21,'80.32-2 - Educação Superior - Graduação e Pós-Graduação')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (22,'80.33-0 - Educação Superior - Pós-Graduação e Extensão')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (23,'80.96-9 - Educação Profissional de Nível Técnico')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (24,'80.97-7 - Educação Profissional de Nível Tecnológico')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (25,'80.99-3 - Outras Atividades de Ensino')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (26,'85.11-1 Atendimento Hospitalar (Hospital)')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (27,'85.12-0 Atendimento a Urgência e Emergências (Pronto Socorro)')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (28,'85.13-8 Atenção Ambulatorial (Posto e Centro de Saúde)')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (29,'85.14-6 Serviços de Complementação Diagnóstica ou Terapêutica')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (30,'85.16-2 Outras Atividades Relacionadas com a Atenção à Saúde (Instituto de Pesquisa)')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (31,'85.20-0 Serviços Veterinários')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (32,'85.31-6 - Serviços Sociais com alojamento')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (33,'85.32-4 - Serviços Sociais sem alojamento')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (34,'90.00-0 - Limpeza Urbana e Esgoto e Atividades Relacionadas')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (35,'91.91-0 - Atividades de Organizações Religiosas')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (97,'Não Aplicável')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoclassecnae (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipogrupocnae (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipogrupocnae_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (1,'80.1 - Educação Infantil e Ensino Fundamental')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (3,'80.3 - Ensino Superior')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (4,'80.9 - Educação Profissional e Outras Atividades de Ensino')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (5,'75-1 - Administração do Estado e da Política Econômica e Social')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (6,'75-2 - Serviços Coletivos Prestados pela Administração Pública')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (7,'75-3 - Seguridade Social')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (8,'85.1 Atividades de Atenção à Saúde')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (9,'85.2 Serviços Veterinários')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (10,'85-3 - Serviço Social')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (19,'80.2 - Ensino Médio')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipogrupocnae (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_veg (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_veg_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (1,'Exploração econômica')#
INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (2,'Subistência')#
INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (3,'Conservação ambiental')#
INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.finalidade_veg (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.regime (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT regime_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.regime (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.regime (code,code_name) VALUES (1,'Permanente')#
INSERT INTO dominios.regime (code,code_name) VALUES (2,'Permanente com grande variação')#
INSERT INTO dominios.regime (code,code_name) VALUES (3,'Temporário')#
INSERT INTO dominios.regime (code,code_name) VALUES (4,'Temporário com leito permanente')#
INSERT INTO dominios.regime (code,code_name) VALUES (5,'Seco')#
INSERT INTO dominios.regime (code,code_name) VALUES (6,'Sazonal')#
INSERT INTO dominios.regime (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.denominacaoassociada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT denominacaoassociada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (5,'Cristã')#
INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (6,'Israelita')#
INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (7,'Muçulmana')#
INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (99,'Outras')#
INSERT INTO dominios.denominacaoassociada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiposecaocnae (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiposecaocnae_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (1,'C - Indústrias Extrativas')#
INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (2,'D - Indústrias de Transformação')#
INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (3,'F - Construção')#
INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tiposecaocnae (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotransporte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotransporte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotransporte (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipotransporte (code,code_name) VALUES (21,'Passageiros')#
INSERT INTO dominios.tipotransporte (code,code_name) VALUES (22,'Cargas')#
INSERT INTO dominios.tipotransporte (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipotransporte (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotravessia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotravessia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotravessia (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.tipotravessia (code,code_name) VALUES (1,'Vau natural')#
INSERT INTO dominios.tipotravessia (code,code_name) VALUES (2,'Vau construída')#
INSERT INTO dominios.tipotravessia (code,code_name) VALUES (3,'Bote transportador')#
INSERT INTO dominios.tipotravessia (code,code_name) VALUES (4,'Balsa')#
INSERT INTO dominios.tipotravessia (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipobanco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipobanco_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipobanco (code,code_name) VALUES (1,'Fluvial')#
INSERT INTO dominios.tipobanco (code,code_name) VALUES (2,'Marítimo')#
INSERT INTO dominios.tipobanco (code,code_name) VALUES (3,'Lacustre')#
INSERT INTO dominios.tipobanco (code,code_name) VALUES (4,'Cordão Arenoso')#
INSERT INTO dominios.tipobanco (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocombustivel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocombustivel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (1,'Nuclear')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (3,'Diesel')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (33,'Carvão')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipocombustivel (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifrelig (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifrelig_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (1,'Igreja')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (2,'Templo')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (3,'Centro')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (4,'Mosteiro')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (5,'Convento')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (6,'Mesquita')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (7,'Sinagoga')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifrelig (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipopostopol (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipopostopol_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipopostopol (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipopostopol (code,code_name) VALUES (20,'Posto PM')#
INSERT INTO dominios.tipopostopol (code,code_name) VALUES (21,'Posto PRF')#
INSERT INTO dominios.tipopostopol (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaomarco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaomarco_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaomarco (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (1,'Bom')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (2,'Destruído')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (3,'Destruído sem chapa')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (4,'Destruído com chapa danificada')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (5,'Não encontrado')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (6,'Não visitado')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (7,'Não construído')#
INSERT INTO dominios.situacaomarco (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.ovgd (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT ovgd_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.ovgd (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.ovgd (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.ovgd (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.ovgd (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoterrexp (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoterrexp_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (4,'Pedregoso')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (12,'Areia')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (23,'Terra')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (24,'Saibro')#
INSERT INTO dominios.tipoterrexp (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolimmassa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolimmassa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (1,'Costa visível da carta')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (2,'Margem de massa d`água')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (3,'Margem esquerda de trechos de massa d`água')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (4,'Margem direita de trechos de massa d`água')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (5,'Limite interno entre massas e/ou trechos')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (6,'Limite com elemento artificial')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (7,'Limite interno com foz marítima')#
INSERT INTO dominios.tipolimmassa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.chamine (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT chamine_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.chamine (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.chamine (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.chamine (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.salinidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT salinidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.salinidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.salinidade (code,code_name) VALUES (1,'Doce')#
INSERT INTO dominios.salinidade (code,code_name) VALUES (2,'Salgada')#
INSERT INTO dominios.salinidade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoestgerad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoestgerad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (5,'Eólica')#
INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (6,'Solar')#
INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (7,'Maré-motriz')#
INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoestgerad (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipofontedagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipofontedagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipofontedagua (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipofontedagua (code,code_name) VALUES (1,'Poço')#
INSERT INTO dominios.tipofontedagua (code,code_name) VALUES (2,'Poço Artesiano')#
INSERT INTO dominios.tipofontedagua (code,code_name) VALUES (3,'Olho d`água')#
INSERT INTO dominios.tipofontedagua (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.nrlinhas (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nrlinhas_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nrlinhas (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.nrlinhas (code,code_name) VALUES (1,'Simples')#
INSERT INTO dominios.nrlinhas (code,code_name) VALUES (2,'Dupla')#
INSERT INTO dominios.nrlinhas (code,code_name) VALUES (3,'Múltipla')#
INSERT INTO dominios.nrlinhas (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolimpol (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolimpol_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolimpol (code,code_name) VALUES (1,'Internacional')#
INSERT INTO dominios.tipolimpol (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.tipolimpol (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.tipolimpol (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiposumvert (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiposumvert_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiposumvert (code,code_name) VALUES (1,'Sumidouro')#
INSERT INTO dominios.tiposumvert (code,code_name) VALUES (2,'Vertedouro')#
INSERT INTO dominios.tiposumvert (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotrechocomunic (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotrechocomunic_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (4,'Dados')#
INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (6,'Telegráfica')#
INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (7,'Telefônica')#
INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipotrechocomunic (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotrechorod (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotrechorod_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotrechorod (code,code_name) VALUES (1,'Acesso')#
INSERT INTO dominios.tipotrechorod (code,code_name) VALUES (2,'Rodovia')#
INSERT INTO dominios.tipotrechorod (code,code_name) VALUES (3,'Caminho carroçável')#
INSERT INTO dominios.tipotrechorod (code,code_name) VALUES (4,'Auto-estrada')#
INSERT INTO dominios.tipotrechorod (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocapital (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocapital_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocapital (code,code_name) VALUES (2,'Capital Federal')#
INSERT INTO dominios.tipocapital (code,code_name) VALUES (3,'Capital Estadual')#
INSERT INTO dominios.tipocapital (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolimareaesp (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolimareaesp_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (1,'Terra pública')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (2,'Terra indígena')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (3,'Quilombo')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (4,'Assentamento rural')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (5,'Amazônia legal')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (6,'Faixa de fronteira')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (7,'Polígono das secas')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (8,'Área de preservação permanente')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (9,'Reserva legal')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (10,'Mosaico')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (11,'Distrito florestal')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (12,'Corredor ecológico')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (13,'Floresta pública')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (14,'Sítios RAMSAR')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (15,'Sítios do patrimônio')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (16,'Reserva da biosfera')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (17,'Reserva florestal')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (18,'Reserva ecológica')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (19,'Estação biológica')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (20,'Horto florestal')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (21,'Estrada parque')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (22,'Floresta de rendimento sustentável')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (23,'Floresta Extrativista')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (24,'Área de proteção ambiental - APA')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (25,'Área de Relevante Interesse Ecológico - ARIE')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (26,'Floresta - FLO')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (27,'Reserva de Desenvolvimento Sustentável - RDS')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (28,'Reserva Extrativista - RESEX')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (29,'Reserva de Fauna - REFAU')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (30,'Reserva Particular do Patrimônio Natural - RPPN')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (31,'Estação Ecológica - ESEC')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (32,'Parque - PAR')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (33,'Monumento Natural - MONA')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (34,'Reserva Biológica - REBIO')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (35,'Refúgio de Vida Silvestre - RVS')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (36,'Area Militar')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipolimareaesp (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipomassadagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipomassadagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (3,'Oceano')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (4,'Baía')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (5,'Enseada')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (6,'Meandro Abandonado')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (7,'Lago')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (8,'Lagoa')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (10,'Represa/Açude')#
INSERT INTO dominios.tipomassadagua (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.emarruamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT emarruamento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.emarruamento (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.emarruamento (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.emarruamento (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.emarruamento (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoareausocomun (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoareausocomun_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoareausocomun (code,code_name) VALUES (1,'Quilombo')#
INSERT INTO dominios.tipoareausocomun (code,code_name) VALUES (2,'Assentamento rural')#
INSERT INTO dominios.tipoareausocomun (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoestrut (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoestrut_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoestrut (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (1,'Estação')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (2,'Comércio e serviços')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (3,'Fiscalização')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (4,'Porto seco')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (5,'Terminal rodoviário')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (6,'Terminal urbano')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (7,'Terminal multimodal')#
INSERT INTO dominios.tipoestrut (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipooperativo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipooperativo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipooperativo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipooperativo (code,code_name) VALUES (1,'Elevadora')#
INSERT INTO dominios.tipooperativo (code,code_name) VALUES (2,'Abaixadora')#
INSERT INTO dominios.tipooperativo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.posicaoreledific (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicaoreledific_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicaoreledific (code,code_name) VALUES (14,'Isolado')#
INSERT INTO dominios.posicaoreledific (code,code_name) VALUES (17,'Adjacente a edificação')#
INSERT INTO dominios.posicaoreledific (code,code_name) VALUES (18,'Sobre edificação')#
INSERT INTO dominios.posicaoreledific (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipodepgeral (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipodepgeral_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (8,'Galpão')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (9,'Silo')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (10,'Composteira')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (11,'Depósito frigorífico')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (32,'Armazém')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipodepgeral (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.unidadevolume (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT unidadevolume_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.unidadevolume (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.unidadevolume (code,code_name) VALUES (1,'Litro')#
INSERT INTO dominios.unidadevolume (code,code_name) VALUES (2,'Metro cúbico')#
INSERT INTO dominios.unidadevolume (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.construcao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT construcao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.construcao (code,code_name) VALUES (1,'Fechada')#
INSERT INTO dominios.construcao (code,code_name) VALUES (2,'Aberta')#
INSERT INTO dominios.construcao (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.construcao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoexposicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoexposicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (3,'Fechado')#
INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (4,'Coberto')#
INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (5,'Céu aberto')#
INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoexposicao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoilha (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoilha_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoilha (code,code_name) VALUES (1,'Fluvial')#
INSERT INTO dominios.tipoilha (code,code_name) VALUES (2,'Marítima')#
INSERT INTO dominios.tipoilha (code,code_name) VALUES (3,'Lacustre')#
INSERT INTO dominios.tipoilha (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.tipoilha (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.geometriaaproximada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT geometriaaproximada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.geometriaaproximada (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.geometriaaproximada (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.geometriaaproximada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocampo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocampo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocampo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocampo (code,code_name) VALUES (1,'Sujo')#
INSERT INTO dominios.tipocampo (code,code_name) VALUES (2,'Limpo')#
INSERT INTO dominios.tipocampo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoalterantrop (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoalterantrop_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (24,'Caixa de empréstimo')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (25,'Área aterrada')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (26,'Corte')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (27,'Aterro')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (28,'Resíduo de bota-fora')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (29,'Resíduo sólido em geral')#
INSERT INTO dominios.tipoalterantrop (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocondutor (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocondutor_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocondutor (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocondutor (code,code_name) VALUES (2,'Calha')#
INSERT INTO dominios.tipocondutor (code,code_name) VALUES (4,'Tubulação')#
INSERT INTO dominios.tipocondutor (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifcomunic (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifcomunic_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (1,'Centro de operações')#
INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (2,'Central comutação e transmissão')#
INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (3,'Estação radio-base')#
INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (4,'Estação repetidora')#
INSERT INTO dominios.tipoedifcomunic (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.posicaorelativa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicaorelativa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (2,'Superfície')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (3,'Elevado')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (4,'Emerso')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (5,'Submerso')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (6,'Subterrâneo')#
INSERT INTO dominios.posicaorelativa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_eco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_eco_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_eco (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.finalidade_eco (code,code_name) VALUES (1,'Comercial')#
INSERT INTO dominios.finalidade_eco (code,code_name) VALUES (2,'Serviço')#
INSERT INTO dominios.finalidade_eco (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.finalidade_eco (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolocalcrit (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolocalcrit_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (1,'Subestação de válvulas e/ou bombas')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (2,'Risco geotécnico')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (3,'Interferência com localidades')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (4,'Interferência com hidrografia')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (5,'Interferência com áreas especiais')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (6,'Interferência com vias')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (7,'Outras interferências')#
INSERT INTO dominios.tipolocalcrit (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoprodutoresiduo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoprodutoresiduo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (6,'Grãos')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (16,'Vinhoto')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (17,'Estrume')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (19,'Semente')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (20,'Inseticida')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (21,'Folhagens')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (22,'Pedra')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (23,'Granito')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (24,'Mármore')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (25,'Bauxita')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (26,'Manganês')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (27,'Talco')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (28,'Óleo diesel')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (29,'Gasolina')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (30,'Álcool')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (31,'Querosene')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (32,'Cobre')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (33,'Carvão')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (34,'Sal')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (35,'Ferro')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (36,'Escória')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (37,'Ouro')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (38,'Diamante')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (39,'Prata')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (40,'Pedras preciosas')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (41,'Forragem')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (42,'Areia')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (43,'Saibro/Piçarra')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoprodutoresiduo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.relacionado_dut (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT relacionado_dut_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (1,'Ponto inicial')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (2,'Ponto final')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (3,'Local crítico')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (4,'Depósito geral')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (5,'Ponto de ramificação')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (17,'Interrupção com a Moldura')#
INSERT INTO dominios.relacionado_dut (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.ensino (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT ensino_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.ensino (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.ensino (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.ensino (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.ensino (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.eletrificada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT eletrificada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.eletrificada (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.eletrificada (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.eletrificada (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.eletrificada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.atividade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT atividade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.atividade (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.atividade (code,code_name) VALUES (9,'Prospecção')#
INSERT INTO dominios.atividade (code,code_name) VALUES (10,'Produção')#
INSERT INTO dominios.atividade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotrechoduto (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotrechoduto_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotrechoduto (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipotrechoduto (code,code_name) VALUES (1,'Duto')#
INSERT INTO dominios.tipotrechoduto (code,code_name) VALUES (2,'Calha')#
INSERT INTO dominios.tipotrechoduto (code,code_name) VALUES (3,'Correia transportadora')#
INSERT INTO dominios.tipotrechoduto (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.multimodal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT multimodal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.multimodal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.multimodal (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.multimodal (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.multimodal (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.administracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT administracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.administracao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.administracao (code,code_name) VALUES (1,'Federal')#
INSERT INTO dominios.administracao (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.administracao (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.administracao (code,code_name) VALUES (4,'Estadual/Municipal')#
INSERT INTO dominios.administracao (code,code_name) VALUES (5,'Distrital')#
INSERT INTO dominios.administracao (code,code_name) VALUES (6,'Particular')#
INSERT INTO dominios.administracao (code,code_name) VALUES (7,'Concessionada')#
INSERT INTO dominios.administracao (code,code_name) VALUES (15,'Privada')#
INSERT INTO dominios.administracao (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.administracao (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.administracao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.combrenovavel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT combrenovavel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.combrenovavel (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.combrenovavel (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.combrenovavel (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.combrenovavel (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tratamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tratamento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tratamento (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tratamento (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.tratamento (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.tratamento (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.tratamento (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.usopista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT usopista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.usopista (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.usopista (code,code_name) VALUES (6,'Particular')#
INSERT INTO dominios.usopista (code,code_name) VALUES (11,'Público')#
INSERT INTO dominios.usopista (code,code_name) VALUES (12,'Militar')#
INSERT INTO dominios.usopista (code,code_name) VALUES (13,'Público/Militar')#
INSERT INTO dominios.usopista (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.destinadoa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT destinadoa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.destinadoa (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (5,'Madeira')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (18,'Açaí')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (34,'Turfa')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (35,'Látex')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (36,'Castanha')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (37,'Carnaúba')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (38,'Coco')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (39,'Jaborandi')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (40,'Palmito')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (41,'Babaçu')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (43,'Pecuária')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (44,'Pesca')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.destinadoa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipousoedif (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipousoedif_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipousoedif (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipousoedif (code,code_name) VALUES (1,'Próprio nacional')#
INSERT INTO dominios.tipousoedif (code,code_name) VALUES (2,'Uso especial da União')#
INSERT INTO dominios.tipousoedif (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.classificsigiloso (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT classificsigiloso_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.classificsigiloso (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.classificsigiloso (code,code_name) VALUES (1,'Sigiloso')#
INSERT INTO dominios.classificsigiloso (code,code_name) VALUES (2,'Ostensivo')#
INSERT INTO dominios.classificsigiloso (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.rede (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT rede_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.rede (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.rede (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.rede (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.rede (code,code_name) VALUES (14,'Nacional')#
INSERT INTO dominios.rede (code,code_name) VALUES (15,'Privada')#
INSERT INTO dominios.rede (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.cotacomprovada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT cotacomprovada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.cotacomprovada (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.cotacomprovada (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.cotacomprovada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipodepabast (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipodepabast_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipodepabast (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipodepabast (code,code_name) VALUES (1,'Tanque')#
INSERT INTO dominios.tipodepabast (code,code_name) VALUES (2,'Caixa d`água')#
INSERT INTO dominios.tipodepabast (code,code_name) VALUES (3,'Cisterna')#
INSERT INTO dominios.tipodepabast (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipodepabast (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.motivodescontinuidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT motivodescontinuidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (1,'Descontinuidade Temporal')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (2,'Descontinuidade devido a transformação')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (3,'Descontinuidade por escala de insumo')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (4,'Descontinuidade por falta de acurácia')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (5,'Descontinuidade por diferente interpretação das classes')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (6,'Descontinuidade por omissão')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (7,'Descontinuidade por excesso')#
INSERT INTO dominios.motivodescontinuidade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situamare (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situamare_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situamare (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.situamare (code,code_name) VALUES (7,'Cobre e descobre')#
INSERT INTO dominios.situamare (code,code_name) VALUES (8,'Sempre fora d´água')#
INSERT INTO dominios.situamare (code,code_name) VALUES (9,'Sempre submerso')#
INSERT INTO dominios.situamare (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiporocha (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiporocha_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiporocha (code,code_name) VALUES (21,'Matacão - pedra')#
INSERT INTO dominios.tiporocha (code,code_name) VALUES (22,'Penedo - isolado')#
INSERT INTO dominios.tiporocha (code,code_name) VALUES (23,'Área Rochosa - lajedo')#
INSERT INTO dominios.tiporocha (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifaero (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifaero_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (15,'Administrativa')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (26,'Terminal de passageiros')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (27,'Terminal de cargas')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (28,'Torre de controle')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (29,'Hangar')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifaero (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.especie (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT especie_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.especie (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.especie (code,code_name) VALUES (2,'Transmissão')#
INSERT INTO dominios.especie (code,code_name) VALUES (3,'Distribuição')#
INSERT INTO dominios.especie (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.coincidecomdentrode_lim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT coincidecomdentrode_lim_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (2,'Contorno Massa D`Água')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (3,'Cumeada')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (4,'Linha Seca')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (5,'Costa Visível da Carta')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (6,'Rodovia')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (7,'Ferrovia')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (8,'Trecho de Drenagem')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (9,'Massa D`Água')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (96,'Não Identificado')#
INSERT INTO dominios.coincidecomdentrode_lim (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoaglomrurisol (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoaglomrurisol_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoaglomrurisol (code,code_name) VALUES (5,'Aglomerado Rural Isolado - Povoado')#
INSERT INTO dominios.tipoaglomrurisol (code,code_name) VALUES (6,'Aglomerado Rural Isolado - Núcleo')#
INSERT INTO dominios.tipoaglomrurisol (code,code_name) VALUES (7,'Outros Aglomerados Rurais Isolados')#
INSERT INTO dominios.tipoaglomrurisol (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocaminhoaereo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocaminhoaereo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocaminhoaereo (code,code_name) VALUES (12,'Teleférico')#
INSERT INTO dominios.tipocaminhoaereo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipocaminhoaereo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.jurisdicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT jurisdicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.jurisdicao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (1,'Federal')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (6,'Particular')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (8,'Propriedade particular')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.nivelatencao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nivelatencao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nivelatencao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.nivelatencao (code,code_name) VALUES (5,'Primário')#
INSERT INTO dominios.nivelatencao (code,code_name) VALUES (6,'Secundário')#
INSERT INTO dominios.nivelatencao (code,code_name) VALUES (7,'Terciário')#
INSERT INTO dominios.nivelatencao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.especiepredominante (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT especiepredominante_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.especiepredominante (code,code_name) VALUES (10,'Cipó')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (11,'Bambu')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (12,'Sororoca')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (17,'Palmeira')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (27,'Araucária')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (41,'Babaçu')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (96,'Não identificado')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.especiepredominante (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolimoper (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolimoper_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolimoper (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (1,'Setor censitário')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (2,'Linha de base normal')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (3,'Linha de base reta')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (4,'Costa visível da carta(interpretada)')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (5,'Linha preamar média - 1831')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (6,'Linha média de enchente-ORD')#
INSERT INTO dominios.tipolimoper (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocemiterio (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocemiterio_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (1,'Crematório')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (2,'Parque')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (3,'Vertical')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (4,'Comum')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (5,'Túmulo Isolado')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipocemiterio (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.classificacao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT classificacao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.classificacao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.classificacao (code,code_name) VALUES (9,'Internacional')#
INSERT INTO dominios.classificacao (code,code_name) VALUES (10,'Doméstico')#
INSERT INTO dominios.classificacao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoptoestmed (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoptoestmed_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (1,'Estação Climatológica Principal - CP')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (2,'Estação Climatológica Auxiliar - CA')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (3,'Estação Agroclimatológica - AC')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (4,'Estação Pluviométrica - PL')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (5,'Estação Eólica - EO')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (6,'Estação Evaporimétrica - EV')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (7,'Estação Solarimétrica - SL')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (8,'Estação de Radar Meteorológico - RD')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (9,'Estação de Radiossonda - RS')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (10,'Estação Fluviométrica - FL')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (11,'Estação Maregráfica - MA')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (12,'Estação de Marés Terrestres - Crosta')#
INSERT INTO dominios.tipoptoestmed (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoequipagropec (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoequipagropec_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoequipagropec (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoequipagropec (code,code_name) VALUES (1,'Pivô central')#
INSERT INTO dominios.tipoequipagropec (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoequipagropec (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.compartilhado (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT compartilhado_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.compartilhado (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.compartilhado (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.compartilhado (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.proximidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT proximidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.proximidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (14,'Isolado')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (15,'Adjacente')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (16,'Coincidente')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.eixoprincipal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT eixoprincipal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.eixoprincipal (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.eixoprincipal (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.eixoprincipal (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoqueda (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoqueda_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoqueda (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoqueda (code,code_name) VALUES (1,'Cachoeira')#
INSERT INTO dominios.tipoqueda (code,code_name) VALUES (2,'Salto')#
INSERT INTO dominios.tipoqueda (code,code_name) VALUES (3,'Catarata')#
INSERT INTO dominios.tipoqueda (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.canteirodivisorio (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT canteirodivisorio_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.canteirodivisorio (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.canteirodivisorio (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.canteirodivisorio (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifenergia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifenergia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (1,'Administração')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (2,'Oficinas')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (3,'Segurança')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (4,'Depósito')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (5,'Chaminé')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifenergia (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.referencialaltim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencialaltim_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.referencialaltim (code,code_name) VALUES (1,'Torres')#
INSERT INTO dominios.referencialaltim (code,code_name) VALUES (2,'Imbituba')#
INSERT INTO dominios.referencialaltim (code,code_name) VALUES (3,'Santana')#
INSERT INTO dominios.referencialaltim (code,code_name) VALUES (4,'Local')#
INSERT INTO dominios.referencialaltim (code,code_name) VALUES (5,'Outra referência')#
INSERT INTO dominios.referencialaltim (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.formaextracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT formaextracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.formaextracao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.formaextracao (code,code_name) VALUES (5,'Céu aberto')#
INSERT INTO dominios.formaextracao (code,code_name) VALUES (6,'Subterrâneo')#
INSERT INTO dominios.formaextracao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipomacchav (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipomacchav_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipomacchav (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipomacchav (code,code_name) VALUES (1,'Macega')#
INSERT INTO dominios.tipomacchav (code,code_name) VALUES (2,'Chavascal')#
INSERT INTO dominios.tipomacchav (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipomaqtermica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipomaqtermica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (1,'Turbina à gás (TBGS)')#
INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (2,'Turbina à vapor (TBVP)')#
INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (3,'Ciclo combinado (CLCB)')#
INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (4,'Motor de Combustão Interna (NCIA)')#
INSERT INTO dominios.tipomaqtermica (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotunel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotunel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotunel (code,code_name) VALUES (1,'Túnel')#
INSERT INTO dominios.tipotunel (code,code_name) VALUES (2,'Passagem subterrânea sob via')#
INSERT INTO dominios.tipotunel (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipopista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipopista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipopista (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (1,'Atletismo')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (2,'Ciclismo')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (3,'Motociclismo')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (4,'Automobilismo')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (5,'Corrida de cavalos')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (9,'Pista de pouso')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (10,'Pista de táxi')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (11,'Heliporto')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipopista (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.revestimento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT revestimento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.revestimento (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (1,'Leito natural')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (2,'Revestimento primário')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (3,'Pavimentado')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (4,'Calçado')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.posicaopista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicaopista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicaopista (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.posicaopista (code,code_name) VALUES (12,'Adjacentes')#
INSERT INTO dominios.posicaopista (code,code_name) VALUES (13,'Superpostas')#
INSERT INTO dominios.posicaopista (code,code_name) VALUES (97,'Não Aplicável')#
INSERT INTO dominios.posicaopista (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.sistemageodesico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT sistemageodesico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (1,'SAD-69')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (2,'SIRGAS')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (3,'WGS-84')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (4,'Córrego Alegre')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (5,'Astro Chuá')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (6,'Outra referência')#
INSERT INTO dominios.sistemageodesico (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifrod (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifrod_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (8,'Terminal interestadual')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (9,'Terminal urbano')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (10,'Parada interestadual')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (12,'Posto de pesagem')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (13,'Posto de pedágio')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (14,'Posto de fiscalização')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (15,'Administrativa')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifrod (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.indice (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT indice_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.indice (code,code_name) VALUES (1,'Mestra')#
INSERT INTO dominios.indice (code,code_name) VALUES (2,'Normal')#
INSERT INTO dominios.indice (code,code_name) VALUES (3,'Auxiliar')#
INSERT INTO dominios.indice (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.denso (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT denso_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.denso (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.denso (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.denso (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.denso (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.coletiva (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT coletiva_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.coletiva (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.coletiva (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.coletiva (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.coletiva (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaojuridica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaojuridica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (1,'Delimitada')#
INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (2,'Declarada')#
INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (3,'Homologada ou demarcada')#
INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (4,'Regularizada')#
INSERT INTO dominios.situacaojuridica (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoestmed (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoestmed_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoestmed (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (1,'Estação Climatológica Principal - CP')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (2,'Estação Climatológica Auxiliar - CA')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (3,'Estação Agroclimatológica - AC')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (4,'Estação Pluviométrica - PL')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (5,'Estação Eólica - EO')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (6,'Estação Evaporimétrica - EV')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (7,'Estação Solarimétrica - SL')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (8,'Estação de Radar Meteorológico - RD')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (9,'Estação de Radiossonda - RS')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (10,'Estação Fluviométrica - FL')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (11,'Estação Maregráfica - MA')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (12,'Estação de Marés Terrestres - Crosta')#
INSERT INTO dominios.tipoestmed (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.antropizada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT antropizada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.antropizada (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.antropizada (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.antropizada (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.antropizada (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.caracteristicafloresta (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT caracteristicafloresta_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.caracteristicafloresta (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.caracteristicafloresta (code,code_name) VALUES (1,'Floresta')#
INSERT INTO dominios.caracteristicafloresta (code,code_name) VALUES (2,'Mata')#
INSERT INTO dominios.caracteristicafloresta (code,code_name) VALUES (3,'Bosque')#
INSERT INTO dominios.caracteristicafloresta (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaocosta (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaocosta_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaocosta (code,code_name) VALUES (10,'Contíguo')#
INSERT INTO dominios.situacaocosta (code,code_name) VALUES (11,'Afastado')#
INSERT INTO dominios.situacaocosta (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocampoquadra (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocampoquadra_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (1,'Futebol')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (2,'Basquete')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (3,'Vôlei')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (4,'Pólo')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (5,'Hipismo')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (6,'Poliesportiva')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (7,'Tênis')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipocampoquadra (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.homologacao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT homologacao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.homologacao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.homologacao (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.homologacao (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.homologacao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.cultivopredominante (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT cultivopredominante_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (1,'Milho')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (2,'Banana')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (3,'Laranja')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (4,'Trigo')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (6,'Algodão herbáceo')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (7,'Cana-de-Açúcar')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (8,'Fumo')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (9,'Soja')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (10,'Batata inglesa')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (11,'Mandioca')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (12,'Feijão')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (13,'Arroz')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (14,'Café')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (15,'Cacau')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (16,'Erva-mate')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (17,'Palmeira')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (18,'Açaí')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (19,'Seringueira')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (20,'Eucalipto')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (21,'Acácia')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (22,'Algaroba')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (23,'Pinus')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (24,'Pastagem cultivada')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (25,'Hortaliças')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (26,'Bracatinga')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (27,'Araucária')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (28,'Carnauba')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (29,'Pera')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (30,'Maçã')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (31,'Pêssego')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (32,'Juta')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (33,'Cebola')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (42,'Videira')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (96,'Não identificado')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.cultivopredominante (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotravessiaped (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotravessiaped_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotravessiaped (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.tipotravessiaped (code,code_name) VALUES (7,'Passagem subterrânea')#
INSERT INTO dominios.tipotravessiaped (code,code_name) VALUES (8,'Passarela')#
INSERT INTO dominios.tipotravessiaped (code,code_name) VALUES (9,'Pinguela')#
INSERT INTO dominios.tipotravessiaped (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifcomercserv (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifcomercserv_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (3,'Centro comercial')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (4,'Mercado')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (5,'Centro de convenções')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (6,'Feira')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (7,'Hotel/motel/pousada')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (8,'Restaurante')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifcomercserv (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.coincidecomdentrode_hid (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT coincidecomdentrode_hid_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (1,'Rio')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (2,'Canal')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (9,'Laguna')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (10,'Represa/açude')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (11,'Vala')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (12,'Queda d´água')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (13,'Corredeira')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (14,'Eclusa')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (15,'Terreno sujeito a inundação')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (16,'Foz marítima')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (19,'Barragem')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.coincidecomdentrode_hid (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.causa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT causa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.causa (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.causa (code,code_name) VALUES (1,'Canalização')#
INSERT INTO dominios.causa (code,code_name) VALUES (2,'Gruta ou Fenda')#
INSERT INTO dominios.causa (code,code_name) VALUES (3,'Absorção')#
INSERT INTO dominios.causa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.materializado (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT materializado_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.materializado (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.materializado (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.materializado (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.materializado (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.funcaoedifmetroferrov (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT funcaoedifmetroferrov_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (15,'Administrativa')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (16,'Estação ferroviária de passageiros')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (17,'Estação metroviária')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (18,'Terminal ferroviário de cargas')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (19,'Terminal ferroviário de passageiros e cargas')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (20,'Oficina de manutenção')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.funcaoedifmetroferrov (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiporesiduo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiporesiduo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (9,'Esgoto')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (12,'Lixo domiciliar e comercial')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (13,'Lixo tóxico')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (14,'Lixo séptico')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (15,'Chorume')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (16,'Vinhoto')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tiporesiduo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoentroncamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoentroncamento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (1,'Cruzamento rodoviário')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (2,'Círculo rodoviário')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (3,'Trevo rodoviário')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (4,'Rótula')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (5,'Entroncamento ferroviário')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoentroncamento (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoatracad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoatracad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoatracad (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (38,'Cais')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (39,'Cais flutuante')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (40,'Trapiche')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (41,'Molhe de atracação')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (42,'Pier')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (43,'Dolfim')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (44,'Desembarcadouro')#
INSERT INTO dominios.tipoatracad (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoplataforma (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoplataforma_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoplataforma (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoplataforma (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.tipoplataforma (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipoplataforma (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipoplataforma (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaofisica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaofisica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaofisica (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (1,'Abandonada')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (2,'Destruída')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (3,'Em Construção')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (4,'Planejada')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (5,'Construída')#
INSERT INTO dominios.situacaofisica (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifturist (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifturist_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (9,'Cruzeiro')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (10,'Estátua')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (11,'Mirante')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (12,'Monumento')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (13,'Panteão')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifturist (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoponte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoponte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoponte (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoponte (code,code_name) VALUES (1,'Móvel')#
INSERT INTO dominios.tipoponte (code,code_name) VALUES (2,'Pênsil')#
INSERT INTO dominios.tipoponte (code,code_name) VALUES (3,'Fixa')#
INSERT INTO dominios.tipoponte (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacaoagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacaoagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacaoagua (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacaoagua (code,code_name) VALUES (6,'Tratada')#
INSERT INTO dominios.situacaoagua (code,code_name) VALUES (7,'Não tratada')#
INSERT INTO dominios.situacaoagua (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipotrechomassa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipotrechomassa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (1,'Rio')#
INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (2,'Canal')#
INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (9,'Laguna')#
INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (10,'Represa/açude')#
INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipotrechomassa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoedifabast (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoedifabast_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (1,'Captação')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (2,'Tratamento')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoedifabast (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.dentrodepoligono (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT dentrodepoligono_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.dentrodepoligono (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.dentrodepoligono (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.dentrodepoligono (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.nascente (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nascente_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nascente (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.nascente (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.nascente (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.nascente (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoptoenergia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoptoenergia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (1,'Estação geradora de energia')#
INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (2,'Subestação de transmissão')#
INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (3,'Subestação de  distribuição')#
INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (4,'Ponto de ramificação')#
INSERT INTO dominios.tipoptoenergia (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.relacionado_hdr (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT relacionado_hdr_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (12,'Queda dágua')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (13,'Corredeira')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (14,'Eclusa')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (16,'Foz marítima')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (17,'Interrupção com a Moldura')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (19,'Barragem')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (21,'Confluência')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (22,'Complexo portuário')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (23,'Entre trechos hidroviários')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (24,'Atracadouro')#
INSERT INTO dominios.relacionado_hdr (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipogrutacaverna (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipogrutacaverna_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipogrutacaverna (code,code_name) VALUES (19,'Gruta')#
INSERT INTO dominios.tipogrutacaverna (code,code_name) VALUES (20,'Caverna')#
INSERT INTO dominios.tipogrutacaverna (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.setor (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT setor_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.setor (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.setor (code,code_name) VALUES (1,'Energético')#
INSERT INTO dominios.setor (code,code_name) VALUES (2,'Econômico')#
INSERT INTO dominios.setor (code,code_name) VALUES (3,'Abastecimento de água')#
INSERT INTO dominios.setor (code,code_name) VALUES (4,'Saneamento básico')#
INSERT INTO dominios.setor (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.instituicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT instituicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.instituicao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (4,'Marinha')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (5,'Exército')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (6,'Aeronáutica')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (7,'Polícia militar')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (8,'Corpo de bombeiros')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.instituicao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipolavoura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipolavoura_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipolavoura (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipolavoura (code,code_name) VALUES (1,'Perene')#
INSERT INTO dominios.tipolavoura (code,code_name) VALUES (2,'Semi-perene')#
INSERT INTO dominios.tipolavoura (code,code_name) VALUES (3,'Anual')#
INSERT INTO dominios.tipolavoura (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.fixa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT fixa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.fixa (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.fixa (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.fixa (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.operacional (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT operacional_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.operacional (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.operacional (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.operacional (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.operacional (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.geracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT geracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.geracao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.geracao (code,code_name) VALUES (1,'Eletricidade - GER 0')#
INSERT INTO dominios.geracao (code,code_name) VALUES (2,'CoGeração')#
INSERT INTO dominios.geracao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipocerr (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipocerr_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipocerr (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipocerr (code,code_name) VALUES (1,'Cerrado')#
INSERT INTO dominios.tipocerr (code,code_name) VALUES (2,'Cerradão')#
INSERT INTO dominios.tipocerr (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipounidprotinteg (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipounidprotinteg_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (1,'Estação Ecológica - ESEC')#
INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (2,'Parque - PAR')#
INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (3,'Monumento batural - MONA')#
INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (4,'Reserva Biológica - REBIO')#
INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (5,'Refúgio de Vida Silvestre - RVS')#
INSERT INTO dominios.tipounidprotinteg (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.usoprincipal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT usoprincipal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.usoprincipal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (1,'Irrigação')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (2,'Abastecimento')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (3,'Energia')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.usoprincipal (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.destinacaofundeadouro (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT destinacaofundeadouro_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (10,'Fundeadouro recomendado sem limite definido')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (11,'Fundeadouro com designação alfanumérica')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (12,'Áreas de fundeio com limite definido')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (13,'Áreas de fundeio proibido')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.destinacaofundeadouro (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.relacionado_fer_rod (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT relacionado_fer_rod_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (1,'Túnel')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (2,'Passagem elevada ou viaduto')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (3,'Ponte')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (4,'Travessia')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (5,'Edificação rodoviária')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (6,'Galeria ou bueiro')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (7,'Mudança de atributo')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (8,'Entroncamento')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (9,'Início ou fim de trecho')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (10,'Edificação Metro Ferroviária')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (11,'Localidade')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (12,'Patio')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (13,'Passagem de nível')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (17,'Interrupção com a Moldura')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (19,'Barragem')#
INSERT INTO dominios.relacionado_fer_rod (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipopocomina (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipopocomina_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipopocomina (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipopocomina (code,code_name) VALUES (2,'Horizontal')#
INSERT INTO dominios.tipopocomina (code,code_name) VALUES (3,'Vertical')#
INSERT INTO dominios.tipopocomina (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.tipopocomina (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.causaexposicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT causaexposicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.causaexposicao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.causaexposicao (code,code_name) VALUES (4,'Natural')#
INSERT INTO dominios.causaexposicao (code,code_name) VALUES (5,'Artificial')#
INSERT INTO dominios.causaexposicao (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoptorefgeodtopo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoptorefgeodtopo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (1,'Vértice de Triangulação - VT')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (2,'Referência de Nível - RN')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (3,'Estação Gravimétrica - EG')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (4,'Estação de Poligonal - EP')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (5,'Ponto Astronômico - PA')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (6,'Ponto barométrico - B')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (7,'Ponto Trigonométrico - RV')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (8,'Ponto de Satélite - SAT')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoptorefgeodtopo (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipoptocontrole (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipoptocontrole_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipoptocontrole (code,code_name) VALUES (9,'Ponto de Controle')#
INSERT INTO dominios.tipoptocontrole (code,code_name) VALUES (12,'Ponto Perspectivo')#
INSERT INTO dominios.tipoptocontrole (code,code_name) VALUES (13,'Ponto Fotogramétrico')#
INSERT INTO dominios.tipoptocontrole (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipoptocontrole (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tiporecife (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tiporecife_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tiporecife (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tiporecife (code,code_name) VALUES (1,'Arenito')#
INSERT INTO dominios.tiporecife (code,code_name) VALUES (2,'Rochoso')#
INSERT INTO dominios.tiporecife (code,code_name) VALUES (20,'Coral')#
INSERT INTO dominios.tiporecife (code,code_name) VALUES (999,'A SER PREENCHIDO')#

CREATE TABLE cb.adm_area_pub_civil_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_area_pub_civil_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_area_pub_civil_a_geom ON cb.adm_area_pub_civil_a USING gist (geom)#

ALTER TABLE cb.adm_area_pub_civil_a
	 ADD CONSTRAINT adm_area_pub_civil_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_area_pub_civil_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.adm_area_pub_militar_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_area_pub_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_area_pub_militar_a_geom ON cb.adm_area_pub_militar_a USING gist (geom)#

ALTER TABLE cb.adm_area_pub_militar_a
	 ADD CONSTRAINT adm_area_pub_militar_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_area_pub_militar_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.adm_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_descontinuidade_geometrica_a_geom ON cb.adm_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.adm_descontinuidade_geometrica_a
	 ADD CONSTRAINT adm_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.adm_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT adm_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_descontinuidade_geometrica_l_geom ON cb.adm_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.adm_descontinuidade_geometrica_l
	 ADD CONSTRAINT adm_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.adm_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT adm_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_descontinuidade_geometrica_p_geom ON cb.adm_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.adm_descontinuidade_geometrica_p
	 ADD CONSTRAINT adm_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.adm_edif_pub_civil_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcivil smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_edif_pub_civil_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_edif_pub_civil_a_geom ON cb.adm_edif_pub_civil_a USING gist (geom)#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_tipoedifcivil_fk FOREIGN KEY (tipoedifcivil)
	 REFERENCES dominios.tipoedifcivil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN tipoedifcivil SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_a
	 ADD CONSTRAINT adm_edif_pub_civil_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipousoedif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_a ALTER COLUMN tipousoedif SET DEFAULT 999#

CREATE TABLE cb.adm_edif_pub_civil_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcivil smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT adm_edif_pub_civil_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_edif_pub_civil_p_geom ON cb.adm_edif_pub_civil_p USING gist (geom)#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_tipoedifcivil_fk FOREIGN KEY (tipoedifcivil)
	 REFERENCES dominios.tipoedifcivil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN tipoedifcivil SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_civil_p
	 ADD CONSTRAINT adm_edif_pub_civil_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipousoedif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_civil_p ALTER COLUMN tipousoedif SET DEFAULT 999#

CREATE TABLE cb.adm_edif_pub_militar_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifmil smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_edif_pub_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_edif_pub_militar_a_geom ON cb.adm_edif_pub_militar_a USING gist (geom)#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_tipoedifmil_fk FOREIGN KEY (tipoedifmil)
	 REFERENCES dominios.tipoedifmil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN tipoedifmil SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_a
	 ADD CONSTRAINT adm_edif_pub_militar_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipousoedif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_a ALTER COLUMN tipousoedif SET DEFAULT 999#

CREATE TABLE cb.adm_edif_pub_militar_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifmil smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT adm_edif_pub_militar_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_edif_pub_militar_p_geom ON cb.adm_edif_pub_militar_p USING gist (geom)#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_tipoedifmil_fk FOREIGN KEY (tipoedifmil)
	 REFERENCES dominios.tipoedifmil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN tipoedifmil SET DEFAULT 999#

ALTER TABLE cb.adm_edif_pub_militar_p
	 ADD CONSTRAINT adm_edif_pub_militar_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipousoedif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_edif_pub_militar_p ALTER COLUMN tipousoedif SET DEFAULT 999#

CREATE TABLE cb.adm_posto_fiscal_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopostofisc smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_posto_fiscal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_posto_fiscal_a_geom ON cb.adm_posto_fiscal_a USING gist (geom)#

ALTER TABLE cb.adm_posto_fiscal_a
	 ADD CONSTRAINT adm_posto_fiscal_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_a
	 ADD CONSTRAINT adm_posto_fiscal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_a
	 ADD CONSTRAINT adm_posto_fiscal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_a
	 ADD CONSTRAINT adm_posto_fiscal_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_posto_fiscal_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_a
	 ADD CONSTRAINT adm_posto_fiscal_a_tipopostofisc_fk FOREIGN KEY (tipopostofisc)
	 REFERENCES dominios.tipopostofisc (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_a ALTER COLUMN tipopostofisc SET DEFAULT 999#

CREATE TABLE cb.adm_posto_fiscal_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopostofisc smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT adm_posto_fiscal_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_posto_fiscal_p_geom ON cb.adm_posto_fiscal_p USING gist (geom)#

ALTER TABLE cb.adm_posto_fiscal_p
	 ADD CONSTRAINT adm_posto_fiscal_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_p
	 ADD CONSTRAINT adm_posto_fiscal_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_p
	 ADD CONSTRAINT adm_posto_fiscal_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_p
	 ADD CONSTRAINT adm_posto_fiscal_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_posto_fiscal_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_posto_fiscal_p
	 ADD CONSTRAINT adm_posto_fiscal_p_tipopostofisc_fk FOREIGN KEY (tipopostofisc)
	 REFERENCES dominios.tipopostofisc (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_fiscal_p ALTER COLUMN tipopostofisc SET DEFAULT 999#

CREATE TABLE cb.adm_posto_pol_rod_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopostopol smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT adm_posto_pol_rod_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_posto_pol_rod_a_geom ON cb.adm_posto_pol_rod_a USING gist (geom)#

ALTER TABLE cb.adm_posto_pol_rod_a
	 ADD CONSTRAINT adm_posto_pol_rod_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_a
	 ADD CONSTRAINT adm_posto_pol_rod_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_a
	 ADD CONSTRAINT adm_posto_pol_rod_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_a
	 ADD CONSTRAINT adm_posto_pol_rod_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_posto_pol_rod_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_a
	 ADD CONSTRAINT adm_posto_pol_rod_a_tipopostopol_fk FOREIGN KEY (tipopostopol)
	 REFERENCES dominios.tipopostopol (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_a ALTER COLUMN tipopostopol SET DEFAULT 999#

CREATE TABLE cb.adm_posto_pol_rod_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopostopol smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT adm_posto_pol_rod_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX adm_posto_pol_rod_p_geom ON cb.adm_posto_pol_rod_p USING gist (geom)#

ALTER TABLE cb.adm_posto_pol_rod_p
	 ADD CONSTRAINT adm_posto_pol_rod_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_p
	 ADD CONSTRAINT adm_posto_pol_rod_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_p
	 ADD CONSTRAINT adm_posto_pol_rod_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_p
	 ADD CONSTRAINT adm_posto_pol_rod_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.adm_posto_pol_rod_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.adm_posto_pol_rod_p
	 ADD CONSTRAINT adm_posto_pol_rod_p_tipopostopol_fk FOREIGN KEY (tipopostopol)
	 REFERENCES dominios.tipopostopol (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.adm_posto_pol_rod_p ALTER COLUMN tipopostopol SET DEFAULT 999#

CREATE TABLE cb.asb_area_abast_agua_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_area_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_area_abast_agua_a_geom ON cb.asb_area_abast_agua_a USING gist (geom)#

ALTER TABLE cb.asb_area_abast_agua_a
	 ADD CONSTRAINT asb_area_abast_agua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_area_abast_agua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.asb_area_saneamento_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_area_saneamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_area_saneamento_a_geom ON cb.asb_area_saneamento_a USING gist (geom)#

ALTER TABLE cb.asb_area_saneamento_a
	 ADD CONSTRAINT asb_area_saneamento_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_area_saneamento_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.asb_cemiterio_a(
	 id serial NOT NULL,
	 denominacaoassociada smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipocemiterio smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_cemiterio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_cemiterio_a_geom ON cb.asb_cemiterio_a USING gist (geom)#

ALTER TABLE cb.asb_cemiterio_a
	 ADD CONSTRAINT asb_cemiterio_a_denominacaoassociada_fk FOREIGN KEY (denominacaoassociada)
	 REFERENCES dominios.denominacaoassociada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_a ALTER COLUMN denominacaoassociada SET DEFAULT 999#

ALTER TABLE cb.asb_cemiterio_a
	 ADD CONSTRAINT asb_cemiterio_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_cemiterio_a
	 ADD CONSTRAINT asb_cemiterio_a_tipocemiterio_fk FOREIGN KEY (tipocemiterio)
	 REFERENCES dominios.tipocemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_a ALTER COLUMN tipocemiterio SET DEFAULT 999#

CREATE TABLE cb.asb_cemiterio_p(
	 id serial NOT NULL,
	 denominacaoassociada smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipocemiterio smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_cemiterio_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_cemiterio_p_geom ON cb.asb_cemiterio_p USING gist (geom)#

ALTER TABLE cb.asb_cemiterio_p
	 ADD CONSTRAINT asb_cemiterio_p_denominacaoassociada_fk FOREIGN KEY (denominacaoassociada)
	 REFERENCES dominios.denominacaoassociada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_p ALTER COLUMN denominacaoassociada SET DEFAULT 999#

ALTER TABLE cb.asb_cemiterio_p
	 ADD CONSTRAINT asb_cemiterio_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_cemiterio_p
	 ADD CONSTRAINT asb_cemiterio_p_tipocemiterio_fk FOREIGN KEY (tipocemiterio)
	 REFERENCES dominios.tipocemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_cemiterio_p ALTER COLUMN tipocemiterio SET DEFAULT 999#

CREATE TABLE cb.asb_dep_abast_agua_a(
	 id serial NOT NULL,
	 construcao smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaoagua smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodepabast smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_dep_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_dep_abast_agua_a_geom ON cb.asb_dep_abast_agua_a USING gist (geom)#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_construcao_fk FOREIGN KEY (construcao)
	 REFERENCES dominios.construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_construcao_check 
	 CHECK (construcao = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN construcao SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_asb (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_situacaoagua_fk FOREIGN KEY (situacaoagua)
	 REFERENCES dominios.situacaoagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN situacaoagua SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_a
	 ADD CONSTRAINT asb_dep_abast_agua_a_tipodepabast_fk FOREIGN KEY (tipodepabast)
	 REFERENCES dominios.tipodepabast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_a ALTER COLUMN tipodepabast SET DEFAULT 999#

CREATE TABLE cb.asb_dep_abast_agua_p(
	 id serial NOT NULL,
	 construcao smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaoagua smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodepabast smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_dep_abast_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_dep_abast_agua_p_geom ON cb.asb_dep_abast_agua_p USING gist (geom)#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_construcao_fk FOREIGN KEY (construcao)
	 REFERENCES dominios.construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_construcao_check 
	 CHECK (construcao = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN construcao SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_asb (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_situacaoagua_fk FOREIGN KEY (situacaoagua)
	 REFERENCES dominios.situacaoagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN situacaoagua SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_dep_abast_agua_p
	 ADD CONSTRAINT asb_dep_abast_agua_p_tipodepabast_fk FOREIGN KEY (tipodepabast)
	 REFERENCES dominios.tipodepabast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_abast_agua_p ALTER COLUMN tipodepabast SET DEFAULT 999#

CREATE TABLE cb.asb_dep_saneamento_a(
	 id serial NOT NULL,
	 construcao smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 residuo smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodepsaneam smallint NOT NULL,
	 tiporesiduo smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_dep_saneamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_dep_saneamento_a_geom ON cb.asb_dep_saneamento_a USING gist (geom)#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_construcao_fk FOREIGN KEY (construcao)
	 REFERENCES dominios.construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN construcao SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_asb (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 8 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_residuo_fk FOREIGN KEY (residuo)
	 REFERENCES dominios.residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN residuo SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_tipodepsaneam_fk FOREIGN KEY (tipodepsaneam)
	 REFERENCES dominios.tipodepsaneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN tipodepsaneam SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_a
	 ADD CONSTRAINT asb_dep_saneamento_a_tiporesiduo_fk FOREIGN KEY (tiporesiduo)
	 REFERENCES dominios.tiporesiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_a ALTER COLUMN tiporesiduo SET DEFAULT 999#

CREATE TABLE cb.asb_dep_saneamento_p(
	 id serial NOT NULL,
	 construcao smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 residuo smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodepsaneam smallint NOT NULL,
	 tiporesiduo smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_dep_saneamento_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_dep_saneamento_p_geom ON cb.asb_dep_saneamento_p USING gist (geom)#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_construcao_fk FOREIGN KEY (construcao)
	 REFERENCES dominios.construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN construcao SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_asb (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 8 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_residuo_fk FOREIGN KEY (residuo)
	 REFERENCES dominios.residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN residuo SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_tipodepsaneam_fk FOREIGN KEY (tipodepsaneam)
	 REFERENCES dominios.tipodepsaneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN tipodepsaneam SET DEFAULT 999#

ALTER TABLE cb.asb_dep_saneamento_p
	 ADD CONSTRAINT asb_dep_saneamento_p_tiporesiduo_fk FOREIGN KEY (tiporesiduo)
	 REFERENCES dominios.tiporesiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_dep_saneamento_p ALTER COLUMN tiporesiduo SET DEFAULT 999#

CREATE TABLE cb.asb_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_descontinuidade_geometrica_a_geom ON cb.asb_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.asb_descontinuidade_geometrica_a
	 ADD CONSTRAINT asb_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.asb_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT asb_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_descontinuidade_geometrica_l_geom ON cb.asb_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.asb_descontinuidade_geometrica_l
	 ADD CONSTRAINT asb_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.asb_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_descontinuidade_geometrica_p_geom ON cb.asb_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.asb_descontinuidade_geometrica_p
	 ADD CONSTRAINT asb_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.asb_edif_abast_agua_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifabast smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_edif_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_edif_abast_agua_a_geom ON cb.asb_edif_abast_agua_a USING gist (geom)#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_edif_abast_agua_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_a
	 ADD CONSTRAINT asb_edif_abast_agua_a_tipoedifabast_fk FOREIGN KEY (tipoedifabast)
	 REFERENCES dominios.tipoedifabast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_a ALTER COLUMN tipoedifabast SET DEFAULT 999#

CREATE TABLE cb.asb_edif_abast_agua_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifabast smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_edif_abast_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_edif_abast_agua_p_geom ON cb.asb_edif_abast_agua_p USING gist (geom)#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_edif_abast_agua_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_edif_abast_agua_p
	 ADD CONSTRAINT asb_edif_abast_agua_p_tipoedifabast_fk FOREIGN KEY (tipoedifabast)
	 REFERENCES dominios.tipoedifabast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_abast_agua_p ALTER COLUMN tipoedifabast SET DEFAULT 999#

CREATE TABLE cb.asb_edif_saneamento_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifsaneam smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT asb_edif_saneamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_edif_saneamento_a_geom ON cb.asb_edif_saneamento_a USING gist (geom)#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_edif_saneamento_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_a
	 ADD CONSTRAINT asb_edif_saneamento_a_tipoedifsaneam_fk FOREIGN KEY (tipoedifsaneam)
	 REFERENCES dominios.tipoedifsaneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_a ALTER COLUMN tipoedifsaneam SET DEFAULT 999#

CREATE TABLE cb.asb_edif_saneamento_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifsaneam smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT asb_edif_saneamento_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX asb_edif_saneamento_p_geom ON cb.asb_edif_saneamento_p USING gist (geom)#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.asb_edif_saneamento_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.asb_edif_saneamento_p
	 ADD CONSTRAINT asb_edif_saneamento_p_tipoedifsaneam_fk FOREIGN KEY (tipoedifsaneam)
	 REFERENCES dominios.tipoedifsaneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.asb_edif_saneamento_p ALTER COLUMN tipoedifsaneam SET DEFAULT 999#

CREATE TABLE cb.eco_area_agrop_ext_veg_pesca_a(
	 id serial NOT NULL,
	 destinadoa smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_area_agrop_ext_veg_pesca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_area_agrop_ext_veg_pesca_a_geom ON cb.eco_area_agrop_ext_veg_pesca_a USING gist (geom)#

ALTER TABLE cb.eco_area_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_area_agrop_ext_veg_pesca_a_destinadoa_fk FOREIGN KEY (destinadoa)
	 REFERENCES dominios.destinadoa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_area_agrop_ext_veg_pesca_a ALTER COLUMN destinadoa SET DEFAULT 999#

ALTER TABLE cb.eco_area_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_area_agrop_ext_veg_pesca_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_area_agrop_ext_veg_pesca_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.eco_area_comerc_serv_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_area_comerc_serv_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_area_comerc_serv_a_geom ON cb.eco_area_comerc_serv_a USING gist (geom)#

ALTER TABLE cb.eco_area_comerc_serv_a
	 ADD CONSTRAINT eco_area_comerc_serv_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_area_comerc_serv_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.eco_area_ext_mineral_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_area_ext_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_area_ext_mineral_a_geom ON cb.eco_area_ext_mineral_a USING gist (geom)#

ALTER TABLE cb.eco_area_ext_mineral_a
	 ADD CONSTRAINT eco_area_ext_mineral_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_area_ext_mineral_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.eco_area_industrial_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_area_industrial_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_area_industrial_a_geom ON cb.eco_area_industrial_a USING gist (geom)#

ALTER TABLE cb.eco_area_industrial_a
	 ADD CONSTRAINT eco_area_industrial_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_area_industrial_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.eco_deposito_geral_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoconteudo smallint NOT NULL,
	 tipodepgeral smallint NOT NULL,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tratamento smallint NOT NULL,
	 unidadevolume smallint NOT NULL,
	 valorvolume real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_deposito_geral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_deposito_geral_a_geom ON cb.eco_deposito_geral_a USING gist (geom)#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipoconteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN tipoconteudo SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipodepgeral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN tipodepgeral SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipoexposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN tipoexposicao SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipoprodutoresiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 36 :: SMALLINT, 41 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN tipoprodutoresiduo SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.tratamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN tratamento SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_a
	 ADD CONSTRAINT eco_deposito_geral_a_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidadevolume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_a ALTER COLUMN unidadevolume SET DEFAULT 999#

CREATE TABLE cb.eco_deposito_geral_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoconteudo smallint NOT NULL,
	 tipodepgeral smallint NOT NULL,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tratamento smallint NOT NULL,
	 unidadevolume smallint NOT NULL,
	 valorvolume real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_deposito_geral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_deposito_geral_p_geom ON cb.eco_deposito_geral_p USING gist (geom)#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipoconteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN tipoconteudo SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipodepgeral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN tipodepgeral SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipoexposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN tipoexposicao SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipoprodutoresiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 36 :: SMALLINT, 41 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN tipoprodutoresiduo SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.tratamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN tratamento SET DEFAULT 999#

ALTER TABLE cb.eco_deposito_geral_p
	 ADD CONSTRAINT eco_deposito_geral_p_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidadevolume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_deposito_geral_p ALTER COLUMN unidadevolume SET DEFAULT 999#

CREATE TABLE cb.eco_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_descontinuidade_geometrica_a_geom ON cb.eco_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.eco_descontinuidade_geometrica_a
	 ADD CONSTRAINT eco_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.eco_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT eco_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_descontinuidade_geometrica_l_geom ON cb.eco_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.eco_descontinuidade_geometrica_l
	 ADD CONSTRAINT eco_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.eco_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_descontinuidade_geometrica_p_geom ON cb.eco_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.eco_descontinuidade_geometrica_p
	 ADD CONSTRAINT eco_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.eco_edif_agrop_ext_veg_pesca_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifagropec smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_agrop_ext_veg_pesca_a_geom ON cb.eco_edif_agrop_ext_veg_pesca_a USING gist (geom)#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_a_tipoedifagropec_fk FOREIGN KEY (tipoedifagropec)
	 REFERENCES dominios.tipoedifagropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_a ALTER COLUMN tipoedifagropec SET DEFAULT 999#

CREATE TABLE cb.eco_edif_agrop_ext_veg_pesca_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifagropec smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_agrop_ext_veg_pesca_p_geom ON cb.eco_edif_agrop_ext_veg_pesca_p USING gist (geom)#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p
	 ADD CONSTRAINT eco_edif_agrop_ext_veg_pesca_p_tipoedifagropec_fk FOREIGN KEY (tipoedifagropec)
	 REFERENCES dominios.tipoedifagropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_agrop_ext_veg_pesca_p ALTER COLUMN tipoedifagropec SET DEFAULT 999#

CREATE TABLE cb.eco_edif_comerc_serv_a(
	 id serial NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_edif_comerc_serv_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_comerc_serv_a_geom ON cb.eco_edif_comerc_serv_a USING gist (geom)#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_eco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_a
	 ADD CONSTRAINT eco_edif_comerc_serv_a_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipoedifcomercserv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_a ALTER COLUMN tipoedifcomercserv SET DEFAULT 999#

CREATE TABLE cb.eco_edif_comerc_serv_p(
	 id serial NOT NULL,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_edif_comerc_serv_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_comerc_serv_p_geom ON cb.eco_edif_comerc_serv_p USING gist (geom)#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_eco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_comerc_serv_p
	 ADD CONSTRAINT eco_edif_comerc_serv_p_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipoedifcomercserv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_comerc_serv_p ALTER COLUMN tipoedifcomercserv SET DEFAULT 999#

CREATE TABLE cb.eco_edif_ext_mineral_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodivisaocnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_edif_ext_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_ext_mineral_a_geom ON cb.eco_edif_ext_mineral_a USING gist (geom)#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_tipodivisaocnae_fk FOREIGN KEY (tipodivisaocnae)
	 REFERENCES dominios.tipodivisaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_a
	 ADD CONSTRAINT eco_edif_ext_mineral_a_tipodivisaocnae_check 
	 CHECK (tipodivisaocnae = ANY(ARRAY[0 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_a ALTER COLUMN tipodivisaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_edif_ext_mineral_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodivisaocnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_edif_ext_mineral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_ext_mineral_p_geom ON cb.eco_edif_ext_mineral_p USING gist (geom)#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_tipodivisaocnae_fk FOREIGN KEY (tipodivisaocnae)
	 REFERENCES dominios.tipodivisaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_ext_mineral_p
	 ADD CONSTRAINT eco_edif_ext_mineral_p_tipodivisaocnae_check 
	 CHECK (tipodivisaocnae = ANY(ARRAY[0 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_ext_mineral_p ALTER COLUMN tipodivisaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_edif_industrial_a(
	 id serial NOT NULL,
	 chamine smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodivisaocnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_edif_industrial_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_industrial_a_geom ON cb.eco_edif_industrial_a USING gist (geom)#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_chamine_fk FOREIGN KEY (chamine)
	 REFERENCES dominios.chamine (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN chamine SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_tipodivisaocnae_fk FOREIGN KEY (tipodivisaocnae)
	 REFERENCES dominios.tipodivisaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_a
	 ADD CONSTRAINT eco_edif_industrial_a_tipodivisaocnae_check 
	 CHECK (tipodivisaocnae = ANY(ARRAY[0 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 36 :: SMALLINT, 37 :: SMALLINT, 45 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_a ALTER COLUMN tipodivisaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_edif_industrial_p(
	 id serial NOT NULL,
	 chamine smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipodivisaocnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_edif_industrial_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_edif_industrial_p_geom ON cb.eco_edif_industrial_p USING gist (geom)#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_chamine_fk FOREIGN KEY (chamine)
	 REFERENCES dominios.chamine (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN chamine SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_tipodivisaocnae_fk FOREIGN KEY (tipodivisaocnae)
	 REFERENCES dominios.tipodivisaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_edif_industrial_p
	 ADD CONSTRAINT eco_edif_industrial_p_tipodivisaocnae_check 
	 CHECK (tipodivisaocnae = ANY(ARRAY[0 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 36 :: SMALLINT, 37 :: SMALLINT, 45 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_edif_industrial_p ALTER COLUMN tipodivisaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_equip_agropec_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoequipagropec smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_equip_agropec_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_a_geom ON cb.eco_equip_agropec_a USING gist (geom)#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipoequipagropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_a ALTER COLUMN tipoequipagropec SET DEFAULT 999#

CREATE TABLE cb.eco_equip_agropec_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoequipagropec smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT eco_equip_agropec_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_l_geom ON cb.eco_equip_agropec_l USING gist (geom)#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipoequipagropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_l ALTER COLUMN tipoequipagropec SET DEFAULT 999#

CREATE TABLE cb.eco_equip_agropec_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoequipagropec smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_equip_agropec_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_p_geom ON cb.eco_equip_agropec_p USING gist (geom)#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_equip_agropec_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipoequipagropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_equip_agropec_p ALTER COLUMN tipoequipagropec SET DEFAULT 999#

CREATE TABLE cb.eco_ext_mineral_a(
	 id serial NOT NULL,
	 atividade smallint NOT NULL,
	 formaextracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 procextracao smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoextmin smallint NOT NULL,
	 tipopocomina smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tiposecaocnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_ext_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_ext_mineral_a_geom ON cb.eco_ext_mineral_a USING gist (geom)#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_atividade_fk FOREIGN KEY (atividade)
	 REFERENCES dominios.atividade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN atividade SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_formaextracao_fk FOREIGN KEY (formaextracao)
	 REFERENCES dominios.formaextracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN formaextracao SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_procextracao_fk FOREIGN KEY (procextracao)
	 REFERENCES dominios.procextracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN procextracao SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoextmin_fk FOREIGN KEY (tipoextmin)
	 REFERENCES dominios.tipoextmin (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN tipoextmin SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipopocomina_fk FOREIGN KEY (tipopocomina)
	 REFERENCES dominios.tipopocomina (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN tipopocomina SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipoprodutoresiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 18 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 37 :: SMALLINT, 38 :: SMALLINT, 39 :: SMALLINT, 40 :: SMALLINT, 42 :: SMALLINT, 43 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN tipoprodutoresiduo SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tiposecaocnae_fk FOREIGN KEY (tiposecaocnae)
	 REFERENCES dominios.tiposecaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tiposecaocnae_check 
	 CHECK (tiposecaocnae = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_a ALTER COLUMN tiposecaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_ext_mineral_p(
	 id serial NOT NULL,
	 atividade smallint NOT NULL,
	 formaextracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 procextracao smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoextmin smallint NOT NULL,
	 tipopocomina smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tiposecaocnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_ext_mineral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_ext_mineral_p_geom ON cb.eco_ext_mineral_p USING gist (geom)#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_atividade_fk FOREIGN KEY (atividade)
	 REFERENCES dominios.atividade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN atividade SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_formaextracao_fk FOREIGN KEY (formaextracao)
	 REFERENCES dominios.formaextracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN formaextracao SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_procextracao_fk FOREIGN KEY (procextracao)
	 REFERENCES dominios.procextracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN procextracao SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoextmin_fk FOREIGN KEY (tipoextmin)
	 REFERENCES dominios.tipoextmin (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN tipoextmin SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipopocomina_fk FOREIGN KEY (tipopocomina)
	 REFERENCES dominios.tipopocomina (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN tipopocomina SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipoprodutoresiduo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 18 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 37 :: SMALLINT, 38 :: SMALLINT, 39 :: SMALLINT, 40 :: SMALLINT, 42 :: SMALLINT, 43 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN tipoprodutoresiduo SET DEFAULT 999#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tiposecaocnae_fk FOREIGN KEY (tiposecaocnae)
	 REFERENCES dominios.tiposecaocnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tiposecaocnae_check 
	 CHECK (tiposecaocnae = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.eco_ext_mineral_p ALTER COLUMN tiposecaocnae SET DEFAULT 999#

CREATE TABLE cb.eco_plataforma_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoplataforma smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_plataforma_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_plataforma_a_geom ON cb.eco_plataforma_a USING gist (geom)#

ALTER TABLE cb.eco_plataforma_a
	 ADD CONSTRAINT eco_plataforma_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_plataforma_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_plataforma_a
	 ADD CONSTRAINT eco_plataforma_a_tipoplataforma_fk FOREIGN KEY (tipoplataforma)
	 REFERENCES dominios.tipoplataforma (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_plataforma_a ALTER COLUMN tipoplataforma SET DEFAULT 999#

CREATE TABLE cb.eco_plataforma_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoplataforma smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_plataforma_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_plataforma_p_geom ON cb.eco_plataforma_p USING gist (geom)#

ALTER TABLE cb.eco_plataforma_p
	 ADD CONSTRAINT eco_plataforma_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_plataforma_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.eco_plataforma_p
	 ADD CONSTRAINT eco_plataforma_p_tipoplataforma_fk FOREIGN KEY (tipoplataforma)
	 REFERENCES dominios.tipoplataforma (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.eco_plataforma_p ALTER COLUMN tipoplataforma SET DEFAULT 999#

CREATE TABLE cb.edu_area_ensino_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_area_ensino_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_area_ensino_a_geom ON cb.edu_area_ensino_a USING gist (geom)#

ALTER TABLE cb.edu_area_ensino_a
	 ADD CONSTRAINT edu_area_ensino_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_area_ensino_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.edu_area_lazer_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_area_lazer_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_area_lazer_a_geom ON cb.edu_area_lazer_a USING gist (geom)#

ALTER TABLE cb.edu_area_lazer_a
	 ADD CONSTRAINT edu_area_lazer_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_area_lazer_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.edu_area_religiosa_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_area_religiosa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_area_religiosa_a_geom ON cb.edu_area_religiosa_a USING gist (geom)#

ALTER TABLE cb.edu_area_religiosa_a
	 ADD CONSTRAINT edu_area_religiosa_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_area_religiosa_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.edu_area_ruinas_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_area_ruinas_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_area_ruinas_a_geom ON cb.edu_area_ruinas_a USING gist (geom)#

ALTER TABLE cb.edu_area_ruinas_a
	 ADD CONSTRAINT edu_area_ruinas_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_area_ruinas_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.edu_arquibancada_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_arquibancada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_arquibancada_a_geom ON cb.edu_arquibancada_a USING gist (geom)#

ALTER TABLE cb.edu_arquibancada_a
	 ADD CONSTRAINT edu_arquibancada_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_arquibancada_a
	 ADD CONSTRAINT edu_arquibancada_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_arquibancada_a
	 ADD CONSTRAINT edu_arquibancada_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_a
	 ADD CONSTRAINT edu_arquibancada_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_arquibancada_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.edu_arquibancada_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_arquibancada_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_arquibancada_p_geom ON cb.edu_arquibancada_p USING gist (geom)#

ALTER TABLE cb.edu_arquibancada_p
	 ADD CONSTRAINT edu_arquibancada_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_arquibancada_p
	 ADD CONSTRAINT edu_arquibancada_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_arquibancada_p
	 ADD CONSTRAINT edu_arquibancada_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_arquibancada_p
	 ADD CONSTRAINT edu_arquibancada_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_arquibancada_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.edu_campo_quadra_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocampoquadra smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_campo_quadra_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_campo_quadra_a_geom ON cb.edu_campo_quadra_a USING gist (geom)#

ALTER TABLE cb.edu_campo_quadra_a
	 ADD CONSTRAINT edu_campo_quadra_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_a
	 ADD CONSTRAINT edu_campo_quadra_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_a
	 ADD CONSTRAINT edu_campo_quadra_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_a
	 ADD CONSTRAINT edu_campo_quadra_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_campo_quadra_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_a
	 ADD CONSTRAINT edu_campo_quadra_a_tipocampoquadra_fk FOREIGN KEY (tipocampoquadra)
	 REFERENCES dominios.tipocampoquadra (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_a ALTER COLUMN tipocampoquadra SET DEFAULT 999#

CREATE TABLE cb.edu_campo_quadra_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocampoquadra smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_campo_quadra_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_campo_quadra_p_geom ON cb.edu_campo_quadra_p USING gist (geom)#

ALTER TABLE cb.edu_campo_quadra_p
	 ADD CONSTRAINT edu_campo_quadra_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_p
	 ADD CONSTRAINT edu_campo_quadra_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_p
	 ADD CONSTRAINT edu_campo_quadra_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_p
	 ADD CONSTRAINT edu_campo_quadra_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_campo_quadra_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_campo_quadra_p
	 ADD CONSTRAINT edu_campo_quadra_p_tipocampoquadra_fk FOREIGN KEY (tipocampoquadra)
	 REFERENCES dominios.tipocampoquadra (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_campo_quadra_p ALTER COLUMN tipocampoquadra SET DEFAULT 999#

CREATE TABLE cb.edu_coreto_tribuna_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_coreto_tribuna_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_coreto_tribuna_a_geom ON cb.edu_coreto_tribuna_a USING gist (geom)#

ALTER TABLE cb.edu_coreto_tribuna_a
	 ADD CONSTRAINT edu_coreto_tribuna_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_coreto_tribuna_a
	 ADD CONSTRAINT edu_coreto_tribuna_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_coreto_tribuna_a
	 ADD CONSTRAINT edu_coreto_tribuna_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_a
	 ADD CONSTRAINT edu_coreto_tribuna_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_coreto_tribuna_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.edu_coreto_tribuna_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_coreto_tribuna_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_coreto_tribuna_p_geom ON cb.edu_coreto_tribuna_p USING gist (geom)#

ALTER TABLE cb.edu_coreto_tribuna_p
	 ADD CONSTRAINT edu_coreto_tribuna_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_coreto_tribuna_p
	 ADD CONSTRAINT edu_coreto_tribuna_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_coreto_tribuna_p
	 ADD CONSTRAINT edu_coreto_tribuna_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_coreto_tribuna_p
	 ADD CONSTRAINT edu_coreto_tribuna_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_coreto_tribuna_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.edu_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_descontinuidade_geometrica_a_geom ON cb.edu_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.edu_descontinuidade_geometrica_a
	 ADD CONSTRAINT edu_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.edu_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edu_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_descontinuidade_geometrica_l_geom ON cb.edu_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.edu_descontinuidade_geometrica_l
	 ADD CONSTRAINT edu_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.edu_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_descontinuidade_geometrica_p_geom ON cb.edu_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.edu_descontinuidade_geometrica_p
	 ADD CONSTRAINT edu_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.edu_edif_const_lazer_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoediflazer smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_edif_const_lazer_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_const_lazer_a_geom ON cb.edu_edif_const_lazer_a USING gist (geom)#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_lazer_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_lazer_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_a
	 ADD CONSTRAINT edu_edif_const_lazer_a_tipoediflazer_fk FOREIGN KEY (tipoediflazer)
	 REFERENCES dominios.tipoediflazer (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_a ALTER COLUMN tipoediflazer SET DEFAULT 999#

CREATE TABLE cb.edu_edif_const_lazer_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoediflazer smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_edif_const_lazer_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_const_lazer_p_geom ON cb.edu_edif_const_lazer_p USING gist (geom)#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_lazer_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_lazer_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_lazer_p
	 ADD CONSTRAINT edu_edif_const_lazer_p_tipoediflazer_fk FOREIGN KEY (tipoediflazer)
	 REFERENCES dominios.tipoediflazer (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_lazer_p ALTER COLUMN tipoediflazer SET DEFAULT 999#

CREATE TABLE cb.edu_edif_const_turistica_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifturist smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_edif_const_turistica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_const_turistica_a_geom ON cb.edu_edif_const_turistica_a USING gist (geom)#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.ovgd (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN ovgd SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_a
	 ADD CONSTRAINT edu_edif_const_turistica_a_tipoedifturist_fk FOREIGN KEY (tipoedifturist)
	 REFERENCES dominios.tipoedifturist (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_a ALTER COLUMN tipoedifturist SET DEFAULT 999#

CREATE TABLE cb.edu_edif_const_turistica_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifturist smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_edif_const_turistica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_const_turistica_p_geom ON cb.edu_edif_const_turistica_p USING gist (geom)#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.ovgd (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN ovgd SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_const_turistica_p
	 ADD CONSTRAINT edu_edif_const_turistica_p_tipoedifturist_fk FOREIGN KEY (tipoedifturist)
	 REFERENCES dominios.tipoedifturist (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_const_turistica_p ALTER COLUMN tipoedifturist SET DEFAULT 999#

CREATE TABLE cb.edu_edif_ensino_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_edif_ensino_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_ensino_a_geom ON cb.edu_edif_ensino_a USING gist (geom)#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_a
	 ADD CONSTRAINT edu_edif_ensino_a_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_a ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.edu_edif_ensino_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_edif_ensino_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_ensino_p_geom ON cb.edu_edif_ensino_p USING gist (geom)#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_ensino_p
	 ADD CONSTRAINT edu_edif_ensino_p_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 23 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_ensino_p ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.edu_edif_religiosa_a(
	 id serial NOT NULL,
	 ensino smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 religiao varchar(255),
	 situacaofisica smallint NOT NULL,
	 tipoedifrelig smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_edif_religiosa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_religiosa_a_geom ON cb.edu_edif_religiosa_a USING gist (geom)#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_ensino_fk FOREIGN KEY (ensino)
	 REFERENCES dominios.ensino (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN ensino SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_a
	 ADD CONSTRAINT edu_edif_religiosa_a_tipoedifrelig_fk FOREIGN KEY (tipoedifrelig)
	 REFERENCES dominios.tipoedifrelig (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_a ALTER COLUMN tipoedifrelig SET DEFAULT 999#

CREATE TABLE cb.edu_edif_religiosa_p(
	 id serial NOT NULL,
	 ensino smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 religiao varchar(255),
	 situacaofisica smallint NOT NULL,
	 tipoedifrelig smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_edif_religiosa_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_edif_religiosa_p_geom ON cb.edu_edif_religiosa_p USING gist (geom)#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_ensino_fk FOREIGN KEY (ensino)
	 REFERENCES dominios.ensino (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN ensino SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_edif_religiosa_p
	 ADD CONSTRAINT edu_edif_religiosa_p_tipoedifrelig_fk FOREIGN KEY (tipoedifrelig)
	 REFERENCES dominios.tipoedifrelig (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_edif_religiosa_p ALTER COLUMN tipoedifrelig SET DEFAULT 999#

CREATE TABLE cb.edu_piscina_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_piscina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_piscina_a_geom ON cb.edu_piscina_a USING gist (geom)#

ALTER TABLE cb.edu_piscina_a
	 ADD CONSTRAINT edu_piscina_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_piscina_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_piscina_a
	 ADD CONSTRAINT edu_piscina_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_piscina_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_piscina_a
	 ADD CONSTRAINT edu_piscina_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_piscina_a
	 ADD CONSTRAINT edu_piscina_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_piscina_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.edu_pista_competicao_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopista smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edu_pista_competicao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_pista_competicao_l_geom ON cb.edu_pista_competicao_l USING gist (geom)#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_pista_competicao_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_pista_competicao_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_pista_competicao_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_pista_competicao_l
	 ADD CONSTRAINT edu_pista_competicao_l_tipopista_check 
	 CHECK (tipopista = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.edu_pista_competicao_l ALTER COLUMN tipopista SET DEFAULT 999#

CREATE TABLE cb.edu_ruina_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edu_ruina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_ruina_a_geom ON cb.edu_ruina_a USING gist (geom)#

ALTER TABLE cb.edu_ruina_a
	 ADD CONSTRAINT edu_ruina_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_ruina_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.edu_ruina_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edu_ruina_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edu_ruina_p_geom ON cb.edu_ruina_p USING gist (geom)#

ALTER TABLE cb.edu_ruina_p
	 ADD CONSTRAINT edu_ruina_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.edu_ruina_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.enc_antena_comunic_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 posicaoreledific smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_antena_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_antena_comunic_p_geom ON cb.enc_antena_comunic_p USING gist (geom)#

ALTER TABLE cb.enc_antena_comunic_p
	 ADD CONSTRAINT enc_antena_comunic_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_antena_comunic_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_antena_comunic_p
	 ADD CONSTRAINT enc_antena_comunic_p_posicaoreledific_fk FOREIGN KEY (posicaoreledific)
	 REFERENCES dominios.posicaoreledific (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_antena_comunic_p ALTER COLUMN posicaoreledific SET DEFAULT 999#

CREATE TABLE cb.enc_area_comunicacao_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_area_comunicacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_area_comunicacao_a_geom ON cb.enc_area_comunicacao_a USING gist (geom)#

ALTER TABLE cb.enc_area_comunicacao_a
	 ADD CONSTRAINT enc_area_comunicacao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_area_comunicacao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.enc_area_energia_eletrica_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_area_energia_eletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_area_energia_eletrica_a_geom ON cb.enc_area_energia_eletrica_a USING gist (geom)#

ALTER TABLE cb.enc_area_energia_eletrica_a
	 ADD CONSTRAINT enc_area_energia_eletrica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_area_energia_eletrica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.enc_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_descontinuidade_geometrica_a_geom ON cb.enc_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.enc_descontinuidade_geometrica_a
	 ADD CONSTRAINT enc_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.enc_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_descontinuidade_geometrica_l_geom ON cb.enc_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.enc_descontinuidade_geometrica_l
	 ADD CONSTRAINT enc_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.enc_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_descontinuidade_geometrica_p_geom ON cb.enc_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.enc_descontinuidade_geometrica_p
	 ADD CONSTRAINT enc_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.enc_edif_comunic_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 modalidade smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcomunic smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_edif_comunic_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_edif_comunic_a_geom ON cb.enc_edif_comunic_a USING gist (geom)#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_modalidade_fk FOREIGN KEY (modalidade)
	 REFERENCES dominios.modalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN modalidade SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_a
	 ADD CONSTRAINT enc_edif_comunic_a_tipoedifcomunic_fk FOREIGN KEY (tipoedifcomunic)
	 REFERENCES dominios.tipoedifcomunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_a ALTER COLUMN tipoedifcomunic SET DEFAULT 999#

CREATE TABLE cb.enc_edif_comunic_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 modalidade smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifcomunic smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_edif_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_edif_comunic_p_geom ON cb.enc_edif_comunic_p USING gist (geom)#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_modalidade_fk FOREIGN KEY (modalidade)
	 REFERENCES dominios.modalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN modalidade SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_edif_comunic_p
	 ADD CONSTRAINT enc_edif_comunic_p_tipoedifcomunic_fk FOREIGN KEY (tipoedifcomunic)
	 REFERENCES dominios.tipoedifcomunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_comunic_p ALTER COLUMN tipoedifcomunic SET DEFAULT 999#

CREATE TABLE cb.enc_edif_energia_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifenergia smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_edif_energia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_edif_energia_a_geom ON cb.enc_edif_energia_a USING gist (geom)#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_energia_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_energia_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_a
	 ADD CONSTRAINT enc_edif_energia_a_tipoedifenergia_fk FOREIGN KEY (tipoedifenergia)
	 REFERENCES dominios.tipoedifenergia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_a ALTER COLUMN tipoedifenergia SET DEFAULT 999#

CREATE TABLE cb.enc_edif_energia_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifenergia smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_edif_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_edif_energia_p_geom ON cb.enc_edif_energia_p USING gist (geom)#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_energia_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_edif_energia_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_edif_energia_p
	 ADD CONSTRAINT enc_edif_energia_p_tipoedifenergia_fk FOREIGN KEY (tipoedifenergia)
	 REFERENCES dominios.tipoedifenergia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_edif_energia_p ALTER COLUMN tipoedifenergia SET DEFAULT 999#

CREATE TABLE cb.enc_est_gerad_energia_eletr_a(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 tipoestgerad smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_est_gerad_energia_eletr_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_est_gerad_energia_eletr_a_geom ON cb.enc_est_gerad_energia_eletr_a USING gist (geom)#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_est_gerad_energia_eletr_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_a_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipoestgerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_a ALTER COLUMN tipoestgerad SET DEFAULT 999#

CREATE TABLE cb.enc_est_gerad_energia_eletr_l(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 tipoestgerad smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_est_gerad_energia_eletr_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_est_gerad_energia_eletr_l_geom ON cb.enc_est_gerad_energia_eletr_l USING gist (geom)#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_est_gerad_energia_eletr_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_l_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipoestgerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_l ALTER COLUMN tipoestgerad SET DEFAULT 999#

CREATE TABLE cb.enc_est_gerad_energia_eletr_p(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 tipoestgerad smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_est_gerad_energia_eletr_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_est_gerad_energia_eletr_p_geom ON cb.enc_est_gerad_energia_eletr_p USING gist (geom)#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_est_gerad_energia_eletr_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletr_p_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipoestgerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_est_gerad_energia_eletr_p ALTER COLUMN tipoestgerad SET DEFAULT 999#

CREATE TABLE cb.enc_grupo_transformadores_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_grupo_transformadores_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_grupo_transformadores_a_geom ON cb.enc_grupo_transformadores_a USING gist (geom)#

ALTER TABLE cb.enc_grupo_transformadores_a
	 ADD CONSTRAINT enc_grupo_transformadores_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_grupo_transformadores_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.enc_grupo_transformadores_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_grupo_transformadores_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_grupo_transformadores_p_geom ON cb.enc_grupo_transformadores_p USING gist (geom)#

ALTER TABLE cb.enc_grupo_transformadores_p
	 ADD CONSTRAINT enc_grupo_transformadores_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_grupo_transformadores_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.enc_hidreletrica_a(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 codigohidreletrica varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_hidreletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_a_geom ON cb.enc_hidreletrica_a USING gist (geom)#

ALTER TABLE cb.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_a ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_hidreletrica_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.enc_hidreletrica_l(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 codigohidreletrica varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_hidreletrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_l_geom ON cb.enc_hidreletrica_l USING gist (geom)#

ALTER TABLE cb.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_l ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_hidreletrica_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.enc_hidreletrica_p(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 codigohidreletrica varchar(255),
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_hidreletrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_p_geom ON cb.enc_hidreletrica_p USING gist (geom)#

ALTER TABLE cb.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_p ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_hidreletrica_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.enc_ponto_trecho_energia_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 tipoptoenergia smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_ponto_trecho_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_ponto_trecho_energia_p_geom ON cb.enc_ponto_trecho_energia_p USING gist (geom)#

ALTER TABLE cb.enc_ponto_trecho_energia_p
	 ADD CONSTRAINT enc_ponto_trecho_energia_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_ponto_trecho_energia_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_ponto_trecho_energia_p
	 ADD CONSTRAINT enc_ponto_trecho_energia_p_tipoptoenergia_fk FOREIGN KEY (tipoptoenergia)
	 REFERENCES dominios.tipoptoenergia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_ponto_trecho_energia_p ALTER COLUMN tipoptoenergia SET DEFAULT 999#

CREATE TABLE cb.enc_termeletrica_a(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 combrenovavel smallint NOT NULL,
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geracao smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 tipocombustivel smallint NOT NULL,
	 tipomaqtermica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_termeletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_termeletrica_a_geom ON cb.enc_termeletrica_a USING gist (geom)#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_combrenovavel_fk FOREIGN KEY (combrenovavel)
	 REFERENCES dominios.combrenovavel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN combrenovavel SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_geracao_fk FOREIGN KEY (geracao)
	 REFERENCES dominios.geracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN geracao SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_tipocombustivel_fk FOREIGN KEY (tipocombustivel)
	 REFERENCES dominios.tipocombustivel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN tipocombustivel SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_tipomaqtermica_fk FOREIGN KEY (tipomaqtermica)
	 REFERENCES dominios.tipomaqtermica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_a ALTER COLUMN tipomaqtermica SET DEFAULT 999#

CREATE TABLE cb.enc_termeletrica_p(
	 id serial NOT NULL,
	 codigoestacao varchar(255),
	 combrenovavel smallint NOT NULL,
	 destenergelet smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geracao smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 potenciafiscalizada real,
	 potenciaoutorgada real,
	 situacaofisica smallint NOT NULL,
	 tipocombustivel smallint NOT NULL,
	 tipomaqtermica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_termeletrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_termeletrica_p_geom ON cb.enc_termeletrica_p USING gist (geom)#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_combrenovavel_fk FOREIGN KEY (combrenovavel)
	 REFERENCES dominios.combrenovavel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN combrenovavel SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_destenergelet_fk FOREIGN KEY (destenergelet)
	 REFERENCES dominios.destenergelet (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN destenergelet SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_geracao_fk FOREIGN KEY (geracao)
	 REFERENCES dominios.geracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN geracao SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_tipocombustivel_fk FOREIGN KEY (tipocombustivel)
	 REFERENCES dominios.tipocombustivel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN tipocombustivel SET DEFAULT 999#

ALTER TABLE cb.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_tipomaqtermica_fk FOREIGN KEY (tipomaqtermica)
	 REFERENCES dominios.tipomaqtermica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_termeletrica_p ALTER COLUMN tipomaqtermica SET DEFAULT 999#

CREATE TABLE cb.enc_torre_comunic_p(
	 id serial NOT NULL,
	 alturaestimada real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 posicaoreledific smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_torre_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_torre_comunic_p_geom ON cb.enc_torre_comunic_p USING gist (geom)#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_comunic_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_comunic_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.ovgd (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_comunic_p ALTER COLUMN ovgd SET DEFAULT 999#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_posicaoreledific_fk FOREIGN KEY (posicaoreledific)
	 REFERENCES dominios.posicaoreledific (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_comunic_p ALTER COLUMN posicaoreledific SET DEFAULT 999#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_torre_comunic_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.enc_torre_energia_p(
	 id serial NOT NULL,
	 alturaestimada real,
	 arranjofases varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotorre smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_torre_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_torre_energia_p_geom ON cb.enc_torre_energia_p USING gist (geom)#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_energia_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_energia_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.ovgd (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_energia_p ALTER COLUMN ovgd SET DEFAULT 999#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_torre_energia_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_tipotorre_fk FOREIGN KEY (tipotorre)
	 REFERENCES dominios.tipotorre (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_torre_energia_p ALTER COLUMN tipotorre SET DEFAULT 999#

CREATE TABLE cb.enc_trecho_comunic_l(
	 id serial NOT NULL,
	 emduto smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotrechocomunic smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_trecho_comunic_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_trecho_comunic_l_geom ON cb.enc_trecho_comunic_l USING gist (geom)#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_emduto_fk FOREIGN KEY (emduto)
	 REFERENCES dominios.emduto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN emduto SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicaorelativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_posicaorelativa_check 
	 CHECK (posicaorelativa = ANY(ARRAY[2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN posicaorelativa SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_tipotrechocomunic_fk FOREIGN KEY (tipotrechocomunic)
	 REFERENCES dominios.tipotrechocomunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_comunic_l ALTER COLUMN tipotrechocomunic SET DEFAULT 999#

CREATE TABLE cb.enc_trecho_energia_l(
	 id serial NOT NULL,
	 emduto smallint NOT NULL,
	 especie smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 numcircuitos integer,
	 operacional smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tensaoeletrica real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_trecho_energia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_trecho_energia_l_geom ON cb.enc_trecho_energia_l USING gist (geom)#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_emduto_fk FOREIGN KEY (emduto)
	 REFERENCES dominios.emduto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN emduto SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_especie_fk FOREIGN KEY (especie)
	 REFERENCES dominios.especie (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN especie SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicaorelativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_posicaorelativa_check 
	 CHECK (posicaorelativa = ANY(ARRAY[2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN posicaorelativa SET DEFAULT 999#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.enc_trecho_energia_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.enc_zona_linhas_energia_com_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_zona_linhas_energia_com_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_zona_linhas_energia_com_a_geom ON cb.enc_zona_linhas_energia_com_a USING gist (geom)#

ALTER TABLE cb.enc_zona_linhas_energia_com_a
	 ADD CONSTRAINT enc_zona_linhas_energia_com_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.enc_zona_linhas_energia_com_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_area_umida_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoareaumida smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_area_umida_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_area_umida_a_geom ON cb.hid_area_umida_a USING gist (geom)#

ALTER TABLE cb.hid_area_umida_a
	 ADD CONSTRAINT hid_area_umida_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_area_umida_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_area_umida_a
	 ADD CONSTRAINT hid_area_umida_a_tipoareaumida_fk FOREIGN KEY (tipoareaumida)
	 REFERENCES dominios.tipoareaumida (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_area_umida_a ALTER COLUMN tipoareaumida SET DEFAULT 999#

CREATE TABLE cb.hid_bacia_hidrografica_a(
	 id serial NOT NULL,
	 codigootto integer,
	 geometriaaproximada smallint NOT NULL,
	 nivelotto integer,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_bacia_hidrografica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_bacia_hidrografica_a_geom ON cb.hid_bacia_hidrografica_a USING gist (geom)#

ALTER TABLE cb.hid_bacia_hidrografica_a
	 ADD CONSTRAINT hid_bacia_hidrografica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_bacia_hidrografica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_banco_areia_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 tipobanco smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_banco_areia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_banco_areia_a_geom ON cb.hid_banco_areia_a USING gist (geom)#

ALTER TABLE cb.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 12 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 24 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_banco_areia_a ALTER COLUMN materialpredominante SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_a ALTER COLUMN situacaoemagua SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_tipobanco_fk FOREIGN KEY (tipobanco)
	 REFERENCES dominios.tipobanco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_a ALTER COLUMN tipobanco SET DEFAULT 999#

CREATE TABLE cb.hid_banco_areia_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 tipobanco smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_banco_areia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_banco_areia_l_geom ON cb.hid_banco_areia_l USING gist (geom)#

ALTER TABLE cb.hid_banco_areia_l
	 ADD CONSTRAINT hid_banco_areia_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_l
	 ADD CONSTRAINT hid_banco_areia_l_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_l
	 ADD CONSTRAINT hid_banco_areia_l_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 12 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 24 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_banco_areia_l ALTER COLUMN materialpredominante SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_l
	 ADD CONSTRAINT hid_banco_areia_l_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_l ALTER COLUMN situacaoemagua SET DEFAULT 999#

ALTER TABLE cb.hid_banco_areia_l
	 ADD CONSTRAINT hid_banco_areia_l_tipobanco_fk FOREIGN KEY (tipobanco)
	 REFERENCES dominios.tipobanco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_banco_areia_l ALTER COLUMN tipobanco SET DEFAULT 999#

CREATE TABLE cb.hid_barragem_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_barragem_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_a_geom ON cb.hid_barragem_a USING gist (geom)#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_barragem_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.usoprincipal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_a ALTER COLUMN usoprincipal SET DEFAULT 999#

CREATE TABLE cb.hid_barragem_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_barragem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_l_geom ON cb.hid_barragem_l USING gist (geom)#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_barragem_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.usoprincipal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_l ALTER COLUMN usoprincipal SET DEFAULT 999#

CREATE TABLE cb.hid_barragem_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_barragem_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_p_geom ON cb.hid_barragem_p USING gist (geom)#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_barragem_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.usoprincipal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_barragem_p ALTER COLUMN usoprincipal SET DEFAULT 999#

CREATE TABLE cb.hid_comporta_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_comporta_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_comporta_l_geom ON cb.hid_comporta_l USING gist (geom)#

ALTER TABLE cb.hid_comporta_l
	 ADD CONSTRAINT hid_comporta_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_comporta_l
	 ADD CONSTRAINT hid_comporta_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_comporta_l
	 ADD CONSTRAINT hid_comporta_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.hid_comporta_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_comporta_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_comporta_p_geom ON cb.hid_comporta_p USING gist (geom)#

ALTER TABLE cb.hid_comporta_p
	 ADD CONSTRAINT hid_comporta_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_comporta_p
	 ADD CONSTRAINT hid_comporta_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_comporta_p
	 ADD CONSTRAINT hid_comporta_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_comporta_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.hid_confluencia_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_confluencia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_confluencia_p_geom ON cb.hid_confluencia_p USING gist (geom)#

ALTER TABLE cb.hid_confluencia_p
	 ADD CONSTRAINT hid_confluencia_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_confluencia_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_corredeira_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_corredeira_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_a_geom ON cb.hid_corredeira_a USING gist (geom)#

ALTER TABLE cb.hid_corredeira_a
	 ADD CONSTRAINT hid_corredeira_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_corredeira_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_corredeira_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_corredeira_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_l_geom ON cb.hid_corredeira_l USING gist (geom)#

ALTER TABLE cb.hid_corredeira_l
	 ADD CONSTRAINT hid_corredeira_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_corredeira_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_corredeira_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_corredeira_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_p_geom ON cb.hid_corredeira_p USING gist (geom)#

ALTER TABLE cb.hid_corredeira_p
	 ADD CONSTRAINT hid_corredeira_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_corredeira_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_descontinuidade_geometrica_a_geom ON cb.hid_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.hid_descontinuidade_geometrica_a
	 ADD CONSTRAINT hid_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.hid_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_descontinuidade_geometrica_l_geom ON cb.hid_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.hid_descontinuidade_geometrica_l
	 ADD CONSTRAINT hid_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.hid_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_descontinuidade_geometrica_p_geom ON cb.hid_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.hid_descontinuidade_geometrica_p
	 ADD CONSTRAINT hid_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.hid_fonte_dagua_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 qualidagua smallint NOT NULL,
	 regime smallint NOT NULL,
	 tipofontedagua smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_fonte_dagua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_fonte_dagua_p_geom ON cb.hid_fonte_dagua_p USING gist (geom)#

ALTER TABLE cb.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_fonte_dagua_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_qualidagua_fk FOREIGN KEY (qualidagua)
	 REFERENCES dominios.qualidagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_fonte_dagua_p ALTER COLUMN qualidagua SET DEFAULT 999#

ALTER TABLE cb.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_regime_check 
	 CHECK (regime = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 3 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_fonte_dagua_p ALTER COLUMN regime SET DEFAULT 999#

ALTER TABLE cb.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_tipofontedagua_fk FOREIGN KEY (tipofontedagua)
	 REFERENCES dominios.tipofontedagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_fonte_dagua_p ALTER COLUMN tipofontedagua SET DEFAULT 999#

CREATE TABLE cb.hid_foz_maritima_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_foz_maritima_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_foz_maritima_a_geom ON cb.hid_foz_maritima_a USING gist (geom)#

ALTER TABLE cb.hid_foz_maritima_a
	 ADD CONSTRAINT hid_foz_maritima_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_foz_maritima_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_foz_maritima_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_foz_maritima_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_foz_maritima_l_geom ON cb.hid_foz_maritima_l USING gist (geom)#

ALTER TABLE cb.hid_foz_maritima_l
	 ADD CONSTRAINT hid_foz_maritima_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_foz_maritima_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_foz_maritima_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_foz_maritima_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_foz_maritima_p_geom ON cb.hid_foz_maritima_p USING gist (geom)#

ALTER TABLE cb.hid_foz_maritima_p
	 ADD CONSTRAINT hid_foz_maritima_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_foz_maritima_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_ilha_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoilha smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_ilha_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ilha_a_geom ON cb.hid_ilha_a USING gist (geom)#

ALTER TABLE cb.hid_ilha_a
	 ADD CONSTRAINT hid_ilha_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_ilha_a
	 ADD CONSTRAINT hid_ilha_a_tipoilha_fk FOREIGN KEY (tipoilha)
	 REFERENCES dominios.tipoilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_a ALTER COLUMN tipoilha SET DEFAULT 999#

CREATE TABLE cb.hid_ilha_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoilha smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_ilha_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ilha_l_geom ON cb.hid_ilha_l USING gist (geom)#

ALTER TABLE cb.hid_ilha_l
	 ADD CONSTRAINT hid_ilha_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_ilha_l
	 ADD CONSTRAINT hid_ilha_l_tipoilha_fk FOREIGN KEY (tipoilha)
	 REFERENCES dominios.tipoilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_l ALTER COLUMN tipoilha SET DEFAULT 999#

CREATE TABLE cb.hid_ilha_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoilha smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_ilha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ilha_p_geom ON cb.hid_ilha_p USING gist (geom)#

ALTER TABLE cb.hid_ilha_p
	 ADD CONSTRAINT hid_ilha_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_ilha_p
	 ADD CONSTRAINT hid_ilha_p_tipoilha_fk FOREIGN KEY (tipoilha)
	 REFERENCES dominios.tipoilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ilha_p ALTER COLUMN tipoilha SET DEFAULT 999#

CREATE TABLE cb.hid_limite_massa_dagua_l(
	 id serial NOT NULL,
	 alturamediamargem real,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nomeabrev varchar(255),
	 tipolimmassa smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_limite_massa_dagua_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_limite_massa_dagua_l_geom ON cb.hid_limite_massa_dagua_l USING gist (geom)#

ALTER TABLE cb.hid_limite_massa_dagua_l
	 ADD CONSTRAINT hid_limite_massa_dagua_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_limite_massa_dagua_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_limite_massa_dagua_l
	 ADD CONSTRAINT hid_limite_massa_dagua_l_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_limite_massa_dagua_l
	 ADD CONSTRAINT hid_limite_massa_dagua_l_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 50 :: SMALLINT, 97 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_limite_massa_dagua_l ALTER COLUMN materialpredominante SET DEFAULT 999#

ALTER TABLE cb.hid_limite_massa_dagua_l
	 ADD CONSTRAINT hid_limite_massa_dagua_l_tipolimmassa_fk FOREIGN KEY (tipolimmassa)
	 REFERENCES dominios.tipolimmassa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_limite_massa_dagua_l ALTER COLUMN tipolimmassa SET DEFAULT 999#

CREATE TABLE cb.hid_massa_dagua_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 regime smallint NOT NULL,
	 salinidade smallint NOT NULL,
	 tipomassadagua smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_massa_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_massa_dagua_a_geom ON cb.hid_massa_dagua_a USING gist (geom)#

ALTER TABLE cb.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_massa_dagua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_regime_check 
	 CHECK (regime = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_massa_dagua_a ALTER COLUMN regime SET DEFAULT 999#

ALTER TABLE cb.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_salinidade_fk FOREIGN KEY (salinidade)
	 REFERENCES dominios.salinidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_massa_dagua_a ALTER COLUMN salinidade SET DEFAULT 999#

ALTER TABLE cb.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_tipomassadagua_fk FOREIGN KEY (tipomassadagua)
	 REFERENCES dominios.tipomassadagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_massa_dagua_a ALTER COLUMN tipomassadagua SET DEFAULT 999#

CREATE TABLE cb.hid_natureza_fundo_a(
	 id serial NOT NULL,
	 espessalgas smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_natureza_fundo_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_natureza_fundo_a_geom ON cb.hid_natureza_fundo_a USING gist (geom)#

ALTER TABLE cb.hid_natureza_fundo_a
	 ADD CONSTRAINT hid_natureza_fundo_a_espessalgas_fk FOREIGN KEY (espessalgas)
	 REFERENCES dominios.espessalgas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_a ALTER COLUMN espessalgas SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_a
	 ADD CONSTRAINT hid_natureza_fundo_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_a
	 ADD CONSTRAINT hid_natureza_fundo_a_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_a
	 ADD CONSTRAINT hid_natureza_fundo_a_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 50 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_natureza_fundo_a ALTER COLUMN materialpredominante SET DEFAULT 999#

CREATE TABLE cb.hid_natureza_fundo_l(
	 id serial NOT NULL,
	 espessalgas smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_natureza_fundo_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_natureza_fundo_l_geom ON cb.hid_natureza_fundo_l USING gist (geom)#

ALTER TABLE cb.hid_natureza_fundo_l
	 ADD CONSTRAINT hid_natureza_fundo_l_espessalgas_fk FOREIGN KEY (espessalgas)
	 REFERENCES dominios.espessalgas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_l ALTER COLUMN espessalgas SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_l
	 ADD CONSTRAINT hid_natureza_fundo_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_l
	 ADD CONSTRAINT hid_natureza_fundo_l_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_l
	 ADD CONSTRAINT hid_natureza_fundo_l_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 50 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_natureza_fundo_l ALTER COLUMN materialpredominante SET DEFAULT 999#

CREATE TABLE cb.hid_natureza_fundo_p(
	 id serial NOT NULL,
	 espessalgas smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 materialpredominante smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_natureza_fundo_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_natureza_fundo_p_geom ON cb.hid_natureza_fundo_p USING gist (geom)#

ALTER TABLE cb.hid_natureza_fundo_p
	 ADD CONSTRAINT hid_natureza_fundo_p_espessalgas_fk FOREIGN KEY (espessalgas)
	 REFERENCES dominios.espessalgas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_p ALTER COLUMN espessalgas SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_p
	 ADD CONSTRAINT hid_natureza_fundo_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_natureza_fundo_p
	 ADD CONSTRAINT hid_natureza_fundo_p_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.materialpredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_natureza_fundo_p
	 ADD CONSTRAINT hid_natureza_fundo_p_materialpredominante_check 
	 CHECK (materialpredominante = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 20 :: SMALLINT, 21 :: SMALLINT, 22 :: SMALLINT, 50 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_natureza_fundo_p ALTER COLUMN materialpredominante SET DEFAULT 999#

CREATE TABLE cb.hid_ponto_drenagem_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 relacionado smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_ponto_drenagem_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ponto_drenagem_p_geom ON cb.hid_ponto_drenagem_p USING gist (geom)#

ALTER TABLE cb.hid_ponto_drenagem_p
	 ADD CONSTRAINT hid_ponto_drenagem_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ponto_drenagem_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_ponto_drenagem_p
	 ADD CONSTRAINT hid_ponto_drenagem_p_relacionado_fk FOREIGN KEY (relacionado)
	 REFERENCES dominios.relacionado_hid (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ponto_drenagem_p ALTER COLUMN relacionado SET DEFAULT 999#

CREATE TABLE cb.hid_ponto_inicio_drenagem_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nascente smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_ponto_inicio_drenagem_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ponto_inicio_drenagem_p_geom ON cb.hid_ponto_inicio_drenagem_p USING gist (geom)#

ALTER TABLE cb.hid_ponto_inicio_drenagem_p
	 ADD CONSTRAINT hid_ponto_inicio_drenagem_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ponto_inicio_drenagem_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_ponto_inicio_drenagem_p
	 ADD CONSTRAINT hid_ponto_inicio_drenagem_p_nascente_fk FOREIGN KEY (nascente)
	 REFERENCES dominios.nascente (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_ponto_inicio_drenagem_p ALTER COLUMN nascente SET DEFAULT 999#

CREATE TABLE cb.hid_quebramar_molhe_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 situamare smallint NOT NULL,
	 tipoquebramolhe smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_quebramar_molhe_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_quebramar_molhe_a_geom ON cb.hid_quebramar_molhe_a USING gist (geom)#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_situamare_fk FOREIGN KEY (situamare)
	 REFERENCES dominios.situamare (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN situamare SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_tipoquebramolhe_fk FOREIGN KEY (tipoquebramolhe)
	 REFERENCES dominios.tipoquebramolhe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_a ALTER COLUMN tipoquebramolhe SET DEFAULT 999#

CREATE TABLE cb.hid_quebramar_molhe_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 situamare smallint NOT NULL,
	 tipoquebramolhe smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_quebramar_molhe_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_quebramar_molhe_l_geom ON cb.hid_quebramar_molhe_l USING gist (geom)#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_situamare_fk FOREIGN KEY (situamare)
	 REFERENCES dominios.situamare (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN situamare SET DEFAULT 999#

ALTER TABLE cb.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_tipoquebramolhe_fk FOREIGN KEY (tipoquebramolhe)
	 REFERENCES dominios.tipoquebramolhe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_quebramar_molhe_l ALTER COLUMN tipoquebramolhe SET DEFAULT 999#

CREATE TABLE cb.hid_queda_dagua_a(
	 id serial NOT NULL,
	 altura real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoqueda smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_queda_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_queda_dagua_a_geom ON cb.hid_queda_dagua_a USING gist (geom)#

ALTER TABLE cb.hid_queda_dagua_a
	 ADD CONSTRAINT hid_queda_dagua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_queda_dagua_a
	 ADD CONSTRAINT hid_queda_dagua_a_tipoqueda_fk FOREIGN KEY (tipoqueda)
	 REFERENCES dominios.tipoqueda (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_a ALTER COLUMN tipoqueda SET DEFAULT 999#

CREATE TABLE cb.hid_queda_dagua_l(
	 id serial NOT NULL,
	 altura real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoqueda smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_queda_dagua_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_queda_dagua_l_geom ON cb.hid_queda_dagua_l USING gist (geom)#

ALTER TABLE cb.hid_queda_dagua_l
	 ADD CONSTRAINT hid_queda_dagua_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_queda_dagua_l
	 ADD CONSTRAINT hid_queda_dagua_l_tipoqueda_fk FOREIGN KEY (tipoqueda)
	 REFERENCES dominios.tipoqueda (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_l ALTER COLUMN tipoqueda SET DEFAULT 999#

CREATE TABLE cb.hid_queda_dagua_p(
	 id serial NOT NULL,
	 altura real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoqueda smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_queda_dagua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_queda_dagua_p_geom ON cb.hid_queda_dagua_p USING gist (geom)#

ALTER TABLE cb.hid_queda_dagua_p
	 ADD CONSTRAINT hid_queda_dagua_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_queda_dagua_p
	 ADD CONSTRAINT hid_queda_dagua_p_tipoqueda_fk FOREIGN KEY (tipoqueda)
	 REFERENCES dominios.tipoqueda (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_queda_dagua_p ALTER COLUMN tipoqueda SET DEFAULT 999#

CREATE TABLE cb.hid_recife_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaocosta smallint NOT NULL,
	 situamare smallint NOT NULL,
	 tiporecife smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_recife_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_recife_a_geom ON cb.hid_recife_a USING gist (geom)#

ALTER TABLE cb.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_situacaocosta_fk FOREIGN KEY (situacaocosta)
	 REFERENCES dominios.situacaocosta (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_a ALTER COLUMN situacaocosta SET DEFAULT 999#

ALTER TABLE cb.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_situamare_fk FOREIGN KEY (situamare)
	 REFERENCES dominios.situamare (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_a ALTER COLUMN situamare SET DEFAULT 999#

ALTER TABLE cb.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_tiporecife_fk FOREIGN KEY (tiporecife)
	 REFERENCES dominios.tiporecife (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_a ALTER COLUMN tiporecife SET DEFAULT 999#

CREATE TABLE cb.hid_recife_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaocosta smallint NOT NULL,
	 situamare smallint NOT NULL,
	 tiporecife smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_recife_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_recife_l_geom ON cb.hid_recife_l USING gist (geom)#

ALTER TABLE cb.hid_recife_l
	 ADD CONSTRAINT hid_recife_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_recife_l
	 ADD CONSTRAINT hid_recife_l_situacaocosta_fk FOREIGN KEY (situacaocosta)
	 REFERENCES dominios.situacaocosta (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_l ALTER COLUMN situacaocosta SET DEFAULT 999#

ALTER TABLE cb.hid_recife_l
	 ADD CONSTRAINT hid_recife_l_situamare_fk FOREIGN KEY (situamare)
	 REFERENCES dominios.situamare (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_l ALTER COLUMN situamare SET DEFAULT 999#

ALTER TABLE cb.hid_recife_l
	 ADD CONSTRAINT hid_recife_l_tiporecife_fk FOREIGN KEY (tiporecife)
	 REFERENCES dominios.tiporecife (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_l ALTER COLUMN tiporecife SET DEFAULT 999#

CREATE TABLE cb.hid_recife_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaocosta smallint NOT NULL,
	 situamare smallint NOT NULL,
	 tiporecife smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_recife_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_recife_p_geom ON cb.hid_recife_p USING gist (geom)#

ALTER TABLE cb.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_situacaocosta_fk FOREIGN KEY (situacaocosta)
	 REFERENCES dominios.situacaocosta (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_p ALTER COLUMN situacaocosta SET DEFAULT 999#

ALTER TABLE cb.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_situamare_fk FOREIGN KEY (situamare)
	 REFERENCES dominios.situamare (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_p ALTER COLUMN situamare SET DEFAULT 999#

ALTER TABLE cb.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_tiporecife_fk FOREIGN KEY (tiporecife)
	 REFERENCES dominios.tiporecife (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_recife_p ALTER COLUMN tiporecife SET DEFAULT 999#

CREATE TABLE cb.hid_reservatorio_hidrico_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 namaximomaximorum integer,
	 namaximooperacional integer,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 usoprincipal smallint NOT NULL,
	 volumeutil integer,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_reservatorio_hidrico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_reservatorio_hidrico_a_geom ON cb.hid_reservatorio_hidrico_a USING gist (geom)#

ALTER TABLE cb.hid_reservatorio_hidrico_a
	 ADD CONSTRAINT hid_reservatorio_hidrico_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_reservatorio_hidrico_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_reservatorio_hidrico_a
	 ADD CONSTRAINT hid_reservatorio_hidrico_a_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.usoprincipal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_reservatorio_hidrico_a ALTER COLUMN usoprincipal SET DEFAULT 999#

CREATE TABLE cb.hid_rocha_em_agua_a(
	 id serial NOT NULL,
	 alturalamina real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_rocha_em_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_rocha_em_agua_a_geom ON cb.hid_rocha_em_agua_a USING gist (geom)#

ALTER TABLE cb.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_rocha_em_agua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_rocha_em_agua_a ALTER COLUMN situacaoemagua SET DEFAULT 999#

CREATE TABLE cb.hid_rocha_em_agua_p(
	 id serial NOT NULL,
	 alturalamina real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_rocha_em_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_rocha_em_agua_p_geom ON cb.hid_rocha_em_agua_p USING gist (geom)#

ALTER TABLE cb.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_rocha_em_agua_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_rocha_em_agua_p ALTER COLUMN situacaoemagua SET DEFAULT 999#

CREATE TABLE cb.hid_sumidouro_vertedouro_p(
	 id serial NOT NULL,
	 causa smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tiposumvert smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_sumidouro_vertedouro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_sumidouro_vertedouro_p_geom ON cb.hid_sumidouro_vertedouro_p USING gist (geom)#

ALTER TABLE cb.hid_sumidouro_vertedouro_p
	 ADD CONSTRAINT hid_sumidouro_vertedouro_p_causa_fk FOREIGN KEY (causa)
	 REFERENCES dominios.causa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_sumidouro_vertedouro_p ALTER COLUMN causa SET DEFAULT 999#

ALTER TABLE cb.hid_sumidouro_vertedouro_p
	 ADD CONSTRAINT hid_sumidouro_vertedouro_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_sumidouro_vertedouro_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_sumidouro_vertedouro_p
	 ADD CONSTRAINT hid_sumidouro_vertedouro_p_tiposumvert_fk FOREIGN KEY (tiposumvert)
	 REFERENCES dominios.tiposumvert (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_sumidouro_vertedouro_p ALTER COLUMN tiposumvert SET DEFAULT 999#

CREATE TABLE cb.hid_terreno_suj_inundacao_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 periodicidadeinunda varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_terreno_suj_inundacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_terreno_suj_inundacao_a_geom ON cb.hid_terreno_suj_inundacao_a USING gist (geom)#

ALTER TABLE cb.hid_terreno_suj_inundacao_a
	 ADD CONSTRAINT hid_terreno_suj_inundacao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_terreno_suj_inundacao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.hid_trecho_drenagem_l(
	 id serial NOT NULL,
	 caladomax real,
	 coincidecomdentrode smallint NOT NULL,
	 compartilhado smallint NOT NULL,
	 dentrodepoligono smallint NOT NULL,
	 eixoprincipal smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 larguramedia real,
	 navegabilidade smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 profundidademedia real,
	 regime smallint NOT NULL,
	 velocidademedcorrente real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_trecho_drenagem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_trecho_drenagem_l_geom ON cb.hid_trecho_drenagem_l USING gist (geom)#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_hid (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_compartilhado_fk FOREIGN KEY (compartilhado)
	 REFERENCES dominios.compartilhado (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN compartilhado SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_dentrodepoligono_fk FOREIGN KEY (dentrodepoligono)
	 REFERENCES dominios.dentrodepoligono (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN dentrodepoligono SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_eixoprincipal_fk FOREIGN KEY (eixoprincipal)
	 REFERENCES dominios.eixoprincipal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN eixoprincipal SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_navegabilidade_fk FOREIGN KEY (navegabilidade)
	 REFERENCES dominios.navegabilidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN navegabilidade SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_regime_check 
	 CHECK (regime = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_trecho_drenagem_l ALTER COLUMN regime SET DEFAULT 999#

CREATE TABLE cb.hid_trecho_massa_dagua_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 regime smallint NOT NULL,
	 salinidade smallint NOT NULL,
	 tipotrechomassa smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_trecho_massa_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_trecho_massa_dagua_a_geom ON cb.hid_trecho_massa_dagua_a USING gist (geom)#

ALTER TABLE cb.hid_trecho_massa_dagua_a
	 ADD CONSTRAINT hid_trecho_massa_dagua_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_massa_dagua_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_massa_dagua_a
	 ADD CONSTRAINT hid_trecho_massa_dagua_a_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_massa_dagua_a
	 ADD CONSTRAINT hid_trecho_massa_dagua_a_regime_check 
	 CHECK (regime = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.hid_trecho_massa_dagua_a ALTER COLUMN regime SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_massa_dagua_a
	 ADD CONSTRAINT hid_trecho_massa_dagua_a_salinidade_fk FOREIGN KEY (salinidade)
	 REFERENCES dominios.salinidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_massa_dagua_a ALTER COLUMN salinidade SET DEFAULT 999#

ALTER TABLE cb.hid_trecho_massa_dagua_a
	 ADD CONSTRAINT hid_trecho_massa_dagua_a_tipotrechomassa_fk FOREIGN KEY (tipotrechomassa)
	 REFERENCES dominios.tipotrechomassa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.hid_trecho_massa_dagua_a ALTER COLUMN tipotrechomassa SET DEFAULT 999#

CREATE TABLE cb.lim_area_de_litigio_a(
	 id serial NOT NULL,
	 descricao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_area_de_litigio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_de_litigio_a_geom ON cb.lim_area_de_litigio_a USING gist (geom)#

ALTER TABLE cb.lim_area_de_litigio_a
	 ADD CONSTRAINT lim_area_de_litigio_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_de_litigio_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_area_desenv_controle_a(
	 id serial NOT NULL,
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_area_desenv_controle_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_desenv_controle_a_geom ON cb.lim_area_desenv_controle_a USING gist (geom)#

ALTER TABLE cb.lim_area_desenv_controle_a
	 ADD CONSTRAINT lim_area_desenv_controle_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_desenv_controle_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_area_desenv_controle_p(
	 id serial NOT NULL,
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_area_desenv_controle_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_desenv_controle_p_geom ON cb.lim_area_desenv_controle_p USING gist (geom)#

ALTER TABLE cb.lim_area_desenv_controle_p
	 ADD CONSTRAINT lim_area_desenv_controle_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_desenv_controle_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_area_de_propriedade_particular_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_area_de_propriedade_particular_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_de_propriedade_particular_a_geom ON cb.lim_area_de_propriedade_particular_a USING gist (geom)#

ALTER TABLE cb.lim_area_de_propriedade_particular_a
	 ADD CONSTRAINT lim_area_de_propriedade_particular_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_de_propriedade_particular_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_area_uso_comunitario_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoareausocomun smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_area_uso_comunitario_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_uso_comunitario_a_geom ON cb.lim_area_uso_comunitario_a USING gist (geom)#

ALTER TABLE cb.lim_area_uso_comunitario_a
	 ADD CONSTRAINT lim_area_uso_comunitario_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_uso_comunitario_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_area_uso_comunitario_a
	 ADD CONSTRAINT lim_area_uso_comunitario_a_tipoareausocomun_fk FOREIGN KEY (tipoareausocomun)
	 REFERENCES dominios.tipoareausocomun (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_uso_comunitario_a ALTER COLUMN tipoareausocomun SET DEFAULT 999#

CREATE TABLE cb.lim_area_uso_comunitario_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoareausocomun smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_area_uso_comunitario_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_area_uso_comunitario_p_geom ON cb.lim_area_uso_comunitario_p USING gist (geom)#

ALTER TABLE cb.lim_area_uso_comunitario_p
	 ADD CONSTRAINT lim_area_uso_comunitario_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_uso_comunitario_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_area_uso_comunitario_p
	 ADD CONSTRAINT lim_area_uso_comunitario_p_tipoareausocomun_fk FOREIGN KEY (tipoareausocomun)
	 REFERENCES dominios.tipoareausocomun (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_area_uso_comunitario_p ALTER COLUMN tipoareausocomun SET DEFAULT 999#

CREATE TABLE cb.lim_bairro_a(
	 id serial NOT NULL,
	 anodereferencia integer,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_bairro_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_bairro_a_geom ON cb.lim_bairro_a USING gist (geom)#

ALTER TABLE cb.lim_bairro_a
	 ADD CONSTRAINT lim_bairro_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_bairro_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_delimitacao_fisica_l(
	 id serial NOT NULL,
	 eletrificada smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipodelimfis smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_delimitacao_fisica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_delimitacao_fisica_l_geom ON cb.lim_delimitacao_fisica_l USING gist (geom)#

ALTER TABLE cb.lim_delimitacao_fisica_l
	 ADD CONSTRAINT lim_delimitacao_fisica_l_eletrificada_fk FOREIGN KEY (eletrificada)
	 REFERENCES dominios.eletrificada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_delimitacao_fisica_l ALTER COLUMN eletrificada SET DEFAULT 999#

ALTER TABLE cb.lim_delimitacao_fisica_l
	 ADD CONSTRAINT lim_delimitacao_fisica_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_delimitacao_fisica_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_delimitacao_fisica_l
	 ADD CONSTRAINT lim_delimitacao_fisica_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_delimitacao_fisica_l
	 ADD CONSTRAINT lim_delimitacao_fisica_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_delimitacao_fisica_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.lim_delimitacao_fisica_l
	 ADD CONSTRAINT lim_delimitacao_fisica_l_tipodelimfis_fk FOREIGN KEY (tipodelimfis)
	 REFERENCES dominios.tipodelimfis (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_delimitacao_fisica_l ALTER COLUMN tipodelimfis SET DEFAULT 999#

CREATE TABLE cb.lim_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_descontinuidade_geometrica_a_geom ON cb.lim_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.lim_descontinuidade_geometrica_a
	 ADD CONSTRAINT lim_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.lim_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_descontinuidade_geometrica_l_geom ON cb.lim_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.lim_descontinuidade_geometrica_l
	 ADD CONSTRAINT lim_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.lim_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_descontinuidade_geometrica_p_geom ON cb.lim_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.lim_descontinuidade_geometrica_p
	 ADD CONSTRAINT lim_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.lim_distrito_a(
	 id serial NOT NULL,
	 anodereferencia varchar(255),
	 geocodigo varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_distrito_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_distrito_a_geom ON cb.lim_distrito_a USING gist (geom)#

ALTER TABLE cb.lim_distrito_a
	 ADD CONSTRAINT lim_distrito_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_distrito_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_limite_area_especial_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 tipolimareaesp smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_limite_area_especial_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_limite_area_especial_l_geom ON cb.lim_limite_area_especial_l USING gist (geom)#

ALTER TABLE cb.lim_limite_area_especial_l
	 ADD CONSTRAINT lim_limite_area_especial_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_area_especial_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_limite_area_especial_l
	 ADD CONSTRAINT lim_limite_area_especial_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_area_especial_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_limite_area_especial_l
	 ADD CONSTRAINT lim_limite_area_especial_l_tipolimareaesp_fk FOREIGN KEY (tipolimareaesp)
	 REFERENCES dominios.tipolimareaesp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_area_especial_l ALTER COLUMN tipolimareaesp SET DEFAULT 999#

CREATE TABLE cb.lim_limite_intra_munic_adm_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 tipolimintramun smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_limite_intra_munic_adm_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_limite_intra_munic_adm_l_geom ON cb.lim_limite_intra_munic_adm_l USING gist (geom)#

ALTER TABLE cb.lim_limite_intra_munic_adm_l
	 ADD CONSTRAINT lim_limite_intra_munic_adm_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_intra_munic_adm_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_limite_intra_munic_adm_l
	 ADD CONSTRAINT lim_limite_intra_munic_adm_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_intra_munic_adm_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_limite_intra_munic_adm_l
	 ADD CONSTRAINT lim_limite_intra_munic_adm_l_tipolimintramun_fk FOREIGN KEY (tipolimintramun)
	 REFERENCES dominios.tipolimintramun (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_intra_munic_adm_l ALTER COLUMN tipolimintramun SET DEFAULT 999#

CREATE TABLE cb.lim_limite_operacional_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 tipolimoper smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_limite_operacional_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_limite_operacional_l_geom ON cb.lim_limite_operacional_l USING gist (geom)#

ALTER TABLE cb.lim_limite_operacional_l
	 ADD CONSTRAINT lim_limite_operacional_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_operacional_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_limite_operacional_l
	 ADD CONSTRAINT lim_limite_operacional_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_operacional_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_limite_operacional_l
	 ADD CONSTRAINT lim_limite_operacional_l_tipolimoper_fk FOREIGN KEY (tipolimoper)
	 REFERENCES dominios.tipolimoper (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_operacional_l ALTER COLUMN tipolimoper SET DEFAULT 999#

CREATE TABLE cb.lim_limite_particular_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_limite_particular_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_limite_particular_l_geom ON cb.lim_limite_particular_l USING gist (geom)#

ALTER TABLE cb.lim_limite_particular_l
	 ADD CONSTRAINT lim_limite_particular_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_particular_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_limite_particular_l
	 ADD CONSTRAINT lim_limite_particular_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_particular_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_limite_politico_adm_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 tipolimpol smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_limite_politico_adm_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_limite_politico_adm_l_geom ON cb.lim_limite_politico_adm_l USING gist (geom)#

ALTER TABLE cb.lim_limite_politico_adm_l
	 ADD CONSTRAINT lim_limite_politico_adm_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_politico_adm_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_limite_politico_adm_l
	 ADD CONSTRAINT lim_limite_politico_adm_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_politico_adm_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_limite_politico_adm_l
	 ADD CONSTRAINT lim_limite_politico_adm_l_tipolimpol_fk FOREIGN KEY (tipolimpol)
	 REFERENCES dominios.tipolimpol (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_limite_politico_adm_l ALTER COLUMN tipolimpol SET DEFAULT 999#

CREATE TABLE cb.lim_linha_de_limite_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_linha_de_limite_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_linha_de_limite_l_geom ON cb.lim_linha_de_limite_l USING gist (geom)#

ALTER TABLE cb.lim_linha_de_limite_l
	 ADD CONSTRAINT lim_linha_de_limite_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_linha_de_limite_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_linha_de_limite_l
	 ADD CONSTRAINT lim_linha_de_limite_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_linha_de_limite_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_marco_de_limite_p(
	 id serial NOT NULL,
	 altitudeortometrica real,
	 geometriaaproximada smallint NOT NULL,
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 orgresp varchar(255),
	 outrarefalt varchar(255),
	 outrarefplan varchar(255),
	 referencialaltim smallint NOT NULL,
	 sistemageodesico smallint NOT NULL,
	 tipomarcolim smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_marco_de_limite_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_marco_de_limite_p_geom ON cb.lim_marco_de_limite_p USING gist (geom)#

ALTER TABLE cb.lim_marco_de_limite_p
	 ADD CONSTRAINT lim_marco_de_limite_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_marco_de_limite_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_marco_de_limite_p
	 ADD CONSTRAINT lim_marco_de_limite_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencialaltim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_marco_de_limite_p ALTER COLUMN referencialaltim SET DEFAULT 999#

ALTER TABLE cb.lim_marco_de_limite_p
	 ADD CONSTRAINT lim_marco_de_limite_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistemageodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_marco_de_limite_p ALTER COLUMN sistemageodesico SET DEFAULT 999#

ALTER TABLE cb.lim_marco_de_limite_p
	 ADD CONSTRAINT lim_marco_de_limite_p_tipomarcolim_fk FOREIGN KEY (tipomarcolim)
	 REFERENCES dominios.tipomarcolim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_marco_de_limite_p ALTER COLUMN tipomarcolim SET DEFAULT 999#

CREATE TABLE cb.lim_municipio_a(
	 id serial NOT NULL,
	 anodereferencia integer,
	 geocodigo varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_municipio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_municipio_a_geom ON cb.lim_municipio_a USING gist (geom)#

ALTER TABLE cb.lim_municipio_a
	 ADD CONSTRAINT lim_municipio_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_municipio_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_outras_unid_protegidas_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao varchar(255),
	 areaoficial varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 historicomodificacao varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipooutunidprot smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_outras_unid_protegidas_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_outras_unid_protegidas_a_geom ON cb.lim_outras_unid_protegidas_a USING gist (geom)#

ALTER TABLE cb.lim_outras_unid_protegidas_a
	 ADD CONSTRAINT lim_outras_unid_protegidas_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_a
	 ADD CONSTRAINT lim_outras_unid_protegidas_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_outras_unid_protegidas_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_outras_unid_protegidas_a
	 ADD CONSTRAINT lim_outras_unid_protegidas_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_outras_unid_protegidas_a
	 ADD CONSTRAINT lim_outras_unid_protegidas_a_tipooutunidprot_fk FOREIGN KEY (tipooutunidprot)
	 REFERENCES dominios.tipooutunidprot (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_a ALTER COLUMN tipooutunidprot SET DEFAULT 999#

CREATE TABLE cb.lim_outras_unid_protegidas_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao varchar(255),
	 areaoficial varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 historicomodificacao varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipooutunidprot smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_outras_unid_protegidas_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_outras_unid_protegidas_p_geom ON cb.lim_outras_unid_protegidas_p USING gist (geom)#

ALTER TABLE cb.lim_outras_unid_protegidas_p
	 ADD CONSTRAINT lim_outras_unid_protegidas_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_p
	 ADD CONSTRAINT lim_outras_unid_protegidas_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_outras_unid_protegidas_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_outras_unid_protegidas_p
	 ADD CONSTRAINT lim_outras_unid_protegidas_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_outras_unid_protegidas_p
	 ADD CONSTRAINT lim_outras_unid_protegidas_p_tipooutunidprot_fk FOREIGN KEY (tipooutunidprot)
	 REFERENCES dominios.tipooutunidprot (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outras_unid_protegidas_p ALTER COLUMN tipooutunidprot SET DEFAULT 999#

CREATE TABLE cb.lim_outros_limites_oficiais_l(
	 id serial NOT NULL,
	 coincidecomdentrode smallint NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obssituacao varchar(255),
	 tipooutlimofic smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT lim_outros_limites_oficiais_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_outros_limites_oficiais_l_geom ON cb.lim_outros_limites_oficiais_l USING gist (geom)#

ALTER TABLE cb.lim_outros_limites_oficiais_l
	 ADD CONSTRAINT lim_outros_limites_oficiais_l_coincidecomdentrode_fk FOREIGN KEY (coincidecomdentrode)
	 REFERENCES dominios.coincidecomdentrode_lim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outros_limites_oficiais_l ALTER COLUMN coincidecomdentrode SET DEFAULT 999#

ALTER TABLE cb.lim_outros_limites_oficiais_l
	 ADD CONSTRAINT lim_outros_limites_oficiais_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outros_limites_oficiais_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_outros_limites_oficiais_l
	 ADD CONSTRAINT lim_outros_limites_oficiais_l_tipooutlimofic_fk FOREIGN KEY (tipooutlimofic)
	 REFERENCES dominios.tipooutlimofic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_outros_limites_oficiais_l ALTER COLUMN tipooutlimofic SET DEFAULT 999#

CREATE TABLE cb.lim_pais_a(
	 id serial NOT NULL,
	 codiso3166 varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_pais_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_pais_a_geom ON cb.lim_pais_a USING gist (geom)#

ALTER TABLE cb.lim_pais_a
	 ADD CONSTRAINT lim_pais_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_pais_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_regiao_administrativa_a(
	 id serial NOT NULL,
	 anodereferencia integer,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_regiao_administrativa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_regiao_administrativa_a_geom ON cb.lim_regiao_administrativa_a USING gist (geom)#

ALTER TABLE cb.lim_regiao_administrativa_a
	 ADD CONSTRAINT lim_regiao_administrativa_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_regiao_administrativa_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_sub_distrito_a(
	 id serial NOT NULL,
	 anodereferencia varchar(255),
	 geocodigo varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_sub_distrito_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_sub_distrito_a_geom ON cb.lim_sub_distrito_a USING gist (geom)#

ALTER TABLE cb.lim_sub_distrito_a
	 ADD CONSTRAINT lim_sub_distrito_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_sub_distrito_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_terra_indigena_a(
	 id serial NOT NULL,
	 areaoficialha real,
	 datasituacaojuridica date,
	 geometriaaproximada smallint NOT NULL,
	 grupoetnico varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nometi varchar(255),
	 perimetrooficial real,
	 situacaojuridica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_terra_indigena_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_terra_indigena_a_geom ON cb.lim_terra_indigena_a USING gist (geom)#

ALTER TABLE cb.lim_terra_indigena_a
	 ADD CONSTRAINT lim_terra_indigena_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_indigena_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_terra_indigena_a
	 ADD CONSTRAINT lim_terra_indigena_a_situacaojuridica_fk FOREIGN KEY (situacaojuridica)
	 REFERENCES dominios.situacaojuridica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_indigena_a ALTER COLUMN situacaojuridica SET DEFAULT 999#

CREATE TABLE cb.lim_terra_indigena_p(
	 id serial NOT NULL,
	 areaoficialha real,
	 datasituacaojuridica date,
	 geometriaaproximada smallint NOT NULL,
	 grupoetnico varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nometi varchar(255),
	 perimetrooficial real,
	 situacaojuridica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_terra_indigena_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_terra_indigena_p_geom ON cb.lim_terra_indigena_p USING gist (geom)#

ALTER TABLE cb.lim_terra_indigena_p
	 ADD CONSTRAINT lim_terra_indigena_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_indigena_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_terra_indigena_p
	 ADD CONSTRAINT lim_terra_indigena_p_situacaojuridica_fk FOREIGN KEY (situacaojuridica)
	 REFERENCES dominios.situacaojuridica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_indigena_p ALTER COLUMN situacaojuridica SET DEFAULT 999#

CREATE TABLE cb.lim_terra_publica_a(
	 id serial NOT NULL,
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_terra_publica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_terra_publica_a_geom ON cb.lim_terra_publica_a USING gist (geom)#

ALTER TABLE cb.lim_terra_publica_a
	 ADD CONSTRAINT lim_terra_publica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_publica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_terra_publica_p(
	 id serial NOT NULL,
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_terra_publica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_terra_publica_p_geom ON cb.lim_terra_publica_p USING gist (geom)#

ALTER TABLE cb.lim_terra_publica_p
	 ADD CONSTRAINT lim_terra_publica_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_terra_publica_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_conserv_nao_snuc_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao varchar(255),
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_unidade_conserv_nao_snuc_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_conserv_nao_snuc_a_geom ON cb.lim_unidade_conserv_nao_snuc_a USING gist (geom)#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_conserv_nao_snuc_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao varchar(255),
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 classificacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_unidade_conserv_nao_snuc_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_conserv_nao_snuc_p_geom ON cb.lim_unidade_conserv_nao_snuc_p USING gist (geom)#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p
	 ADD CONSTRAINT lim_unidade_conserv_nao_snuc_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_conserv_nao_snuc_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_federacao_a(
	 id serial NOT NULL,
	 geocodigo varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_unidade_federacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_federacao_a_geom ON cb.lim_unidade_federacao_a USING gist (geom)#

ALTER TABLE cb.lim_unidade_federacao_a
	 ADD CONSTRAINT lim_unidade_federacao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_federacao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_protecao_integral_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao integer,
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipounidprotinteg smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_unidade_protecao_integral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_protecao_integral_a_geom ON cb.lim_unidade_protecao_integral_a USING gist (geom)#

ALTER TABLE cb.lim_unidade_protecao_integral_a
	 ADD CONSTRAINT lim_unidade_protecao_integral_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_a
	 ADD CONSTRAINT lim_unidade_protecao_integral_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_protecao_integral_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_protecao_integral_a
	 ADD CONSTRAINT lim_unidade_protecao_integral_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_protecao_integral_a
	 ADD CONSTRAINT lim_unidade_protecao_integral_a_tipounidprotinteg_fk FOREIGN KEY (tipounidprotinteg)
	 REFERENCES dominios.tipounidprotinteg (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_a ALTER COLUMN tipounidprotinteg SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_protecao_integral_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao integer,
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipounidprotinteg smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_unidade_protecao_integral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_protecao_integral_p_geom ON cb.lim_unidade_protecao_integral_p USING gist (geom)#

ALTER TABLE cb.lim_unidade_protecao_integral_p
	 ADD CONSTRAINT lim_unidade_protecao_integral_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_p
	 ADD CONSTRAINT lim_unidade_protecao_integral_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_protecao_integral_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_protecao_integral_p
	 ADD CONSTRAINT lim_unidade_protecao_integral_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_protecao_integral_p
	 ADD CONSTRAINT lim_unidade_protecao_integral_p_tipounidprotinteg_fk FOREIGN KEY (tipounidprotinteg)
	 REFERENCES dominios.tipounidprotinteg (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_protecao_integral_p ALTER COLUMN tipounidprotinteg SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_uso_sustentavel_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao integer,
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipounidusosust smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lim_unidade_uso_sustentavel_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_uso_sustentavel_a_geom ON cb.lim_unidade_uso_sustentavel_a USING gist (geom)#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_uso_sustentavel_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_a_tipounidusosust_fk FOREIGN KEY (tipounidusosust)
	 REFERENCES dominios.tipounidusosust (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_a ALTER COLUMN tipounidusosust SET DEFAULT 999#

CREATE TABLE cb.lim_unidade_uso_sustentavel_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 anocriacao integer,
	 areaoficial varchar(255),
	 atolegal varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 tipounidusosust smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lim_unidade_uso_sustentavel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lim_unidade_uso_sustentavel_p_geom ON cb.lim_unidade_uso_sustentavel_p USING gist (geom)#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.lim_unidade_uso_sustentavel_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p
	 ADD CONSTRAINT lim_unidade_uso_sustentavel_p_tipounidusosust_fk FOREIGN KEY (tipounidusosust)
	 REFERENCES dominios.tipounidusosust (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.lim_unidade_uso_sustentavel_p ALTER COLUMN tipounidusosust SET DEFAULT 999#

CREATE TABLE cb.loc_aglom_rural_de_ext_urbana_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 identificador varchar(255),
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_aglom_rural_de_ext_urbana_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_aglom_rural_de_ext_urbana_p_geom ON cb.loc_aglom_rural_de_ext_urbana_p USING gist (geom)#

ALTER TABLE cb.loc_aglom_rural_de_ext_urbana_p
	 ADD CONSTRAINT loc_aglom_rural_de_ext_urbana_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_aglom_rural_de_ext_urbana_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.loc_aglomerado_rural_isolado_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 identificador varchar(255),
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoaglomrurisol smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_aglomerado_rural_isolado_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_aglomerado_rural_isolado_p_geom ON cb.loc_aglomerado_rural_isolado_p USING gist (geom)#

ALTER TABLE cb.loc_aglomerado_rural_isolado_p
	 ADD CONSTRAINT loc_aglomerado_rural_isolado_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_aglomerado_rural_isolado_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_aglomerado_rural_isolado_p
	 ADD CONSTRAINT loc_aglomerado_rural_isolado_p_tipoaglomrurisol_fk FOREIGN KEY (tipoaglomrurisol)
	 REFERENCES dominios.tipoaglomrurisol (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_aglomerado_rural_isolado_p ALTER COLUMN tipoaglomrurisol SET DEFAULT 999#

CREATE TABLE cb.loc_area_edificada_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_area_edificada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_area_edificada_a_geom ON cb.loc_area_edificada_a USING gist (geom)#

ALTER TABLE cb.loc_area_edificada_a
	 ADD CONSTRAINT loc_area_edificada_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_area_edificada_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.loc_area_habitacional_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_area_habitacional_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_area_habitacional_a_geom ON cb.loc_area_habitacional_a USING gist (geom)#

ALTER TABLE cb.loc_area_habitacional_a
	 ADD CONSTRAINT loc_area_habitacional_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_area_habitacional_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.loc_area_urbana_isolada_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoassociado smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_area_urbana_isolada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_area_urbana_isolada_a_geom ON cb.loc_area_urbana_isolada_a USING gist (geom)#

ALTER TABLE cb.loc_area_urbana_isolada_a
	 ADD CONSTRAINT loc_area_urbana_isolada_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_area_urbana_isolada_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_area_urbana_isolada_a
	 ADD CONSTRAINT loc_area_urbana_isolada_a_tipoassociado_fk FOREIGN KEY (tipoassociado)
	 REFERENCES dominios.tipoassociado (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_area_urbana_isolada_a ALTER COLUMN tipoassociado SET DEFAULT 999#

CREATE TABLE cb.loc_capital_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 identificador varchar(255),
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipocapital smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_capital_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_capital_p_geom ON cb.loc_capital_p USING gist (geom)#

ALTER TABLE cb.loc_capital_p
	 ADD CONSTRAINT loc_capital_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_capital_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_capital_p
	 ADD CONSTRAINT loc_capital_p_tipocapital_fk FOREIGN KEY (tipocapital)
	 REFERENCES dominios.tipocapital (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_capital_p ALTER COLUMN tipocapital SET DEFAULT 999#

CREATE TABLE cb.loc_cidade_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 identificador varchar(255),
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_cidade_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_cidade_p_geom ON cb.loc_cidade_p USING gist (geom)#

ALTER TABLE cb.loc_cidade_p
	 ADD CONSTRAINT loc_cidade_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_cidade_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.loc_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_descontinuidade_geometrica_a_geom ON cb.loc_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.loc_descontinuidade_geometrica_a
	 ADD CONSTRAINT loc_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.loc_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT loc_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_descontinuidade_geometrica_l_geom ON cb.loc_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.loc_descontinuidade_geometrica_l
	 ADD CONSTRAINT loc_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.loc_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_descontinuidade_geometrica_p_geom ON cb.loc_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.loc_descontinuidade_geometrica_p
	 ADD CONSTRAINT loc_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.loc_edif_habitacional_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_edif_habitacional_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_edif_habitacional_a_geom ON cb.loc_edif_habitacional_a USING gist (geom)#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edif_habitacional_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_a
	 ADD CONSTRAINT loc_edif_habitacional_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edif_habitacional_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.loc_edif_habitacional_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_edif_habitacional_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_edif_habitacional_p_geom ON cb.loc_edif_habitacional_p USING gist (geom)#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edif_habitacional_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edif_habitacional_p
	 ADD CONSTRAINT loc_edif_habitacional_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edif_habitacional_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.loc_edificacao_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_edificacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_edificacao_a_geom ON cb.loc_edificacao_a USING gist (geom)#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edificacao_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_a
	 ADD CONSTRAINT loc_edificacao_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edificacao_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.loc_edificacao_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_edificacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_edificacao_p_geom ON cb.loc_edificacao_p USING gist (geom)#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edificacao_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_edificacao_p
	 ADD CONSTRAINT loc_edificacao_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.loc_edificacao_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.loc_hab_indigena_a(
	 id serial NOT NULL,
	 coletiva smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 isolada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT loc_hab_indigena_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_hab_indigena_a_geom ON cb.loc_hab_indigena_a USING gist (geom)#

ALTER TABLE cb.loc_hab_indigena_a
	 ADD CONSTRAINT loc_hab_indigena_a_coletiva_fk FOREIGN KEY (coletiva)
	 REFERENCES dominios.coletiva (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_a ALTER COLUMN coletiva SET DEFAULT 999#

ALTER TABLE cb.loc_hab_indigena_a
	 ADD CONSTRAINT loc_hab_indigena_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_hab_indigena_a
	 ADD CONSTRAINT loc_hab_indigena_a_isolada_fk FOREIGN KEY (isolada)
	 REFERENCES dominios.isolada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_a ALTER COLUMN isolada SET DEFAULT 999#

CREATE TABLE cb.loc_hab_indigena_p(
	 id serial NOT NULL,
	 coletiva smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 isolada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_hab_indigena_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_hab_indigena_p_geom ON cb.loc_hab_indigena_p USING gist (geom)#

ALTER TABLE cb.loc_hab_indigena_p
	 ADD CONSTRAINT loc_hab_indigena_p_coletiva_fk FOREIGN KEY (coletiva)
	 REFERENCES dominios.coletiva (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_p ALTER COLUMN coletiva SET DEFAULT 999#

ALTER TABLE cb.loc_hab_indigena_p
	 ADD CONSTRAINT loc_hab_indigena_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.loc_hab_indigena_p
	 ADD CONSTRAINT loc_hab_indigena_p_isolada_fk FOREIGN KEY (isolada)
	 REFERENCES dominios.isolada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_hab_indigena_p ALTER COLUMN isolada SET DEFAULT 999#

CREATE TABLE cb.loc_nome_local_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_nome_local_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_nome_local_p_geom ON cb.loc_nome_local_p USING gist (geom)#

ALTER TABLE cb.loc_nome_local_p
	 ADD CONSTRAINT loc_nome_local_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_nome_local_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.loc_vila_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 identificador varchar(255),
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT loc_vila_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX loc_vila_p_geom ON cb.loc_vila_p USING gist (geom)#

ALTER TABLE cb.loc_vila_p
	 ADD CONSTRAINT loc_vila_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.loc_vila_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.pto_area_est_med_fenom_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT pto_area_est_med_fenom_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_area_est_med_fenom_a_geom ON cb.pto_area_est_med_fenom_a USING gist (geom)#

ALTER TABLE cb.pto_area_est_med_fenom_a
	 ADD CONSTRAINT pto_area_est_med_fenom_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_area_est_med_fenom_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.pto_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT pto_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_descontinuidade_geometrica_a_geom ON cb.pto_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.pto_descontinuidade_geometrica_a
	 ADD CONSTRAINT pto_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.pto_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT pto_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_descontinuidade_geometrica_l_geom ON cb.pto_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.pto_descontinuidade_geometrica_l
	 ADD CONSTRAINT pto_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.pto_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_descontinuidade_geometrica_p_geom ON cb.pto_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.pto_descontinuidade_geometrica_p
	 ADD CONSTRAINT pto_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.pto_edif_constr_est_med_fen_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT pto_edif_constr_est_med_fen_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_edif_constr_est_med_fen_a_geom ON cb.pto_edif_constr_est_med_fen_a USING gist (geom)#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.pto_edif_constr_est_med_fen_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_a
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.pto_edif_constr_est_med_fen_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.pto_edif_constr_est_med_fen_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_edif_constr_est_med_fen_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_edif_constr_est_med_fen_p_geom ON cb.pto_edif_constr_est_med_fen_p USING gist (geom)#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.pto_edif_constr_est_med_fen_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_edif_constr_est_med_fen_p
	 ADD CONSTRAINT pto_edif_constr_est_med_fen_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.pto_edif_constr_est_med_fen_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.pto_pto_controle_p(
	 id serial NOT NULL,
	 altitudeortometrica real,
	 codponto varchar(255),
	 codprojeto varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 latitude varchar(255),
	 longitude varchar(255),
	 materializado smallint NOT NULL,
	 nomeabrev varchar(255),
	 obs varchar(255),
	 orgaoenteresp varchar(255),
	 outrarefalt varchar(255),
	 outrarefplan varchar(255),
	 referencialaltim smallint NOT NULL,
	 sistemageodesico smallint NOT NULL,
	 tipoptocontrole smallint NOT NULL,
	 tiporef smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_controle_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_controle_p_geom ON cb.pto_pto_controle_p USING gist (geom)#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_materializado_fk FOREIGN KEY (materializado)
	 REFERENCES dominios.materializado (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN materializado SET DEFAULT 999#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencialaltim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN referencialaltim SET DEFAULT 999#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistemageodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN sistemageodesico SET DEFAULT 999#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_tipoptocontrole_fk FOREIGN KEY (tipoptocontrole)
	 REFERENCES dominios.tipoptocontrole (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN tipoptocontrole SET DEFAULT 999#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_tiporef_fk FOREIGN KEY (tiporef)
	 REFERENCES dominios.tiporef (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_controle_p
	 ADD CONSTRAINT pto_pto_controle_p_tiporef_check 
	 CHECK (tiporef = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.pto_pto_controle_p ALTER COLUMN tiporef SET DEFAULT 999#

CREATE TABLE cb.pto_pto_est_med_fenomenos_p(
	 id serial NOT NULL,
	 codestacao varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 orgaoenteresp varchar(255),
	 tipoptoestmed smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_est_med_fenomenos_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_est_med_fenomenos_p_geom ON cb.pto_pto_est_med_fenomenos_p USING gist (geom)#

ALTER TABLE cb.pto_pto_est_med_fenomenos_p
	 ADD CONSTRAINT pto_pto_est_med_fenomenos_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_est_med_fenomenos_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.pto_pto_est_med_fenomenos_p
	 ADD CONSTRAINT pto_pto_est_med_fenomenos_p_tipoptoestmed_fk FOREIGN KEY (tipoptoestmed)
	 REFERENCES dominios.tipoptoestmed (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_est_med_fenomenos_p ALTER COLUMN tipoptoestmed SET DEFAULT 999#

CREATE TABLE cb.pto_pto_ref_geod_topo_p(
	 id serial NOT NULL,
	 altitudeortometrica real,
	 codponto varchar(255),
	 datavisita varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 latitude varchar(255),
	 longitude varchar(255),
	 nome varchar(255),
	 nomeabrev varchar(255),
	 obs varchar(255),
	 orgaoenteresp varchar(255),
	 outrarefalt varchar(255),
	 outrarefplan varchar(255),
	 proximidade smallint NOT NULL,
	 rede smallint NOT NULL,
	 referencialaltim smallint NOT NULL,
	 referencialgrav smallint NOT NULL,
	 sistemageodesico smallint NOT NULL,
	 situacaomarco smallint NOT NULL,
	 tipoptorefgeodtopo smallint NOT NULL,
	 tiporef smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_ref_geod_topo_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_ref_geod_topo_p_geom ON cb.pto_pto_ref_geod_topo_p USING gist (geom)#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_proximidade_fk FOREIGN KEY (proximidade)
	 REFERENCES dominios.proximidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN proximidade SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_rede_fk FOREIGN KEY (rede)
	 REFERENCES dominios.rede (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN rede SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencialaltim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN referencialaltim SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_referencialgrav_fk FOREIGN KEY (referencialgrav)
	 REFERENCES dominios.referencialgrav (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN referencialgrav SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistemageodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN sistemageodesico SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_situacaomarco_fk FOREIGN KEY (situacaomarco)
	 REFERENCES dominios.situacaomarco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN situacaomarco SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_tipoptorefgeodtopo_fk FOREIGN KEY (tipoptorefgeodtopo)
	 REFERENCES dominios.tipoptorefgeodtopo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN tipoptorefgeodtopo SET DEFAULT 999#

ALTER TABLE cb.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_tiporef_fk FOREIGN KEY (tiporef)
	 REFERENCES dominios.tiporef (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.pto_pto_ref_geod_topo_p ALTER COLUMN tiporef SET DEFAULT 999#

CREATE TABLE cb.rel_alter_fisiog_antropica_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoalterantrop smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_alter_fisiog_antropica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_alter_fisiog_antropica_a_geom ON cb.rel_alter_fisiog_antropica_a USING gist (geom)#

ALTER TABLE cb.rel_alter_fisiog_antropica_a
	 ADD CONSTRAINT rel_alter_fisiog_antropica_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_alter_fisiog_antropica_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_alter_fisiog_antropica_a
	 ADD CONSTRAINT rel_alter_fisiog_antropica_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipoalterantrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_alter_fisiog_antropica_a ALTER COLUMN tipoalterantrop SET DEFAULT 999#

CREATE TABLE cb.rel_alter_fisiog_antropica_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoalterantrop smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_alter_fisiog_antropica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_alter_fisiog_antropica_l_geom ON cb.rel_alter_fisiog_antropica_l USING gist (geom)#

ALTER TABLE cb.rel_alter_fisiog_antropica_l
	 ADD CONSTRAINT rel_alter_fisiog_antropica_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_alter_fisiog_antropica_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_alter_fisiog_antropica_l
	 ADD CONSTRAINT rel_alter_fisiog_antropica_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipoalterantrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_alter_fisiog_antropica_l ALTER COLUMN tipoalterantrop SET DEFAULT 999#

CREATE TABLE cb.rel_curva_batimetrica_l(
	 id serial NOT NULL,
	 profundidade integer,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_curva_batimetrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_curva_batimetrica_l_geom ON cb.rel_curva_batimetrica_l USING gist (geom)#

CREATE TABLE cb.rel_curva_nivel_l(
	 id serial NOT NULL,
	 cota integer,
	 depressao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 indice smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_curva_nivel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_curva_nivel_l_geom ON cb.rel_curva_nivel_l USING gist (geom)#

ALTER TABLE cb.rel_curva_nivel_l
	 ADD CONSTRAINT rel_curva_nivel_l_depressao_fk FOREIGN KEY (depressao)
	 REFERENCES dominios.depressao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_curva_nivel_l ALTER COLUMN depressao SET DEFAULT 999#

ALTER TABLE cb.rel_curva_nivel_l
	 ADD CONSTRAINT rel_curva_nivel_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_curva_nivel_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_curva_nivel_l
	 ADD CONSTRAINT rel_curva_nivel_l_indice_fk FOREIGN KEY (indice)
	 REFERENCES dominios.indice (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_curva_nivel_l ALTER COLUMN indice SET DEFAULT 999#

CREATE TABLE cb.rel_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_descontinuidade_geometrica_a_geom ON cb.rel_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.rel_descontinuidade_geometrica_a
	 ADD CONSTRAINT rel_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.rel_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_descontinuidade_geometrica_l_geom ON cb.rel_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.rel_descontinuidade_geometrica_l
	 ADD CONSTRAINT rel_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.rel_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_descontinuidade_geometrica_p_geom ON cb.rel_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.rel_descontinuidade_geometrica_p
	 ADD CONSTRAINT rel_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.rel_dolina_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_dolina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_dolina_a_geom ON cb.rel_dolina_a USING gist (geom)#

ALTER TABLE cb.rel_dolina_a
	 ADD CONSTRAINT rel_dolina_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_dolina_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_dolina_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_dolina_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_dolina_p_geom ON cb.rel_dolina_p USING gist (geom)#

ALTER TABLE cb.rel_dolina_p
	 ADD CONSTRAINT rel_dolina_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_dolina_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_duna_a(
	 id serial NOT NULL,
	 fixa smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_duna_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_duna_a_geom ON cb.rel_duna_a USING gist (geom)#

ALTER TABLE cb.rel_duna_a
	 ADD CONSTRAINT rel_duna_a_fixa_fk FOREIGN KEY (fixa)
	 REFERENCES dominios.fixa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_duna_a ALTER COLUMN fixa SET DEFAULT 999#

ALTER TABLE cb.rel_duna_a
	 ADD CONSTRAINT rel_duna_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_duna_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_duna_p(
	 id serial NOT NULL,
	 fixa smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_duna_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_duna_p_geom ON cb.rel_duna_p USING gist (geom)#

ALTER TABLE cb.rel_duna_p
	 ADD CONSTRAINT rel_duna_p_fixa_fk FOREIGN KEY (fixa)
	 REFERENCES dominios.fixa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_duna_p ALTER COLUMN fixa SET DEFAULT 999#

ALTER TABLE cb.rel_duna_p
	 ADD CONSTRAINT rel_duna_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_duna_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_elemento_fisiog_natural_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_elemento_fisiog_natural_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiog_natural_a_geom ON cb.rel_elemento_fisiog_natural_a USING gist (geom)#

ALTER TABLE cb.rel_elemento_fisiog_natural_a
	 ADD CONSTRAINT rel_elemento_fisiog_natural_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_elemento_fisiog_natural_a
	 ADD CONSTRAINT rel_elemento_fisiog_natural_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipoelemnat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_a ALTER COLUMN tipoelemnat SET DEFAULT 999#

CREATE TABLE cb.rel_elemento_fisiog_natural_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_elemento_fisiog_natural_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiog_natural_l_geom ON cb.rel_elemento_fisiog_natural_l USING gist (geom)#

ALTER TABLE cb.rel_elemento_fisiog_natural_l
	 ADD CONSTRAINT rel_elemento_fisiog_natural_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_elemento_fisiog_natural_l
	 ADD CONSTRAINT rel_elemento_fisiog_natural_l_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipoelemnat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_l ALTER COLUMN tipoelemnat SET DEFAULT 999#

CREATE TABLE cb.rel_elemento_fisiog_natural_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_elemento_fisiog_natural_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiog_natural_p_geom ON cb.rel_elemento_fisiog_natural_p USING gist (geom)#

ALTER TABLE cb.rel_elemento_fisiog_natural_p
	 ADD CONSTRAINT rel_elemento_fisiog_natural_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_elemento_fisiog_natural_p
	 ADD CONSTRAINT rel_elemento_fisiog_natural_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipoelemnat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_elemento_fisiog_natural_p ALTER COLUMN tipoelemnat SET DEFAULT 999#

CREATE TABLE cb.rel_gruta_caverna_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipogrutacaverna smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_gruta_caverna_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_gruta_caverna_p_geom ON cb.rel_gruta_caverna_p USING gist (geom)#

ALTER TABLE cb.rel_gruta_caverna_p
	 ADD CONSTRAINT rel_gruta_caverna_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_gruta_caverna_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_gruta_caverna_p
	 ADD CONSTRAINT rel_gruta_caverna_p_tipogrutacaverna_fk FOREIGN KEY (tipogrutacaverna)
	 REFERENCES dominios.tipogrutacaverna (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_gruta_caverna_p ALTER COLUMN tipogrutacaverna SET DEFAULT 999#

CREATE TABLE cb.rel_pico_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_pico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_pico_p_geom ON cb.rel_pico_p USING gist (geom)#

ALTER TABLE cb.rel_pico_p
	 ADD CONSTRAINT rel_pico_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_pico_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_ponto_cotado_altimetrico_p(
	 id serial NOT NULL,
	 cota real,
	 cotacomprovada smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_ponto_cotado_altimetrico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_ponto_cotado_altimetrico_p_geom ON cb.rel_ponto_cotado_altimetrico_p USING gist (geom)#

ALTER TABLE cb.rel_ponto_cotado_altimetrico_p
	 ADD CONSTRAINT rel_ponto_cotado_altimetrico_p_cotacomprovada_fk FOREIGN KEY (cotacomprovada)
	 REFERENCES dominios.cotacomprovada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_ponto_cotado_altimetrico_p ALTER COLUMN cotacomprovada SET DEFAULT 999#

ALTER TABLE cb.rel_ponto_cotado_altimetrico_p
	 ADD CONSTRAINT rel_ponto_cotado_altimetrico_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_ponto_cotado_altimetrico_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.rel_ponto_cotado_batimetrico_p(
	 id serial NOT NULL,
	 profundidade real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_ponto_cotado_batimetrico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_ponto_cotado_batimetrico_p_geom ON cb.rel_ponto_cotado_batimetrico_p USING gist (geom)#

CREATE TABLE cb.rel_rocha_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tiporocha smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_rocha_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_rocha_a_geom ON cb.rel_rocha_a USING gist (geom)#

ALTER TABLE cb.rel_rocha_a
	 ADD CONSTRAINT rel_rocha_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_rocha_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_rocha_a
	 ADD CONSTRAINT rel_rocha_a_tiporocha_fk FOREIGN KEY (tiporocha)
	 REFERENCES dominios.tiporocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_rocha_a ALTER COLUMN tiporocha SET DEFAULT 999#

CREATE TABLE cb.rel_rocha_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tiporocha smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_rocha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_rocha_p_geom ON cb.rel_rocha_p USING gist (geom)#

ALTER TABLE cb.rel_rocha_p
	 ADD CONSTRAINT rel_rocha_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_rocha_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_rocha_p
	 ADD CONSTRAINT rel_rocha_p_tiporocha_fk FOREIGN KEY (tiporocha)
	 REFERENCES dominios.tiporocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_rocha_p ALTER COLUMN tiporocha SET DEFAULT 999#

CREATE TABLE cb.rel_terreno_exposto_a(
	 id serial NOT NULL,
	 causaexposicao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 tipoterrexp smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_terreno_exposto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_terreno_exposto_a_geom ON cb.rel_terreno_exposto_a USING gist (geom)#

ALTER TABLE cb.rel_terreno_exposto_a
	 ADD CONSTRAINT rel_terreno_exposto_a_causaexposicao_fk FOREIGN KEY (causaexposicao)
	 REFERENCES dominios.causaexposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_terreno_exposto_a ALTER COLUMN causaexposicao SET DEFAULT 999#

ALTER TABLE cb.rel_terreno_exposto_a
	 ADD CONSTRAINT rel_terreno_exposto_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_terreno_exposto_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.rel_terreno_exposto_a
	 ADD CONSTRAINT rel_terreno_exposto_a_tipoterrexp_fk FOREIGN KEY (tipoterrexp)
	 REFERENCES dominios.tipoterrexp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.rel_terreno_exposto_a ALTER COLUMN tipoterrexp SET DEFAULT 999#

CREATE TABLE cb.sau_area_saude_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT sau_area_saude_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_area_saude_a_geom ON cb.sau_area_saude_a USING gist (geom)#

ALTER TABLE cb.sau_area_saude_a
	 ADD CONSTRAINT sau_area_saude_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_area_saude_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.sau_area_servico_social_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT sau_area_servico_social_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_area_servico_social_a_geom ON cb.sau_area_servico_social_a USING gist (geom)#

ALTER TABLE cb.sau_area_servico_social_a
	 ADD CONSTRAINT sau_area_servico_social_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_area_servico_social_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.sau_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT sau_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_descontinuidade_geometrica_a_geom ON cb.sau_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.sau_descontinuidade_geometrica_a
	 ADD CONSTRAINT sau_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.sau_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT sau_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_descontinuidade_geometrica_l_geom ON cb.sau_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.sau_descontinuidade_geometrica_l
	 ADD CONSTRAINT sau_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.sau_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT sau_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_descontinuidade_geometrica_p_geom ON cb.sau_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.sau_descontinuidade_geometrica_p
	 ADD CONSTRAINT sau_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.sau_edif_saude_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nivelatencao smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT sau_edif_saude_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_edif_saude_a_geom ON cb.sau_edif_saude_a USING gist (geom)#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_nivelatencao_fk FOREIGN KEY (nivelatencao)
	 REFERENCES dominios.nivelatencao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN nivelatencao SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_a
	 ADD CONSTRAINT sau_edif_saude_a_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_a ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.sau_edif_saude_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nivelatencao smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT sau_edif_saude_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_edif_saude_p_geom ON cb.sau_edif_saude_p USING gist (geom)#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_nivelatencao_fk FOREIGN KEY (nivelatencao)
	 REFERENCES dominios.nivelatencao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN nivelatencao SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_saude_p
	 ADD CONSTRAINT sau_edif_saude_p_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_saude_p ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.sau_edif_servico_social_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT sau_edif_servico_social_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_edif_servico_social_a_geom ON cb.sau_edif_servico_social_a USING gist (geom)#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_a
	 ADD CONSTRAINT sau_edif_servico_social_a_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_a ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.sau_edif_servico_social_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoclassecnae smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT sau_edif_servico_social_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX sau_edif_servico_social_p_geom ON cb.sau_edif_servico_social_p USING gist (geom)#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 97 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_tipoclassecnae_fk FOREIGN KEY (tipoclassecnae)
	 REFERENCES dominios.tipoclassecnae (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.sau_edif_servico_social_p
	 ADD CONSTRAINT sau_edif_servico_social_p_tipoclassecnae_check 
	 CHECK (tipoclassecnae = ANY(ARRAY[0 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.sau_edif_servico_social_p ALTER COLUMN tipoclassecnae SET DEFAULT 999#

CREATE TABLE cb.tra_area_duto_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_area_duto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_area_duto_a_geom ON cb.tra_area_duto_a USING gist (geom)#

ALTER TABLE cb.tra_area_duto_a
	 ADD CONSTRAINT tra_area_duto_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_area_duto_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_area_estrut_transporte_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_area_estrut_transporte_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_area_estrut_transporte_a_geom ON cb.tra_area_estrut_transporte_a USING gist (geom)#

ALTER TABLE cb.tra_area_estrut_transporte_a
	 ADD CONSTRAINT tra_area_estrut_transporte_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_area_estrut_transporte_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_arruamento_l(
	 id serial NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 trafego smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_arruamento_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_arruamento_l_geom ON cb.tra_arruamento_l USING gist (geom)#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.canteirodivisorio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN canteirodivisorio SET DEFAULT 999#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_arruamento_l
	 ADD CONSTRAINT tra_arruamento_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_arruamento_l ALTER COLUMN trafego SET DEFAULT 999#

CREATE TABLE cb.tra_atracadouro_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoatracad smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_atracadouro_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_atracadouro_a_geom ON cb.tra_atracadouro_a USING gist (geom)#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_a
	 ADD CONSTRAINT tra_atracadouro_a_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipoatracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_a ALTER COLUMN tipoatracad SET DEFAULT 999#

CREATE TABLE cb.tra_atracadouro_l(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoatracad smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_atracadouro_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_atracadouro_l_geom ON cb.tra_atracadouro_l USING gist (geom)#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_l
	 ADD CONSTRAINT tra_atracadouro_l_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipoatracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_l ALTER COLUMN tipoatracad SET DEFAULT 999#

CREATE TABLE cb.tra_atracadouro_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoatracad smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_atracadouro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_atracadouro_p_geom ON cb.tra_atracadouro_p USING gist (geom)#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_atracadouro_p
	 ADD CONSTRAINT tra_atracadouro_p_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipoatracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_atracadouro_p ALTER COLUMN tipoatracad SET DEFAULT 999#

CREATE TABLE cb.tra_caminho_aereo_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocaminhoaereo smallint NOT NULL,
	 tipousocaminhoaer smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_caminho_aereo_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_caminho_aereo_l_geom ON cb.tra_caminho_aereo_l USING gist (geom)#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_caminho_aereo_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_caminho_aereo_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_caminho_aereo_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_tipocaminhoaereo_fk FOREIGN KEY (tipocaminhoaereo)
	 REFERENCES dominios.tipocaminhoaereo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_caminho_aereo_l ALTER COLUMN tipocaminhoaereo SET DEFAULT 999#

ALTER TABLE cb.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_tipousocaminhoaer_fk FOREIGN KEY (tipousocaminhoaer)
	 REFERENCES dominios.tipousocaminhoaer (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_caminho_aereo_l ALTER COLUMN tipousocaminhoaer SET DEFAULT 999#

CREATE TABLE cb.tra_ciclovia_l(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 trafego smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_ciclovia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ciclovia_l_geom ON cb.tra_ciclovia_l USING gist (geom)#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_ciclovia_l
	 ADD CONSTRAINT tra_ciclovia_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ciclovia_l ALTER COLUMN trafego SET DEFAULT 999#

CREATE TABLE cb.tra_condutor_hidrico_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 mattransp smallint NOT NULL,
	 nrdutos integer,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 setor smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocondutor smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_condutor_hidrico_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_condutor_hidrico_l_geom ON cb.tra_condutor_hidrico_l USING gist (geom)#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_mattransp_fk FOREIGN KEY (mattransp)
	 REFERENCES dominios.mattransp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_mattransp_check 
	 CHECK (mattransp = ANY(ARRAY[1 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN mattransp SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicaorelativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN posicaorelativa SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_setor_fk FOREIGN KEY (setor)
	 REFERENCES dominios.setor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_setor_check 
	 CHECK (setor = ANY(ARRAY[1 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN setor SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacaoespacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN situacaoespacial SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_condutor_hidrico_l
	 ADD CONSTRAINT tra_condutor_hidrico_l_tipocondutor_fk FOREIGN KEY (tipocondutor)
	 REFERENCES dominios.tipocondutor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_condutor_hidrico_l ALTER COLUMN tipocondutor SET DEFAULT 999#

CREATE TABLE cb.tra_cremalheira_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_cremalheira_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_cremalheira_l_geom ON cb.tra_cremalheira_l USING gist (geom)#

ALTER TABLE cb.tra_cremalheira_l
	 ADD CONSTRAINT tra_cremalheira_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_cremalheira_l
	 ADD CONSTRAINT tra_cremalheira_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_cremalheira_l
	 ADD CONSTRAINT tra_cremalheira_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_cremalheira_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_cremalheira_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_cremalheira_p_geom ON cb.tra_cremalheira_p USING gist (geom)#

ALTER TABLE cb.tra_cremalheira_p
	 ADD CONSTRAINT tra_cremalheira_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_cremalheira_p
	 ADD CONSTRAINT tra_cremalheira_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_cremalheira_p
	 ADD CONSTRAINT tra_cremalheira_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_cremalheira_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_descontinuidade_geometrica_a_geom ON cb.tra_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.tra_descontinuidade_geometrica_a
	 ADD CONSTRAINT tra_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.tra_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_descontinuidade_geometrica_l_geom ON cb.tra_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.tra_descontinuidade_geometrica_l
	 ADD CONSTRAINT tra_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.tra_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_descontinuidade_geometrica_p_geom ON cb.tra_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.tra_descontinuidade_geometrica_p
	 ADD CONSTRAINT tra_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.tra_eclusa_a(
	 id serial NOT NULL,
	 calado real,
	 desnivel real,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_eclusa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_eclusa_a_geom ON cb.tra_eclusa_a USING gist (geom)#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_a
	 ADD CONSTRAINT tra_eclusa_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_eclusa_l(
	 id serial NOT NULL,
	 calado real,
	 desnivel real,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_eclusa_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_eclusa_l_geom ON cb.tra_eclusa_l USING gist (geom)#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_l
	 ADD CONSTRAINT tra_eclusa_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_eclusa_p(
	 id serial NOT NULL,
	 calado real,
	 desnivel real,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_eclusa_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_eclusa_p_geom ON cb.tra_eclusa_p USING gist (geom)#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_eclusa_p
	 ADD CONSTRAINT tra_eclusa_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_eclusa_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_edif_constr_aeroportuaria_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifaero smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_edif_constr_aeroportuaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_constr_aeroportuaria_a_geom ON cb.tra_edif_constr_aeroportuaria_a USING gist (geom)#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_a_tipoedifaero_fk FOREIGN KEY (tipoedifaero)
	 REFERENCES dominios.tipoedifaero (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_a ALTER COLUMN tipoedifaero SET DEFAULT 999#

CREATE TABLE cb.tra_edif_constr_aeroportuaria_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifaero smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_edif_constr_aeroportuaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_constr_aeroportuaria_p_geom ON cb.tra_edif_constr_aeroportuaria_p USING gist (geom)#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT tra_edif_constr_aeroportuaria_p_tipoedifaero_fk FOREIGN KEY (tipoedifaero)
	 REFERENCES dominios.tipoedifaero (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_aeroportuaria_p ALTER COLUMN tipoedifaero SET DEFAULT 999#

CREATE TABLE cb.tra_edif_constr_portuaria_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifport smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_edif_constr_portuaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_constr_portuaria_a_geom ON cb.tra_edif_constr_portuaria_a USING gist (geom)#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_a
	 ADD CONSTRAINT tra_edif_constr_portuaria_a_tipoedifport_fk FOREIGN KEY (tipoedifport)
	 REFERENCES dominios.tipoedifport (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_a ALTER COLUMN tipoedifport SET DEFAULT 999#

CREATE TABLE cb.tra_edif_constr_portuaria_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifport smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_edif_constr_portuaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_constr_portuaria_p_geom ON cb.tra_edif_constr_portuaria_p USING gist (geom)#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_constr_portuaria_p
	 ADD CONSTRAINT tra_edif_constr_portuaria_p_tipoedifport_fk FOREIGN KEY (tipoedifport)
	 REFERENCES dominios.tipoedifport (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_constr_portuaria_p ALTER COLUMN tipoedifport SET DEFAULT 999#

CREATE TABLE cb.tra_edif_metro_ferroviaria_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 funcaoedifmetroferrov smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 multimodal smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_edif_metro_ferroviaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_metro_ferroviaria_a_geom ON cb.tra_edif_metro_ferroviaria_a USING gist (geom)#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_funcaoedifmetroferrov_fk FOREIGN KEY (funcaoedifmetroferrov)
	 REFERENCES dominios.funcaoedifmetroferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN funcaoedifmetroferrov SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_multimodal_fk FOREIGN KEY (multimodal)
	 REFERENCES dominios.multimodal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN multimodal SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_edif_metro_ferroviaria_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 funcaoedifmetroferrov smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 multimodal smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_edif_metro_ferroviaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_metro_ferroviaria_p_geom ON cb.tra_edif_metro_ferroviaria_p USING gist (geom)#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_funcaoedifmetroferrov_fk FOREIGN KEY (funcaoedifmetroferrov)
	 REFERENCES dominios.funcaoedifmetroferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN funcaoedifmetroferrov SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_multimodal_fk FOREIGN KEY (multimodal)
	 REFERENCES dominios.multimodal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN multimodal SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p
	 ADD CONSTRAINT tra_edif_metro_ferroviaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_metro_ferroviaria_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_edif_rodoviaria_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifrod smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_edif_rodoviaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_rodoviaria_a_geom ON cb.tra_edif_rodoviaria_a USING gist (geom)#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_a
	 ADD CONSTRAINT tra_edif_rodoviaria_a_tipoedifrod_fk FOREIGN KEY (tipoedifrod)
	 REFERENCES dominios.tipoedifrod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_a ALTER COLUMN tipoedifrod SET DEFAULT 999#

CREATE TABLE cb.tra_edif_rodoviaria_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoedifrod smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_edif_rodoviaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_edif_rodoviaria_p_geom ON cb.tra_edif_rodoviaria_p USING gist (geom)#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_edif_rodoviaria_p
	 ADD CONSTRAINT tra_edif_rodoviaria_p_tipoedifrod_fk FOREIGN KEY (tipoedifrod)
	 REFERENCES dominios.tipoedifrod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_edif_rodoviaria_p ALTER COLUMN tipoedifrod SET DEFAULT 999#

CREATE TABLE cb.tra_entroncamento_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipoentroncamento smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_entroncamento_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_entroncamento_p_geom ON cb.tra_entroncamento_p USING gist (geom)#

ALTER TABLE cb.tra_entroncamento_p
	 ADD CONSTRAINT tra_entroncamento_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_entroncamento_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_entroncamento_p
	 ADD CONSTRAINT tra_entroncamento_p_tipoentroncamento_fk FOREIGN KEY (tipoentroncamento)
	 REFERENCES dominios.tipoentroncamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_entroncamento_p ALTER COLUMN tipoentroncamento SET DEFAULT 999#

CREATE TABLE cb.tra_faixa_seguranca_a(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_faixa_seguranca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_faixa_seguranca_a_geom ON cb.tra_faixa_seguranca_a USING gist (geom)#

ALTER TABLE cb.tra_faixa_seguranca_a
	 ADD CONSTRAINT tra_faixa_seguranca_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_faixa_seguranca_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_fundeadouro_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 destinacaofundeadouro smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_fundeadouro_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_fundeadouro_a_geom ON cb.tra_fundeadouro_a USING gist (geom)#

ALTER TABLE cb.tra_fundeadouro_a
	 ADD CONSTRAINT tra_fundeadouro_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_a
	 ADD CONSTRAINT tra_fundeadouro_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_fundeadouro_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_a
	 ADD CONSTRAINT tra_fundeadouro_a_destinacaofundeadouro_fk FOREIGN KEY (destinacaofundeadouro)
	 REFERENCES dominios.destinacaofundeadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_a ALTER COLUMN destinacaofundeadouro SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_a
	 ADD CONSTRAINT tra_fundeadouro_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_fundeadouro_l(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 destinacaofundeadouro smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_fundeadouro_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_fundeadouro_l_geom ON cb.tra_fundeadouro_l USING gist (geom)#

ALTER TABLE cb.tra_fundeadouro_l
	 ADD CONSTRAINT tra_fundeadouro_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_l
	 ADD CONSTRAINT tra_fundeadouro_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_fundeadouro_l ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_l
	 ADD CONSTRAINT tra_fundeadouro_l_destinacaofundeadouro_fk FOREIGN KEY (destinacaofundeadouro)
	 REFERENCES dominios.destinacaofundeadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_l ALTER COLUMN destinacaofundeadouro SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_l
	 ADD CONSTRAINT tra_fundeadouro_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_fundeadouro_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 destinacaofundeadouro smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_fundeadouro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_fundeadouro_p_geom ON cb.tra_fundeadouro_p USING gist (geom)#

ALTER TABLE cb.tra_fundeadouro_p
	 ADD CONSTRAINT tra_fundeadouro_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_p
	 ADD CONSTRAINT tra_fundeadouro_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_fundeadouro_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_p
	 ADD CONSTRAINT tra_fundeadouro_p_destinacaofundeadouro_fk FOREIGN KEY (destinacaofundeadouro)
	 REFERENCES dominios.destinacaofundeadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_p ALTER COLUMN destinacaofundeadouro SET DEFAULT 999#

ALTER TABLE cb.tra_fundeadouro_p
	 ADD CONSTRAINT tra_fundeadouro_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_fundeadouro_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_funicular_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_funicular_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_funicular_l_geom ON cb.tra_funicular_l USING gist (geom)#

ALTER TABLE cb.tra_funicular_l
	 ADD CONSTRAINT tra_funicular_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_funicular_l
	 ADD CONSTRAINT tra_funicular_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_funicular_l
	 ADD CONSTRAINT tra_funicular_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_funicular_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_funicular_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_funicular_p_geom ON cb.tra_funicular_p USING gist (geom)#

ALTER TABLE cb.tra_funicular_p
	 ADD CONSTRAINT tra_funicular_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_funicular_p
	 ADD CONSTRAINT tra_funicular_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_funicular_p
	 ADD CONSTRAINT tra_funicular_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_funicular_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_galeria_bueiro_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 pesosuportmaximo real,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_galeria_bueiro_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_galeria_bueiro_l_geom ON cb.tra_galeria_bueiro_l USING gist (geom)#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_galeria_bueiro_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_l
	 ADD CONSTRAINT tra_galeria_bueiro_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_galeria_bueiro_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_galeria_bueiro_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 pesosuportmaximo real,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_galeria_bueiro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_galeria_bueiro_p_geom ON cb.tra_galeria_bueiro_p USING gist (geom)#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_galeria_bueiro_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_galeria_bueiro_p
	 ADD CONSTRAINT tra_galeria_bueiro_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_galeria_bueiro_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_girador_ferroviario_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_girador_ferroviario_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_girador_ferroviario_p_geom ON cb.tra_girador_ferroviario_p USING gist (geom)#

ALTER TABLE cb.tra_girador_ferroviario_p
	 ADD CONSTRAINT tra_girador_ferroviario_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_girador_ferroviario_p
	 ADD CONSTRAINT tra_girador_ferroviario_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_girador_ferroviario_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_girador_ferroviario_p
	 ADD CONSTRAINT tra_girador_ferroviario_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_girador_ferroviario_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_girador_ferroviario_p
	 ADD CONSTRAINT tra_girador_ferroviario_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_girador_ferroviario_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_girador_ferroviario_p
	 ADD CONSTRAINT tra_girador_ferroviario_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_girador_ferroviario_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_identific_trecho_rod_p(
	 id serial NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 sigla varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_identific_trecho_rod_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_identific_trecho_rod_p_geom ON cb.tra_identific_trecho_rod_p USING gist (geom)#

CREATE TABLE cb.tra_local_critico_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipolocalcrit smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_local_critico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_local_critico_a_geom ON cb.tra_local_critico_a USING gist (geom)#

ALTER TABLE cb.tra_local_critico_a
	 ADD CONSTRAINT tra_local_critico_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_local_critico_a
	 ADD CONSTRAINT tra_local_critico_a_tipolocalcrit_fk FOREIGN KEY (tipolocalcrit)
	 REFERENCES dominios.tipolocalcrit (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_a ALTER COLUMN tipolocalcrit SET DEFAULT 999#

CREATE TABLE cb.tra_local_critico_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipolocalcrit smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_local_critico_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_local_critico_l_geom ON cb.tra_local_critico_l USING gist (geom)#

ALTER TABLE cb.tra_local_critico_l
	 ADD CONSTRAINT tra_local_critico_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_local_critico_l
	 ADD CONSTRAINT tra_local_critico_l_tipolocalcrit_fk FOREIGN KEY (tipolocalcrit)
	 REFERENCES dominios.tipolocalcrit (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_l ALTER COLUMN tipolocalcrit SET DEFAULT 999#

CREATE TABLE cb.tra_local_critico_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipolocalcrit smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_local_critico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_local_critico_p_geom ON cb.tra_local_critico_p USING gist (geom)#

ALTER TABLE cb.tra_local_critico_p
	 ADD CONSTRAINT tra_local_critico_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_local_critico_p
	 ADD CONSTRAINT tra_local_critico_p_tipolocalcrit_fk FOREIGN KEY (tipolocalcrit)
	 REFERENCES dominios.tipolocalcrit (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_local_critico_p ALTER COLUMN tipolocalcrit SET DEFAULT 999#

CREATE TABLE cb.tra_obstaculo_navegacao_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 tipoobst smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_obstaculo_navegacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_obstaculo_navegacao_a_geom ON cb.tra_obstaculo_navegacao_a USING gist (geom)#

ALTER TABLE cb.tra_obstaculo_navegacao_a
	 ADD CONSTRAINT tra_obstaculo_navegacao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_a
	 ADD CONSTRAINT tra_obstaculo_navegacao_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_a ALTER COLUMN situacaoemagua SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_a
	 ADD CONSTRAINT tra_obstaculo_navegacao_a_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipoobst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_a ALTER COLUMN tipoobst SET DEFAULT 999#

CREATE TABLE cb.tra_obstaculo_navegacao_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 tipoobst smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_obstaculo_navegacao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_obstaculo_navegacao_l_geom ON cb.tra_obstaculo_navegacao_l USING gist (geom)#

ALTER TABLE cb.tra_obstaculo_navegacao_l
	 ADD CONSTRAINT tra_obstaculo_navegacao_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_l
	 ADD CONSTRAINT tra_obstaculo_navegacao_l_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_l ALTER COLUMN situacaoemagua SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_l
	 ADD CONSTRAINT tra_obstaculo_navegacao_l_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipoobst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_l ALTER COLUMN tipoobst SET DEFAULT 999#

CREATE TABLE cb.tra_obstaculo_navegacao_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 situacaoemagua smallint NOT NULL,
	 tipoobst smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_obstaculo_navegacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_obstaculo_navegacao_p_geom ON cb.tra_obstaculo_navegacao_p USING gist (geom)#

ALTER TABLE cb.tra_obstaculo_navegacao_p
	 ADD CONSTRAINT tra_obstaculo_navegacao_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_p
	 ADD CONSTRAINT tra_obstaculo_navegacao_p_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacaoemagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_p ALTER COLUMN situacaoemagua SET DEFAULT 999#

ALTER TABLE cb.tra_obstaculo_navegacao_p
	 ADD CONSTRAINT tra_obstaculo_navegacao_p_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipoobst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_obstaculo_navegacao_p ALTER COLUMN tipoobst SET DEFAULT 999#

CREATE TABLE cb.tra_passag_elevada_viaduto_l(
	 id serial NOT NULL,
	 cargasuportmaxima real,
	 extensao real,
	 gabhorizsup real,
	 gabvertsup real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopassagviad smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_passag_elevada_viaduto_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passag_elevada_viaduto_l_geom ON cb.tra_passag_elevada_viaduto_l USING gist (geom)#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_l
	 ADD CONSTRAINT tra_passag_elevada_viaduto_l_tipopassagviad_fk FOREIGN KEY (tipopassagviad)
	 REFERENCES dominios.tipopassagviad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_l ALTER COLUMN tipopassagviad SET DEFAULT 999#

CREATE TABLE cb.tra_passag_elevada_viaduto_p(
	 id serial NOT NULL,
	 cargasuportmaxima real,
	 extensao real,
	 gabhorizsup real,
	 gabvertsup real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopassagviad smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_passag_elevada_viaduto_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passag_elevada_viaduto_p_geom ON cb.tra_passag_elevada_viaduto_p USING gist (geom)#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_passag_elevada_viaduto_p
	 ADD CONSTRAINT tra_passag_elevada_viaduto_p_tipopassagviad_fk FOREIGN KEY (tipopassagviad)
	 REFERENCES dominios.tipopassagviad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passag_elevada_viaduto_p ALTER COLUMN tipopassagviad SET DEFAULT 999#

CREATE TABLE cb.tra_passagem_nivel_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_passagem_nivel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passagem_nivel_p_geom ON cb.tra_passagem_nivel_p USING gist (geom)#

ALTER TABLE cb.tra_passagem_nivel_p
	 ADD CONSTRAINT tra_passagem_nivel_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_passagem_nivel_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_patio_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_patio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_patio_a_geom ON cb.tra_patio_a USING gist (geom)#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_patio_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 14 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_patio_a ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_patio_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_patio_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_patio_p_geom ON cb.tra_patio_p USING gist (geom)#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_patio_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 14 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_patio_p ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_patio_p
	 ADD CONSTRAINT tra_patio_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_patio_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_pista_ponto_pouso_a(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 largura real,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopista smallint NOT NULL,
	 usopista smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_pista_ponto_pouso_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_pista_ponto_pouso_a_geom ON cb.tra_pista_ponto_pouso_a USING gist (geom)#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.homologacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN homologacao SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_tipopista_check 
	 CHECK (tipopista = ANY(ARRAY[9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN tipopista SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_a
	 ADD CONSTRAINT tra_pista_ponto_pouso_a_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.usopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_a ALTER COLUMN usopista SET DEFAULT 999#

CREATE TABLE cb.tra_pista_ponto_pouso_l(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 largura real,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopista smallint NOT NULL,
	 usopista smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_pista_ponto_pouso_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_pista_ponto_pouso_l_geom ON cb.tra_pista_ponto_pouso_l USING gist (geom)#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.homologacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN homologacao SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_tipopista_check 
	 CHECK (tipopista = ANY(ARRAY[9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN tipopista SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_l
	 ADD CONSTRAINT tra_pista_ponto_pouso_l_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.usopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_l ALTER COLUMN usopista SET DEFAULT 999#

CREATE TABLE cb.tra_pista_ponto_pouso_p(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 largura real,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipopista smallint NOT NULL,
	 usopista smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_pista_ponto_pouso_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_pista_ponto_pouso_p_geom ON cb.tra_pista_ponto_pouso_p USING gist (geom)#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.homologacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN homologacao SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_tipopista_check 
	 CHECK (tipopista = ANY(ARRAY[9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN tipopista SET DEFAULT 999#

ALTER TABLE cb.tra_pista_ponto_pouso_p
	 ADD CONSTRAINT tra_pista_ponto_pouso_p_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.usopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_pista_ponto_pouso_p ALTER COLUMN usopista SET DEFAULT 999#

CREATE TABLE cb.tra_ponte_l(
	 id serial NOT NULL,
	 cargasuportmaxima real,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoponte smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_ponte_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponte_l_geom ON cb.tra_ponte_l USING gist (geom)#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_ponte_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_ponte_l ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_tipoponte_fk FOREIGN KEY (tipoponte)
	 REFERENCES dominios.tipoponte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_l ALTER COLUMN tipoponte SET DEFAULT 999#

CREATE TABLE cb.tra_ponte_p(
	 id serial NOT NULL,
	 cargasuportmaxima real,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipoponte smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_ponte_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponte_p_geom ON cb.tra_ponte_p USING gist (geom)#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_ponte_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_ponte_p ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_tipoponte_fk FOREIGN KEY (tipoponte)
	 REFERENCES dominios.tipoponte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponte_p ALTER COLUMN tipoponte SET DEFAULT 999#

CREATE TABLE cb.tra_ponto_duto_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 relacionado smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_ponto_duto_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponto_duto_p_geom ON cb.tra_ponto_duto_p USING gist (geom)#

ALTER TABLE cb.tra_ponto_duto_p
	 ADD CONSTRAINT tra_ponto_duto_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_duto_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ponto_duto_p
	 ADD CONSTRAINT tra_ponto_duto_p_relacionado_fk FOREIGN KEY (relacionado)
	 REFERENCES dominios.relacionado_dut (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_duto_p ALTER COLUMN relacionado SET DEFAULT 999#

CREATE TABLE cb.tra_ponto_rodoviario_ferrov_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 relacionado smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_ponto_rodoviario_ferrov_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponto_rodoviario_ferrov_p_geom ON cb.tra_ponto_rodoviario_ferrov_p USING gist (geom)#

ALTER TABLE cb.tra_ponto_rodoviario_ferrov_p
	 ADD CONSTRAINT tra_ponto_rodoviario_ferrov_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_rodoviario_ferrov_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ponto_rodoviario_ferrov_p
	 ADD CONSTRAINT tra_ponto_rodoviario_ferrov_p_relacionado_fk FOREIGN KEY (relacionado)
	 REFERENCES dominios.relacionado_fer_rod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_rodoviario_ferrov_p ALTER COLUMN relacionado SET DEFAULT 999#

CREATE TABLE cb.tra_ponto_hidroviario_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 relacionado smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_ponto_hidroviario_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponto_hidroviario_p_geom ON cb.tra_ponto_hidroviario_p USING gist (geom)#

ALTER TABLE cb.tra_ponto_hidroviario_p
	 ADD CONSTRAINT tra_ponto_hidroviario_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_hidroviario_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_ponto_hidroviario_p
	 ADD CONSTRAINT tra_ponto_hidroviario_p_relacionado_fk FOREIGN KEY (relacionado)
	 REFERENCES dominios.relacionado_hdr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_ponto_hidroviario_p ALTER COLUMN relacionado SET DEFAULT 999#

CREATE TABLE cb.tra_posto_combustivel_a(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_posto_combustivel_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_posto_combustivel_a_geom ON cb.tra_posto_combustivel_a USING gist (geom)#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_a ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_a ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_a ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_a
	 ADD CONSTRAINT tra_posto_combustivel_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_a ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_posto_combustivel_p(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_posto_combustivel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_posto_combustivel_p_geom ON cb.tra_posto_combustivel_p USING gist (geom)#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_p ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_posto_combustivel_p
	 ADD CONSTRAINT tra_posto_combustivel_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_posto_combustivel_p ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_sinalizacao_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tiposinal smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_sinalizacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_sinalizacao_p_geom ON cb.tra_sinalizacao_p USING gist (geom)#

ALTER TABLE cb.tra_sinalizacao_p
	 ADD CONSTRAINT tra_sinalizacao_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_sinalizacao_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_sinalizacao_p
	 ADD CONSTRAINT tra_sinalizacao_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_sinalizacao_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_sinalizacao_p
	 ADD CONSTRAINT tra_sinalizacao_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_sinalizacao_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_sinalizacao_p
	 ADD CONSTRAINT tra_sinalizacao_p_tiposinal_fk FOREIGN KEY (tiposinal)
	 REFERENCES dominios.tiposinal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_sinalizacao_p ALTER COLUMN tiposinal SET DEFAULT 999#

CREATE TABLE cb.tra_travessia_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipotravessia smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_travessia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_l_geom ON cb.tra_travessia_l USING gist (geom)#

ALTER TABLE cb.tra_travessia_l
	 ADD CONSTRAINT tra_travessia_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_l
	 ADD CONSTRAINT tra_travessia_l_tipotravessia_fk FOREIGN KEY (tipotravessia)
	 REFERENCES dominios.tipotravessia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_l ALTER COLUMN tipotravessia SET DEFAULT 999#

CREATE TABLE cb.tra_travessia_p(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipotravessia smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_travessia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_p_geom ON cb.tra_travessia_p USING gist (geom)#

ALTER TABLE cb.tra_travessia_p
	 ADD CONSTRAINT tra_travessia_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_p
	 ADD CONSTRAINT tra_travessia_p_tipotravessia_fk FOREIGN KEY (tipotravessia)
	 REFERENCES dominios.tipotravessia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_p ALTER COLUMN tipotravessia SET DEFAULT 999#

CREATE TABLE cb.tra_travessia_pedestre_l(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotravessiaped smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_travessia_pedestre_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_pedestre_l_geom ON cb.tra_travessia_pedestre_l USING gist (geom)#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_travessia_pedestre_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_travessia_pedestre_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_tipotravessiaped_fk FOREIGN KEY (tipotravessiaped)
	 REFERENCES dominios.tipotravessiaped (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_l ALTER COLUMN tipotravessiaped SET DEFAULT 999#

CREATE TABLE cb.tra_travessia_pedestre_p(
	 id serial NOT NULL,
	 extensao real,
	 geometriaaproximada smallint NOT NULL,
	 largura real,
	 matconstr smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotravessiaped smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_travessia_pedestre_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_pedestre_p_geom ON cb.tra_travessia_pedestre_p USING gist (geom)#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_travessia_pedestre_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_travessia_pedestre_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_tipotravessiaped_fk FOREIGN KEY (tipotravessiaped)
	 REFERENCES dominios.tipotravessiaped (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_travessia_pedestre_p ALTER COLUMN tipotravessiaped SET DEFAULT 999#

CREATE TABLE cb.tra_trecho_duto_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 mattransp smallint NOT NULL,
	 nrdutos integer,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 setor smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotrechoduto smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trecho_duto_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trecho_duto_l_geom ON cb.tra_trecho_duto_l USING gist (geom)#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_mattransp_fk FOREIGN KEY (mattransp)
	 REFERENCES dominios.mattransp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN mattransp SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicaorelativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN posicaorelativa SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_setor_fk FOREIGN KEY (setor)
	 REFERENCES dominios.setor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN setor SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacaoespacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN situacaoespacial SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_duto_l
	 ADD CONSTRAINT tra_trecho_duto_l_tipotrechoduto_fk FOREIGN KEY (tipotrechoduto)
	 REFERENCES dominios.tipotrechoduto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_duto_l ALTER COLUMN tipotrechoduto SET DEFAULT 999#

CREATE TABLE cb.tra_trecho_ferroviario_l(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 bitola smallint NOT NULL,
	 cargasuportmaxima real,
	 codtrechoferrov varchar(255),
	 concessionaria varchar(255),
	 eletrificada smallint NOT NULL,
	 emarruamento smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrlinhas smallint NOT NULL,
	 operacional smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotrechoferrov smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trecho_ferroviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trecho_ferroviario_l_geom ON cb.tra_trecho_ferroviario_l USING gist (geom)#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 97 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_bitola_fk FOREIGN KEY (bitola)
	 REFERENCES dominios.bitola (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN bitola SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_eletrificada_fk FOREIGN KEY (eletrificada)
	 REFERENCES dominios.eletrificada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN eletrificada SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_emarruamento_fk FOREIGN KEY (emarruamento)
	 REFERENCES dominios.emarruamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN emarruamento SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN jurisdicao SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_nrlinhas_fk FOREIGN KEY (nrlinhas)
	 REFERENCES dominios.nrlinhas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN nrlinhas SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicaorelativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_posicaorelativa_check 
	 CHECK (posicaorelativa = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN posicaorelativa SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_ferroviario_l
	 ADD CONSTRAINT tra_trecho_ferroviario_l_tipotrechoferrov_fk FOREIGN KEY (tipotrechoferrov)
	 REFERENCES dominios.tipotrechoferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_ferroviario_l ALTER COLUMN tipotrechoferrov SET DEFAULT 999#

CREATE TABLE cb.tra_trecho_hidroviario_l(
	 id serial NOT NULL,
	 caladomaxseca real,
	 extensaotrecho real,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 operacional smallint NOT NULL,
	 regime smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trecho_hidroviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trecho_hidroviario_l_geom ON cb.tra_trecho_hidroviario_l USING gist (geom)#

ALTER TABLE cb.tra_trecho_hidroviario_l
	 ADD CONSTRAINT tra_trecho_hidroviario_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_hidroviario_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_hidroviario_l
	 ADD CONSTRAINT tra_trecho_hidroviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_hidroviario_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_hidroviario_l
	 ADD CONSTRAINT tra_trecho_hidroviario_l_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_hidroviario_l
	 ADD CONSTRAINT tra_trecho_hidroviario_l_regime_check 
	 CHECK (regime = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 6 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_hidroviario_l ALTER COLUMN regime SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_hidroviario_l
	 ADD CONSTRAINT tra_trecho_hidroviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_hidroviario_l ALTER COLUMN situacaofisica SET DEFAULT 999#

CREATE TABLE cb.tra_trecho_rodoviario_l(
	 id serial NOT NULL,
	 administracao smallint NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 capaccarga real,
	 codtrechorodov varchar(255),
	 concessionaria varchar(255),
	 geometriaaproximada smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotrechorod smallint NOT NULL,
	 trafego smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trecho_rodoviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trecho_rodoviario_l_geom ON cb.tra_trecho_rodoviario_l USING gist (geom)#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN administracao SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.canteirodivisorio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN canteirodivisorio SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 8 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN jurisdicao SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN revestimento SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_tipotrechorod_fk FOREIGN KEY (tipotrechorod)
	 REFERENCES dominios.tipotrechorod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN tipotrechorod SET DEFAULT 999#

ALTER TABLE cb.tra_trecho_rodoviario_l
	 ADD CONSTRAINT tra_trecho_rodoviario_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trecho_rodoviario_l ALTER COLUMN trafego SET DEFAULT 999#

CREATE TABLE cb.tra_trilha_picada_l(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trilha_picada_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trilha_picada_l_geom ON cb.tra_trilha_picada_l USING gist (geom)#

ALTER TABLE cb.tra_trilha_picada_l
	 ADD CONSTRAINT tra_trilha_picada_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_trilha_picada_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.tra_tunel_l(
	 id serial NOT NULL,
	 altura real,
	 extensao real,
	 largura real,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotunel smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_tunel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_tunel_l_geom ON cb.tra_tunel_l USING gist (geom)#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_tunel_l ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_tunel_l ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_tipotunel_fk FOREIGN KEY (tipotunel)
	 REFERENCES dominios.tipotunel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_l ALTER COLUMN tipotunel SET DEFAULT 999#

CREATE TABLE cb.tra_tunel_p(
	 id serial NOT NULL,
	 altura real,
	 extensao real,
	 largura real,
	 geometriaaproximada smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 modaluso smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 nrfaixas integer,
	 nrpistas integer,
	 operacional smallint NOT NULL,
	 posicaopista smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipotunel smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_tunel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_tunel_p_geom ON cb.tra_tunel_p USING gist (geom)#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.matconstr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 99 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_tunel_p ALTER COLUMN matconstr SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modaluso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.tra_tunel_p ALTER COLUMN modaluso SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.operacional (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p ALTER COLUMN operacional SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.posicaopista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p ALTER COLUMN posicaopista SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacaofisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p ALTER COLUMN situacaofisica SET DEFAULT 999#

ALTER TABLE cb.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_tipotunel_fk FOREIGN KEY (tipotunel)
	 REFERENCES dominios.tipotunel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.tra_tunel_p ALTER COLUMN tipotunel SET DEFAULT 999#

CREATE TABLE cb.veg_brejo_pantano_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipobrejopantano smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_brejo_pantano_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_brejo_pantano_a_geom ON cb.veg_brejo_pantano_a USING gist (geom)#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_brejo_pantano_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_brejo_pantano_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_brejo_pantano_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_brejo_pantano_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_tipobrejopantano_fk FOREIGN KEY (tipobrejopantano)
	 REFERENCES dominios.tipobrejopantano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_brejo_pantano_a ALTER COLUMN tipobrejopantano SET DEFAULT 999#

CREATE TABLE cb.veg_caatinga_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_caatinga_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_caatinga_a_geom ON cb.veg_caatinga_a USING gist (geom)#

ALTER TABLE cb.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_caatinga_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_caatinga_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_caatinga_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_caatinga_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_campinarana_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_campinarana_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_campinarana_a_geom ON cb.veg_campinarana_a USING gist (geom)#

ALTER TABLE cb.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campinarana_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_campinarana_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campinarana_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campinarana_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_campo_a(
	 id serial NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 ocorrenciaem smallint NOT NULL,
	 tipocampo smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_campo_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_campo_a_geom ON cb.veg_campo_a USING gist (geom)#

ALTER TABLE cb.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campo_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_ocorrenciaem_fk FOREIGN KEY (ocorrenciaem)
	 REFERENCES dominios.ocorrenciaem (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campo_a ALTER COLUMN ocorrenciaem SET DEFAULT 999#

ALTER TABLE cb.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_tipocampo_fk FOREIGN KEY (tipocampo)
	 REFERENCES dominios.tipocampo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_campo_a ALTER COLUMN tipocampo SET DEFAULT 999#

CREATE TABLE cb.veg_cerrado_cerradao_a(
	 id serial NOT NULL,
	 antropizada smallint NOT NULL,
	 alturamediaindividuos real,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipocerr smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_cerrado_cerradao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_cerrado_cerradao_a_geom ON cb.veg_cerrado_cerradao_a USING gist (geom)#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_cerrado_cerradao_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_cerrado_cerradao_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_cerrado_cerradao_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_cerrado_cerradao_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.veg_cerrado_cerradao_a
	 ADD CONSTRAINT veg_cerrado_cerradao_a_tipocerr_fk FOREIGN KEY (tipocerr)
	 REFERENCES dominios.tipocerr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_cerrado_cerradao_a ALTER COLUMN tipocerr SET DEFAULT 999#

CREATE TABLE cb.veg_descontinuidade_geometrica_a(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_descontinuidade_geometrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_descontinuidade_geometrica_a_geom ON cb.veg_descontinuidade_geometrica_a USING gist (geom)#

ALTER TABLE cb.veg_descontinuidade_geometrica_a
	 ADD CONSTRAINT veg_descontinuidade_geometrica_a_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_descontinuidade_geometrica_a ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.veg_descontinuidade_geometrica_l(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT veg_descontinuidade_geometrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_descontinuidade_geometrica_l_geom ON cb.veg_descontinuidade_geometrica_l USING gist (geom)#

ALTER TABLE cb.veg_descontinuidade_geometrica_l
	 ADD CONSTRAINT veg_descontinuidade_geometrica_l_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_descontinuidade_geometrica_l ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.veg_descontinuidade_geometrica_p(
	 id serial NOT NULL,
	 motivodescontinuidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT veg_descontinuidade_geometrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_descontinuidade_geometrica_p_geom ON cb.veg_descontinuidade_geometrica_p USING gist (geom)#

ALTER TABLE cb.veg_descontinuidade_geometrica_p
	 ADD CONSTRAINT veg_descontinuidade_geometrica_p_motivodescontinuidade_fk FOREIGN KEY (motivodescontinuidade)
	 REFERENCES dominios.motivodescontinuidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_descontinuidade_geometrica_p ALTER COLUMN motivodescontinuidade SET DEFAULT 999#

CREATE TABLE cb.veg_estepe_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_estepe_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_estepe_a_geom ON cb.veg_estepe_a USING gist (geom)#

ALTER TABLE cb.veg_estepe_a
	 ADD CONSTRAINT veg_estepe_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_estepe_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_estepe_a
	 ADD CONSTRAINT veg_estepe_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_estepe_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_estepe_a
	 ADD CONSTRAINT veg_estepe_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_estepe_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_floresta_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 caracteristicafloresta smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 especiepredominante smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_floresta_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_floresta_a_geom ON cb.veg_floresta_a USING gist (geom)#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_caracteristicafloresta_fk FOREIGN KEY (caracteristicafloresta)
	 REFERENCES dominios.caracteristicafloresta (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a ALTER COLUMN caracteristicafloresta SET DEFAULT 999#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_floresta_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_especiepredominante_fk FOREIGN KEY (especiepredominante)
	 REFERENCES dominios.especiepredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a ALTER COLUMN especiepredominante SET DEFAULT 999#

ALTER TABLE cb.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_floresta_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_macega_chavascal_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 tipomacchav smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_macega_chavascal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_macega_chavascal_a_geom ON cb.veg_macega_chavascal_a USING gist (geom)#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_macega_chavascal_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_macega_chavascal_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_macega_chavascal_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_macega_chavascal_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.veg_macega_chavascal_a
	 ADD CONSTRAINT veg_macega_chavascal_a_tipomacchav_fk FOREIGN KEY (tipomacchav)
	 REFERENCES dominios.tipomacchav (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_macega_chavascal_a ALTER COLUMN tipomacchav SET DEFAULT 999#

CREATE TABLE cb.veg_mangue_a(
	 id serial NOT NULL,
	 antropizada smallint NOT NULL,
	 alturamediaindividuos real,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_mangue_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_mangue_a_geom ON cb.veg_mangue_a USING gist (geom)#

ALTER TABLE cb.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_mangue_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_mangue_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_mangue_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_mangue_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_veg_area_contato_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_area_contato_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_area_contato_a_geom ON cb.veg_veg_area_contato_a USING gist (geom)#

ALTER TABLE cb.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_area_contato_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_veg_area_contato_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_area_contato_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_area_contato_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.veg_veg_cultivada_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 classificacaoporte smallint NOT NULL,
	 cultivopredominante smallint NOT NULL,
	 denso smallint NOT NULL,
	 espacamentoindividuos real,
	 espessuradap real,
	 finalidade smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 terreno smallint NOT NULL,
	 tipolavoura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_cultivada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_cultivada_a_geom ON cb.veg_veg_cultivada_a USING gist (geom)#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_cultivopredominante_fk FOREIGN KEY (cultivopredominante)
	 REFERENCES dominios.cultivopredominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN cultivopredominante SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_veg (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN finalidade SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_terreno_fk FOREIGN KEY (terreno)
	 REFERENCES dominios.terreno (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN terreno SET DEFAULT 999#

ALTER TABLE cb.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_tipolavoura_fk FOREIGN KEY (tipolavoura)
	 REFERENCES dominios.tipolavoura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_cultivada_a ALTER COLUMN tipolavoura SET DEFAULT 999#

CREATE TABLE cb.veg_veg_restinga_a(
	 id serial NOT NULL,
	 alturamediaindividuos real,
	 antropizada smallint NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 denso smallint NOT NULL,
	 geometriaaproximada smallint NOT NULL,
	 nome varchar(255),
	 nomeabrev varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_restinga_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_restinga_a_geom ON cb.veg_veg_restinga_a USING gist (geom)#

ALTER TABLE cb.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.antropizada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_restinga_a ALTER COLUMN antropizada SET DEFAULT 999#

ALTER TABLE cb.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacaoporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 98 :: SMALLINT, 999 :: SMALLINT]))# 
ALTER TABLE cb.veg_veg_restinga_a ALTER COLUMN classificacaoporte SET DEFAULT 999#

ALTER TABLE cb.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_denso_fk FOREIGN KEY (denso)
	 REFERENCES dominios.denso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_restinga_a ALTER COLUMN denso SET DEFAULT 999#

ALTER TABLE cb.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_geometriaaproximada_fk FOREIGN KEY (geometriaaproximada)
	 REFERENCES dominios.geometriaaproximada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE cb.veg_veg_restinga_a ALTER COLUMN geometriaaproximada SET DEFAULT 999#

CREATE TABLE cb.aux_objeto_desconhecido_a(
	 id serial NOT NULL,
	 classe varchar(255),
	 descricao varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_objeto_desconhecido_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_objeto_desconhecido_a_geom ON cb.aux_objeto_desconhecido_a USING gist (geom)#

CREATE TABLE cb.aux_objeto_desconhecido_l(
	 id serial NOT NULL,
	 classe varchar(255),
	 descricao varchar(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT aux_objeto_desconhecido_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_objeto_desconhecido_l_geom ON cb.aux_objeto_desconhecido_l USING gist (geom)#

CREATE TABLE cb.aux_objeto_desconhecido_p(
	 id serial NOT NULL,
	 classe varchar(255),
	 descricao varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT aux_objeto_desconhecido_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_objeto_desconhecido_p_geom ON cb.aux_objeto_desconhecido_p USING gist (geom)#

CREATE TABLE cb.aux_moldura_a(
	 id serial NOT NULL,
	 escala varchar(255),
	 inom varchar(255),
	 mi varchar(255),
	 nome varchar(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_moldura_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_moldura_a_geom ON cb.aux_moldura_a USING gist (geom)#
