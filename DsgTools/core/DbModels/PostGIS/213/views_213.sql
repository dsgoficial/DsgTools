DROP SCHEMA IF EXISTS views CASCADE#
CREATE SCHEMA views#
DROP VIEW IF EXISTS views.edu_descontinuidade_geometrica_l#
CREATE [VIEW] views.edu_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.edu_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edu_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.pto_pto_geod_topo_controle_p#
CREATE [VIEW] views.pto_pto_geod_topo_controle_p as 
	SELECT
	id as id,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	outrarefplan as outrarefplan,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom
    [FROM]
        cb.pto_pto_geod_topo_controle_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_geod_topo_controle_p.geometriaaproximada 
	left join dominios.tiporef as dominio_tiporef on dominio_tiporef.code = pto_pto_geod_topo_controle_p.tiporef 
	left join dominios.sistemageodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_geod_topo_controle_p.sistemageodesico 
	left join dominios.referencialaltim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_geod_topo_controle_p.referencialaltim
#
DROP VIEW IF EXISTS views.edu_edif_religiosa_a#
CREATE [VIEW] views.edu_edif_religiosa_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifrelig.code_name as tipoedifrelig,
	dominio_ensino.code_name as ensino,
	religiao as religiao,
	id_org_religiosa as id_org_religiosa
    [FROM]
        cb.edu_edif_religiosa_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_religiosa_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_religiosa_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_religiosa_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_religiosa_a.matconstr 
	left join dominios.tipoedifrelig as dominio_tipoedifrelig on dominio_tipoedifrelig.code = edu_edif_religiosa_a.tipoedifrelig 
	left join dominios.ensino as dominio_ensino on dominio_ensino.code = edu_edif_religiosa_a.ensino
#
DROP VIEW IF EXISTS views.lim_terra_publica_p#
CREATE [VIEW] views.lim_terra_publica_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	classificacao as classificacao
    [FROM]
        cb.lim_terra_publica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_terra_publica_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_area_saneamento_a#
CREATE [VIEW] views.asb_area_saneamento_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        cb.asb_area_saneamento_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_area_saneamento_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_edif_comerc_serv_p#
CREATE [VIEW] views.eco_edif_comerc_serv_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifcomercserv.code_name as tipoedifcomercserv,
	dominio_finalidade.code_name as finalidade,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        cb.eco_edif_comerc_serv_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_comerc_serv_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_comerc_serv_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_comerc_serv_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_comerc_serv_p.matconstr 
	left join dominios.tipoedifcomercserv as dominio_tipoedifcomercserv on dominio_tipoedifcomercserv.code = eco_edif_comerc_serv_p.tipoedifcomercserv 
	left join dominios.finalidade_eco as dominio_finalidade on dominio_finalidade.code = eco_edif_comerc_serv_p.finalidade
#
DROP VIEW IF EXISTS views.pto_edif_constr_est_med_fen_a#
CREATE [VIEW] views.pto_edif_constr_est_med_fen_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom
    [FROM]
        cb.pto_edif_constr_est_med_fen_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_edif_constr_est_med_fen_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = pto_edif_constr_est_med_fen_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = pto_edif_constr_est_med_fen_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = pto_edif_constr_est_med_fen_a.matconstr
#
DROP VIEW IF EXISTS views.tra_trecho_duto_l#
CREATE [VIEW] views.tra_trecho_duto_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	dominio_mattransp.code_name as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_matconstr.code_name as matconstr,
	ndutos as ndutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom
    [FROM]
        cb.tra_trecho_duto_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trecho_duto_l.geometriaaproximada 
	left join dominios.tipotrechoduto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = tra_trecho_duto_l.tipotrechoduto 
	left join dominios.mattransp as dominio_mattransp on dominio_mattransp.code = tra_trecho_duto_l.mattransp 
	left join dominios.setor as dominio_setor on dominio_setor.code = tra_trecho_duto_l.setor 
	left join dominios.posicaorelativa as dominio_posicaorelativa on dominio_posicaorelativa.code = tra_trecho_duto_l.posicaorelativa 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_trecho_duto_l.matconstr 
	left join dominios.situacaoespacial as dominio_situacaoespacial on dominio_situacaoespacial.code = tra_trecho_duto_l.situacaoespacial 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_trecho_duto_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_trecho_duto_l.situacaofisica
#
DROP VIEW IF EXISTS views.edu_descontinuidade_geometrica_a#
CREATE [VIEW] views.edu_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.edu_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edu_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.adm_area_pub_civil_a#
CREATE [VIEW] views.adm_area_pub_civil_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        cb.adm_area_pub_civil_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_area_pub_civil_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_pico_p#
CREATE [VIEW] views.rel_pico_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_pico_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_pico_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_pico_p.tipoelemnat
#
DROP VIEW IF EXISTS views.lim_terra_publica_a#
CREATE [VIEW] views.lim_terra_publica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	classificacao as classificacao
    [FROM]
        cb.lim_terra_publica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_terra_publica_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.pto_edif_constr_est_med_fen_p#
CREATE [VIEW] views.pto_edif_constr_est_med_fen_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom
    [FROM]
        cb.pto_edif_constr_est_med_fen_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_edif_constr_est_med_fen_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = pto_edif_constr_est_med_fen_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = pto_edif_constr_est_med_fen_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = pto_edif_constr_est_med_fen_p.matconstr
#
DROP VIEW IF EXISTS views.eco_edif_comerc_serv_a#
CREATE [VIEW] views.eco_edif_comerc_serv_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifcomercserv.code_name as tipoedifcomercserv,
	dominio_finalidade.code_name as finalidade,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        cb.eco_edif_comerc_serv_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_comerc_serv_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_comerc_serv_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_comerc_serv_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_comerc_serv_a.matconstr 
	left join dominios.tipoedifcomercserv as dominio_tipoedifcomercserv on dominio_tipoedifcomercserv.code = eco_edif_comerc_serv_a.tipoedifcomercserv 
	left join dominios.finalidade_eco as dominio_finalidade on dominio_finalidade.code = eco_edif_comerc_serv_a.finalidade
#
DROP VIEW IF EXISTS views.edu_descontinuidade_geometrica_p#
CREATE [VIEW] views.edu_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.edu_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edu_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_edif_ext_mineral_p#
CREATE [VIEW] views.eco_edif_ext_mineral_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        cb.eco_edif_ext_mineral_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_ext_mineral_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_ext_mineral_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_ext_mineral_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_ext_mineral_p.matconstr 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_edif_ext_mineral_p.tipodivisaocnae
#
DROP VIEW IF EXISTS views.loc_area_edificada_a#
CREATE [VIEW] views.loc_area_edificada_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.loc_area_edificada_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_area_edificada_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_eclusa_l#
CREATE [VIEW] views.tra_eclusa_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_eclusa_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_eclusa_l.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_eclusa_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_eclusa_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_eclusa_l.situacaofisica
#
DROP VIEW IF EXISTS views.adm_area_pub_militar_a#
CREATE [VIEW] views.adm_area_pub_militar_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        cb.adm_area_pub_militar_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_area_pub_militar_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_barragem_p#
CREATE [VIEW] views.hid_barragem_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.hid_barragem_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_p.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = hid_barragem_p.matconstr 
	left join dominios.usoprincipal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_p.usoprincipal 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_barragem_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_p.situacaofisica
#
DROP VIEW IF EXISTS views.lim_bairro_a#
CREATE [VIEW] views.lim_bairro_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	anodereferencia as anodereferencia
    [FROM]
        cb.lim_bairro_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_bairro_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_dep_saneamento_p#
CREATE [VIEW] views.asb_dep_saneamento_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodepsaneam.code_name as tipodepsaneam,
	dominio_construcao.code_name as construcao,
	dominio_matconstr.code_name as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_residuo.code_name as residuo,
	dominio_tiporesiduo.code_name as tiporesiduo,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        cb.asb_dep_saneamento_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_dep_saneamento_p.geometriaaproximada 
	left join dominios.tipodepsaneam as dominio_tipodepsaneam on dominio_tipodepsaneam.code = asb_dep_saneamento_p.tipodepsaneam 
	left join dominios.construcao as dominio_construcao on dominio_construcao.code = asb_dep_saneamento_p.construcao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_dep_saneamento_p.matconstr 
	left join dominios.finalidade_asb as dominio_finalidade on dominio_finalidade.code = asb_dep_saneamento_p.finalidade 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_dep_saneamento_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_dep_saneamento_p.situacaofisica 
	left join dominios.residuo as dominio_residuo on dominio_residuo.code = asb_dep_saneamento_p.residuo 
	left join dominios.tiporesiduo as dominio_tiporesiduo on dominio_tiporesiduo.code = asb_dep_saneamento_p.tiporesiduo
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_p#
CREATE [VIEW] views.eco_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.eco_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edu_campo_quadra_p#
CREATE [VIEW] views.edu_campo_quadra_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipocampoquadra.code_name as tipocampoquadra,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_campo_quadra_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_campo_quadra_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_campo_quadra_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_campo_quadra_p.situacaofisica 
	left join dominios.tipocampoquadra as dominio_tipocampoquadra on dominio_tipocampoquadra.code = edu_campo_quadra_p.tipocampoquadra
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_a#
CREATE [VIEW] views.rel_elemento_fisiog_natural_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_elemento_fisiog_natural_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_a.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_a.tipoelemnat
#
DROP VIEW IF EXISTS views.tra_atracadouro_a#
CREATE [VIEW] views.tra_atracadouro_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_atracadouro_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_atracadouro_a.geometriaaproximada 
	left join dominios.tipoatracad as dominio_tipoatracad on dominio_tipoatracad.code = tra_atracadouro_a.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_atracadouro_a.administracao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_atracadouro_a.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_atracadouro_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_atracadouro_a.situacaofisica
#
DROP VIEW IF EXISTS views.lim_descontinuidade_geometrica_a#
CREATE [VIEW] views.lim_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.lim_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = lim_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_edif_ext_mineral_a#
CREATE [VIEW] views.eco_edif_ext_mineral_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        cb.eco_edif_ext_mineral_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_ext_mineral_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_ext_mineral_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_ext_mineral_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_ext_mineral_a.matconstr 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_edif_ext_mineral_a.tipodivisaocnae
#
DROP VIEW IF EXISTS views.hid_ponto_inicio_drenagem_p#
CREATE [VIEW] views.hid_ponto_inicio_drenagem_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom,
	dominio_nascente.code_name as nascente
    [FROM]
        cb.hid_ponto_inicio_drenagem_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ponto_inicio_drenagem_p.geometriaaproximada 
	left join dominios.relacionado_hid as dominio_relacionado on dominio_relacionado.code = hid_ponto_inicio_drenagem_p.relacionado 
	left join dominios.nascente as dominio_nascente on dominio_nascente.code = hid_ponto_inicio_drenagem_p.nascente
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_l#
CREATE [VIEW] views.eco_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.eco_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_caminho_aereo_l#
CREATE [VIEW] views.tra_caminho_aereo_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocaminhoaereo.code_name as tipocaminhoaereo,
	dominio_tipousocaminhoaer.code_name as tipousocaminhoaer,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_org_ext_mineral as id_org_ext_mineral,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.tra_caminho_aereo_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_caminho_aereo_l.geometriaaproximada 
	left join dominios.tipocaminhoaereo as dominio_tipocaminhoaereo on dominio_tipocaminhoaereo.code = tra_caminho_aereo_l.tipocaminhoaereo 
	left join dominios.tipousocaminhoaer as dominio_tipousocaminhoaer on dominio_tipousocaminhoaer.code = tra_caminho_aereo_l.tipousocaminhoaer 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_caminho_aereo_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_caminho_aereo_l.situacaofisica
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_a#
CREATE [VIEW] views.eco_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.eco_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edu_campo_quadra_a#
CREATE [VIEW] views.edu_campo_quadra_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipocampoquadra.code_name as tipocampoquadra,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_campo_quadra_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_campo_quadra_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_campo_quadra_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_campo_quadra_a.situacaofisica 
	left join dominios.tipocampoquadra as dominio_tipocampoquadra on dominio_tipocampoquadra.code = edu_campo_quadra_a.tipocampoquadra
#
DROP VIEW IF EXISTS views.lim_distrito_a#
CREATE [VIEW] views.lim_distrito_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	geocodigo as geocodigo,
	anodereferencia as anodereferencia
    [FROM]
        cb.lim_distrito_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_distrito_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_passag_elevada_viaduto_p#
CREATE [VIEW] views.tra_passag_elevada_viaduto_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipopassagviad.code_name as tipopassagviad,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	gabhorizsup as gabhorizsup,
	gabvertsup as gabvertsup,
	cargasuportmaxima as cargasuportmaxima,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_posicaopista.code_name as posicaopista,
	extensao as extensao,
	largura as largura,
	geom as geom
    [FROM]
        cb.tra_passag_elevada_viaduto_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_passag_elevada_viaduto_p.geometriaaproximada 
	left join dominios.tipopassagviad as dominio_tipopassagviad on dominio_tipopassagviad.code = tra_passag_elevada_viaduto_p.tipopassagviad 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_passag_elevada_viaduto_p.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_passag_elevada_viaduto_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_passag_elevada_viaduto_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_passag_elevada_viaduto_p.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_passag_elevada_viaduto_p.posicaopista
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_p#
CREATE [VIEW] views.rel_elemento_fisiog_natural_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_elemento_fisiog_natural_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_p.tipoelemnat
#
DROP VIEW IF EXISTS views.tra_eclusa_p#
CREATE [VIEW] views.tra_eclusa_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_eclusa_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_eclusa_p.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_eclusa_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_eclusa_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_eclusa_p.situacaofisica
#
DROP VIEW IF EXISTS views.tra_atracadouro_p#
CREATE [VIEW] views.tra_atracadouro_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_atracadouro_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_atracadouro_p.geometriaaproximada 
	left join dominios.tipoatracad as dominio_tipoatracad on dominio_tipoatracad.code = tra_atracadouro_p.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_atracadouro_p.administracao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_atracadouro_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_atracadouro_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_atracadouro_p.situacaofisica
#
DROP VIEW IF EXISTS views.enc_torre_comunic_p#
CREATE [VIEW] views.enc_torre_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_posicaoreledific.code_name as posicaoreledific,
	dominio_ovgd.code_name as ovgd,
	alturaestimada as alturaestimada,
	id_complexo_comunicacao as id_complexo_comunicacao,
	geom as geom
    [FROM]
        cb.enc_torre_comunic_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_torre_comunic_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_torre_comunic_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_torre_comunic_p.situacaofisica 
	left join dominios.posicaoreledific as dominio_posicaoreledific on dominio_posicaoreledific.code = enc_torre_comunic_p.posicaoreledific 
	left join dominios.ovgd as dominio_ovgd on dominio_ovgd.code = enc_torre_comunic_p.ovgd
#
DROP VIEW IF EXISTS views.loc_hab_indigena_p#
CREATE [VIEW] views.loc_hab_indigena_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_coletiva.code_name as coletiva,
	dominio_isolada.code_name as isolada,
	id_aldeia_indigena as id_aldeia_indigena,
	geom as geom
    [FROM]
        cb.loc_hab_indigena_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_hab_indigena_p.geometriaaproximada 
	left join dominios.coletiva as dominio_coletiva on dominio_coletiva.code = loc_hab_indigena_p.coletiva 
	left join dominios.isolada as dominio_isolada on dominio_isolada.code = loc_hab_indigena_p.isolada
#
DROP VIEW IF EXISTS views.edu_edif_const_turistica_a#
CREATE [VIEW] views.edu_edif_const_turistica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifturist.code_name as tipoedifturist,
	dominio_ovgd.code_name as ovgd,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_edif_const_turistica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_const_turistica_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_const_turistica_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_const_turistica_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_const_turistica_a.matconstr 
	left join dominios.tipoedifturist as dominio_tipoedifturist on dominio_tipoedifturist.code = edu_edif_const_turistica_a.tipoedifturist 
	left join dominios.ovgd as dominio_ovgd on dominio_ovgd.code = edu_edif_const_turistica_a.ovgd
#
DROP VIEW IF EXISTS views.rel_terreno_exposto_a#
CREATE [VIEW] views.rel_terreno_exposto_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoterrexp.code_name as tipoterrexp,
	dominio_causaexposicao.code_name as causaexposicao,
	geom as geom
    [FROM]
        cb.rel_terreno_exposto_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_terreno_exposto_a.geometriaaproximada 
	left join dominios.tipoterrexp as dominio_tipoterrexp on dominio_tipoterrexp.code = rel_terreno_exposto_a.tipoterrexp 
	left join dominios.causaexposicao as dominio_causaexposicao on dominio_causaexposicao.code = rel_terreno_exposto_a.causaexposicao
#
DROP VIEW IF EXISTS views.adm_posto_pol_rod_p#
CREATE [VIEW] views.adm_posto_pol_rod_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipopostopol.code_name as tipopostopol,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_pub_militar as id_org_pub_militar,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        cb.adm_posto_pol_rod_p 
	left join dominios.tipopostopol as dominio_tipopostopol on dominio_tipopostopol.code = adm_posto_pol_rod_p.tipopostopol 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_posto_pol_rod_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_posto_pol_rod_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_posto_pol_rod_p.situacaofisica
#
DROP VIEW IF EXISTS views.enc_edif_comunic_p#
CREATE [VIEW] views.enc_edif_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_modalidade.code_name as modalidade,
	dominio_tipoedifcomunic.code_name as tipoedifcomunic,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        cb.enc_edif_comunic_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_edif_comunic_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_edif_comunic_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_edif_comunic_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = enc_edif_comunic_p.matconstr 
	left join dominios.modalidade as dominio_modalidade on dominio_modalidade.code = enc_edif_comunic_p.modalidade 
	left join dominios.tipoedifcomunic as dominio_tipoedifcomunic on dominio_tipoedifcomunic.code = enc_edif_comunic_p.tipoedifcomunic
#
DROP VIEW IF EXISTS views.tra_girador_ferroviario_p#
CREATE [VIEW] views.tra_girador_ferroviario_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        cb.tra_girador_ferroviario_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_girador_ferroviario_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_girador_ferroviario_p.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_girador_ferroviario_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_girador_ferroviario_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_sumidouro_vertedouro_p#
CREATE [VIEW] views.hid_sumidouro_vertedouro_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposumvert.code_name as tiposumvert,
	dominio_causa.code_name as causa,
	geom as geom
    [FROM]
        cb.hid_sumidouro_vertedouro_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_sumidouro_vertedouro_p.geometriaaproximada 
	left join dominios.tiposumvert as dominio_tiposumvert on dominio_tiposumvert.code = hid_sumidouro_vertedouro_p.tiposumvert 
	left join dominios.causa as dominio_causa on dominio_causa.code = hid_sumidouro_vertedouro_p.causa
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_p#
CREATE [VIEW] views.tra_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.tra_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = tra_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lim_limite_politico_adm_l#
CREATE [VIEW] views.lim_limite_politico_adm_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	dominio_tipolimpol.code_name as tipolimpol,
	obssituacao as obssituacao
    [FROM]
        cb.lim_limite_politico_adm_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_limite_politico_adm_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_limite_politico_adm_l.geometriaaproximada 
	left join dominios.tipolimpol as dominio_tipolimpol on dominio_tipolimpol.code = lim_limite_politico_adm_l.tipolimpol
#
DROP VIEW IF EXISTS views.tra_trilha_picada_l#
CREATE [VIEW] views.tra_trilha_picada_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.tra_trilha_picada_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trilha_picada_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_travessia_p#
CREATE [VIEW] views.tra_travessia_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessia.code_name as tipotravessia,
	geom as geom
    [FROM]
        cb.tra_travessia_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_p.geometriaaproximada 
	left join dominios.tipotravessia as dominio_tipotravessia on dominio_tipotravessia.code = tra_travessia_p.tipotravessia
