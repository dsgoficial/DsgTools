CREATE SCHEMA edgv#
CREATE SCHEMA dominios#

CREATE EXTENSION postgis#
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"#
SET search_path TO pg_catalog,public,edgv,dominios#

CREATE TABLE public.db_metadata(
	 edgvversion varchar(50) NOT NULL DEFAULT 'EDGV 3.0 Orto',
	 dbimplversion varchar(50) NOT NULL DEFAULT '2.4.0',
	 CONSTRAINT edgvversioncheck CHECK (edgvversion = 'EDGV 3.0 Orto')
)#
INSERT INTO public.db_metadata (edgvversion, dbimplversion) VALUES ('EDGV 3.0 Orto','2.4.0')#

CREATE TABLE dominios.tipo_produto_residuo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_produto_residuo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (3,'Petróleo (3)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (5,'Gás (5)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (18,'Cascalho (18)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (22,'Pedra (brita) (22)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (23,'Granito (23)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (24,'Mármore (24)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (25,'Bauxita (25)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (26,'Manganês (26)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (27,'Talco (27)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (32,'Cobre (32)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (33,'Carvão mineral (33)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (34,'Sal (34)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (35,'Ferro (35)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (37,'Ouro (37)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (38,'Diamante (38)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (39,'Prata (39)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (40,'Pedra preciosa (40)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (42,'Areia (42)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (43,'Saibro/piçarra (43)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (45,'Ágata (45)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (47,'Água marinha (47)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (48,'Água mineral (48)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (49,'Alexandrita (49)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (50,'Ametista (50)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (51,'Amianto (51)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (52,'Argila (52)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (53,'Barita (53)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (54,'Bentonita (54)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (55,'Calcário (55)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (56,'Carvão vegetal (56)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (57,'Caulim (57)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (59,'Chumbo (59)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (60,'Citrino (60)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (61,'Crisoberilo (61)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (62,'Cristal de rocha (62)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (63,'Cromo (63)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (64,'Diatomita (64)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (65,'Dolomito (65)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (67,'Esmeralda (67)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (68,'Estanho (68)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (69,'Feldspato (69)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (70,'Fosfato (70)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (71,'Gipsita (71)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (72,'Grafita (72)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (73,'Granada (73)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (74,'Lítio (74)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (78,'Magnesita (78)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (79,'Mica (79)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (80,'Nióbio (80)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (81,'Níquel (81)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (82,'Opala (82)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (83,'Rocha ornamental (83)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (84,'Sal-gema (84)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (85,'Terras raras (85)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (86,'Titânio (86)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (87,'Topázio (87)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (88,'Tório (88)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (89,'Tungstênio (89)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (90,'Turfa (90)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (91,'Turmalina (91)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (92,'Urânio (92)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (93,'Vermiculita (93)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (94,'Zinco (94)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (99,'Outros (99)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (100,'Zircônio (100)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_produto_residuo OWNER TO postgres#

CREATE TABLE dominios.auxiliar (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT auxiliar_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.auxiliar (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (1,'Sim (1)')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (2,'Não (2)')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.auxiliar OWNER TO postgres#

CREATE TABLE dominios.posicao_rotulo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicao_rotulo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicao_rotulo (code,code_name) VALUES (1,'Na linha (1)')#
INSERT INTO dominios.posicao_rotulo (code,code_name) VALUES (2,'Acima da linha (2)')#
INSERT INTO dominios.posicao_rotulo (code,code_name) VALUES (3,'Abaixo da linha (3)')#
INSERT INTO dominios.posicao_rotulo (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.posicao_rotulo OWNER TO postgres#

CREATE TABLE dominios.justificativa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT justificativa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.justificativa (code,code_name) VALUES (1,'Esquerda (1)')#
INSERT INTO dominios.justificativa (code,code_name) VALUES (2,'Centro (2)')#
INSERT INTO dominios.justificativa (code,code_name) VALUES (3,'Direita (3)')#
INSERT INTO dominios.justificativa (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.justificativa OWNER TO postgres#

CREATE TABLE dominios.ancora_horizontal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT ancora_horizontal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.ancora_horizontal (code,code_name) VALUES (1,'Esquerda (1)')#
INSERT INTO dominios.ancora_horizontal (code,code_name) VALUES (2,'Centro (2)')#
INSERT INTO dominios.ancora_horizontal (code,code_name) VALUES (3,'Direita (3)')#
INSERT INTO dominios.ancora_horizontal (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.ancora_horizontal OWNER TO postgres#

CREATE TABLE dominios.ancora_vertical (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT ancora_vertical_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.ancora_vertical (code,code_name) VALUES (1,'Inferior (1)')#
INSERT INTO dominios.ancora_vertical (code,code_name) VALUES (2,'Meio (2)')#
INSERT INTO dominios.ancora_vertical (code,code_name) VALUES (3,'Superior (3)')#
INSERT INTO dominios.ancora_vertical (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.ancora_vertical OWNER TO postgres#

CREATE TABLE dominios.material_construcao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT material_construcao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.material_construcao (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (1,'Alvenaria (1)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (2,'Concreto (2)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (3,'Metal (3)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (4,'Rocha (4)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (5,'Madeira (5)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (9,'Fibra (9)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (23,'Terra (23)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (97,'Não aplicável (97)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (98,'Outros (98)')#
INSERT INTO dominios.material_construcao (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.material_construcao OWNER TO postgres#

CREATE TABLE dominios.tipo_barragem (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_barragem_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_barragem (code,code_name) VALUES (1,'Barragem (1)')#
INSERT INTO dominios.tipo_barragem (code,code_name) VALUES (2,'Dique (2)')#
INSERT INTO dominios.tipo_barragem (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_barragem OWNER TO postgres#

CREATE TABLE dominios.tipo_extracao_mineral (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_extracao_mineral_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (1,'Poço / Água subterrânea (1)')#
INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (4,'Mina / Pedreira (4)')#
INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (5,'Garimpo (5)')#
INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (6,'Salina (6)')#
INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (8,'Poço / Petróleo (8)')#
INSERT INTO dominios.tipo_extracao_mineral (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_extracao_mineral OWNER TO postgres#

CREATE TABLE dominios.tipo_ilha (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ilha_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (1,'Fluvial (1)')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (2,'Marítima (2)')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (3,'Lacustre (3)')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_ilha OWNER TO postgres#

CREATE TABLE dominios.tipo_toponimo_fisiografico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_toponimo_fisiografico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (1,'Serra (1)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (2,'Morro (2)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (3,'Montanha (3)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (4,'Chapada (4)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (5,'Maciço (5)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (6,'Planalto (6)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (7,'Planície (7)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (9,'Península (9)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (10,'Ponta (10)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (11,'Cabo (11)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (12,'Praia (12)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (17,'Pico (17)')#
INSERT INTO dominios.tipo_toponimo_fisiografico (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_toponimo_fisiografico OWNER TO postgres#

CREATE TABLE dominios.tipo_elemento_hidrografico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_elemento_hidrografico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (6,'Foz marítima (6)')#
INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (9,'Cachoeira (9)')#
INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (10,'Salto (10)')#
INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (11,'Catarata (11)')#
INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (12,'Corredeira (12)')#
INSERT INTO dominios.tipo_elemento_hidrografico (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_elemento_hidrografico OWNER TO postgres#

CREATE TABLE dominios.forma_extracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT forma_extracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.forma_extracao (code,code_name) VALUES (5,'A céu aberto (5)')#
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (6,'Subterrânea (6)')#
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.forma_extracao OWNER TO postgres#

CREATE TABLE dominios.situacao_fisica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_fisica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (0,'Desconhecida (0)')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (1,'Abandonada (1)')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (2,'Destruída (2)')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (3,'Construída (3)')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (4,'Em construção (4)')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.situacao_fisica OWNER TO postgres#

CREATE TABLE dominios.tipo_elemento_energia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_elemento_energia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (303,'Linha de transmissão de energia (303)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (405,'Estação geradora – Eólica (405)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (408,'Estação geradora – Hidrelétrica (408)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (407,'Estação geradora – Maré-motriz (407)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (498,'Estação geradora – Outras (498)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (406,'Estação geradora – Solar (406)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (409,'Estação geradora – Termelétrica (409)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (1801,'Subestação de transmissão de energia elétrica (1801)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (1802,'Subestação de distribuição de energia elétrica (1802)')#
INSERT INTO dominios.tipo_elemento_energia (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_elemento_energia OWNER TO postgres#

CREATE TABLE dominios.bitola (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT bitola_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.bitola (code,code_name) VALUES (0,'Desconhecida (0)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (1,'Métrica (1)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (2,'Internacional (2)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (3,'Larga (3)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (4,'Mista métrica internacional (4)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (5,'Mista métrica larga (5)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (6,'Mista internacional larga (6)')#
INSERT INTO dominios.bitola (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.bitola OWNER TO postgres#

CREATE TABLE dominios.tipo_massa_dagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_massa_dagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (1,'Rio (com fluxo) (1)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (2,'Canal (com fluxo) (2)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (3,'Oceano (sem fluxo) (3)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (4,'Baía (sem fluxo) (4)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (5,'Enseada (sem fluxo) (5)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (6,'Meando Abandonado (sem fluxo) (6)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (7,'Lago ou Lagoa (sem fluxo) (7)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (9,'Laguna (com fluxo) (9)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (10,'Represa/açude com fluxo (10)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (11,'Represa/açude sem fluxo (11)')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_massa_dagua OWNER TO postgres#

CREATE TABLE dominios.regime (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT regime_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.regime (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.regime (code,code_name) VALUES (1,'Permanente (1)')#
INSERT INTO dominios.regime (code,code_name) VALUES (3,'Temporário (3)')#
INSERT INTO dominios.regime (code,code_name) VALUES (5,'Seco (5)')#
INSERT INTO dominios.regime (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.regime OWNER TO postgres#

CREATE TABLE dominios.tipo_trecho_drenagem (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_trecho_drenagem_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (1,'Rio (1)')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (2,'Canal (2)')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (3,'Trecho pluvial (3)')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (4,'Canal encoberto (4)')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (5,'Canal não operacional (5)')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_trecho_drenagem OWNER TO postgres#

CREATE TABLE dominios.situacao_em_poligono (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_em_poligono_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_em_poligono (code,code_name) VALUES (1,'Fora de polígono (1)')#
INSERT INTO dominios.situacao_em_poligono (code,code_name) VALUES (2,'Dentro de polígono - Trecho principal (2)')#
INSERT INTO dominios.situacao_em_poligono (code,code_name) VALUES (3,'Dentro de polígono - Trecho secundário (3)')#
INSERT INTO dominios.situacao_em_poligono (code,code_name) VALUES (4,'Dentro de polígono - Trecho compartilhado (4)')#
INSERT INTO dominios.situacao_em_poligono (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.situacao_em_poligono OWNER TO postgres#

CREATE TABLE dominios.tipo_limite_especial (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_limite_especial_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (2,'Terra indígena (2)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (5,'Unidade de Conservação (5)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (24,'Área de Proteção Ambiental – APA (24)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (25,'Área de Relevante Interesse Ecológico – ARIE (25)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (26,'Floresta – FLO (26)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (27,'Reserva de Desenvolvimento Sustentável – RDS (27)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (28,'Reserva Extrativista – RESEX (28)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (29,'Reserva de Fauna – REFAU (29)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (30,'Reserva Particular do Patrimônio Natural – RPPN (30)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (31,'Estação Ecológica – ESEC (31)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (32,'Parque – PAR (32)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (33,'Monumento Natural – MONA (33)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (34,'Reserva Biológica – REBIO (34)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (35,'Refúgio de Vida Silvestre – RVS (35)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (36,'Área militar (36)')#
INSERT INTO dominios.tipo_limite_especial (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_limite_especial OWNER TO postgres#

CREATE TABLE dominios.booleano (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT booleano_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.booleano (code,code_name) VALUES (1,'Sim (1)')#
INSERT INTO dominios.booleano (code,code_name) VALUES (2,'Não (2)')#
INSERT INTO dominios.booleano (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.booleano OWNER TO postgres#

CREATE TABLE dominios.tipo_localidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_localidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (1,'Cidade (1)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (2,'Capital estadual (2)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (3,'Capital federal (3)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (4,'Vila (4)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (5,'Aglomerado rural isolado – Núcleo (5)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (6,'Aglomerado rural isolado – Povoado (6)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (7,'Outros aglomerados rurais – Lugarejo (7)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (8,'Nome local (8)')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_localidade OWNER TO postgres#

CREATE TABLE dominios.uso_pista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT uso_pista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.uso_pista (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (6,'Particular (6)')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (11,'Público (11)')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (12,'Militar (12)')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (13,'Público/Militar (13)')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.uso_pista OWNER TO postgres#

CREATE TABLE dominios.indice (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT indice_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.indice (code,code_name) VALUES (1,'Mestra (1)')#
INSERT INTO dominios.indice (code,code_name) VALUES (2,'Normal (2)')#
INSERT INTO dominios.indice (code,code_name) VALUES (3,'Auxiliar (3)')#
INSERT INTO dominios.indice (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.indice OWNER TO postgres#

CREATE TABLE dominios.tipo_pista_pouso (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pista_pouso_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pista_pouso (code,code_name) VALUES (9,'Pista de pouso (9)')#
INSERT INTO dominios.tipo_pista_pouso (code,code_name) VALUES (10,'Pista de táxi (10)')#
INSERT INTO dominios.tipo_pista_pouso (code,code_name) VALUES (11,'Heliponto (11)')#
INSERT INTO dominios.tipo_pista_pouso (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_pista_pouso OWNER TO postgres#

CREATE TABLE dominios.revestimento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT revestimento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.revestimento (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (1,'Leito natural (1)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (2,'Revestimento primário (solto) (2)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (3,'Pavimentado (3)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (4,'Calçado (4)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.revestimento OWNER TO postgres#

CREATE TABLE dominios.tipo_limite_legal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_limite_legal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_limite_legal (code,code_name) VALUES (1,'Limite Internacional (1)')#
INSERT INTO dominios.tipo_limite_legal (code,code_name) VALUES (2,'Limite Estadual (2)')#
INSERT INTO dominios.tipo_limite_legal (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_limite_legal OWNER TO postgres#

CREATE TABLE dominios.posicao_relativa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicao_relativa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (2,'Superfície (2)')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (3,'Elevado (3)')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (6,'Subterrâneo (6)')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.posicao_relativa OWNER TO postgres#

CREATE TABLE dominios.jurisdicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT jurisdicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.jurisdicao (code,code_name) VALUES (0,'Desconhecida (0)')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (1,'Federal (1)')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (2,'Estadual (2)')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (3,'Municipal (3)')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (6,'Particular (6)')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.jurisdicao OWNER TO postgres#

CREATE TABLE dominios.administracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT administracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.administracao (code,code_name) VALUES (0,'Desconhecida (0)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (1,'Federal (1)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (2,'Estadual (2)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (3,'Municipal (3)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (6,'Particular (6)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (7,'Concessionada (7)')#
INSERT INTO dominios.administracao (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.administracao OWNER TO postgres#

CREATE TABLE dominios.tipo_elemento_infraestrutura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_elemento_infraestrutura_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1938,'Atrac - Cais (1938)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1939,'Atrac - Cais flutuante (1939)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1940,'Atrac - Trapiche (1940)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1941,'Atrac - Molhe de atracação (1941)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1942,'Atrac - Pier (1942)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1943,'Atrac - Dolfim (1943)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (1944,'Atrac - Desembarcadouro (1944)')#
INSERT INTO dominios.tipo_elemento_infraestrutura (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_elemento_infraestrutura OWNER TO postgres#

CREATE TABLE dominios.tipo_via_deslocamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_via_deslocamento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_via_deslocamento (code,code_name) VALUES (2,'Estrada/Rodovia (2)')#
INSERT INTO dominios.tipo_via_deslocamento (code,code_name) VALUES (4,'Auto-estrada (4)')#
INSERT INTO dominios.tipo_via_deslocamento (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_via_deslocamento OWNER TO postgres#

CREATE TABLE dominios.tipo_ferrovia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ferrovia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ferrovia (code,code_name) VALUES (5,'Bonde (5)')#
INSERT INTO dominios.tipo_ferrovia (code,code_name) VALUES (6,'Aeromóvel (6)')#
INSERT INTO dominios.tipo_ferrovia (code,code_name) VALUES (7,'Trem (7)')#
INSERT INTO dominios.tipo_ferrovia (code,code_name) VALUES (8,'Metrô (8)')#
INSERT INTO dominios.tipo_ferrovia (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.tipo_ferrovia OWNER TO postgres#

CREATE TABLE dominios.nr_linhas (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nr_linhas_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nr_linhas (code,code_name) VALUES (0,'Desconhecido (0)')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (1,'Simples (1)')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (2,'Dupla (2)')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (3,'Múltipla (3)')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.nr_linhas OWNER TO postgres#

CREATE TABLE dominios.trafego (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT trafego_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.trafego (code,code_name) VALUES (1,'Permanente (1)')#
INSERT INTO dominios.trafego (code,code_name) VALUES (2,'Periódico (2)')#
INSERT INTO dominios.trafego (code,code_name) VALUES (9999,'A SER PREENCHIDO (9999)')#

ALTER TABLE dominios.trafego OWNER TO postgres#

CREATE TABLE edgv.cobter_massa_dagua_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 regime smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 apresentar_simbologia smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cobter_massa_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cobter_massa_dagua_a_geom ON edgv.cobter_massa_dagua_a USING gist (geom)#

ALTER TABLE edgv.cobter_massa_dagua_a OWNER TO postgres#

ALTER TABLE edgv.cobter_massa_dagua_a
	 ADD CONSTRAINT cobter_massa_dagua_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_massa_dagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cobter_massa_dagua_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.cobter_massa_dagua_a
	 ADD CONSTRAINT cobter_massa_dagua_a_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cobter_massa_dagua_a ALTER COLUMN regime SET DEFAULT 9999#

ALTER TABLE edgv.cobter_massa_dagua_a
	 ADD CONSTRAINT cobter_massa_dagua_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cobter_massa_dagua_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.cobter_massa_dagua_a
	 ADD CONSTRAINT cobter_massa_dagua_a_apresentar_simbologia_fk FOREIGN KEY (apresentar_simbologia)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cobter_massa_dagua_a ALTER COLUMN apresentar_simbologia SET DEFAULT 9999#

ALTER TABLE edgv.cobter_massa_dagua_a
	 ADD CONSTRAINT cobter_massa_dagua_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cobter_massa_dagua_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.constr_extracao_mineral_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 tipo_produto smallint NOT NULL,
	 forma_extracao smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT constr_extracao_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX constr_extracao_mineral_a_geom ON edgv.constr_extracao_mineral_a USING gist (geom)#

ALTER TABLE edgv.constr_extracao_mineral_a OWNER TO postgres#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_extracao_mineral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_tipo_produto_fk FOREIGN KEY (tipo_produto)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN tipo_produto SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_forma_extracao_fk FOREIGN KEY (forma_extracao)
	 REFERENCES dominios.forma_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN forma_extracao SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_a
	 ADD CONSTRAINT constr_extracao_mineral_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.constr_extracao_mineral_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 tipo_produto smallint NOT NULL,
	 forma_extracao smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT constr_extracao_mineral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX constr_extracao_mineral_p_geom ON edgv.constr_extracao_mineral_p USING gist (geom)#

ALTER TABLE edgv.constr_extracao_mineral_p OWNER TO postgres#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_extracao_mineral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_tipo_produto_fk FOREIGN KEY (tipo_produto)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN tipo_produto SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_forma_extracao_fk FOREIGN KEY (forma_extracao)
	 REFERENCES dominios.forma_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN forma_extracao SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.constr_extracao_mineral_p
	 ADD CONSTRAINT constr_extracao_mineral_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.constr_extracao_mineral_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_curva_nivel_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 cota integer NOT NULL,
	 indice smallint NOT NULL,
	 depressao smallint NOT NULL,
	 dentro_de_massa_dagua smallint NOT NULL,
	 texto_edicao varchar(255),
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT elemnat_curva_nivel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_curva_nivel_l_geom ON edgv.elemnat_curva_nivel_l USING gist (geom)#

ALTER TABLE edgv.elemnat_curva_nivel_l OWNER TO postgres#

ALTER TABLE edgv.elemnat_curva_nivel_l
	 ADD CONSTRAINT elemnat_curva_nivel_l_indice_fk FOREIGN KEY (indice)
	 REFERENCES dominios.indice (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_curva_nivel_l ALTER COLUMN indice SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_curva_nivel_l
	 ADD CONSTRAINT elemnat_curva_nivel_l_depressao_fk FOREIGN KEY (depressao)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_curva_nivel_l ALTER COLUMN depressao SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_curva_nivel_l
	 ADD CONSTRAINT elemnat_curva_nivel_l_dentro_de_massa_dagua_fk FOREIGN KEY (dentro_de_massa_dagua)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_curva_nivel_l ALTER COLUMN dentro_de_massa_dagua SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_curva_nivel_l
	 ADD CONSTRAINT elemnat_curva_nivel_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_curva_nivel_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_elemento_hidrografico_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT elemnat_elemento_hidrografico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_elemento_hidrografico_a_geom ON edgv.elemnat_elemento_hidrografico_a USING gist (geom)#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a OWNER TO postgres#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a
	 ADD CONSTRAINT elemnat_elemento_hidrografico_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_hidrografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a
	 ADD CONSTRAINT elemnat_elemento_hidrografico_a_tipo_check 
	 CHECK (tipo = ANY(ARRAY[6 :: SMALLINT, 12 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.elemnat_elemento_hidrografico_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a
	 ADD CONSTRAINT elemnat_elemento_hidrografico_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a
	 ADD CONSTRAINT elemnat_elemento_hidrografico_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_elemento_hidrografico_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT elemnat_elemento_hidrografico_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_elemento_hidrografico_l_geom ON edgv.elemnat_elemento_hidrografico_l USING gist (geom)#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l OWNER TO postgres#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l
	 ADD CONSTRAINT elemnat_elemento_hidrografico_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_hidrografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l
	 ADD CONSTRAINT elemnat_elemento_hidrografico_l_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l
	 ADD CONSTRAINT elemnat_elemento_hidrografico_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_elemento_hidrografico_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT elemnat_elemento_hidrografico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_elemento_hidrografico_p_geom ON edgv.elemnat_elemento_hidrografico_p USING gist (geom)#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p OWNER TO postgres#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p
	 ADD CONSTRAINT elemnat_elemento_hidrografico_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_hidrografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p
	 ADD CONSTRAINT elemnat_elemento_hidrografico_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p
	 ADD CONSTRAINT elemnat_elemento_hidrografico_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_elemento_hidrografico_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_ilha_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT elemnat_ilha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_ilha_p_geom ON edgv.elemnat_ilha_p USING gist (geom)#

ALTER TABLE edgv.elemnat_ilha_p OWNER TO postgres#

ALTER TABLE edgv.elemnat_ilha_p
	 ADD CONSTRAINT elemnat_ilha_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_ilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ilha_p
	 ADD CONSTRAINT elemnat_ilha_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ilha_p
	 ADD CONSTRAINT elemnat_ilha_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_ilha_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT elemnat_ilha_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_ilha_a_geom ON edgv.elemnat_ilha_a USING gist (geom)#

ALTER TABLE edgv.elemnat_ilha_a OWNER TO postgres#

ALTER TABLE edgv.elemnat_ilha_a
	 ADD CONSTRAINT elemnat_ilha_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_ilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ilha_a
	 ADD CONSTRAINT elemnat_ilha_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ilha_a
	 ADD CONSTRAINT elemnat_ilha_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ilha_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_ponto_cotado_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 cota real NOT NULL,
	 cota_comprovada smallint NOT NULL,
	 cota_mais_alta smallint NOT NULL,
	 label_x real,
	 label_y real,
	 visivel smallint NOT NULL,
	 ancora_horizontal smallint NOT NULL,
	 ancora_vertical smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT elemnat_ponto_cotado_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_ponto_cotado_p_geom ON edgv.elemnat_ponto_cotado_p USING gist (geom)#

ALTER TABLE edgv.elemnat_ponto_cotado_p OWNER TO postgres#

ALTER TABLE edgv.elemnat_ponto_cotado_p
	 ADD CONSTRAINT elemnat_ponto_cotado_p_cota_comprovada_fk FOREIGN KEY (cota_comprovada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ponto_cotado_p ALTER COLUMN cota_comprovada SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ponto_cotado_p
	 ADD CONSTRAINT elemnat_ponto_cotado_p_cota_mais_alta_fk FOREIGN KEY (cota_mais_alta)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ponto_cotado_p ALTER COLUMN cota_mais_alta SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ponto_cotado_p
	 ADD CONSTRAINT elemnat_ponto_cotado_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ponto_cotado_p ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ponto_cotado_p
	 ADD CONSTRAINT elemnat_ponto_cotado_p_ancora_horizontal_fk FOREIGN KEY (ancora_horizontal)
	 REFERENCES dominios.ancora_horizontal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ponto_cotado_p ALTER COLUMN ancora_horizontal SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_ponto_cotado_p
	 ADD CONSTRAINT elemnat_ponto_cotado_p_ancora_vertical_fk FOREIGN KEY (ancora_vertical)
	 REFERENCES dominios.ancora_vertical (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_ponto_cotado_p ALTER COLUMN ancora_vertical SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_terreno_sujeito_inundacao_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT elemnat_terreno_sujeito_inundacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_terreno_sujeito_inundacao_a_geom ON edgv.elemnat_terreno_sujeito_inundacao_a USING gist (geom)#

ALTER TABLE edgv.elemnat_terreno_sujeito_inundacao_a OWNER TO postgres#

ALTER TABLE edgv.elemnat_terreno_sujeito_inundacao_a
	 ADD CONSTRAINT elemnat_terreno_sujeito_inundacao_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_terreno_sujeito_inundacao_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_toponimo_fisiografico_natural_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 espacamento real,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT elemnat_toponimo_fisiografico_natural_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_toponimo_fisiografico_natural_p_geom ON edgv.elemnat_toponimo_fisiografico_natural_p USING gist (geom)#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p OWNER TO postgres#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_toponimo_fisiografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 12 :: SMALLINT, 17 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_toponimo_fisiografico_natural_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 tamanho_txt real,
	 espacamento real,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT elemnat_toponimo_fisiografico_natural_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_toponimo_fisiografico_natural_l_geom ON edgv.elemnat_toponimo_fisiografico_natural_l USING gist (geom)#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l OWNER TO postgres#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_toponimo_fisiografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_l_tipo_check 
	 CHECK (tipo = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 12 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l
	 ADD CONSTRAINT elemnat_toponimo_fisiografico_natural_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_toponimo_fisiografico_natural_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.elemnat_trecho_drenagem_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_em_poligono smallint NOT NULL,
	 regime smallint NOT NULL,
	 texto_edicao varchar(255),
	 tamanho_txt real,
	 visivel smallint NOT NULL,
	 posicao_rotulo smallint NOT NULL,
	 direcao_fixada smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT elemnat_trecho_drenagem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX elemnat_trecho_drenagem_l_geom ON edgv.elemnat_trecho_drenagem_l USING gist (geom)#

ALTER TABLE edgv.elemnat_trecho_drenagem_l OWNER TO postgres#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_trecho_drenagem (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_situacao_em_poligono_fk FOREIGN KEY (situacao_em_poligono)
	 REFERENCES dominios.situacao_em_poligono (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN situacao_em_poligono SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN regime SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_posicao_rotulo_fk FOREIGN KEY (posicao_rotulo)
	 REFERENCES dominios.posicao_rotulo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN posicao_rotulo SET DEFAULT 9999#

ALTER TABLE edgv.elemnat_trecho_drenagem_l
	 ADD CONSTRAINT elemnat_trecho_drenagem_l_direcao_fixada_fk FOREIGN KEY (direcao_fixada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.elemnat_trecho_drenagem_l ALTER COLUMN direcao_fixada SET DEFAULT 9999#

CREATE TABLE edgv.infra_barragem_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 material_construcao smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_barragem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_barragem_l_geom ON edgv.infra_barragem_l USING gist (geom)#

ALTER TABLE edgv.infra_barragem_l OWNER TO postgres#

ALTER TABLE edgv.infra_barragem_l
	 ADD CONSTRAINT infra_barragem_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_barragem (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_barragem_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_barragem_l
	 ADD CONSTRAINT infra_barragem_l_material_construcao_fk FOREIGN KEY (material_construcao)
	 REFERENCES dominios.material_construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_barragem_l
	 ADD CONSTRAINT infra_barragem_l_material_construcao_check 
	 CHECK (material_construcao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 23 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_barragem_l ALTER COLUMN material_construcao SET DEFAULT 9999#

CREATE TABLE edgv.infra_barragem_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 material_construcao smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT infra_barragem_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_barragem_a_geom ON edgv.infra_barragem_a USING gist (geom)#

ALTER TABLE edgv.infra_barragem_a OWNER TO postgres#

ALTER TABLE edgv.infra_barragem_a
	 ADD CONSTRAINT infra_barragem_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_barragem (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_barragem_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_barragem_a
	 ADD CONSTRAINT infra_barragem_a_material_construcao_fk FOREIGN KEY (material_construcao)
	 REFERENCES dominios.material_construcao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_barragem_a
	 ADD CONSTRAINT infra_barragem_a_material_construcao_check 
	 CHECK (material_construcao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 23 :: SMALLINT, 9999 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_barragem_a ALTER COLUMN material_construcao SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_energia_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT infra_elemento_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_energia_p_geom ON edgv.infra_elemento_energia_p USING gist (geom)#

ALTER TABLE edgv.infra_elemento_energia_p OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_energia_p
	 ADD CONSTRAINT infra_elemento_energia_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_p
	 ADD CONSTRAINT infra_elemento_energia_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[1801 :: SMALLINT, 1802 :: SMALLINT, 405 :: SMALLINT, 408 :: SMALLINT, 407 :: SMALLINT, 498 :: SMALLINT, 406 :: SMALLINT, 409 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_elemento_energia_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_p
	 ADD CONSTRAINT infra_elemento_energia_p_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_p ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_p
	 ADD CONSTRAINT infra_elemento_energia_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_p ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_p
	 ADD CONSTRAINT infra_elemento_energia_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_energia_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT infra_elemento_energia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_energia_a_geom ON edgv.infra_elemento_energia_a USING gist (geom)#

ALTER TABLE edgv.infra_elemento_energia_a OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_energia_a
	 ADD CONSTRAINT infra_elemento_energia_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_a
	 ADD CONSTRAINT infra_elemento_energia_a_tipo_check 
	 CHECK (tipo = ANY(ARRAY[1801 :: SMALLINT, 1802 :: SMALLINT, 405 :: SMALLINT, 408 :: SMALLINT, 407 :: SMALLINT, 498 :: SMALLINT, 406 :: SMALLINT, 409 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_elemento_energia_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_a
	 ADD CONSTRAINT infra_elemento_energia_a_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_a ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_a
	 ADD CONSTRAINT infra_elemento_energia_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_a ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_a
	 ADD CONSTRAINT infra_elemento_energia_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_energia_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_elemento_energia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_energia_l_geom ON edgv.infra_elemento_energia_l USING gist (geom)#

ALTER TABLE edgv.infra_elemento_energia_l OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_energia_l
	 ADD CONSTRAINT infra_elemento_energia_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_l
	 ADD CONSTRAINT infra_elemento_energia_l_tipo_check 
	 CHECK (tipo = ANY(ARRAY[303 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_elemento_energia_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_l
	 ADD CONSTRAINT infra_elemento_energia_l_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_l ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_energia_l
	 ADD CONSTRAINT infra_elemento_energia_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_energia_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_infraestrutura_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT infra_elemento_infraestrutura_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_infraestrutura_a_geom ON edgv.infra_elemento_infraestrutura_a USING gist (geom)#

ALTER TABLE edgv.infra_elemento_infraestrutura_a OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_infraestrutura_a
	 ADD CONSTRAINT infra_elemento_infraestrutura_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_infraestrutura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_a
	 ADD CONSTRAINT infra_elemento_infraestrutura_a_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_a ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_a
	 ADD CONSTRAINT infra_elemento_infraestrutura_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_a
	 ADD CONSTRAINT infra_elemento_infraestrutura_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_infraestrutura_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_elemento_infraestrutura_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_infraestrutura_l_geom ON edgv.infra_elemento_infraestrutura_l USING gist (geom)#

ALTER TABLE edgv.infra_elemento_infraestrutura_l OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_infraestrutura_l
	 ADD CONSTRAINT infra_elemento_infraestrutura_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_infraestrutura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_l
	 ADD CONSTRAINT infra_elemento_infraestrutura_l_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_l ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_l
	 ADD CONSTRAINT infra_elemento_infraestrutura_l_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_l ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_l
	 ADD CONSTRAINT infra_elemento_infraestrutura_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.infra_elemento_infraestrutura_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT infra_elemento_infraestrutura_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_elemento_infraestrutura_p_geom ON edgv.infra_elemento_infraestrutura_p USING gist (geom)#

ALTER TABLE edgv.infra_elemento_infraestrutura_p OWNER TO postgres#

ALTER TABLE edgv.infra_elemento_infraestrutura_p
	 ADD CONSTRAINT infra_elemento_infraestrutura_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_infraestrutura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_p
	 ADD CONSTRAINT infra_elemento_infraestrutura_p_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_p ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_p
	 ADD CONSTRAINT infra_elemento_infraestrutura_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.infra_elemento_infraestrutura_p
	 ADD CONSTRAINT infra_elemento_infraestrutura_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_elemento_infraestrutura_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.infra_ferrovia_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 posicao_relativa smallint NOT NULL,
	 nr_linhas smallint NOT NULL,
	 eletrificada smallint NOT NULL,
	 bitola smallint NOT NULL,
	 em_arruamento smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(255),
	 texto_edicao varchar(255),
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_ferrovia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_ferrovia_l_geom ON edgv.infra_ferrovia_l USING gist (geom)#

ALTER TABLE edgv.infra_ferrovia_l OWNER TO postgres#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_ferrovia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_posicao_relativa_fk FOREIGN KEY (posicao_relativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN posicao_relativa SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_nr_linhas_fk FOREIGN KEY (nr_linhas)
	 REFERENCES dominios.nr_linhas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN nr_linhas SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_eletrificada_fk FOREIGN KEY (eletrificada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN eletrificada SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_bitola_fk FOREIGN KEY (bitola)
	 REFERENCES dominios.bitola (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN bitola SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_em_arruamento_fk FOREIGN KEY (em_arruamento)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN em_arruamento SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.infra_ferrovia_l
	 ADD CONSTRAINT infra_ferrovia_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_ferrovia_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.infra_pista_pouso_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 uso_pista smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 altitude real,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT infra_pista_pouso_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_pista_pouso_a_geom ON edgv.infra_pista_pouso_a USING gist (geom)#

ALTER TABLE edgv.infra_pista_pouso_a OWNER TO postgres#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_pista_pouso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_tipo_check 
	 CHECK (tipo = ANY(ARRAY[9 :: SMALLINT, 10 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_revestimento_check 
	 CHECK (revestimento = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_uso_pista_fk FOREIGN KEY (uso_pista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN uso_pista SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_a
	 ADD CONSTRAINT infra_pista_pouso_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.infra_pista_pouso_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 uso_pista smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 altitude real,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_pista_pouso_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_pista_pouso_l_geom ON edgv.infra_pista_pouso_l USING gist (geom)#

ALTER TABLE edgv.infra_pista_pouso_l OWNER TO postgres#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_pista_pouso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_tipo_check 
	 CHECK (tipo = ANY(ARRAY[9 :: SMALLINT, 10 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_revestimento_check 
	 CHECK (revestimento = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_uso_pista_fk FOREIGN KEY (uso_pista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN uso_pista SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_l
	 ADD CONSTRAINT infra_pista_pouso_l_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_l ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.infra_pista_pouso_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 uso_pista smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 altitude real,
	 visivel smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 simb_rot real,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT infra_pista_pouso_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_pista_pouso_p_geom ON edgv.infra_pista_pouso_p USING gist (geom)#

ALTER TABLE edgv.infra_pista_pouso_p OWNER TO postgres#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_pista_pouso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[9 :: SMALLINT, 11 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_revestimento_check 
	 CHECK (revestimento = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT, 9999 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_uso_pista_fk FOREIGN KEY (uso_pista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN uso_pista SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.infra_pista_pouso_p
	 ADD CONSTRAINT infra_pista_pouso_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_pista_pouso_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.infra_via_deslocamento_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 trafego smallint NOT NULL,
	 nr_faixas varchar(255),
	 nr_pistas varchar(255),
	 canteiro_divisorio smallint NOT NULL,
	 situacao_fisica smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 sigla varchar(255),
	 administracao smallint NOT NULL,
	 concessionaria varchar(255),
	 texto_edicao varchar(255),
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT infra_via_deslocamento_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX infra_via_deslocamento_l_geom ON edgv.infra_via_deslocamento_l USING gist (geom)#

ALTER TABLE edgv.infra_via_deslocamento_l OWNER TO postgres#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_via_deslocamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_revestimento_check 
	 CHECK (revestimento = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN trafego SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_canteiro_divisorio_fk FOREIGN KEY (canteiro_divisorio)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN canteiro_divisorio SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_situacao_fisica_fk FOREIGN KEY (situacao_fisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN situacao_fisica SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 7 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.infra_via_deslocamento_l
	 ADD CONSTRAINT infra_via_deslocamento_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.infra_via_deslocamento_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_aglomerado_rural_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT llp_aglomerado_rural_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_aglomerado_rural_p_geom ON edgv.llp_aglomerado_rural_p USING gist (geom)#

ALTER TABLE edgv.llp_aglomerado_rural_p OWNER TO postgres#

ALTER TABLE edgv.llp_aglomerado_rural_p
	 ADD CONSTRAINT llp_aglomerado_rural_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_localidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_aglomerado_rural_p
	 ADD CONSTRAINT llp_aglomerado_rural_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.llp_aglomerado_rural_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.llp_aglomerado_rural_p
	 ADD CONSTRAINT llp_aglomerado_rural_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_aglomerado_rural_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.llp_aglomerado_rural_p
	 ADD CONSTRAINT llp_aglomerado_rural_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_aglomerado_rural_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_area_pub_militar_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 geometria_aproximada smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT llp_area_pub_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_area_pub_militar_a_geom ON edgv.llp_area_pub_militar_a USING gist (geom)#

ALTER TABLE edgv.llp_area_pub_militar_a OWNER TO postgres#

ALTER TABLE edgv.llp_area_pub_militar_a
	 ADD CONSTRAINT llp_area_pub_militar_a_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_area_pub_militar_a ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.llp_area_pub_militar_a
	 ADD CONSTRAINT llp_area_pub_militar_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_area_pub_militar_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.llp_area_pub_militar_a
	 ADD CONSTRAINT llp_area_pub_militar_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_area_pub_militar_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_localidade_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 populacao integer,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT llp_localidade_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_localidade_p_geom ON edgv.llp_localidade_p USING gist (geom)#

ALTER TABLE edgv.llp_localidade_p OWNER TO postgres#

ALTER TABLE edgv.llp_localidade_p
	 ADD CONSTRAINT llp_localidade_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_localidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_localidade_p
	 ADD CONSTRAINT llp_localidade_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.llp_localidade_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.llp_localidade_p
	 ADD CONSTRAINT llp_localidade_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_localidade_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.llp_localidade_p
	 ADD CONSTRAINT llp_localidade_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_localidade_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_nome_local_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 texto_edicao varchar(255),
	 visivel smallint NOT NULL,
	 label_x real,
	 label_y real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT llp_nome_local_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_nome_local_p_geom ON edgv.llp_nome_local_p USING gist (geom)#

ALTER TABLE edgv.llp_nome_local_p OWNER TO postgres#

ALTER TABLE edgv.llp_nome_local_p
	 ADD CONSTRAINT llp_nome_local_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_nome_local_p ALTER COLUMN visivel SET DEFAULT 9999#

ALTER TABLE edgv.llp_nome_local_p
	 ADD CONSTRAINT llp_nome_local_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_nome_local_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.llp_terra_indigena_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 geometria_aproximada smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT llp_terra_indigena_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_terra_indigena_a_geom ON edgv.llp_terra_indigena_a USING gist (geom)#

ALTER TABLE edgv.llp_terra_indigena_a OWNER TO postgres#

ALTER TABLE edgv.llp_terra_indigena_a
	 ADD CONSTRAINT llp_terra_indigena_a_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_terra_indigena_a ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.llp_terra_indigena_a
	 ADD CONSTRAINT llp_terra_indigena_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_terra_indigena_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.llp_terra_indigena_a
	 ADD CONSTRAINT llp_terra_indigena_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_terra_indigena_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_unidade_conservacao_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 geometria_aproximada smallint NOT NULL,
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT llp_unidade_conservacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_unidade_conservacao_a_geom ON edgv.llp_unidade_conservacao_a USING gist (geom)#

ALTER TABLE edgv.llp_unidade_conservacao_a OWNER TO postgres#

ALTER TABLE edgv.llp_unidade_conservacao_a
	 ADD CONSTRAINT llp_unidade_conservacao_a_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_limite_especial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_unidade_conservacao_a
	 ADD CONSTRAINT llp_unidade_conservacao_a_tipo_check 
	 CHECK (tipo = ANY(ARRAY[5 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.llp_unidade_conservacao_a ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.llp_unidade_conservacao_a
	 ADD CONSTRAINT llp_unidade_conservacao_a_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_unidade_conservacao_a ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.llp_unidade_conservacao_a
	 ADD CONSTRAINT llp_unidade_conservacao_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_unidade_conservacao_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

ALTER TABLE edgv.llp_unidade_conservacao_a
	 ADD CONSTRAINT llp_unidade_conservacao_a_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_unidade_conservacao_a ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.llp_unidade_federacao_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 sigla varchar(255),
	 geometria_aproximada smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT llp_unidade_federacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX llp_unidade_federacao_a_geom ON edgv.llp_unidade_federacao_a USING gist (geom)#

ALTER TABLE edgv.llp_unidade_federacao_a OWNER TO postgres#

ALTER TABLE edgv.llp_unidade_federacao_a
	 ADD CONSTRAINT llp_unidade_federacao_a_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.llp_unidade_federacao_a ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

CREATE TABLE edgv.edicao_area_pub_militar_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 geometria_aproximada smallint NOT NULL,
	 sobreposto smallint NOT NULL,
	 exibir_rotulo_aproximado smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_area_pub_militar_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_area_pub_militar_l_geom ON edgv.edicao_area_pub_militar_l USING gist (geom)#

ALTER TABLE edgv.edicao_area_pub_militar_l OWNER TO postgres#

ALTER TABLE edgv.edicao_area_pub_militar_l
	 ADD CONSTRAINT edicao_area_pub_militar_l_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_area_pub_militar_l ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.edicao_area_pub_militar_l
	 ADD CONSTRAINT edicao_area_pub_militar_l_sobreposto_fk FOREIGN KEY (sobreposto)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_area_pub_militar_l ALTER COLUMN sobreposto SET DEFAULT 9999#

ALTER TABLE edgv.edicao_area_pub_militar_l
	 ADD CONSTRAINT edicao_area_pub_militar_l_exibir_rotulo_aproximado_fk FOREIGN KEY (exibir_rotulo_aproximado)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_area_pub_militar_l ALTER COLUMN exibir_rotulo_aproximado SET DEFAULT 9999#

ALTER TABLE edgv.edicao_area_pub_militar_l
	 ADD CONSTRAINT edicao_area_pub_militar_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_area_pub_militar_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_terra_indigena_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 geometria_aproximada smallint NOT NULL,
	 sobreposto smallint NOT NULL,
	 exibir_rotulo_aproximado smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_terra_indigena_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_terra_indigena_l_geom ON edgv.edicao_terra_indigena_l USING gist (geom)#

ALTER TABLE edgv.edicao_terra_indigena_l OWNER TO postgres#

ALTER TABLE edgv.edicao_terra_indigena_l
	 ADD CONSTRAINT edicao_terra_indigena_l_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_terra_indigena_l ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.edicao_terra_indigena_l
	 ADD CONSTRAINT edicao_terra_indigena_l_sobreposto_fk FOREIGN KEY (sobreposto)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_terra_indigena_l ALTER COLUMN sobreposto SET DEFAULT 9999#

ALTER TABLE edgv.edicao_terra_indigena_l
	 ADD CONSTRAINT edicao_terra_indigena_l_exibir_rotulo_aproximado_fk FOREIGN KEY (exibir_rotulo_aproximado)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_terra_indigena_l ALTER COLUMN exibir_rotulo_aproximado SET DEFAULT 9999#

ALTER TABLE edgv.edicao_terra_indigena_l
	 ADD CONSTRAINT edicao_terra_indigena_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_terra_indigena_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_unidade_conservacao_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 geometria_aproximada smallint NOT NULL,
	 sobreposto smallint NOT NULL,
	 exibir_rotulo_aproximado smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_unidade_conservacao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_unidade_conservacao_l_geom ON edgv.edicao_unidade_conservacao_l USING gist (geom)#

ALTER TABLE edgv.edicao_unidade_conservacao_l OWNER TO postgres#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_limite_especial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_tipo_check 
	 CHECK (tipo = ANY(ARRAY[5 :: SMALLINT, 24 :: SMALLINT, 25 :: SMALLINT, 26 :: SMALLINT, 27 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 30 :: SMALLINT, 31 :: SMALLINT, 32 :: SMALLINT, 33 :: SMALLINT, 34 :: SMALLINT, 35 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.edicao_unidade_conservacao_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_unidade_conservacao_l ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_sobreposto_fk FOREIGN KEY (sobreposto)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_unidade_conservacao_l ALTER COLUMN sobreposto SET DEFAULT 9999#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_exibir_rotulo_aproximado_fk FOREIGN KEY (exibir_rotulo_aproximado)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_unidade_conservacao_l ALTER COLUMN exibir_rotulo_aproximado SET DEFAULT 9999#

ALTER TABLE edgv.edicao_unidade_conservacao_l
	 ADD CONSTRAINT edicao_unidade_conservacao_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_unidade_conservacao_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_limite_legal_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 geometria_aproximada smallint NOT NULL,
	 texto_edicao varchar(255),
	 sobreposto smallint NOT NULL,
	 exibir_rotulo_aproximado smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_limite_legal_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_limite_legal_l_geom ON edgv.edicao_limite_legal_l USING gist (geom)#

ALTER TABLE edgv.edicao_limite_legal_l OWNER TO postgres#

ALTER TABLE edgv.edicao_limite_legal_l
	 ADD CONSTRAINT edicao_limite_legal_l_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_limite_legal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_limite_legal_l ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.edicao_limite_legal_l
	 ADD CONSTRAINT edicao_limite_legal_l_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_limite_legal_l ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

ALTER TABLE edgv.edicao_limite_legal_l
	 ADD CONSTRAINT edicao_limite_legal_l_sobreposto_fk FOREIGN KEY (sobreposto)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_limite_legal_l ALTER COLUMN sobreposto SET DEFAULT 9999#

ALTER TABLE edgv.edicao_limite_legal_l
	 ADD CONSTRAINT edicao_limite_legal_l_exibir_rotulo_aproximado_fk FOREIGN KEY (exibir_rotulo_aproximado)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_limite_legal_l ALTER COLUMN exibir_rotulo_aproximado SET DEFAULT 9999#

ALTER TABLE edgv.edicao_limite_legal_l
	 ADD CONSTRAINT edicao_limite_legal_l_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_limite_legal_l ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_grid_edicao_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_grid_edicao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_grid_edicao_l_geom ON edgv.edicao_grid_edicao_l USING gist (geom)#

ALTER TABLE edgv.edicao_grid_edicao_l OWNER TO postgres#

CREATE TABLE edgv.edicao_articulacao_imagem_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome_sensor varchar(255),
	 nome_abrev_sensor varchar(255),
	 data varchar(255),
	 tipo varchar(255),
	 plataforma varchar(255),
	 resolucao varchar(255),
	 bandas varchar(255),
	 nivel_produto varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edicao_articulacao_imagem_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_articulacao_imagem_a_geom ON edgv.edicao_articulacao_imagem_a USING gist (geom)#

ALTER TABLE edgv.edicao_articulacao_imagem_a OWNER TO postgres#

CREATE TABLE edgv.edicao_area_sem_dados_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edicao_area_sem_dados_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_area_sem_dados_a_geom ON edgv.edicao_area_sem_dados_a USING gist (geom)#

ALTER TABLE edgv.edicao_area_sem_dados_a OWNER TO postgres#

ALTER TABLE edgv.edicao_area_sem_dados_a
	 ADD CONSTRAINT edicao_area_sem_dados_a_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_area_sem_dados_a ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.delimitador_area_sem_dados_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT delimitador_area_sem_dados_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX delimitador_area_sem_dados_l_geom ON edgv.delimitador_area_sem_dados_l USING gist (geom)#

ALTER TABLE edgv.delimitador_area_sem_dados_l OWNER TO postgres#

CREATE TABLE edgv.aux_validacao_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_validacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_validacao_a_geom ON edgv.aux_validacao_a USING gist (geom)#

ALTER TABLE edgv.aux_validacao_a OWNER TO postgres#

CREATE TABLE edgv.aux_validacao_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT aux_validacao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_validacao_l_geom ON edgv.aux_validacao_l USING gist (geom)#

ALTER TABLE edgv.aux_validacao_l OWNER TO postgres#

CREATE TABLE edgv.aux_validacao_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT aux_validacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_validacao_p_geom ON edgv.aux_validacao_p USING gist (geom)#

ALTER TABLE edgv.aux_validacao_p OWNER TO postgres#

CREATE TABLE edgv.aux_revisao_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 corrigido smallint NOT NULL,
	 justificativa varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_revisao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_revisao_a_geom ON edgv.aux_revisao_a USING gist (geom)#

ALTER TABLE edgv.aux_revisao_a OWNER TO postgres#

ALTER TABLE edgv.aux_revisao_a
	 ADD CONSTRAINT aux_revisao_a_corrigido_fk FOREIGN KEY (corrigido)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aux_revisao_a ALTER COLUMN corrigido SET DEFAULT 9999#

CREATE TABLE edgv.aux_revisao_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 corrigido smallint NOT NULL,
	 justificativa varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT aux_revisao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_revisao_l_geom ON edgv.aux_revisao_l USING gist (geom)#

ALTER TABLE edgv.aux_revisao_l OWNER TO postgres#

ALTER TABLE edgv.aux_revisao_l
	 ADD CONSTRAINT aux_revisao_l_corrigido_fk FOREIGN KEY (corrigido)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aux_revisao_l ALTER COLUMN corrigido SET DEFAULT 9999#

CREATE TABLE edgv.aux_revisao_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 descricao varchar(255),
	 subfase_id integer,
	 corrigido smallint NOT NULL,
	 justificativa varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT aux_revisao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_revisao_p_geom ON edgv.aux_revisao_p USING gist (geom)#

ALTER TABLE edgv.aux_revisao_p OWNER TO postgres#

ALTER TABLE edgv.aux_revisao_p
	 ADD CONSTRAINT aux_revisao_p_corrigido_fk FOREIGN KEY (corrigido)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aux_revisao_p ALTER COLUMN corrigido SET DEFAULT 9999#

CREATE TABLE edgv.aux_moldura_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 mi varchar(255),
	 inom varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_moldura_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_moldura_a_geom ON edgv.aux_moldura_a USING gist (geom)#

ALTER TABLE edgv.aux_moldura_a OWNER TO postgres#

CREATE TABLE edgv.aux_moldura_area_continua_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_moldura_area_continua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_moldura_area_continua_a_geom ON edgv.aux_moldura_area_continua_a USING gist (geom)#

ALTER TABLE edgv.aux_moldura_area_continua_a OWNER TO postgres#

CREATE TABLE edgv.delimitador_massa_dagua_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT delimitador_massa_dagua_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX delimitador_massa_dagua_l_geom ON edgv.delimitador_massa_dagua_l USING gist (geom)#

ALTER TABLE edgv.delimitador_massa_dagua_l OWNER TO postgres#

CREATE TABLE edgv.delimitador_elemento_hidrografico_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT delimitador_elemento_hidrografico_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX delimitador_elemento_hidrografico_l_geom ON edgv.delimitador_elemento_hidrografico_l USING gist (geom)#

ALTER TABLE edgv.delimitador_elemento_hidrografico_l OWNER TO postgres#

CREATE TABLE edgv.centroide_massa_dagua_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 regime smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT centroide_massa_dagua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX centroide_massa_dagua_p_geom ON edgv.centroide_massa_dagua_p USING gist (geom)#

ALTER TABLE edgv.centroide_massa_dagua_p OWNER TO postgres#

ALTER TABLE edgv.centroide_massa_dagua_p
	 ADD CONSTRAINT centroide_massa_dagua_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_massa_dagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_massa_dagua_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.centroide_massa_dagua_p
	 ADD CONSTRAINT centroide_massa_dagua_p_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_massa_dagua_p ALTER COLUMN regime SET DEFAULT 9999#

CREATE TABLE edgv.centroide_ilha_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT centroide_ilha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX centroide_ilha_p_geom ON edgv.centroide_ilha_p USING gist (geom)#

ALTER TABLE edgv.centroide_ilha_p OWNER TO postgres#

ALTER TABLE edgv.centroide_ilha_p
	 ADD CONSTRAINT centroide_ilha_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_ilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_ilha_p ALTER COLUMN tipo SET DEFAULT 9999#

CREATE TABLE edgv.centroide_elemento_hidrografico_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT centroide_elemento_hidrografico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX centroide_elemento_hidrografico_p_geom ON edgv.centroide_elemento_hidrografico_p USING gist (geom)#

ALTER TABLE edgv.centroide_elemento_hidrografico_p OWNER TO postgres#

ALTER TABLE edgv.centroide_elemento_hidrografico_p
	 ADD CONSTRAINT centroide_elemento_hidrografico_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_elemento_hidrografico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_elemento_hidrografico_p
	 ADD CONSTRAINT centroide_elemento_hidrografico_p_tipo_check 
	 CHECK (tipo = ANY(ARRAY[6 :: SMALLINT, 12 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.centroide_elemento_hidrografico_p ALTER COLUMN tipo SET DEFAULT 9999#

CREATE TABLE edgv.edicao_identificador_trecho_rod_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 sigla varchar(255),
	 tipo smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edicao_identificador_trecho_rod_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_identificador_trecho_rod_p_geom ON edgv.edicao_identificador_trecho_rod_p USING gist (geom)#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p OWNER TO postgres#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p
	 ADD CONSTRAINT edicao_identificador_trecho_rod_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_via_deslocamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p
	 ADD CONSTRAINT edicao_identificador_trecho_rod_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p
	 ADD CONSTRAINT edicao_identificador_trecho_rod_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 9999 :: SMALLINT]))# 

ALTER TABLE edgv.edicao_identificador_trecho_rod_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p
	 ADD CONSTRAINT edicao_identificador_trecho_rod_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_identificador_trecho_rod_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_simb_torre_energia_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 simb_rot real,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edicao_simb_torre_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_simb_torre_energia_p_geom ON edgv.edicao_simb_torre_energia_p USING gist (geom)#

ALTER TABLE edgv.edicao_simb_torre_energia_p OWNER TO postgres#

ALTER TABLE edgv.edicao_simb_torre_energia_p
	 ADD CONSTRAINT edicao_simb_torre_energia_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_simb_torre_energia_p ALTER COLUMN visivel SET DEFAULT 9999#

CREATE TABLE edgv.edicao_simb_cota_mestra_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 texto_edicao varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_simb_cota_mestra_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_simb_cota_mestra_l_geom ON edgv.edicao_simb_cota_mestra_l USING gist (geom)#

ALTER TABLE edgv.edicao_simb_cota_mestra_l OWNER TO postgres#

CREATE TABLE edgv.edicao_texto_generico_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 texto_edicao varchar(255),
	 label_x real,
	 label_y real,
	 estilo_fonte varchar(255),
	 tamanho_txt real,
	 justificativa_txt smallint NOT NULL,
	 espacamento real,
	 cor varchar(255),
	 cor_buffer varchar(255),
	 tamanho_buffer real,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edicao_texto_generico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_texto_generico_p_geom ON edgv.edicao_texto_generico_p USING gist (geom)#

ALTER TABLE edgv.edicao_texto_generico_p OWNER TO postgres#

ALTER TABLE edgv.edicao_texto_generico_p
	 ADD CONSTRAINT edicao_texto_generico_p_justificativa_txt_fk FOREIGN KEY (justificativa_txt)
	 REFERENCES dominios.justificativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_texto_generico_p ALTER COLUMN justificativa_txt SET DEFAULT 9999#

CREATE TABLE edgv.edicao_texto_generico_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 texto_edicao varchar(255),
	 estilo_fonte varchar(255),
	 tamanho_txt real,
	 espacamento real,
	 cor varchar(255),
	 cor_buffer varchar(255),
	 tamanho_buffer real,
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT edicao_texto_generico_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_texto_generico_l_geom ON edgv.edicao_texto_generico_l USING gist (geom)#

ALTER TABLE edgv.edicao_texto_generico_l OWNER TO postgres#

CREATE TABLE edgv.delimitador_limite_especial_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT delimitador_limite_especial_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX delimitador_limite_especial_l_geom ON edgv.delimitador_limite_especial_l USING gist (geom)#

ALTER TABLE edgv.delimitador_limite_especial_l OWNER TO postgres#

CREATE TABLE edgv.centroide_area_sem_dados_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT centroide_area_sem_dados_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX centroide_area_sem_dados_p_geom ON edgv.centroide_area_sem_dados_p USING gist (geom)#

ALTER TABLE edgv.centroide_area_sem_dados_p OWNER TO postgres#

CREATE TABLE edgv.centroide_limite_especial_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 tipo smallint NOT NULL,
	 geometria_aproximada smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT centroide_limite_especial_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX centroide_limite_especial_p_geom ON edgv.centroide_limite_especial_p USING gist (geom)#

ALTER TABLE edgv.centroide_limite_especial_p OWNER TO postgres#

ALTER TABLE edgv.centroide_limite_especial_p
	 ADD CONSTRAINT centroide_limite_especial_p_tipo_fk FOREIGN KEY (tipo)
	 REFERENCES dominios.tipo_limite_especial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_limite_especial_p ALTER COLUMN tipo SET DEFAULT 9999#

ALTER TABLE edgv.centroide_limite_especial_p
	 ADD CONSTRAINT centroide_limite_especial_p_geometria_aproximada_fk FOREIGN KEY (geometria_aproximada)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.centroide_limite_especial_p ALTER COLUMN geometria_aproximada SET DEFAULT 9999#

CREATE TABLE edgv.aux_insumo_externo_a(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 fonte varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_insumo_externo_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_insumo_externo_a_geom ON edgv.aux_insumo_externo_a USING gist (geom)#

ALTER TABLE edgv.aux_insumo_externo_a OWNER TO postgres#

CREATE TABLE edgv.aux_insumo_externo_l(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 fonte varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT aux_insumo_externo_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_insumo_externo_l_geom ON edgv.aux_insumo_externo_l USING gist (geom)#

ALTER TABLE edgv.aux_insumo_externo_l OWNER TO postgres#

CREATE TABLE edgv.aux_insumo_externo_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 nome varchar(255),
	 fonte varchar(255),
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT aux_insumo_externo_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_insumo_externo_p_geom ON edgv.aux_insumo_externo_p USING gist (geom)#

ALTER TABLE edgv.aux_insumo_externo_p OWNER TO postgres#

CREATE TABLE edgv.edicao_ponto_mudanca_p(
	 id uuid NOT NULL DEFAULT uuid_generate_v4(),
	 simb_rot real,
	 desloc real,
	 visivel smallint NOT NULL,
	 observacao VARCHAR(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edicao_ponto_mudanca_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edicao_ponto_mudanca_p_geom ON edgv.edicao_ponto_mudanca_p USING gist (geom)#

ALTER TABLE edgv.edicao_ponto_mudanca_p OWNER TO postgres#

ALTER TABLE edgv.edicao_ponto_mudanca_p
	 ADD CONSTRAINT edicao_ponto_mudanca_p_visivel_fk FOREIGN KEY (visivel)
	 REFERENCES dominios.booleano (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edicao_ponto_mudanca_p ALTER COLUMN visivel SET DEFAULT 9999#