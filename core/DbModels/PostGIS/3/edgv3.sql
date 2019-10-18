CREATE SCHEMA edgv#
CREATE SCHEMA dominios#

CREATE EXTENSION postgis#
SET search_path TO pg_catalog,public,edgv,dominios#

CREATE TABLE public.db_metadata(
	 edgvversion varchar(50) NOT NULL DEFAULT '3.0',
	 dbimplversion varchar(50) NOT NULL DEFAULT '4',
	 CONSTRAINT edgvversioncheck CHECK (edgvversion = '3.0')
)#
INSERT INTO public.db_metadata (edgvversion, dbimplversion) VALUES ('3.0','4')#

CREATE TABLE dominios.aptidao_operacional_atracadouro (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT aptidao_operacional_atracadouro_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.aptidao_operacional_atracadouro (code,code_name) VALUES (2,'Transporte de cabotagem')#
INSERT INTO dominios.aptidao_operacional_atracadouro (code,code_name) VALUES (3,'Transporte oceânico')#
INSERT INTO dominios.aptidao_operacional_atracadouro (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_sinal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_sinal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (1,'Boia luminosa')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (2,'Boia cega')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (3,'Boia de amarração')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (4,'Farol ou farolete')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (5,'Barca farol')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (6,'Sinalização de margem')#
INSERT INTO dominios.tipo_sinal (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_cultura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_cultura_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (1,'Exploração econômica')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (2,'Subsistência')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (3,'Conservação ambiental')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (4,'Ornamental')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.finalidade_cultura (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_travessia_ped (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_travessia_ped_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (7,'Passagem subterrânea')#
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (8,'Passarela')#
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (9,'Pinguela')#
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (10,'Passarela em área úmida')#
INSERT INTO dominios.tipo_travessia_ped (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_quebra_molhe (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_quebra_molhe_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (1,'Quebramar')#
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (2,'Molhe')#
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (4,'Espigão')#
INSERT INTO dominios.tipo_quebra_molhe (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.bitola (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT bitola_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.bitola (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.bitola (code,code_name) VALUES (2,'Métrica')#
INSERT INTO dominios.bitola (code,code_name) VALUES (3,'Internacional')#
INSERT INTO dominios.bitola (code,code_name) VALUES (4,'Larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (5,'Mista métrica internacional')#
INSERT INTO dominios.bitola (code,code_name) VALUES (6,'Mista métrica larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (7,'Mista internacional larga')#
INSERT INTO dominios.bitola (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.forma_extracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT forma_extracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.forma_extracao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (5,'A céu aberto')#
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (6,'Subterrânea')#
INSERT INTO dominios.forma_extracao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_turist (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_turist_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (9,'Cruzeiro')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (10,'Estátua')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (11,'Mirante')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (12,'Monumento')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (13,'Panteão')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (14,'Chafariz')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (15,'Chaminé')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (16,'Escultura')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (17,'Obelisco')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (18,'Torre')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (19,'Administração')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_turist (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_trecho_duto (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_trecho_duto_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (1,'Duto')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (2,'Calha')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (3,'Correia transportadora')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (4,'Bueiro')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (5,'Galeria')#
INSERT INTO dominios.tipo_trecho_duto (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_unid_prot_integ (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_unid_prot_integ_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (1,'Estação ecológica - ESEC')#
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (2,'Parque - PAR')#
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (3,'Monumento natural – MONA')#
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (4,'Reserva biológica – REBIO')#
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (5,'Refúgio da vida silvestre – RVS')#
INSERT INTO dominios.tipo_unid_prot_integ (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_uso_edif (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_uso_edif_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (1,'Próprio nacional')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (2,'Uso da União')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (5,'Uso do município')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (6,'Uso da UF')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_uso_edif (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_dep_geral (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_dep_geral_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (1,'Tanque')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (2,'Caixa d''água')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (3,'Cisterna')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (4,'Depósito de lixo')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (5,'Aterro sanitário')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (6,'Aterro controlado')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (8,'Galpão')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (9,'Silo')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (10,'Composteira')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (11,'Depósito frigorífico')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (19,'Reservatório')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (26,'Barracão industrial')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (32,'Armazém')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_dep_geral (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.secao_ativ_econ (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT secao_ativ_econ_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (1,'Indústrias extrativas')#
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (2,'Indústrias de transformação')#
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (3,'Construção')#
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.secao_ativ_econ (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.sistema_geodesico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT sistema_geodesico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (1,'SAD-69')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (2,'SIRGAS2000')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (3,'WGS-84')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (4,'Córrego Alegre')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (5,'Astro Chuá')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (6,'Outra referência')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (7,'SAD-69 (96)')#
INSERT INTO dominios.sistema_geodesico (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_trecho_comunic (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_trecho_comunic_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (3,'Sinal de TV')#
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (4,'Dados')#
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (7,'Telefônica')#
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_trecho_comunic (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.administracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT administracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.administracao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.administracao (code,code_name) VALUES (2,'Federal')#
INSERT INTO dominios.administracao (code,code_name) VALUES (3,'Estadual/Distrital')#
INSERT INTO dominios.administracao (code,code_name) VALUES (4,'Municipal')#
INSERT INTO dominios.administracao (code,code_name) VALUES (5,'Concessionada')#
INSERT INTO dominios.administracao (code,code_name) VALUES (6,'Privada')#
INSERT INTO dominios.administracao (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.administracao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_via (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_via_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_via (code,code_name) VALUES (1,'Logradouro')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (2,'Rodovia')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (3,'Beco')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (4,'Autoestrada')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (5,'Ligação entre pistas')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (6,'Trecho de entroncamento')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (7,'Servidão')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_via (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.cultivo_predominante (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT cultivo_predominante_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (1,'Milho')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (2,'Banana')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (3,'Laranja')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (4,'Trigo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (6,'Algodão herbáceo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (7,'Cana-de-açúcar')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (8,'Fumo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (9,'Soja')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (10,'Batata inglesa')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (11,'Mandioca, aipim ou macaxeira')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (12,'Feijão')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (13,'Arroz')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (14,'Café')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (15,'Cacau')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (16,'Erva-mate')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (17,'Palmeira')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (18,'Açaí')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (19,'Seringueira')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (20,'Eucalipto')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (21,'Acácia')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (22,'Algaroba')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (23,'Pinus')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (24,'Pastagem cultivada')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (25,'Hortaliças')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (26,'Bracatinga')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (27,'Araucária')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (28,'Carnaúba')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (29,'Pera')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (30,'Maçã')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (31,'Pêssego')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (32,'Juta')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (33,'Cebola')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (42,'Uva')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (43,'Abacate')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (44,'Abacaxi ou ananás')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (45,'Abóbora')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (46,'Acerola')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (47,'Alcachofra')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (48,'Alfafa')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (49,'Algodão arbóreo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (50,'Alho')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (51,'Ameixa')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (52,'Amendoim')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (53,'Amora')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (54,'Aveia')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (55,'Azeitona')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (56,'Azevem')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (57,'Batata-doce')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (58,'Caju')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (59,'Caqui')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (60,'Carambola')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (61,'Centeio')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (62,'Cevada')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (63,'Chá-da-índia')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (64,'Cidra')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (65,'Coco-da-baía')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (66,'Cravo-da-índia')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (67,'Cupuaçu')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (68,'Dendê')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (69,'Ervilha')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (70,'Fava')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (71,'Figo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (72,'Flores')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (73,'Girassol')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (74,'Goiaba')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (75,'Grão-de-Bico')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (76,'Guaraná')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (77,'Inhame')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (78,'Kiwi')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (79,'Lentilha')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (80,'Limão')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (81,'Linho')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (82,'Malva')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (83,'Mamão')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (84,'Mamona')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (85,'Manga')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (86,'Maracujá')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (87,'Marmelo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (88,'Melancia')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (89,'Melão')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (90,'Milheto')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (96,'Não identificado')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (100,'Nabo forrageiro')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (101,'Noz')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (102,'Palmito')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (103,'Pepino')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (104,'Piaçava')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (105,'Pimenta-do-reino')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (106,'Plantas ornamentais')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (108,'Rami')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (110,'Sisal ou agave')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (111,'Sorgo')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (112,'Tangerina')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (113,'Tomate')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (114,'Triticale')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (115,'Tungue')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (116,'Urucum')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (117,'Gergelim')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (118,'Pupunha')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (119,'Lima')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (120,'Araçá')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (121,'Cultura rotativa')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (122,'Mandacaru')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (123,'Milho pipoca')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (124,'Morango')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (125,'Graviola')#
INSERT INTO dominios.cultivo_predominante (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.forma_rocha (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT forma_rocha_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.forma_rocha (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (21,'Matacão - pedra')#
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (22,'Penedo isolado')#
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (23,'Área rochosa - lajedo')#
INSERT INTO dominios.forma_rocha (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_hierarquia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_hierarquia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (23,'Estadual')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (24,'Internacional secundário')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (25,'Internacional de referência')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (26,'Internacional principal')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_hierarquia (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_transporte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_transporte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (21,'Passageiro')#
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (22,'Carga')#
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_transporte (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.sigla_uf (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT sigla_uf_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.sigla_uf (code,code_name) VALUES (1,'AC')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (2,'AL')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (3,'AM')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (4,'AP')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (5,'BA')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (6,'CE')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (7,'DF')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (8,'ES')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (9,'GO')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (10,'MA')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (11,'MG')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (12,'MS')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (13,'MT')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (14,'PA')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (15,'PB')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (16,'PE')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (17,'PI')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (18,'PR')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (19,'RJ')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (20,'RN')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (21,'RO')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (22,'RR')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (23,'RS')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (24,'SC')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (25,'SE')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (26,'SP')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (27,'TO')#
INSERT INTO dominios.sigla_uf (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.referencial_grav (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_grav_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.referencial_grav (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (1,'Potsdam 1930')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (2,'IGSN71')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (3,'Absoluto')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (4,'Local')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (5,'RGFB')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.referencial_grav (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_pista_comp (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pista_comp_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (1,'Atletismo')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (3,'Motociclismo')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (4,'Automobilismo')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (5,'Corrida de cavalos')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (6,'Bicicross')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (7,'Ciclismo')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (8,'Motocross')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_pista_comp (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.estado_fisico (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT estado_fisico_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.estado_fisico (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (1,'Líquido')#
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (2,'Sólido')#
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (3,'Gasoso')#
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.estado_fisico (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_travessia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_travessia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (1,'Vau natural')#
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (2,'Vau construída')#
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (3,'Bote transportador')#
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (4,'Balsa')#
INSERT INTO dominios.tipo_travessia (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_atracad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_atracad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (38,'Cais')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (39,'Cais flutuante')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (40,'Trapiche')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (41,'Molhe de atracação')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (42,'Píer')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (43,'Dolfim')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (44,'Desembarcadouro')#
INSERT INTO dominios.tipo_atracad (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.uso_principal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT uso_principal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.uso_principal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (1,'Irrigação')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (2,'Abastecimento')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (3,'Energia')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (4,'Lazer')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (5,'Dessedentação animal')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (6,'Drenagem')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.uso_principal (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.densidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT densidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.densidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.densidade (code,code_name) VALUES (1,'Alta')#
INSERT INTO dominios.densidade (code,code_name) VALUES (2,'Baixa')#
INSERT INTO dominios.densidade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.atividade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT atividade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.atividade (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.atividade (code,code_name) VALUES (9,'Prospecção')#
INSERT INTO dominios.atividade (code,code_name) VALUES (10,'Produção')#
INSERT INTO dominios.atividade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_ahe (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ahe_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ahe (code,code_name) VALUES (1,'UHE')#
INSERT INTO dominios.tipo_ahe (code,code_name) VALUES (2,'PCH')#
INSERT INTO dominios.tipo_ahe (code,code_name) VALUES (3,'CGH')#
INSERT INTO dominios.tipo_ahe (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_vegetacao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_vegetacao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (2,'Vegetação cultivada')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (3,'Floresta')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (4,'Vegetação de mangue')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (5,'Refúgio ecológico')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (6,'Campinarana')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (7,'Cerrado')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (8,'Vegetação de restinga')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (9,'Estepe')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (10,'Vegetação de brejo ou pântano')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (11,'Caatinga')#
INSERT INTO dominios.tipo_vegetacao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_curva_nivel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_curva_nivel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (1,'Mestra')#
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (2,'Normal')#
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (3,'Auxiliar')#
INSERT INTO dominios.tipo_curva_nivel (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.modalidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT modalidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.modalidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (1,'Radiocomunicação')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (2,'Imagem')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (3,'Telefonia')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (4,'Dados')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (5,'Som')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.modalidade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_instal_militar (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_instal_militar_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (5,'Aquartelamento')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (6,'Campo de instrução')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (7,'Campo de tiro')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (8,'Base aérea')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (9,'Distrito naval')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (10,'Hotel de trânsito')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (11,'Delegacia de serviço militar')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (12,'Quartel general')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (13,'Posto de vigilância')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (14,'Posto de policiamento urbano')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (15,'Posto de policiamento rodoviário')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (16,'Capitania dos portos')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (17,'Base naval')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_instal_militar (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.uso_pista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT uso_pista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.uso_pista (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (6,'Particular')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (11,'Público')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (12,'Militar')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (13,'Público compartilhado com uso militar')#
INSERT INTO dominios.uso_pista (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_combustivel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_combustivel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (1,'Nuclear')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (3,'Diesel')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (7,'Biomassa')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (33,'Carvão')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_combustivel (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_equip_agropec (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_equip_agropec_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (1,'Pivô central')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (2,'Moinho')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (3,'Elevador de grãos')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (4,'Moega')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (5,'Secador')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (6,'Tombador')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_equip_agropec (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_org_civil (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_org_civil_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (1,'Policial')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (2,'Prisional')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (3,'Cartorial')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (4,'Gestão')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (5,'Eleitoral')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (6,'Produção e/ou pesquisa')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (7,'Seguridade social')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (8,'Câmara municipal')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (9,'Assembleia legislativa')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (10,'Autarquia')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (11,'Delegacia de polícia civil')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (12,'Educação')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (13,'Fórum')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (14,'Fundação')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (15,'Procuradoria')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (16,'Secretaria')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (22,'Prefeitura')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_org_civil (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.modal_uso (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT modal_uso_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.modal_uso (code,code_name) VALUES (4,'Rodoviário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (5,'Ferroviário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (6,'Metroviário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (7,'Dutos')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (9,'Aeroportuário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (10,'Hidroviário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (14,'Portuário')#
INSERT INTO dominios.modal_uso (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.causa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT causa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.causa (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.causa (code,code_name) VALUES (2,'Absorção')#
INSERT INTO dominios.causa (code,code_name) VALUES (4,'Gruta ou fenda')#
INSERT INTO dominios.causa (code,code_name) VALUES (5,'Canalização')#
INSERT INTO dominios.causa (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

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
INSERT INTO dominios.regime (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.rede_referencia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT rede_referencia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.rede_referencia (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (2,'Estadual')#
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (14,'Nacional')#
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (15,'Privada')#
INSERT INTO dominios.rede_referencia (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.especie_trecho_energia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT especie_trecho_energia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (2,'Distribuição')#
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (3,'Transmissão')#
INSERT INTO dominios.especie_trecho_energia (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_rod (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_rod_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (8,'Terminal interestadual')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (9,'Terminal urbano')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (10,'Parada interestadual')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (13,'Posto de pedágio')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (15,'Administração')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (20,'Garagem')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_rod (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_area (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_area_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_area (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (1,'Área de propriedade particular')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (2,'Área habitacional')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (3,'Área relacionada a dutos')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (4,'Área relacionada a edificação agropecuária ou extrativismo vegetal ou pesca')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (5,'Área relacionada a edificação de comércio ou serviços')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (6,'Área relacionada a edificação de ensino')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (7,'Área relacionada a edificação de saúde')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (8,'Área relacionada a edificação industrial')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (9,'Área relacionada a edificação religiosa')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (10,'Área relacionada a energia elétrica')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (11,'Área relacionada a equipamentos de desenvolvimento social')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (12,'Área relacionada a estação de medição de fenômenos')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (13,'Área relacionada ao extrativismo mineral')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (14,'Área relacionada a instalação de abastecimento de água')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (15,'Área relacionada a instalação de comunicações')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (16,'Área relacionada a instalação de estrutura de transporte')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (17,'Área relacionada a instalação de saneamento')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (18,'Área relacionada ao lazer')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (19,'Área relacionada a ruínas de valor histórico')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_area (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_alter_antrop (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_alter_antrop_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (24,'Caixa de empréstimo')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (26,'Corte')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (27,'Aterro')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (28,'Resíduo de bota-fora')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (29,'Resíduo sólido em geral')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (30,'Canal')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (31,'Vala')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (32,'Área de extração mineral')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_alter_antrop (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_comunic (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_comunic_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (1,'Centro de operações')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (2,'Central comutação e transmissão')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (3,'Estação rádio base')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (4,'Estação repetidora')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (5,'Administração')#
INSERT INTO dominios.tipo_edif_comunic (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_tunel (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_tunel_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_tunel (code,code_name) VALUES (1,'Túnel')#
INSERT INTO dominios.tipo_tunel (code,code_name) VALUES (2,'Passagem subterrânea')#
INSERT INTO dominios.tipo_tunel (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.nr_linhas (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nr_linhas_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nr_linhas (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (1,'Simples')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (2,'Dupla')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (3,'Múltipla')#
INSERT INTO dominios.nr_linhas (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_pto_ref_geod_topo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pto_ref_geod_topo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (1,'Vértice de triangulação - VT')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (2,'Referência de nível - RN')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (3,'Estação gravimétrica - EG')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (4,'Estação de poligonal - EP')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (5,'Ponto astronômico - PA')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (6,'Ponto barométrico - B')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (7,'Ponto trigonométrico - RV')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (8,'Ponto de satélite - SAT')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_pto_ref_geod_topo (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_trecho_ferrov (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_trecho_ferrov_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (5,'Trecho para bonde')#
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (6,'Trecho para aeromóvel')#
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (7,'Trecho para trem')#
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (8,'Trecho para metrô')#
INSERT INTO dominios.tipo_trecho_ferrov (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.material_predominante (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT material_predominante_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.material_predominante (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (4,'Rocha')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (12,'Areia')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (13,'Areia fina')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (14,'Lama')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (15,'Argila')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (16,'Lodo')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (17,'Concha')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (19,'Seixo')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (20,'Coral')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (22,'Ervas marinhas')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (50,'Pedra')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.material_predominante (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_rep_diplomatica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_rep_diplomatica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_rep_diplomatica (code,code_name) VALUES (2,'Embaixada')#
INSERT INTO dominios.tipo_rep_diplomatica (code,code_name) VALUES (3,'Consulado')#
INSERT INTO dominios.tipo_rep_diplomatica (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_embarcacao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_embarcacao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (2,'Balsa')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (3,'Lancha')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (6,'Empurrador-balsa')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (7,'Embarcação de pequeno porte')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.tipo_embarcacao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_terreno_exposto (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_terreno_exposto_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (4,'Pedregoso')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (12,'Areia')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (23,'Terra')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (24,'Saibro')#
INSERT INTO dominios.tipo_terreno_exposto (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_delim_fis (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_delim_fis_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (1,'Cerca')#
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (2,'Muro')#
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (3,'Mureta')#
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (4,'Gradil')#
INSERT INTO dominios.tipo_delim_fis (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_banco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_banco_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_banco (code,code_name) VALUES (1,'Fluvial')#
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (2,'Marítimo')#
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (3,'Lacustre')#
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (4,'Cordão arenoso')#
INSERT INTO dominios.tipo_banco (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.local_equip_desenv_social (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT local_equip_desenv_social_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (1,'Terras Indígena')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (2,'Terras de População Ribeirinha')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (3,'Terras Quilombola')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (4,'Rural')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (5,'Urbano central')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (6,'Urbana periférica')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (7,'Outras Comunidades tradicionais')#
INSERT INTO dominios.local_equip_desenv_social (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_ref (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ref_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ref (code,code_name) VALUES (1,'Altimétrico')#
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (2,'Planimétrico')#
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (3,'Planialtimétrico')#
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (4,'Gravimétrico')#
INSERT INTO dominios.tipo_ref (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_pista (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pista_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pista (code,code_name) VALUES (9,'Pista de pouso')#
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (10,'Pista de taxiamento')#
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (11,'Heliponto')#
INSERT INTO dominios.tipo_pista (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.destinacao_cemiterio (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT destinacao_cemiterio_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.destinacao_cemiterio (code,code_name) VALUES (2,'Humanos')#
INSERT INTO dominios.destinacao_cemiterio (code,code_name) VALUES (3,'Animais')#
INSERT INTO dominios.destinacao_cemiterio (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_fonte_dagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_fonte_dagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (1,'Poço')#
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (2,'Poço artesiano')#
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (3,'Olho d''água')#
INSERT INTO dominios.tipo_fonte_dagua (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_aero (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_aero_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (15,'Administração')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (26,'Terminal de passageiros')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (27,'Terminal de cargas')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (28,'Torre de controle')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (29,'Hangar')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (30,'Serviço de combate a incêndios (SCI)')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_aero (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_entroncamento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_entroncamento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (1,'Cruzamento ou injunções simples')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (2,'Círculo')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (3,'Trevo')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (4,'Rótula')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (5,'Entroncamento ferroviário')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (99,'Outros tipos de entroncamento em nível')#
INSERT INTO dominios.tipo_entroncamento (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_est_gerad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_est_gerad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (5,'Eólica')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (6,'Solar')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (7,'Maré-motriz')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (8,'Hidrelétrica')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (9,'Termelétrica')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_est_gerad (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_juridica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_juridica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (1,'Delimitada')#
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (2,'Declarada')#
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (3,'Homologada ou demarcada')#
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (4,'Regularizada')#
INSERT INTO dominios.situacao_juridica (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_relig (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_relig_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (1,'Igreja')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (2,'Templo')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (3,'Centro')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (4,'Mosteiro')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (5,'Convento')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (6,'Mesquita')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (7,'Sinagoga')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (8,'Terreiro')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (9,'Capela mortuária')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (10,'Administração')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_relig (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.denominacao_associada (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT denominacao_associada_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (5,'Cristã')#
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (6,'Israelita')#
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (7,'Muçulmana')#
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (99,'Outras')#
INSERT INTO dominios.denominacao_associada (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_lavoura (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_lavoura_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (1,'Perene')#
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (2,'Semi-perene')#
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (3,'Anual')#
INSERT INTO dominios.tipo_lavoura (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_ilha (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ilha_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (1,'Fluvial')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (2,'Marítima')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (3,'Lacustre')#
INSERT INTO dominios.tipo_ilha (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_campo_quadra (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_campo_quadra_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (1,'Futebol')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (2,'Basquetebol')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (3,'Voleibol')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (4,'Pólo')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (5,'Hipismo')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (6,'Poliesportiva')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (7,'Tênis')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_campo_quadra (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_ponte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ponte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (1,'Móvel')#
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (2,'Pênsil')#
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (3,'Fixa')#
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (7,'Estaiada')#
INSERT INTO dominios.tipo_ponte (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_lazer (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_lazer_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (1,'Estádio')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (2,'Ginásio')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (3,'Museu')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (4,'Teatro')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (5,'Anfiteatro')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (6,'Espaço de exibição de filmes')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (7,'Centro cultural')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (8,'Plataforma de pesca')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (9,'Arquivo')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (10,'Biblioteca')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (11,'Centro de documentação')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (12,'Circo')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (13,'Concha acústica')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (14,'Conservatório')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (15,'Coreto ou tribuna')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (17,'Equipamentos culturais diversos')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (18,'Espaço de eventos e/ou cultural')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (19,'Galeria')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (21,'Quiosque')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (22,'Administração')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_lazer (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_galeria_bueiro (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_galeria_bueiro_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (1,'Abastecimento animal')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (2,'Abastecimento humano')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (3,'Abastecimento industrial')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (4,'Canalização de águas pluviais')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (5,'Canalização de curso d''água')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (6,'Canalização de efluentes domésticos')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (7,'Canalização de efluentes industriais')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (8,'Irrigação')#
INSERT INTO dominios.finalidade_galeria_bueiro (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.causa_exposicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT causa_exposicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (2,'Natural')#
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (3,'Artificial')#
INSERT INTO dominios.causa_exposicao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.qualid_agua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT qualid_agua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.qualid_agua (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (1,'Potável')#
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (2,'Não potável')#
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (3,'Mineral')#
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (4,'Salobra')#
INSERT INTO dominios.qualid_agua (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_exposicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_exposicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (3,'Fechado')#
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (4,'Coberto')#
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (5,'Céu aberto')#
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_exposicao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.especie (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT especie_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.especie (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.especie (code,code_name) VALUES (10,'Cipó')#
INSERT INTO dominios.especie (code,code_name) VALUES (11,'Bambu')#
INSERT INTO dominios.especie (code,code_name) VALUES (17,'Palmeira')#
INSERT INTO dominios.especie (code,code_name) VALUES (27,'Araucária')#
INSERT INTO dominios.especie (code,code_name) VALUES (37,'Sem predominância')#
INSERT INTO dominios.especie (code,code_name) VALUES (96,'Não identificado')#
INSERT INTO dominios.especie (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_equip_desenv_social (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_equip_desenv_social_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (1,'Banco de alimentos')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (2,'Barragem calçadão')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (3,'Bolsa verde')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (4,'Centro de convivência')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (5,'Centro POP')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (6,'Centro-dia')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (7,'Cisterna subterrânea')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (8,'Cisterna de polietileno')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (9,'Cisterna de placa')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (10,'Cozinha comunitária')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (11,'CRAS')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (12,'CREAS')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (13,'PAA')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (14,'PRONAF')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (15,'PRONATEC')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (16,'Restaurante popular')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (17,'Unidade de acolhimento para crianças e adolescentes')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (18,'Unidade de acolhimento para crianças e adolescentes (casa de passagem)')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (19,'Unidade de acolhimento para idosos')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (20,'Unidade de acolhimento para mulheres vítimas de violência')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (21,'Unidade de acolhimento para pessoas em situação de rua')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_equip_desenv_social (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_marco (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_marco_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_marco (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (1,'Bom')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (2,'Destruído')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (3,'Destruído sem chapa')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (4,'Destruído com chapa danificada')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (5,'Não encontrado')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (6,'Não visitado')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (7,'Não construído')#
INSERT INTO dominios.situacao_marco (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_caminho_aereo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_caminho_aereo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_caminho_aereo (code,code_name) VALUES (12,'Teleférico')#
INSERT INTO dominios.tipo_caminho_aereo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_caminho_aereo (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_obst (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_obst_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_obst (code,code_name) VALUES (4,'Natural')#
INSERT INTO dominios.tipo_obst (code,code_name) VALUES (5,'Artificial')#
INSERT INTO dominios.tipo_obst (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_produto_residuo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_produto_residuo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (6,'Grãos')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (16,'Vinhoto')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (17,'Estrume')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (18,'Cascalho')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (20,'Inseticida')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (21,'Folhagens')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (22,'Pedra (brita)')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (23,'Granito')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (24,'Mármore')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (25,'Bauxita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (26,'Manganês')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (27,'Talco')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (28,'Óleo diesel')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (29,'Gasolina')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (30,'Álcool')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (31,'Querosene')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (32,'Cobre')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (33,'Carvão mineral')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (34,'Sal')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (35,'Ferro')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (36,'Escória')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (37,'Ouro')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (38,'Diamante')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (39,'Prata')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (40,'Pedra preciosa')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (41,'Forragem')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (42,'Areia')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (43,'Saibro/piçarra')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (45,'Ágata')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (46,'Água')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (47,'Água marinha')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (48,'Água mineral')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (49,'Alexandrita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (50,'Ametista')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (51,'Amianto')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (52,'Argila')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (53,'Barita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (54,'Bentonita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (55,'Calcário')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (56,'Carvão vegetal')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (57,'Caulim')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (58,'Chorume')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (59,'Chumbo')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (60,'Citrino')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (61,'Crisoberilo')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (62,'Cristal de rocha')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (63,'Cromo')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (64,'Diatomita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (65,'Dolomito')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (66,'Esgoto')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (67,'Esmeralda')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (68,'Estanho')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (69,'Feldspato')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (70,'Fosfato')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (71,'Gipsita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (72,'Grafita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (73,'Granada')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (74,'Lítio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (75,'Lixo domiciliar e comercial')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (76,'Lixo séptico')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (77,'Lixo tóxico')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (78,'Magnesita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (79,'Mica')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (80,'Nióbio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (81,'Níquel')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (82,'Opala')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (83,'Rocha ornamental')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (84,'Sal-gema')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (85,'Terras raras')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (86,'Titânio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (87,'Topázio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (88,'Tório')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (89,'Tungstênio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (90,'Turfa')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (91,'Turmalina')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (92,'Urânio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (93,'Vermiculita')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (94,'Zinco')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (100,'Zircônio')#
INSERT INTO dominios.tipo_produto_residuo (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_massa_dagua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_massa_dagua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (1,'Rio')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (3,'Oceano')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (4,'Baía')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (5,'Enseada')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (6,'Meandro abandonado')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (7,'Lago ou lagoa')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (9,'Laguna')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (10,'Represa/açude')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_massa_dagua (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.classe_ativ_econ (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT classe_ativ_econ_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (2,'Produção de energia elétrica')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (3,'Transmissão de energia elétrica')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (4,'Distribuição de energia elétrica')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (5,'Captação, tratamento e distribuição de água')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (6,'Telecomunicações')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (7,'Administração pública em geral')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (8,'Seguridade social')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (9,'Regulação das atividades econômicas')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (10,'Atividades de apoio à administração pública')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (11,'Relações exteriores')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (12,'Defesa')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (13,'Justiça')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (14,'Segurança e ordem pública')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (15,'Defesa civil')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (16,'Regulação das atividades sociais e culturais')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (17,'Educação infantil - creche')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (18,'Educação infantil - pré-escola')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (19,'Ensino fundamental')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (20,'Ensino médio')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (21,'Educação superior - graduação')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (22,'Educação superior - graduação e pós-graduação')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (23,'Educação superior - pós-graduação e extensão')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (24,'Educação profissional de nível técnico')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (25,'Educação profissional de nível tecnológico')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (26,'Outras atividades de ensino')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (27,'Atendimento hospitalar (hospital)')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (28,'Atendimento às urgências e emergências (pronto-socorro)')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (29,'Atenção ambulatorial (posto e centro de saúde)')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (30,'Serviços de complementação diagnóstica ou terapêutica')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (31,'Atividades de organizações religiosas')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (32,'Outras atividades relacionadas com atenção à saúde (instituto de pesquisa)')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (33,'Serviços sociais com alojamento')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (34,'Serviços sociais sem alojamento')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (35,'Limpeza urbana e atividades relacionadas')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (36,'Serviços veterinários')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.classe_ativ_econ (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_agua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_agua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_agua (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (6,'Tratada')#
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (7,'Não tratada')#
INSERT INTO dominios.situacao_agua (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_em_agua (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_em_agua_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (4,'Emerso')#
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (5,'Submerso')#
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (7,'Cobre e descobre')#
INSERT INTO dominios.situacao_em_agua (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.auxiliar (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT auxiliar_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.auxiliar (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (1,'Sim')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (2,'Não')#
INSERT INTO dominios.auxiliar (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_fisica (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_fisica_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (1,'Abandonada')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (2,'Destruída')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (3,'Em construção')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (4,'Planejada')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (5,'Construída')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (6,'Construída, mas em obras')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.situacao_fisica (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_pavimentacao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pavimentacao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (2,'Asfalto')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (3,'Placa de concreto')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (4,'Pedra regular')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (5,'Ladrilho de concreto')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (6,'Paralelepípedo')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (7,'Pedra irregular')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_pavimentacao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_energia (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_energia_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (1,'Administração')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (2,'Oficinas')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (3,'Segurança')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (4,'Depósito')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (5,'Chaminé')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_energia (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.trafego (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT trafego_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.trafego (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.trafego (code,code_name) VALUES (1,'Permanente')#
INSERT INTO dominios.trafego (code,code_name) VALUES (2,'Periódico')#
INSERT INTO dominios.trafego (code,code_name) VALUES (4,'Temporário')#
INSERT INTO dominios.trafego (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_manguezal (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_manguezal_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (2,'Manguezal')#
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (3,'Manguezal tipo apicum')#
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (4,'Manguezal tipo salgado')#
INSERT INTO dominios.tipo_manguezal (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.posicao_rel_edific (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicao_rel_edific_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (14,'Isolada')#
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (17,'Adjacente à edificação')#
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (18,'Sobre edificação')#
INSERT INTO dominios.posicao_rel_edific (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.posicao_relativa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT posicao_relativa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (2,'Superfície')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (3,'Elevada')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (4,'Emersa')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (5,'Submersa')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (6,'Subterrânea')#
INSERT INTO dominios.posicao_relativa (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_campo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_campo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_campo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (1,'Sujo')#
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (2,'Limpo')#
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (3,'Rupestre')#
INSERT INTO dominios.tipo_campo (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_passag_viad (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_passag_viad_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_passag_viad (code,code_name) VALUES (5,'Passagem elevada')#
INSERT INTO dominios.tipo_passag_viad (code,code_name) VALUES (6,'Viaduto')#
INSERT INTO dominios.tipo_passag_viad (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_queda (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_queda_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_queda (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (1,'Cachoeira')#
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (2,'Salto')#
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (3,'Catarata')#
INSERT INTO dominios.tipo_queda (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_conteudo (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_conteudo_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (1,'Insumo')#
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (2,'Produto')#
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (3,'Resíduo')#
INSERT INTO dominios.tipo_conteudo (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_localidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_localidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (1,'Aglomerado rural')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (2,'Aglomerado rural de extensão urbana')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (3,'Aglomerado rural isolado')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (4,'Capital')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (5,'Cidade')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (6,'Vila')#
INSERT INTO dominios.tipo_localidade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.proximidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT proximidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.proximidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (14,'Isolada')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (15,'Adjacente')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (16,'Coincidente')#
INSERT INTO dominios.proximidade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_ext_min (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_ext_min_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (1,'Poço para água subterrânea')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (4,'Mina')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (5,'Garimpo')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (6,'Salina')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (8,'Poço de petróleo')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_ext_min (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_fundeadouro (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_fundeadouro_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (1,'Com limite definido')#
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (2,'Sem limite definido')#
INSERT INTO dominios.tipo_fundeadouro (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.classificacao_porte (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT classificacao_porte_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (2,'Rasteira')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (3,'Herbácea')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (4,'Arbórea')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (5,'Arbustiva')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (98,'Mista')#
INSERT INTO dominios.classificacao_porte (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_comerc_serv (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_comerc_serv_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (3,'Centro comercial')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (4,'Mercado público')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (5,'Centro de convenções')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (6,'Banca de jornal')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (7,'Hotel')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (8,'Restaurante')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (9,'Comércio de carnes')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (10,'Farmácia')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (11,'Banco')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (12,'Loja de conveniência')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (13,'Loja de materiais de construção e/ou ferragem')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (14,'Loja de móveis')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (15,'Loja de roupas e/ou tecidos')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (16,'Motel')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (17,'Oficina mecânica')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (18,'Outros comércios')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (19,'Posto de combustível')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (20,'Pousada')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (21,'Quiosque')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (22,'Quitanda')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (23,'Supermercado')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (24,'Venda de veículos')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (25,'Administração')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (26,'Centro de exposições')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (99,'Outros serviços')#
INSERT INTO dominios.tipo_edif_comerc_serv (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_costa (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_costa_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_costa (code,code_name) VALUES (10,'Contígua')#
INSERT INTO dominios.situacao_costa (code,code_name) VALUES (11,'Afastada')#
INSERT INTO dominios.situacao_costa (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.finalidade (code,code_name) VALUES (1,'Comercial')#
INSERT INTO dominios.finalidade (code,code_name) VALUES (2,'Residencial')#
INSERT INTO dominios.finalidade (code,code_name) VALUES (4,'Serviço')#
INSERT INTO dominios.finalidade (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.finalidade (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.referencial_altim (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT referencial_altim_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.referencial_altim (code,code_name) VALUES (1,'Torres')#
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (2,'Imbituba')#
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (3,'Santana')#
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (99,'Outra referência')#
INSERT INTO dominios.referencial_altim (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_pto_est_med (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_pto_est_med_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (1,'Climatológica principal - CP')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (2,'Climatológica auxiliar - CA')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (3,'Agroclimatológica - AC')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (4,'Pluviométrica - PL')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (5,'Eólica - EO')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (6,'Evaporimétrica - EV')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (7,'Solarimétrica - SL')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (8,'Radar metereológico - RD')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (9,'Radiossonda - RS')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (10,'Fluviométrica - FL')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (11,'Maregráfica - MA')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (12,'Marés terrestres-crosta')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (13,'Metero-maregráfica')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (14,'Hidrológica')#
INSERT INTO dominios.tipo_pto_est_med (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_recife (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_recife_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_recife (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (1,'Arenito')#
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (2,'Rochoso')#
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (20,'Coral')#
INSERT INTO dominios.tipo_recife (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_agropec (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_agropec_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (4,'Administração')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (12,'Sede operacional de fazenda')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (13,'Aviário')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (14,'Apiário')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (15,'Viveiro de plantas')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (16,'Viveiro para aquicultura')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (17,'Pocilga')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (18,'Curral')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_agropec (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_trecho_drenagem (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_trecho_drenagem_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (4,'Curso d''água')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (5,'Pluvial')#
INSERT INTO dominios.tipo_trecho_drenagem (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_cemiterio (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_cemiterio_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (1,'Crematório')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (2,'Parque')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (3,'Vertical')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (4,'Comum')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (5,'Túmulo isolado')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (6,'Horizontal/vertical')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_cemiterio (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_unid_uso_sust (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_unid_uso_sust_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (1,'Área de proteção ambiental - APA')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (2,'Área de relevante interesse ecológico – ARIE')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (3,'Floresta – FLO')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (4,'Reserva de desenvolvimento sustentável – RDS')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (5,'Reserva extrativista')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (6,'Reserva de fauna – REFAU')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (7,'Reserva particular de patrimônio natural – RPPN')#
INSERT INTO dominios.tipo_unid_uso_sust (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_port (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_port_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (15,'Administração')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (26,'Terminal de passageiros')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (27,'Terminal de cargas')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (32,'Armazém')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (33,'Estaleiro')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (34,'Dique de estaleiro')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (35,'Rampa transportadora')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (36,'Carreira')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (37,'Terminal de uso privativo')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_port (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_plataforma (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_plataforma_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_plataforma (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_posto_fisc (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_posto_fisc_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (10,'Tributação')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (12,'Fiscalização sanitária')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (13,'Posto de pesagem')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_posto_fisc (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_unid_protegida (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_unid_protegida_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (1,'Unidade de conservação não SNUC')#
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (2,'Unidade de proteção integral')#
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (3,'Unidade de uso sustentável')#
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (4,'Unidade de conservação')#
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (5,'Outras unidades protegidas')#
INSERT INTO dominios.tipo_unid_protegida (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_abast (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_abast_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (1,'Captação')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (2,'Tratamento')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (4,'Administração')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (98,'Misto')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_abast (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.proc_extracao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT proc_extracao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.proc_extracao (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (1,'Mecanizado')#
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (2,'Manual')#
INSERT INTO dominios.proc_extracao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_area_umida (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_area_umida_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (3,'Lamacento')#
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (4,'Arenoso')#
INSERT INTO dominios.tipo_area_umida (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.mat_transp (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT mat_transp_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.mat_transp (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (1,'Água')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (2,'Óleo')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (3,'Petróleo')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (4,'Nafta')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (5,'Gás')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (6,'Grãos')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (7,'Minério')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (8,'Efluentes')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (9,'Esgoto')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (29,'Gasolina')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (30,'Álcool')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (31,'Querosene')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.mat_transp (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_poco_mina (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_poco_mina_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (2,'Horizontal')#
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (3,'Vertical')#
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.tipo_poco_mina (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_metro_ferrov (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_metro_ferrov_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (15,'Administração')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (16,'Estação ferroviária de passageiros')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (17,'Estação metroviária')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (18,'Terminal ferroviário de cargas')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (19,'Terminal ferroviário de passageiros e cargas')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (20,'Oficina de manutenção')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_metro_ferrov (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.nivel_atencao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT nivel_atencao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (5,'Primário')#
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (6,'Secundário')#
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (7,'Terciário')#
INSERT INTO dominios.nivel_atencao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

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
INSERT INTO dominios.setor (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.revestimento (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT revestimento_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.revestimento (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (1,'Sem revestimento (leito natural)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (2,'Revestimento primário (solto)')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (3,'Pavimentado')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (4,'Madeira')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.revestimento (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_deposito (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_deposito_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (2,'Tratamento')#
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (4,'Distribuição')#
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (8,'Armazenamento')#
INSERT INTO dominios.finalidade_deposito (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_poste (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_poste_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_poste (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (2,'Iluminação')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (3,'Ornamental')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (4,'Rede elétrica')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (5,'Sinalização')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_poste (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.unidade_volume (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT unidade_volume_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.unidade_volume (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (1,'Litro')#
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (2,'Metro cúbico')#
INSERT INTO dominios.unidade_volume (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_edif_saneam (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_edif_saneam_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (3,'Recalque')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (5,'Tratamento de esgoto')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (6,'Usina de reciclagem')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (7,'Incinerador')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (8,'Administração')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_edif_saneam (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_sum_vert (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_sum_vert_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_sum_vert (code,code_name) VALUES (1,'Sumidouro')#
INSERT INTO dominios.tipo_sum_vert (code,code_name) VALUES (2,'Vertedouro')#
INSERT INTO dominios.tipo_sum_vert (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_elevador (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_elevador_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_elevador (code,code_name) VALUES (2,'Inclinado')#
INSERT INTO dominios.tipo_elevador (code,code_name) VALUES (3,'Vertical')#
INSERT INTO dominios.tipo_elevador (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_elem_nat (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_elem_nat_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (1,'Serra')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (2,'Morro')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (3,'Montanha')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (4,'Chapada')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (5,'Maciço')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (6,'Planalto')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (7,'Planície')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (8,'Escarpa')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (9,'Península')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (10,'Ponta')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (11,'Cabo')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (12,'Praia')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (13,'Falésia')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (14,'Talude')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (15,'Caverna')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (16,'Dolina')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (17,'Duna')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (18,'Falha')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (19,'Fenda')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (20,'Gruta')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (21,'Ilha')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (22,'Pico')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (23,'Rocha')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.tipo_elem_nat (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.mat_condutor (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT mat_condutor_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.mat_condutor (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (1,'Fibra ótica')#
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (2,'Fio metálico')#
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.mat_condutor (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.mat_constr (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT mat_constr_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.mat_constr (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (1,'Alvenaria')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (2,'Concreto')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (3,'Metal')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (4,'Rocha')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (5,'Madeira')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (8,'Fibra')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (23,'Terra')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.mat_constr (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.situacao_espacial (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT situacao_espacial_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (2,'Subterrânea')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (4,'Superposta nível 2')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (5,'Nível do solo')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (7,'Superposta nível 3')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (12,'Adjacente')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (13,'Superposta nível 1')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (97,'Não aplicável')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (99,'Outra')#
INSERT INTO dominios.situacao_espacial (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.tipo_associado (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT tipo_associado_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.tipo_associado (code,code_name) VALUES (1,'Cidade')#
INSERT INTO dominios.tipo_associado (code,code_name) VALUES (4,'Vila')#
INSERT INTO dominios.tipo_associado (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.finalidade_patio (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT finalidade_patio_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (2,'Depósito temporário de cargas e contêineres')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (3,'Estacionamento de veículos')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (4,'Estacionamento de locomotivas')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (5,'Estacionamento de aeronaves')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (6,'Manobra de cargas')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (7,'Manobra de veículos em geral')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (8,'Manutenção')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.finalidade_patio (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.jurisdicao (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT jurisdicao_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.jurisdicao (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (1,'Federal')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (2,'Estadual/Distrital')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (3,'Municipal')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (4,'Internacional')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (8,'Propriedade particular')#
INSERT INTO dominios.jurisdicao (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.destinado_a (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT destinado_a_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.destinado_a (code,code_name) VALUES (0,'Desconhecido')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (5,'Madeira')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (18,'Açaí')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (34,'Turfa')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (35,'Látex')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (36,'Castanha')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (37,'Carnaúba')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (38,'Coco')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (39,'Jaborandi')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (40,'Palmito')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (41,'Babaçu')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (43,'Pecuária')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (44,'Pesca')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (99,'Outros')#
INSERT INTO dominios.destinado_a (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE dominios.condicao_terreno (
	 code smallint NOT NULL,
	 code_name text NOT NULL,
	 CONSTRAINT condicao_terreno_pk PRIMARY KEY (code)
)#

INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (0,'Desconhecida')#
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (1,'Seco')#
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (2,'Irrigado')#
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (3,'Inundado')#
INSERT INTO dominios.condicao_terreno (code,code_name) VALUES (9999,'A SER PREENCHIDO')#

CREATE TABLE edgv.aer_pista_ponto_pouso_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipopista smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 usopista smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 largura real,
	 extensao real,
	 altitude real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT aer_pista_ponto_pouso_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aer_pista_ponto_pouso_l_geom ON edgv.aer_pista_ponto_pouso_l USING gist (geom)#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipo_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN tipopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN usopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN homologacao SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_l
	 ADD CONSTRAINT aer_pista_ponto_pouso_l_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.aer_pista_ponto_pouso_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.aer_pista_ponto_pouso_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipopista smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 usopista smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 largura real,
	 extensao real,
	 altitude real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT aer_pista_ponto_pouso_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aer_pista_ponto_pouso_p_geom ON edgv.aer_pista_ponto_pouso_p USING gist (geom)#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipo_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN tipopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN usopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN homologacao SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_p
	 ADD CONSTRAINT aer_pista_ponto_pouso_p_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.aer_pista_ponto_pouso_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.aer_pista_ponto_pouso_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipopista smallint NOT NULL,
	 revestimento smallint NOT NULL,
	 usopista smallint NOT NULL,
	 homologacao smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 largura real,
	 extensao real,
	 altitude real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aer_pista_ponto_pouso_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aer_pista_ponto_pouso_a_geom ON edgv.aer_pista_ponto_pouso_a USING gist (geom)#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_tipopista_fk FOREIGN KEY (tipopista)
	 REFERENCES dominios.tipo_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN tipopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_usopista_fk FOREIGN KEY (usopista)
	 REFERENCES dominios.uso_pista (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN usopista SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_homologacao_fk FOREIGN KEY (homologacao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN homologacao SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.aer_pista_ponto_pouso_a
	 ADD CONSTRAINT aer_pista_ponto_pouso_a_situacaofisica_check 
	 CHECK (situacaofisica = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.aer_pista_ponto_pouso_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.aux_moldura_a(
	 id serial NOT NULL,
	 escala varchar(255),
	 inom varchar(255),
	 mi varchar(255),
	 nome varchar(80),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT aux_moldura_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX aux_moldura_a_geom ON edgv.aux_moldura_a USING gist (geom)#

CREATE TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 idtsub integer,
	 centrodecarga smallint NOT NULL,
	 classeativecon smallint NOT NULL,
	 operacional smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_subest_transm_distrib_energia_eletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_subest_transm_distrib_energia_eletrica_a_geom ON edgv.enc_subest_transm_distrib_energia_eletrica_a USING gist (geom)#

ALTER TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a
	 ADD CONSTRAINT enc_subest_transm_distrib_energia_eletrica_a_classeativecon_fk FOREIGN KEY (classeativecon)
	 REFERENCES dominios.classe_ativ_econ (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a
	 ADD CONSTRAINT enc_subest_transm_distrib_energia_eletrica_a_classeativecon_check 
	 CHECK (classeativecon = ANY(ARRAY[3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a ALTER COLUMN classeativecon SET DEFAULT 9999#

ALTER TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a
	 ADD CONSTRAINT enc_subest_transm_distrib_energia_eletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_subest_transm_distrib_energia_eletrica_a ALTER COLUMN operacional SET DEFAULT 9999#

CREATE TABLE edgv.cbge_deposito_geral_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipodepgeral smallint,
	 matconstr smallint,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint,
	 tipoconteudo smallint,
	 unidadevolume smallint,
	 valorvolume real,
	 tratamento smallint NOT NULL,
	 estadofisico smallint,
	 finalidadedep smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT cbge_deposito_geral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_deposito_geral_p_geom ON edgv.cbge_deposito_geral_p USING gist (geom)#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipo_dep_geral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN tipodepgeral SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipo_exposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN tipoexposicao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN tipoprodutoresiduo SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipo_conteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN tipoconteudo SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidade_volume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN unidadevolume SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN tratamento SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_estadofisico_fk FOREIGN KEY (estadofisico)
	 REFERENCES dominios.estado_fisico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN estadofisico SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_p
	 ADD CONSTRAINT cbge_deposito_geral_p_finalidadedep_fk FOREIGN KEY (finalidadedep)
	 REFERENCES dominios.finalidade_deposito (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_p ALTER COLUMN finalidadedep SET DEFAULT 9999#

CREATE TABLE edgv.cbge_deposito_geral_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipodepgeral smallint,
	 matconstr smallint,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint,
	 tipoconteudo smallint,
	 unidadevolume smallint,
	 valorvolume real,
	 tratamento smallint NOT NULL,
	 estadofisico smallint,
	 finalidadedep smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_deposito_geral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_deposito_geral_a_geom ON edgv.cbge_deposito_geral_a USING gist (geom)#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipo_dep_geral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN tipodepgeral SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipo_exposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN tipoexposicao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN tipoprodutoresiduo SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipo_conteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN tipoconteudo SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidade_volume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN unidadevolume SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN tratamento SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_estadofisico_fk FOREIGN KEY (estadofisico)
	 REFERENCES dominios.estado_fisico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN estadofisico SET DEFAULT 9999#

ALTER TABLE edgv.cbge_deposito_geral_a
	 ADD CONSTRAINT cbge_deposito_geral_a_finalidadedep_fk FOREIGN KEY (finalidadedep)
	 REFERENCES dominios.finalidade_deposito (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_deposito_geral_a ALTER COLUMN finalidadedep SET DEFAULT 9999#

CREATE TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoarea smallint NOT NULL,
	 destinadoa smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_agropec_ext_vegetal_pesca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_agropec_ext_vegetal_pesca_a_geom ON edgv.cbge_area_agropec_ext_vegetal_pesca_a USING gist (geom)#

ALTER TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT cbge_area_agropec_ext_vegetal_pesca_a_tipoarea_fk FOREIGN KEY (tipoarea)
	 REFERENCES dominios.tipo_area (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT cbge_area_agropec_ext_vegetal_pesca_a_tipoarea_check 
	 CHECK (tipoarea = ANY(ARRAY[4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a ALTER COLUMN tipoarea SET DEFAULT 9999#

ALTER TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT cbge_area_agropec_ext_vegetal_pesca_a_destinadoa_fk FOREIGN KEY (destinadoa)
	 REFERENCES dominios.destinado_a (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_agropec_ext_vegetal_pesca_a ALTER COLUMN destinadoa SET DEFAULT 9999#

CREATE TABLE edgv.cbge_canteiro_central_l(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 situacaoespacial smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT cbge_canteiro_central_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_canteiro_central_l_geom ON edgv.cbge_canteiro_central_l USING gist (geom)#

ALTER TABLE edgv.cbge_canteiro_central_l
	 ADD CONSTRAINT cbge_canteiro_central_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_canteiro_central_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.cbge_canteiro_central_a(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 situacaoespacial smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_canteiro_central_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_canteiro_central_a_geom ON edgv.cbge_canteiro_central_a USING gist (geom)#

ALTER TABLE edgv.cbge_canteiro_central_a
	 ADD CONSTRAINT cbge_canteiro_central_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_canteiro_central_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.cbge_poste_p(
	 id serial NOT NULL,
	 codident varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint,
	 tipoposte smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT cbge_poste_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_poste_p_geom ON edgv.cbge_poste_p USING gist (geom)#

ALTER TABLE edgv.cbge_poste_p
	 ADD CONSTRAINT cbge_poste_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_poste_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.cbge_poste_p
	 ADD CONSTRAINT cbge_poste_p_tipoposte_fk FOREIGN KEY (tipoposte)
	 REFERENCES dominios.tipo_poste (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_poste_p ALTER COLUMN tipoposte SET DEFAULT 9999#

CREATE TABLE edgv.cbge_espelho_dagua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 codident varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_espelho_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_espelho_dagua_a_geom ON edgv.cbge_espelho_dagua_a USING gist (geom)#

CREATE TABLE edgv.cbge_entroncamento_area_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoentroncamento smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_entroncamento_area_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_entroncamento_area_a_geom ON edgv.cbge_entroncamento_area_a USING gist (geom)#

ALTER TABLE edgv.cbge_entroncamento_area_a
	 ADD CONSTRAINT cbge_entroncamento_area_a_tipoentroncamento_fk FOREIGN KEY (tipoentroncamento)
	 REFERENCES dominios.tipo_entroncamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_entroncamento_area_a ALTER COLUMN tipoentroncamento SET DEFAULT 9999#

CREATE TABLE edgv.cbge_retorno_l(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT cbge_retorno_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_retorno_l_geom ON edgv.cbge_retorno_l USING gist (geom)#

CREATE TABLE edgv.cbge_retorno_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT cbge_retorno_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_retorno_p_geom ON edgv.cbge_retorno_p USING gist (geom)#

CREATE TABLE edgv.cbge_trecho_arruamento_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(100),
	 revestimento smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 trafego smallint NOT NULL,
	 tipopavimentacao smallint NOT NULL,
	 tipovia smallint NOT NULL,
	 meiofio boolean NOT NULL,
	 sarjeta boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT cbge_trecho_arruamento_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_trecho_arruamento_l_geom ON edgv.cbge_trecho_arruamento_l USING gist (geom)#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN canteirodivisorio SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN trafego SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_l
	 ADD CONSTRAINT cbge_trecho_arruamento_l_tipovia_fk FOREIGN KEY (tipovia)
	 REFERENCES dominios.tipo_via (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_l ALTER COLUMN tipovia SET DEFAULT 9999#

CREATE TABLE edgv.cbge_trecho_arruamento_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(100),
	 revestimento smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 trafego smallint NOT NULL,
	 tipopavimentacao smallint NOT NULL,
	 tipovia smallint NOT NULL,
	 meiofio boolean NOT NULL,
	 sarjeta boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_trecho_arruamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_trecho_arruamento_a_geom ON edgv.cbge_trecho_arruamento_a USING gist (geom)#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN canteirodivisorio SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN trafego SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_trecho_arruamento_a
	 ADD CONSTRAINT cbge_trecho_arruamento_a_tipovia_fk FOREIGN KEY (tipovia)
	 REFERENCES dominios.tipo_via (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_trecho_arruamento_a ALTER COLUMN tipovia SET DEFAULT 9999#

CREATE TABLE edgv.cbge_cemiterio_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipocemiterio smallint NOT NULL,
	 denominacaoassociada smallint,
	 destinacaocemiterio smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT cbge_cemiterio_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_cemiterio_p_geom ON edgv.cbge_cemiterio_p USING gist (geom)#

ALTER TABLE edgv.cbge_cemiterio_p
	 ADD CONSTRAINT cbge_cemiterio_p_tipocemiterio_fk FOREIGN KEY (tipocemiterio)
	 REFERENCES dominios.tipo_cemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_p ALTER COLUMN tipocemiterio SET DEFAULT 9999#

ALTER TABLE edgv.cbge_cemiterio_p
	 ADD CONSTRAINT cbge_cemiterio_p_denominacaoassociada_fk FOREIGN KEY (denominacaoassociada)
	 REFERENCES dominios.denominacao_associada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_p ALTER COLUMN denominacaoassociada SET DEFAULT 9999#

ALTER TABLE edgv.cbge_cemiterio_p
	 ADD CONSTRAINT cbge_cemiterio_p_destinacaocemiterio_fk FOREIGN KEY (destinacaocemiterio)
	 REFERENCES dominios.destinacao_cemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_p ALTER COLUMN destinacaocemiterio SET DEFAULT 9999#

CREATE TABLE edgv.cbge_cemiterio_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipocemiterio smallint NOT NULL,
	 denominacaoassociada smallint,
	 destinacaocemiterio smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_cemiterio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_cemiterio_a_geom ON edgv.cbge_cemiterio_a USING gist (geom)#

ALTER TABLE edgv.cbge_cemiterio_a
	 ADD CONSTRAINT cbge_cemiterio_a_tipocemiterio_fk FOREIGN KEY (tipocemiterio)
	 REFERENCES dominios.tipo_cemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_a ALTER COLUMN tipocemiterio SET DEFAULT 9999#

ALTER TABLE edgv.cbge_cemiterio_a
	 ADD CONSTRAINT cbge_cemiterio_a_denominacaoassociada_fk FOREIGN KEY (denominacaoassociada)
	 REFERENCES dominios.denominacao_associada (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_a ALTER COLUMN denominacaoassociada SET DEFAULT 9999#

ALTER TABLE edgv.cbge_cemiterio_a
	 ADD CONSTRAINT cbge_cemiterio_a_destinacaocemiterio_fk FOREIGN KEY (destinacaocemiterio)
	 REFERENCES dominios.destinacao_cemiterio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_cemiterio_a ALTER COLUMN destinacaocemiterio SET DEFAULT 9999#

CREATE TABLE edgv.cbge_delimitacao_fisica_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipodelimfis smallint NOT NULL,
	 matconstr smallint,
	 eletrificada smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT cbge_delimitacao_fisica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_delimitacao_fisica_l_geom ON edgv.cbge_delimitacao_fisica_l USING gist (geom)#

ALTER TABLE edgv.cbge_delimitacao_fisica_l
	 ADD CONSTRAINT cbge_delimitacao_fisica_l_tipodelimfis_fk FOREIGN KEY (tipodelimfis)
	 REFERENCES dominios.tipo_delim_fis (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_delimitacao_fisica_l ALTER COLUMN tipodelimfis SET DEFAULT 9999#

ALTER TABLE edgv.cbge_delimitacao_fisica_l
	 ADD CONSTRAINT cbge_delimitacao_fisica_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_delimitacao_fisica_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.cbge_delimitacao_fisica_l
	 ADD CONSTRAINT cbge_delimitacao_fisica_l_eletrificada_fk FOREIGN KEY (eletrificada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_delimitacao_fisica_l ALTER COLUMN eletrificada SET DEFAULT 9999#

CREATE TABLE edgv.cbge_area_construida_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_construida_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_construida_a_geom ON edgv.cbge_area_construida_a USING gist (geom)#

CREATE TABLE edgv.cbge_area_habitacional_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoarea smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_habitacional_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_habitacional_a_geom ON edgv.cbge_area_habitacional_a USING gist (geom)#

ALTER TABLE edgv.cbge_area_habitacional_a
	 ADD CONSTRAINT cbge_area_habitacional_a_tipoarea_fk FOREIGN KEY (tipoarea)
	 REFERENCES dominios.tipo_area (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_habitacional_a
	 ADD CONSTRAINT cbge_area_habitacional_a_tipoarea_check 
	 CHECK (tipoarea = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_area_habitacional_a ALTER COLUMN tipoarea SET DEFAULT 9999#

CREATE TABLE edgv.cbge_estacionamento_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 administracao smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 finalidadepatio smallint NOT NULL,
	 publico boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_estacionamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_estacionamento_a_geom ON edgv.cbge_estacionamento_a USING gist (geom)#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_estacionamento_a ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_estacionamento_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_estacionamento_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_estacionamento_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_finalidadepatio_fk FOREIGN KEY (finalidadepatio)
	 REFERENCES dominios.finalidade_patio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_estacionamento_a
	 ADD CONSTRAINT cbge_estacionamento_a_finalidadepatio_check 
	 CHECK (finalidadepatio = ANY(ARRAY[3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_estacionamento_a ALTER COLUMN finalidadepatio SET DEFAULT 9999#

CREATE TABLE edgv.cbge_praca_a(
	 id serial NOT NULL,
	 nome varchar(80) NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 turistica boolean,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_praca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_praca_a_geom ON edgv.cbge_praca_a USING gist (geom)#

CREATE TABLE edgv.cbge_area_duto_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoarea smallint NOT NULL,
	 areavalvulas boolean,
	 bombeamento boolean,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_duto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_duto_a_geom ON edgv.cbge_area_duto_a USING gist (geom)#

ALTER TABLE edgv.cbge_area_duto_a
	 ADD CONSTRAINT cbge_area_duto_a_tipoarea_fk FOREIGN KEY (tipoarea)
	 REFERENCES dominios.tipo_area (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_duto_a
	 ADD CONSTRAINT cbge_area_duto_a_tipoarea_check 
	 CHECK (tipoarea = ANY(ARRAY[3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_area_duto_a ALTER COLUMN tipoarea SET DEFAULT 9999#

CREATE TABLE edgv.cbge_area_de_propriedade_particular_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoarea smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_de_propriedade_particular_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_de_propriedade_particular_a_geom ON edgv.cbge_area_de_propriedade_particular_a USING gist (geom)#

ALTER TABLE edgv.cbge_area_de_propriedade_particular_a
	 ADD CONSTRAINT cbge_area_de_propriedade_particular_a_tipoarea_fk FOREIGN KEY (tipoarea)
	 REFERENCES dominios.tipo_area (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_de_propriedade_particular_a
	 ADD CONSTRAINT cbge_area_de_propriedade_particular_a_tipoarea_check 
	 CHECK (tipoarea = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_area_de_propriedade_particular_a ALTER COLUMN tipoarea SET DEFAULT 9999#

CREATE TABLE edgv.cbge_quadra_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_quadra_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_quadra_a_geom ON edgv.cbge_quadra_a USING gist (geom)#

CREATE TABLE edgv.cbge_area_uso_especifico_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoarea smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_area_uso_especifico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_area_uso_especifico_a_geom ON edgv.cbge_area_uso_especifico_a USING gist (geom)#

ALTER TABLE edgv.cbge_area_uso_especifico_a
	 ADD CONSTRAINT cbge_area_uso_especifico_a_tipoarea_fk FOREIGN KEY (tipoarea)
	 REFERENCES dominios.tipo_area (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_area_uso_especifico_a
	 ADD CONSTRAINT cbge_area_uso_especifico_a_tipoarea_check 
	 CHECK (tipoarea = ANY(ARRAY[0 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 17 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.cbge_area_uso_especifico_a ALTER COLUMN tipoarea SET DEFAULT 9999#

CREATE TABLE edgv.cbge_passeio_l(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 largura real,
	 calcada smallint NOT NULL,
	 pavimentacao smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT cbge_passeio_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_passeio_l_geom ON edgv.cbge_passeio_l USING gist (geom)#

ALTER TABLE edgv.cbge_passeio_l
	 ADD CONSTRAINT cbge_passeio_l_calcada_fk FOREIGN KEY (calcada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_passeio_l ALTER COLUMN calcada SET DEFAULT 9999#

ALTER TABLE edgv.cbge_passeio_l
	 ADD CONSTRAINT cbge_passeio_l_pavimentacao_fk FOREIGN KEY (pavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_passeio_l ALTER COLUMN pavimentacao SET DEFAULT 9999#

CREATE TABLE edgv.cbge_passeio_a(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 largura real,
	 calcada smallint NOT NULL,
	 pavimentacao smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_passeio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_passeio_a_geom ON edgv.cbge_passeio_a USING gist (geom)#

ALTER TABLE edgv.cbge_passeio_a
	 ADD CONSTRAINT cbge_passeio_a_calcada_fk FOREIGN KEY (calcada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_passeio_a ALTER COLUMN calcada SET DEFAULT 9999#

ALTER TABLE edgv.cbge_passeio_a
	 ADD CONSTRAINT cbge_passeio_a_pavimentacao_fk FOREIGN KEY (pavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.cbge_passeio_a ALTER COLUMN pavimentacao SET DEFAULT 9999#

CREATE TABLE edgv.cbge_largo_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT cbge_largo_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX cbge_largo_a_geom ON edgv.cbge_largo_a USING gist (geom)#

CREATE TABLE edgv.dut_galeria_bueiro_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotrechoduto smallint NOT NULL,
	 mattransp smallint,
	 setor smallint NOT NULL,
	 posicaorelativa smallint,
	 matconstr smallint,
	 nrdutos integer,
	 situacaoespacial smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 finalidade smallint,
	 pesosuportmaximo real,
	 largura real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT dut_galeria_bueiro_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX dut_galeria_bueiro_l_geom ON edgv.dut_galeria_bueiro_l USING gist (geom)#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_tipotrechoduto_fk FOREIGN KEY (tipotrechoduto)
	 REFERENCES dominios.tipo_trecho_duto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_tipotrechoduto_check 
	 CHECK (tipotrechoduto = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN tipotrechoduto SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_mattransp_fk FOREIGN KEY (mattransp)
	 REFERENCES dominios.mat_transp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN mattransp SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_setor_fk FOREIGN KEY (setor)
	 REFERENCES dominios.setor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_setor_check 
	 CHECK (setor = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN setor SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_l
	 ADD CONSTRAINT dut_galeria_bueiro_l_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_l ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.dut_galeria_bueiro_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotrechoduto smallint NOT NULL,
	 mattransp smallint,
	 setor smallint NOT NULL,
	 posicaorelativa smallint,
	 matconstr smallint,
	 nrdutos integer,
	 situacaoespacial smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 finalidade smallint,
	 pesosuportmaximo real,
	 largura real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT dut_galeria_bueiro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX dut_galeria_bueiro_p_geom ON edgv.dut_galeria_bueiro_p USING gist (geom)#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_tipotrechoduto_fk FOREIGN KEY (tipotrechoduto)
	 REFERENCES dominios.tipo_trecho_duto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_tipotrechoduto_check 
	 CHECK (tipotrechoduto = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN tipotrechoduto SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_mattransp_fk FOREIGN KEY (mattransp)
	 REFERENCES dominios.mat_transp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN mattransp SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_setor_fk FOREIGN KEY (setor)
	 REFERENCES dominios.setor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_setor_check 
	 CHECK (setor = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN setor SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.dut_galeria_bueiro_p
	 ADD CONSTRAINT dut_galeria_bueiro_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_galeria_bueiro_p ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.dut_trecho_duto_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotrechoduto smallint NOT NULL,
	 mattransp smallint,
	 setor smallint NOT NULL,
	 posicaorelativa smallint,
	 matconstr smallint,
	 nrdutos integer,
	 situacaoespacial smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT dut_trecho_duto_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX dut_trecho_duto_l_geom ON edgv.dut_trecho_duto_l USING gist (geom)#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_tipotrechoduto_fk FOREIGN KEY (tipotrechoduto)
	 REFERENCES dominios.tipo_trecho_duto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_tipotrechoduto_check 
	 CHECK (tipotrechoduto = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN tipotrechoduto SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_mattransp_fk FOREIGN KEY (mattransp)
	 REFERENCES dominios.mat_transp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN mattransp SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_setor_fk FOREIGN KEY (setor)
	 REFERENCES dominios.setor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN setor SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.dut_trecho_duto_l
	 ADD CONSTRAINT dut_trecho_duto_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.dut_trecho_duto_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.eco_equip_agropec_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipoequipagropec smallint NOT NULL,
	 matconstr smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT eco_equip_agropec_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_l_geom ON edgv.eco_equip_agropec_l USING gist (geom)#

ALTER TABLE edgv.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipo_equip_agropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_l ALTER COLUMN tipoequipagropec SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_l
	 ADD CONSTRAINT eco_equip_agropec_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_l ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.eco_equip_agropec_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipoequipagropec smallint NOT NULL,
	 matconstr smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_equip_agropec_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_p_geom ON edgv.eco_equip_agropec_p USING gist (geom)#

ALTER TABLE edgv.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipo_equip_agropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_p ALTER COLUMN tipoequipagropec SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_p
	 ADD CONSTRAINT eco_equip_agropec_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_p ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.eco_equip_agropec_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipoequipagropec smallint NOT NULL,
	 matconstr smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_equip_agropec_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_equip_agropec_a_geom ON edgv.eco_equip_agropec_a USING gist (geom)#

ALTER TABLE edgv.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_tipoequipagropec_fk FOREIGN KEY (tipoequipagropec)
	 REFERENCES dominios.tipo_equip_agropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_a ALTER COLUMN tipoequipagropec SET DEFAULT 9999#

ALTER TABLE edgv.eco_equip_agropec_a
	 ADD CONSTRAINT eco_equip_agropec_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_equip_agropec_a ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.eco_ext_mineral_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 secaoativecon smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipoextmin smallint NOT NULL,
	 tipoproduto smallint NOT NULL,
	 tipopocomina smallint NOT NULL,
	 procextracao smallint,
	 formaextracao smallint NOT NULL,
	 atividade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_ext_mineral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_ext_mineral_p_geom ON edgv.eco_ext_mineral_p USING gist (geom)#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[32 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_secaoativecon_fk FOREIGN KEY (secaoativecon)
	 REFERENCES dominios.secao_ativ_econ (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_secaoativecon_check 
	 CHECK (secaoativecon = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN secaoativecon SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoextmin_fk FOREIGN KEY (tipoextmin)
	 REFERENCES dominios.tipo_ext_min (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN tipoextmin SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipoproduto_fk FOREIGN KEY (tipoproduto)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN tipoproduto SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_tipopocomina_fk FOREIGN KEY (tipopocomina)
	 REFERENCES dominios.tipo_poco_mina (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN tipopocomina SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_procextracao_fk FOREIGN KEY (procextracao)
	 REFERENCES dominios.proc_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN procextracao SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_formaextracao_fk FOREIGN KEY (formaextracao)
	 REFERENCES dominios.forma_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN formaextracao SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_p
	 ADD CONSTRAINT eco_ext_mineral_p_atividade_fk FOREIGN KEY (atividade)
	 REFERENCES dominios.atividade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_p ALTER COLUMN atividade SET DEFAULT 9999#

CREATE TABLE edgv.eco_ext_mineral_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 secaoativecon smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipoextmin smallint NOT NULL,
	 tipoproduto smallint NOT NULL,
	 tipopocomina smallint NOT NULL,
	 procextracao smallint,
	 formaextracao smallint NOT NULL,
	 atividade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_ext_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_ext_mineral_a_geom ON edgv.eco_ext_mineral_a USING gist (geom)#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[32 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_secaoativecon_fk FOREIGN KEY (secaoativecon)
	 REFERENCES dominios.secao_ativ_econ (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_secaoativecon_check 
	 CHECK (secaoativecon = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN secaoativecon SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoextmin_fk FOREIGN KEY (tipoextmin)
	 REFERENCES dominios.tipo_ext_min (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN tipoextmin SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipoproduto_fk FOREIGN KEY (tipoproduto)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN tipoproduto SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_tipopocomina_fk FOREIGN KEY (tipopocomina)
	 REFERENCES dominios.tipo_poco_mina (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN tipopocomina SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_procextracao_fk FOREIGN KEY (procextracao)
	 REFERENCES dominios.proc_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN procextracao SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_formaextracao_fk FOREIGN KEY (formaextracao)
	 REFERENCES dominios.forma_extracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN formaextracao SET DEFAULT 9999#

ALTER TABLE edgv.eco_ext_mineral_a
	 ADD CONSTRAINT eco_ext_mineral_a_atividade_fk FOREIGN KEY (atividade)
	 REFERENCES dominios.atividade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_ext_mineral_a ALTER COLUMN atividade SET DEFAULT 9999#

CREATE TABLE edgv.eco_plataforma_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoplataforma smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT eco_plataforma_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_plataforma_p_geom ON edgv.eco_plataforma_p USING gist (geom)#

ALTER TABLE edgv.eco_plataforma_p
	 ADD CONSTRAINT eco_plataforma_p_tipoplataforma_fk FOREIGN KEY (tipoplataforma)
	 REFERENCES dominios.tipo_plataforma (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_plataforma_p ALTER COLUMN tipoplataforma SET DEFAULT 9999#

CREATE TABLE edgv.eco_plataforma_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoplataforma smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT eco_plataforma_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX eco_plataforma_a_geom ON edgv.eco_plataforma_a USING gist (geom)#

ALTER TABLE edgv.eco_plataforma_a
	 ADD CONSTRAINT eco_plataforma_a_tipoplataforma_fk FOREIGN KEY (tipoplataforma)
	 REFERENCES dominios.tipo_plataforma (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.eco_plataforma_a ALTER COLUMN tipoplataforma SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_rodoviaria_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifrod smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_rodoviaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_rodoviaria_p_geom ON edgv.edf_edif_rodoviaria_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_tipoedifrod_fk FOREIGN KEY (tipoedifrod)
	 REFERENCES dominios.tipo_edif_rod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN tipoedifrod SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_p
	 ADD CONSTRAINT edf_edif_rodoviaria_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_rodoviaria_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifrod smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_rodoviaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_rodoviaria_a_geom ON edgv.edf_edif_rodoviaria_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_tipoedifrod_fk FOREIGN KEY (tipoedifrod)
	 REFERENCES dominios.tipo_edif_rod (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN tipoedifrod SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_rodoviaria_a
	 ADD CONSTRAINT edf_edif_rodoviaria_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_rodoviaria_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_turistica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifturist smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 tombada boolean,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_constr_turistica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_turistica_p_geom ON edgv.edf_edif_constr_turistica_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_turistica_check 
	 CHECK (turistica = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_tipoedifturist_fk FOREIGN KEY (tipoedifturist)
	 REFERENCES dominios.tipo_edif_turist (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN tipoedifturist SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_p
	 ADD CONSTRAINT edf_edif_constr_turistica_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_p ALTER COLUMN ovgd SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_turistica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifturist smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 tombada boolean,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_constr_turistica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_turistica_a_geom ON edgv.edf_edif_constr_turistica_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_turistica_check 
	 CHECK (turistica = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_tipoedifturist_fk FOREIGN KEY (tipoedifturist)
	 REFERENCES dominios.tipo_edif_turist (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN tipoedifturist SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_turistica_a
	 ADD CONSTRAINT edf_edif_constr_turistica_a_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_turistica_a ALTER COLUMN ovgd SET DEFAULT 9999#

CREATE TABLE edgv.edf_representacao_diplomatica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tiporepdiplomatica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_representacao_diplomatica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_representacao_diplomatica_p_geom ON edgv.edf_representacao_diplomatica_p USING gist (geom)#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_p
	 ADD CONSTRAINT edf_representacao_diplomatica_p_tiporepdiplomatica_fk FOREIGN KEY (tiporepdiplomatica)
	 REFERENCES dominios.tipo_rep_diplomatica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_p ALTER COLUMN tiporepdiplomatica SET DEFAULT 9999#

CREATE TABLE edgv.edf_representacao_diplomatica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tiporepdiplomatica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_representacao_diplomatica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_representacao_diplomatica_a_geom ON edgv.edf_representacao_diplomatica_a USING gist (geom)#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_representacao_diplomatica_a
	 ADD CONSTRAINT edf_representacao_diplomatica_a_tiporepdiplomatica_fk FOREIGN KEY (tiporepdiplomatica)
	 REFERENCES dominios.tipo_rep_diplomatica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_representacao_diplomatica_a ALTER COLUMN tiporepdiplomatica SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifagropec smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_agropec_ext_vegetal_pesca_p_geom ON edgv.edf_edif_agropec_ext_vegetal_pesca_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_p_tipoedifagropec_fk FOREIGN KEY (tipoedifagropec)
	 REFERENCES dominios.tipo_edif_agropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_p ALTER COLUMN tipoedifagropec SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifagropec smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_agropec_ext_vegetal_pesca_a_geom ON edgv.edf_edif_agropec_ext_vegetal_pesca_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a
	 ADD CONSTRAINT edf_edif_agropec_ext_vegetal_pesca_a_tipoedifagropec_fk FOREIGN KEY (tipoedifagropec)
	 REFERENCES dominios.tipo_edif_agropec (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_agropec_ext_vegetal_pesca_a ALTER COLUMN tipoedifagropec SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_aeroportuaria_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifaero smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_constr_aeroportuaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_aeroportuaria_p_geom ON edgv.edf_edif_constr_aeroportuaria_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_tipoedifaero_fk FOREIGN KEY (tipoedifaero)
	 REFERENCES dominios.tipo_edif_aero (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN tipoedifaero SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_aeroportuaria_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifaero smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_constr_aeroportuaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_aeroportuaria_a_geom ON edgv.edf_edif_constr_aeroportuaria_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_tipoedifaero_fk FOREIGN KEY (tipoedifaero)
	 REFERENCES dominios.tipo_edif_aero (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN tipoedifaero SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a
	 ADD CONSTRAINT edf_edif_constr_aeroportuaria_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_aeroportuaria_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_banheiro_publico_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_banheiro_publico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_banheiro_publico_p_geom ON edgv.edf_banheiro_publico_p USING gist (geom)#

ALTER TABLE edgv.edf_banheiro_publico_p
	 ADD CONSTRAINT edf_banheiro_publico_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_p
	 ADD CONSTRAINT edf_banheiro_publico_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_p
	 ADD CONSTRAINT edf_banheiro_publico_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_p
	 ADD CONSTRAINT edf_banheiro_publico_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_p
	 ADD CONSTRAINT edf_banheiro_publico_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_banheiro_publico_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_banheiro_publico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_banheiro_publico_a_geom ON edgv.edf_banheiro_publico_a USING gist (geom)#

ALTER TABLE edgv.edf_banheiro_publico_a
	 ADD CONSTRAINT edf_banheiro_publico_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_a
	 ADD CONSTRAINT edf_banheiro_publico_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_a
	 ADD CONSTRAINT edf_banheiro_publico_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_a
	 ADD CONSTRAINT edf_banheiro_publico_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_banheiro_publico_a
	 ADD CONSTRAINT edf_banheiro_publico_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_banheiro_publico_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_metro_ferroviaria_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifmetroferrov smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_metro_ferroviaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_metro_ferroviaria_p_geom ON edgv.edf_edif_metro_ferroviaria_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_tipoedifmetroferrov_fk FOREIGN KEY (tipoedifmetroferrov)
	 REFERENCES dominios.tipo_edif_metro_ferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN tipoedifmetroferrov SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_metro_ferroviaria_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifmetroferrov smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_metro_ferroviaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_metro_ferroviaria_a_geom ON edgv.edf_edif_metro_ferroviaria_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_tipoedifmetroferrov_fk FOREIGN KEY (tipoedifmetroferrov)
	 REFERENCES dominios.tipo_edif_metro_ferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN tipoedifmetroferrov SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a
	 ADD CONSTRAINT edf_edif_metro_ferroviaria_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_metro_ferroviaria_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_comerc_serv_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_comerc_serv_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_comerc_serv_p_geom ON edgv.edf_edif_comerc_serv_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipo_edif_comerc_serv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN tipoedifcomercserv SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_p
	 ADD CONSTRAINT edf_edif_comerc_serv_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_p ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_comerc_serv_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_comerc_serv_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_comerc_serv_a_geom ON edgv.edf_edif_comerc_serv_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipo_edif_comerc_serv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN tipoedifcomercserv SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comerc_serv_a
	 ADD CONSTRAINT edf_edif_comerc_serv_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comerc_serv_a ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_edificacao_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edificacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edificacao_p_geom ON edgv.edf_edificacao_p USING gist (geom)#

ALTER TABLE edgv.edf_edificacao_p
	 ADD CONSTRAINT edf_edificacao_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_p
	 ADD CONSTRAINT edf_edificacao_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_p
	 ADD CONSTRAINT edf_edificacao_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_p
	 ADD CONSTRAINT edf_edificacao_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_p
	 ADD CONSTRAINT edf_edificacao_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edificacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edificacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edificacao_a_geom ON edgv.edf_edificacao_a USING gist (geom)#

ALTER TABLE edgv.edf_edificacao_a
	 ADD CONSTRAINT edf_edificacao_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_a
	 ADD CONSTRAINT edf_edificacao_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_a
	 ADD CONSTRAINT edf_edificacao_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_a
	 ADD CONSTRAINT edf_edificacao_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edificacao_a
	 ADD CONSTRAINT edf_edificacao_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edificacao_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_saude_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 nivelatencao smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_saude_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_saude_p_geom ON edgv.edf_edif_saude_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_p
	 ADD CONSTRAINT edf_edif_saude_p_nivelatencao_fk FOREIGN KEY (nivelatencao)
	 REFERENCES dominios.nivel_atencao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_p ALTER COLUMN nivelatencao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_saude_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 nivelatencao smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_saude_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_saude_a_geom ON edgv.edf_edif_saude_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saude_a
	 ADD CONSTRAINT edf_edif_saude_a_nivelatencao_fk FOREIGN KEY (nivelatencao)
	 REFERENCES dominios.nivel_atencao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saude_a ALTER COLUMN nivelatencao SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_guarda_municipal_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_posto_guarda_municipal_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_guarda_municipal_p_geom ON edgv.edf_posto_guarda_municipal_p USING gist (geom)#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_p
	 ADD CONSTRAINT edf_posto_guarda_municipal_p_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_p ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_guarda_municipal_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_posto_guarda_municipal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_guarda_municipal_a_geom ON edgv.edf_posto_guarda_municipal_a USING gist (geom)#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_guarda_municipal_a
	 ADD CONSTRAINT edf_posto_guarda_municipal_a_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_guarda_municipal_a ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_abast_agua_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifabast smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_abast_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_abast_agua_p_geom ON edgv.edf_edif_abast_agua_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_p
	 ADD CONSTRAINT edf_edif_abast_agua_p_tipoedifabast_fk FOREIGN KEY (tipoedifabast)
	 REFERENCES dominios.tipo_edif_abast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_p ALTER COLUMN tipoedifabast SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_abast_agua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifabast smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_abast_agua_a_geom ON edgv.edf_edif_abast_agua_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_abast_agua_a
	 ADD CONSTRAINT edf_edif_abast_agua_a_tipoedifabast_fk FOREIGN KEY (tipoedifabast)
	 REFERENCES dominios.tipo_edif_abast (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_abast_agua_a ALTER COLUMN tipoedifabast SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_fiscal_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 tipopostofisc smallint NOT NULL,
	 concessionaria varchar(100),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_posto_fiscal_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_fiscal_p_geom ON edgv.edf_posto_fiscal_p USING gist (geom)#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_p
	 ADD CONSTRAINT edf_posto_fiscal_p_tipopostofisc_fk FOREIGN KEY (tipopostofisc)
	 REFERENCES dominios.tipo_posto_fisc (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_p ALTER COLUMN tipopostofisc SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_fiscal_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 tipopostofisc smallint NOT NULL,
	 concessionaria varchar(100),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_posto_fiscal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_fiscal_a_geom ON edgv.edf_posto_fiscal_a USING gist (geom)#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_fiscal_a
	 ADD CONSTRAINT edf_posto_fiscal_a_tipopostofisc_fk FOREIGN KEY (tipopostofisc)
	 REFERENCES dominios.tipo_posto_fisc (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_fiscal_a ALTER COLUMN tipopostofisc SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_religiosa_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifrelig smallint NOT NULL,
	 ensino smallint NOT NULL,
	 religiao varchar(100),
	 crista boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_religiosa_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_religiosa_p_geom ON edgv.edf_edif_religiosa_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_tipoedifrelig_fk FOREIGN KEY (tipoedifrelig)
	 REFERENCES dominios.tipo_edif_relig (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN tipoedifrelig SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_p
	 ADD CONSTRAINT edf_edif_religiosa_p_ensino_fk FOREIGN KEY (ensino)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_p ALTER COLUMN ensino SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_religiosa_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifrelig smallint NOT NULL,
	 ensino smallint NOT NULL,
	 religiao varchar(100),
	 crista boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_religiosa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_religiosa_a_geom ON edgv.edf_edif_religiosa_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_tipoedifrelig_fk FOREIGN KEY (tipoedifrelig)
	 REFERENCES dominios.tipo_edif_relig (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN tipoedifrelig SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_religiosa_a
	 ADD CONSTRAINT edf_edif_religiosa_a_ensino_fk FOREIGN KEY (ensino)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_religiosa_a ALTER COLUMN ensino SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_ext_mineral_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_ext_mineral_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_ext_mineral_p_geom ON edgv.edf_edif_ext_mineral_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_ext_mineral_p
	 ADD CONSTRAINT edf_edif_ext_mineral_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_p
	 ADD CONSTRAINT edf_edif_ext_mineral_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_p
	 ADD CONSTRAINT edf_edif_ext_mineral_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_p
	 ADD CONSTRAINT edf_edif_ext_mineral_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_p
	 ADD CONSTRAINT edf_edif_ext_mineral_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_ext_mineral_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_ext_mineral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_ext_mineral_a_geom ON edgv.edf_edif_ext_mineral_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_ext_mineral_a
	 ADD CONSTRAINT edf_edif_ext_mineral_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_a
	 ADD CONSTRAINT edf_edif_ext_mineral_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_a
	 ADD CONSTRAINT edf_edif_ext_mineral_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_a
	 ADD CONSTRAINT edf_edif_ext_mineral_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ext_mineral_a
	 ADD CONSTRAINT edf_edif_ext_mineral_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ext_mineral_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_est_med_fen_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_constr_est_med_fen_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_est_med_fen_p_geom ON edgv.edf_edif_constr_est_med_fen_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_est_med_fen_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_constr_est_med_fen_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_est_med_fen_a_geom ON edgv.edf_edif_constr_est_med_fen_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a
	 ADD CONSTRAINT edf_edif_constr_est_med_fen_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_est_med_fen_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_ensino_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_ensino_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_ensino_p_geom ON edgv.edf_edif_ensino_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_ensino_p
	 ADD CONSTRAINT edf_edif_ensino_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_p
	 ADD CONSTRAINT edf_edif_ensino_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_p
	 ADD CONSTRAINT edf_edif_ensino_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_p
	 ADD CONSTRAINT edf_edif_ensino_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_p
	 ADD CONSTRAINT edf_edif_ensino_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_ensino_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_ensino_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_ensino_a_geom ON edgv.edf_edif_ensino_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_ensino_a
	 ADD CONSTRAINT edf_edif_ensino_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_a
	 ADD CONSTRAINT edf_edif_ensino_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_a
	 ADD CONSTRAINT edf_edif_ensino_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_a
	 ADD CONSTRAINT edf_edif_ensino_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_ensino_a
	 ADD CONSTRAINT edf_edif_ensino_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_ensino_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_combustivel_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_posto_combustivel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_combustivel_p_geom ON edgv.edf_posto_combustivel_p USING gist (geom)#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipo_edif_comerc_serv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_tipoedifcomercserv_check 
	 CHECK (tipoedifcomercserv = ANY(ARRAY[19 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN tipoedifcomercserv SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_p
	 ADD CONSTRAINT edf_posto_combustivel_p_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_p ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_combustivel_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomercserv smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_posto_combustivel_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_combustivel_a_geom ON edgv.edf_posto_combustivel_a USING gist (geom)#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_tipoedifcomercserv_fk FOREIGN KEY (tipoedifcomercserv)
	 REFERENCES dominios.tipo_edif_comerc_serv (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_tipoedifcomercserv_check 
	 CHECK (tipoedifcomercserv = ANY(ARRAY[19 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN tipoedifcomercserv SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_combustivel_a
	 ADD CONSTRAINT edf_posto_combustivel_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_combustivel_a ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_policia_militar_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoinstalmilitar smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_posto_policia_militar_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_policia_militar_p_geom ON edgv.edf_posto_policia_militar_p USING gist (geom)#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_tipoinstalmilitar_fk FOREIGN KEY (tipoinstalmilitar)
	 REFERENCES dominios.tipo_instal_militar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_p
	 ADD CONSTRAINT edf_posto_policia_militar_p_tipoinstalmilitar_check 
	 CHECK (tipoinstalmilitar = ANY(ARRAY[14 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_p ALTER COLUMN tipoinstalmilitar SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_policia_militar_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoinstalmilitar smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_posto_policia_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_policia_militar_a_geom ON edgv.edf_posto_policia_militar_a USING gist (geom)#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_tipoinstalmilitar_fk FOREIGN KEY (tipoinstalmilitar)
	 REFERENCES dominios.tipo_instal_militar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_militar_a
	 ADD CONSTRAINT edf_posto_policia_militar_a_tipoinstalmilitar_check 
	 CHECK (tipoinstalmilitar = ANY(ARRAY[14 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_militar_a ALTER COLUMN tipoinstalmilitar SET DEFAULT 9999#

CREATE TABLE edgv.edf_hab_indigena_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 coletiva smallint NOT NULL,
	 isolada smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_hab_indigena_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_hab_indigena_p_geom ON edgv.edf_hab_indigena_p USING gist (geom)#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_coletiva_fk FOREIGN KEY (coletiva)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN coletiva SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_p
	 ADD CONSTRAINT edf_hab_indigena_p_isolada_fk FOREIGN KEY (isolada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_p ALTER COLUMN isolada SET DEFAULT 9999#

CREATE TABLE edgv.edf_hab_indigena_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 coletiva smallint NOT NULL,
	 isolada smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_hab_indigena_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_hab_indigena_a_geom ON edgv.edf_hab_indigena_a USING gist (geom)#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_coletiva_fk FOREIGN KEY (coletiva)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN coletiva SET DEFAULT 9999#

ALTER TABLE edgv.edf_hab_indigena_a
	 ADD CONSTRAINT edf_hab_indigena_a_isolada_fk FOREIGN KEY (isolada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_hab_indigena_a ALTER COLUMN isolada SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_desenv_social_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 sigla varchar(80),
	 codequipdesenvsocial varchar(80),
	 localizacaoequipdesenvsocial smallint,
	 tipoequipdesenvsocial smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_desenv_social_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_desenv_social_p_geom ON edgv.edf_edif_desenv_social_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_localizacaoequipdesenvsocial_fk FOREIGN KEY (localizacaoequipdesenvsocial)
	 REFERENCES dominios.local_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN localizacaoequipdesenvsocial SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_p
	 ADD CONSTRAINT edf_edif_desenv_social_p_tipoequipdesenvsocial_fk FOREIGN KEY (tipoequipdesenvsocial)
	 REFERENCES dominios.tipo_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_p ALTER COLUMN tipoequipdesenvsocial SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_desenv_social_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 sigla varchar(80),
	 codequipdesenvsocial varchar(80),
	 localizacaoequipdesenvsocial smallint,
	 tipoequipdesenvsocial smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_desenv_social_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_desenv_social_a_geom ON edgv.edf_edif_desenv_social_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_localizacaoequipdesenvsocial_fk FOREIGN KEY (localizacaoequipdesenvsocial)
	 REFERENCES dominios.local_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN localizacaoequipdesenvsocial SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_desenv_social_a
	 ADD CONSTRAINT edf_edif_desenv_social_a_tipoequipdesenvsocial_fk FOREIGN KEY (tipoequipdesenvsocial)
	 REFERENCES dominios.tipo_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_desenv_social_a ALTER COLUMN tipoequipdesenvsocial SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_lazer_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoediflazer smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_constr_lazer_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_lazer_p_geom ON edgv.edf_edif_constr_lazer_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_p
	 ADD CONSTRAINT edf_edif_constr_lazer_p_tipoediflazer_fk FOREIGN KEY (tipoediflazer)
	 REFERENCES dominios.tipo_edif_lazer (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_p ALTER COLUMN tipoediflazer SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_lazer_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoediflazer smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_constr_lazer_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_lazer_a_geom ON edgv.edf_edif_constr_lazer_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_lazer_a
	 ADD CONSTRAINT edf_edif_constr_lazer_a_tipoediflazer_fk FOREIGN KEY (tipoediflazer)
	 REFERENCES dominios.tipo_edif_lazer (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_lazer_a ALTER COLUMN tipoediflazer SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_energia_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifenergia smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_energia_p_geom ON edgv.edf_edif_energia_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_p
	 ADD CONSTRAINT edf_edif_energia_p_tipoedifenergia_fk FOREIGN KEY (tipoedifenergia)
	 REFERENCES dominios.tipo_edif_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_p ALTER COLUMN tipoedifenergia SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_energia_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifenergia smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_energia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_energia_a_geom ON edgv.edf_edif_energia_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_energia_a
	 ADD CONSTRAINT edf_edif_energia_a_tipoedifenergia_fk FOREIGN KEY (tipoedifenergia)
	 REFERENCES dominios.tipo_edif_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_energia_a ALTER COLUMN tipoedifenergia SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_industrial_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 chamine smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_industrial_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_industrial_p_geom ON edgv.edf_edif_industrial_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_p
	 ADD CONSTRAINT edf_edif_industrial_p_chamine_fk FOREIGN KEY (chamine)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_p ALTER COLUMN chamine SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_industrial_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 chamine smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_industrial_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_industrial_a_geom ON edgv.edf_edif_industrial_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_industrial_a
	 ADD CONSTRAINT edf_edif_industrial_a_chamine_fk FOREIGN KEY (chamine)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_industrial_a ALTER COLUMN chamine SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_portuaria_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifport smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_constr_portuaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_portuaria_p_geom ON edgv.edf_edif_constr_portuaria_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_tipoedifport_fk FOREIGN KEY (tipoedifport)
	 REFERENCES dominios.tipo_edif_port (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN tipoedifport SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_p
	 ADD CONSTRAINT edf_edif_constr_portuaria_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_constr_portuaria_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifport smallint NOT NULL,
	 jurisdicao smallint,
	 concessionaria varchar(100),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_constr_portuaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_constr_portuaria_a_geom ON edgv.edf_edif_constr_portuaria_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_tipoedifport_fk FOREIGN KEY (tipoedifport)
	 REFERENCES dominios.tipo_edif_port (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN tipoedifport SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_constr_portuaria_a
	 ADD CONSTRAINT edf_edif_constr_portuaria_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_constr_portuaria_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_comunic_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomunic smallint NOT NULL,
	 modalidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_comunic_p_geom ON edgv.edf_edif_comunic_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_tipoedifcomunic_fk FOREIGN KEY (tipoedifcomunic)
	 REFERENCES dominios.tipo_edif_comunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN tipoedifcomunic SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_p
	 ADD CONSTRAINT edf_edif_comunic_p_modalidade_fk FOREIGN KEY (modalidade)
	 REFERENCES dominios.modalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_p ALTER COLUMN modalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_comunic_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifcomunic smallint NOT NULL,
	 modalidade smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_comunic_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_comunic_a_geom ON edgv.edf_edif_comunic_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_tipoedifcomunic_fk FOREIGN KEY (tipoedifcomunic)
	 REFERENCES dominios.tipo_edif_comunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN tipoedifcomunic SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_comunic_a
	 ADD CONSTRAINT edf_edif_comunic_a_modalidade_fk FOREIGN KEY (modalidade)
	 REFERENCES dominios.modalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_comunic_a ALTER COLUMN modalidade SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_policia_rod_federal_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_posto_policia_rod_federal_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_policia_rod_federal_p_geom ON edgv.edf_posto_policia_rod_federal_p USING gist (geom)#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_p
	 ADD CONSTRAINT edf_posto_policia_rod_federal_p_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_p ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_posto_policia_rod_federal_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_posto_policia_rod_federal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_posto_policia_rod_federal_a_geom ON edgv.edf_posto_policia_rod_federal_a USING gist (geom)#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_posto_policia_rod_federal_a
	 ADD CONSTRAINT edf_posto_policia_rod_federal_a_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_posto_policia_rod_federal_a ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_pub_civil_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_pub_civil_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_pub_civil_p_geom ON edgv.edf_edif_pub_civil_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_p
	 ADD CONSTRAINT edf_edif_pub_civil_p_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 22 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_civil_p ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_pub_civil_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_pub_civil_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_pub_civil_a_geom ON edgv.edf_edif_pub_civil_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_civil_a
	 ADD CONSTRAINT edf_edif_pub_civil_a_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[0 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 15 :: SMALLINT, 16 :: SMALLINT, 22 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_civil_a ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_saneamento_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifsaneam smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_saneamento_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_saneamento_p_geom ON edgv.edf_edif_saneamento_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_p
	 ADD CONSTRAINT edf_edif_saneamento_p_tipoedifsaneam_fk FOREIGN KEY (tipoedifsaneam)
	 REFERENCES dominios.tipo_edif_saneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_p ALTER COLUMN tipoedifsaneam SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_saneamento_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipoedifsaneam smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_saneamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_saneamento_a_geom ON edgv.edf_edif_saneamento_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_saneamento_a
	 ADD CONSTRAINT edf_edif_saneamento_a_tipoedifsaneam_fk FOREIGN KEY (tipoedifsaneam)
	 REFERENCES dominios.tipo_edif_saneam (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_saneamento_a ALTER COLUMN tipoedifsaneam SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_policia_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_policia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_policia_p_geom ON edgv.edf_edif_policia_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_p
	 ADD CONSTRAINT edf_edif_policia_p_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 11 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_p ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_policia_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoedifpubcivil smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_policia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_policia_a_geom ON edgv.edf_edif_policia_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_tipoedifpubcivil_fk FOREIGN KEY (tipoedifpubcivil)
	 REFERENCES dominios.tipo_org_civil (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_policia_a
	 ADD CONSTRAINT edf_edif_policia_a_tipoedifpubcivil_check 
	 CHECK (tipoedifpubcivil = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 11 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_policia_a ALTER COLUMN tipoedifpubcivil SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_pub_militar_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoinstalmilitar smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_pub_militar_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_pub_militar_p_geom ON edgv.edf_edif_pub_militar_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_p
	 ADD CONSTRAINT edf_edif_pub_militar_p_tipoinstalmilitar_fk FOREIGN KEY (tipoinstalmilitar)
	 REFERENCES dominios.tipo_instal_militar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_p ALTER COLUMN tipoinstalmilitar SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_pub_militar_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 tipousoedif smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 tipoinstalmilitar smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_pub_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_pub_militar_a_geom ON edgv.edf_edif_pub_militar_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN cultura SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_tipousoedif_fk FOREIGN KEY (tipousoedif)
	 REFERENCES dominios.tipo_uso_edif (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_tipousoedif_check 
	 CHECK (tipousoedif = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN tipousoedif SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_pub_militar_a
	 ADD CONSTRAINT edf_edif_pub_militar_a_tipoinstalmilitar_fk FOREIGN KEY (tipoinstalmilitar)
	 REFERENCES dominios.tipo_instal_militar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_pub_militar_a ALTER COLUMN tipoinstalmilitar SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_residencial_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT edf_edif_residencial_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_residencial_p_geom ON edgv.edf_edif_residencial_p USING gist (geom)#

ALTER TABLE edgv.edf_edif_residencial_p
	 ADD CONSTRAINT edf_edif_residencial_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_p
	 ADD CONSTRAINT edf_edif_residencial_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_p
	 ADD CONSTRAINT edf_edif_residencial_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_p
	 ADD CONSTRAINT edf_edif_residencial_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_p
	 ADD CONSTRAINT edf_edif_residencial_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.edf_edif_residencial_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 matconstr smallint,
	 alturaaproximada real,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT edf_edif_residencial_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX edf_edif_residencial_a_geom ON edgv.edf_edif_residencial_a USING gist (geom)#

ALTER TABLE edgv.edf_edif_residencial_a
	 ADD CONSTRAINT edf_edif_residencial_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_a
	 ADD CONSTRAINT edf_edif_residencial_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_a
	 ADD CONSTRAINT edf_edif_residencial_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_a
	 ADD CONSTRAINT edf_edif_residencial_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.edf_edif_residencial_a
	 ADD CONSTRAINT edf_edif_residencial_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.edf_edif_residencial_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.emu_acesso_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT emu_acesso_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_acesso_l_geom ON edgv.emu_acesso_l USING gist (geom)#

ALTER TABLE edgv.emu_acesso_l
	 ADD CONSTRAINT emu_acesso_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_l
	 ADD CONSTRAINT emu_acesso_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_l
	 ADD CONSTRAINT emu_acesso_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_l
	 ADD CONSTRAINT emu_acesso_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_acesso_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT emu_acesso_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_acesso_p_geom ON edgv.emu_acesso_p USING gist (geom)#

ALTER TABLE edgv.emu_acesso_p
	 ADD CONSTRAINT emu_acesso_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_p
	 ADD CONSTRAINT emu_acesso_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_p
	 ADD CONSTRAINT emu_acesso_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_p
	 ADD CONSTRAINT emu_acesso_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_acesso_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT emu_acesso_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_acesso_a_geom ON edgv.emu_acesso_a USING gist (geom)#

ALTER TABLE edgv.emu_acesso_a
	 ADD CONSTRAINT emu_acesso_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_a
	 ADD CONSTRAINT emu_acesso_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_a
	 ADD CONSTRAINT emu_acesso_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_acesso_a
	 ADD CONSTRAINT emu_acesso_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_acesso_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_rampa_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT emu_rampa_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_rampa_l_geom ON edgv.emu_rampa_l USING gist (geom)#

ALTER TABLE edgv.emu_rampa_l
	 ADD CONSTRAINT emu_rampa_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_l
	 ADD CONSTRAINT emu_rampa_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_l
	 ADD CONSTRAINT emu_rampa_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_l
	 ADD CONSTRAINT emu_rampa_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_rampa_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT emu_rampa_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_rampa_p_geom ON edgv.emu_rampa_p USING gist (geom)#

ALTER TABLE edgv.emu_rampa_p
	 ADD CONSTRAINT emu_rampa_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_p
	 ADD CONSTRAINT emu_rampa_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_p
	 ADD CONSTRAINT emu_rampa_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_p
	 ADD CONSTRAINT emu_rampa_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_rampa_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT emu_rampa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_rampa_a_geom ON edgv.emu_rampa_a USING gist (geom)#

ALTER TABLE edgv.emu_rampa_a
	 ADD CONSTRAINT emu_rampa_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_a
	 ADD CONSTRAINT emu_rampa_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_a
	 ADD CONSTRAINT emu_rampa_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_rampa_a
	 ADD CONSTRAINT emu_rampa_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_rampa_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_ciclovia_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 revestimento smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT emu_ciclovia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_ciclovia_l_geom ON edgv.emu_ciclovia_l USING gist (geom)#

ALTER TABLE edgv.emu_ciclovia_l
	 ADD CONSTRAINT emu_ciclovia_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_ciclovia_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_ciclovia_l
	 ADD CONSTRAINT emu_ciclovia_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_ciclovia_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_ciclovia_l
	 ADD CONSTRAINT emu_ciclovia_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_ciclovia_l ALTER COLUMN revestimento SET DEFAULT 9999#

CREATE TABLE edgv.emu_elevador_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipoelevador smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT emu_elevador_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_elevador_l_geom ON edgv.emu_elevador_l USING gist (geom)#

ALTER TABLE edgv.emu_elevador_l
	 ADD CONSTRAINT emu_elevador_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_l
	 ADD CONSTRAINT emu_elevador_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_l
	 ADD CONSTRAINT emu_elevador_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_l
	 ADD CONSTRAINT emu_elevador_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_l
	 ADD CONSTRAINT emu_elevador_l_tipoelevador_fk FOREIGN KEY (tipoelevador)
	 REFERENCES dominios.tipo_elevador (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_l ALTER COLUMN tipoelevador SET DEFAULT 9999#

CREATE TABLE edgv.emu_elevador_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipoelevador smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT emu_elevador_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_elevador_p_geom ON edgv.emu_elevador_p USING gist (geom)#

ALTER TABLE edgv.emu_elevador_p
	 ADD CONSTRAINT emu_elevador_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_p
	 ADD CONSTRAINT emu_elevador_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_p
	 ADD CONSTRAINT emu_elevador_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_p
	 ADD CONSTRAINT emu_elevador_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_p
	 ADD CONSTRAINT emu_elevador_p_tipoelevador_fk FOREIGN KEY (tipoelevador)
	 REFERENCES dominios.tipo_elevador (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_p ALTER COLUMN tipoelevador SET DEFAULT 9999#

CREATE TABLE edgv.emu_elevador_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipoelevador smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT emu_elevador_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_elevador_a_geom ON edgv.emu_elevador_a USING gist (geom)#

ALTER TABLE edgv.emu_elevador_a
	 ADD CONSTRAINT emu_elevador_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_a
	 ADD CONSTRAINT emu_elevador_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_a
	 ADD CONSTRAINT emu_elevador_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_a
	 ADD CONSTRAINT emu_elevador_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.emu_elevador_a
	 ADD CONSTRAINT emu_elevador_a_tipoelevador_fk FOREIGN KEY (tipoelevador)
	 REFERENCES dominios.tipo_elevador (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_elevador_a ALTER COLUMN tipoelevador SET DEFAULT 9999#

CREATE TABLE edgv.emu_escadaria_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT emu_escadaria_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_escadaria_l_geom ON edgv.emu_escadaria_l USING gist (geom)#

ALTER TABLE edgv.emu_escadaria_l
	 ADD CONSTRAINT emu_escadaria_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_l
	 ADD CONSTRAINT emu_escadaria_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_l
	 ADD CONSTRAINT emu_escadaria_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_l
	 ADD CONSTRAINT emu_escadaria_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_escadaria_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT emu_escadaria_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_escadaria_p_geom ON edgv.emu_escadaria_p USING gist (geom)#

ALTER TABLE edgv.emu_escadaria_p
	 ADD CONSTRAINT emu_escadaria_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_p
	 ADD CONSTRAINT emu_escadaria_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_p
	 ADD CONSTRAINT emu_escadaria_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_p
	 ADD CONSTRAINT emu_escadaria_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_escadaria_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT emu_escadaria_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_escadaria_a_geom ON edgv.emu_escadaria_a USING gist (geom)#

ALTER TABLE edgv.emu_escadaria_a
	 ADD CONSTRAINT emu_escadaria_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_a
	 ADD CONSTRAINT emu_escadaria_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_a
	 ADD CONSTRAINT emu_escadaria_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_escadaria_a
	 ADD CONSTRAINT emu_escadaria_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_escadaria_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

CREATE TABLE edgv.emu_poste_sinalizacao_p(
	 id serial NOT NULL,
	 codident varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint,
	 tipoposte smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT emu_poste_sinalizacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX emu_poste_sinalizacao_p_geom ON edgv.emu_poste_sinalizacao_p USING gist (geom)#

ALTER TABLE edgv.emu_poste_sinalizacao_p
	 ADD CONSTRAINT emu_poste_sinalizacao_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_poste_sinalizacao_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.emu_poste_sinalizacao_p
	 ADD CONSTRAINT emu_poste_sinalizacao_p_tipoposte_fk FOREIGN KEY (tipoposte)
	 REFERENCES dominios.tipo_poste (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.emu_poste_sinalizacao_p
	 ADD CONSTRAINT emu_poste_sinalizacao_p_tipoposte_check 
	 CHECK (tipoposte = ANY(ARRAY[5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.emu_poste_sinalizacao_p ALTER COLUMN tipoposte SET DEFAULT 9999#

CREATE TABLE edgv.enc_casa_de_forca_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_casa_de_forca_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_casa_de_forca_p_geom ON edgv.enc_casa_de_forca_p USING gist (geom)#

CREATE TABLE edgv.enc_torre_energia_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 ovgd smallint NOT NULL,
	 alturaestimada real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_torre_energia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_torre_energia_p_geom ON edgv.enc_torre_energia_p USING gist (geom)#

ALTER TABLE edgv.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_energia_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_energia_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_energia_p
	 ADD CONSTRAINT enc_torre_energia_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_energia_p ALTER COLUMN ovgd SET DEFAULT 9999#

CREATE TABLE edgv.enc_trecho_energia_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 especie smallint,
	 posicaorelativa smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 largurafaixaservidao real,
	 sin smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_trecho_energia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_trecho_energia_l_geom ON edgv.enc_trecho_energia_l USING gist (geom)#

ALTER TABLE edgv.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_especie_fk FOREIGN KEY (especie)
	 REFERENCES dominios.especie_trecho_energia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_energia_l ALTER COLUMN especie SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_energia_l ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_energia_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_energia_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_energia_l
	 ADD CONSTRAINT enc_trecho_energia_l_sin_fk FOREIGN KEY (sin)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_energia_l ALTER COLUMN sin SET DEFAULT 9999#

CREATE TABLE edgv.enc_grupo_transformadores_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_grupo_transformadores_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_grupo_transformadores_p_geom ON edgv.enc_grupo_transformadores_p USING gist (geom)#

CREATE TABLE edgv.enc_grupo_transformadores_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_grupo_transformadores_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_grupo_transformadores_a_geom ON edgv.enc_grupo_transformadores_a USING gist (geom)#

CREATE TABLE edgv.enc_est_gerad_energia_eletrica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_est_gerad_energia_eletrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_est_gerad_energia_eletrica_p_geom ON edgv.enc_est_gerad_energia_eletrica_p USING gist (geom)#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_p_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_p_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[0 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.enc_est_gerad_energia_eletrica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_est_gerad_energia_eletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_est_gerad_energia_eletrica_a_geom ON edgv.enc_est_gerad_energia_eletrica_a USING gist (geom)#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_a_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_a_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[0 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a
	 ADD CONSTRAINT enc_est_gerad_energia_eletrica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_est_gerad_energia_eletrica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.enc_central_geradora_eolica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_central_geradora_eolica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_central_geradora_eolica_p_geom ON edgv.enc_central_geradora_eolica_p USING gist (geom)#

ALTER TABLE edgv.enc_central_geradora_eolica_p
	 ADD CONSTRAINT enc_central_geradora_eolica_p_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_p
	 ADD CONSTRAINT enc_central_geradora_eolica_p_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_central_geradora_eolica_p ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_central_geradora_eolica_p
	 ADD CONSTRAINT enc_central_geradora_eolica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_central_geradora_eolica_p
	 ADD CONSTRAINT enc_central_geradora_eolica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.enc_central_geradora_eolica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_central_geradora_eolica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_central_geradora_eolica_a_geom ON edgv.enc_central_geradora_eolica_a USING gist (geom)#

ALTER TABLE edgv.enc_central_geradora_eolica_a
	 ADD CONSTRAINT enc_central_geradora_eolica_a_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_a
	 ADD CONSTRAINT enc_central_geradora_eolica_a_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_central_geradora_eolica_a ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_central_geradora_eolica_a
	 ADD CONSTRAINT enc_central_geradora_eolica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_central_geradora_eolica_a
	 ADD CONSTRAINT enc_central_geradora_eolica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_central_geradora_eolica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.enc_aerogerador_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 alturatorreaer real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_aerogerador_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_aerogerador_p_geom ON edgv.enc_aerogerador_p USING gist (geom)#

CREATE TABLE edgv.enc_hidreletrica_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 tipoahe smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_hidreletrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_l_geom ON edgv.enc_hidreletrica_l USING gist (geom)#

ALTER TABLE edgv.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[8 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_hidreletrica_l ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_l
	 ADD CONSTRAINT enc_hidreletrica_l_tipoahe_fk FOREIGN KEY (tipoahe)
	 REFERENCES dominios.tipo_ahe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_l ALTER COLUMN tipoahe SET DEFAULT 9999#

CREATE TABLE edgv.enc_hidreletrica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 tipoahe smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_hidreletrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_p_geom ON edgv.enc_hidreletrica_p USING gist (geom)#

ALTER TABLE edgv.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[8 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_hidreletrica_p ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_p
	 ADD CONSTRAINT enc_hidreletrica_p_tipoahe_fk FOREIGN KEY (tipoahe)
	 REFERENCES dominios.tipo_ahe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_p ALTER COLUMN tipoahe SET DEFAULT 9999#

CREATE TABLE edgv.enc_hidreletrica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 tipoahe smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_hidreletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_hidreletrica_a_geom ON edgv.enc_hidreletrica_a USING gist (geom)#

ALTER TABLE edgv.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[8 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_hidreletrica_a ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_hidreletrica_a
	 ADD CONSTRAINT enc_hidreletrica_a_tipoahe_fk FOREIGN KEY (tipoahe)
	 REFERENCES dominios.tipo_ahe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_hidreletrica_a ALTER COLUMN tipoahe SET DEFAULT 9999#

CREATE TABLE edgv.enc_antena_comunic_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 posicaoreledific smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_antena_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_antena_comunic_p_geom ON edgv.enc_antena_comunic_p USING gist (geom)#

ALTER TABLE edgv.enc_antena_comunic_p
	 ADD CONSTRAINT enc_antena_comunic_p_posicaoreledific_fk FOREIGN KEY (posicaoreledific)
	 REFERENCES dominios.posicao_rel_edific (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_antena_comunic_p ALTER COLUMN posicaoreledific SET DEFAULT 9999#

CREATE TABLE edgv.enc_termeletrica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 tipocombustivel smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_termeletrica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_termeletrica_p_geom ON edgv.enc_termeletrica_p USING gist (geom)#

ALTER TABLE edgv.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_termeletrica_p ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_p
	 ADD CONSTRAINT enc_termeletrica_p_tipocombustivel_fk FOREIGN KEY (tipocombustivel)
	 REFERENCES dominios.tipo_combustivel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_p ALTER COLUMN tipocombustivel SET DEFAULT 9999#

CREATE TABLE edgv.enc_termeletrica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 ceg varchar(16),
	 tipoestgerad smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 potenciaout real,
	 tipocombustivel smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_termeletrica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_termeletrica_a_geom ON edgv.enc_termeletrica_a USING gist (geom)#

ALTER TABLE edgv.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_tipoestgerad_fk FOREIGN KEY (tipoestgerad)
	 REFERENCES dominios.tipo_est_gerad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_tipoestgerad_check 
	 CHECK (tipoestgerad = ANY(ARRAY[9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.enc_termeletrica_a ALTER COLUMN tipoestgerad SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_termeletrica_a
	 ADD CONSTRAINT enc_termeletrica_a_tipocombustivel_fk FOREIGN KEY (tipocombustivel)
	 REFERENCES dominios.tipo_combustivel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_termeletrica_a ALTER COLUMN tipocombustivel SET DEFAULT 9999#

CREATE TABLE edgv.enc_trecho_comunic_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotrechocomunic smallint NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 matcondutor smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 emduto boolean,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT enc_trecho_comunic_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_trecho_comunic_l_geom ON edgv.enc_trecho_comunic_l USING gist (geom)#

ALTER TABLE edgv.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_tipotrechocomunic_fk FOREIGN KEY (tipotrechocomunic)
	 REFERENCES dominios.tipo_trecho_comunic (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_comunic_l ALTER COLUMN tipotrechocomunic SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_comunic_l ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_matcondutor_fk FOREIGN KEY (matcondutor)
	 REFERENCES dominios.mat_condutor (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_comunic_l ALTER COLUMN matcondutor SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_comunic_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_trecho_comunic_l
	 ADD CONSTRAINT enc_trecho_comunic_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_trecho_comunic_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.enc_torre_comunic_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 posicaoreledific smallint NOT NULL,
	 ovgd smallint NOT NULL,
	 alturaestimada real,
	 modalidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT enc_torre_comunic_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_torre_comunic_p_geom ON edgv.enc_torre_comunic_p USING gist (geom)#

ALTER TABLE edgv.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_comunic_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_comunic_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_posicaoreledific_fk FOREIGN KEY (posicaoreledific)
	 REFERENCES dominios.posicao_rel_edific (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_comunic_p ALTER COLUMN posicaoreledific SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_ovgd_fk FOREIGN KEY (ovgd)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_comunic_p ALTER COLUMN ovgd SET DEFAULT 9999#

ALTER TABLE edgv.enc_torre_comunic_p
	 ADD CONSTRAINT enc_torre_comunic_p_modalidade_fk FOREIGN KEY (modalidade)
	 REFERENCES dominios.modalidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.enc_torre_comunic_p ALTER COLUMN modalidade SET DEFAULT 9999#

CREATE TABLE edgv.enc_zona_linhas_energia_comunicacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT enc_zona_linhas_energia_comunicacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX enc_zona_linhas_energia_comunicacao_a_geom ON edgv.enc_zona_linhas_energia_comunicacao_a USING gist (geom)#

CREATE TABLE edgv.fer_girador_ferroviario_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 administracao smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT fer_girador_ferroviario_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX fer_girador_ferroviario_p_geom ON edgv.fer_girador_ferroviario_p USING gist (geom)#

ALTER TABLE edgv.fer_girador_ferroviario_p
	 ADD CONSTRAINT fer_girador_ferroviario_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_girador_ferroviario_p ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.fer_girador_ferroviario_p
	 ADD CONSTRAINT fer_girador_ferroviario_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_girador_ferroviario_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.fer_girador_ferroviario_p
	 ADD CONSTRAINT fer_girador_ferroviario_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_girador_ferroviario_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.fer_trecho_ferroviario_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codtrechoferrov varchar(25) NOT NULL,
	 posicaorelativa smallint NOT NULL,
	 tipotrechoferrov smallint NOT NULL,
	 bitola smallint NOT NULL,
	 eletrificada smallint NOT NULL,
	 nrlinhas smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(25),
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 cargasuportmaxima real,
	 emarruamento boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT fer_trecho_ferroviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX fer_trecho_ferroviario_l_geom ON edgv.fer_trecho_ferroviario_l USING gist (geom)#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_posicaorelativa_fk FOREIGN KEY (posicaorelativa)
	 REFERENCES dominios.posicao_relativa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN posicaorelativa SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_tipotrechoferrov_fk FOREIGN KEY (tipotrechoferrov)
	 REFERENCES dominios.tipo_trecho_ferrov (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN tipotrechoferrov SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_bitola_fk FOREIGN KEY (bitola)
	 REFERENCES dominios.bitola (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN bitola SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_eletrificada_fk FOREIGN KEY (eletrificada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN eletrificada SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_nrlinhas_fk FOREIGN KEY (nrlinhas)
	 REFERENCES dominios.nr_linhas (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN nrlinhas SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.fer_trecho_ferroviario_l
	 ADD CONSTRAINT fer_trecho_ferroviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_trecho_ferroviario_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.fer_cremalheira_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT fer_cremalheira_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX fer_cremalheira_l_geom ON edgv.fer_cremalheira_l USING gist (geom)#

ALTER TABLE edgv.fer_cremalheira_l
	 ADD CONSTRAINT fer_cremalheira_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_cremalheira_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.fer_cremalheira_l
	 ADD CONSTRAINT fer_cremalheira_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_cremalheira_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.fer_cremalheira_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT fer_cremalheira_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX fer_cremalheira_p_geom ON edgv.fer_cremalheira_p USING gist (geom)#

ALTER TABLE edgv.fer_cremalheira_p
	 ADD CONSTRAINT fer_cremalheira_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_cremalheira_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.fer_cremalheira_p
	 ADD CONSTRAINT fer_cremalheira_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.fer_cremalheira_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hdv_eclusa_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 desnivel real,
	 largura real,
	 extensao real,
	 calado real,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hdv_eclusa_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_eclusa_l_geom ON edgv.hdv_eclusa_l USING gist (geom)#

ALTER TABLE edgv.hdv_eclusa_l
	 ADD CONSTRAINT hdv_eclusa_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_l
	 ADD CONSTRAINT hdv_eclusa_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_l
	 ADD CONSTRAINT hdv_eclusa_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hdv_eclusa_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 desnivel real,
	 largura real,
	 extensao real,
	 calado real,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hdv_eclusa_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_eclusa_p_geom ON edgv.hdv_eclusa_p USING gist (geom)#

ALTER TABLE edgv.hdv_eclusa_p
	 ADD CONSTRAINT hdv_eclusa_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_p
	 ADD CONSTRAINT hdv_eclusa_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_p
	 ADD CONSTRAINT hdv_eclusa_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hdv_eclusa_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 desnivel real,
	 largura real,
	 extensao real,
	 calado real,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hdv_eclusa_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_eclusa_a_geom ON edgv.hdv_eclusa_a USING gist (geom)#

ALTER TABLE edgv.hdv_eclusa_a
	 ADD CONSTRAINT hdv_eclusa_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_a
	 ADD CONSTRAINT hdv_eclusa_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_eclusa_a
	 ADD CONSTRAINT hdv_eclusa_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_eclusa_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hdv_obstaculo_navegacao_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoobst smallint NOT NULL,
	 situacaoemagua smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hdv_obstaculo_navegacao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_obstaculo_navegacao_l_geom ON edgv.hdv_obstaculo_navegacao_l USING gist (geom)#

ALTER TABLE edgv.hdv_obstaculo_navegacao_l
	 ADD CONSTRAINT hdv_obstaculo_navegacao_l_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipo_obst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_l ALTER COLUMN tipoobst SET DEFAULT 9999#

ALTER TABLE edgv.hdv_obstaculo_navegacao_l
	 ADD CONSTRAINT hdv_obstaculo_navegacao_l_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_l ALTER COLUMN situacaoemagua SET DEFAULT 9999#

CREATE TABLE edgv.hdv_obstaculo_navegacao_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoobst smallint NOT NULL,
	 situacaoemagua smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hdv_obstaculo_navegacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_obstaculo_navegacao_p_geom ON edgv.hdv_obstaculo_navegacao_p USING gist (geom)#

ALTER TABLE edgv.hdv_obstaculo_navegacao_p
	 ADD CONSTRAINT hdv_obstaculo_navegacao_p_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipo_obst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_p ALTER COLUMN tipoobst SET DEFAULT 9999#

ALTER TABLE edgv.hdv_obstaculo_navegacao_p
	 ADD CONSTRAINT hdv_obstaculo_navegacao_p_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_p ALTER COLUMN situacaoemagua SET DEFAULT 9999#

CREATE TABLE edgv.hdv_obstaculo_navegacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoobst smallint NOT NULL,
	 situacaoemagua smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hdv_obstaculo_navegacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_obstaculo_navegacao_a_geom ON edgv.hdv_obstaculo_navegacao_a USING gist (geom)#

ALTER TABLE edgv.hdv_obstaculo_navegacao_a
	 ADD CONSTRAINT hdv_obstaculo_navegacao_a_tipoobst_fk FOREIGN KEY (tipoobst)
	 REFERENCES dominios.tipo_obst (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_a ALTER COLUMN tipoobst SET DEFAULT 9999#

ALTER TABLE edgv.hdv_obstaculo_navegacao_a
	 ADD CONSTRAINT hdv_obstaculo_navegacao_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_obstaculo_navegacao_a ALTER COLUMN situacaoemagua SET DEFAULT 9999#

CREATE TABLE edgv.hdv_sinalizacao_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tiposinal smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hdv_sinalizacao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_sinalizacao_p_geom ON edgv.hdv_sinalizacao_p USING gist (geom)#

ALTER TABLE edgv.hdv_sinalizacao_p
	 ADD CONSTRAINT hdv_sinalizacao_p_tiposinal_fk FOREIGN KEY (tiposinal)
	 REFERENCES dominios.tipo_sinal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_sinalizacao_p ALTER COLUMN tiposinal SET DEFAULT 9999#

ALTER TABLE edgv.hdv_sinalizacao_p
	 ADD CONSTRAINT hdv_sinalizacao_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_sinalizacao_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_sinalizacao_p
	 ADD CONSTRAINT hdv_sinalizacao_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_sinalizacao_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hdv_atracadouro_terminal_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoatracad smallint NOT NULL,
	 administracao smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 aptidaooperacional smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hdv_atracadouro_terminal_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_atracadouro_terminal_l_geom ON edgv.hdv_atracadouro_terminal_l USING gist (geom)#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipo_atracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN tipoatracad SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_l
	 ADD CONSTRAINT hdv_atracadouro_terminal_l_aptidaooperacional_fk FOREIGN KEY (aptidaooperacional)
	 REFERENCES dominios.aptidao_operacional_atracadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_l ALTER COLUMN aptidaooperacional SET DEFAULT 9999#

CREATE TABLE edgv.hdv_atracadouro_terminal_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoatracad smallint NOT NULL,
	 administracao smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 aptidaooperacional smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hdv_atracadouro_terminal_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_atracadouro_terminal_p_geom ON edgv.hdv_atracadouro_terminal_p USING gist (geom)#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipo_atracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN tipoatracad SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_p
	 ADD CONSTRAINT hdv_atracadouro_terminal_p_aptidaooperacional_fk FOREIGN KEY (aptidaooperacional)
	 REFERENCES dominios.aptidao_operacional_atracadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_p ALTER COLUMN aptidaooperacional SET DEFAULT 9999#

CREATE TABLE edgv.hdv_atracadouro_terminal_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoatracad smallint NOT NULL,
	 administracao smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 aptidaooperacional smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hdv_atracadouro_terminal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_atracadouro_terminal_a_geom ON edgv.hdv_atracadouro_terminal_a USING gist (geom)#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_tipoatracad_fk FOREIGN KEY (tipoatracad)
	 REFERENCES dominios.tipo_atracad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN tipoatracad SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hdv_atracadouro_terminal_a
	 ADD CONSTRAINT hdv_atracadouro_terminal_a_aptidaooperacional_fk FOREIGN KEY (aptidaooperacional)
	 REFERENCES dominios.aptidao_operacional_atracadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_atracadouro_terminal_a ALTER COLUMN aptidaooperacional SET DEFAULT 9999#

CREATE TABLE edgv.hdv_fundeadouro_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipofundeadouro smallint NOT NULL,
	 administracao smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hdv_fundeadouro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_fundeadouro_p_geom ON edgv.hdv_fundeadouro_p USING gist (geom)#

ALTER TABLE edgv.hdv_fundeadouro_p
	 ADD CONSTRAINT hdv_fundeadouro_p_tipofundeadouro_fk FOREIGN KEY (tipofundeadouro)
	 REFERENCES dominios.tipo_fundeadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_fundeadouro_p ALTER COLUMN tipofundeadouro SET DEFAULT 9999#

ALTER TABLE edgv.hdv_fundeadouro_p
	 ADD CONSTRAINT hdv_fundeadouro_p_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_fundeadouro_p
	 ADD CONSTRAINT hdv_fundeadouro_p_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hdv_fundeadouro_p ALTER COLUMN administracao SET DEFAULT 9999#

CREATE TABLE edgv.hdv_fundeadouro_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipofundeadouro smallint NOT NULL,
	 administracao smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hdv_fundeadouro_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_fundeadouro_a_geom ON edgv.hdv_fundeadouro_a USING gist (geom)#

ALTER TABLE edgv.hdv_fundeadouro_a
	 ADD CONSTRAINT hdv_fundeadouro_a_tipofundeadouro_fk FOREIGN KEY (tipofundeadouro)
	 REFERENCES dominios.tipo_fundeadouro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_fundeadouro_a ALTER COLUMN tipofundeadouro SET DEFAULT 9999#

ALTER TABLE edgv.hdv_fundeadouro_a
	 ADD CONSTRAINT hdv_fundeadouro_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_fundeadouro_a
	 ADD CONSTRAINT hdv_fundeadouro_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hdv_fundeadouro_a ALTER COLUMN administracao SET DEFAULT 9999#

CREATE TABLE edgv.hdv_trecho_hidroviario_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 regime smallint,
	 extensaotrecho real,
	 caladomaxseca real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hdv_trecho_hidroviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hdv_trecho_hidroviario_l_geom ON edgv.hdv_trecho_hidroviario_l USING gist (geom)#

ALTER TABLE edgv.hdv_trecho_hidroviario_l
	 ADD CONSTRAINT hdv_trecho_hidroviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_trecho_hidroviario_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hdv_trecho_hidroviario_l
	 ADD CONSTRAINT hdv_trecho_hidroviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_trecho_hidroviario_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hdv_trecho_hidroviario_l
	 ADD CONSTRAINT hdv_trecho_hidroviario_l_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hdv_trecho_hidroviario_l ALTER COLUMN regime SET DEFAULT 9999#

CREATE TABLE edgv.hid_sumidouro_vertedouro_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tiposumvert smallint NOT NULL,
	 causa smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_sumidouro_vertedouro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_sumidouro_vertedouro_p_geom ON edgv.hid_sumidouro_vertedouro_p USING gist (geom)#

ALTER TABLE edgv.hid_sumidouro_vertedouro_p
	 ADD CONSTRAINT hid_sumidouro_vertedouro_p_tiposumvert_fk FOREIGN KEY (tiposumvert)
	 REFERENCES dominios.tipo_sum_vert (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_sumidouro_vertedouro_p ALTER COLUMN tiposumvert SET DEFAULT 9999#

ALTER TABLE edgv.hid_sumidouro_vertedouro_p
	 ADD CONSTRAINT hid_sumidouro_vertedouro_p_causa_fk FOREIGN KEY (causa)
	 REFERENCES dominios.causa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_sumidouro_vertedouro_p ALTER COLUMN causa SET DEFAULT 9999#

CREATE TABLE edgv.hid_ilha_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 tipoilha smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_ilha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ilha_p_geom ON edgv.hid_ilha_p USING gist (geom)#

ALTER TABLE edgv.hid_ilha_p
	 ADD CONSTRAINT hid_ilha_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_ilha_p
	 ADD CONSTRAINT hid_ilha_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[21 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_ilha_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.hid_ilha_p
	 ADD CONSTRAINT hid_ilha_p_tipoilha_fk FOREIGN KEY (tipoilha)
	 REFERENCES dominios.tipo_ilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_ilha_p ALTER COLUMN tipoilha SET DEFAULT 9999#

CREATE TABLE edgv.hid_ilha_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 tipoilha smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_ilha_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_ilha_a_geom ON edgv.hid_ilha_a USING gist (geom)#

ALTER TABLE edgv.hid_ilha_a
	 ADD CONSTRAINT hid_ilha_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_ilha_a
	 ADD CONSTRAINT hid_ilha_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[21 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_ilha_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.hid_ilha_a
	 ADD CONSTRAINT hid_ilha_a_tipoilha_fk FOREIGN KEY (tipoilha)
	 REFERENCES dominios.tipo_ilha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_ilha_a ALTER COLUMN tipoilha SET DEFAULT 9999#

CREATE TABLE edgv.hid_vala_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 finalidade smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_vala_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_vala_l_geom ON edgv.hid_vala_l USING gist (geom)#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[31 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_vala_l ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_l
	 ADD CONSTRAINT hid_vala_l_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_vala_l ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.hid_vala_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 finalidade smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_vala_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_vala_a_geom ON edgv.hid_vala_a USING gist (geom)#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[31 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_vala_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_vala_a
	 ADD CONSTRAINT hid_vala_a_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_vala_a ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.hid_dique_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_dique_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_dique_l_geom ON edgv.hid_dique_l USING gist (geom)#

ALTER TABLE edgv.hid_dique_l
	 ADD CONSTRAINT hid_dique_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_dique_l ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.hid_dique_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_dique_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_dique_p_geom ON edgv.hid_dique_p USING gist (geom)#

ALTER TABLE edgv.hid_dique_p
	 ADD CONSTRAINT hid_dique_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_dique_p ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.hid_dique_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_dique_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_dique_a_geom ON edgv.hid_dique_a USING gist (geom)#

ALTER TABLE edgv.hid_dique_a
	 ADD CONSTRAINT hid_dique_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_dique_a ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.hid_canal_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 finalidade smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_canal_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_canal_l_geom ON edgv.hid_canal_l USING gist (geom)#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[30 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_canal_l ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_l
	 ADD CONSTRAINT hid_canal_l_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_canal_l ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.hid_canal_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 finalidade smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_canal_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_canal_a_geom ON edgv.hid_canal_a USING gist (geom)#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[30 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_canal_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_galeria_bueiro (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_canal_a
	 ADD CONSTRAINT hid_canal_a_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_canal_a ALTER COLUMN finalidade SET DEFAULT 9999#

CREATE TABLE edgv.hid_massa_dagua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipomassadagua smallint NOT NULL,
	 regime smallint NOT NULL,
	 salgada smallint NOT NULL,
	 dominialidade smallint,
	 artificial smallint NOT NULL,
	 possuitrechodrenagem boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_massa_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_massa_dagua_a_geom ON edgv.hid_massa_dagua_a USING gist (geom)#

ALTER TABLE edgv.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_tipomassadagua_fk FOREIGN KEY (tipomassadagua)
	 REFERENCES dominios.tipo_massa_dagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_massa_dagua_a ALTER COLUMN tipomassadagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_massa_dagua_a ALTER COLUMN regime SET DEFAULT 9999#

ALTER TABLE edgv.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_salgada_fk FOREIGN KEY (salgada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_massa_dagua_a ALTER COLUMN salgada SET DEFAULT 9999#

ALTER TABLE edgv.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_dominialidade_fk FOREIGN KEY (dominialidade)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_massa_dagua_a ALTER COLUMN dominialidade SET DEFAULT 9999#

ALTER TABLE edgv.hid_massa_dagua_a
	 ADD CONSTRAINT hid_massa_dagua_a_artificial_fk FOREIGN KEY (artificial)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_massa_dagua_a ALTER COLUMN artificial SET DEFAULT 9999#

CREATE TABLE edgv.hid_trecho_drenagem_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotrechodrenagem smallint NOT NULL,
	 navegavel smallint NOT NULL,
	 larguramedia real,
	 regime smallint NOT NULL,
	 encoberto boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_trecho_drenagem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_trecho_drenagem_l_geom ON edgv.hid_trecho_drenagem_l USING gist (geom)#

ALTER TABLE edgv.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_tipotrechodrenagem_fk FOREIGN KEY (tipotrechodrenagem)
	 REFERENCES dominios.tipo_trecho_drenagem (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_trecho_drenagem_l ALTER COLUMN tipotrechodrenagem SET DEFAULT 9999#

ALTER TABLE edgv.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_navegavel_fk FOREIGN KEY (navegavel)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_trecho_drenagem_l ALTER COLUMN navegavel SET DEFAULT 9999#

ALTER TABLE edgv.hid_trecho_drenagem_l
	 ADD CONSTRAINT hid_trecho_drenagem_l_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_trecho_drenagem_l ALTER COLUMN regime SET DEFAULT 9999#

CREATE TABLE edgv.hid_comporta_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_comporta_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_comporta_l_geom ON edgv.hid_comporta_l USING gist (geom)#

ALTER TABLE edgv.hid_comporta_l
	 ADD CONSTRAINT hid_comporta_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_comporta_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_comporta_l
	 ADD CONSTRAINT hid_comporta_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_comporta_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_comporta_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_comporta_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_comporta_p_geom ON edgv.hid_comporta_p USING gist (geom)#

ALTER TABLE edgv.hid_comporta_p
	 ADD CONSTRAINT hid_comporta_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_comporta_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_comporta_p
	 ADD CONSTRAINT hid_comporta_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_comporta_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_corredeira_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_corredeira_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_l_geom ON edgv.hid_corredeira_l USING gist (geom)#

CREATE TABLE edgv.hid_corredeira_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_corredeira_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_p_geom ON edgv.hid_corredeira_p USING gist (geom)#

CREATE TABLE edgv.hid_corredeira_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_corredeira_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_corredeira_a_geom ON edgv.hid_corredeira_a USING gist (geom)#

CREATE TABLE edgv.hid_queda_dagua_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoqueda smallint NOT NULL,
	 altura real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_queda_dagua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_queda_dagua_p_geom ON edgv.hid_queda_dagua_p USING gist (geom)#

ALTER TABLE edgv.hid_queda_dagua_p
	 ADD CONSTRAINT hid_queda_dagua_p_tipoqueda_fk FOREIGN KEY (tipoqueda)
	 REFERENCES dominios.tipo_queda (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_queda_dagua_p ALTER COLUMN tipoqueda SET DEFAULT 9999#

CREATE TABLE edgv.hid_queda_dagua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoqueda smallint NOT NULL,
	 altura real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_queda_dagua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_queda_dagua_a_geom ON edgv.hid_queda_dagua_a USING gist (geom)#

ALTER TABLE edgv.hid_queda_dagua_a
	 ADD CONSTRAINT hid_queda_dagua_a_tipoqueda_fk FOREIGN KEY (tipoqueda)
	 REFERENCES dominios.tipo_queda (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_queda_dagua_a ALTER COLUMN tipoqueda SET DEFAULT 9999#

CREATE TABLE edgv.hid_recife_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tiporecife smallint NOT NULL,
	 situacaoemagua smallint NOT NULL,
	 situacaocosta smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_recife_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_recife_p_geom ON edgv.hid_recife_p USING gist (geom)#

ALTER TABLE edgv.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_tiporecife_fk FOREIGN KEY (tiporecife)
	 REFERENCES dominios.tipo_recife (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_p ALTER COLUMN tiporecife SET DEFAULT 9999#

ALTER TABLE edgv.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_p ALTER COLUMN situacaoemagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_recife_p
	 ADD CONSTRAINT hid_recife_p_situacaocosta_fk FOREIGN KEY (situacaocosta)
	 REFERENCES dominios.situacao_costa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_p ALTER COLUMN situacaocosta SET DEFAULT 9999#

CREATE TABLE edgv.hid_recife_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tiporecife smallint NOT NULL,
	 situacaoemagua smallint NOT NULL,
	 situacaocosta smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_recife_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_recife_a_geom ON edgv.hid_recife_a USING gist (geom)#

ALTER TABLE edgv.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_tiporecife_fk FOREIGN KEY (tiporecife)
	 REFERENCES dominios.tipo_recife (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_a ALTER COLUMN tiporecife SET DEFAULT 9999#

ALTER TABLE edgv.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_a ALTER COLUMN situacaoemagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_recife_a
	 ADD CONSTRAINT hid_recife_a_situacaocosta_fk FOREIGN KEY (situacaocosta)
	 REFERENCES dominios.situacao_costa (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_recife_a ALTER COLUMN situacaocosta SET DEFAULT 9999#

CREATE TABLE edgv.hid_terreno_sujeito_inundacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 periodicidadeinunda varchar(20),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_terreno_sujeito_inundacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_terreno_sujeito_inundacao_a_geom ON edgv.hid_terreno_sujeito_inundacao_a USING gist (geom)#

CREATE TABLE edgv.hid_rocha_em_agua_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 formarocha smallint,
	 situacaoemagua smallint NOT NULL,
	 alturalamina real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_rocha_em_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_rocha_em_agua_p_geom ON edgv.hid_rocha_em_agua_p USING gist (geom)#

ALTER TABLE edgv.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[23 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_rocha_em_agua_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_formarocha_fk FOREIGN KEY (formarocha)
	 REFERENCES dominios.forma_rocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_p ALTER COLUMN formarocha SET DEFAULT 9999#

ALTER TABLE edgv.hid_rocha_em_agua_p
	 ADD CONSTRAINT hid_rocha_em_agua_p_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_p ALTER COLUMN situacaoemagua SET DEFAULT 9999#

CREATE TABLE edgv.hid_rocha_em_agua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 formarocha smallint,
	 situacaoemagua smallint NOT NULL,
	 alturalamina real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_rocha_em_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_rocha_em_agua_a_geom ON edgv.hid_rocha_em_agua_a USING gist (geom)#

ALTER TABLE edgv.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[23 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.hid_rocha_em_agua_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_formarocha_fk FOREIGN KEY (formarocha)
	 REFERENCES dominios.forma_rocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_a ALTER COLUMN formarocha SET DEFAULT 9999#

ALTER TABLE edgv.hid_rocha_em_agua_a
	 ADD CONSTRAINT hid_rocha_em_agua_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_rocha_em_agua_a ALTER COLUMN situacaoemagua SET DEFAULT 9999#

CREATE TABLE edgv.hid_banco_areia_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipobanco smallint NOT NULL,
	 situacaoemagua smallint,
	 materialpredominante smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_banco_areia_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_banco_areia_a_geom ON edgv.hid_banco_areia_a USING gist (geom)#

ALTER TABLE edgv.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_tipobanco_fk FOREIGN KEY (tipobanco)
	 REFERENCES dominios.tipo_banco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_banco_areia_a ALTER COLUMN tipobanco SET DEFAULT 9999#

ALTER TABLE edgv.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_banco_areia_a ALTER COLUMN situacaoemagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_banco_areia_a
	 ADD CONSTRAINT hid_banco_areia_a_materialpredominante_fk FOREIGN KEY (materialpredominante)
	 REFERENCES dominios.material_predominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_banco_areia_a ALTER COLUMN materialpredominante SET DEFAULT 9999#

CREATE TABLE edgv.hid_quebramar_molhe_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoquebramolhe smallint NOT NULL,
	 situacaoemagua smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_quebramar_molhe_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_quebramar_molhe_l_geom ON edgv.hid_quebramar_molhe_l USING gist (geom)#

ALTER TABLE edgv.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_tipoquebramolhe_fk FOREIGN KEY (tipoquebramolhe)
	 REFERENCES dominios.tipo_quebra_molhe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_l ALTER COLUMN tipoquebramolhe SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_l ALTER COLUMN situacaoemagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_l
	 ADD CONSTRAINT hid_quebramar_molhe_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_quebramar_molhe_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoquebramolhe smallint NOT NULL,
	 situacaoemagua smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_quebramar_molhe_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_quebramar_molhe_a_geom ON edgv.hid_quebramar_molhe_a USING gist (geom)#

ALTER TABLE edgv.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_tipoquebramolhe_fk FOREIGN KEY (tipoquebramolhe)
	 REFERENCES dominios.tipo_quebra_molhe (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_a ALTER COLUMN tipoquebramolhe SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_situacaoemagua_fk FOREIGN KEY (situacaoemagua)
	 REFERENCES dominios.situacao_em_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_a ALTER COLUMN situacaoemagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_quebramar_molhe_a
	 ADD CONSTRAINT hid_quebramar_molhe_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_quebramar_molhe_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_foz_maritima_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_foz_maritima_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_foz_maritima_l_geom ON edgv.hid_foz_maritima_l USING gist (geom)#

CREATE TABLE edgv.hid_foz_maritima_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_foz_maritima_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_foz_maritima_p_geom ON edgv.hid_foz_maritima_p USING gist (geom)#

CREATE TABLE edgv.hid_fonte_dagua_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipofontedagua smallint NOT NULL,
	 qualidagua smallint,
	 regime smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_fonte_dagua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_fonte_dagua_p_geom ON edgv.hid_fonte_dagua_p USING gist (geom)#

ALTER TABLE edgv.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_tipofontedagua_fk FOREIGN KEY (tipofontedagua)
	 REFERENCES dominios.tipo_fonte_dagua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_fonte_dagua_p ALTER COLUMN tipofontedagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_qualidagua_fk FOREIGN KEY (qualidagua)
	 REFERENCES dominios.qualid_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_fonte_dagua_p ALTER COLUMN qualidagua SET DEFAULT 9999#

ALTER TABLE edgv.hid_fonte_dagua_p
	 ADD CONSTRAINT hid_fonte_dagua_p_regime_fk FOREIGN KEY (regime)
	 REFERENCES dominios.regime (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_fonte_dagua_p ALTER COLUMN regime SET DEFAULT 9999#

CREATE TABLE edgv.hid_area_umida_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoareaumida smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_area_umida_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_area_umida_a_geom ON edgv.hid_area_umida_a USING gist (geom)#

ALTER TABLE edgv.hid_area_umida_a
	 ADD CONSTRAINT hid_area_umida_a_tipoareaumida_fk FOREIGN KEY (tipoareaumida)
	 REFERENCES dominios.tipo_area_umida (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_area_umida_a ALTER COLUMN tipoareaumida SET DEFAULT 9999#

CREATE TABLE edgv.hid_barragem_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT hid_barragem_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_l_geom ON edgv.hid_barragem_l USING gist (geom)#

ALTER TABLE edgv.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_l ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_l
	 ADD CONSTRAINT hid_barragem_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_barragem_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT hid_barragem_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_p_geom ON edgv.hid_barragem_p USING gist (geom)#

ALTER TABLE edgv.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_p ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_p
	 ADD CONSTRAINT hid_barragem_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.hid_barragem_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 matconstr smallint NOT NULL,
	 usoprincipal smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT hid_barragem_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX hid_barragem_a_geom ON edgv.hid_barragem_a USING gist (geom)#

ALTER TABLE edgv.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_usoprincipal_fk FOREIGN KEY (usoprincipal)
	 REFERENCES dominios.uso_principal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_a ALTER COLUMN usoprincipal SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.hid_barragem_a
	 ADD CONSTRAINT hid_barragem_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.hid_barragem_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.laz_sitio_arqueologico_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT laz_sitio_arqueologico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_sitio_arqueologico_p_geom ON edgv.laz_sitio_arqueologico_p USING gist (geom)#

ALTER TABLE edgv.laz_sitio_arqueologico_p
	 ADD CONSTRAINT laz_sitio_arqueologico_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_sitio_arqueologico_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.laz_sitio_arqueologico_p
	 ADD CONSTRAINT laz_sitio_arqueologico_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_sitio_arqueologico_p
	 ADD CONSTRAINT laz_sitio_arqueologico_p_cultura_check 
	 CHECK (cultura = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.laz_sitio_arqueologico_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.laz_sitio_arqueologico_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_sitio_arqueologico_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_sitio_arqueologico_a_geom ON edgv.laz_sitio_arqueologico_a USING gist (geom)#

ALTER TABLE edgv.laz_sitio_arqueologico_a
	 ADD CONSTRAINT laz_sitio_arqueologico_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_sitio_arqueologico_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.laz_sitio_arqueologico_a
	 ADD CONSTRAINT laz_sitio_arqueologico_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_sitio_arqueologico_a
	 ADD CONSTRAINT laz_sitio_arqueologico_a_cultura_check 
	 CHECK (cultura = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.laz_sitio_arqueologico_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.laz_pista_competicao_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipopistacomp smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT laz_pista_competicao_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_pista_competicao_l_geom ON edgv.laz_pista_competicao_l USING gist (geom)#

ALTER TABLE edgv.laz_pista_competicao_l
	 ADD CONSTRAINT laz_pista_competicao_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_l
	 ADD CONSTRAINT laz_pista_competicao_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_l
	 ADD CONSTRAINT laz_pista_competicao_l_tipopistacomp_fk FOREIGN KEY (tipopistacomp)
	 REFERENCES dominios.tipo_pista_comp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_l ALTER COLUMN tipopistacomp SET DEFAULT 9999#

CREATE TABLE edgv.laz_pista_competicao_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipopistacomp smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT laz_pista_competicao_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_pista_competicao_p_geom ON edgv.laz_pista_competicao_p USING gist (geom)#

ALTER TABLE edgv.laz_pista_competicao_p
	 ADD CONSTRAINT laz_pista_competicao_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_p
	 ADD CONSTRAINT laz_pista_competicao_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_p
	 ADD CONSTRAINT laz_pista_competicao_p_tipopistacomp_fk FOREIGN KEY (tipopistacomp)
	 REFERENCES dominios.tipo_pista_comp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_p ALTER COLUMN tipopistacomp SET DEFAULT 9999#

CREATE TABLE edgv.laz_pista_competicao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipopistacomp smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_pista_competicao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_pista_competicao_a_geom ON edgv.laz_pista_competicao_a USING gist (geom)#

ALTER TABLE edgv.laz_pista_competicao_a
	 ADD CONSTRAINT laz_pista_competicao_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_a
	 ADD CONSTRAINT laz_pista_competicao_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.laz_pista_competicao_a
	 ADD CONSTRAINT laz_pista_competicao_a_tipopistacomp_fk FOREIGN KEY (tipopistacomp)
	 REFERENCES dominios.tipo_pista_comp (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_pista_competicao_a ALTER COLUMN tipopistacomp SET DEFAULT 9999#

CREATE TABLE edgv.laz_arquibancada_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_arquibancada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_arquibancada_a_geom ON edgv.laz_arquibancada_a USING gist (geom)#

ALTER TABLE edgv.laz_arquibancada_a
	 ADD CONSTRAINT laz_arquibancada_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_arquibancada_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_arquibancada_a
	 ADD CONSTRAINT laz_arquibancada_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_arquibancada_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.laz_campo_quadra_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocampoquadra smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT laz_campo_quadra_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_campo_quadra_p_geom ON edgv.laz_campo_quadra_p USING gist (geom)#

ALTER TABLE edgv.laz_campo_quadra_p
	 ADD CONSTRAINT laz_campo_quadra_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_campo_quadra_p
	 ADD CONSTRAINT laz_campo_quadra_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.laz_campo_quadra_p
	 ADD CONSTRAINT laz_campo_quadra_p_tipocampoquadra_fk FOREIGN KEY (tipocampoquadra)
	 REFERENCES dominios.tipo_campo_quadra (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_p ALTER COLUMN tipocampoquadra SET DEFAULT 9999#

CREATE TABLE edgv.laz_campo_quadra_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 tipocampoquadra smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_campo_quadra_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_campo_quadra_a_geom ON edgv.laz_campo_quadra_a USING gist (geom)#

ALTER TABLE edgv.laz_campo_quadra_a
	 ADD CONSTRAINT laz_campo_quadra_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_campo_quadra_a
	 ADD CONSTRAINT laz_campo_quadra_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.laz_campo_quadra_a
	 ADD CONSTRAINT laz_campo_quadra_a_tipocampoquadra_fk FOREIGN KEY (tipocampoquadra)
	 REFERENCES dominios.tipo_campo_quadra (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_campo_quadra_a ALTER COLUMN tipocampoquadra SET DEFAULT 9999#

CREATE TABLE edgv.laz_piscina_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_piscina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_piscina_a_geom ON edgv.laz_piscina_a USING gist (geom)#

ALTER TABLE edgv.laz_piscina_a
	 ADD CONSTRAINT laz_piscina_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_piscina_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.laz_piscina_a
	 ADD CONSTRAINT laz_piscina_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_piscina_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.laz_ruina_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT laz_ruina_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_ruina_p_geom ON edgv.laz_ruina_p USING gist (geom)#

ALTER TABLE edgv.laz_ruina_p
	 ADD CONSTRAINT laz_ruina_p_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_ruina_p ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.laz_ruina_p
	 ADD CONSTRAINT laz_ruina_p_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_ruina_p
	 ADD CONSTRAINT laz_ruina_p_cultura_check 
	 CHECK (cultura = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.laz_ruina_p ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.laz_ruina_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 turistica smallint NOT NULL,
	 cultura smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT laz_ruina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX laz_ruina_a_geom ON edgv.laz_ruina_a USING gist (geom)#

ALTER TABLE edgv.laz_ruina_a
	 ADD CONSTRAINT laz_ruina_a_turistica_fk FOREIGN KEY (turistica)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_ruina_a ALTER COLUMN turistica SET DEFAULT 9999#

ALTER TABLE edgv.laz_ruina_a
	 ADD CONSTRAINT laz_ruina_a_cultura_fk FOREIGN KEY (cultura)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.laz_ruina_a
	 ADD CONSTRAINT laz_ruina_a_cultura_check 
	 CHECK (cultura = ANY(ARRAY[1 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.laz_ruina_a ALTER COLUMN cultura SET DEFAULT 9999#

CREATE TABLE edgv.lml_pais_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 sigla varchar(3),
	 codiso3166 varchar(3),
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_pais_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_pais_a_geom ON edgv.lml_pais_a USING gist (geom)#

CREATE TABLE edgv.lml_posic_geo_localidade_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 identificador varchar(80),
	 latitude varchar(15) NOT NULL,
	 longitude varchar(15) NOT NULL,
	 nomelocal varchar(80) NOT NULL,
	 anodereferencia integer NOT NULL,
	 tipolocalidade smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lml_posic_geo_localidade_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_posic_geo_localidade_p_geom ON edgv.lml_posic_geo_localidade_p USING gist (geom)#

ALTER TABLE edgv.lml_posic_geo_localidade_p
	 ADD CONSTRAINT lml_posic_geo_localidade_p_tipolocalidade_fk FOREIGN KEY (tipolocalidade)
	 REFERENCES dominios.tipo_localidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_posic_geo_localidade_p ALTER COLUMN tipolocalidade SET DEFAULT 9999#

CREATE TABLE edgv.lml_distrito_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geocodigo varchar(15) NOT NULL,
	 anodereferencia integer,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_distrito_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_distrito_a_geom ON edgv.lml_distrito_a USING gist (geom)#

CREATE TABLE edgv.lml_area_densamente_edificada_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_area_densamente_edificada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_area_densamente_edificada_a_geom ON edgv.lml_area_densamente_edificada_a USING gist (geom)#

CREATE TABLE edgv.lml_unidade_federacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geocodigo varchar(15) NOT NULL,
	 sigla smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_unidade_federacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_unidade_federacao_a_geom ON edgv.lml_unidade_federacao_a USING gist (geom)#

ALTER TABLE edgv.lml_unidade_federacao_a
	 ADD CONSTRAINT lml_unidade_federacao_a_sigla_fk FOREIGN KEY (sigla)
	 REFERENCES dominios.sigla_uf (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_federacao_a ALTER COLUMN sigla SET DEFAULT 9999#

CREATE TABLE edgv.lml_terra_indigena_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 classificacao varchar(100),
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 situacaojuridica smallint NOT NULL,
	 datasituacaojuridica varchar(10),
	 grupoetnico varchar(100),
	 perimetrooficial real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_terra_indigena_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_terra_indigena_a_geom ON edgv.lml_terra_indigena_a USING gist (geom)#

ALTER TABLE edgv.lml_terra_indigena_a
	 ADD CONSTRAINT lml_terra_indigena_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_terra_indigena_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.lml_terra_indigena_a
	 ADD CONSTRAINT lml_terra_indigena_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_terra_indigena_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.lml_terra_indigena_a
	 ADD CONSTRAINT lml_terra_indigena_a_situacaojuridica_fk FOREIGN KEY (situacaojuridica)
	 REFERENCES dominios.situacao_juridica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_terra_indigena_a ALTER COLUMN situacaojuridica SET DEFAULT 9999#

CREATE TABLE edgv.lml_unidade_protecao_integral_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 anocriacao varchar(4),
	 historicomodificacoes varchar(255),
	 sigla varchar(6),
	 atolegal varchar(100),
	 areaoficial varchar(15),
	 administracao smallint NOT NULL,
	 classificacao varchar(100),
	 jurisdicao smallint NOT NULL,
	 tipounidprotegida smallint NOT NULL,
	 tipounidprotinteg smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_unidade_protecao_integral_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_unidade_protecao_integral_a_geom ON edgv.lml_unidade_protecao_integral_a USING gist (geom)#

ALTER TABLE edgv.lml_unidade_protecao_integral_a
	 ADD CONSTRAINT lml_unidade_protecao_integral_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_protecao_integral_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_protecao_integral_a
	 ADD CONSTRAINT lml_unidade_protecao_integral_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_protecao_integral_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_protecao_integral_a
	 ADD CONSTRAINT lml_unidade_protecao_integral_a_tipounidprotegida_fk FOREIGN KEY (tipounidprotegida)
	 REFERENCES dominios.tipo_unid_protegida (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_protecao_integral_a
	 ADD CONSTRAINT lml_unidade_protecao_integral_a_tipounidprotegida_check 
	 CHECK (tipounidprotegida = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.lml_unidade_protecao_integral_a ALTER COLUMN tipounidprotegida SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_protecao_integral_a
	 ADD CONSTRAINT lml_unidade_protecao_integral_a_tipounidprotinteg_fk FOREIGN KEY (tipounidprotinteg)
	 REFERENCES dominios.tipo_unid_prot_integ (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_protecao_integral_a ALTER COLUMN tipounidprotinteg SET DEFAULT 9999#

CREATE TABLE edgv.lml_unidade_uso_sustentavel_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 anocriacao varchar(4),
	 historicomodificacoes varchar(255),
	 sigla varchar(6),
	 atolegal varchar(100),
	 areaoficial varchar(15),
	 administracao smallint NOT NULL,
	 classificacao varchar(100),
	 jurisdicao smallint NOT NULL,
	 tipounidprotegida smallint NOT NULL,
	 tipounidusosust smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_unidade_uso_sustentavel_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_unidade_uso_sustentavel_a_geom ON edgv.lml_unidade_uso_sustentavel_a USING gist (geom)#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lml_unidade_uso_sustentavel_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lml_unidade_uso_sustentavel_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lml_unidade_uso_sustentavel_a_tipounidprotegida_fk FOREIGN KEY (tipounidprotegida)
	 REFERENCES dominios.tipo_unid_protegida (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lml_unidade_uso_sustentavel_a_tipounidprotegida_check 
	 CHECK (tipounidprotegida = ANY(ARRAY[3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.lml_unidade_uso_sustentavel_a ALTER COLUMN tipounidprotegida SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a
	 ADD CONSTRAINT lml_unidade_uso_sustentavel_a_tipounidusosust_fk FOREIGN KEY (tipounidusosust)
	 REFERENCES dominios.tipo_unid_uso_sust (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_uso_sustentavel_a ALTER COLUMN tipounidusosust SET DEFAULT 9999#

CREATE TABLE edgv.lml_municipio_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geocodigo varchar(15) NOT NULL,
	 anodereferencia integer,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_municipio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_municipio_a_geom ON edgv.lml_municipio_a USING gist (geom)#

CREATE TABLE edgv.lml_terra_publica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 classificacao varchar(100),
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_terra_publica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_terra_publica_a_geom ON edgv.lml_terra_publica_a USING gist (geom)#

ALTER TABLE edgv.lml_terra_publica_a
	 ADD CONSTRAINT lml_terra_publica_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_terra_publica_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.lml_terra_publica_a
	 ADD CONSTRAINT lml_terra_publica_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_terra_publica_a ALTER COLUMN administracao SET DEFAULT 9999#

CREATE TABLE edgv.lml_area_pub_militar_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 classificacao varchar(100),
	 administracao smallint NOT NULL,
	 jurisdicao smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_area_pub_militar_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_area_pub_militar_a_geom ON edgv.lml_area_pub_militar_a USING gist (geom)#

ALTER TABLE edgv.lml_area_pub_militar_a
	 ADD CONSTRAINT lml_area_pub_militar_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_area_pub_militar_a
	 ADD CONSTRAINT lml_area_pub_militar_a_administracao_check 
	 CHECK (administracao = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.lml_area_pub_militar_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.lml_area_pub_militar_a
	 ADD CONSTRAINT lml_area_pub_militar_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_area_pub_militar_a
	 ADD CONSTRAINT lml_area_pub_militar_a_jurisdicao_check 
	 CHECK (jurisdicao = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.lml_area_pub_militar_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

CREATE TABLE edgv.lml_area_urbana_isolada_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoassociado smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_area_urbana_isolada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_area_urbana_isolada_a_geom ON edgv.lml_area_urbana_isolada_a USING gist (geom)#

ALTER TABLE edgv.lml_area_urbana_isolada_a
	 ADD CONSTRAINT lml_area_urbana_isolada_a_tipoassociado_fk FOREIGN KEY (tipoassociado)
	 REFERENCES dominios.tipo_associado (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_area_urbana_isolada_a ALTER COLUMN tipoassociado SET DEFAULT 9999#

CREATE TABLE edgv.lml_nome_local_p(
	 id serial NOT NULL,
	 nome varchar(80) NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT lml_nome_local_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_nome_local_p_geom ON edgv.lml_nome_local_p USING gist (geom)#

CREATE TABLE edgv.lml_unidade_conservacao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 codidentificadorunico varchar(50),
	 arealegal real,
	 anocriacao varchar(4),
	 historicomodificacoes varchar(255),
	 sigla varchar(6),
	 atolegal varchar(100),
	 areaoficial varchar(15),
	 administracao smallint NOT NULL,
	 classificacao varchar(100),
	 jurisdicao smallint NOT NULL,
	 tipounidprotegida smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT lml_unidade_conservacao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX lml_unidade_conservacao_a_geom ON edgv.lml_unidade_conservacao_a USING gist (geom)#

ALTER TABLE edgv.lml_unidade_conservacao_a
	 ADD CONSTRAINT lml_unidade_conservacao_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_conservacao_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_conservacao_a
	 ADD CONSTRAINT lml_unidade_conservacao_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_conservacao_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.lml_unidade_conservacao_a
	 ADD CONSTRAINT lml_unidade_conservacao_a_tipounidprotegida_fk FOREIGN KEY (tipounidprotegida)
	 REFERENCES dominios.tipo_unid_protegida (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.lml_unidade_conservacao_a
	 ADD CONSTRAINT lml_unidade_conservacao_a_tipounidprotegida_check 
	 CHECK (tipounidprotegida = ANY(ARRAY[4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.lml_unidade_conservacao_a ALTER COLUMN tipounidprotegida SET DEFAULT 9999#

CREATE TABLE edgv.pto_marco_de_limite_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipomarcolim smallint NOT NULL,
	 latitude varchar(15) NOT NULL,
	 longitude varchar(15) NOT NULL,
	 altitudeortometrica real,
	 sistemageodesico smallint NOT NULL,
	 outrarefplan varchar(20),
	 referencialaltim smallint,
	 outrarefalt varchar(20),
	 codigo varchar(9),
	 orgaoenteresp varchar(15),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_marco_de_limite_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_marco_de_limite_p_geom ON edgv.pto_marco_de_limite_p USING gist (geom)#

ALTER TABLE edgv.pto_marco_de_limite_p
	 ADD CONSTRAINT pto_marco_de_limite_p_tipomarcolim_fk FOREIGN KEY (tipomarcolim)
	 REFERENCES dominios.tipo_hierarquia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_marco_de_limite_p ALTER COLUMN tipomarcolim SET DEFAULT 9999#

ALTER TABLE edgv.pto_marco_de_limite_p
	 ADD CONSTRAINT pto_marco_de_limite_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistema_geodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_marco_de_limite_p ALTER COLUMN sistemageodesico SET DEFAULT 9999#

ALTER TABLE edgv.pto_marco_de_limite_p
	 ADD CONSTRAINT pto_marco_de_limite_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencial_altim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_marco_de_limite_p ALTER COLUMN referencialaltim SET DEFAULT 9999#

CREATE TABLE edgv.pto_pto_ref_geod_topo_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 tiporef smallint NOT NULL,
	 latitude varchar(16) NOT NULL,
	 longitude varchar(16) NOT NULL,
	 altitudeortometrica real,
	 altitudegeometrica real,
	 sistemageodesico smallint NOT NULL,
	 outrarefplan varchar(20),
	 referencialaltim smallint NOT NULL,
	 outrarefalt varchar(20),
	 codponto varchar(12),
	 obs varchar(255),
	 nome varchar(80),
	 proximidade smallint NOT NULL,
	 tipoptorefgeodtopo smallint NOT NULL,
	 redereferencia smallint NOT NULL,
	 referencialgrav smallint NOT NULL,
	 situacaomarco smallint,
	 datavisita varchar(10),
	 datamedicao varchar(10),
	 valorgravidade real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_ref_geod_topo_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_ref_geod_topo_p_geom ON edgv.pto_pto_ref_geod_topo_p USING gist (geom)#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_tiporef_fk FOREIGN KEY (tiporef)
	 REFERENCES dominios.tipo_ref (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN tiporef SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistema_geodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN sistemageodesico SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencial_altim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN referencialaltim SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_proximidade_fk FOREIGN KEY (proximidade)
	 REFERENCES dominios.proximidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN proximidade SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_tipoptorefgeodtopo_fk FOREIGN KEY (tipoptorefgeodtopo)
	 REFERENCES dominios.tipo_pto_ref_geod_topo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN tipoptorefgeodtopo SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_redereferencia_fk FOREIGN KEY (redereferencia)
	 REFERENCES dominios.rede_referencia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN redereferencia SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_referencialgrav_fk FOREIGN KEY (referencialgrav)
	 REFERENCES dominios.referencial_grav (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN referencialgrav SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p
	 ADD CONSTRAINT pto_pto_ref_geod_topo_p_situacaomarco_fk FOREIGN KEY (situacaomarco)
	 REFERENCES dominios.situacao_marco (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_ref_geod_topo_p ALTER COLUMN situacaomarco SET DEFAULT 9999#

CREATE TABLE edgv.pto_pto_geod_topo_controle_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 tiporef smallint NOT NULL,
	 latitude varchar(16) NOT NULL,
	 longitude varchar(16) NOT NULL,
	 altitudeortometrica real,
	 altitudegeometrica real,
	 sistemageodesico smallint NOT NULL,
	 outrarefplan varchar(20),
	 referencialaltim smallint NOT NULL,
	 outrarefalt varchar(20),
	 codponto varchar(9),
	 obs varchar(255),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_geod_topo_controle_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_geod_topo_controle_p_geom ON edgv.pto_pto_geod_topo_controle_p USING gist (geom)#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p
	 ADD CONSTRAINT pto_pto_geod_topo_controle_p_tiporef_fk FOREIGN KEY (tiporef)
	 REFERENCES dominios.tipo_ref (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p ALTER COLUMN tiporef SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p
	 ADD CONSTRAINT pto_pto_geod_topo_controle_p_sistemageodesico_fk FOREIGN KEY (sistemageodesico)
	 REFERENCES dominios.sistema_geodesico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p ALTER COLUMN sistemageodesico SET DEFAULT 9999#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p
	 ADD CONSTRAINT pto_pto_geod_topo_controle_p_referencialaltim_fk FOREIGN KEY (referencialaltim)
	 REFERENCES dominios.referencial_altim (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_geod_topo_controle_p ALTER COLUMN referencialaltim SET DEFAULT 9999#

CREATE TABLE edgv.pto_pto_est_med_fenomenos_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoptoestmed smallint NOT NULL,
	 codestacao varchar(50),
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT pto_pto_est_med_fenomenos_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX pto_pto_est_med_fenomenos_p_geom ON edgv.pto_pto_est_med_fenomenos_p USING gist (geom)#

ALTER TABLE edgv.pto_pto_est_med_fenomenos_p
	 ADD CONSTRAINT pto_pto_est_med_fenomenos_p_tipoptoestmed_fk FOREIGN KEY (tipoptoestmed)
	 REFERENCES dominios.tipo_pto_est_med (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.pto_pto_est_med_fenomenos_p ALTER COLUMN tipoptoestmed SET DEFAULT 9999#

CREATE TABLE edgv.rel_curva_nivel_l(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 cota integer NOT NULL,
	 depressao boolean NOT NULL,
	 tipocurvanivel smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_curva_nivel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_curva_nivel_l_geom ON edgv.rel_curva_nivel_l USING gist (geom)#

ALTER TABLE edgv.rel_curva_nivel_l
	 ADD CONSTRAINT rel_curva_nivel_l_tipocurvanivel_fk FOREIGN KEY (tipocurvanivel)
	 REFERENCES dominios.tipo_curva_nivel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_curva_nivel_l ALTER COLUMN tipocurvanivel SET DEFAULT 9999#

CREATE TABLE edgv.rel_gruta_caverna_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_gruta_caverna_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_gruta_caverna_l_geom ON edgv.rel_gruta_caverna_l USING gist (geom)#

ALTER TABLE edgv.rel_gruta_caverna_l
	 ADD CONSTRAINT rel_gruta_caverna_l_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_gruta_caverna_l
	 ADD CONSTRAINT rel_gruta_caverna_l_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[15 :: SMALLINT, 20 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_gruta_caverna_l ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_gruta_caverna_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_gruta_caverna_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_gruta_caverna_p_geom ON edgv.rel_gruta_caverna_p USING gist (geom)#

ALTER TABLE edgv.rel_gruta_caverna_p
	 ADD CONSTRAINT rel_gruta_caverna_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_gruta_caverna_p
	 ADD CONSTRAINT rel_gruta_caverna_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[15 :: SMALLINT, 20 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_gruta_caverna_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_rocha_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 formarocha smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_rocha_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_rocha_l_geom ON edgv.rel_rocha_l USING gist (geom)#

ALTER TABLE edgv.rel_rocha_l
	 ADD CONSTRAINT rel_rocha_l_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_l
	 ADD CONSTRAINT rel_rocha_l_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[23 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_rocha_l ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.rel_rocha_l
	 ADD CONSTRAINT rel_rocha_l_formarocha_fk FOREIGN KEY (formarocha)
	 REFERENCES dominios.forma_rocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_l ALTER COLUMN formarocha SET DEFAULT 9999#

CREATE TABLE edgv.rel_rocha_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 formarocha smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_rocha_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_rocha_p_geom ON edgv.rel_rocha_p USING gist (geom)#

ALTER TABLE edgv.rel_rocha_p
	 ADD CONSTRAINT rel_rocha_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_p
	 ADD CONSTRAINT rel_rocha_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[23 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_rocha_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.rel_rocha_p
	 ADD CONSTRAINT rel_rocha_p_formarocha_fk FOREIGN KEY (formarocha)
	 REFERENCES dominios.forma_rocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_p ALTER COLUMN formarocha SET DEFAULT 9999#

CREATE TABLE edgv.rel_rocha_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 formarocha smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_rocha_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_rocha_a_geom ON edgv.rel_rocha_a USING gist (geom)#

ALTER TABLE edgv.rel_rocha_a
	 ADD CONSTRAINT rel_rocha_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_a
	 ADD CONSTRAINT rel_rocha_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[23 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_rocha_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

ALTER TABLE edgv.rel_rocha_a
	 ADD CONSTRAINT rel_rocha_a_formarocha_fk FOREIGN KEY (formarocha)
	 REFERENCES dominios.forma_rocha (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_rocha_a ALTER COLUMN formarocha SET DEFAULT 9999#

CREATE TABLE edgv.rel_corte_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_corte_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_corte_l_geom ON edgv.rel_corte_l USING gist (geom)#

ALTER TABLE edgv.rel_corte_l
	 ADD CONSTRAINT rel_corte_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_l
	 ADD CONSTRAINT rel_corte_l_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[26 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_l ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_corte_l
	 ADD CONSTRAINT rel_corte_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_l
	 ADD CONSTRAINT rel_corte_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_l ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_corte_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_corte_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_corte_p_geom ON edgv.rel_corte_p USING gist (geom)#

ALTER TABLE edgv.rel_corte_p
	 ADD CONSTRAINT rel_corte_p_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_p
	 ADD CONSTRAINT rel_corte_p_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[26 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_p ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_corte_p
	 ADD CONSTRAINT rel_corte_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_p
	 ADD CONSTRAINT rel_corte_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_p ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_corte_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_corte_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_corte_a_geom ON edgv.rel_corte_a USING gist (geom)#

ALTER TABLE edgv.rel_corte_a
	 ADD CONSTRAINT rel_corte_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_a
	 ADD CONSTRAINT rel_corte_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[26 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_corte_a
	 ADD CONSTRAINT rel_corte_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_corte_a
	 ADD CONSTRAINT rel_corte_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_corte_a ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_terreno_exposto_a(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 tipoterrexp smallint,
	 causaexposicao smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_terreno_exposto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_terreno_exposto_a_geom ON edgv.rel_terreno_exposto_a USING gist (geom)#

ALTER TABLE edgv.rel_terreno_exposto_a
	 ADD CONSTRAINT rel_terreno_exposto_a_tipoterrexp_fk FOREIGN KEY (tipoterrexp)
	 REFERENCES dominios.tipo_terreno_exposto (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_terreno_exposto_a ALTER COLUMN tipoterrexp SET DEFAULT 9999#

ALTER TABLE edgv.rel_terreno_exposto_a
	 ADD CONSTRAINT rel_terreno_exposto_a_causaexposicao_fk FOREIGN KEY (causaexposicao)
	 REFERENCES dominios.causa_exposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_terreno_exposto_a ALTER COLUMN causaexposicao SET DEFAULT 9999#

CREATE TABLE edgv.rel_dolina_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_dolina_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_dolina_p_geom ON edgv.rel_dolina_p USING gist (geom)#

ALTER TABLE edgv.rel_dolina_p
	 ADD CONSTRAINT rel_dolina_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_dolina_p
	 ADD CONSTRAINT rel_dolina_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[16 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_dolina_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_dolina_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_dolina_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_dolina_a_geom ON edgv.rel_dolina_a USING gist (geom)#

ALTER TABLE edgv.rel_dolina_a
	 ADD CONSTRAINT rel_dolina_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_dolina_a
	 ADD CONSTRAINT rel_dolina_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[16 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_dolina_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_aterro_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_aterro_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_aterro_l_geom ON edgv.rel_aterro_l USING gist (geom)#

ALTER TABLE edgv.rel_aterro_l
	 ADD CONSTRAINT rel_aterro_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_l
	 ADD CONSTRAINT rel_aterro_l_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[27 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_l ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_aterro_l
	 ADD CONSTRAINT rel_aterro_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_l
	 ADD CONSTRAINT rel_aterro_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_l ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_aterro_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_aterro_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_aterro_p_geom ON edgv.rel_aterro_p USING gist (geom)#

ALTER TABLE edgv.rel_aterro_p
	 ADD CONSTRAINT rel_aterro_p_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_p
	 ADD CONSTRAINT rel_aterro_p_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[27 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_p ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_aterro_p
	 ADD CONSTRAINT rel_aterro_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_p
	 ADD CONSTRAINT rel_aterro_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_p ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_aterro_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_aterro_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_aterro_a_geom ON edgv.rel_aterro_a USING gist (geom)#

ALTER TABLE edgv.rel_aterro_a
	 ADD CONSTRAINT rel_aterro_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_a
	 ADD CONSTRAINT rel_aterro_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[27 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

ALTER TABLE edgv.rel_aterro_a
	 ADD CONSTRAINT rel_aterro_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_aterro_a
	 ADD CONSTRAINT rel_aterro_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 23 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_aterro_a ALTER COLUMN matconstr SET DEFAULT 9999#

CREATE TABLE edgv.rel_ponto_cotado_altimetrico_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 cotacomprovada boolean NOT NULL,
	 cota real NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_ponto_cotado_altimetrico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_ponto_cotado_altimetrico_p_geom ON edgv.rel_ponto_cotado_altimetrico_p USING gist (geom)#

CREATE TABLE edgv.rel_elemento_fisiografico_natural_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_elemento_fisiografico_natural_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiografico_natural_l_geom ON edgv.rel_elemento_fisiografico_natural_l USING gist (geom)#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_l
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_l_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_l
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_l_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_elemento_fisiografico_natural_l ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_elemento_fisiografico_natural_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_elemento_fisiografico_natural_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiografico_natural_p_geom ON edgv.rel_elemento_fisiografico_natural_p USING gist (geom)#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_p
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_p
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_elemento_fisiografico_natural_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_elemento_fisiografico_natural_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_elemento_fisiografico_natural_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_elemento_fisiografico_natural_a_geom ON edgv.rel_elemento_fisiografico_natural_a USING gist (geom)#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_a
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_elemento_fisiografico_natural_a
	 ADD CONSTRAINT rel_elemento_fisiografico_natural_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 9 :: SMALLINT, 10 :: SMALLINT, 11 :: SMALLINT, 12 :: SMALLINT, 13 :: SMALLINT, 14 :: SMALLINT, 18 :: SMALLINT, 19 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_elemento_fisiografico_natural_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_pico_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_pico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_pico_p_geom ON edgv.rel_pico_p USING gist (geom)#

ALTER TABLE edgv.rel_pico_p
	 ADD CONSTRAINT rel_pico_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_pico_p
	 ADD CONSTRAINT rel_pico_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[22 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_pico_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_duna_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 fixa boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_duna_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_duna_l_geom ON edgv.rel_duna_l USING gist (geom)#

ALTER TABLE edgv.rel_duna_l
	 ADD CONSTRAINT rel_duna_l_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_duna_l
	 ADD CONSTRAINT rel_duna_l_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[17 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_duna_l ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_duna_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 fixa boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_duna_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_duna_p_geom ON edgv.rel_duna_p USING gist (geom)#

ALTER TABLE edgv.rel_duna_p
	 ADD CONSTRAINT rel_duna_p_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_duna_p
	 ADD CONSTRAINT rel_duna_p_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[17 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_duna_p ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_duna_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoelemnat smallint NOT NULL,
	 fixa boolean NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_duna_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_duna_a_geom ON edgv.rel_duna_a USING gist (geom)#

ALTER TABLE edgv.rel_duna_a
	 ADD CONSTRAINT rel_duna_a_tipoelemnat_fk FOREIGN KEY (tipoelemnat)
	 REFERENCES dominios.tipo_elem_nat (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_duna_a
	 ADD CONSTRAINT rel_duna_a_tipoelemnat_check 
	 CHECK (tipoelemnat = ANY(ARRAY[17 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_duna_a ALTER COLUMN tipoelemnat SET DEFAULT 9999#

CREATE TABLE edgv.rel_curva_batimetrica_l(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 profundidade integer NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_curva_batimetrica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_curva_batimetrica_l_geom ON edgv.rel_curva_batimetrica_l USING gist (geom)#

CREATE TABLE edgv.rel_alteracao_fisiografica_antropica_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rel_alteracao_fisiografica_antropica_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_alteracao_fisiografica_antropica_l_geom ON edgv.rel_alteracao_fisiografica_antropica_l USING gist (geom)#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_l
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_l_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_l
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_l_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[0 :: SMALLINT, 24 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 32 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_l ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

CREATE TABLE edgv.rel_alteracao_fisiografica_antropica_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_alteracao_fisiografica_antropica_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_alteracao_fisiografica_antropica_p_geom ON edgv.rel_alteracao_fisiografica_antropica_p USING gist (geom)#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_p
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_p_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_p
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_p_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[0 :: SMALLINT, 24 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 32 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_p ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

CREATE TABLE edgv.rel_alteracao_fisiografica_antropica_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoalterantrop smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rel_alteracao_fisiografica_antropica_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_alteracao_fisiografica_antropica_a_geom ON edgv.rel_alteracao_fisiografica_antropica_a USING gist (geom)#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_a
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_a_tipoalterantrop_fk FOREIGN KEY (tipoalterantrop)
	 REFERENCES dominios.tipo_alter_antrop (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_a
	 ADD CONSTRAINT rel_alteracao_fisiografica_antropica_a_tipoalterantrop_check 
	 CHECK (tipoalterantrop = ANY(ARRAY[0 :: SMALLINT, 24 :: SMALLINT, 28 :: SMALLINT, 29 :: SMALLINT, 32 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rel_alteracao_fisiografica_antropica_a ALTER COLUMN tipoalterantrop SET DEFAULT 9999#

CREATE TABLE edgv.rel_ponto_cotado_batimetrico_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 profundidade real NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT rel_ponto_cotado_batimetrico_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rel_ponto_cotado_batimetrico_p_geom ON edgv.rel_ponto_cotado_batimetrico_p USING gist (geom)#

CREATE TABLE edgv.rod_trecho_rodoviario_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(100),
	 revestimento smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 trafego smallint NOT NULL,
	 tipopavimentacao smallint NOT NULL,
	 tipovia smallint NOT NULL,
	 sigla varchar(6),
	 codtrechorod varchar(25),
	 limitevelocidade real,
	 trechoemperimetrourbano boolean,
	 acostamento boolean,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT rod_trecho_rodoviario_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rod_trecho_rodoviario_l_geom ON edgv.rod_trecho_rodoviario_l USING gist (geom)#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN canteirodivisorio SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN trafego SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_tipovia_fk FOREIGN KEY (tipovia)
	 REFERENCES dominios.tipo_via (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_l
	 ADD CONSTRAINT rod_trecho_rodoviario_l_tipovia_check 
	 CHECK (tipovia = ANY(ARRAY[2 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rod_trecho_rodoviario_l ALTER COLUMN tipovia SET DEFAULT 9999#

CREATE TABLE edgv.rod_trecho_rodoviario_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 jurisdicao smallint NOT NULL,
	 administracao smallint NOT NULL,
	 concessionaria varchar(100),
	 revestimento smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 canteirodivisorio smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 trafego smallint NOT NULL,
	 tipopavimentacao smallint NOT NULL,
	 tipovia smallint NOT NULL,
	 sigla varchar(6),
	 codtrechorod varchar(25),
	 limitevelocidade real,
	 trechoemperimetrourbano boolean,
	 acostamento boolean,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT rod_trecho_rodoviario_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX rod_trecho_rodoviario_a_geom ON edgv.rod_trecho_rodoviario_a USING gist (geom)#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_jurisdicao_fk FOREIGN KEY (jurisdicao)
	 REFERENCES dominios.jurisdicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN jurisdicao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_revestimento_fk FOREIGN KEY (revestimento)
	 REFERENCES dominios.revestimento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN revestimento SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_canteirodivisorio_fk FOREIGN KEY (canteirodivisorio)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN canteirodivisorio SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_trafego_fk FOREIGN KEY (trafego)
	 REFERENCES dominios.trafego (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN trafego SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_tipovia_fk FOREIGN KEY (tipovia)
	 REFERENCES dominios.tipo_via (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.rod_trecho_rodoviario_a
	 ADD CONSTRAINT rod_trecho_rodoviario_a_tipovia_check 
	 CHECK (tipovia = ANY(ARRAY[2 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.rod_trecho_rodoviario_a ALTER COLUMN tipovia SET DEFAULT 9999#

CREATE TABLE edgv.snb_dep_abast_agua_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipodepgeral smallint,
	 matconstr smallint,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tipoconteudo smallint,
	 unidadevolume smallint,
	 valorvolume real,
	 tratamento smallint NOT NULL,
	 estadofisico smallint,
	 finalidadedep smallint NOT NULL,
	 situacaoagua smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT snb_dep_abast_agua_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX snb_dep_abast_agua_p_geom ON edgv.snb_dep_abast_agua_p USING gist (geom)#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipo_dep_geral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipodepgeral_check 
	 CHECK (tipodepgeral = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN tipodepgeral SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipo_exposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN tipoexposicao SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[46 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN tipoprodutoresiduo SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipo_conteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN tipoconteudo SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidade_volume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN unidadevolume SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN tratamento SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_estadofisico_fk FOREIGN KEY (estadofisico)
	 REFERENCES dominios.estado_fisico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN estadofisico SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_finalidadedep_fk FOREIGN KEY (finalidadedep)
	 REFERENCES dominios.finalidade_deposito (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN finalidadedep SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_p
	 ADD CONSTRAINT snb_dep_abast_agua_p_situacaoagua_fk FOREIGN KEY (situacaoagua)
	 REFERENCES dominios.situacao_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_p ALTER COLUMN situacaoagua SET DEFAULT 9999#

CREATE TABLE edgv.snb_dep_abast_agua_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 tipodepgeral smallint,
	 matconstr smallint,
	 tipoexposicao smallint NOT NULL,
	 tipoprodutoresiduo smallint NOT NULL,
	 tipoconteudo smallint,
	 unidadevolume smallint,
	 valorvolume real,
	 tratamento smallint NOT NULL,
	 estadofisico smallint,
	 finalidadedep smallint NOT NULL,
	 situacaoagua smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT snb_dep_abast_agua_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX snb_dep_abast_agua_a_geom ON edgv.snb_dep_abast_agua_a USING gist (geom)#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipodepgeral_fk FOREIGN KEY (tipodepgeral)
	 REFERENCES dominios.tipo_dep_geral (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipodepgeral_check 
	 CHECK (tipodepgeral = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN tipodepgeral SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipoexposicao_fk FOREIGN KEY (tipoexposicao)
	 REFERENCES dominios.tipo_exposicao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN tipoexposicao SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipoprodutoresiduo_fk FOREIGN KEY (tipoprodutoresiduo)
	 REFERENCES dominios.tipo_produto_residuo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipoprodutoresiduo_check 
	 CHECK (tipoprodutoresiduo = ANY(ARRAY[46 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN tipoprodutoresiduo SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tipoconteudo_fk FOREIGN KEY (tipoconteudo)
	 REFERENCES dominios.tipo_conteudo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN tipoconteudo SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_unidadevolume_fk FOREIGN KEY (unidadevolume)
	 REFERENCES dominios.unidade_volume (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN unidadevolume SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_tratamento_fk FOREIGN KEY (tratamento)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN tratamento SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_estadofisico_fk FOREIGN KEY (estadofisico)
	 REFERENCES dominios.estado_fisico (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN estadofisico SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_finalidadedep_fk FOREIGN KEY (finalidadedep)
	 REFERENCES dominios.finalidade_deposito (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN finalidadedep SET DEFAULT 9999#

ALTER TABLE edgv.snb_dep_abast_agua_a
	 ADD CONSTRAINT snb_dep_abast_agua_a_situacaoagua_fk FOREIGN KEY (situacaoagua)
	 REFERENCES dominios.situacao_agua (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_dep_abast_agua_a ALTER COLUMN situacaoagua SET DEFAULT 9999#

CREATE TABLE edgv.snb_barragem_calcadao_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoequipdesenvsocial smallint NOT NULL,
	 sigla varchar(80),
	 codequipdesenvsocial varchar(80),
	 localizacaoequipdesenvsocial smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT snb_barragem_calcadao_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX snb_barragem_calcadao_a_geom ON edgv.snb_barragem_calcadao_a USING gist (geom)#

ALTER TABLE edgv.snb_barragem_calcadao_a
	 ADD CONSTRAINT snb_barragem_calcadao_a_tipoequipdesenvsocial_fk FOREIGN KEY (tipoequipdesenvsocial)
	 REFERENCES dominios.tipo_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_barragem_calcadao_a
	 ADD CONSTRAINT snb_barragem_calcadao_a_tipoequipdesenvsocial_check 
	 CHECK (tipoequipdesenvsocial = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.snb_barragem_calcadao_a ALTER COLUMN tipoequipdesenvsocial SET DEFAULT 9999#

ALTER TABLE edgv.snb_barragem_calcadao_a
	 ADD CONSTRAINT snb_barragem_calcadao_a_localizacaoequipdesenvsocial_fk FOREIGN KEY (localizacaoequipdesenvsocial)
	 REFERENCES dominios.local_equip_desenv_social (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.snb_barragem_calcadao_a ALTER COLUMN localizacaoequipdesenvsocial SET DEFAULT 9999#

CREATE TABLE edgv.tra_entroncamento_pto_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipoentroncamento smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_entroncamento_pto_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_entroncamento_pto_p_geom ON edgv.tra_entroncamento_pto_p USING gist (geom)#

ALTER TABLE edgv.tra_entroncamento_pto_p
	 ADD CONSTRAINT tra_entroncamento_pto_p_tipoentroncamento_fk FOREIGN KEY (tipoentroncamento)
	 REFERENCES dominios.tipo_entroncamento (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_entroncamento_pto_p ALTER COLUMN tipoentroncamento SET DEFAULT 9999#

CREATE TABLE edgv.tra_funicular_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_funicular_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_funicular_l_geom ON edgv.tra_funicular_l USING gist (geom)#

ALTER TABLE edgv.tra_funicular_l
	 ADD CONSTRAINT tra_funicular_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_funicular_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_funicular_l
	 ADD CONSTRAINT tra_funicular_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_funicular_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.tra_ponte_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipoponte smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 cargasuportmaxima real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_ponte_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponte_l_geom ON edgv.tra_ponte_l USING gist (geom)#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_l ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_l
	 ADD CONSTRAINT tra_ponte_l_tipoponte_fk FOREIGN KEY (tipoponte)
	 REFERENCES dominios.tipo_ponte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_l ALTER COLUMN tipoponte SET DEFAULT 9999#

CREATE TABLE edgv.tra_ponte_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipoponte smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 cargasuportmaxima real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_ponte_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponte_p_geom ON edgv.tra_ponte_p USING gist (geom)#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_p ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_p
	 ADD CONSTRAINT tra_ponte_p_tipoponte_fk FOREIGN KEY (tipoponte)
	 REFERENCES dominios.tipo_ponte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_p ALTER COLUMN tipoponte SET DEFAULT 9999#

CREATE TABLE edgv.tra_ponte_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipoponte smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 cargasuportmaxima real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_ponte_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_ponte_a_geom ON edgv.tra_ponte_a USING gist (geom)#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_a ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_matconstr_check 
	 CHECK (matconstr = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 8 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_ponte_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_ponte_a
	 ADD CONSTRAINT tra_ponte_a_tipoponte_fk FOREIGN KEY (tipoponte)
	 REFERENCES dominios.tipo_ponte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_ponte_a ALTER COLUMN tipoponte SET DEFAULT 9999#

CREATE TABLE edgv.tra_caminho_aereo_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipocaminhoaereo smallint NOT NULL,
	 tipousocaminhoaer smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_caminho_aereo_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_caminho_aereo_l_geom ON edgv.tra_caminho_aereo_l USING gist (geom)#

ALTER TABLE edgv.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_tipocaminhoaereo_fk FOREIGN KEY (tipocaminhoaereo)
	 REFERENCES dominios.tipo_caminho_aereo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_caminho_aereo_l ALTER COLUMN tipocaminhoaereo SET DEFAULT 9999#

ALTER TABLE edgv.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_tipousocaminhoaer_fk FOREIGN KEY (tipousocaminhoaer)
	 REFERENCES dominios.tipo_transporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_caminho_aereo_l ALTER COLUMN tipousocaminhoaer SET DEFAULT 9999#

ALTER TABLE edgv.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_caminho_aereo_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_caminho_aereo_l
	 ADD CONSTRAINT tra_caminho_aereo_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_caminho_aereo_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

CREATE TABLE edgv.tra_trilha_picada_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_trilha_picada_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_trilha_picada_l_geom ON edgv.tra_trilha_picada_l USING gist (geom)#

CREATE TABLE edgv.tra_passagem_nivel_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_passagem_nivel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passagem_nivel_p_geom ON edgv.tra_passagem_nivel_p USING gist (geom)#

CREATE TABLE edgv.tra_travessia_pedestre_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipotravessiaped smallint NOT NULL,
	 extensao real,
	 largura real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_travessia_pedestre_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_pedestre_l_geom ON edgv.tra_travessia_pedestre_l USING gist (geom)#

ALTER TABLE edgv.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_l ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_l
	 ADD CONSTRAINT tra_travessia_pedestre_l_tipotravessiaped_fk FOREIGN KEY (tipotravessiaped)
	 REFERENCES dominios.tipo_travessia_ped (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_l ALTER COLUMN tipotravessiaped SET DEFAULT 9999#

CREATE TABLE edgv.tra_travessia_pedestre_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipotravessiaped smallint NOT NULL,
	 extensao real,
	 largura real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_travessia_pedestre_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_pedestre_p_geom ON edgv.tra_travessia_pedestre_p USING gist (geom)#

ALTER TABLE edgv.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_p ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_p
	 ADD CONSTRAINT tra_travessia_pedestre_p_tipotravessiaped_fk FOREIGN KEY (tipotravessiaped)
	 REFERENCES dominios.tipo_travessia_ped (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_p ALTER COLUMN tipotravessiaped SET DEFAULT 9999#

CREATE TABLE edgv.tra_travessia_pedestre_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 situacaoespacial smallint NOT NULL,
	 tipotravessiaped smallint NOT NULL,
	 extensao real,
	 largura real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_travessia_pedestre_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_pedestre_a_geom ON edgv.tra_travessia_pedestre_a USING gist (geom)#

ALTER TABLE edgv.tra_travessia_pedestre_a
	 ADD CONSTRAINT tra_travessia_pedestre_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_a
	 ADD CONSTRAINT tra_travessia_pedestre_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_a
	 ADD CONSTRAINT tra_travessia_pedestre_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_a
	 ADD CONSTRAINT tra_travessia_pedestre_a_situacaoespacial_fk FOREIGN KEY (situacaoespacial)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_a ALTER COLUMN situacaoespacial SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_pedestre_a
	 ADD CONSTRAINT tra_travessia_pedestre_a_tipotravessiaped_fk FOREIGN KEY (tipotravessiaped)
	 REFERENCES dominios.tipo_travessia_ped (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_pedestre_a ALTER COLUMN tipotravessiaped SET DEFAULT 9999#

CREATE TABLE edgv.tra_travessia_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotravessia smallint NOT NULL,
	 tipouso smallint NOT NULL,
	 tipoembarcacao smallint NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_travessia_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_l_geom ON edgv.tra_travessia_l USING gist (geom)#

ALTER TABLE edgv.tra_travessia_l
	 ADD CONSTRAINT tra_travessia_l_tipotravessia_fk FOREIGN KEY (tipotravessia)
	 REFERENCES dominios.tipo_travessia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_l ALTER COLUMN tipotravessia SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_l
	 ADD CONSTRAINT tra_travessia_l_tipouso_fk FOREIGN KEY (tipouso)
	 REFERENCES dominios.tipo_transporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_l ALTER COLUMN tipouso SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_l
	 ADD CONSTRAINT tra_travessia_l_tipoembarcacao_fk FOREIGN KEY (tipoembarcacao)
	 REFERENCES dominios.tipo_embarcacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_l ALTER COLUMN tipoembarcacao SET DEFAULT 9999#

CREATE TABLE edgv.tra_travessia_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 tipotravessia smallint NOT NULL,
	 tipouso smallint NOT NULL,
	 tipoembarcacao smallint NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_travessia_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_travessia_p_geom ON edgv.tra_travessia_p USING gist (geom)#

ALTER TABLE edgv.tra_travessia_p
	 ADD CONSTRAINT tra_travessia_p_tipotravessia_fk FOREIGN KEY (tipotravessia)
	 REFERENCES dominios.tipo_travessia (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_p ALTER COLUMN tipotravessia SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_p
	 ADD CONSTRAINT tra_travessia_p_tipouso_fk FOREIGN KEY (tipouso)
	 REFERENCES dominios.tipo_transporte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_p ALTER COLUMN tipouso SET DEFAULT 9999#

ALTER TABLE edgv.tra_travessia_p
	 ADD CONSTRAINT tra_travessia_p_tipoembarcacao_fk FOREIGN KEY (tipoembarcacao)
	 REFERENCES dominios.tipo_embarcacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_travessia_p ALTER COLUMN tipoembarcacao SET DEFAULT 9999#

CREATE TABLE edgv.tra_caminho_carrocavel_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_caminho_carrocavel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_caminho_carrocavel_l_geom ON edgv.tra_caminho_carrocavel_l USING gist (geom)#

CREATE TABLE edgv.tra_tunel_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao boolean NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 altura real,
	 tipotunel smallint,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_tunel_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_tunel_l_geom ON edgv.tra_tunel_l USING gist (geom)#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_l ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_l ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_l
	 ADD CONSTRAINT tra_tunel_l_tipotunel_fk FOREIGN KEY (tipotunel)
	 REFERENCES dominios.tipo_tunel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_l ALTER COLUMN tipotunel SET DEFAULT 9999#

CREATE TABLE edgv.tra_tunel_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao boolean NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 altura real,
	 tipotunel smallint,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_tunel_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_tunel_p_geom ON edgv.tra_tunel_p USING gist (geom)#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_p ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_p ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_p
	 ADD CONSTRAINT tra_tunel_p_tipotunel_fk FOREIGN KEY (tipotunel)
	 REFERENCES dominios.tipo_tunel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_p ALTER COLUMN tipotunel SET DEFAULT 9999#

CREATE TABLE edgv.tra_tunel_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao boolean NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 altura real,
	 tipotunel smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_tunel_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_tunel_a_geom ON edgv.tra_tunel_a USING gist (geom)#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_a ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_tunel_a ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_tunel_a
	 ADD CONSTRAINT tra_tunel_a_tipotunel_fk FOREIGN KEY (tipotunel)
	 REFERENCES dominios.tipo_tunel (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_tunel_a ALTER COLUMN tipotunel SET DEFAULT 9999#

CREATE TABLE edgv.tra_passagem_elevada_viaduto_l(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipopassagviad smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 gabhorizsup real,
	 gabvertsup real,
	 cargasuportmaxima real,
	 geom geometry(MultiLinestring, [epsg]),
	 CONSTRAINT tra_passagem_elevada_viaduto_l_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passagem_elevada_viaduto_l_geom ON edgv.tra_passagem_elevada_viaduto_l USING gist (geom)#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 7 :: SMALLINT, 13 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_l_tipopassagviad_fk FOREIGN KEY (tipopassagviad)
	 REFERENCES dominios.tipo_passag_viad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_l ALTER COLUMN tipopassagviad SET DEFAULT 9999#

CREATE TABLE edgv.tra_passagem_elevada_viaduto_p(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipopassagviad smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 gabhorizsup real,
	 gabvertsup real,
	 cargasuportmaxima real,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT tra_passagem_elevada_viaduto_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passagem_elevada_viaduto_p_geom ON edgv.tra_passagem_elevada_viaduto_p USING gist (geom)#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 7 :: SMALLINT, 13 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_p_tipopassagviad_fk FOREIGN KEY (tipopassagviad)
	 REFERENCES dominios.tipo_passag_viad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_p ALTER COLUMN tipopassagviad SET DEFAULT 9999#

CREATE TABLE edgv.tra_passagem_elevada_viaduto_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint NOT NULL,
	 matconstr smallint NOT NULL,
	 operacional smallint NOT NULL,
	 situacaofisica smallint NOT NULL,
	 necessitamanutencao smallint NOT NULL,
	 nrpistas integer NOT NULL,
	 nrfaixas integer,
	 posicaopista smallint NOT NULL,
	 largura real,
	 extensao real,
	 tipopavimentacao smallint NOT NULL,
	 tipopassagviad smallint NOT NULL,
	 vaolivrehoriz real,
	 vaovertical real,
	 gabhorizsup real,
	 gabvertsup real,
	 cargasuportmaxima real,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_passagem_elevada_viaduto_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_passagem_elevada_viaduto_a_geom ON edgv.tra_passagem_elevada_viaduto_a USING gist (geom)#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_modaluso_check 
	 CHECK (modaluso = ANY(ARRAY[4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 9 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_matconstr_fk FOREIGN KEY (matconstr)
	 REFERENCES dominios.mat_constr (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN matconstr SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_necessitamanutencao_fk FOREIGN KEY (necessitamanutencao)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN necessitamanutencao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_posicaopista_fk FOREIGN KEY (posicaopista)
	 REFERENCES dominios.situacao_espacial (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_posicaopista_check 
	 CHECK (posicaopista = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 7 :: SMALLINT, 13 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN posicaopista SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_tipopavimentacao_fk FOREIGN KEY (tipopavimentacao)
	 REFERENCES dominios.tipo_pavimentacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN tipopavimentacao SET DEFAULT 9999#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a
	 ADD CONSTRAINT tra_passagem_elevada_viaduto_a_tipopassagviad_fk FOREIGN KEY (tipopassagviad)
	 REFERENCES dominios.tipo_passag_viad (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_passagem_elevada_viaduto_a ALTER COLUMN tipopassagviad SET DEFAULT 9999#

CREATE TABLE edgv.tra_patio_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 modaluso smallint,
	 administracao smallint,
	 operacional smallint NOT NULL,
	 situacaofisica smallint,
	 finalidadepatio smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT tra_patio_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX tra_patio_a_geom ON edgv.tra_patio_a USING gist (geom)#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_modaluso_fk FOREIGN KEY (modaluso)
	 REFERENCES dominios.modal_uso (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_patio_a ALTER COLUMN modaluso SET DEFAULT 9999#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_administracao_fk FOREIGN KEY (administracao)
	 REFERENCES dominios.administracao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_patio_a ALTER COLUMN administracao SET DEFAULT 9999#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_operacional_fk FOREIGN KEY (operacional)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_patio_a ALTER COLUMN operacional SET DEFAULT 9999#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_situacaofisica_fk FOREIGN KEY (situacaofisica)
	 REFERENCES dominios.situacao_fisica (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_patio_a ALTER COLUMN situacaofisica SET DEFAULT 9999#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_finalidadepatio_fk FOREIGN KEY (finalidadepatio)
	 REFERENCES dominios.finalidade_patio (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.tra_patio_a
	 ADD CONSTRAINT tra_patio_a_finalidadepatio_check 
	 CHECK (finalidadepatio = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 6 :: SMALLINT, 7 :: SMALLINT, 8 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.tra_patio_a ALTER COLUMN finalidadepatio SET DEFAULT 9999#

CREATE TABLE edgv.veg_floresta_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 especiepredominante smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_floresta_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_floresta_a_geom ON edgv.veg_floresta_a USING gist (geom)#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 4 :: SMALLINT, 5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.veg_floresta_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_floresta_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_floresta_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_floresta_a ALTER COLUMN secundaria SET DEFAULT 9999#

ALTER TABLE edgv.veg_floresta_a
	 ADD CONSTRAINT veg_floresta_a_especiepredominante_fk FOREIGN KEY (especiepredominante)
	 REFERENCES dominios.especie (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_floresta_a ALTER COLUMN especiepredominante SET DEFAULT 9999#

CREATE TABLE edgv.veg_campinarana_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_campinarana_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_campinarana_a_geom ON edgv.veg_campinarana_a USING gist (geom)#

ALTER TABLE edgv.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campinarana_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campinarana_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campinarana_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_campinarana_a
	 ADD CONSTRAINT veg_campinarana_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campinarana_a ALTER COLUMN secundaria SET DEFAULT 9999#

CREATE TABLE edgv.veg_veg_cultivada_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 tipolavoura smallint NOT NULL,
	 finalidade smallint,
	 terreno smallint,
	 cultivopredominante smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_cultivada_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_cultivada_a_geom ON edgv.veg_veg_cultivada_a USING gist (geom)#

ALTER TABLE edgv.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_cultivada_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_tipolavoura_fk FOREIGN KEY (tipolavoura)
	 REFERENCES dominios.tipo_lavoura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_cultivada_a ALTER COLUMN tipolavoura SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_cultura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_cultivada_a ALTER COLUMN finalidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_terreno_fk FOREIGN KEY (terreno)
	 REFERENCES dominios.condicao_terreno (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_cultivada_a ALTER COLUMN terreno SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_cultivada_a
	 ADD CONSTRAINT veg_veg_cultivada_a_cultivopredominante_fk FOREIGN KEY (cultivopredominante)
	 REFERENCES dominios.cultivo_predominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_cultivada_a ALTER COLUMN cultivopredominante SET DEFAULT 9999#

CREATE TABLE edgv.veg_veg_restinga_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_restinga_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_restinga_a_geom ON edgv.veg_veg_restinga_a USING gist (geom)#

ALTER TABLE edgv.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_restinga_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_restinga_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_restinga_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_restinga_a
	 ADD CONSTRAINT veg_veg_restinga_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_restinga_a ALTER COLUMN secundaria SET DEFAULT 9999#

CREATE TABLE edgv.veg_cerrado_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 vereda smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_cerrado_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_cerrado_a_geom ON edgv.veg_cerrado_a USING gist (geom)#

ALTER TABLE edgv.veg_cerrado_a
	 ADD CONSTRAINT veg_cerrado_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_cerrado_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_cerrado_a
	 ADD CONSTRAINT veg_cerrado_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_cerrado_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_cerrado_a
	 ADD CONSTRAINT veg_cerrado_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_cerrado_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_cerrado_a
	 ADD CONSTRAINT veg_cerrado_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_cerrado_a ALTER COLUMN secundaria SET DEFAULT 9999#

ALTER TABLE edgv.veg_cerrado_a
	 ADD CONSTRAINT veg_cerrado_a_vereda_fk FOREIGN KEY (vereda)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_cerrado_a ALTER COLUMN vereda SET DEFAULT 9999#

CREATE TABLE edgv.veg_brejo_pantano_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_brejo_pantano_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_brejo_pantano_a_geom ON edgv.veg_brejo_pantano_a USING gist (geom)#

ALTER TABLE edgv.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_brejo_pantano_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_brejo_pantano_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_brejo_pantano_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_brejo_pantano_a
	 ADD CONSTRAINT veg_brejo_pantano_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_brejo_pantano_a ALTER COLUMN secundaria SET DEFAULT 9999#

CREATE TABLE edgv.veg_mangue_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 tipomanguezal smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_mangue_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_mangue_a_geom ON edgv.veg_mangue_a USING gist (geom)#

ALTER TABLE edgv.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_mangue_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_mangue_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_mangue_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_mangue_a ALTER COLUMN secundaria SET DEFAULT 9999#

ALTER TABLE edgv.veg_mangue_a
	 ADD CONSTRAINT veg_mangue_a_tipomanguezal_fk FOREIGN KEY (tipomanguezal)
	 REFERENCES dominios.tipo_manguezal (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_mangue_a ALTER COLUMN tipomanguezal SET DEFAULT 9999#

CREATE TABLE edgv.veg_reflorestamento_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 tipolavoura smallint NOT NULL,
	 finalidade smallint,
	 terreno smallint,
	 cultivopredominante smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_reflorestamento_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_reflorestamento_a_geom ON edgv.veg_reflorestamento_a USING gist (geom)#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_reflorestamento_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_tipolavoura_fk FOREIGN KEY (tipolavoura)
	 REFERENCES dominios.tipo_lavoura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_tipolavoura_check 
	 CHECK (tipolavoura = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.veg_reflorestamento_a ALTER COLUMN tipolavoura SET DEFAULT 9999#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_cultura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_reflorestamento_a ALTER COLUMN finalidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_terreno_fk FOREIGN KEY (terreno)
	 REFERENCES dominios.condicao_terreno (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_reflorestamento_a ALTER COLUMN terreno SET DEFAULT 9999#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_cultivopredominante_fk FOREIGN KEY (cultivopredominante)
	 REFERENCES dominios.cultivo_predominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_reflorestamento_a
	 ADD CONSTRAINT veg_reflorestamento_a_cultivopredominante_check 
	 CHECK (cultivopredominante = ANY(ARRAY[20 :: SMALLINT, 21 :: SMALLINT, 23 :: SMALLINT, 96 :: SMALLINT, 98 :: SMALLINT, 99 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.veg_reflorestamento_a ALTER COLUMN cultivopredominante SET DEFAULT 9999#

CREATE TABLE edgv.veg_campo_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint NOT NULL,
	 secundaria smallint NOT NULL,
	 tipocampo smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_campo_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_campo_a_geom ON edgv.veg_campo_a USING gist (geom)#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_classificacaoporte_check 
	 CHECK (classificacaoporte = ANY(ARRAY[0 :: SMALLINT, 2 :: SMALLINT, 3 :: SMALLINT, 5 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.veg_campo_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campo_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_densidade_check 
	 CHECK (densidade = ANY(ARRAY[2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.veg_campo_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campo_a ALTER COLUMN secundaria SET DEFAULT 9999#

ALTER TABLE edgv.veg_campo_a
	 ADD CONSTRAINT veg_campo_a_tipocampo_fk FOREIGN KEY (tipocampo)
	 REFERENCES dominios.tipo_campo (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_campo_a ALTER COLUMN tipocampo SET DEFAULT 9999#

CREATE TABLE edgv.veg_caatinga_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_caatinga_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_caatinga_a_geom ON edgv.veg_caatinga_a USING gist (geom)#

ALTER TABLE edgv.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_caatinga_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_caatinga_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_caatinga_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_caatinga_a
	 ADD CONSTRAINT veg_caatinga_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_caatinga_a ALTER COLUMN secundaria SET DEFAULT 9999#

CREATE TABLE edgv.veg_veg_area_contato_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 antropizada smallint NOT NULL,
	 densidade smallint,
	 secundaria smallint NOT NULL,
	 tipoveg smallint,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT veg_veg_area_contato_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX veg_veg_area_contato_a_geom ON edgv.veg_veg_area_contato_a USING gist (geom)#

ALTER TABLE edgv.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_area_contato_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_antropizada_fk FOREIGN KEY (antropizada)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_area_contato_a ALTER COLUMN antropizada SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_densidade_fk FOREIGN KEY (densidade)
	 REFERENCES dominios.densidade (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_area_contato_a ALTER COLUMN densidade SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_secundaria_fk FOREIGN KEY (secundaria)
	 REFERENCES dominios.auxiliar (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_area_contato_a ALTER COLUMN secundaria SET DEFAULT 9999#

ALTER TABLE edgv.veg_veg_area_contato_a
	 ADD CONSTRAINT veg_veg_area_contato_a_tipoveg_fk FOREIGN KEY (tipoveg)
	 REFERENCES dominios.tipo_vegetacao (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.veg_veg_area_contato_a ALTER COLUMN tipoveg SET DEFAULT 9999#

CREATE TABLE edgv.ver_arvore_isolada_p(
	 id serial NOT NULL,
	 geometriaaproximada boolean NOT NULL,
	 geom geometry(MultiPoint, [epsg]),
	 CONSTRAINT ver_arvore_isolada_p_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX ver_arvore_isolada_p_geom ON edgv.ver_arvore_isolada_p USING gist (geom)#

CREATE TABLE edgv.ver_jardim_a(
	 id serial NOT NULL,
	 nome varchar(80),
	 geometriaaproximada boolean NOT NULL,
	 classificacaoporte smallint NOT NULL,
	 tipolavoura smallint NOT NULL,
	 finalidade smallint NOT NULL,
	 terreno smallint,
	 cultivopredominante smallint NOT NULL,
	 geom geometry(MultiPolygon, [epsg]),
	 CONSTRAINT ver_jardim_a_pk PRIMARY KEY (id)
	 WITH (FILLFACTOR = 80)
)#
CREATE INDEX ver_jardim_a_geom ON edgv.ver_jardim_a USING gist (geom)#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_classificacaoporte_fk FOREIGN KEY (classificacaoporte)
	 REFERENCES dominios.classificacao_porte (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.ver_jardim_a ALTER COLUMN classificacaoporte SET DEFAULT 9999#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_tipolavoura_fk FOREIGN KEY (tipolavoura)
	 REFERENCES dominios.tipo_lavoura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_tipolavoura_check 
	 CHECK (tipolavoura = ANY(ARRAY[0 :: SMALLINT, 1 :: SMALLINT, 2 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.ver_jardim_a ALTER COLUMN tipolavoura SET DEFAULT 9999#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_finalidade_fk FOREIGN KEY (finalidade)
	 REFERENCES dominios.finalidade_cultura (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_finalidade_check 
	 CHECK (finalidade = ANY(ARRAY[4 :: SMALLINT, 9999 :: SMALLINT]))# 
ALTER TABLE edgv.ver_jardim_a ALTER COLUMN finalidade SET DEFAULT 9999#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_terreno_fk FOREIGN KEY (terreno)
	 REFERENCES dominios.condicao_terreno (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.ver_jardim_a ALTER COLUMN terreno SET DEFAULT 9999#

ALTER TABLE edgv.ver_jardim_a
	 ADD CONSTRAINT ver_jardim_a_cultivopredominante_fk FOREIGN KEY (cultivopredominante)
	 REFERENCES dominios.cultivo_predominante (code) MATCH FULL
	 ON UPDATE NO ACTION ON DELETE NO ACTION#

ALTER TABLE edgv.ver_jardim_a ALTER COLUMN cultivopredominante SET DEFAULT 9999#