#
DROP VIEW IF EXISTS views.lim_terra_indigena_p#
CREATE [VIEW] views.lim_terra_indigena_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	nometi as nometi,
	dominio_situacaojuridica.code_name as situacaojuridica,
	datasituacaojuridica as datasituacaojuridica,
	grupoetnico as grupoetnico,
	areaoficialha as areaoficialha,
	perimetrooficial as perimetrooficial,
	geom as geom
    [FROM]
        cb.lim_terra_indigena_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_terra_indigena_p.geometriaaproximada 
	left join dominios.situacaojuridica as dominio_situacaojuridica on dominio_situacaojuridica.code = lim_terra_indigena_p.situacaojuridica
#
DROP VIEW IF EXISTS views.edu_piscina_a#
CREATE [VIEW] views.edu_piscina_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_piscina_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_piscina_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_piscina_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_piscina_a.situacaofisica
#
DROP VIEW IF EXISTS views.loc_hab_indigena_a#
CREATE [VIEW] views.loc_hab_indigena_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_coletiva.code_name as coletiva,
	dominio_isolada.code_name as isolada,
	id_aldeia_indigena as id_aldeia_indigena,
	geom as geom
    [FROM]
        cb.loc_hab_indigena_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_hab_indigena_a.geometriaaproximada 
	left join dominios.coletiva as dominio_coletiva on dominio_coletiva.code = loc_hab_indigena_a.coletiva 
	left join dominios.isolada as dominio_isolada on dominio_isolada.code = loc_hab_indigena_a.isolada
#
DROP VIEW IF EXISTS views.pto_area_est_med_fenom_a#
CREATE [VIEW] views.pto_area_est_med_fenom_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_est_med_fenomenos as id_est_med_fenomenos,
	geom as geom
    [FROM]
        cb.pto_area_est_med_fenom_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_area_est_med_fenom_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_edif_const_turistica_p#
CREATE [VIEW] views.edu_edif_const_turistica_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifturist.code_name as tipoedifturist,
	dominio_ovgd.code_name as ovgd,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_edif_const_turistica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_const_turistica_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_const_turistica_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_const_turistica_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_const_turistica_p.matconstr 
	left join dominios.tipoedifturist as dominio_tipoedifturist on dominio_tipoedifturist.code = edu_edif_const_turistica_p.tipoedifturist 
	left join dominios.ovgd as dominio_ovgd on dominio_ovgd.code = edu_edif_const_turistica_p.ovgd
#
DROP VIEW IF EXISTS views.enc_edif_comunic_a#
CREATE [VIEW] views.enc_edif_comunic_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_modalidade.code_name as modalidade,
	dominio_tipoedifcomunic.code_name as tipoedifcomunic,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        cb.enc_edif_comunic_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_edif_comunic_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_edif_comunic_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_edif_comunic_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = enc_edif_comunic_a.matconstr 
	left join dominios.modalidade as dominio_modalidade on dominio_modalidade.code = enc_edif_comunic_a.modalidade 
	left join dominios.tipoedifcomunic as dominio_tipoedifcomunic on dominio_tipoedifcomunic.code = enc_edif_comunic_a.tipoedifcomunic
#
DROP VIEW IF EXISTS views.adm_posto_pol_rod_a#
CREATE [VIEW] views.adm_posto_pol_rod_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipopostopol.code_name as tipopostopol,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_pub_militar as id_org_pub_militar,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        cb.adm_posto_pol_rod_a 
	left join dominios.tipopostopol as dominio_tipopostopol on dominio_tipopostopol.code = adm_posto_pol_rod_a.tipopostopol 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_posto_pol_rod_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_posto_pol_rod_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_posto_pol_rod_a.situacaofisica
#
DROP VIEW IF EXISTS views.tra_ponto_duto_p#
CREATE [VIEW] views.tra_ponto_duto_p as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado
    [FROM]
        cb.tra_ponto_duto_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponto_duto_p.geometriaaproximada 
	left join dominios.relacionado_dut as dominio_relacionado on dominio_relacionado.code = tra_ponto_duto_p.relacionado
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_a#
CREATE [VIEW] views.tra_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.tra_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = tra_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_deposito_geral_a#
CREATE [VIEW] views.eco_deposito_geral_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	dominio_matconstr.code_name as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	dominio_tipoprodutoresiduo.code_name as tipoprodutoresiduo,
	dominio_tipoconteudo.code_name as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_tratamento.code_name as tratamento,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	id_estrut_transporte as id_estrut_transporte,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        cb.eco_deposito_geral_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_deposito_geral_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_deposito_geral_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_deposito_geral_a.situacaofisica 
	left join dominios.tipodepgeral as dominio_tipodepgeral on dominio_tipodepgeral.code = eco_deposito_geral_a.tipodepgeral 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_deposito_geral_a.matconstr 
	left join dominios.tipoexposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = eco_deposito_geral_a.tipoexposicao 
	left join dominios.tipoprodutoresiduo as dominio_tipoprodutoresiduo on dominio_tipoprodutoresiduo.code = eco_deposito_geral_a.tipoprodutoresiduo 
	left join dominios.tipoconteudo as dominio_tipoconteudo on dominio_tipoconteudo.code = eco_deposito_geral_a.tipoconteudo 
	left join dominios.unidadevolume as dominio_unidadevolume on dominio_unidadevolume.code = eco_deposito_geral_a.unidadevolume 
	left join dominios.tratamento as dominio_tratamento on dominio_tratamento.code = eco_deposito_geral_a.tratamento
#
DROP VIEW IF EXISTS views.lim_regiao_administrativa_a#
CREATE [VIEW] views.lim_regiao_administrativa_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	anodereferencia as anodereferencia
    [FROM]
        cb.lim_regiao_administrativa_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_regiao_administrativa_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_terra_indigena_a#
CREATE [VIEW] views.lim_terra_indigena_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	nometi as nometi,
	dominio_situacaojuridica.code_name as situacaojuridica,
	datasituacaojuridica as datasituacaojuridica,
	grupoetnico as grupoetnico,
	areaoficialha as areaoficialha,
	perimetrooficial as perimetrooficial,
	geom as geom
    [FROM]
        cb.lim_terra_indigena_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_terra_indigena_a.geometriaaproximada 
	left join dominios.situacaojuridica as dominio_situacaojuridica on dominio_situacaojuridica.code = lim_terra_indigena_a.situacaojuridica
#
DROP VIEW IF EXISTS views.tra_edif_rodoviaria_p#
CREATE [VIEW] views.tra_edif_rodoviaria_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifrod.code_name as tipoedifrod,
	dominio_administracao.code_name as administracao,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        cb.tra_edif_rodoviaria_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_rodoviaria_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_rodoviaria_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_rodoviaria_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_rodoviaria_p.matconstr 
	left join dominios.tipoedifrod as dominio_tipoedifrod on dominio_tipoedifrod.code = tra_edif_rodoviaria_p.tipoedifrod 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_rodoviaria_p.administracao
#
DROP VIEW IF EXISTS views.enc_descontinuidade_geometrica_p#
CREATE [VIEW] views.enc_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.enc_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = enc_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_banco_areia_a#
CREATE [VIEW] views.hid_banco_areia_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipobanco.code_name as tipobanco,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_materialpredominante.code_name as materialpredominante,
	geom as geom
    [FROM]
        cb.hid_banco_areia_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_banco_areia_a.geometriaaproximada 
	left join dominios.tipobanco as dominio_tipobanco on dominio_tipobanco.code = hid_banco_areia_a.tipobanco 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_banco_areia_a.situacaoemagua 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_banco_areia_a.materialpredominante
#
DROP VIEW IF EXISTS views.asb_area_abast_agua_a#
CREATE [VIEW] views.asb_area_abast_agua_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        cb.asb_area_abast_agua_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_area_abast_agua_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_condutor_hidrico_l#
CREATE [VIEW] views.tra_condutor_hidrico_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	dominio_mattransp.code_name as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_matconstr.code_name as matconstr,
	ndutos as ndutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom,
	dominio_tipocondutor.code_name as tipocondutor,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr
    [FROM]
        cb.tra_condutor_hidrico_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_condutor_hidrico_l.geometriaaproximada 
	left join dominios.tipotrechoduto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = tra_condutor_hidrico_l.tipotrechoduto 
	left join dominios.mattransp as dominio_mattransp on dominio_mattransp.code = tra_condutor_hidrico_l.mattransp 
	left join dominios.setor as dominio_setor on dominio_setor.code = tra_condutor_hidrico_l.setor 
	left join dominios.posicaorelativa as dominio_posicaorelativa on dominio_posicaorelativa.code = tra_condutor_hidrico_l.posicaorelativa 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_condutor_hidrico_l.matconstr 
	left join dominios.situacaoespacial as dominio_situacaoespacial on dominio_situacaoespacial.code = tra_condutor_hidrico_l.situacaoespacial 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_condutor_hidrico_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_condutor_hidrico_l.situacaofisica 
	left join dominios.tipocondutor as dominio_tipocondutor on dominio_tipocondutor.code = tra_condutor_hidrico_l.tipocondutor
#
DROP VIEW IF EXISTS views.asb_cemiterio_p#
CREATE [VIEW] views.asb_cemiterio_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocemiterio.code_name as tipocemiterio,
	dominio_denominacaoassociada.code_name as denominacaoassociada,
	geom as geom
    [FROM]
        cb.asb_cemiterio_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_cemiterio_p.geometriaaproximada 
	left join dominios.tipocemiterio as dominio_tipocemiterio on dominio_tipocemiterio.code = asb_cemiterio_p.tipocemiterio 
	left join dominios.denominacaoassociada as dominio_denominacaoassociada on dominio_denominacaoassociada.code = asb_cemiterio_p.denominacaoassociada
#
DROP VIEW IF EXISTS views.lim_outras_unid_protegidas_a#
CREATE [VIEW] views.lim_outras_unid_protegidas_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_tipooutunidprot.code_name as tipooutunidprot,
	anocriacao as anocriacao,
	historicomodificacao as historicomodificacao,
	sigla as sigla,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao
    [FROM]
        cb.lim_outras_unid_protegidas_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_outras_unid_protegidas_a.geometriaaproximada 
	left join dominios.tipooutunidprot as dominio_tipooutunidprot on dominio_tipooutunidprot.code = lim_outras_unid_protegidas_a.tipooutunidprot 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_outras_unid_protegidas_a.administracao
#
DROP VIEW IF EXISTS views.tra_ponto_hidroviario_p#
CREATE [VIEW] views.tra_ponto_hidroviario_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        cb.tra_ponto_hidroviario_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponto_hidroviario_p.geometriaaproximada 
	left join dominios.relacionado_hdr as dominio_relacionado on dominio_relacionado.code = tra_ponto_hidroviario_p.relacionado
#
DROP VIEW IF EXISTS views.loc_descontinuidade_geometrica_l#
CREATE [VIEW] views.loc_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.loc_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = loc_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.loc_descontinuidade_geometrica_a#
CREATE [VIEW] views.loc_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.loc_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = loc_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.sau_descontinuidade_geometrica_p#
CREATE [VIEW] views.sau_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.sau_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = sau_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edu_coreto_tribuna_p#
CREATE [VIEW] views.edu_coreto_tribuna_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_coreto_tribuna_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_coreto_tribuna_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_coreto_tribuna_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_coreto_tribuna_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_banco_areia_l#
CREATE [VIEW] views.hid_banco_areia_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipobanco.code_name as tipobanco,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_materialpredominante.code_name as materialpredominante,
	geom as geom
    [FROM]
        cb.hid_banco_areia_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_banco_areia_l.geometriaaproximada 
	left join dominios.tipobanco as dominio_tipobanco on dominio_tipobanco.code = hid_banco_areia_l.tipobanco 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_banco_areia_l.situacaoemagua 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_banco_areia_l.materialpredominante
#
DROP VIEW IF EXISTS views.hid_foz_maritima_p#
CREATE [VIEW] views.hid_foz_maritima_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_foz_maritima_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_edif_rodoviaria_a#
CREATE [VIEW] views.tra_edif_rodoviaria_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifrod.code_name as tipoedifrod,
	dominio_administracao.code_name as administracao,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        cb.tra_edif_rodoviaria_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_rodoviaria_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_rodoviaria_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_rodoviaria_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_rodoviaria_a.matconstr 
	left join dominios.tipoedifrod as dominio_tipoedifrod on dominio_tipoedifrod.code = tra_edif_rodoviaria_a.tipoedifrod 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_rodoviaria_a.administracao
#
DROP VIEW IF EXISTS views.hid_terreno_suj_inundacao_a#
CREATE [VIEW] views.hid_terreno_suj_inundacao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	periodicidadeinunda as periodicidadeinunda,
	geom as geom
    [FROM]
        cb.hid_terreno_suj_inundacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_terreno_suj_inundacao_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_foz_maritima_l#
CREATE [VIEW] views.hid_foz_maritima_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_foz_maritima_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.veg_veg_restinga_a#
CREATE [VIEW] views.veg_veg_restinga_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_veg_restinga_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_restinga_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_veg_restinga_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_veg_restinga_a.antropizada 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_restinga_a.classificacaoporte
#
DROP VIEW IF EXISTS views.lim_outras_unid_protegidas_p#
CREATE [VIEW] views.lim_outras_unid_protegidas_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_tipooutunidprot.code_name as tipooutunidprot,
	anocriacao as anocriacao,
	historicomodificacao as historicomodificacao,
	sigla as sigla,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao
    [FROM]
        cb.lim_outras_unid_protegidas_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_outras_unid_protegidas_p.geometriaaproximada 
	left join dominios.tipooutunidprot as dominio_tipooutunidprot on dominio_tipooutunidprot.code = lim_outras_unid_protegidas_p.tipooutunidprot 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_outras_unid_protegidas_p.administracao
#
DROP VIEW IF EXISTS views.asb_cemiterio_a#
CREATE [VIEW] views.asb_cemiterio_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocemiterio.code_name as tipocemiterio,
	dominio_denominacaoassociada.code_name as denominacaoassociada,
	geom as geom
    [FROM]
        cb.asb_cemiterio_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_cemiterio_a.geometriaaproximada 
	left join dominios.tipocemiterio as dominio_tipocemiterio on dominio_tipocemiterio.code = asb_cemiterio_a.tipocemiterio 
	left join dominios.denominacaoassociada as dominio_denominacaoassociada on dominio_denominacaoassociada.code = asb_cemiterio_a.denominacaoassociada
#
DROP VIEW IF EXISTS views.enc_edif_energia_p#
CREATE [VIEW] views.enc_edif_energia_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifenergia.code_name as tipoedifenergia,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	id_subestacao_ener_eletr as id_subestacao_ener_eletr
    [FROM]
        cb.enc_edif_energia_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_edif_energia_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_edif_energia_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_edif_energia_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = enc_edif_energia_p.matconstr 
	left join dominios.tipoedifenergia as dominio_tipoedifenergia on dominio_tipoedifenergia.code = enc_edif_energia_p.tipoedifenergia
#
DROP VIEW IF EXISTS views.tra_posto_combustivel_p#
CREATE [VIEW] views.tra_posto_combustivel_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	id_estrut_transporte as id_estrut_transporte,
	geom as geom
    [FROM]
        cb.tra_posto_combustivel_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_posto_combustivel_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_posto_combustivel_p.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_posto_combustivel_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_posto_combustivel_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_posto_combustivel_p.matconstr
#
DROP VIEW IF EXISTS views.pto_pto_est_med_fenomenos_p#
CREATE [VIEW] views.pto_pto_est_med_fenomenos_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoptoestmed.code_name as tipoptoestmed,
	codestacao as codestacao,
	orgaoenteresp as orgaoenteresp,
	id_est_med_fenomenos as id_est_med_fenomenos,
	geom as geom
    [FROM]
        cb.pto_pto_est_med_fenomenos_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_est_med_fenomenos_p.geometriaaproximada 
	left join dominios.tipoptoestmed as dominio_tipoptoestmed on dominio_tipoptoestmed.code = pto_pto_est_med_fenomenos_p.tipoptoestmed
#
DROP VIEW IF EXISTS views.hid_comporta_p#
CREATE [VIEW] views.hid_comporta_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.hid_comporta_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_comporta_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_comporta_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_comporta_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_corredeira_p#
CREATE [VIEW] views.hid_corredeira_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_corredeira_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_faixa_seguranca_a#
CREATE [VIEW] views.tra_faixa_seguranca_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_faixa_seguranca_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_faixa_seguranca_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_edif_ensino_a#
CREATE [VIEW] views.edu_edif_ensino_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_ensino as id_org_ensino
    [FROM]
        cb.edu_edif_ensino_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_ensino_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_ensino_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_ensino_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_ensino_a.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_edif_ensino_a.tipoclassecnae
#
DROP VIEW IF EXISTS views.veg_descontinuidade_geometrica_p#
CREATE [VIEW] views.veg_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.veg_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = veg_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lim_area_uso_comunitario_p#
CREATE [VIEW] views.lim_area_uso_comunitario_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_tipoareausocomun.code_name as tipoareausocomun
    [FROM]
        cb.lim_area_uso_comunitario_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_uso_comunitario_p.geometriaaproximada 
	left join dominios.tipoareausocomun as dominio_tipoareausocomun on dominio_tipoareausocomun.code = lim_area_uso_comunitario_p.tipoareausocomun
#
DROP VIEW IF EXISTS views.tra_ciclovia_l#
CREATE [VIEW] views.tra_ciclovia_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_administracao.code_name as administracao,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_trafego.code_name as trafego,
	geom as geom
    [FROM]
        cb.tra_ciclovia_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ciclovia_l.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_ciclovia_l.administracao 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_ciclovia_l.revestimento 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_ciclovia_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_ciclovia_l.situacaofisica 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = tra_ciclovia_l.trafego
#
DROP VIEW IF EXISTS views.enc_hidreletrica_p#
CREATE [VIEW] views.enc_hidreletrica_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom,
	codigohidreletrica as codigohidreletrica
    [FROM]
        cb.enc_hidreletrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_p.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_p.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_hidreletrica_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_p.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_hidreletrica_p.destenergelet
#
DROP VIEW IF EXISTS views.hid_corredeira_a#
CREATE [VIEW] views.hid_corredeira_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_corredeira_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_coreto_tribuna_a#
CREATE [VIEW] views.edu_coreto_tribuna_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_coreto_tribuna_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_coreto_tribuna_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_coreto_tribuna_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_coreto_tribuna_a.situacaofisica
#
DROP VIEW IF EXISTS views.edu_edif_ensino_p#
CREATE [VIEW] views.edu_edif_ensino_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_ensino as id_org_ensino
    [FROM]
        cb.edu_edif_ensino_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_ensino_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_ensino_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_ensino_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_ensino_p.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_edif_ensino_p.tipoclassecnae
#
DROP VIEW IF EXISTS views.tra_posto_combustivel_a#
CREATE [VIEW] views.tra_posto_combustivel_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	id_estrut_transporte as id_estrut_transporte,
	geom as geom
    [FROM]
        cb.tra_posto_combustivel_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_posto_combustivel_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_posto_combustivel_a.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_posto_combustivel_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_posto_combustivel_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_posto_combustivel_a.matconstr
#
DROP VIEW IF EXISTS views.enc_ponto_trecho_energia_p#
CREATE [VIEW] views.enc_ponto_trecho_energia_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoptoenergia.code_name as tipoptoenergia,
	geom as geom
    [FROM]
        cb.enc_ponto_trecho_energia_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_ponto_trecho_energia_p.geometriaaproximada 
	left join dominios.tipoptoenergia as dominio_tipoptoenergia on dominio_tipoptoenergia.code = enc_ponto_trecho_energia_p.tipoptoenergia
#
DROP VIEW IF EXISTS views.hid_descontinuidade_geometrica_l#
CREATE [VIEW] views.hid_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.hid_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hid_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_trecho_massa_dagua_a#
CREATE [VIEW] views.hid_trecho_massa_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipotrechomassa.code_name as tipotrechomassa,
	dominio_regime.code_name as regime,
	dominio_salinidade.code_name as salinidade,
	id_trecho_curso_dagua as id_trecho_curso_dagua,
	geom as geom
    [FROM]
        cb.hid_trecho_massa_dagua_a 
	left join dominios.tipotrechomassa as dominio_tipotrechomassa on dominio_tipotrechomassa.code = hid_trecho_massa_dagua_a.tipotrechomassa 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_trecho_massa_dagua_a.regime 
	left join dominios.salinidade as dominio_salinidade on dominio_salinidade.code = hid_trecho_massa_dagua_a.salinidade
#
DROP VIEW IF EXISTS views.veg_descontinuidade_geometrica_l#
CREATE [VIEW] views.veg_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.veg_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = veg_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.enc_edif_energia_a#
CREATE [VIEW] views.enc_edif_energia_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifenergia.code_name as tipoedifenergia,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	id_subestacao_ener_eletr as id_subestacao_ener_eletr
    [FROM]
        cb.enc_edif_energia_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_edif_energia_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_edif_energia_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_edif_energia_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = enc_edif_energia_a.matconstr 
	left join dominios.tipoedifenergia as dominio_tipoedifenergia on dominio_tipoedifenergia.code = enc_edif_energia_a.tipoedifenergia
#
DROP VIEW IF EXISTS views.hid_comporta_l#
CREATE [VIEW] views.hid_comporta_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.hid_comporta_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_comporta_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_comporta_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_comporta_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_corredeira_l#
CREATE [VIEW] views.hid_corredeira_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_corredeira_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.adm_descontinuidade_geometrica_p#
CREATE [VIEW] views.adm_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.adm_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = adm_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lim_area_desenv_controle_a#
CREATE [VIEW] views.lim_area_desenv_controle_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	classificacao as classificacao
    [FROM]
        cb.lim_area_desenv_controle_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_desenv_controle_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_sinalizacao_p#
CREATE [VIEW] views.tra_sinalizacao_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposinal.code_name as tiposinal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_sinalizacao_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_sinalizacao_p.geometriaaproximada 
	left join dominios.tiposinal as dominio_tiposinal on dominio_tiposinal.code = tra_sinalizacao_p.tiposinal 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_sinalizacao_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_sinalizacao_p.situacaofisica
#
DROP VIEW IF EXISTS views.lim_limite_intra_munic_adm_l#
CREATE [VIEW] views.lim_limite_intra_munic_adm_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	dominio_tipolimintramun.code_name as tipolimintramun,
	obssituacao as obssituacao
    [FROM]
        cb.lim_limite_intra_munic_adm_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_limite_intra_munic_adm_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_limite_intra_munic_adm_l.geometriaaproximada 
	left join dominios.tipolimintramun as dominio_tipolimintramun on dominio_tipolimintramun.code = lim_limite_intra_munic_adm_l.tipolimintramun
#
DROP VIEW IF EXISTS views.edu_area_ensino_a#
CREATE [VIEW] views.edu_area_ensino_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_ensino as id_org_ensino
    [FROM]
        cb.edu_area_ensino_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_area_ensino_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.adm_posto_fiscal_a#
CREATE [VIEW] views.adm_posto_fiscal_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopostofisc.code_name as tipopostofisc,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        cb.adm_posto_fiscal_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_posto_fiscal_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_posto_fiscal_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_posto_fiscal_a.situacaofisica 
	left join dominios.tipopostofisc as dominio_tipopostofisc on dominio_tipopostofisc.code = adm_posto_fiscal_a.tipopostofisc
#
DROP VIEW IF EXISTS views.rel_dolina_p#
CREATE [VIEW] views.rel_dolina_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_dolina_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_dolina_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_dolina_p.tipoelemnat
#
DROP VIEW IF EXISTS views.tra_travessia_pedestre_l#
CREATE [VIEW] views.tra_travessia_pedestre_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessiaped.code_name as tipotravessiaped,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_travessia_pedestre_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_pedestre_l.geometriaaproximada 
	left join dominios.tipotravessiaped as dominio_tipotravessiaped on dominio_tipotravessiaped.code = tra_travessia_pedestre_l.tipotravessiaped 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_travessia_pedestre_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_travessia_pedestre_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_travessia_pedestre_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_trecho_drenagem_l#
CREATE [VIEW] views.hid_trecho_drenagem_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_dentrodepoligono.code_name as dentrodepoligono,
	dominio_compartilhado.code_name as compartilhado,
	dominio_eixoprincipal.code_name as eixoprincipal,
	dominio_navegabilidade.code_name as navegabilidade,
	caladomax as caladomax,
	dominio_regime.code_name as regime,
	larguramedia as larguramedia,
	velocidademedcorrente as velocidademedcorrente,
	profundidademedia as profundidademedia,
	id_trecho_curso_dagua as id_trecho_curso_dagua,
	geom as geom
    [FROM]
        cb.hid_trecho_drenagem_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_trecho_drenagem_l.geometriaaproximada 
	left join dominios.coincidecomdentrode_hid as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = hid_trecho_drenagem_l.coincidecomdentrode 
	left join dominios.dentrodepoligono as dominio_dentrodepoligono on dominio_dentrodepoligono.code = hid_trecho_drenagem_l.dentrodepoligono 
	left join dominios.compartilhado as dominio_compartilhado on dominio_compartilhado.code = hid_trecho_drenagem_l.compartilhado 
	left join dominios.eixoprincipal as dominio_eixoprincipal on dominio_eixoprincipal.code = hid_trecho_drenagem_l.eixoprincipal 
	left join dominios.navegabilidade as dominio_navegabilidade on dominio_navegabilidade.code = hid_trecho_drenagem_l.navegabilidade 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_trecho_drenagem_l.regime
#
DROP VIEW IF EXISTS views.lim_unidade_conserv_nao_snuc_a#
CREATE [VIEW] views.lim_unidade_conserv_nao_snuc_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	atolegal as atolegal,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	anocriacao as anocriacao,
	sigla as sigla,
	areaoficial as areaoficial
    [FROM]
        cb.lim_unidade_conserv_nao_snuc_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_conserv_nao_snuc_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_conserv_nao_snuc_a.administracao
#
DROP VIEW IF EXISTS views.lim_area_especial_a#
CREATE [VIEW] views.lim_area_especial_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.lim_area_especial_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_especial_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.adm_descontinuidade_geometrica_a#
CREATE [VIEW] views.adm_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.adm_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = adm_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.loc_edif_habitacional_a#
CREATE [VIEW] views.loc_edif_habitacional_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	id_complexo_habitacional as id_complexo_habitacional
    [FROM]
        cb.loc_edif_habitacional_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_edif_habitacional_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = loc_edif_habitacional_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = loc_edif_habitacional_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = loc_edif_habitacional_a.matconstr
#
DROP VIEW IF EXISTS views.loc_aglom_rural_de_ext_urbana_p#
CREATE [VIEW] views.loc_aglom_rural_de_ext_urbana_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom
    [FROM]
        cb.loc_aglom_rural_de_ext_urbana_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_aglom_rural_de_ext_urbana_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.adm_posto_fiscal_p#
CREATE [VIEW] views.adm_posto_fiscal_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopostofisc.code_name as tipopostofisc,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        cb.adm_posto_fiscal_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_posto_fiscal_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_posto_fiscal_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_posto_fiscal_p.situacaofisica 
	left join dominios.tipopostofisc as dominio_tipopostofisc on dominio_tipopostofisc.code = adm_posto_fiscal_p.tipopostofisc
#
DROP VIEW IF EXISTS views.tra_passagem_nivel_p#
CREATE [VIEW] views.tra_passagem_nivel_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.tra_passagem_nivel_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_passagem_nivel_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_edif_constr_portuaria_p#
CREATE [VIEW] views.tra_edif_constr_portuaria_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifport.code_name as tipoedifport,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario
    [FROM]
        cb.tra_edif_constr_portuaria_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_constr_portuaria_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_constr_portuaria_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_constr_portuaria_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_constr_portuaria_p.matconstr 
	left join dominios.tipoedifport as dominio_tipoedifport on dominio_tipoedifport.code = tra_edif_constr_portuaria_p.tipoedifport 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_constr_portuaria_p.administracao
#
DROP VIEW IF EXISTS views.edu_edif_religiosa_p#
CREATE [VIEW] views.edu_edif_religiosa_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifrelig.code_name as tipoedifrelig,
	dominio_ensino.code_name as ensino,
	religiao as religiao,
	id_org_religiosa as id_org_religiosa
    [FROM]
        cb.edu_edif_religiosa_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_religiosa_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_religiosa_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_religiosa_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_religiosa_p.matconstr 
	left join dominios.tipoedifrelig as dominio_tipoedifrelig on dominio_tipoedifrelig.code = edu_edif_religiosa_p.tipoedifrelig 
	left join dominios.ensino as dominio_ensino on dominio_ensino.code = edu_edif_religiosa_p.ensino
#
DROP VIEW IF EXISTS views.hid_massa_dagua_a#
CREATE [VIEW] views.hid_massa_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipomassadagua.code_name as tipomassadagua,
	dominio_regime.code_name as regime,
	dominio_salinidade.code_name as salinidade,
	geom as geom
    [FROM]
        cb.hid_massa_dagua_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_massa_dagua_a.geometriaaproximada 
	left join dominios.tipomassadagua as dominio_tipomassadagua on dominio_tipomassadagua.code = hid_massa_dagua_a.tipomassadagua 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_massa_dagua_a.regime 
	left join dominios.salinidade as dominio_salinidade on dominio_salinidade.code = hid_massa_dagua_a.salinidade
#
DROP VIEW IF EXISTS views.lim_unidade_conserv_nao_snuc_p#
CREATE [VIEW] views.lim_unidade_conserv_nao_snuc_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	atolegal as atolegal,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	anocriacao as anocriacao,
	sigla as sigla,
	areaoficial as areaoficial
    [FROM]
        cb.lim_unidade_conserv_nao_snuc_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_conserv_nao_snuc_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_conserv_nao_snuc_p.administracao
#
DROP VIEW IF EXISTS views.enc_trecho_comunic_l#
CREATE [VIEW] views.enc_trecho_comunic_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechocomunic.code_name as tipotrechocomunic,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_emduto.code_name as emduto,
	id_org_comerc_serv as id_org_comerc_serv,
	geom as geom
    [FROM]
        cb.enc_trecho_comunic_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_trecho_comunic_l.geometriaaproximada 
	left join dominios.tipotrechocomunic as dominio_tipotrechocomunic on dominio_tipotrechocomunic.code = enc_trecho_comunic_l.tipotrechocomunic 
	left join dominios.posicaorelativa as dominio_posicaorelativa on dominio_posicaorelativa.code = enc_trecho_comunic_l.posicaorelativa 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = enc_trecho_comunic_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_trecho_comunic_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_trecho_comunic_l.situacaofisica 
	left join dominios.emduto as dominio_emduto on dominio_emduto.code = enc_trecho_comunic_l.emduto
#
DROP VIEW IF EXISTS views.lim_unidade_uso_sustentavel_a#
CREATE [VIEW] views.lim_unidade_uso_sustentavel_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	anocriacao as anocriacao,
	sigla as sigla,
	areaoficialha as areaoficialha,
	atolegal as atolegal,
	dominio_administracao.code_name as administracao,
	dominio_tipounidusosust.code_name as tipounidusosust
    [FROM]
        cb.lim_unidade_uso_sustentavel_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_uso_sustentavel_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_uso_sustentavel_a.administracao 
	left join dominios.tipounidusosust as dominio_tipounidusosust on dominio_tipounidusosust.code = lim_unidade_uso_sustentavel_a.tipounidusosust
#
DROP VIEW IF EXISTS views.tra_travessia_l#
CREATE [VIEW] views.tra_travessia_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessia.code_name as tipotravessia,
	geom as geom
    [FROM]
        cb.tra_travessia_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_l.geometriaaproximada 
	left join dominios.tipotravessia as dominio_tipotravessia on dominio_tipotravessia.code = tra_travessia_l.tipotravessia
#
DROP VIEW IF EXISTS views.loc_descontinuidade_geometrica_p#
CREATE [VIEW] views.loc_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.loc_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = loc_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_l#
CREATE [VIEW] views.rel_elemento_fisiog_natural_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_elemento_fisiog_natural_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_l.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_l.tipoelemnat
#
DROP VIEW IF EXISTS views.eco_ext_mineral_a#
CREATE [VIEW] views.eco_ext_mineral_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposecaocnae.code_name as tiposecaocnae,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoextmin.code_name as tipoextmin,
	dominio_tipoprodutoresiduo.code_name as tipoprodutoresiduo,
	dominio_tipopocomina.code_name as tipopocomina,
	dominio_procextracao.code_name as procextracao,
	dominio_formaextracao.code_name as formaextracao,
	dominio_atividade.code_name as atividade,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        cb.eco_ext_mineral_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_ext_mineral_a.geometriaaproximada 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_ext_mineral_a.tiposecaocnae 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_ext_mineral_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_ext_mineral_a.situacaofisica 
	left join dominios.tipoextmin as dominio_tipoextmin on dominio_tipoextmin.code = eco_ext_mineral_a.tipoextmin 
	left join dominios.tipoprodutoresiduo as dominio_tipoprodutoresiduo on dominio_tipoprodutoresiduo.code = eco_ext_mineral_a.tipoprodutoresiduo 
	left join dominios.tipopocomina as dominio_tipopocomina on dominio_tipopocomina.code = eco_ext_mineral_a.tipopocomina 
	left join dominios.procextracao as dominio_procextracao on dominio_procextracao.code = eco_ext_mineral_a.procextracao 
	left join dominios.formaextracao as dominio_formaextracao on dominio_formaextracao.code = eco_ext_mineral_a.formaextracao 
	left join dominios.atividade as dominio_atividade on dominio_atividade.code = eco_ext_mineral_a.atividade
#
DROP VIEW IF EXISTS views.sau_edif_servico_social_p#
CREATE [VIEW] views.sau_edif_servico_social_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_servico_social as id_org_servico_social
    [FROM]
        cb.sau_edif_servico_social_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_edif_servico_social_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = sau_edif_servico_social_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = sau_edif_servico_social_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = sau_edif_servico_social_p.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_edif_servico_social_p.tipoclassecnae
#
DROP VIEW IF EXISTS views.enc_zona_linhas_energia_com_a#
CREATE [VIEW] views.enc_zona_linhas_energia_com_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.enc_zona_linhas_energia_com_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_zona_linhas_energia_com_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_ponto_rodoviario_p#
CREATE [VIEW] views.tra_ponto_rodoviario_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        cb.tra_ponto_rodoviario_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponto_rodoviario_p.geometriaaproximada 
	left join dominios.relacionado_rod as dominio_relacionado on dominio_relacionado.code = tra_ponto_rodoviario_p.relacionado
#
DROP VIEW IF EXISTS views.lim_unidade_uso_sustentavel_p#
CREATE [VIEW] views.lim_unidade_uso_sustentavel_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	anocriacao as anocriacao,
	sigla as sigla,
	areaoficialha as areaoficialha,
	atolegal as atolegal,
	dominio_administracao.code_name as administracao,
	dominio_tipounidusosust.code_name as tipounidusosust
    [FROM]
        cb.lim_unidade_uso_sustentavel_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_uso_sustentavel_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_uso_sustentavel_p.administracao 
	left join dominios.tipounidusosust as dominio_tipounidusosust on dominio_tipounidusosust.code = lim_unidade_uso_sustentavel_p.tipounidusosust
#
DROP VIEW IF EXISTS views.aux_descontinuidade_geometrica_l#
CREATE [VIEW] views.aux_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.aux_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aux_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aux_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_atracadouro_l#
CREATE [VIEW] views.tra_atracadouro_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_atracadouro_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_atracadouro_l.geometriaaproximada 
	left join dominios.tipoatracad as dominio_tipoatracad on dominio_tipoatracad.code = tra_atracadouro_l.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_atracadouro_l.administracao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_atracadouro_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_atracadouro_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_atracadouro_l.situacaofisica
#
DROP VIEW IF EXISTS views.aux_descontinuidade_geometrica_p#
CREATE [VIEW] views.aux_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.aux_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aux_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aux_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edu_arquibancada_a#
CREATE [VIEW] views.edu_arquibancada_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_arquibancada_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_arquibancada_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_arquibancada_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_arquibancada_a.situacaofisica
#
DROP VIEW IF EXISTS views.tra_area_estrut_transporte_a#
CREATE [VIEW] views.tra_area_estrut_transporte_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_estrut_transporte as id_estrut_transporte,
	geom as geom
    [FROM]
        cb.tra_area_estrut_transporte_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_area_estrut_transporte_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.loc_cidade_p#
CREATE [VIEW] views.loc_cidade_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom
    [FROM]
        cb.loc_cidade_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_cidade_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_equip_agropec_a#
CREATE [VIEW] views.eco_equip_agropec_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	dominio_matconstr.code_name as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        cb.eco_equip_agropec_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_equip_agropec_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_a.situacaofisica 
	left join dominios.tipoequipagropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_a.tipoequipagropec 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_equip_agropec_a.matconstr
#
DROP VIEW IF EXISTS views.hid_area_umida_a#
CREATE [VIEW] views.hid_area_umida_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoareaumida.code_name as tipoareaumida,
	geom as geom
    [FROM]
        cb.hid_area_umida_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_area_umida_a.geometriaaproximada 
	left join dominios.tipoareaumida as dominio_tipoareaumida on dominio_tipoareaumida.code = hid_area_umida_a.tipoareaumida
#
DROP VIEW IF EXISTS views.aux_descontinuidade_geometrica_a#
CREATE [VIEW] views.aux_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.aux_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aux_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aux_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lim_unidade_protecao_integral_p#
CREATE [VIEW] views.lim_unidade_protecao_integral_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	anocriacao as anocriacao,
	areaoficial as areaoficial,
	atolegal as atolegal,
	dominio_administracao.code_name as administracao,
	dominio_tipounidprotinteg.code_name as tipounidprotinteg,
	sigla as sigla
    [FROM]
        cb.lim_unidade_protecao_integral_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_protecao_integral_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_protecao_integral_p.administracao 
	left join dominios.tipounidprotinteg as dominio_tipounidprotinteg on dominio_tipounidprotinteg.code = lim_unidade_protecao_integral_p.tipounidprotinteg
#
DROP VIEW IF EXISTS views.enc_area_comunicacao_a#
CREATE [VIEW] views.enc_area_comunicacao_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        cb.enc_area_comunicacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_area_comunicacao_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_plataforma_a#
CREATE [VIEW] views.eco_plataforma_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoplataforma.code_name as tipoplataforma,
	geom as geom
    [FROM]
        cb.eco_plataforma_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_plataforma_a.geometriaaproximada 
	left join dominios.tipoplataforma as dominio_tipoplataforma on dominio_tipoplataforma.code = eco_plataforma_a.tipoplataforma
#
DROP VIEW IF EXISTS views.enc_termeletrica_a#
CREATE [VIEW] views.enc_termeletrica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom,
	dominio_tipocombustivel.code_name as tipocombustivel,
	dominio_combrenovavel.code_name as combrenovavel,
	dominio_tipomaqtermica.code_name as tipomaqtermica,
	dominio_geracao.code_name as geracao
    [FROM]
        cb.enc_termeletrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_termeletrica_a.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_termeletrica_a.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_termeletrica_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_termeletrica_a.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_termeletrica_a.destenergelet 
	left join dominios.tipocombustivel as dominio_tipocombustivel on dominio_tipocombustivel.code = enc_termeletrica_a.tipocombustivel 
	left join dominios.combrenovavel as dominio_combrenovavel on dominio_combrenovavel.code = enc_termeletrica_a.combrenovavel 
	left join dominios.tipomaqtermica as dominio_tipomaqtermica on dominio_tipomaqtermica.code = enc_termeletrica_a.tipomaqtermica 
	left join dominios.geracao as dominio_geracao on dominio_geracao.code = enc_termeletrica_a.geracao
#
DROP VIEW IF EXISTS views.lim_sub_distrito_a#
CREATE [VIEW] views.lim_sub_distrito_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	geocodigo as geocodigo,
	anodereferencia as anodereferencia
    [FROM]
        cb.lim_sub_distrito_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_sub_distrito_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.loc_nome_local_p#
CREATE [VIEW] views.loc_nome_local_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.loc_nome_local_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_nome_local_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_area_ext_mineral_a#
CREATE [VIEW] views.eco_area_ext_mineral_a as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        cb.eco_area_ext_mineral_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_area_ext_mineral_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_unidade_protecao_integral_a#
CREATE [VIEW] views.lim_unidade_protecao_integral_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_tipounidprotinteg.code_name as tipounidprotinteg,
	dominio_administracao.code_name as administracao,
	atolegal as atolegal,
	areaoficial as areaoficial,
	anocriacao as anocriacao,
	sigla as sigla
    [FROM]
        cb.lim_unidade_protecao_integral_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_protecao_integral_a.geometriaaproximada 
	left join dominios.tipounidprotinteg as dominio_tipounidprotinteg on dominio_tipounidprotinteg.code = lim_unidade_protecao_integral_a.tipounidprotinteg 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lim_unidade_protecao_integral_a.administracao
#
DROP VIEW IF EXISTS views.eco_plataforma_p#
CREATE [VIEW] views.eco_plataforma_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoplataforma.code_name as tipoplataforma,
	geom as geom
    [FROM]
        cb.eco_plataforma_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_plataforma_p.geometriaaproximada 
	left join dominios.tipoplataforma as dominio_tipoplataforma on dominio_tipoplataforma.code = eco_plataforma_p.tipoplataforma
#
DROP VIEW IF EXISTS views.hid_foz_maritima_a#
CREATE [VIEW] views.hid_foz_maritima_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.hid_foz_maritima_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.enc_termeletrica_p#
CREATE [VIEW] views.enc_termeletrica_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom,
	dominio_tipocombustivel.code_name as tipocombustivel,
	dominio_combrenovavel.code_name as combrenovavel,
	dominio_tipomaqtermica.code_name as tipomaqtermica,
	dominio_geracao.code_name as geracao
    [FROM]
        cb.enc_termeletrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_termeletrica_p.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_termeletrica_p.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_termeletrica_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_termeletrica_p.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_termeletrica_p.destenergelet 
	left join dominios.tipocombustivel as dominio_tipocombustivel on dominio_tipocombustivel.code = enc_termeletrica_p.tipocombustivel 
	left join dominios.combrenovavel as dominio_combrenovavel on dominio_combrenovavel.code = enc_termeletrica_p.combrenovavel 
	left join dominios.tipomaqtermica as dominio_tipomaqtermica on dominio_tipomaqtermica.code = enc_termeletrica_p.tipomaqtermica 
	left join dominios.geracao as dominio_geracao on dominio_geracao.code = enc_termeletrica_p.geracao
#
DROP VIEW IF EXISTS views.enc_torre_energia_p#
CREATE [VIEW] views.enc_torre_energia_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_ovgd.code_name as ovgd,
	alturaestimada as alturaestimada,
	dominio_tipotorre.code_name as tipotorre,
	arranjofases as arranjofases,
	geom as geom
    [FROM]
        cb.enc_torre_energia_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_torre_energia_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_torre_energia_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_torre_energia_p.situacaofisica 
	left join dominios.ovgd as dominio_ovgd on dominio_ovgd.code = enc_torre_energia_p.ovgd 
	left join dominios.tipotorre as dominio_tipotorre on dominio_tipotorre.code = enc_torre_energia_p.tipotorre
#
DROP VIEW IF EXISTS views.hid_natureza_fundo_p#
CREATE [VIEW] views.hid_natureza_fundo_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_materialpredominante.code_name as materialpredominante,
	dominio_espessalgas.code_name as espessalgas,
	geom as geom
    [FROM]
        cb.hid_natureza_fundo_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_natureza_fundo_p.geometriaaproximada 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_natureza_fundo_p.materialpredominante 
	left join dominios.espessalgas as dominio_espessalgas on dominio_espessalgas.code = hid_natureza_fundo_p.espessalgas
#
DROP VIEW IF EXISTS views.hid_bacia_hidrografica_a#
CREATE [VIEW] views.hid_bacia_hidrografica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codigootto as codigootto,
	nivelotto as nivelotto,
	geom as geom
    [FROM]
        cb.hid_bacia_hidrografica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_bacia_hidrografica_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_edif_const_lazer_a#
CREATE [VIEW] views.edu_edif_const_lazer_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoediflazer.code_name as tipoediflazer,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_edif_const_lazer_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_const_lazer_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_const_lazer_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_const_lazer_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_const_lazer_a.matconstr 
	left join dominios.tipoediflazer as dominio_tipoediflazer on dominio_tipoediflazer.code = edu_edif_const_lazer_a.tipoediflazer
#
DROP VIEW IF EXISTS views.enc_hidreletrica_l#
CREATE [VIEW] views.enc_hidreletrica_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom,
	codigohidreletrica as codigohidreletrica
    [FROM]
        cb.enc_hidreletrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_l.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_l.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_hidreletrica_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_l.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_hidreletrica_l.destenergelet
#
DROP VIEW IF EXISTS views.hid_descontinuidade_geometrica_p#
CREATE [VIEW] views.hid_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.hid_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hid_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_area_comerc_serv_a#
CREATE [VIEW] views.eco_area_comerc_serv_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        cb.eco_area_comerc_serv_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_area_comerc_serv_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_patio_p#
CREATE [VIEW] views.tra_patio_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_modaluso.code_name as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_estrut_transporte as id_estrut_transporte,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_org_industrial as id_org_industrial,
	id_org_ensino as id_org_ensino,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.tra_patio_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_patio_p.geometriaaproximada 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_patio_p.modaluso 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_patio_p.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_patio_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_patio_p.situacaofisica
#
DROP VIEW IF EXISTS views.sau_descontinuidade_geometrica_a#
CREATE [VIEW] views.sau_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.sau_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = sau_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.enc_hidreletrica_a#
CREATE [VIEW] views.enc_hidreletrica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom,
	codigohidreletrica as codigohidreletrica
    [FROM]
        cb.enc_hidreletrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_a.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_a.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_hidreletrica_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_a.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_hidreletrica_a.destenergelet
#
DROP VIEW IF EXISTS views.loc_aglomerado_rural_p#
CREATE [VIEW] views.loc_aglomerado_rural_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom
    [FROM]
        cb.loc_aglomerado_rural_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_aglomerado_rural_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_edif_constr_aeroportuaria_p#
CREATE [VIEW] views.tra_edif_constr_aeroportuaria_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifaero.code_name as tipoedifaero,
	dominio_administracao.code_name as administracao,
	id_complexo_aeroportuario as id_complexo_aeroportuario
    [FROM]
        cb.tra_edif_constr_aeroportuaria_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_constr_aeroportuaria_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_constr_aeroportuaria_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_constr_aeroportuaria_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_constr_aeroportuaria_p.matconstr 
	left join dominios.tipoedifaero as dominio_tipoedifaero on dominio_tipoedifaero.code = tra_edif_constr_aeroportuaria_p.tipoedifaero 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_constr_aeroportuaria_p.administracao
#
DROP VIEW IF EXISTS views.rel_dolina_a#
CREATE [VIEW] views.rel_dolina_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        cb.rel_dolina_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_dolina_a.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_dolina_a.tipoelemnat
#
DROP VIEW IF EXISTS views.hid_confluencia_p#
CREATE [VIEW] views.hid_confluencia_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        cb.hid_confluencia_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_confluencia_p.geometriaaproximada 
	left join dominios.relacionado_hid as dominio_relacionado on dominio_relacionado.code = hid_confluencia_p.relacionado
#
DROP VIEW IF EXISTS views.tra_pista_ponto_pouso_l#
CREATE [VIEW] views.tra_pista_ponto_pouso_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipopista.code_name as tipopista,
	dominio_revestimento.code_name as revestimento,
	dominio_usopista.code_name as usopista,
	dominio_homologacao.code_name as homologacao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	largura as largura,
	extensao as extensao,
	id_complexo_aeroportuario as id_complexo_aeroportuario,
	geom as geom
    [FROM]
        cb.tra_pista_ponto_pouso_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_pista_ponto_pouso_l.geometriaaproximada 
	left join dominios.tipopista as dominio_tipopista on dominio_tipopista.code = tra_pista_ponto_pouso_l.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_pista_ponto_pouso_l.revestimento 
	left join dominios.usopista as dominio_usopista on dominio_usopista.code = tra_pista_ponto_pouso_l.usopista 
	left join dominios.homologacao as dominio_homologacao on dominio_homologacao.code = tra_pista_ponto_pouso_l.homologacao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_pista_ponto_pouso_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_pista_ponto_pouso_l.situacaofisica
#
DROP VIEW IF EXISTS views.tra_passag_elevada_viaduto_l#
CREATE [VIEW] views.tra_passag_elevada_viaduto_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipopassagviad.code_name as tipopassagviad,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	gabhorizsup as gabhorizsup,
	gabvertsup as gabvertsup,
	cargasuportmaxima as cargasuportmaxima,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_posicaopista.code_name as posicaopista,
	extensao as extensao,
	largura as largura,
	geom as geom
    [FROM]
        cb.tra_passag_elevada_viaduto_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_passag_elevada_viaduto_l.geometriaaproximada 
	left join dominios.tipopassagviad as dominio_tipopassagviad on dominio_tipopassagviad.code = tra_passag_elevada_viaduto_l.tipopassagviad 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_passag_elevada_viaduto_l.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_passag_elevada_viaduto_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_passag_elevada_viaduto_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_passag_elevada_viaduto_l.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_passag_elevada_viaduto_l.posicaopista
#
DROP VIEW IF EXISTS views.hid_natureza_fundo_a#
CREATE [VIEW] views.hid_natureza_fundo_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_materialpredominante.code_name as materialpredominante,
	dominio_espessalgas.code_name as espessalgas,
	geom as geom
    [FROM]
        cb.hid_natureza_fundo_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_natureza_fundo_a.geometriaaproximada 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_natureza_fundo_a.materialpredominante 
	left join dominios.espessalgas as dominio_espessalgas on dominio_espessalgas.code = hid_natureza_fundo_a.espessalgas
#
DROP VIEW IF EXISTS views.tra_eclusa_a#
CREATE [VIEW] views.tra_eclusa_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_eclusa_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_eclusa_a.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_eclusa_a.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_eclusa_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_eclusa_a.situacaofisica
#
DROP VIEW IF EXISTS views.sau_edif_saude_a#
CREATE [VIEW] views.sau_edif_saude_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_nivelatencao.code_name as nivelatencao,
	id_org_saude as id_org_saude
    [FROM]
        cb.sau_edif_saude_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_edif_saude_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = sau_edif_saude_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = sau_edif_saude_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = sau_edif_saude_a.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_edif_saude_a.tipoclassecnae 
	left join dominios.nivelatencao as dominio_nivelatencao on dominio_nivelatencao.code = sau_edif_saude_a.nivelatencao
#
DROP VIEW IF EXISTS views.veg_campo_a#
CREATE [VIEW] views.veg_campo_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocampo.code_name as tipocampo,
	dominio_ocorrenciaem.code_name as ocorrenciaem,
	geom as geom
    [FROM]
        cb.veg_campo_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_campo_a.geometriaaproximada 
	left join dominios.tipocampo as dominio_tipocampo on dominio_tipocampo.code = veg_campo_a.tipocampo 
	left join dominios.ocorrenciaem as dominio_ocorrenciaem on dominio_ocorrenciaem.code = veg_campo_a.ocorrenciaem
#
DROP VIEW IF EXISTS views.loc_vila_p#
CREATE [VIEW] views.loc_vila_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom
    [FROM]
        cb.loc_vila_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_vila_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_fonte_dagua_p#
CREATE [VIEW] views.hid_fonte_dagua_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipofontedagua.code_name as tipofontedagua,
	dominio_qualidagua.code_name as qualidagua,
	dominio_regime.code_name as regime,
	geom as geom
    [FROM]
        cb.hid_fonte_dagua_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_fonte_dagua_p.geometriaaproximada 
	left join dominios.tipofontedagua as dominio_tipofontedagua on dominio_tipofontedagua.code = hid_fonte_dagua_p.tipofontedagua 
	left join dominios.qualidagua as dominio_qualidagua on dominio_qualidagua.code = hid_fonte_dagua_p.qualidagua 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_fonte_dagua_p.regime
#
DROP VIEW IF EXISTS views.loc_capital_p#
CREATE [VIEW] views.loc_capital_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom,
	dominio_tipocapital.code_name as tipocapital
    [FROM]
        cb.loc_capital_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_capital_p.geometriaaproximada 
	left join dominios.tipocapital as dominio_tipocapital on dominio_tipocapital.code = loc_capital_p.tipocapital
#
DROP VIEW IF EXISTS views.hid_natureza_fundo_l#
CREATE [VIEW] views.hid_natureza_fundo_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_materialpredominante.code_name as materialpredominante,
	dominio_espessalgas.code_name as espessalgas,
	geom as geom
    [FROM]
        cb.hid_natureza_fundo_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_natureza_fundo_l.geometriaaproximada 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_natureza_fundo_l.materialpredominante 
	left join dominios.espessalgas as dominio_espessalgas on dominio_espessalgas.code = hid_natureza_fundo_l.espessalgas
#
DROP VIEW IF EXISTS views.lim_area_politico_adm_a#
CREATE [VIEW] views.lim_area_politico_adm_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.lim_area_politico_adm_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_politico_adm_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_deposito_geral_p#
CREATE [VIEW] views.eco_deposito_geral_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	dominio_matconstr.code_name as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	dominio_tipoprodutoresiduo.code_name as tipoprodutoresiduo,
	dominio_tipoconteudo.code_name as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_tratamento.code_name as tratamento,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	id_estrut_transporte as id_estrut_transporte,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        cb.eco_deposito_geral_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_deposito_geral_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_deposito_geral_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_deposito_geral_p.situacaofisica 
	left join dominios.tipodepgeral as dominio_tipodepgeral on dominio_tipodepgeral.code = eco_deposito_geral_p.tipodepgeral 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_deposito_geral_p.matconstr 
	left join dominios.tipoexposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = eco_deposito_geral_p.tipoexposicao 
	left join dominios.tipoprodutoresiduo as dominio_tipoprodutoresiduo on dominio_tipoprodutoresiduo.code = eco_deposito_geral_p.tipoprodutoresiduo 
	left join dominios.tipoconteudo as dominio_tipoconteudo on dominio_tipoconteudo.code = eco_deposito_geral_p.tipoconteudo 
	left join dominios.unidadevolume as dominio_unidadevolume on dominio_unidadevolume.code = eco_deposito_geral_p.unidadevolume 
	left join dominios.tratamento as dominio_tratamento on dominio_tratamento.code = eco_deposito_geral_p.tratamento
#
DROP VIEW IF EXISTS views.sau_area_servico_social_a#
CREATE [VIEW] views.sau_area_servico_social_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_servico_social as id_org_servico_social,
	geom as geom
    [FROM]
        cb.sau_area_servico_social_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_area_servico_social_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_ruina_a#
CREATE [VIEW] views.edu_ruina_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_ruina_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_ruina_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_pista_competicao_l#
CREATE [VIEW] views.edu_pista_competicao_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopista.code_name as tipopista,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_pista_competicao_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_pista_competicao_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_pista_competicao_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_pista_competicao_l.situacaofisica 
	left join dominios.tipopista as dominio_tipopista on dominio_tipopista.code = edu_pista_competicao_l.tipopista
#
DROP VIEW IF EXISTS views.rel_duna_p#
CREATE [VIEW] views.rel_duna_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_fixa.code_name as fixa
    [FROM]
        cb.rel_duna_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_duna_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_duna_p.tipoelemnat 
	left join dominios.fixa as dominio_fixa on dominio_fixa.code = rel_duna_p.fixa
#
DROP VIEW IF EXISTS views.asb_descontinuidade_geometrica_p#
CREATE [VIEW] views.asb_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.asb_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = asb_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_entroncamento_p#
CREATE [VIEW] views.tra_entroncamento_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoentroncamento.code_name as tipoentroncamento,
	geom as geom
    [FROM]
        cb.tra_entroncamento_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_entroncamento_p.geometriaaproximada 
	left join dominios.tipoentroncamento as dominio_tipoentroncamento on dominio_tipoentroncamento.code = tra_entroncamento_p.tipoentroncamento
#
DROP VIEW IF EXISTS views.eco_edif_industrial_a#
CREATE [VIEW] views.eco_edif_industrial_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_chamine.code_name as chamine,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	id_org_industrial as id_org_industrial
    [FROM]
        cb.eco_edif_industrial_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_industrial_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_industrial_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_industrial_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_industrial_a.matconstr 
	left join dominios.chamine as dominio_chamine on dominio_chamine.code = eco_edif_industrial_a.chamine 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_edif_industrial_a.tipodivisaocnae
#
DROP VIEW IF EXISTS views.hid_ilha_p#
CREATE [VIEW] views.hid_ilha_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha
    [FROM]
        cb.hid_ilha_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_p.tipoelemnat 
	left join dominios.tipoilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_p.tipoilha
#
DROP VIEW IF EXISTS views.edu_ruina_p#
CREATE [VIEW] views.edu_ruina_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_ruina_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_ruina_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_area_industrial_a#
CREATE [VIEW] views.eco_area_industrial_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        cb.eco_area_industrial_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_area_industrial_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_marco_de_limite_p#
CREATE [VIEW] views.lim_marco_de_limite_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipomarcolim.code_name as tipomarcolim,
	latitude_gms as latitude_gms,
	latitude as latitude,
	longitude_gms as longitude_gms,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	outrarefplan as outrarefplan,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	orgresp as orgresp,
	geom as geom
    [FROM]
        cb.lim_marco_de_limite_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_marco_de_limite_p.geometriaaproximada 
	left join dominios.tipomarcolim as dominio_tipomarcolim on dominio_tipomarcolim.code = lim_marco_de_limite_p.tipomarcolim 
	left join dominios.sistemageodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = lim_marco_de_limite_p.sistemageodesico 
	left join dominios.referencialaltim as dominio_referencialaltim on dominio_referencialaltim.code = lim_marco_de_limite_p.referencialaltim
#
DROP VIEW IF EXISTS views.hid_ilha_l#
CREATE [VIEW] views.hid_ilha_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha
    [FROM]
        cb.hid_ilha_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_l.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_l.tipoelemnat 
	left join dominios.tipoilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_l.tipoilha
#
DROP VIEW IF EXISTS views.rel_duna_a#
CREATE [VIEW] views.rel_duna_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_fixa.code_name as fixa
    [FROM]
        cb.rel_duna_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_duna_a.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_duna_a.tipoelemnat 
	left join dominios.fixa as dominio_fixa on dominio_fixa.code = rel_duna_a.fixa
#
DROP VIEW IF EXISTS views.lim_limite_area_especial_l#
CREATE [VIEW] views.lim_limite_area_especial_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	dominio_tipolimareaesp.code_name as tipolimareaesp,
	obssituacao as obssituacao
    [FROM]
        cb.lim_limite_area_especial_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_limite_area_especial_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_limite_area_especial_l.geometriaaproximada 
	left join dominios.tipolimareaesp as dominio_tipolimareaesp on dominio_tipolimareaesp.code = lim_limite_area_especial_l.tipolimareaesp
#
DROP VIEW IF EXISTS views.asb_descontinuidade_geometrica_a#
CREATE [VIEW] views.asb_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.asb_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = asb_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_funicular_l#
CREATE [VIEW] views.tra_funicular_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_ext_mineral as id_org_ext_mineral,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.tra_funicular_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_funicular_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_funicular_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_funicular_l.situacaofisica
#
DROP VIEW IF EXISTS views.eco_edif_industrial_p#
CREATE [VIEW] views.eco_edif_industrial_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_chamine.code_name as chamine,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	id_org_industrial as id_org_industrial
    [FROM]
        cb.eco_edif_industrial_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_industrial_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_industrial_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_industrial_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_industrial_p.matconstr 
	left join dominios.chamine as dominio_chamine on dominio_chamine.code = eco_edif_industrial_p.chamine 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_edif_industrial_p.tipodivisaocnae
#
DROP VIEW IF EXISTS views.rel_rocha_p#
CREATE [VIEW] views.rel_rocha_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tiporocha.code_name as tiporocha
    [FROM]
        cb.rel_rocha_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_rocha_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_rocha_p.tipoelemnat 
	left join dominios.tiporocha as dominio_tiporocha on dominio_tiporocha.code = rel_rocha_p.tiporocha
#
DROP VIEW IF EXISTS views.edu_area_religiosa_a#
CREATE [VIEW] views.edu_area_religiosa_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_religiosa as id_org_religiosa
    [FROM]
        cb.edu_area_religiosa_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_area_religiosa_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_ponte_p#
CREATE [VIEW] views.tra_ponte_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoponte.code_name as tipoponte,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	vaolivrehoriz as vaolivrehoriz,
	vaolivrevertical as vaolivrevertical,
	cargasuportmaxima as cargasuportmaxima,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_ponte_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponte_p.geometriaaproximada 
	left join dominios.tipoponte as dominio_tipoponte on dominio_tipoponte.code = tra_ponte_p.tipoponte 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_ponte_p.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_ponte_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_ponte_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_ponte_p.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_ponte_p.posicaopista
#
DROP VIEW IF EXISTS views.hid_ilha_a#
CREATE [VIEW] views.hid_ilha_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha
    [FROM]
        cb.hid_ilha_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_a.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_a.tipoelemnat 
	left join dominios.tipoilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_a.tipoilha
#
DROP VIEW IF EXISTS views.tra_arruamento_l#
CREATE [VIEW] views.tra_arruamento_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrfaixas as nrfaixas,
	dominio_trafego.code_name as trafego,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	geom as geom
    [FROM]
        cb.tra_arruamento_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_arruamento_l.geometriaaproximada 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_arruamento_l.revestimento 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_arruamento_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_arruamento_l.situacaofisica 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = tra_arruamento_l.trafego 
	left join dominios.canteirodivisorio as dominio_canteirodivisorio on dominio_canteirodivisorio.code = tra_arruamento_l.canteirodivisorio
#
DROP VIEW IF EXISTS views.pto_descontinuidade_geometrica_p#
CREATE [VIEW] views.pto_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.pto_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = pto_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_rocha_em_agua_a#
CREATE [VIEW] views.hid_rocha_em_agua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_situacaoemagua.code_name as situacaoemagua,
	alturalamina as alturalamina,
	geom as geom
    [FROM]
        cb.hid_rocha_em_agua_a 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_rocha_em_agua_a.situacaoemagua
#
DROP VIEW IF EXISTS views.tra_local_critico_p#
CREATE [VIEW] views.tra_local_critico_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolocalcrit.code_name as tipolocalcrit,
	geom as geom
    [FROM]
        cb.tra_local_critico_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_local_critico_p.geometriaaproximada 
	left join dominios.tipolocalcrit as dominio_tipolocalcrit on dominio_tipolocalcrit.code = tra_local_critico_p.tipolocalcrit
#
DROP VIEW IF EXISTS views.hid_recife_a#
CREATE [VIEW] views.hid_recife_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situamare.code_name as situamare,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        cb.hid_recife_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_a.geometriaaproximada 
	left join dominios.tiporecife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_a.tiporecife 
	left join dominios.situamare as dominio_situamare on dominio_situamare.code = hid_recife_a.situamare 
	left join dominios.situacaocosta as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_a.situacaocosta
#
DROP VIEW IF EXISTS views.hid_recife_l#
CREATE [VIEW] views.hid_recife_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situamare.code_name as situamare,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        cb.hid_recife_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_l.geometriaaproximada 
	left join dominios.tiporecife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_l.tiporecife 
	left join dominios.situamare as dominio_situamare on dominio_situamare.code = hid_recife_l.situamare 
	left join dominios.situacaocosta as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_l.situacaocosta
#
DROP VIEW IF EXISTS views.veg_cerrado_cerradao_a#
CREATE [VIEW] views.veg_cerrado_cerradao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	dominio_tipocerr.code_name as tipocerr,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_cerrado_cerradao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_cerrado_cerradao_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_cerrado_cerradao_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_cerrado_cerradao_a.antropizada 
	left join dominios.tipocerr as dominio_tipocerr on dominio_tipocerr.code = veg_cerrado_cerradao_a.tipocerr 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_cerrado_cerradao_a.classificacaoporte
#
DROP VIEW IF EXISTS views.loc_area_habitacional_a#
CREATE [VIEW] views.loc_area_habitacional_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        cb.loc_area_habitacional_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_area_habitacional_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_l#
CREATE [VIEW] views.tra_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.tra_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = tra_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.pto_descontinuidade_geometrica_a#
CREATE [VIEW] views.pto_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.pto_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = pto_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_barragem_l#
CREATE [VIEW] views.hid_barragem_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.hid_barragem_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_l.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = hid_barragem_l.matconstr 
	left join dominios.usoprincipal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_l.usoprincipal 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_barragem_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_l.situacaofisica
#
DROP VIEW IF EXISTS views.tra_local_critico_a#
CREATE [VIEW] views.tra_local_critico_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolocalcrit.code_name as tipolocalcrit,
	geom as geom
    [FROM]
        cb.tra_local_critico_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_local_critico_a.geometriaaproximada 
	left join dominios.tipolocalcrit as dominio_tipolocalcrit on dominio_tipolocalcrit.code = tra_local_critico_a.tipolocalcrit
#
DROP VIEW IF EXISTS views.hid_rocha_em_agua_p#
CREATE [VIEW] views.hid_rocha_em_agua_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_situacaoemagua.code_name as situacaoemagua,
	alturalamina as alturalamina,
	geom as geom
    [FROM]
        cb.hid_rocha_em_agua_p 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_rocha_em_agua_p.situacaoemagua
#
DROP VIEW IF EXISTS views.tra_funicular_p#
CREATE [VIEW] views.tra_funicular_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_ext_mineral as id_org_ext_mineral,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.tra_funicular_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_funicular_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_funicular_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_funicular_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_recife_p#
CREATE [VIEW] views.hid_recife_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situamare.code_name as situamare,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        cb.hid_recife_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_p.geometriaaproximada 
	left join dominios.tiporecife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_p.tiporecife 
	left join dominios.situamare as dominio_situamare on dominio_situamare.code = hid_recife_p.situamare 
	left join dominios.situacaocosta as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_p.situacaocosta
#
DROP VIEW IF EXISTS views.veg_macega_chavascal_a#
CREATE [VIEW] views.veg_macega_chavascal_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	dominio_tipomacchav.code_name as tipomacchav,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_macega_chavascal_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_macega_chavascal_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_macega_chavascal_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_macega_chavascal_a.antropizada 
	left join dominios.tipomacchav as dominio_tipomacchav on dominio_tipomacchav.code = veg_macega_chavascal_a.tipomacchav 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_macega_chavascal_a.classificacaoporte
#
DROP VIEW IF EXISTS views.lim_area_desenv_controle_p#
CREATE [VIEW] views.lim_area_desenv_controle_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	classificacao as classificacao
    [FROM]
        cb.lim_area_desenv_controle_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_desenv_controle_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_descontinuidade_geometrica_l#
CREATE [VIEW] views.asb_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.asb_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = asb_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_tunel_p#
CREATE [VIEW] views.tra_tunel_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotunel.code_name as tipotunel,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_posicaopista.code_name as posicaopista,
	altura as altura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_tunel_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_tunel_p.geometriaaproximada 
	left join dominios.tipotunel as dominio_tipotunel on dominio_tipotunel.code = tra_tunel_p.tipotunel 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_tunel_p.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_tunel_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_tunel_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_tunel_p.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_tunel_p.posicaopista
#
DROP VIEW IF EXISTS views.loc_aglomerado_rural_isolado_p#
CREATE [VIEW] views.loc_aglomerado_rural_isolado_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom,
	dominio_tipoaglomrurisol.code_name as tipoaglomrurisol
    [FROM]
        cb.loc_aglomerado_rural_isolado_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_aglomerado_rural_isolado_p.geometriaaproximada 
	left join dominios.tipoaglomrurisol as dominio_tipoaglomrurisol on dominio_tipoaglomrurisol.code = loc_aglomerado_rural_isolado_p.tipoaglomrurisol
#
DROP VIEW IF EXISTS views.tra_obstaculo_navegacao_p#
CREATE [VIEW] views.tra_obstaculo_navegacao_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        cb.tra_obstaculo_navegacao_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_obstaculo_navegacao_p.geometriaaproximada 
	left join dominios.tipoobst as dominio_tipoobst on dominio_tipoobst.code = tra_obstaculo_navegacao_p.tipoobst 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = tra_obstaculo_navegacao_p.situacaoemagua
#
DROP VIEW IF EXISTS views.loc_area_urbana_isolada_a#
CREATE [VIEW] views.loc_area_urbana_isolada_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoassociado.code_name as tipoassociado,
	geom as geom
    [FROM]
        cb.loc_area_urbana_isolada_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_area_urbana_isolada_a.geometriaaproximada 
	left join dominios.tipoassociado as dominio_tipoassociado on dominio_tipoassociado.code = loc_area_urbana_isolada_a.tipoassociado
#
DROP VIEW IF EXISTS views.enc_grupo_transformadores_p#
CREATE [VIEW] views.enc_grupo_transformadores_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_subestacao_ener_eletr as id_subestacao_ener_eletr,
	geom as geom
    [FROM]
        cb.enc_grupo_transformadores_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_grupo_transformadores_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_pais_a#
CREATE [VIEW] views.lim_pais_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	sigla as sigla,
	codiso3166 as codiso3166
    [FROM]
        cb.lim_pais_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_pais_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_edif_saneamento_p#
CREATE [VIEW] views.asb_edif_saneamento_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifsaneam.code_name as tipoedifsaneam,
	id_complexo_saneamento as id_complexo_saneamento
    [FROM]
        cb.asb_edif_saneamento_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_edif_saneamento_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_edif_saneamento_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_edif_saneamento_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_edif_saneamento_p.matconstr 
	left join dominios.tipoedifsaneam as dominio_tipoedifsaneam on dominio_tipoedifsaneam.code = asb_edif_saneamento_p.tipoedifsaneam
#
DROP VIEW IF EXISTS views.pto_pto_ref_geod_topo_p#
CREATE [VIEW] views.pto_pto_ref_geod_topo_p as 
	SELECT
	id as id,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	outrarefplan as outrarefplan,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom,
	nome as nome,
	dominio_proximidade.code_name as proximidade,
	dominio_tipoptorefgeodtopo.code_name as tipoptorefgeodtopo,
	dominio_rede.code_name as rede,
	dominio_referencialgrav.code_name as referencialgrav,
	dominio_situacaomarco.code_name as situacaomarco,
	datavisita as datavisita
    [FROM]
        cb.pto_pto_ref_geod_topo_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_ref_geod_topo_p.geometriaaproximada 
	left join dominios.tiporef as dominio_tiporef on dominio_tiporef.code = pto_pto_ref_geod_topo_p.tiporef 
	left join dominios.sistemageodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_ref_geod_topo_p.sistemageodesico 
	left join dominios.referencialaltim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_ref_geod_topo_p.referencialaltim 
	left join dominios.proximidade as dominio_proximidade on dominio_proximidade.code = pto_pto_ref_geod_topo_p.proximidade 
	left join dominios.tipoptorefgeodtopo as dominio_tipoptorefgeodtopo on dominio_tipoptorefgeodtopo.code = pto_pto_ref_geod_topo_p.tipoptorefgeodtopo 
	left join dominios.rede as dominio_rede on dominio_rede.code = pto_pto_ref_geod_topo_p.rede 
	left join dominios.referencialgrav as dominio_referencialgrav on dominio_referencialgrav.code = pto_pto_ref_geod_topo_p.referencialgrav 
	left join dominios.situacaomarco as dominio_situacaomarco on dominio_situacaomarco.code = pto_pto_ref_geod_topo_p.situacaomarco
#
DROP VIEW IF EXISTS views.rel_curva_batimetrica_l#
CREATE [VIEW] views.rel_curva_batimetrica_l as 
	SELECT
	id as id,
	profundidade as profundidade,
	geom as geom
    [FROM]
        cb.rel_curva_batimetrica_l
#
DROP VIEW IF EXISTS views.veg_floresta_a#
CREATE [VIEW] views.veg_floresta_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	dominio_especiepredominante.code_name as especiepredominante,
	dominio_caracteristicafloresta.code_name as caracteristicafloresta,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_floresta_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_floresta_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_floresta_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_floresta_a.antropizada 
	left join dominios.especiepredominante as dominio_especiepredominante on dominio_especiepredominante.code = veg_floresta_a.especiepredominante 
	left join dominios.caracteristicafloresta as dominio_caracteristicafloresta on dominio_caracteristicafloresta.code = veg_floresta_a.caracteristicafloresta 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_floresta_a.classificacaoporte
#
DROP VIEW IF EXISTS views.lim_outros_limites_oficiais_l#
CREATE [VIEW] views.lim_outros_limites_oficiais_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	dominio_tipooutlimofic.code_name as tipooutlimofic,
	obssituacao as obssituacao
    [FROM]
        cb.lim_outros_limites_oficiais_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_outros_limites_oficiais_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_outros_limites_oficiais_l.geometriaaproximada 
	left join dominios.tipooutlimofic as dominio_tipooutlimofic on dominio_tipooutlimofic.code = lim_outros_limites_oficiais_l.tipooutlimofic
#
DROP VIEW IF EXISTS views.adm_edif_pub_militar_a#
CREATE [VIEW] views.adm_edif_pub_militar_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifmil.code_name as tipoedifmil,
	dominio_tipousoedif.code_name as tipousoedif,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        cb.adm_edif_pub_militar_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_edif_pub_militar_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_edif_pub_militar_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_edif_pub_militar_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = adm_edif_pub_militar_a.matconstr 
	left join dominios.tipoedifmil as dominio_tipoedifmil on dominio_tipoedifmil.code = adm_edif_pub_militar_a.tipoedifmil 
	left join dominios.tipousoedif as dominio_tipousoedif on dominio_tipousoedif.code = adm_edif_pub_militar_a.tipousoedif
#
DROP VIEW IF EXISTS views.eco_area_agrop_ext_veg_pesca_a#
CREATE [VIEW] views.eco_area_agrop_ext_veg_pesca_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_destinadoa.code_name as destinadoa,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        cb.eco_area_agrop_ext_veg_pesca_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_area_agrop_ext_veg_pesca_a.geometriaaproximada 
	left join dominios.destinadoa as dominio_destinadoa on dominio_destinadoa.code = eco_area_agrop_ext_veg_pesca_a.destinadoa
#
DROP VIEW IF EXISTS views.rel_ponto_cotado_batimetrico_p#
CREATE [VIEW] views.rel_ponto_cotado_batimetrico_p as 
	SELECT
	id as id,
	profundidade as profundidade,
	geom as geom
    [FROM]
        cb.rel_ponto_cotado_batimetrico_p
#
DROP VIEW IF EXISTS views.tra_obstaculo_navegacao_a#
CREATE [VIEW] views.tra_obstaculo_navegacao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        cb.tra_obstaculo_navegacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_obstaculo_navegacao_a.geometriaaproximada 
	left join dominios.tipoobst as dominio_tipoobst on dominio_tipoobst.code = tra_obstaculo_navegacao_a.tipoobst 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = tra_obstaculo_navegacao_a.situacaoemagua
#
DROP VIEW IF EXISTS views.enc_grupo_transformadores_a#
CREATE [VIEW] views.enc_grupo_transformadores_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_subestacao_ener_eletr as id_subestacao_ener_eletr,
	geom as geom
    [FROM]
        cb.enc_grupo_transformadores_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_grupo_transformadores_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_descontinuidade_geometrica_p#
CREATE [VIEW] views.lim_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.lim_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = lim_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.veg_estepe_a#
CREATE [VIEW] views.veg_estepe_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	alturamediaindividuos as alturamediaindividuos
    [FROM]
        cb.veg_estepe_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_estepe_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_estepe_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_estepe_a.antropizada
#
DROP VIEW IF EXISTS views.tra_obstaculo_navegacao_l#
CREATE [VIEW] views.tra_obstaculo_navegacao_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        cb.tra_obstaculo_navegacao_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_obstaculo_navegacao_l.geometriaaproximada 
	left join dominios.tipoobst as dominio_tipoobst on dominio_tipoobst.code = tra_obstaculo_navegacao_l.tipoobst 
	left join dominios.situacaoemagua as dominio_situacaoemagua on dominio_situacaoemagua.code = tra_obstaculo_navegacao_l.situacaoemagua
#
DROP VIEW IF EXISTS views.lim_limite_operacional_l#
CREATE [VIEW] views.lim_limite_operacional_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	dominio_tipolimoper.code_name as tipolimoper,
	obssituacao as obssituacao
    [FROM]
        cb.lim_limite_operacional_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_limite_operacional_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_limite_operacional_l.geometriaaproximada 
	left join dominios.tipolimoper as dominio_tipolimoper on dominio_tipolimoper.code = lim_limite_operacional_l.tipolimoper
#
DROP VIEW IF EXISTS views.adm_edif_pub_militar_p#
CREATE [VIEW] views.adm_edif_pub_militar_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_tipoedifmil.code_name as tipoedifmil,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        cb.adm_edif_pub_militar_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_edif_pub_militar_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_edif_pub_militar_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_edif_pub_militar_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = adm_edif_pub_militar_p.matconstr 
	left join dominios.tipousoedif as dominio_tipousoedif on dominio_tipousoedif.code = adm_edif_pub_militar_p.tipousoedif 
	left join dominios.tipoedifmil as dominio_tipoedifmil on dominio_tipoedifmil.code = adm_edif_pub_militar_p.tipoedifmil
#
DROP VIEW IF EXISTS views.asb_edif_saneamento_a#
CREATE [VIEW] views.asb_edif_saneamento_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifsaneam.code_name as tipoedifsaneam,
	id_complexo_saneamento as id_complexo_saneamento
    [FROM]
        cb.asb_edif_saneamento_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_edif_saneamento_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_edif_saneamento_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_edif_saneamento_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_edif_saneamento_a.matconstr 
	left join dominios.tipoedifsaneam as dominio_tipoedifsaneam on dominio_tipoedifsaneam.code = asb_edif_saneamento_a.tipoedifsaneam
#
DROP VIEW IF EXISTS views.tra_patio_a#
CREATE [VIEW] views.tra_patio_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_modaluso.code_name as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_estrut_transporte as id_estrut_transporte,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_org_industrial as id_org_industrial,
	id_org_ensino as id_org_ensino,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.tra_patio_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_patio_a.geometriaaproximada 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_patio_a.modaluso 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_patio_a.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_patio_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_patio_a.situacaofisica
#
DROP VIEW IF EXISTS views.enc_trecho_energia_l#
CREATE [VIEW] views.enc_trecho_energia_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_especie.code_name as especie,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_emduto.code_name as emduto,
	tensaoeletrica as tensaoeletrica,
	numcircuitos as numcircuitos,
	id_org_comerc_serv as id_org_comerc_serv,
	geom as geom
    [FROM]
        cb.enc_trecho_energia_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_trecho_energia_l.geometriaaproximada 
	left join dominios.especie as dominio_especie on dominio_especie.code = enc_trecho_energia_l.especie 
	left join dominios.posicaorelativa as dominio_posicaorelativa on dominio_posicaorelativa.code = enc_trecho_energia_l.posicaorelativa 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_trecho_energia_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_trecho_energia_l.situacaofisica 
	left join dominios.emduto as dominio_emduto on dominio_emduto.code = enc_trecho_energia_l.emduto
#
DROP VIEW IF EXISTS views.tra_ponte_l#
CREATE [VIEW] views.tra_ponte_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoponte.code_name as tipoponte,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	vaolivrehoriz as vaolivrehoriz,
	vaolivrevertical as vaolivrevertical,
	cargasuportmaxima as cargasuportmaxima,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_ponte_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponte_l.geometriaaproximada 
	left join dominios.tipoponte as dominio_tipoponte on dominio_tipoponte.code = tra_ponte_l.tipoponte 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_ponte_l.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_ponte_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_ponte_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_ponte_l.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_ponte_l.posicaopista
#
DROP VIEW IF EXISTS views.tra_edif_metro_ferroviaria_p#
CREATE [VIEW] views.tra_edif_metro_ferroviaria_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_funcaoedifmetroferrov.code_name as funcaoedifmetroferrov,
	dominio_multimodal.code_name as multimodal,
	dominio_administracao.code_name as administracao,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        cb.tra_edif_metro_ferroviaria_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_metro_ferroviaria_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_metro_ferroviaria_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_metro_ferroviaria_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_metro_ferroviaria_p.matconstr 
	left join dominios.funcaoedifmetroferrov as dominio_funcaoedifmetroferrov on dominio_funcaoedifmetroferrov.code = tra_edif_metro_ferroviaria_p.funcaoedifmetroferrov 
	left join dominios.multimodal as dominio_multimodal on dominio_multimodal.code = tra_edif_metro_ferroviaria_p.multimodal 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_metro_ferroviaria_p.administracao
#
DROP VIEW IF EXISTS views.tra_trecho_hidroviario_l#
CREATE [VIEW] views.tra_trecho_hidroviario_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_regime.code_name as regime,
	extensaotrecho as extensaotrecho,
	caladomaxseca as caladomaxseca,
	geom as geom,
	id_hidrovia as id_hidrovia
    [FROM]
        cb.tra_trecho_hidroviario_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trecho_hidroviario_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_trecho_hidroviario_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_trecho_hidroviario_l.situacaofisica 
	left join dominios.regime as dominio_regime on dominio_regime.code = tra_trecho_hidroviario_l.regime
#
DROP VIEW IF EXISTS views.adm_edif_pub_civil_p#
CREATE [VIEW] views.adm_edif_pub_civil_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifcivil.code_name as tipoedifcivil,
	dominio_tipousoedif.code_name as tipousoedif,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        cb.adm_edif_pub_civil_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_edif_pub_civil_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_edif_pub_civil_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_edif_pub_civil_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = adm_edif_pub_civil_p.matconstr 
	left join dominios.tipoedifcivil as dominio_tipoedifcivil on dominio_tipoedifcivil.code = adm_edif_pub_civil_p.tipoedifcivil 
	left join dominios.tipousoedif as dominio_tipousoedif on dominio_tipousoedif.code = adm_edif_pub_civil_p.tipousoedif
#
DROP VIEW IF EXISTS views.sau_area_saude_a#
CREATE [VIEW] views.sau_area_saude_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_saude as id_org_saude,
	geom as geom
    [FROM]
        cb.sau_area_saude_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_area_saude_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_dep_abast_agua_p#
CREATE [VIEW] views.asb_dep_abast_agua_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodepabast.code_name as tipodepabast,
	dominio_situacaoagua.code_name as situacaoagua,
	dominio_construcao.code_name as construcao,
	dominio_matconstr.code_name as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	id_complexo_abast_agua as id_complexo_abast_agua,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        cb.asb_dep_abast_agua_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_dep_abast_agua_p.geometriaaproximada 
	left join dominios.tipodepabast as dominio_tipodepabast on dominio_tipodepabast.code = asb_dep_abast_agua_p.tipodepabast 
	left join dominios.situacaoagua as dominio_situacaoagua on dominio_situacaoagua.code = asb_dep_abast_agua_p.situacaoagua 
	left join dominios.construcao as dominio_construcao on dominio_construcao.code = asb_dep_abast_agua_p.construcao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_dep_abast_agua_p.matconstr 
	left join dominios.finalidade_asb as dominio_finalidade on dominio_finalidade.code = asb_dep_abast_agua_p.finalidade 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_dep_abast_agua_p.situacaofisica 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_dep_abast_agua_p.operacional
#
DROP VIEW IF EXISTS views.veg_veg_cultivada_a#
CREATE [VIEW] views.veg_veg_cultivada_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolavoura.code_name as tipolavoura,
	dominio_finalidade.code_name as finalidade,
	dominio_terreno.code_name as terreno,
	dominio_classificacaoporte.code_name as classificacaoporte,
	espacamentoindividuos as espacamentoindividuos,
	espessuradap as espessuradap,
	dominio_denso.code_name as denso,
	alturamediaindividuos as alturamediaindividuos,
	dominio_cultivopredominante.code_name as cultivopredominante,
	geom as geom
    [FROM]
        cb.veg_veg_cultivada_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_cultivada_a.geometriaaproximada 
	left join dominios.tipolavoura as dominio_tipolavoura on dominio_tipolavoura.code = veg_veg_cultivada_a.tipolavoura 
	left join dominios.finalidade_veg as dominio_finalidade on dominio_finalidade.code = veg_veg_cultivada_a.finalidade 
	left join dominios.terreno as dominio_terreno on dominio_terreno.code = veg_veg_cultivada_a.terreno 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_cultivada_a.classificacaoporte 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_veg_cultivada_a.denso 
	left join dominios.cultivopredominante as dominio_cultivopredominante on dominio_cultivopredominante.code = veg_veg_cultivada_a.cultivopredominante
#
DROP VIEW IF EXISTS views.adm_edif_pub_civil_a#
CREATE [VIEW] views.adm_edif_pub_civil_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifcivil.code_name as tipoedifcivil,
	dominio_tipousoedif.code_name as tipousoedif,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        cb.adm_edif_pub_civil_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = adm_edif_pub_civil_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = adm_edif_pub_civil_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = adm_edif_pub_civil_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = adm_edif_pub_civil_a.matconstr 
	left join dominios.tipoedifcivil as dominio_tipoedifcivil on dominio_tipoedifcivil.code = adm_edif_pub_civil_a.tipoedifcivil 
	left join dominios.tipousoedif as dominio_tipousoedif on dominio_tipousoedif.code = adm_edif_pub_civil_a.tipousoedif
#
DROP VIEW IF EXISTS views.sau_edif_saude_p#
CREATE [VIEW] views.sau_edif_saude_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_nivelatencao.code_name as nivelatencao,
	id_org_saude as id_org_saude
    [FROM]
        cb.sau_edif_saude_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_edif_saude_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = sau_edif_saude_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = sau_edif_saude_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = sau_edif_saude_p.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_edif_saude_p.tipoclassecnae 
	left join dominios.nivelatencao as dominio_nivelatencao on dominio_nivelatencao.code = sau_edif_saude_p.nivelatencao
#
DROP VIEW IF EXISTS views.enc_area_energia_eletrica_a#
CREATE [VIEW] views.enc_area_energia_eletrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_subestacao_ener_eletr as id_subestacao_ener_eletr,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr
    [FROM]
        cb.enc_area_energia_eletrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_area_energia_eletrica_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lim_limite_particular_l#
CREATE [VIEW] views.lim_limite_particular_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom,
	obssituacao as obssituacao
    [FROM]
        cb.lim_limite_particular_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_limite_particular_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_limite_particular_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.enc_descontinuidade_geometrica_a#
CREATE [VIEW] views.enc_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.enc_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = enc_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_identific_trecho_rod_p#
CREATE [VIEW] views.tra_identific_trecho_rod_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	sigla as sigla,
	geom as geom,
	id_via_rodoviaria as id_via_rodoviaria
    [FROM]
        cb.tra_identific_trecho_rod_p
#
DROP VIEW IF EXISTS views.tra_edif_metro_ferroviaria_a#
CREATE [VIEW] views.tra_edif_metro_ferroviaria_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_funcaoedifmetroferrov.code_name as funcaoedifmetroferrov,
	dominio_multimodal.code_name as multimodal,
	dominio_administracao.code_name as administracao,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        cb.tra_edif_metro_ferroviaria_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_metro_ferroviaria_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_metro_ferroviaria_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_metro_ferroviaria_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_metro_ferroviaria_a.matconstr 
	left join dominios.funcaoedifmetroferrov as dominio_funcaoedifmetroferrov on dominio_funcaoedifmetroferrov.code = tra_edif_metro_ferroviaria_a.funcaoedifmetroferrov 
	left join dominios.multimodal as dominio_multimodal on dominio_multimodal.code = tra_edif_metro_ferroviaria_a.multimodal 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_metro_ferroviaria_a.administracao
#
DROP VIEW IF EXISTS views.eco_ext_mineral_p#
CREATE [VIEW] views.eco_ext_mineral_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposecaocnae.code_name as tiposecaocnae,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoextmin.code_name as tipoextmin,
	dominio_tipoprodutoresiduo.code_name as tipoprodutoresiduo,
	dominio_tipopocomina.code_name as tipopocomina,
	dominio_procextracao.code_name as procextracao,
	dominio_formaextracao.code_name as formaextracao,
	dominio_atividade.code_name as atividade,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        cb.eco_ext_mineral_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_ext_mineral_p.geometriaaproximada 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_ext_mineral_p.tiposecaocnae 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_ext_mineral_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_ext_mineral_p.situacaofisica 
	left join dominios.tipoextmin as dominio_tipoextmin on dominio_tipoextmin.code = eco_ext_mineral_p.tipoextmin 
	left join dominios.tipoprodutoresiduo as dominio_tipoprodutoresiduo on dominio_tipoprodutoresiduo.code = eco_ext_mineral_p.tipoprodutoresiduo 
	left join dominios.tipopocomina as dominio_tipopocomina on dominio_tipopocomina.code = eco_ext_mineral_p.tipopocomina 
	left join dominios.procextracao as dominio_procextracao on dominio_procextracao.code = eco_ext_mineral_p.procextracao 
	left join dominios.formaextracao as dominio_formaextracao on dominio_formaextracao.code = eco_ext_mineral_p.formaextracao 
	left join dominios.atividade as dominio_atividade on dominio_atividade.code = eco_ext_mineral_p.atividade
#
DROP VIEW IF EXISTS views.rel_gruta_caverna_p#
CREATE [VIEW] views.rel_gruta_caverna_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipogrutacaverna.code_name as tipogrutacaverna
    [FROM]
        cb.rel_gruta_caverna_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_gruta_caverna_p.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_gruta_caverna_p.tipoelemnat 
	left join dominios.tipogrutacaverna as dominio_tipogrutacaverna on dominio_tipogrutacaverna.code = rel_gruta_caverna_p.tipogrutacaverna
#
DROP VIEW IF EXISTS views.edu_area_lazer_a#
CREATE [VIEW] views.edu_area_lazer_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_area_lazer_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_area_lazer_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.loc_edificacao_p#
CREATE [VIEW] views.loc_edificacao_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom
    [FROM]
        cb.loc_edificacao_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_edificacao_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = loc_edificacao_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = loc_edificacao_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = loc_edificacao_p.matconstr
#
DROP VIEW IF EXISTS views.tra_local_critico_l#
CREATE [VIEW] views.tra_local_critico_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolocalcrit.code_name as tipolocalcrit,
	geom as geom
    [FROM]
        cb.tra_local_critico_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_local_critico_l.geometriaaproximada 
	left join dominios.tipolocalcrit as dominio_tipolocalcrit on dominio_tipolocalcrit.code = tra_local_critico_l.tipolocalcrit
#
DROP VIEW IF EXISTS views.lim_area_uso_comunitario_a#
CREATE [VIEW] views.lim_area_uso_comunitario_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_tipoareausocomun.code_name as tipoareausocomun
    [FROM]
        cb.lim_area_uso_comunitario_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_uso_comunitario_a.geometriaaproximada 
	left join dominios.tipoareausocomun as dominio_tipoareausocomun on dominio_tipoareausocomun.code = lim_area_uso_comunitario_a.tipoareausocomun
#
DROP VIEW IF EXISTS views.veg_campinarana_a#
CREATE [VIEW] views.veg_campinarana_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_campinarana_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_campinarana_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_campinarana_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_campinarana_a.antropizada 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_campinarana_a.classificacaoporte
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_a#
CREATE [VIEW] views.rel_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.rel_descontinuidade_geometrica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_quebramar_molhe_a#
CREATE [VIEW] views.hid_quebramar_molhe_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoquebramolhe.code_name as tipoquebramolhe,
	dominio_matconstr.code_name as matconstr,
	dominio_situamare.code_name as situamare,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.hid_quebramar_molhe_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_quebramar_molhe_a.geometriaaproximada 
	left join dominios.tipoquebramolhe as dominio_tipoquebramolhe on dominio_tipoquebramolhe.code = hid_quebramar_molhe_a.tipoquebramolhe 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = hid_quebramar_molhe_a.matconstr 
	left join dominios.situamare as dominio_situamare on dominio_situamare.code = hid_quebramar_molhe_a.situamare 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_quebramar_molhe_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_quebramar_molhe_a.situacaofisica
#
DROP VIEW IF EXISTS views.rel_curva_nivel_l#
CREATE [VIEW] views.rel_curva_nivel_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	cota as cota,
	dominio_depressao.code_name as depressao,
	dominio_indice.code_name as indice,
	geom as geom
    [FROM]
        cb.rel_curva_nivel_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_curva_nivel_l.geometriaaproximada 
	left join dominios.depressao as dominio_depressao on dominio_depressao.code = rel_curva_nivel_l.depressao 
	left join dominios.indice as dominio_indice on dominio_indice.code = rel_curva_nivel_l.indice
#
DROP VIEW IF EXISTS views.hid_quebramar_molhe_l#
CREATE [VIEW] views.hid_quebramar_molhe_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoquebramolhe.code_name as tipoquebramolhe,
	dominio_matconstr.code_name as matconstr,
	dominio_situamare.code_name as situamare,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.hid_quebramar_molhe_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_quebramar_molhe_l.geometriaaproximada 
	left join dominios.tipoquebramolhe as dominio_tipoquebramolhe on dominio_tipoquebramolhe.code = hid_quebramar_molhe_l.tipoquebramolhe 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = hid_quebramar_molhe_l.matconstr 
	left join dominios.situamare as dominio_situamare on dominio_situamare.code = hid_quebramar_molhe_l.situamare 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_quebramar_molhe_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_quebramar_molhe_l.situacaofisica
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_l#
CREATE [VIEW] views.rel_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.rel_descontinuidade_geometrica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.veg_brejo_pantano_a#
CREATE [VIEW] views.veg_brejo_pantano_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	dominio_tipobrejopantano.code_name as tipobrejopantano,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_brejo_pantano_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_brejo_pantano_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_brejo_pantano_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_brejo_pantano_a.antropizada 
	left join dominios.tipobrejopantano as dominio_tipobrejopantano on dominio_tipobrejopantano.code = veg_brejo_pantano_a.tipobrejopantano 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_brejo_pantano_a.classificacaoporte
#
DROP VIEW IF EXISTS views.veg_caatinga_a#
CREATE [VIEW] views.veg_caatinga_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	alturamediaindividuos as alturamediaindividuos,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_caatinga_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_caatinga_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_caatinga_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_caatinga_a.antropizada 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_caatinga_a.classificacaoporte
#
DROP VIEW IF EXISTS views.tra_trecho_ferroviario_l#
CREATE [VIEW] views.tra_trecho_ferroviario_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codtrechoferrov as codtrechoferrov,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_tipotrechoferrov.code_name as tipotrechoferrov,
	dominio_bitola.code_name as bitola,
	dominio_eletrificada.code_name as eletrificada,
	dominio_nrlinhas.code_name as nrlinhas,
	dominio_emarruamento.code_name as emarruamento,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_administracao.code_name as administracao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	cargasuportmaxima as cargasuportmaxima,
	id_via_ferrea as id_via_ferrea,
	geom as geom
    [FROM]
        cb.tra_trecho_ferroviario_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trecho_ferroviario_l.geometriaaproximada 
	left join dominios.posicaorelativa as dominio_posicaorelativa on dominio_posicaorelativa.code = tra_trecho_ferroviario_l.posicaorelativa 
	left join dominios.tipotrechoferrov as dominio_tipotrechoferrov on dominio_tipotrechoferrov.code = tra_trecho_ferroviario_l.tipotrechoferrov 
	left join dominios.bitola as dominio_bitola on dominio_bitola.code = tra_trecho_ferroviario_l.bitola 
	left join dominios.eletrificada as dominio_eletrificada on dominio_eletrificada.code = tra_trecho_ferroviario_l.eletrificada 
	left join dominios.nrlinhas as dominio_nrlinhas on dominio_nrlinhas.code = tra_trecho_ferroviario_l.nrlinhas 
	left join dominios.emarruamento as dominio_emarruamento on dominio_emarruamento.code = tra_trecho_ferroviario_l.emarruamento 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = tra_trecho_ferroviario_l.jurisdicao 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_trecho_ferroviario_l.administracao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_trecho_ferroviario_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_trecho_ferroviario_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_ponto_drenagem_p#
CREATE [VIEW] views.hid_ponto_drenagem_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        cb.hid_ponto_drenagem_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ponto_drenagem_p.geometriaaproximada 
	left join dominios.relacionado_hid as dominio_relacionado on dominio_relacionado.code = hid_ponto_drenagem_p.relacionado
#
DROP VIEW IF EXISTS views.sau_edif_servico_social_a#
CREATE [VIEW] views.sau_edif_servico_social_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_servico_social as id_org_servico_social
    [FROM]
        cb.sau_edif_servico_social_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sau_edif_servico_social_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = sau_edif_servico_social_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = sau_edif_servico_social_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = sau_edif_servico_social_a.matconstr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_edif_servico_social_a.tipoclassecnae
#
DROP VIEW IF EXISTS views.lim_linha_de_limite_l#
CREATE [VIEW] views.lim_linha_de_limite_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_coincidecomdentrode.code_name as coincidecomdentrode,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.lim_linha_de_limite_l 
	left join dominios.coincidecomdentrode_lim as dominio_coincidecomdentrode on dominio_coincidecomdentrode.code = lim_linha_de_limite_l.coincidecomdentrode 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_linha_de_limite_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_area_duto_a#
CREATE [VIEW] views.tra_area_duto_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.tra_area_duto_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_area_duto_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_edif_agrop_ext_veg_pesca_p#
CREATE [VIEW] views.eco_edif_agrop_ext_veg_pesca_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifagropec.code_name as tipoedifagropec,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        cb.eco_edif_agrop_ext_veg_pesca_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_agrop_ext_veg_pesca_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_agrop_ext_veg_pesca_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_agrop_ext_veg_pesca_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_agrop_ext_veg_pesca_p.matconstr 
	left join dominios.tipoedifagropec as dominio_tipoedifagropec on dominio_tipoedifagropec.code = eco_edif_agrop_ext_veg_pesca_p.tipoedifagropec
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_p#
CREATE [VIEW] views.rel_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        cb.rel_descontinuidade_geometrica_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lim_unidade_federacao_a#
CREATE [VIEW] views.lim_unidade_federacao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_sigla.code_name as sigla,
	geocodigo as geocodigo
    [FROM]
        cb.lim_unidade_federacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_unidade_federacao_a.geometriaaproximada 
	left join dominios.sigla as dominio_sigla on dominio_sigla.code = lim_unidade_federacao_a.sigla
#
DROP VIEW IF EXISTS views.asb_dep_abast_agua_a#
CREATE [VIEW] views.asb_dep_abast_agua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodepabast.code_name as tipodepabast,
	dominio_situacaoagua.code_name as situacaoagua,
	dominio_construcao.code_name as construcao,
	dominio_matconstr.code_name as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	id_complexo_abast_agua as id_complexo_abast_agua,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        cb.asb_dep_abast_agua_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_dep_abast_agua_a.geometriaaproximada 
	left join dominios.tipodepabast as dominio_tipodepabast on dominio_tipodepabast.code = asb_dep_abast_agua_a.tipodepabast 
	left join dominios.situacaoagua as dominio_situacaoagua on dominio_situacaoagua.code = asb_dep_abast_agua_a.situacaoagua 
	left join dominios.construcao as dominio_construcao on dominio_construcao.code = asb_dep_abast_agua_a.construcao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_dep_abast_agua_a.matconstr 
	left join dominios.finalidade_asb as dominio_finalidade on dominio_finalidade.code = asb_dep_abast_agua_a.finalidade 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_dep_abast_agua_a.situacaofisica 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_dep_abast_agua_a.operacional
#
DROP VIEW IF EXISTS views.veg_mangue_a#
CREATE [VIEW] views.veg_mangue_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom,
	dominio_classificacaoporte.code_name as classificacaoporte
    [FROM]
        cb.veg_mangue_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_mangue_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_mangue_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_mangue_a.antropizada 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_mangue_a.classificacaoporte
#
DROP VIEW IF EXISTS views.tra_travessia_pedestre_p#
CREATE [VIEW] views.tra_travessia_pedestre_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessiaped.code_name as tipotravessiaped,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_travessia_pedestre_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_pedestre_p.geometriaaproximada 
	left join dominios.tipotravessiaped as dominio_tipotravessiaped on dominio_tipotravessiaped.code = tra_travessia_pedestre_p.tipotravessiaped 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_travessia_pedestre_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_travessia_pedestre_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_travessia_pedestre_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_limite_massa_dagua_l#
CREATE [VIEW] views.hid_limite_massa_dagua_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolimmassa.code_name as tipolimmassa,
	dominio_materialpredominante.code_name as materialpredominante,
	alturamediamargem as alturamediamargem,
	nomeabrev as nomeabrev,
	geom as geom
    [FROM]
        cb.hid_limite_massa_dagua_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_limite_massa_dagua_l.geometriaaproximada 
	left join dominios.tipolimmassa as dominio_tipolimmassa on dominio_tipolimmassa.code = hid_limite_massa_dagua_l.tipolimmassa 
	left join dominios.materialpredominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_limite_massa_dagua_l.materialpredominante
#
DROP VIEW IF EXISTS views.tra_tunel_l#
CREATE [VIEW] views.tra_tunel_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotunel.code_name as tipotunel,
	dominio_modaluso.code_name as modaluso,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_posicaopista.code_name as posicaopista,
	altura as altura,
	extensao as extensao,
	geom as geom
    [FROM]
        cb.tra_tunel_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_tunel_l.geometriaaproximada 
	left join dominios.tipotunel as dominio_tipotunel on dominio_tipotunel.code = tra_tunel_l.tipotunel 
	left join dominios.modaluso as dominio_modaluso on dominio_modaluso.code = tra_tunel_l.modaluso 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_tunel_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_tunel_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_tunel_l.situacaofisica 
	left join dominios.posicaopista as dominio_posicaopista on dominio_posicaopista.code = tra_tunel_l.posicaopista
#
DROP VIEW IF EXISTS views.asb_dep_saneamento_a#
CREATE [VIEW] views.asb_dep_saneamento_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodepsaneam.code_name as tipodepsaneam,
	dominio_construcao.code_name as construcao,
	dominio_matconstr.code_name as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_residuo.code_name as residuo,
	dominio_tiporesiduo.code_name as tiporesiduo,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        cb.asb_dep_saneamento_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_dep_saneamento_a.geometriaaproximada 
	left join dominios.tipodepsaneam as dominio_tipodepsaneam on dominio_tipodepsaneam.code = asb_dep_saneamento_a.tipodepsaneam 
	left join dominios.construcao as dominio_construcao on dominio_construcao.code = asb_dep_saneamento_a.construcao 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_dep_saneamento_a.matconstr 
	left join dominios.finalidade_asb as dominio_finalidade on dominio_finalidade.code = asb_dep_saneamento_a.finalidade 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_dep_saneamento_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_dep_saneamento_a.situacaofisica 
	left join dominios.residuo as dominio_residuo on dominio_residuo.code = asb_dep_saneamento_a.residuo 
	left join dominios.tiporesiduo as dominio_tiporesiduo on dominio_tiporesiduo.code = asb_dep_saneamento_a.tiporesiduo
#
DROP VIEW IF EXISTS views.hid_queda_dagua_p#
CREATE [VIEW] views.hid_queda_dagua_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        cb.hid_queda_dagua_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_p.geometriaaproximada 
	left join dominios.tipoqueda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_p.tipoqueda
#
DROP VIEW IF EXISTS views.rel_alter_fisiog_antropica_a#
CREATE [VIEW] views.rel_alter_fisiog_antropica_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom
    [FROM]
        cb.rel_alter_fisiog_antropica_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_alter_fisiog_antropica_a.geometriaaproximada 
	left join dominios.tipoalterantrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_alter_fisiog_antropica_a.tipoalterantrop
#
DROP VIEW IF EXISTS views.lim_area_especial_p#
CREATE [VIEW] views.lim_area_especial_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.lim_area_especial_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_especial_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_alter_fisiog_antropica_l#
CREATE [VIEW] views.rel_alter_fisiog_antropica_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom
    [FROM]
        cb.rel_alter_fisiog_antropica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_alter_fisiog_antropica_l.geometriaaproximada 
	left join dominios.tipoalterantrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_alter_fisiog_antropica_l.tipoalterantrop
#
DROP VIEW IF EXISTS views.asb_edif_abast_agua_p#
CREATE [VIEW] views.asb_edif_abast_agua_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifabast.code_name as tipoedifabast,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        cb.asb_edif_abast_agua_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_edif_abast_agua_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_edif_abast_agua_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_edif_abast_agua_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_edif_abast_agua_p.matconstr 
	left join dominios.tipoedifabast as dominio_tipoedifabast on dominio_tipoedifabast.code = asb_edif_abast_agua_p.tipoedifabast
#
DROP VIEW IF EXISTS views.hid_barragem_a#
CREATE [VIEW] views.hid_barragem_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.hid_barragem_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_a.geometriaaproximada 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = hid_barragem_a.matconstr 
	left join dominios.usoprincipal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_a.usoprincipal 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = hid_barragem_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_a.situacaofisica
#
DROP VIEW IF EXISTS views.hid_reservatorio_hidrico_a#
CREATE [VIEW] views.hid_reservatorio_hidrico_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_usoprincipal.code_name as usoprincipal,
	volumeutil as volumeutil,
	namaximomaximorum as namaximomaximorum,
	namaximooperacional as namaximooperacional,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.hid_reservatorio_hidrico_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_reservatorio_hidrico_a.geometriaaproximada 
	left join dominios.usoprincipal as dominio_usoprincipal on dominio_usoprincipal.code = hid_reservatorio_hidrico_a.usoprincipal
#
DROP VIEW IF EXISTS views.tra_galeria_bueiro_l#
CREATE [VIEW] views.tra_galeria_bueiro_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_matconstr.code_name as matconstr,
	pesosuportmaximo as pesosuportmaximo,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_galeria_bueiro_l 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_galeria_bueiro_l.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_galeria_bueiro_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_galeria_bueiro_l.situacaofisica
#
DROP VIEW IF EXISTS views.rel_rocha_a#
CREATE [VIEW] views.rel_rocha_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tiporocha.code_name as tiporocha
    [FROM]
        cb.rel_rocha_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_rocha_a.geometriaaproximada 
	left join dominios.tipoelemnat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_rocha_a.tipoelemnat 
	left join dominios.tiporocha as dominio_tiporocha on dominio_tiporocha.code = rel_rocha_a.tiporocha
#
DROP VIEW IF EXISTS views.loc_edif_habitacional_p#
CREATE [VIEW] views.loc_edif_habitacional_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	id_complexo_habitacional as id_complexo_habitacional
    [FROM]
        cb.loc_edif_habitacional_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_edif_habitacional_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = loc_edif_habitacional_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = loc_edif_habitacional_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = loc_edif_habitacional_p.matconstr
#
DROP VIEW IF EXISTS views.tra_pista_ponto_pouso_a#
CREATE [VIEW] views.tra_pista_ponto_pouso_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipopista.code_name as tipopista,
	dominio_revestimento.code_name as revestimento,
	dominio_usopista.code_name as usopista,
	dominio_homologacao.code_name as homologacao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	largura as largura,
	extensao as extensao,
	id_complexo_aeroportuario as id_complexo_aeroportuario,
	geom as geom
    [FROM]
        cb.tra_pista_ponto_pouso_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_pista_ponto_pouso_a.geometriaaproximada 
	left join dominios.tipopista as dominio_tipopista on dominio_tipopista.code = tra_pista_ponto_pouso_a.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_pista_ponto_pouso_a.revestimento 
	left join dominios.usopista as dominio_usopista on dominio_usopista.code = tra_pista_ponto_pouso_a.usopista 
	left join dominios.homologacao as dominio_homologacao on dominio_homologacao.code = tra_pista_ponto_pouso_a.homologacao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_pista_ponto_pouso_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_pista_ponto_pouso_a.situacaofisica
#
DROP VIEW IF EXISTS views.tra_galeria_bueiro_p#
CREATE [VIEW] views.tra_galeria_bueiro_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_matconstr.code_name as matconstr,
	pesosuportmaximo as pesosuportmaximo,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_galeria_bueiro_p 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_galeria_bueiro_p.matconstr 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_galeria_bueiro_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_galeria_bueiro_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_queda_dagua_a#
CREATE [VIEW] views.hid_queda_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        cb.hid_queda_dagua_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_a.geometriaaproximada 
	left join dominios.tipoqueda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_a.tipoqueda
#
DROP VIEW IF EXISTS views.loc_localidade_p#
CREATE [VIEW] views.loc_localidade_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitude_gms as latitude_gms,
	longitude as longitude,
	longitude_gms as longitude_gms,
	geom as geom
    [FROM]
        cb.loc_localidade_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_localidade_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.edu_edif_const_lazer_p#
CREATE [VIEW] views.edu_edif_const_lazer_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoediflazer.code_name as tipoediflazer,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_edif_const_lazer_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_edif_const_lazer_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_edif_const_lazer_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_edif_const_lazer_p.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = edu_edif_const_lazer_p.matconstr 
	left join dominios.tipoediflazer as dominio_tipoediflazer on dominio_tipoediflazer.code = edu_edif_const_lazer_p.tipoediflazer
#
DROP VIEW IF EXISTS views.lim_delimitacao_fisica_l#
CREATE [VIEW] views.lim_delimitacao_fisica_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodelimfis.code_name as tipodelimfis,
	dominio_matconstr.code_name as matconstr,
	dominio_eletrificada.code_name as eletrificada,
	geom as geom
    [FROM]
        cb.lim_delimitacao_fisica_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_delimitacao_fisica_l.geometriaaproximada 
	left join dominios.tipodelimfis as dominio_tipodelimfis on dominio_tipodelimfis.code = lim_delimitacao_fisica_l.tipodelimfis 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = lim_delimitacao_fisica_l.matconstr 
	left join dominios.eletrificada as dominio_eletrificada on dominio_eletrificada.code = lim_delimitacao_fisica_l.eletrificada
#
DROP VIEW IF EXISTS views.asb_edif_abast_agua_a#
CREATE [VIEW] views.asb_edif_abast_agua_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifabast.code_name as tipoedifabast,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        cb.asb_edif_abast_agua_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = asb_edif_abast_agua_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = asb_edif_abast_agua_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = asb_edif_abast_agua_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = asb_edif_abast_agua_a.matconstr 
	left join dominios.tipoedifabast as dominio_tipoedifabast on dominio_tipoedifabast.code = asb_edif_abast_agua_a.tipoedifabast
#
DROP VIEW IF EXISTS views.tra_ponto_ferroviario_p#
CREATE [VIEW] views.tra_ponto_ferroviario_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        cb.tra_ponto_ferroviario_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponto_ferroviario_p.geometriaaproximada 
	left join dominios.relacionado_fer as dominio_relacionado on dominio_relacionado.code = tra_ponto_ferroviario_p.relacionado
#
DROP VIEW IF EXISTS views.edu_arquibancada_p#
CREATE [VIEW] views.edu_arquibancada_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_lazer as id_complexo_lazer,
	geom as geom
    [FROM]
        cb.edu_arquibancada_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_arquibancada_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = edu_arquibancada_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = edu_arquibancada_p.situacaofisica
#
DROP VIEW IF EXISTS views.enc_antena_comunic_p#
CREATE [VIEW] views.enc_antena_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_posicaoreledific.code_name as posicaoreledific,
	geom as geom,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        cb.enc_antena_comunic_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_antena_comunic_p.geometriaaproximada 
	left join dominios.posicaoreledific as dominio_posicaoreledific on dominio_posicaoreledific.code = enc_antena_comunic_p.posicaoreledific
#
DROP VIEW IF EXISTS views.hid_queda_dagua_l#
CREATE [VIEW] views.hid_queda_dagua_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        cb.hid_queda_dagua_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_l.geometriaaproximada 
	left join dominios.tipoqueda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_l.tipoqueda
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_p#
CREATE [VIEW] views.enc_est_gerad_energia_eletr_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.enc_est_gerad_energia_eletr_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_p.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_p.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_p.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_est_gerad_energia_eletr_p.destenergelet
#
DROP VIEW IF EXISTS views.veg_vegetacao_a#
CREATE [VIEW] views.veg_vegetacao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_denso.code_name as denso,
	dominio_antropizada.code_name as antropizada,
	geom as geom
    [FROM]
        cb.veg_vegetacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_vegetacao_a.geometriaaproximada 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_vegetacao_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_vegetacao_a.antropizada
#
DROP VIEW IF EXISTS views.veg_veg_area_contato_a#
CREATE [VIEW] views.veg_veg_area_contato_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_classificacaoporte.code_name as classificacaoporte,
	dominio_denso.code_name as denso,
	alturamediaindividuos as alturamediaindividuos,
	dominio_antropizada.code_name as antropizada,
	geom as geom
    [FROM]
        cb.veg_veg_area_contato_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_area_contato_a.geometriaaproximada 
	left join dominios.classificacaoporte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_area_contato_a.classificacaoporte 
	left join dominios.denso as dominio_denso on dominio_denso.code = veg_veg_area_contato_a.denso 
	left join dominios.antropizada as dominio_antropizada on dominio_antropizada.code = veg_veg_area_contato_a.antropizada
#
DROP VIEW IF EXISTS views.tra_pista_ponto_pouso_p#
CREATE [VIEW] views.tra_pista_ponto_pouso_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipopista.code_name as tipopista,
	dominio_revestimento.code_name as revestimento,
	dominio_usopista.code_name as usopista,
	dominio_homologacao.code_name as homologacao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	largura as largura,
	extensao as extensao,
	id_complexo_aeroportuario as id_complexo_aeroportuario,
	geom as geom
    [FROM]
        cb.tra_pista_ponto_pouso_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_pista_ponto_pouso_p.geometriaaproximada 
	left join dominios.tipopista as dominio_tipopista on dominio_tipopista.code = tra_pista_ponto_pouso_p.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_pista_ponto_pouso_p.revestimento 
	left join dominios.usopista as dominio_usopista on dominio_usopista.code = tra_pista_ponto_pouso_p.usopista 
	left join dominios.homologacao as dominio_homologacao on dominio_homologacao.code = tra_pista_ponto_pouso_p.homologacao 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_pista_ponto_pouso_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_pista_ponto_pouso_p.situacaofisica
#
DROP VIEW IF EXISTS views.tra_fundeadouro_p#
CREATE [VIEW] views.tra_fundeadouro_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_destinacaofundeadouro.code_name as destinacaofundeadouro,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_fundeadouro_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_fundeadouro_p.geometriaaproximada 
	left join dominios.destinacaofundeadouro as dominio_destinacaofundeadouro on dominio_destinacaofundeadouro.code = tra_fundeadouro_p.destinacaofundeadouro 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_fundeadouro_p.administracao
#
DROP VIEW IF EXISTS views.lim_municipio_a#
CREATE [VIEW] views.lim_municipio_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	geocodigo as geocodigo,
	anodereferencia as anodereferencia
    [FROM]
        cb.lim_municipio_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_municipio_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_edif_constr_aeroportuaria_a#
CREATE [VIEW] views.tra_edif_constr_aeroportuaria_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifaero.code_name as tipoedifaero,
	dominio_administracao.code_name as administracao,
	id_complexo_aeroportuario as id_complexo_aeroportuario
    [FROM]
        cb.tra_edif_constr_aeroportuaria_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_constr_aeroportuaria_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_constr_aeroportuaria_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_constr_aeroportuaria_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_constr_aeroportuaria_a.matconstr 
	left join dominios.tipoedifaero as dominio_tipoedifaero on dominio_tipoedifaero.code = tra_edif_constr_aeroportuaria_a.tipoedifaero 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_constr_aeroportuaria_a.administracao
#
DROP VIEW IF EXISTS views.tra_cremalheira_p#
CREATE [VIEW] views.tra_cremalheira_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_cremalheira_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_cremalheira_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_cremalheira_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_cremalheira_p.situacaofisica
#
DROP VIEW IF EXISTS views.eco_equip_agropec_l#
CREATE [VIEW] views.eco_equip_agropec_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	dominio_matconstr.code_name as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        cb.eco_equip_agropec_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_equip_agropec_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_l.situacaofisica 
	left join dominios.tipoequipagropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_l.tipoequipagropec 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_equip_agropec_l.matconstr
#
DROP VIEW IF EXISTS views.loc_edificacao_a#
CREATE [VIEW] views.loc_edificacao_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom
    [FROM]
        cb.loc_edificacao_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = loc_edificacao_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = loc_edificacao_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = loc_edificacao_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = loc_edificacao_a.matconstr
#
DROP VIEW IF EXISTS views.pto_pto_controle_p#
CREATE [VIEW] views.pto_pto_controle_p as 
	SELECT
	id as id,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	outrarefplan as outrarefplan,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom,
	dominio_tipoptocontrole.code_name as tipoptocontrole,
	dominio_materializado.code_name as materializado,
	codprojeto as codprojeto
    [FROM]
        cb.pto_pto_controle_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_controle_p.geometriaaproximada 
	left join dominios.tiporef as dominio_tiporef on dominio_tiporef.code = pto_pto_controle_p.tiporef 
	left join dominios.sistemageodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_controle_p.sistemageodesico 
	left join dominios.referencialaltim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_controle_p.referencialaltim 
	left join dominios.tipoptocontrole as dominio_tipoptocontrole on dominio_tipoptocontrole.code = pto_pto_controle_p.tipoptocontrole 
	left join dominios.materializado as dominio_materializado on dominio_materializado.code = pto_pto_controle_p.materializado
#
DROP VIEW IF EXISTS views.tra_cremalheira_l#
CREATE [VIEW] views.tra_cremalheira_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        cb.tra_cremalheira_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_cremalheira_l.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_cremalheira_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_cremalheira_l.situacaofisica
#
DROP VIEW IF EXISTS views.eco_equip_agropec_p#
CREATE [VIEW] views.eco_equip_agropec_p as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	dominio_matconstr.code_name as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        cb.eco_equip_agropec_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_p.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_equip_agropec_p.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_p.situacaofisica 
	left join dominios.tipoequipagropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_p.tipoequipagropec 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_equip_agropec_p.matconstr
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_a#
CREATE [VIEW] views.enc_est_gerad_energia_eletr_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.enc_est_gerad_energia_eletr_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_a.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_a.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_a.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_est_gerad_energia_eletr_a.destenergelet
#
DROP VIEW IF EXISTS views.edu_area_ruinas_a#
CREATE [VIEW] views.edu_area_ruinas_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_lazer as id_complexo_lazer
    [FROM]
        cb.edu_area_ruinas_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edu_area_ruinas_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_fundeadouro_l#
CREATE [VIEW] views.tra_fundeadouro_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_destinacaofundeadouro.code_name as destinacaofundeadouro,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_fundeadouro_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_fundeadouro_l.geometriaaproximada 
	left join dominios.destinacaofundeadouro as dominio_destinacaofundeadouro on dominio_destinacaofundeadouro.code = tra_fundeadouro_l.destinacaofundeadouro 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_fundeadouro_l.administracao
#
DROP VIEW IF EXISTS views.tra_edif_constr_portuaria_a#
CREATE [VIEW] views.tra_edif_constr_portuaria_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifport.code_name as tipoedifport,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario
    [FROM]
        cb.tra_edif_constr_portuaria_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_edif_constr_portuaria_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_edif_constr_portuaria_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_edif_constr_portuaria_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = tra_edif_constr_portuaria_a.matconstr 
	left join dominios.tipoedifport as dominio_tipoedifport on dominio_tipoedifport.code = tra_edif_constr_portuaria_a.tipoedifport 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_edif_constr_portuaria_a.administracao
#
DROP VIEW IF EXISTS views.rel_ponto_cotado_altimetrico_p#
CREATE [VIEW] views.rel_ponto_cotado_altimetrico_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_cotacomprovada.code_name as cotacomprovada,
	cota as cota,
	geom as geom
    [FROM]
        cb.rel_ponto_cotado_altimetrico_p 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_ponto_cotado_altimetrico_p.geometriaaproximada 
	left join dominios.cotacomprovada as dominio_cotacomprovada on dominio_cotacomprovada.code = rel_ponto_cotado_altimetrico_p.cotacomprovada
#
DROP VIEW IF EXISTS views.eco_edif_agrop_ext_veg_pesca_a#
CREATE [VIEW] views.eco_edif_agrop_ext_veg_pesca_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	geom as geom,
	dominio_tipoedifagropec.code_name as tipoedifagropec,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        cb.eco_edif_agrop_ext_veg_pesca_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_edif_agrop_ext_veg_pesca_a.geometriaaproximada 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = eco_edif_agrop_ext_veg_pesca_a.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_edif_agrop_ext_veg_pesca_a.situacaofisica 
	left join dominios.matconstr as dominio_matconstr on dominio_matconstr.code = eco_edif_agrop_ext_veg_pesca_a.matconstr 
	left join dominios.tipoedifagropec as dominio_tipoedifagropec on dominio_tipoedifagropec.code = eco_edif_agrop_ext_veg_pesca_a.tipoedifagropec
#
DROP VIEW IF EXISTS views.tra_fundeadouro_a#
CREATE [VIEW] views.tra_fundeadouro_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_destinacaofundeadouro.code_name as destinacaofundeadouro,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        cb.tra_fundeadouro_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_fundeadouro_a.geometriaaproximada 
	left join dominios.destinacaofundeadouro as dominio_destinacaofundeadouro on dominio_destinacaofundeadouro.code = tra_fundeadouro_a.destinacaofundeadouro 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_fundeadouro_a.administracao
#
DROP VIEW IF EXISTS views.tra_trecho_rodoviario_l#
CREATE [VIEW] views.tra_trecho_rodoviario_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codtrechorodov as codtrechorodov,
	dominio_tipotrechorod.code_name as tipotrechorod,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_administracao.code_name as administracao,
	concessionaria as concessionaria,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_trafego.code_name as trafego,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	geom as geom,
	id_via_rodoviaria as id_via_rodoviaria
    [FROM]
        cb.tra_trecho_rodoviario_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trecho_rodoviario_l.geometriaaproximada 
	left join dominios.tipotrechorod as dominio_tipotrechorod on dominio_tipotrechorod.code = tra_trecho_rodoviario_l.tipotrechorod 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = tra_trecho_rodoviario_l.jurisdicao 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_trecho_rodoviario_l.administracao 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = tra_trecho_rodoviario_l.revestimento 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = tra_trecho_rodoviario_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_trecho_rodoviario_l.situacaofisica 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = tra_trecho_rodoviario_l.trafego 
	left join dominios.canteirodivisorio as dominio_canteirodivisorio on dominio_canteirodivisorio.code = tra_trecho_rodoviario_l.canteirodivisorio
#
DROP VIEW IF EXISTS views.lim_area_particular_a#
CREATE [VIEW] views.lim_area_particular_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        cb.lim_area_particular_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_particular_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_l#
CREATE [VIEW] views.enc_est_gerad_energia_eletr_l as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_destenergelet.code_name as destenergelet,
	codigoestacao as codigoestacao,
	potenciaoutorgada as potenciaoutorgada,
	potenciafiscalizada as potenciafiscalizada,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr,
	geom as geom
    [FROM]
        cb.enc_est_gerad_energia_eletr_l 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_l.geometriaaproximada 
	left join dominios.tipoestgerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_l.tipoestgerad 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_l.operacional 
	left join dominios.situacaofisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_l.situacaofisica 
	left join dominios.destenergelet as dominio_destenergelet on dominio_destenergelet.code = enc_est_gerad_energia_eletr_l.destenergelet
#
DROP VIEW IF EXISTS views.lim_area_de_litigio_a#
CREATE [VIEW] views.lim_area_de_litigio_a as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	descricao as descricao,
	geom as geom
    [FROM]
        cb.lim_area_de_litigio_a 
	left join dominios.geometriaaproximada as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lim_area_de_litigio_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.asb_complexo_saneamento#
CREATE [VIEW] views.asb_complexo_saneamento as 
	SELECT
	id as id,
	nome as nome,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_administracao.code_name as administracao,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.asb_complexo_saneamento 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = asb_complexo_saneamento.tipoclassecnae 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = asb_complexo_saneamento.administracao
#
DROP VIEW IF EXISTS views.sau_org_saude#
CREATE [VIEW] views.sau_org_saude as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae
    [FROM]
        complexos.sau_org_saude 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = sau_org_saude.tipogrupocnae
#
DROP VIEW IF EXISTS views.hid_trecho_curso_dagua#
CREATE [VIEW] views.hid_trecho_curso_dagua as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	id_curso_dagua as id_curso_dagua
    [FROM]
        complexos.hid_trecho_curso_dagua
#
DROP VIEW IF EXISTS views.edu_org_ensino_religioso#
CREATE [VIEW] views.edu_org_ensino_religioso as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_religiosa as id_org_religiosa
    [FROM]
        complexos.edu_org_ensino_religioso 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_religioso.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = edu_org_ensino_religioso.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_org_ensino_religioso.tipoclassecnae
#
DROP VIEW IF EXISTS views.eco_frigorifico_matadouro#
CREATE [VIEW] views.eco_frigorifico_matadouro as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tiposecaocnae.code_name as tiposecaocnae,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar,
	dominio_frigorifico.code_name as frigorifico,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        complexos.eco_frigorifico_matadouro 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_frigorifico_matadouro.tiposecaocnae 
	left join dominios.frigorifico as dominio_frigorifico on dominio_frigorifico.code = eco_frigorifico_matadouro.frigorifico
#
DROP VIEW IF EXISTS views.tra_duto#
CREATE [VIEW] views.tra_duto as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.tra_duto
#
DROP VIEW IF EXISTS views.loc_complexo_habitacional#
CREATE [VIEW] views.loc_complexo_habitacional as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev
    [FROM]
        complexos.loc_complexo_habitacional
#
DROP VIEW IF EXISTS views.tra_complexo_portuario#
CREATE [VIEW] views.tra_complexo_portuario as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipotransporte.code_name as tipotransporte,
	dominio_tipocomplexoportuario.code_name as tipocomplexoportuario
    [FROM]
        complexos.tra_complexo_portuario 
	left join dominios.tipotransporte as dominio_tipotransporte on dominio_tipotransporte.code = tra_complexo_portuario.tipotransporte 
	left join dominios.tipocomplexoportuario as dominio_tipocomplexoportuario on dominio_tipocomplexoportuario.code = tra_complexo_portuario.tipocomplexoportuario
#
DROP VIEW IF EXISTS views.enc_complexo_comunicacao#
CREATE [VIEW] views.enc_complexo_comunicacao as 
	SELECT
	id as id,
	nome as nome,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_comerc_serv as id_org_comerc_serv,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        complexos.enc_complexo_comunicacao 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = enc_complexo_comunicacao.tipoclassecnae
#
DROP VIEW IF EXISTS views.adm_org_pub_civil#
CREATE [VIEW] views.adm_org_pub_civil as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_administracao.code_name as administracao,
	dominio_poderpublico.code_name as poderpublico,
	id_instituicao_publica as id_instituicao_publica,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.adm_org_pub_civil 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = adm_org_pub_civil.tipoclassecnae 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = adm_org_pub_civil.administracao 
	left join dominios.poderpublico as dominio_poderpublico on dominio_poderpublico.code = adm_org_pub_civil.poderpublico
#
DROP VIEW IF EXISTS views.sau_org_saude_militar#
CREATE [VIEW] views.sau_org_saude_militar as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_instituicao.code_name as instituicao,
	dominio_classificsigiloso.code_name as classificsigiloso,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.sau_org_saude_militar 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude_militar.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = sau_org_saude_militar.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_org_saude_militar.tipoclassecnae 
	left join dominios.instituicao as dominio_instituicao on dominio_instituicao.code = sau_org_saude_militar.instituicao 
	left join dominios.classificsigiloso as dominio_classificsigiloso on dominio_classificsigiloso.code = sau_org_saude_militar.classificsigiloso
#
DROP VIEW IF EXISTS views.adm_org_pub_militar#
CREATE [VIEW] views.adm_org_pub_militar as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_administracao.code_name as administracao,
	id_org_pub_militar as id_org_pub_militar,
	id_instituicao_publica as id_instituicao_publica,
	dominio_instituicao.code_name as instituicao,
	dominio_classificsigiloso.code_name as classificsigiloso
    [FROM]
        complexos.adm_org_pub_militar 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = adm_org_pub_militar.tipoclassecnae 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = adm_org_pub_militar.administracao 
	left join dominios.instituicao as dominio_instituicao on dominio_instituicao.code = adm_org_pub_militar.instituicao 
	left join dominios.classificsigiloso as dominio_classificsigiloso on dominio_classificsigiloso.code = adm_org_pub_militar.classificsigiloso
#
DROP VIEW IF EXISTS views.edu_complexo_lazer#
CREATE [VIEW] views.edu_complexo_lazer as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipocomplexolazer.code_name as tipocomplexolazer,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	dominio_administracao.code_name as administracao,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar,
	id_org_ensino as id_org_ensino
    [FROM]
        complexos.edu_complexo_lazer 
	left join dominios.tipocomplexolazer as dominio_tipocomplexolazer on dominio_tipocomplexolazer.code = edu_complexo_lazer.tipocomplexolazer 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = edu_complexo_lazer.tipodivisaocnae 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_complexo_lazer.administracao
#
DROP VIEW IF EXISTS views.hid_curso_dagua#
CREATE [VIEW] views.hid_curso_dagua as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev
    [FROM]
        complexos.hid_curso_dagua
#
DROP VIEW IF EXISTS views.edu_org_ensino_militar#
CREATE [VIEW] views.edu_org_ensino_militar as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_instituicao.code_name as instituicao,
	dominio_classificsigiloso.code_name as classificsigiloso,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.edu_org_ensino_militar 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_militar.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = edu_org_ensino_militar.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_org_ensino_militar.tipoclassecnae 
	left join dominios.instituicao as dominio_instituicao on dominio_instituicao.code = edu_org_ensino_militar.instituicao 
	left join dominios.classificsigiloso as dominio_classificsigiloso on dominio_classificsigiloso.code = edu_org_ensino_militar.classificsigiloso
#
DROP VIEW IF EXISTS views.sau_org_servico_social_pub#
CREATE [VIEW] views.sau_org_servico_social_pub as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sau_org_servico_social_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_servico_social_pub.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = sau_org_servico_social_pub.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_org_servico_social_pub.tipoclassecnae
#
DROP VIEW IF EXISTS views.tra_via_rodoviaria#
CREATE [VIEW] views.tra_via_rodoviaria as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	sigla as sigla
    [FROM]
        complexos.tra_via_rodoviaria
#
DROP VIEW IF EXISTS views.pto_est_med_fenomenos#
CREATE [VIEW] views.pto_est_med_fenomenos as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoestmed.code_name as tipoestmed,
	codigoest as codigoest,
	orgaoenteresp as orgaoenteresp,
	id_est_med_fenomenos as id_est_med_fenomenos
    [FROM]
        complexos.pto_est_med_fenomenos 
	left join dominios.tipoestmed as dominio_tipoestmed on dominio_tipoestmed.code = pto_est_med_fenomenos.tipoestmed
#
DROP VIEW IF EXISTS views.enc_complexo_gerad_energ_eletr#
CREATE [VIEW] views.enc_complexo_gerad_energ_eletr as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.enc_complexo_gerad_energ_eletr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = enc_complexo_gerad_energ_eletr.tipoclassecnae
#
DROP VIEW IF EXISTS views.eco_madeireira#
CREATE [VIEW] views.eco_madeireira as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tiposecaocnae.code_name as tiposecaocnae,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        complexos.eco_madeireira 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_madeireira.tiposecaocnae
#
DROP VIEW IF EXISTS views.asb_complexo_abast_agua#
CREATE [VIEW] views.asb_complexo_abast_agua as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.asb_complexo_abast_agua 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = asb_complexo_abast_agua.tipoclassecnae
#
DROP VIEW IF EXISTS views.adm_instituicao_publica#
CREATE [VIEW] views.adm_instituicao_publica as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	id_instituicao_publica as id_instituicao_publica
    [FROM]
        complexos.adm_instituicao_publica 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = adm_instituicao_publica.tipogrupocnae
#
DROP VIEW IF EXISTS views.sau_org_servico_social#
CREATE [VIEW] views.sau_org_servico_social as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae
    [FROM]
        complexos.sau_org_servico_social 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_servico_social.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = sau_org_servico_social.tipogrupocnae
#
DROP VIEW IF EXISTS views.edu_org_religiosa#
CREATE [VIEW] views.edu_org_religiosa as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoclassecnae.code_name as tipoclassecnae
    [FROM]
        complexos.edu_org_religiosa 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_org_religiosa.tipoclassecnae
#
DROP VIEW IF EXISTS views.tra_via_ferrea#
CREATE [VIEW] views.tra_via_ferrea as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev
    [FROM]
        complexos.tra_via_ferrea
#
DROP VIEW IF EXISTS views.loc_aldeia_indigena#
CREATE [VIEW] views.loc_aldeia_indigena as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	codigofunai as codigofunai,
	terraindigena as terraindigena,
	etnia as etnia
    [FROM]
        complexos.loc_aldeia_indigena
#
DROP VIEW IF EXISTS views.eco_org_comerc_serv#
CREATE [VIEW] views.eco_org_comerc_serv as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae,
	dominio_finalidade.code_name as finalidade
    [FROM]
        complexos.eco_org_comerc_serv 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_org_comerc_serv.tipodivisaocnae 
	left join dominios.finalidade_eco as dominio_finalidade on dominio_finalidade.code = eco_org_comerc_serv.finalidade
#
DROP VIEW IF EXISTS views.tra_estrut_apoio#
CREATE [VIEW] views.tra_estrut_apoio as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tipoestrut.code_name as tipoestrut
    [FROM]
        complexos.tra_estrut_apoio 
	left join dominios.tipoestrut as dominio_tipoestrut on dominio_tipoestrut.code = tra_estrut_apoio.tipoestrut
#
DROP VIEW IF EXISTS views.eco_org_agrop_ext_veg_pesca#
CREATE [VIEW] views.eco_org_agrop_ext_veg_pesca as 
	SELECT
	id as id,
	nome as nome,
	dominio_tipodivisaocnae.code_name as tipodivisaocnae
    [FROM]
        complexos.eco_org_agrop_ext_veg_pesca 
	left join dominios.tipodivisaocnae as dominio_tipodivisaocnae on dominio_tipodivisaocnae.code = eco_org_agrop_ext_veg_pesca.tipodivisaocnae
#
DROP VIEW IF EXISTS views.edu_org_ensino_pub#
CREATE [VIEW] views.edu_org_ensino_pub as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_poderpublico.code_name as poderpublico,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.edu_org_ensino_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_pub.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = edu_org_ensino_pub.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = edu_org_ensino_pub.tipoclassecnae 
	left join dominios.poderpublico as dominio_poderpublico on dominio_poderpublico.code = edu_org_ensino_pub.poderpublico
#
DROP VIEW IF EXISTS views.sau_org_saude_pub#
CREATE [VIEW] views.sau_org_saude_pub as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sau_org_saude_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude_pub.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = sau_org_saude_pub.tipogrupocnae 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = sau_org_saude_pub.tipoclassecnae
#
DROP VIEW IF EXISTS views.eco_org_ext_mineral#
CREATE [VIEW] views.eco_org_ext_mineral as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tiposecaocnae.code_name as tiposecaocnae
    [FROM]
        complexos.eco_org_ext_mineral 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_org_ext_mineral.tiposecaocnae
#
DROP VIEW IF EXISTS views.tra_complexo_aeroportuario#
CREATE [VIEW] views.tra_complexo_aeroportuario as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	indicador as indicador,
	siglaaero as siglaaero,
	dominio_tipocomplexoaero.code_name as tipocomplexoaero,
	dominio_classificacao.code_name as classificacao,
	latoficial as latoficial,
	longoficial as longoficial,
	altitude as altitude
    [FROM]
        complexos.tra_complexo_aeroportuario 
	left join dominios.tipocomplexoaero as dominio_tipocomplexoaero on dominio_tipocomplexoaero.code = tra_complexo_aeroportuario.tipocomplexoaero 
	left join dominios.classificacao as dominio_classificacao on dominio_classificacao.code = tra_complexo_aeroportuario.classificacao
#
DROP VIEW IF EXISTS views.enc_subestacao_ener_eletr#
CREATE [VIEW] views.enc_subestacao_ener_eletr as 
	SELECT
	id as id,
	nome as nome,
	dominio_tipoclassecnae.code_name as tipoclassecnae,
	dominio_tipooperativo.code_name as tipooperativo,
	dominio_operacional.code_name as operacional,
	id_complexo_gerad_energ_eletr as id_complexo_gerad_energ_eletr
    [FROM]
        complexos.enc_subestacao_ener_eletr 
	left join dominios.tipoclassecnae as dominio_tipoclassecnae on dominio_tipoclassecnae.code = enc_subestacao_ener_eletr.tipoclassecnae 
	left join dominios.tipooperativo as dominio_tipooperativo on dominio_tipooperativo.code = enc_subestacao_ener_eletr.tipooperativo 
	left join dominios.operacional as dominio_operacional on dominio_operacional.code = enc_subestacao_ener_eletr.operacional
#
DROP VIEW IF EXISTS views.edu_org_ensino#
CREATE [VIEW] views.edu_org_ensino as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	dominio_tipogrupocnae.code_name as tipogrupocnae
    [FROM]
        complexos.edu_org_ensino 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino.administracao 
	left join dominios.tipogrupocnae as dominio_tipogrupocnae on dominio_tipogrupocnae.code = edu_org_ensino.tipogrupocnae
#
DROP VIEW IF EXISTS views.tra_estrut_transporte#
CREATE [VIEW] views.tra_estrut_transporte as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev
    [FROM]
        complexos.tra_estrut_transporte
#
DROP VIEW IF EXISTS views.tra_hidrovia#
CREATE [VIEW] views.tra_hidrovia as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_administracao.code_name as administracao,
	extensaototal as extensaototal
    [FROM]
        complexos.tra_hidrovia 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_hidrovia.administracao
#
DROP VIEW IF EXISTS views.eco_org_industrial#
CREATE [VIEW] views.eco_org_industrial as 
	SELECT
	id as id,
	nome as nome,
	nomeabrev as nomeabrev,
	dominio_tiposecaocnae.code_name as tiposecaocnae,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.eco_org_industrial 
	left join dominios.tiposecaocnae as dominio_tiposecaocnae on dominio_tiposecaocnae.code = eco_org_industrial.tiposecaocnae