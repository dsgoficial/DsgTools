CREATE OR REPLACE FUNCTION edu_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $edu_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_area_saneamento_a_avoid_multi () RETURNS TRIGGER AS $asb_area_saneamento_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_area_saneamento_a(geometriaaproximada,id_complexo_saneamento,geom) SELECT NEW.geometriaaproximada,NEW.id_complexo_saneamento,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_area_saneamento_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_area_saneamento_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_area_saneamento_a
    FOR EACH ROW EXECUTE PROCEDURE asb_area_saneamento_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_comerc_serv_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_comerc_serv_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_comerc_serv_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifcomercserv,finalidade,id_org_comerc_serv) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcomercserv,NEW.finalidade,NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_comerc_serv_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_comerc_serv_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_comerc_serv_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_comerc_serv_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_cerrado_cerradao_a_avoid_multi () RETURNS TRIGGER AS $veg_cerrado_cerradao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_cerrado_cerradao_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,tipocerr,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocerr,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_cerrado_cerradao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_cerrado_cerradao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_cerrado_cerradao_a
    FOR EACH ROW EXECUTE PROCEDURE veg_cerrado_cerradao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_comerc_serv_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_comerc_serv_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_comerc_serv_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifcomercserv,finalidade,id_org_comerc_serv) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcomercserv,NEW.finalidade,NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_comerc_serv_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_comerc_serv_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_comerc_serv_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_comerc_serv_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $edu_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_l_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_l(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_l
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_l_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_area_pub_militar_a_avoid_multi () RETURNS TRIGGER AS $adm_area_pub_militar_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_area_pub_militar_a(geometriaaproximada,geom,id_org_pub_militar) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_pub_militar ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_area_pub_militar_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_area_pub_militar_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_area_pub_militar_a
    FOR EACH ROW EXECUTE PROCEDURE adm_area_pub_militar_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_campo_quadra_p_avoid_multi () RETURNS TRIGGER AS $edu_campo_quadra_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_campo_quadra_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipocampoquadra,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipocampoquadra,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_campo_quadra_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_campo_quadra_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_campo_quadra_p
    FOR EACH ROW EXECUTE PROCEDURE edu_campo_quadra_p_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_a_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_a(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_a
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_particular_a_avoid_multi () RETURNS TRIGGER AS $lim_area_particular_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_particular_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_particular_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_particular_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_particular_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_particular_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_campo_quadra_a_avoid_multi () RETURNS TRIGGER AS $edu_campo_quadra_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_campo_quadra_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipocampoquadra,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipocampoquadra,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_campo_quadra_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_campo_quadra_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_campo_quadra_a
    FOR EACH ROW EXECUTE PROCEDURE edu_campo_quadra_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_p_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_p
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_delimitacao_fisica_l_avoid_multi () RETURNS TRIGGER AS $lim_delimitacao_fisica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_delimitacao_fisica_l(nome,nomeabrev,geometriaaproximada,tipodelimfis,matconstr,eletrificada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodelimfis,NEW.matconstr,NEW.eletrificada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_delimitacao_fisica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_delimitacao_fisica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_delimitacao_fisica_l
    FOR EACH ROW EXECUTE PROCEDURE lim_delimitacao_fisica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_hab_indigena_p_avoid_multi () RETURNS TRIGGER AS $loc_hab_indigena_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_hab_indigena_p(nome,nomeabrev,geometriaaproximada,coletiva,isolada,id_aldeia_indigena,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.coletiva,NEW.isolada,NEW.id_aldeia_indigena,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_hab_indigena_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_hab_indigena_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_hab_indigena_p
    FOR EACH ROW EXECUTE PROCEDURE loc_hab_indigena_p_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_edif_constr_est_med_fen_a_avoid_multi () RETURNS TRIGGER AS $pto_edif_constr_est_med_fen_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_edif_constr_est_med_fen_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_edif_constr_est_med_fen_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_edif_constr_est_med_fen_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_edif_constr_est_med_fen_a
    FOR EACH ROW EXECUTE PROCEDURE pto_edif_constr_est_med_fen_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_edif_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_edif_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_comunic_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,modalidade,tipoedifcomunic,id_complexo_comunicacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.modalidade,NEW.tipoedifcomunic,NEW.id_complexo_comunicacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_comunic_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_terra_indigena_p_avoid_multi () RETURNS TRIGGER AS $lim_terra_indigena_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_indigena_p(nome,nomeabrev,nomeTi,situacaojuridica,datasituacaojuridica,grupoetnico,areaoficialha,perimetrooficial,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.nomeTi,NEW.situacaojuridica,NEW.datasituacaojuridica,NEW.grupoetnico,NEW.areaoficialha,NEW.perimetrooficial,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_indigena_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_indigena_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_indigena_p
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_indigena_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $edu_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_hab_indigena_a_avoid_multi () RETURNS TRIGGER AS $loc_hab_indigena_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_hab_indigena_a(nome,nomeabrev,geometriaaproximada,coletiva,isolada,id_aldeia_indigena,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.coletiva,NEW.isolada,NEW.id_aldeia_indigena,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_hab_indigena_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_hab_indigena_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_hab_indigena_a
    FOR EACH ROW EXECUTE PROCEDURE loc_hab_indigena_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_edif_comunic_a_avoid_multi () RETURNS TRIGGER AS $enc_edif_comunic_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_comunic_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,modalidade,tipoedifcomunic,id_complexo_comunicacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.modalidade,NEW.tipoedifcomunic,NEW.id_complexo_comunicacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_comunic_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_comunic_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_comunic_a
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_comunic_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_terra_indigena_a_avoid_multi () RETURNS TRIGGER AS $lim_terra_indigena_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_indigena_a(nome,nomeabrev,nomeTi,situacaojuridica,datasituacaojuridica,grupoetnico,areaoficialha,perimetrooficial,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.nomeTi,NEW.situacaojuridica,NEW.datasituacaojuridica,NEW.grupoetnico,NEW.areaoficialha,NEW.perimetrooficial,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_indigena_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_indigena_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_indigena_a
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_indigena_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_limite_operacional_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_operacional_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_operacional_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,tipolimoper,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolimoper,NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_operacional_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_operacional_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_operacional_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_operacional_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_foz_maritima_p_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_p(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_p
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_foz_maritima_l_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_l(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_l
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_foz_maritima_a_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_a
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponte_p_avoid_multi () RETURNS TRIGGER AS $tra_ponte_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponte_p(nome,nomeabrev,geometriaaproximada,tipoponte,modaluso,matconstr,operacional,situacaofisica,vaolivrehoriz,vaolivrevertical,cargasuportmaxima,nrfaixas,nrpistas,posicaopista,largura,extensao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoponte,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaolivrevertical,NEW.cargasuportmaxima,NEW.nrfaixas,NEW.nrpistas,NEW.posicaopista,NEW.largura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponte_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponte_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponte_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponte_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponte_l_avoid_multi () RETURNS TRIGGER AS $tra_ponte_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponte_l(nome,nomeabrev,geometriaaproximada,tipoponte,modaluso,matconstr,operacional,situacaofisica,vaolivrehoriz,vaolivrevertical,cargasuportmaxima,nrfaixas,nrpistas,posicaopista,largura,extensao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoponte,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaolivrevertical,NEW.cargasuportmaxima,NEW.nrfaixas,NEW.nrpistas,NEW.posicaopista,NEW.largura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponte_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponte_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponte_l
    FOR EACH ROW EXECUTE PROCEDURE tra_ponte_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_sinalizacao_p_avoid_multi () RETURNS TRIGGER AS $tra_sinalizacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_sinalizacao_p(nome,nomeabrev,geometriaaproximada,tiposinal,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiposinal,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_sinalizacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_sinalizacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_sinalizacao_p
    FOR EACH ROW EXECUTE PROCEDURE tra_sinalizacao_p_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_pto_controle_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_controle_p(nomeabrev,geometriaaproximada,tiporef,latitude,longitude,altitudeortometrica,sistemageodesico,referencialaltim,outrarefalt,orgaoenteresp,codponto,obs,geom,tipoptocontrole,materializado,codprojeto) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporef,NEW.latitude,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.referencialaltim,NEW.outrarefalt,NEW.orgaoenteresp,NEW.codponto,NEW.obs,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoptocontrole,NEW.materializado,NEW.codprojeto ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_controle_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_controle_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_conserv_nao_snuc_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_conserv_nao_snuc_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_conserv_nao_snuc_a(nome,nomeabrev,geometriaaproximada,geom,atolegal,administracao,classificacao,anocriacao,sigla,areaoficial) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.atolegal,NEW.administracao,NEW.classificacao,NEW.anocriacao,NEW.sigla,NEW.areaoficial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_conserv_nao_snuc_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_conserv_nao_snuc_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_conserv_nao_snuc_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_conserv_nao_snuc_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_aglomerado_rural_isolado_p_avoid_multi () RETURNS TRIGGER AS $loc_aglomerado_rural_isolado_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglomerado_rural_isolado_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom,tipoaglomrurisol) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoaglomrurisol ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglomerado_rural_isolado_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglomerado_rural_isolado_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglomerado_rural_isolado_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglomerado_rural_isolado_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_massa_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_massa_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_massa_dagua_a(nome,nomeabrev,geometriaaproximada,tipomassadagua,regime,salinidade,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipomassadagua,NEW.regime,NEW.salinidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_massa_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_massa_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_massa_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_massa_dagua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_conserv_nao_snuc_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_conserv_nao_snuc_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_conserv_nao_snuc_p(nome,nomeabrev,geometriaaproximada,geom,atolegal,administracao,classificacao,anocriacao,sigla,areaoficial) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.atolegal,NEW.administracao,NEW.classificacao,NEW.anocriacao,NEW.sigla,NEW.areaoficial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_conserv_nao_snuc_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_conserv_nao_snuc_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_conserv_nao_snuc_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_conserv_nao_snuc_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_ext_mineral_a(nome,nomeabrev,tiposecaocnae,operacional,situacaofisica,tipoextmin,tipoprodutoresiduo,tipopocomina,procextracao,formaextracao,atividade,id_org_ext_mineral,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.tiposecaocnae,NEW.operacional,NEW.situacaofisica,NEW.tipoextmin,NEW.tipoprodutoresiduo,NEW.tipopocomina,NEW.procextracao,NEW.formaextracao,NEW.atividade,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_ext_mineral_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_ext_mineral_p_avoid_multi () RETURNS TRIGGER AS $eco_ext_mineral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_ext_mineral_p(nome,nomeabrev,tiposecaocnae,operacional,situacaofisica,tipoextmin,tipoprodutoresiduo,tipopocomina,procextracao,formaextracao,atividade,id_org_ext_mineral,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.tiposecaocnae,NEW.operacional,NEW.situacaofisica,NEW.tipoextmin,NEW.tipoprodutoresiduo,NEW.tipopocomina,NEW.procextracao,NEW.formaextracao,NEW.atividade,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_ext_mineral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_ext_mineral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_ext_mineral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_ext_mineral_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_area_comunicacao_a_avoid_multi () RETURNS TRIGGER AS $enc_area_comunicacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_area_comunicacao_a(geometriaaproximada,geom,id_complexo_comunicacao) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_comunicacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_area_comunicacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_area_comunicacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_area_comunicacao_a
    FOR EACH ROW EXECUTE PROCEDURE enc_area_comunicacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_vegetacao_a_avoid_multi () RETURNS TRIGGER AS $veg_vegetacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_vegetacao_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_vegetacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_vegetacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_vegetacao_a
    FOR EACH ROW EXECUTE PROCEDURE veg_vegetacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_nome_local_p_avoid_multi () RETURNS TRIGGER AS $loc_nome_local_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_nome_local_p(nome,geometriaaproximada,geom) SELECT NEW.nome,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_nome_local_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_nome_local_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_nome_local_p
    FOR EACH ROW EXECUTE PROCEDURE loc_nome_local_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_aglomerado_rural_p_avoid_multi () RETURNS TRIGGER AS $loc_aglomerado_rural_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglomerado_rural_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglomerado_rural_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglomerado_rural_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglomerado_rural_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglomerado_rural_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_ruina_a_avoid_multi () RETURNS TRIGGER AS $edu_ruina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_ruina_a(nome,nomeabrev,geometriaaproximada,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_ruina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_ruina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_ruina_a
    FOR EACH ROW EXECUTE PROCEDURE edu_ruina_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_industrial_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_industrial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_industrial_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,chamine,tipodivisaocnae,id_org_industrial) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.chamine,NEW.tipodivisaocnae,NEW.id_org_industrial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_industrial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_industrial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_industrial_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_industrial_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_ruina_p_avoid_multi () RETURNS TRIGGER AS $edu_ruina_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_ruina_p(nome,nomeabrev,geometriaaproximada,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_ruina_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_ruina_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_ruina_p
    FOR EACH ROW EXECUTE PROCEDURE edu_ruina_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_industrial_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_industrial_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_industrial_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,chamine,tipodivisaocnae,id_org_industrial) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.chamine,NEW.tipodivisaocnae,NEW.id_org_industrial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_industrial_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_industrial_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_industrial_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_industrial_p_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $pto_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE pto_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_rocha_em_agua_a_avoid_multi () RETURNS TRIGGER AS $hid_rocha_em_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_rocha_em_agua_a(nome,nomeabrev,situacaoemagua,alturalamina,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.situacaoemagua,NEW.alturalamina,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_rocha_em_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_rocha_em_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_rocha_em_agua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_rocha_em_agua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $pto_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE pto_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_rocha_em_agua_p_avoid_multi () RETURNS TRIGGER AS $hid_rocha_em_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_rocha_em_agua_p(nome,nomeabrev,situacaoemagua,alturalamina,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.situacaoemagua,NEW.alturalamina,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_rocha_em_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_rocha_em_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_rocha_em_agua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_rocha_em_agua_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_estepe_a_avoid_multi () RETURNS TRIGGER AS $veg_estepe_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_estepe_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,alturamediaindividuos) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.alturamediaindividuos ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_estepe_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_estepe_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_estepe_a
    FOR EACH ROW EXECUTE PROCEDURE veg_estepe_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_tunel_p_avoid_multi () RETURNS TRIGGER AS $tra_tunel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_tunel_p(geometriaaproximada,nome,nomeabrev,tipotunel,modaluso,matconstr,operacional,situacaofisica,nrpistas,nrfaixas,posicaopista,altura,extensao,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.tipotunel,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.nrpistas,NEW.nrfaixas,NEW.posicaopista,NEW.altura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_tunel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_tunel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_tunel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_tunel_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_p_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_p(nome,nomeabrev,geometriaaproximada,tipoobst,situacaoemagua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoobst,NEW.situacaoemagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_p
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_grupo_transformadores_p_avoid_multi () RETURNS TRIGGER AS $enc_grupo_transformadores_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_grupo_transformadores_p(nome,nomeabrev,geometriaaproximada,id_subestacao_ener_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_subestacao_ener_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_grupo_transformadores_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_grupo_transformadores_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_grupo_transformadores_p
    FOR EACH ROW EXECUTE PROCEDURE enc_grupo_transformadores_p_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_pto_ref_geod_topo_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_ref_geod_topo_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_ref_geod_topo_p(nomeabrev,geometriaaproximada,tiporef,latitude,longitude,altitudeortometrica,sistemageodesico,referencialaltim,outrarefalt,orgaoenteresp,codponto,obs,geom,nome,proximidade,tipoptorefgeodtopo,rede,referencialgrav,situacaomarco,datavisita) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporef,NEW.latitude,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.referencialaltim,NEW.outrarefalt,NEW.orgaoenteresp,NEW.codponto,NEW.obs,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.proximidade,NEW.tipoptorefgeodtopo,NEW.rede,NEW.referencialgrav,NEW.situacaomarco,NEW.datavisita ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_ref_geod_topo_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_ref_geod_topo_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_ref_geod_topo_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_ref_geod_topo_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_a_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_a(nome,nomeabrev,geometriaaproximada,tipoobst,situacaoemagua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoobst,NEW.situacaoemagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_a
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_grupo_transformadores_a_avoid_multi () RETURNS TRIGGER AS $enc_grupo_transformadores_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_grupo_transformadores_a(nome,nomeabrev,geometriaaproximada,id_subestacao_ener_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_subestacao_ener_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_grupo_transformadores_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_grupo_transformadores_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_grupo_transformadores_a
    FOR EACH ROW EXECUTE PROCEDURE enc_grupo_transformadores_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_l_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_l(nome,nomeabrev,geometriaaproximada,tipoobst,situacaoemagua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoobst,NEW.situacaoemagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_l
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_l_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_edif_saneamento_a_avoid_multi () RETURNS TRIGGER AS $asb_edif_saneamento_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_saneamento_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifsaneam,id_complexo_saneamento) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifsaneam,NEW.id_complexo_saneamento ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_saneamento_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_saneamento_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_saneamento_a
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_saneamento_a_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_edif_saude_a_avoid_multi () RETURNS TRIGGER AS $sau_edif_saude_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_saude_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,nivelatencao,id_org_saude) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.nivelatencao,NEW.id_org_saude ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_saude_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_saude_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_saude_a
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_saude_a_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_edif_saneamento_p_avoid_multi () RETURNS TRIGGER AS $asb_edif_saneamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_saneamento_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifsaneam,id_complexo_saneamento) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifsaneam,NEW.id_complexo_saneamento ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_saneamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_saneamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_saneamento_p
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_saneamento_p_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_edif_saude_p_avoid_multi () RETURNS TRIGGER AS $sau_edif_saude_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_saude_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,nivelatencao,id_org_saude) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.nivelatencao,NEW.id_org_saude ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_saude_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_saude_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_saude_p
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_saude_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_area_energia_eletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_area_energia_eletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_area_energia_eletrica_a(geometriaaproximada,geom,id_subestacao_ener_eletr,id_complexo_gerad_energ_eletr) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_subestacao_ener_eletr,NEW.id_complexo_gerad_energ_eletr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_area_energia_eletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_area_energia_eletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_area_energia_eletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_area_energia_eletrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_area_lazer_a_avoid_multi () RETURNS TRIGGER AS $edu_area_lazer_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_lazer_a(geometriaaproximada,geom,id_complexo_lazer) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_lazer_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_lazer_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_lazer_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_lazer_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_campinarana_a_avoid_multi () RETURNS TRIGGER AS $veg_campinarana_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_campinarana_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_campinarana_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_campinarana_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_campinarana_a
    FOR EACH ROW EXECUTE PROCEDURE veg_campinarana_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_brejo_pantano_a_avoid_multi () RETURNS TRIGGER AS $veg_brejo_pantano_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_brejo_pantano_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,tipobrejopantano,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipobrejopantano,NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_brejo_pantano_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_brejo_pantano_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_brejo_pantano_a
    FOR EACH ROW EXECUTE PROCEDURE veg_brejo_pantano_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_ponto_drenagem_p_avoid_multi () RETURNS TRIGGER AS $hid_ponto_drenagem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ponto_drenagem_p(nome,nomeabrev,geometriaaproximada,relacionado,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ponto_drenagem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ponto_drenagem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ponto_drenagem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ponto_drenagem_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_limite_massa_dagua_l_avoid_multi () RETURNS TRIGGER AS $hid_limite_massa_dagua_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_limite_massa_dagua_l(geometriaaproximada,tipolimmassa,materialpredominante,alturamediamargem,nomeabrev,geom) SELECT NEW.geometriaaproximada,NEW.tipolimmassa,NEW.materialpredominante,NEW.alturamediamargem,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_limite_massa_dagua_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_limite_massa_dagua_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_limite_massa_dagua_l
    FOR EACH ROW EXECUTE PROCEDURE hid_limite_massa_dagua_l_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_coreto_tribuna_a_avoid_multi () RETURNS TRIGGER AS $edu_coreto_tribuna_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_coreto_tribuna_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_coreto_tribuna_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_coreto_tribuna_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_coreto_tribuna_a
    FOR EACH ROW EXECUTE PROCEDURE edu_coreto_tribuna_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_alter_fisiog_antropica_a_avoid_multi () RETURNS TRIGGER AS $rel_alter_fisiog_antropica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_alter_fisiog_antropica_a(nome,nomeabrev,geometriaaproximada,tipoalterantrop,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoalterantrop,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_alter_fisiog_antropica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_alter_fisiog_antropica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_alter_fisiog_antropica_a
    FOR EACH ROW EXECUTE PROCEDURE rel_alter_fisiog_antropica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_alter_fisiog_antropica_l_avoid_multi () RETURNS TRIGGER AS $rel_alter_fisiog_antropica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_alter_fisiog_antropica_l(nome,nomeabrev,geometriaaproximada,tipoalterantrop,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoalterantrop,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_alter_fisiog_antropica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_alter_fisiog_antropica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_alter_fisiog_antropica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_alter_fisiog_antropica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_coreto_tribuna_p_avoid_multi () RETURNS TRIGGER AS $edu_coreto_tribuna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_coreto_tribuna_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_coreto_tribuna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_coreto_tribuna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_coreto_tribuna_p
    FOR EACH ROW EXECUTE PROCEDURE edu_coreto_tribuna_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_piscina_a_avoid_multi () RETURNS TRIGGER AS $edu_piscina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_piscina_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_piscina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_piscina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_piscina_a
    FOR EACH ROW EXECUTE PROCEDURE edu_piscina_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_edificacao_a_avoid_multi () RETURNS TRIGGER AS $loc_edificacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edificacao_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edificacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edificacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edificacao_a
    FOR EACH ROW EXECUTE PROCEDURE loc_edificacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_pto_geod_topo_controle_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_geod_topo_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_geod_topo_controle_p(nomeabrev,geometriaaproximada,tiporef,latitude,longitude,altitudeortometrica,sistemageodesico,referencialaltim,outrarefalt,orgaoenteresp,codponto,obs,geom) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporef,NEW.latitude,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.referencialaltim,NEW.outrarefalt,NEW.orgaoenteresp,NEW.codponto,NEW.obs,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_geod_topo_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_geod_topo_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_geod_topo_controle_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_geod_topo_controle_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_edificacao_p_avoid_multi () RETURNS TRIGGER AS $loc_edificacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edificacao_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edificacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edificacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edificacao_p
    FOR EACH ROW EXECUTE PROCEDURE loc_edificacao_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_bairro_a_avoid_multi () RETURNS TRIGGER AS $lim_bairro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_bairro_a(nome,nomeabrev,geometriaaproximada,geom,anodereferencia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anodereferencia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_bairro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_bairro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_bairro_a
    FOR EACH ROW EXECUTE PROCEDURE lim_bairro_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_terra_publica_a_avoid_multi () RETURNS TRIGGER AS $lim_terra_publica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_publica_a(nome,nomeabrev,geometriaaproximada,geom,classificacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_publica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_publica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_publica_a
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_publica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_limite_intra_munic_adm_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_intra_munic_adm_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_intra_munic_adm_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,tipolimintramun,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolimintramun,NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_intra_munic_adm_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_intra_munic_adm_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_intra_munic_adm_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_intra_munic_adm_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_eclusa_l_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_l(nome,nomeabrev,geometriaaproximada,desnivel,largura,extensao,calado,matconstr,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.desnivel,NEW.largura,NEW.extensao,NEW.calado,NEW.matconstr,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_l
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_atracadouro_l_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_l(nome,nomeabrev,geometriaaproximada,tipoatracad,administracao,matconstr,operacional,situacaofisica,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_barragem_p_avoid_multi () RETURNS TRIGGER AS $hid_barragem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_p(nome,nomeabrev,geometriaaproximada,matconstr,usoprincipal,operacional,situacaofisica,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.matconstr,NEW.usoprincipal,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $eco_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_atracadouro_a_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_a(nome,nomeabrev,geometriaaproximada,tipoatracad,administracao,matconstr,operacional,situacaofisica,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_a
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_eclusa_a_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_a(nome,nomeabrev,geometriaaproximada,desnivel,largura,extensao,calado,matconstr,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.desnivel,NEW.largura,NEW.extensao,NEW.calado,NEW.matconstr,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_a
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_ponto_inicio_drenagem_p_avoid_multi () RETURNS TRIGGER AS $hid_ponto_inicio_drenagem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ponto_inicio_drenagem_p(nome,nomeabrev,geometriaaproximada,relacionado,geom,nascente) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nascente ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ponto_inicio_drenagem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ponto_inicio_drenagem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ponto_inicio_drenagem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ponto_inicio_drenagem_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $eco_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $eco_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_linha_de_limite_l_avoid_multi () RETURNS TRIGGER AS $lim_linha_de_limite_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_linha_de_limite_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_linha_de_limite_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_linha_de_limite_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_linha_de_limite_l
    FOR EACH ROW EXECUTE PROCEDURE lim_linha_de_limite_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $lim_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE lim_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_atracadouro_p_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_p(nome,nomeabrev,geometriaaproximada,tipoatracad,administracao,matconstr,operacional,situacaofisica,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_sumidouro_vertedouro_p_avoid_multi () RETURNS TRIGGER AS $hid_sumidouro_vertedouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_sumidouro_vertedouro_p(nome,nomeabrev,geometriaaproximada,tiposumvert,causa,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiposumvert,NEW.causa,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_sumidouro_vertedouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_sumidouro_vertedouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_sumidouro_vertedouro_p
    FOR EACH ROW EXECUTE PROCEDURE hid_sumidouro_vertedouro_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_limite_politico_adm_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_politico_adm_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_politico_adm_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,tipolimpol,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolimpol,NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_politico_adm_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_politico_adm_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_politico_adm_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_politico_adm_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_confluencia_p_avoid_multi () RETURNS TRIGGER AS $hid_confluencia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_confluencia_p(nome,nomeabrev,geometriaaproximada,relacionado,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_confluencia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_confluencia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_confluencia_p
    FOR EACH ROW EXECUTE PROCEDURE hid_confluencia_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_rodoviaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_rodoviaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_rodoviaria_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifrod,administracao,id_estrut_apoio) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifrod,NEW.administracao,NEW.id_estrut_apoio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_rodoviaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_rodoviaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_rodoviaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_rodoviaria_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_area_abast_agua_a_avoid_multi () RETURNS TRIGGER AS $asb_area_abast_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_area_abast_agua_a(geometriaaproximada,geom,id_complexo_abast_agua) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_abast_agua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_area_abast_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_area_abast_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_area_abast_agua_a
    FOR EACH ROW EXECUTE PROCEDURE asb_area_abast_agua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_condutor_hidrico_l_avoid_multi () RETURNS TRIGGER AS $tra_condutor_hidrico_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_condutor_hidrico_l(nome,nomeabrev,geometriaaproximada,tipotrechoduto,mattransp,setor,posicaorelativa,matconstr,ndutos,situacaoespacial,operacional,situacaofisica,id_duto,geom,tipocondutor,id_complexo_gerad_energ_eletr) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotrechoduto,NEW.mattransp,NEW.setor,NEW.posicaorelativa,NEW.matconstr,NEW.ndutos,NEW.situacaoespacial,NEW.operacional,NEW.situacaofisica,NEW.id_duto,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocondutor,NEW.id_complexo_gerad_energ_eletr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_condutor_hidrico_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_condutor_hidrico_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_condutor_hidrico_l
    FOR EACH ROW EXECUTE PROCEDURE tra_condutor_hidrico_l_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_cemiterio_p_avoid_multi () RETURNS TRIGGER AS $asb_cemiterio_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_cemiterio_p(nome,nomeabrev,geometriaaproximada,tipocemiterio,denominacaoassociada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipocemiterio,NEW.denominacaoassociada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_cemiterio_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_cemiterio_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_cemiterio_p
    FOR EACH ROW EXECUTE PROCEDURE asb_cemiterio_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_outras_unid_protegidas_a_avoid_multi () RETURNS TRIGGER AS $lim_outras_unid_protegidas_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_outras_unid_protegidas_a(nome,nomeabrev,geometriaaproximada,geom,tipooutunidprot,anocriacao,historicomodificacao,sigla,areaoficial,administracao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipooutunidprot,NEW.anocriacao,NEW.historicomodificacao,NEW.sigla,NEW.areaoficial,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_outras_unid_protegidas_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_outras_unid_protegidas_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_outras_unid_protegidas_a
    FOR EACH ROW EXECUTE PROCEDURE lim_outras_unid_protegidas_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponto_hidroviario_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_hidroviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_hidroviario_p(geometriaaproximada,relacionado,geom) SELECT NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_hidroviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_hidroviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_hidroviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_hidroviario_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_rodoviaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_rodoviaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_rodoviaria_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifrod,administracao,id_estrut_apoio) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifrod,NEW.administracao,NEW.id_estrut_apoio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_rodoviaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_rodoviaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_rodoviaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_rodoviaria_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_outras_unid_protegidas_p_avoid_multi () RETURNS TRIGGER AS $lim_outras_unid_protegidas_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_outras_unid_protegidas_p(nome,nomeabrev,geometriaaproximada,geom,tipooutunidprot,anocriacao,historicomodificacao,sigla,areaoficial,administracao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipooutunidprot,NEW.anocriacao,NEW.historicomodificacao,NEW.sigla,NEW.areaoficial,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_outras_unid_protegidas_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_outras_unid_protegidas_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_outras_unid_protegidas_p
    FOR EACH ROW EXECUTE PROCEDURE lim_outras_unid_protegidas_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_cemiterio_a_avoid_multi () RETURNS TRIGGER AS $asb_cemiterio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_cemiterio_a(nome,nomeabrev,geometriaaproximada,tipocemiterio,denominacaoassociada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipocemiterio,NEW.denominacaoassociada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_cemiterio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_cemiterio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_cemiterio_a
    FOR EACH ROW EXECUTE PROCEDURE asb_cemiterio_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_comporta_p_avoid_multi () RETURNS TRIGGER AS $hid_comporta_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_comporta_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_comporta_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_comporta_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_comporta_p
    FOR EACH ROW EXECUTE PROCEDURE hid_comporta_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_trecho_ferroviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_ferroviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_ferroviario_l(nome,nomeabrev,geometriaaproximada,codtrechoferrov,posicaorelativa,tipotrechoferrov,bitola,eletrificada,nrlinhas,emarruamento,jurisdicao,administracao,concessionaria,operacional,situacaofisica,cargasuportmaxima,id_via_ferrea,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.codtrechoferrov,NEW.posicaorelativa,NEW.tipotrechoferrov,NEW.bitola,NEW.eletrificada,NEW.nrlinhas,NEW.emarruamento,NEW.jurisdicao,NEW.administracao,NEW.concessionaria,NEW.operacional,NEW.situacaofisica,NEW.cargasuportmaxima,NEW.id_via_ferrea,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_ferroviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_ferroviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_ferroviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_ferroviario_l_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_vila_p_avoid_multi () RETURNS TRIGGER AS $loc_vila_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_vila_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_vila_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_vila_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_vila_p
    FOR EACH ROW EXECUTE PROCEDURE loc_vila_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_comporta_l_avoid_multi () RETURNS TRIGGER AS $hid_comporta_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_comporta_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_comporta_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_comporta_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_comporta_l
    FOR EACH ROW EXECUTE PROCEDURE hid_comporta_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_constr_portuaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_portuaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_portuaria_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifport,administracao,id_complexo_portuario) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifport,NEW.administracao,NEW.id_complexo_portuario ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_portuaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_portuaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_portuaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_portuaria_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_trecho_drenagem_l_avoid_multi () RETURNS TRIGGER AS $hid_trecho_drenagem_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_trecho_drenagem_l(nome,nomeabrev,geometriaaproximada,coincidecomdentrode,dentrodepoligono,compartilhado,eixoprincipal,navegabilidade,caladomax,regime,larguramedia,velocidademedcorrente,profundidademedia,id_trecho_curso_dagua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.coincidecomdentrode,NEW.dentrodepoligono,NEW.compartilhado,NEW.eixoprincipal,NEW.navegabilidade,NEW.caladomax,NEW.regime,NEW.larguramedia,NEW.velocidademedcorrente,NEW.profundidademedia,NEW.id_trecho_curso_dagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_trecho_drenagem_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_trecho_drenagem_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_trecho_drenagem_l
    FOR EACH ROW EXECUTE PROCEDURE hid_trecho_drenagem_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_constr_portuaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_portuaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_portuaria_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifport,administracao,id_complexo_portuario) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifport,NEW.administracao,NEW.id_complexo_portuario ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_portuaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_portuaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_portuaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_portuaria_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_travessia_l_avoid_multi () RETURNS TRIGGER AS $tra_travessia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_l(nome,nomeabrev,geometriaaproximada,tipotravessia,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotravessia,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_l
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_travessia_p_avoid_multi () RETURNS TRIGGER AS $tra_travessia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_p(nome,nomeabrev,geometriaaproximada,tipotravessia,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotravessia,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_p
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_area_duto_a_avoid_multi () RETURNS TRIGGER AS $tra_area_duto_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_area_duto_a(geometriaaproximada,geom) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_area_duto_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_area_duto_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_area_duto_a
    FOR EACH ROW EXECUTE PROCEDURE tra_area_duto_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_plataforma_a_avoid_multi () RETURNS TRIGGER AS $eco_plataforma_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_plataforma_a(nome,nomeabrev,geometriaaproximada,tipoplataforma,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoplataforma,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_plataforma_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_plataforma_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_plataforma_a
    FOR EACH ROW EXECUTE PROCEDURE eco_plataforma_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_plataforma_p_avoid_multi () RETURNS TRIGGER AS $eco_plataforma_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_plataforma_p(nome,nomeabrev,geometriaaproximada,tipoplataforma,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoplataforma,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_plataforma_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_plataforma_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_plataforma_p
    FOR EACH ROW EXECUTE PROCEDURE eco_plataforma_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_torre_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_torre_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_torre_energia_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,ovgd,alturaestimada,tipotorre,arranjofases,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.ovgd,NEW.alturaestimada,NEW.tipotorre,NEW.arranjofases,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_torre_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_torre_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_torre_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_torre_energia_p_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_pto_est_med_fenomenos_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_est_med_fenomenos_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_est_med_fenomenos_p(nome,geometriaaproximada,tipoptoestmed,codestacao,orgaoenteresp,id_est_med_fenomenos,geom) SELECT NEW.nome,NEW.geometriaaproximada,NEW.tipoptoestmed,NEW.codestacao,NEW.orgaoenteresp,NEW.id_est_med_fenomenos,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_est_med_fenomenos_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_est_med_fenomenos_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_est_med_fenomenos_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_est_med_fenomenos_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_const_lazer_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_lazer_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_lazer_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoediflazer,id_complexo_lazer) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoediflazer,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_lazer_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_lazer_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_lazer_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_lazer_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_deposito_geral_a_avoid_multi () RETURNS TRIGGER AS $eco_deposito_geral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_deposito_geral_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipodepgeral,matconstr,tipoexposicao,tipoprodutoresiduo,tipoconteudo,unidadevolume,valorvolume,tratamento,id_org_comerc_serv,id_org_ext_mineral,id_org_agrop_ext_veg_pesca,id_complexo_gerad_energ_eletr,id_estrut_transporte,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipodepgeral,NEW.matconstr,NEW.tipoexposicao,NEW.tipoprodutoresiduo,NEW.tipoconteudo,NEW.unidadevolume,NEW.valorvolume,NEW.tratamento,NEW.id_org_comerc_serv,NEW.id_org_ext_mineral,NEW.id_org_agrop_ext_veg_pesca,NEW.id_complexo_gerad_energ_eletr,NEW.id_estrut_transporte,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_deposito_geral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_deposito_geral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_deposito_geral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_deposito_geral_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponto_ferroviario_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_ferroviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_ferroviario_p(geometriaaproximada,relacionado,geom) SELECT NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_ferroviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_ferroviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_ferroviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_ferroviario_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_const_lazer_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_lazer_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_lazer_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoediflazer,id_complexo_lazer) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoediflazer,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_lazer_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_lazer_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_lazer_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_lazer_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_deposito_geral_p_avoid_multi () RETURNS TRIGGER AS $eco_deposito_geral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_deposito_geral_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipodepgeral,matconstr,tipoexposicao,tipoprodutoresiduo,tipoconteudo,unidadevolume,valorvolume,tratamento,id_org_comerc_serv,id_org_ext_mineral,id_org_agrop_ext_veg_pesca,id_complexo_gerad_energ_eletr,id_estrut_transporte,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipodepgeral,NEW.matconstr,NEW.tipoexposicao,NEW.tipoprodutoresiduo,NEW.tipoconteudo,NEW.unidadevolume,NEW.valorvolume,NEW.tratamento,NEW.id_org_comerc_serv,NEW.id_org_ext_mineral,NEW.id_org_agrop_ext_veg_pesca,NEW.id_complexo_gerad_energ_eletr,NEW.id_estrut_transporte,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_deposito_geral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_deposito_geral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_deposito_geral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_deposito_geral_p_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_area_servico_social_a_avoid_multi () RETURNS TRIGGER AS $sau_area_servico_social_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_area_servico_social_a(geometriaaproximada,id_org_servico_social,geom) SELECT NEW.geometriaaproximada,NEW.id_org_servico_social,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_area_servico_social_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_area_servico_social_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_area_servico_social_a
    FOR EACH ROW EXECUTE PROCEDURE sau_area_servico_social_a_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_posto_fiscal_a_avoid_multi () RETURNS TRIGGER AS $adm_posto_fiscal_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_fiscal_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipopostofisc,id_org_pub_civil,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipopostofisc,NEW.id_org_pub_civil,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_fiscal_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_fiscal_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_fiscal_a
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_fiscal_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_duna_p_avoid_multi () RETURNS TRIGGER AS $rel_duna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_duna_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,fixa) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.fixa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_duna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_duna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_duna_p
    FOR EACH ROW EXECUTE PROCEDURE rel_duna_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_marco_de_limite_p_avoid_multi () RETURNS TRIGGER AS $lim_marco_de_limite_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_marco_de_limite_p(nome,nomeabrev,geometriaaproximada,tipomarcolim,latitude_gms,latitude,longitude_gms,longitude,altitudeortometrica,sistemageodesico,outrarefplan,referencialaltim,outrarefalt,orgresp,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipomarcolim,NEW.latitude_gms,NEW.latitude,NEW.longitude_gms,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.outrarefplan,NEW.referencialaltim,NEW.outrarefalt,NEW.orgresp,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_marco_de_limite_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_marco_de_limite_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_marco_de_limite_p
    FOR EACH ROW EXECUTE PROCEDURE lim_marco_de_limite_p_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_duna_a_avoid_multi () RETURNS TRIGGER AS $rel_duna_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_duna_a(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,fixa) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.fixa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_duna_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_duna_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_duna_a
    FOR EACH ROW EXECUTE PROCEDURE rel_duna_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_arruamento_l_avoid_multi () RETURNS TRIGGER AS $tra_arruamento_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_arruamento_l(nome,nomeabrev,geometriaaproximada,revestimento,operacional,situacaofisica,nrfaixas,trafego,canteirodivisorio,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.revestimento,NEW.operacional,NEW.situacaofisica,NEW.nrfaixas,NEW.trafego,NEW.canteirodivisorio,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_arruamento_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_arruamento_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_arruamento_l
    FOR EACH ROW EXECUTE PROCEDURE tra_arruamento_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_recife_a_avoid_multi () RETURNS TRIGGER AS $hid_recife_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_a(nome,nomeabrev,geometriaaproximada,tiporecife,situamare,situacaocosta,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporecife,NEW.situamare,NEW.situacaocosta,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_a
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_recife_l_avoid_multi () RETURNS TRIGGER AS $hid_recife_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_l(nome,nomeabrev,geometriaaproximada,tiporecife,situamare,situacaocosta,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporecife,NEW.situamare,NEW.situacaocosta,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_l
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_recife_p_avoid_multi () RETURNS TRIGGER AS $hid_recife_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_p(nome,nomeabrev,geometriaaproximada,tiporecife,situamare,situacaocosta,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporecife,NEW.situamare,NEW.situacaocosta,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_p
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_pais_a_avoid_multi () RETURNS TRIGGER AS $lim_pais_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_pais_a(nome,nomeabrev,geometriaaproximada,geom,sigla,codiso3166) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.sigla,NEW.codiso3166 ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_pais_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_pais_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_pais_a
    FOR EACH ROW EXECUTE PROCEDURE lim_pais_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_curva_batimetrica_l_avoid_multi () RETURNS TRIGGER AS $rel_curva_batimetrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_curva_batimetrica_l(profundidade,geom) SELECT NEW.profundidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_curva_batimetrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_curva_batimetrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_curva_batimetrica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_curva_batimetrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_ponto_cotado_batimetrico_p_avoid_multi () RETURNS TRIGGER AS $rel_ponto_cotado_batimetrico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_ponto_cotado_batimetrico_p(profundidade,geom) SELECT NEW.profundidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_ponto_cotado_batimetrico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_ponto_cotado_batimetrico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_ponto_cotado_batimetrico_p
    FOR EACH ROW EXECUTE PROCEDURE rel_ponto_cotado_batimetrico_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_dep_abast_agua_p_avoid_multi () RETURNS TRIGGER AS $asb_dep_abast_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_abast_agua_p(nome,nomeabrev,geometriaaproximada,tipodepabast,situacaoagua,construcao,matconstr,finalidade,situacaofisica,operacional,id_complexo_abast_agua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepabast,NEW.situacaoagua,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.situacaofisica,NEW.operacional,NEW.id_complexo_abast_agua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_abast_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_abast_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_abast_agua_p
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_abast_agua_p_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_gruta_caverna_p_avoid_multi () RETURNS TRIGGER AS $rel_gruta_caverna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_gruta_caverna_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tipogrutacaverna) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipogrutacaverna ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_gruta_caverna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_gruta_caverna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_gruta_caverna_p
    FOR EACH ROW EXECUTE PROCEDURE rel_gruta_caverna_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_dep_abast_agua_a_avoid_multi () RETURNS TRIGGER AS $asb_dep_abast_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_abast_agua_a(nome,nomeabrev,geometriaaproximada,tipodepabast,situacaoagua,construcao,matconstr,finalidade,situacaofisica,operacional,id_complexo_abast_agua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepabast,NEW.situacaoagua,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.situacaofisica,NEW.operacional,NEW.id_complexo_abast_agua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_abast_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_abast_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_abast_agua_a
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_abast_agua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_caatinga_a_avoid_multi () RETURNS TRIGGER AS $veg_caatinga_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_caatinga_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_caatinga_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_caatinga_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_caatinga_a
    FOR EACH ROW EXECUTE PROCEDURE veg_caatinga_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_dep_saneamento_a_avoid_multi () RETURNS TRIGGER AS $asb_dep_saneamento_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_saneamento_a(nome,nomeabrev,geometriaaproximada,tipodepsaneam,construcao,matconstr,finalidade,operacional,situacaofisica,residuo,tiporesiduo,id_complexo_saneamento,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepsaneam,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.operacional,NEW.situacaofisica,NEW.residuo,NEW.tiporesiduo,NEW.id_complexo_saneamento,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_saneamento_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_saneamento_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_saneamento_a
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_saneamento_a_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $sau_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE sau_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_edif_habitacional_p_avoid_multi () RETURNS TRIGGER AS $loc_edif_habitacional_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edif_habitacional_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,id_complexo_habitacional) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_habitacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edif_habitacional_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edif_habitacional_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edif_habitacional_p
    FOR EACH ROW EXECUTE PROCEDURE loc_edif_habitacional_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_galeria_bueiro_p_avoid_multi () RETURNS TRIGGER AS $tra_galeria_bueiro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_galeria_bueiro_p(nome,nomeabrev,matconstr,pesosuportmaximo,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.matconstr,NEW.pesosuportmaximo,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_galeria_bueiro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_galeria_bueiro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_galeria_bueiro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_galeria_bueiro_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_politico_adm_a_avoid_multi () RETURNS TRIGGER AS $lim_area_politico_adm_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_politico_adm_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_politico_adm_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_politico_adm_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_politico_adm_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_politico_adm_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_edif_habitacional_a_avoid_multi () RETURNS TRIGGER AS $loc_edif_habitacional_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edif_habitacional_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,id_complexo_habitacional) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_habitacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edif_habitacional_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edif_habitacional_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edif_habitacional_a
    FOR EACH ROW EXECUTE PROCEDURE loc_edif_habitacional_a_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $sau_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE sau_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_area_ensino_a_avoid_multi () RETURNS TRIGGER AS $edu_area_ensino_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_ensino_a(geometriaaproximada,geom,id_org_ensino) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_ensino ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_ensino_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_ensino_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_ensino_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_ensino_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_fundeadouro_p_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_p(nome,nomeabrev,geometriaaproximada,destinacaofundeadouro,administracao,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.destinacaofundeadouro,NEW.administracao,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_agrop_ext_veg_pesca_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_agrop_ext_veg_pesca_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifagropec,id_org_agrop_ext_veg_pesca) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifagropec,NEW.id_org_agrop_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_agrop_ext_veg_pesca_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_agrop_ext_veg_pesca_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_constr_aeroportuaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_aeroportuaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_aeroportuaria_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifaero,administracao,id_complexo_aeroportuario) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifaero,NEW.administracao,NEW.id_complexo_aeroportuario ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_aeroportuaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_aeroportuaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_aeroportuaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_aeroportuaria_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_area_ruinas_a_avoid_multi () RETURNS TRIGGER AS $edu_area_ruinas_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_ruinas_a(geometriaaproximada,geom,id_complexo_lazer) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_ruinas_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_ruinas_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_ruinas_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_ruinas_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_fundeadouro_l_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_l(nome,nomeabrev,geometriaaproximada,destinacaofundeadouro,administracao,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.destinacaofundeadouro,NEW.administracao,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_l_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_agrop_ext_veg_pesca_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_agrop_ext_veg_pesca_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifagropec,id_org_agrop_ext_veg_pesca) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifagropec,NEW.id_org_agrop_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_agrop_ext_veg_pesca_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_agrop_ext_veg_pesca_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_fundeadouro_a_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_a(nome,nomeabrev,geometriaaproximada,destinacaofundeadouro,administracao,id_complexo_portuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.destinacaofundeadouro,NEW.administracao,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_a
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_constr_aeroportuaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_aeroportuaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_aeroportuaria_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifaero,administracao,id_complexo_aeroportuario) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifaero,NEW.administracao,NEW.id_complexo_aeroportuario ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_aeroportuaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_aeroportuaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_aeroportuaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_aeroportuaria_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_de_litigio_a_avoid_multi () RETURNS TRIGGER AS $lim_area_de_litigio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_de_litigio_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_de_litigio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_de_litigio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_de_litigio_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_de_litigio_a_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_edif_constr_est_med_fen_p_avoid_multi () RETURNS TRIGGER AS $pto_edif_constr_est_med_fen_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_edif_constr_est_med_fen_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_edif_constr_est_med_fen_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_edif_constr_est_med_fen_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_edif_constr_est_med_fen_p
    FOR EACH ROW EXECUTE PROCEDURE pto_edif_constr_est_med_fen_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_area_edificada_a_avoid_multi () RETURNS TRIGGER AS $loc_area_edificada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_edificada_a(nome,nomeabrev,geom) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_edificada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_edificada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_edificada_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_edificada_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_terra_publica_p_avoid_multi () RETURNS TRIGGER AS $lim_terra_publica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_publica_p(nome,nomeabrev,geometriaaproximada,geom,classificacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_publica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_publica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_publica_p
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_publica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_dep_saneamento_p_avoid_multi () RETURNS TRIGGER AS $asb_dep_saneamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_saneamento_p(nome,nomeabrev,geometriaaproximada,tipodepsaneam,construcao,matconstr,finalidade,operacional,situacaofisica,residuo,tiporesiduo,id_complexo_saneamento,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepsaneam,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.operacional,NEW.situacaofisica,NEW.residuo,NEW.tiporesiduo,NEW.id_complexo_saneamento,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_saneamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_saneamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_saneamento_p
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_saneamento_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_caminho_aereo_l_avoid_multi () RETURNS TRIGGER AS $tra_caminho_aereo_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_caminho_aereo_l(nome,nomeabrev,geometriaaproximada,tipocaminhoaereo,tipousocaminhoaer,operacional,situacaofisica,geom,id_org_ext_mineral) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipocaminhoaereo,NEW.tipousocaminhoaer,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_ext_mineral ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_caminho_aereo_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_caminho_aereo_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_caminho_aereo_l
    FOR EACH ROW EXECUTE PROCEDURE tra_caminho_aereo_l_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_ext_mineral_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_ext_mineral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_ext_mineral_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipodivisaocnae,id_org_ext_mineral) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipodivisaocnae,NEW.id_org_ext_mineral ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_ext_mineral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_ext_mineral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_ext_mineral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_ext_mineral_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ciclovia_l_avoid_multi () RETURNS TRIGGER AS $tra_ciclovia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ciclovia_l(nome,nomeabrev,geometriaaproximada,administracao,revestimento,operacional,situacaofisica,trafego,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.administracao,NEW.revestimento,NEW.operacional,NEW.situacaofisica,NEW.trafego,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ciclovia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ciclovia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ciclovia_l
    FOR EACH ROW EXECUTE PROCEDURE tra_ciclovia_l_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_area_urbana_isolada_a_avoid_multi () RETURNS TRIGGER AS $loc_area_urbana_isolada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_urbana_isolada_a(geometriaaproximada,nome,nomeabrev,tipoassociado,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.tipoassociado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_urbana_isolada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_urbana_isolada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_urbana_isolada_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_urbana_isolada_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_ponto_cotado_altimetrico_p_avoid_multi () RETURNS TRIGGER AS $rel_ponto_cotado_altimetrico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_ponto_cotado_altimetrico_p(geometriaaproximada,cotacomprovada,cota,geom) SELECT NEW.geometriaaproximada,NEW.cotacomprovada,NEW.cota,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_ponto_cotado_altimetrico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_ponto_cotado_altimetrico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_ponto_cotado_altimetrico_p
    FOR EACH ROW EXECUTE PROCEDURE rel_ponto_cotado_altimetrico_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponto_duto_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_duto_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_duto_p(geom,geometriaaproximada,relacionado) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.relacionado ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_duto_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_duto_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_duto_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_duto_p_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_area_pub_civil_a_avoid_multi () RETURNS TRIGGER AS $adm_area_pub_civil_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_area_pub_civil_a(geometriaaproximada,geom,id_org_pub_civil) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_pub_civil ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_area_pub_civil_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_area_pub_civil_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_area_pub_civil_a
    FOR EACH ROW EXECUTE PROCEDURE adm_area_pub_civil_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_regiao_administrativa_a_avoid_multi () RETURNS TRIGGER AS $lim_regiao_administrativa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_regiao_administrativa_a(nome,nomeabrev,geometriaaproximada,geom,anodereferencia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anodereferencia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_regiao_administrativa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_regiao_administrativa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_regiao_administrativa_a
    FOR EACH ROW EXECUTE PROCEDURE lim_regiao_administrativa_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $loc_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $loc_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_posto_combustivel_a_avoid_multi () RETURNS TRIGGER AS $tra_posto_combustivel_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_posto_combustivel_a(nome,nomeabrev,geometriaaproximada,administracao,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_posto_combustivel_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_posto_combustivel_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_posto_combustivel_a
    FOR EACH ROW EXECUTE PROCEDURE tra_posto_combustivel_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_edif_energia_a_avoid_multi () RETURNS TRIGGER AS $enc_edif_energia_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_energia_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifenergia,id_complexo_gerad_energ_eletr,id_subestacao_ener_eletr) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifenergia,NEW.id_complexo_gerad_energ_eletr,NEW.id_subestacao_ener_eletr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_energia_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_energia_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_energia_a
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_energia_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $loc_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_edif_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_edif_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_energia_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifenergia,id_complexo_gerad_energ_eletr,id_subestacao_ener_eletr) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifenergia,NEW.id_complexo_gerad_energ_eletr,NEW.id_subestacao_ener_eletr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_energia_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_posto_combustivel_p_avoid_multi () RETURNS TRIGGER AS $tra_posto_combustivel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_posto_combustivel_p(nome,nomeabrev,geometriaaproximada,administracao,operacional,situacaofisica,matconstr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_posto_combustivel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_posto_combustivel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_posto_combustivel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_posto_combustivel_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_bacia_hidrografica_a_avoid_multi () RETURNS TRIGGER AS $hid_bacia_hidrografica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_bacia_hidrografica_a(nome,nomeabrev,geometriaaproximada,codigootto,nivelotto,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.codigootto,NEW.nivelotto,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_bacia_hidrografica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_bacia_hidrografica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_bacia_hidrografica_a
    FOR EACH ROW EXECUTE PROCEDURE hid_bacia_hidrografica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_veg_area_contato_a_avoid_multi () RETURNS TRIGGER AS $veg_veg_area_contato_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_veg_area_contato_a(nome,nomeabrev,classificacaoporte,denso,alturamediaindividuos,antropizada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.classificacaoporte,NEW.denso,NEW.alturamediaindividuos,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_veg_area_contato_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_veg_area_contato_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_veg_area_contato_a
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_area_contato_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_uso_comunitario_p_avoid_multi () RETURNS TRIGGER AS $lim_area_uso_comunitario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_uso_comunitario_p(nome,nomeabrev,geometriaaproximada,geom,tipoareausocomun) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoareausocomun ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_uso_comunitario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_uso_comunitario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_uso_comunitario_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_uso_comunitario_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_floresta_a_avoid_multi () RETURNS TRIGGER AS $veg_floresta_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_floresta_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,especiepredominante,caracteristicafloresta,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.especiepredominante,NEW.caracteristicafloresta,NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_floresta_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_floresta_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_floresta_a
    FOR EACH ROW EXECUTE PROCEDURE veg_floresta_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_uso_comunitario_a_avoid_multi () RETURNS TRIGGER AS $lim_area_uso_comunitario_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_uso_comunitario_a(nome,nomeabrev,geometriaaproximada,geom,tipoareausocomun) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoareausocomun ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_uso_comunitario_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_uso_comunitario_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_uso_comunitario_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_uso_comunitario_a_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $adm_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE adm_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_especial_p_avoid_multi () RETURNS TRIGGER AS $lim_area_especial_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_especial_p(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_especial_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_especial_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_especial_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_especial_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_travessia_pedestre_l_avoid_multi () RETURNS TRIGGER AS $tra_travessia_pedestre_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_pedestre_l(nome,nomeabrev,geometriaaproximada,tipotravessiaped,matconstr,operacional,situacaofisica,largura,extensao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotravessiaped,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_pedestre_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_pedestre_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_pedestre_l
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_pedestre_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_especial_a_avoid_multi () RETURNS TRIGGER AS $lim_area_especial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_especial_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_especial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_especial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_especial_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_especial_a_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $adm_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE adm_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_aglom_rural_de_ext_urbana_p_avoid_multi () RETURNS TRIGGER AS $loc_aglom_rural_de_ext_urbana_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglom_rural_de_ext_urbana_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglom_rural_de_ext_urbana_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglom_rural_de_ext_urbana_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglom_rural_de_ext_urbana_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglom_rural_de_ext_urbana_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_travessia_pedestre_p_avoid_multi () RETURNS TRIGGER AS $tra_travessia_pedestre_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_pedestre_p(nome,nomeabrev,geometriaaproximada,tipotravessiaped,matconstr,operacional,situacaofisica,largura,extensao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotravessiaped,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_pedestre_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_pedestre_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_pedestre_p
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_pedestre_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_uso_sustentavel_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_uso_sustentavel_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_uso_sustentavel_a(nome,nomeabrev,geometriaaproximada,geom,anocriacao,sigla,areaoficialha,atolegal,administracao,tipounidusosust) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.sigla,NEW.areaoficialha,NEW.atolegal,NEW.administracao,NEW.tipounidusosust ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_uso_sustentavel_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_uso_sustentavel_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_uso_sustentavel_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_uso_sustentavel_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_ponto_rodoviario_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_rodoviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_rodoviario_p(geometriaaproximada,relacionado,geom) SELECT NEW.geometriaaproximada,NEW.relacionado,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_rodoviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_rodoviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_rodoviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_rodoviario_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_uso_sustentavel_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_uso_sustentavel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_uso_sustentavel_p(nome,nomeabrev,geometriaaproximada,geom,anocriacao,sigla,areaoficialha,atolegal,administracao,tipounidusosust) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.sigla,NEW.areaoficialha,NEW.atolegal,NEW.administracao,NEW.tipounidusosust ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_uso_sustentavel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_uso_sustentavel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_uso_sustentavel_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_uso_sustentavel_p_avoid_multi ();
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_area_construida_a_avoid_multi () RETURNS TRIGGER AS $loc_area_construida_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_construida_a(nome,nomeabrev,geom) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_construida_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_construida_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_construida_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_construida_a_avoid_multi ();
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_protecao_integral_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_protecao_integral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_protecao_integral_p(nome,nomeabrev,geometriaaproximada,geom,anocriacao,areaoficial,atolegal,administracao,tipounidprotinteg) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.areaoficial,NEW.atolegal,NEW.administracao,NEW.tipounidprotinteg ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_protecao_integral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_protecao_integral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_protecao_integral_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_protecao_integral_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_area_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_area_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_ext_mineral_a(geom,geometriaaproximada,id_org_ext_mineral) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.id_org_ext_mineral ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_ext_mineral_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_protecao_integral_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_protecao_integral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_protecao_integral_a(nome,nomeabrev,geometriaaproximada,geom,anocriacao,areaoficial,atolegal,administracao,tipounidprotinteg) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.areaoficial,NEW.atolegal,NEW.administracao,NEW.tipounidprotinteg ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_protecao_integral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_protecao_integral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_protecao_integral_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_protecao_integral_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_natureza_fundo_p_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_p(nome,nomeabrev,geometriaaproximada,materialpredominante,espessalgas,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.materialpredominante,NEW.espessalgas,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_p
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_a_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_a(nome,nomeabrev,geometriaaproximada,tipopista,revestimento,usopista,homologacao,operacional,situacaofisica,largura,extensao,id_complexo_aeroportuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopista,NEW.revestimento,NEW.usopista,NEW.homologacao,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao,NEW.id_complexo_aeroportuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_a
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $hid_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE hid_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_patio_p_avoid_multi () RETURNS TRIGGER AS $tra_patio_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_patio_p(nome,nomeabrev,geometriaaproximada,modaluso,administracao,operacional,situacaofisica,id_estrut_transporte,id_org_ext_mineral,id_org_comerc_serv,id_org_industrial,id_org_ensino,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.modaluso,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,NEW.id_org_ext_mineral,NEW.id_org_comerc_serv,NEW.id_org_industrial,NEW.id_org_ensino,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_patio_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_patio_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_patio_p
    FOR EACH ROW EXECUTE PROCEDURE tra_patio_p_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_dolina_a_avoid_multi () RETURNS TRIGGER AS $rel_dolina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_dolina_a(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_dolina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_dolina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_dolina_a
    FOR EACH ROW EXECUTE PROCEDURE rel_dolina_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_l_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_l(nome,nomeabrev,geometriaaproximada,tipopista,revestimento,usopista,homologacao,operacional,situacaofisica,largura,extensao,id_complexo_aeroportuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopista,NEW.revestimento,NEW.usopista,NEW.homologacao,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao,NEW.id_complexo_aeroportuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_l
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_natureza_fundo_a_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_a(nome,nomeabrev,geometriaaproximada,materialpredominante,espessalgas,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.materialpredominante,NEW.espessalgas,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_a
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_p_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_p(nome,nomeabrev,geometriaaproximada,tipopista,revestimento,usopista,homologacao,operacional,situacaofisica,largura,extensao,id_complexo_aeroportuario,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopista,NEW.revestimento,NEW.usopista,NEW.homologacao,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao,NEW.id_complexo_aeroportuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_p
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_patio_a_avoid_multi () RETURNS TRIGGER AS $tra_patio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_patio_a(nome,nomeabrev,geometriaaproximada,modaluso,administracao,operacional,situacaofisica,id_estrut_transporte,id_org_ext_mineral,id_org_comerc_serv,id_org_industrial,id_org_ensino,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.modaluso,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,NEW.id_org_ext_mineral,NEW.id_org_comerc_serv,NEW.id_org_industrial,NEW.id_org_ensino,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_patio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_patio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_patio_a
    FOR EACH ROW EXECUTE PROCEDURE tra_patio_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $hid_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE hid_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $lim_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE lim_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_dolina_p_avoid_multi () RETURNS TRIGGER AS $rel_dolina_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_dolina_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_dolina_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_dolina_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_dolina_p
    FOR EACH ROW EXECUTE PROCEDURE rel_dolina_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_pista_competicao_l_avoid_multi () RETURNS TRIGGER AS $edu_pista_competicao_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_pista_competicao_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipopista,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipopista,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_pista_competicao_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_pista_competicao_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_pista_competicao_l
    FOR EACH ROW EXECUTE PROCEDURE edu_pista_competicao_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_ilha_p_avoid_multi () RETURNS TRIGGER AS $hid_ilha_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tipoilha) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoilha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_area_industrial_a_avoid_multi () RETURNS TRIGGER AS $eco_area_industrial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_industrial_a(geometriaaproximada,id_org_industrial,geom) SELECT NEW.geometriaaproximada,NEW.id_org_industrial,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_industrial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_industrial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_industrial_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_industrial_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_ilha_l_avoid_multi () RETURNS TRIGGER AS $hid_ilha_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_l(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tipoilha) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoilha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_l
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_l_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_area_religiosa_a_avoid_multi () RETURNS TRIGGER AS $edu_area_religiosa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_religiosa_a(geometriaaproximada,geom,id_org_religiosa) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_religiosa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_religiosa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_religiosa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_religiosa_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_religiosa_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_ilha_a_avoid_multi () RETURNS TRIGGER AS $hid_ilha_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_a(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tipoilha) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoilha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_a
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_barragem_a_avoid_multi () RETURNS TRIGGER AS $hid_barragem_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_a(nome,nomeabrev,geometriaaproximada,matconstr,usoprincipal,operacional,situacaofisica,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.matconstr,NEW.usoprincipal,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_a
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_a_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_area_saude_a_avoid_multi () RETURNS TRIGGER AS $sau_area_saude_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_area_saude_a(geometriaaproximada,geom,id_org_saude) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_saude ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_area_saude_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_area_saude_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_area_saude_a
    FOR EACH ROW EXECUTE PROCEDURE sau_area_saude_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_barragem_l_avoid_multi () RETURNS TRIGGER AS $hid_barragem_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_l(nome,nomeabrev,geometriaaproximada,matconstr,usoprincipal,operacional,situacaofisica,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.matconstr,NEW.usoprincipal,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_l
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_outros_limites_oficiais_l_avoid_multi () RETURNS TRIGGER AS $lim_outros_limites_oficiais_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_outros_limites_oficiais_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,tipooutlimofic,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipooutlimofic,NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_outros_limites_oficiais_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_outros_limites_oficiais_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_outros_limites_oficiais_l
    FOR EACH ROW EXECUTE PROCEDURE lim_outros_limites_oficiais_l_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_edif_pub_militar_a_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_militar_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_militar_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifmil,tipousoedif,id_org_pub_militar) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifmil,NEW.tipousoedif,NEW.id_org_pub_militar ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_militar_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_militar_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_militar_a
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_militar_a_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_area_agrop_ext_veg_pesca_a_avoid_multi () RETURNS TRIGGER AS $eco_area_agrop_ext_veg_pesca_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_agrop_ext_veg_pesca_a(geometriaaproximada,destinadoa,id_org_agropec_ext_veg_pesca,geom) SELECT NEW.geometriaaproximada,NEW.destinadoa,NEW.id_org_agropec_ext_veg_pesca,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_agrop_ext_veg_pesca_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_agrop_ext_veg_pesca_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_agrop_ext_veg_pesca_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_agrop_ext_veg_pesca_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_eclusa_p_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_p(nome,nomeabrev,geometriaaproximada,desnivel,largura,extensao,calado,matconstr,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.desnivel,NEW.largura,NEW.extensao,NEW.calado,NEW.matconstr,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_p
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_limite_particular_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_particular_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_particular_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_particular_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_particular_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_particular_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_particular_l_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_edif_pub_militar_p_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_militar_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_militar_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipousoedif,tipoedifmil,id_org_pub_militar) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipousoedif,NEW.tipoedifmil,NEW.id_org_pub_militar ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_militar_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_militar_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_militar_p
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_militar_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $enc_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE enc_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_trecho_hidroviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_hidroviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_hidroviario_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,regime,extensaotrecho,caladomaxseca,geom,id_hidrovia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.regime,NEW.extensaotrecho,NEW.caladomaxseca,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_hidrovia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_hidroviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_hidroviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_hidroviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_hidroviario_l_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_veg_cultivada_a_avoid_multi () RETURNS TRIGGER AS $veg_veg_cultivada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_veg_cultivada_a(nome,nomeabrev,geometriaaproximada,tipolavoura,finalidade,terreno,classificacaoporte,espacamentoindividuos,espessuradap,denso,alturamediaindividuos,cultivopredominante,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipolavoura,NEW.finalidade,NEW.terreno,NEW.classificacaoporte,NEW.espacamentoindividuos,NEW.espessuradap,NEW.denso,NEW.alturamediaindividuos,NEW.cultivopredominante,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_veg_cultivada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_veg_cultivada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_veg_cultivada_a
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_cultivada_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_identific_trecho_rod_p_avoid_multi () RETURNS TRIGGER AS $tra_identific_trecho_rod_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_identific_trecho_rod_p(nome,nomeabrev,sigla,geom,id_via_rodoviaria) SELECT NEW.nome,NEW.nomeabrev,NEW.sigla,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_via_rodoviaria ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_identific_trecho_rod_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_identific_trecho_rod_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_identific_trecho_rod_p
    FOR EACH ROW EXECUTE PROCEDURE tra_identific_trecho_rod_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $enc_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_curva_nivel_l_avoid_multi () RETURNS TRIGGER AS $rel_curva_nivel_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_curva_nivel_l(geometriaaproximada,cota,depressao,indice,geom) SELECT NEW.geometriaaproximada,NEW.cota,NEW.depressao,NEW.indice,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_curva_nivel_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_curva_nivel_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_curva_nivel_l
    FOR EACH ROW EXECUTE PROCEDURE rel_curva_nivel_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_trecho_massa_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_trecho_massa_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_trecho_massa_dagua_a(nome,nomeabrev,tipotrechomassa,regime,salinidade,id_trecho_curso_dagua,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.tipotrechomassa,NEW.regime,NEW.salinidade,NEW.id_trecho_curso_dagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_trecho_massa_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_trecho_massa_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_trecho_massa_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_trecho_massa_dagua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_reservatorio_hidrico_a_avoid_multi () RETURNS TRIGGER AS $hid_reservatorio_hidrico_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_reservatorio_hidrico_a(nome,nomeabrev,geometriaaproximada,usoprincipal,volumeutil,namaximomaximorum,namaximooperacional,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.usoprincipal,NEW.volumeutil,NEW.namaximomaximorum,NEW.namaximooperacional,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_reservatorio_hidrico_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_reservatorio_hidrico_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_reservatorio_hidrico_a
    FOR EACH ROW EXECUTE PROCEDURE hid_reservatorio_hidrico_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_antena_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_antena_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_antena_comunic_p(nome,nomeabrev,geometriaaproximada,geom,id_complexo_comunicacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_comunicacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_antena_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_antena_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_antena_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_antena_comunic_p_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_edif_servico_social_p_avoid_multi () RETURNS TRIGGER AS $sau_edif_servico_social_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_servico_social_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,id_org_servico_social) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.id_org_servico_social ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_servico_social_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_servico_social_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_servico_social_p
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_servico_social_p_avoid_multi ();
CREATE OR REPLACE FUNCTION sau_edif_servico_social_a_avoid_multi () RETURNS TRIGGER AS $sau_edif_servico_social_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_servico_social_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,id_org_servico_social) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.id_org_servico_social ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_servico_social_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_servico_social_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_servico_social_a
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_servico_social_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_entroncamento_p_avoid_multi () RETURNS TRIGGER AS $tra_entroncamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_entroncamento_p(nome,nomeabrev,geometriaaproximada,tipoentroncamento,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoentroncamento,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_entroncamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_entroncamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_entroncamento_p
    FOR EACH ROW EXECUTE PROCEDURE tra_entroncamento_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_trecho_rodoviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_rodoviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_rodoviario_l(geometriaaproximada,codtrechorodov,tipotrechorod,jurisdicao,administracao,concessionaria,revestimento,operacional,situacaofisica,nrpistas,nrfaixas,trafego,canteirodivisorio,geom,id_via_rodoviaria) SELECT NEW.geometriaaproximada,NEW.codtrechorodov,NEW.tipotrechorod,NEW.jurisdicao,NEW.administracao,NEW.concessionaria,NEW.revestimento,NEW.operacional,NEW.situacaofisica,NEW.nrpistas,NEW.nrfaixas,NEW.trafego,NEW.canteirodivisorio,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_via_rodoviaria ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_rodoviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_rodoviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_rodoviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_rodoviario_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_trecho_duto_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_duto_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_duto_l(nome,nomeabrev,geometriaaproximada,tipotrechoduto,mattransp,setor,posicaorelativa,matconstr,ndutos,situacaoespacial,operacional,situacaofisica,id_duto,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotrechoduto,NEW.mattransp,NEW.setor,NEW.posicaorelativa,NEW.matconstr,NEW.ndutos,NEW.situacaoespacial,NEW.operacional,NEW.situacaofisica,NEW.id_duto,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_duto_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_duto_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_duto_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_duto_l_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_pico_p_avoid_multi () RETURNS TRIGGER AS $rel_pico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_pico_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_pico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_pico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_pico_p
    FOR EACH ROW EXECUTE PROCEDURE rel_pico_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_passag_elevada_viaduto_l_avoid_multi () RETURNS TRIGGER AS $tra_passag_elevada_viaduto_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passag_elevada_viaduto_l(nome,nomeabrev,geometriaaproximada,tipopassagviad,modaluso,matconstr,operacional,situacaofisica,vaolivrehoriz,vaovertical,gabhorizsup,gabvertsup,cargasuportmaxima,nrpistas,nrfaixas,posicaopista,extensao,largura,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopassagviad,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaovertical,NEW.gabhorizsup,NEW.gabvertsup,NEW.cargasuportmaxima,NEW.nrpistas,NEW.nrfaixas,NEW.posicaopista,NEW.extensao,NEW.largura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passag_elevada_viaduto_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passag_elevada_viaduto_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passag_elevada_viaduto_l
    FOR EACH ROW EXECUTE PROCEDURE tra_passag_elevada_viaduto_l_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_cidade_p_avoid_multi () RETURNS TRIGGER AS $loc_cidade_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_cidade_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_cidade_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_cidade_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_cidade_p
    FOR EACH ROW EXECUTE PROCEDURE loc_cidade_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_capital_p_avoid_multi () RETURNS TRIGGER AS $loc_capital_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_capital_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom,tipocapital) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocapital ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_capital_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_capital_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_capital_p
    FOR EACH ROW EXECUTE PROCEDURE loc_capital_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_edif_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_ext_mineral_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipodivisaocnae,id_org_ext_mineral) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipodivisaocnae,NEW.id_org_ext_mineral ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_ext_mineral_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_distrito_a_avoid_multi () RETURNS TRIGGER AS $lim_distrito_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_distrito_a(nome,nomeabrev,geometriaaproximada,geom,geocodigo,anodereferencia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geocodigo,NEW.anodereferencia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_distrito_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_distrito_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_distrito_a
    FOR EACH ROW EXECUTE PROCEDURE lim_distrito_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_passag_elevada_viaduto_p_avoid_multi () RETURNS TRIGGER AS $tra_passag_elevada_viaduto_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passag_elevada_viaduto_p(nome,nomeabrev,geometriaaproximada,tipopassagviad,modaluso,matconstr,operacional,situacaofisica,vaolivrehoriz,vaovertical,gabhorizsup,gabvertsup,cargasuportmaxima,nrpistas,nrfaixas,posicaopista,extensao,largura,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopassagviad,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaovertical,NEW.gabhorizsup,NEW.gabvertsup,NEW.cargasuportmaxima,NEW.nrpistas,NEW.nrfaixas,NEW.posicaopista,NEW.extensao,NEW.largura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passag_elevada_viaduto_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passag_elevada_viaduto_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passag_elevada_viaduto_p
    FOR EACH ROW EXECUTE PROCEDURE tra_passag_elevada_viaduto_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_torre_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_torre_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_torre_comunic_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,posicaoreledific,ovgd,alturaestimada,id_complexo_comunicacao,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.posicaoreledific,NEW.ovgd,NEW.alturaestimada,NEW.id_complexo_comunicacao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_torre_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_torre_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_torre_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_torre_comunic_p_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_const_turistica_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_turistica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_turistica_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifturist,ovgd,id_complexo_lazer) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifturist,NEW.ovgd,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_turistica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_turistica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_turistica_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_turistica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_terreno_exposto_a_avoid_multi () RETURNS TRIGGER AS $rel_terreno_exposto_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_terreno_exposto_a(geometriaaproximada,tipoterrexp,causaexposicao,geom) SELECT NEW.geometriaaproximada,NEW.tipoterrexp,NEW.causaexposicao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_terreno_exposto_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_terreno_exposto_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_terreno_exposto_a
    FOR EACH ROW EXECUTE PROCEDURE rel_terreno_exposto_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_girador_ferroviario_p_avoid_multi () RETURNS TRIGGER AS $tra_girador_ferroviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_girador_ferroviario_p(nome,nomeabrev,geometriaaproximada,administracao,operacional,situacaofisica,geom,id_estrut_apoio) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.administracao,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_estrut_apoio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_girador_ferroviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_girador_ferroviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_girador_ferroviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_girador_ferroviario_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_trilha_picada_l_avoid_multi () RETURNS TRIGGER AS $tra_trilha_picada_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trilha_picada_l(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trilha_picada_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trilha_picada_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trilha_picada_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trilha_picada_l_avoid_multi ();
CREATE OR REPLACE FUNCTION pto_area_est_med_fenom_a_avoid_multi () RETURNS TRIGGER AS $pto_area_est_med_fenom_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_area_est_med_fenom_a(geometriaaproximada,id_est_med_fenomenos,geom) SELECT NEW.geometriaaproximada,NEW.id_est_med_fenomenos,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_area_est_med_fenom_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_area_est_med_fenom_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_area_est_med_fenom_a
    FOR EACH ROW EXECUTE PROCEDURE pto_area_est_med_fenom_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_const_turistica_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_turistica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_turistica_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifturist,ovgd,id_complexo_lazer) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifturist,NEW.ovgd,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_turistica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_turistica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_turistica_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_turistica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_posto_pol_rod_a_avoid_multi () RETURNS TRIGGER AS $adm_posto_pol_rod_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_pol_rod_a(nome,nomeabrev,tipopostopol,geometriaaproximada,operacional,situacaofisica,id_org_pub_militar,id_org_pub_civil,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.tipopostopol,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_org_pub_militar,NEW.id_org_pub_civil,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_pol_rod_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_pol_rod_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_pol_rod_a
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_pol_rod_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_trecho_comunic_l_avoid_multi () RETURNS TRIGGER AS $enc_trecho_comunic_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_trecho_comunic_l(nome,nomeabrev,geometriaaproximada,tipotrechocomunic,posicaorelativa,matconstr,operacional,situacaofisica,emduto,id_org_comerc_serv,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotrechocomunic,NEW.posicaorelativa,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.emduto,NEW.id_org_comerc_serv,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_trecho_comunic_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_trecho_comunic_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_trecho_comunic_l
    FOR EACH ROW EXECUTE PROCEDURE enc_trecho_comunic_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_banco_areia_a_avoid_multi () RETURNS TRIGGER AS $hid_banco_areia_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_banco_areia_a(nome,nomeabrev,geometriaaproximada,tipobanco,situacaoemagua,materialpredominante,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipobanco,NEW.situacaoemagua,NEW.materialpredominante,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_banco_areia_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_banco_areia_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_banco_areia_a
    FOR EACH ROW EXECUTE PROCEDURE hid_banco_areia_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_banco_areia_l_avoid_multi () RETURNS TRIGGER AS $hid_banco_areia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_banco_areia_l(nome,nomeabrev,geometriaaproximada,tipobanco,situacaoemagua,materialpredominante,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipobanco,NEW.situacaoemagua,NEW.materialpredominante,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_banco_areia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_banco_areia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_banco_areia_l
    FOR EACH ROW EXECUTE PROCEDURE hid_banco_areia_l_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_posto_pol_rod_p_avoid_multi () RETURNS TRIGGER AS $adm_posto_pol_rod_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_pol_rod_p(nome,nomeabrev,tipopostopol,geometriaaproximada,operacional,situacaofisica,id_org_pub_militar,id_org_pub_civil,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.tipopostopol,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_org_pub_militar,NEW.id_org_pub_civil,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_pol_rod_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_pol_rod_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_pol_rod_p
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_pol_rod_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_veg_restinga_a_avoid_multi () RETURNS TRIGGER AS $veg_veg_restinga_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_veg_restinga_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_veg_restinga_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_veg_restinga_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_veg_restinga_a
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_restinga_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_corredeira_p_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_p(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_p
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_faixa_seguranca_a_avoid_multi () RETURNS TRIGGER AS $tra_faixa_seguranca_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_faixa_seguranca_a(geometriaaproximada,largura,extensao,geom) SELECT NEW.geometriaaproximada,NEW.largura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_faixa_seguranca_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_faixa_seguranca_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_faixa_seguranca_a
    FOR EACH ROW EXECUTE PROCEDURE tra_faixa_seguranca_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_ensino_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_ensino_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_ensino_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,id_org_ensino) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.id_org_ensino ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_ensino_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_ensino_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_ensino_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_ensino_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_corredeira_a_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_a
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_ensino_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_ensino_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_ensino_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,id_org_ensino) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.id_org_ensino ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_ensino_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_ensino_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_ensino_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_ensino_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_ponto_trecho_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_ponto_trecho_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_ponto_trecho_energia_p(geometriaaproximada,tipoptoenergia,geom) SELECT NEW.geometriaaproximada,NEW.tipoptoenergia,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_ponto_trecho_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_ponto_trecho_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_ponto_trecho_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_ponto_trecho_energia_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_fonte_dagua_p_avoid_multi () RETURNS TRIGGER AS $hid_fonte_dagua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_fonte_dagua_p(nome,nomeabrev,geometriaaproximada,tipofontedagua,qualidagua,regime,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipofontedagua,NEW.qualidagua,NEW.regime,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_fonte_dagua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_fonte_dagua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_fonte_dagua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_fonte_dagua_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $veg_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE veg_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_corredeira_l_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_l(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_l
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_desenv_controle_a_avoid_multi () RETURNS TRIGGER AS $lim_area_desenv_controle_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_desenv_controle_a(nome,nomeabrev,geometriaaproximada,geom,classificacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_desenv_controle_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_desenv_controle_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_desenv_controle_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_desenv_controle_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_municipio_a_avoid_multi () RETURNS TRIGGER AS $lim_municipio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_municipio_a(nome,nomeabrev,geometriaaproximada,geom,geocodigo,anodereferencia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geocodigo,NEW.anodereferencia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_municipio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_municipio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_municipio_a
    FOR EACH ROW EXECUTE PROCEDURE lim_municipio_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_natureza_fundo_l_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_l(nome,nomeabrev,geometriaaproximada,materialpredominante,espessalgas,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.materialpredominante,NEW.espessalgas,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_l
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_area_desenv_controle_p_avoid_multi () RETURNS TRIGGER AS $lim_area_desenv_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_desenv_controle_p(nome,nomeabrev,geometriaaproximada,geom,classificacao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_desenv_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_desenv_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_desenv_controle_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_desenv_controle_p_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_posto_fiscal_p_avoid_multi () RETURNS TRIGGER AS $adm_posto_fiscal_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_fiscal_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipopostofisc,id_org_pub_civil,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipopostofisc,NEW.id_org_pub_civil,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_fiscal_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_fiscal_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_fiscal_p
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_fiscal_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_passagem_nivel_p_avoid_multi () RETURNS TRIGGER AS $tra_passagem_nivel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passagem_nivel_p(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passagem_nivel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passagem_nivel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passagem_nivel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_passagem_nivel_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_zona_linhas_energia_com_a_avoid_multi () RETURNS TRIGGER AS $enc_zona_linhas_energia_com_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_zona_linhas_energia_com_a(nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_zona_linhas_energia_com_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_zona_linhas_energia_com_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_zona_linhas_energia_com_a
    FOR EACH ROW EXECUTE PROCEDURE enc_zona_linhas_energia_com_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_galeria_bueiro_l_avoid_multi () RETURNS TRIGGER AS $tra_galeria_bueiro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_galeria_bueiro_l(nome,nomeabrev,matconstr,pesosuportmaximo,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.matconstr,NEW.pesosuportmaximo,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_galeria_bueiro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_galeria_bueiro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_galeria_bueiro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_galeria_bueiro_l_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_sub_distrito_a_avoid_multi () RETURNS TRIGGER AS $lim_sub_distrito_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_sub_distrito_a(nome,nomeabrev,geometriaaproximada,geom,geocodigo,anodereferencia) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geocodigo,NEW.anodereferencia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_sub_distrito_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_sub_distrito_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_sub_distrito_a
    FOR EACH ROW EXECUTE PROCEDURE lim_sub_distrito_a_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_rocha_a_avoid_multi () RETURNS TRIGGER AS $rel_rocha_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_rocha_a(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tiporocha) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tiporocha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_rocha_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_rocha_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_rocha_a
    FOR EACH ROW EXECUTE PROCEDURE rel_rocha_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_area_estrut_transporte_a_avoid_multi () RETURNS TRIGGER AS $tra_area_estrut_transporte_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_area_estrut_transporte_a(geometriaaproximada,id_estrut_transporte,geom) SELECT NEW.geometriaaproximada,NEW.id_estrut_transporte,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_area_estrut_transporte_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_area_estrut_transporte_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_area_estrut_transporte_a
    FOR EACH ROW EXECUTE PROCEDURE tra_area_estrut_transporte_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_area_umida_a_avoid_multi () RETURNS TRIGGER AS $hid_area_umida_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_area_umida_a(nome,nomeabrev,geometriaaproximada,tipoareaumida,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoareaumida,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_area_umida_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_area_umida_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_area_umida_a
    FOR EACH ROW EXECUTE PROCEDURE hid_area_umida_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_termeletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_termeletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_termeletrica_a(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom,tipocombustivel,combrenovavel,tipomaqtermica,geracao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocombustivel,NEW.combrenovavel,NEW.tipomaqtermica,NEW.geracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_termeletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_termeletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_termeletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_termeletrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_termeletrica_p_avoid_multi () RETURNS TRIGGER AS $enc_termeletrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_termeletrica_p(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom,tipocombustivel,combrenovavel,tipomaqtermica,geracao) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocombustivel,NEW.combrenovavel,NEW.tipomaqtermica,NEW.geracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_termeletrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_termeletrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_termeletrica_p
    FOR EACH ROW EXECUTE PROCEDURE enc_termeletrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_hidreletrica_l_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_l(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom,codigohidreletrica) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.codigohidreletrica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_l
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_area_comerc_serv_a_avoid_multi () RETURNS TRIGGER AS $eco_area_comerc_serv_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_comerc_serv_a(geometriaaproximada,geom,id_org_comerc_serv) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_comerc_serv_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_comerc_serv_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_comerc_serv_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_comerc_serv_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_hidreletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_a(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom,codigohidreletrica) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.codigohidreletrica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_campo_a_avoid_multi () RETURNS TRIGGER AS $veg_campo_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_campo_a(nome,nomeabrev,geometriaaproximada,tipocampo,ocorrenciaem,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipocampo,NEW.ocorrenciaem,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_campo_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_campo_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_campo_a
    FOR EACH ROW EXECUTE PROCEDURE veg_campo_a_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_hidreletrica_p_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_p(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom,codigohidreletrica) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.codigohidreletrica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_p
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_funicular_p_avoid_multi () RETURNS TRIGGER AS $tra_funicular_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_funicular_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_org_ext_mineral,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_funicular_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_funicular_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_funicular_p
    FOR EACH ROW EXECUTE PROCEDURE tra_funicular_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $veg_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_descontinuidade_geometrica_p(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE veg_descontinuidade_geometrica_p_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_unidade_federacao_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_federacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_federacao_a(nome,nomeabrev,geometriaaproximada,geom,sigla,geocodigo) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.sigla,NEW.geocodigo ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_federacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_federacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_federacao_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_federacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION lim_limite_area_especial_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_area_especial_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_area_especial_l(nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,tipolimareaesp,obssituacao) SELECT NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolimareaesp,NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_area_especial_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_area_especial_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_area_especial_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_area_especial_l_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_a(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_funicular_l_avoid_multi () RETURNS TRIGGER AS $tra_funicular_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_funicular_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_org_ext_mineral,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_funicular_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_funicular_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_funicular_l
    FOR EACH ROW EXECUTE PROCEDURE tra_funicular_l_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_l(geometriaaproximada,motivodescontinuidade,geom) SELECT NEW.geometriaaproximada,NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_l_avoid_multi ();
CREATE OR REPLACE FUNCTION rel_rocha_p_avoid_multi () RETURNS TRIGGER AS $rel_rocha_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_rocha_p(nome,nomeabrev,geometriaaproximada,tipoelemnat,geom,tiporocha) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tiporocha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_rocha_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_rocha_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_rocha_p
    FOR EACH ROW EXECUTE PROCEDURE rel_rocha_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_local_critico_p_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_p(nome,nomeabrev,geometriaaproximada,tipolocalcrit,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipolocalcrit,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_p
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_p_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_area_habitacional_a_avoid_multi () RETURNS TRIGGER AS $loc_area_habitacional_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_habitacional_a(nome,nomeabrev,id_complexo_habitacional,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.id_complexo_habitacional,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_habitacional_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_habitacional_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_habitacional_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_habitacional_a_avoid_multi ();
CREATE OR REPLACE FUNCTION loc_localidade_p_avoid_multi () RETURNS TRIGGER AS $loc_localidade_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_localidade_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_localidade_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_localidade_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_localidade_p
    FOR EACH ROW EXECUTE PROCEDURE loc_localidade_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_local_critico_a_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_a(nome,nomeabrev,geometriaaproximada,tipolocalcrit,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipolocalcrit,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_a
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_a_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_macega_chavascal_a_avoid_multi () RETURNS TRIGGER AS $veg_macega_chavascal_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_macega_chavascal_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,tipomacchav,alturamediaindividuos,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipomacchav,NEW.alturamediaindividuos,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_macega_chavascal_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_macega_chavascal_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_macega_chavascal_a
    FOR EACH ROW EXECUTE PROCEDURE veg_macega_chavascal_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_local_critico_l_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_l(nome,nomeabrev,geometriaaproximada,tipolocalcrit,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipolocalcrit,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_l
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_l_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_religiosa_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_religiosa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_religiosa_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifrelig,ensino,religiao,id_org_religiosa) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifrelig,NEW.ensino,NEW.religiao,NEW.id_org_religiosa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_religiosa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_religiosa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_religiosa_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_religiosa_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_terreno_suj_inundacao_a_avoid_multi () RETURNS TRIGGER AS $hid_terreno_suj_inundacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_terreno_suj_inundacao_a(nome,nomeabrev,geometriaaproximada,periodicidadeinunda,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.periodicidadeinunda,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_terreno_suj_inundacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_terreno_suj_inundacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_terreno_suj_inundacao_a
    FOR EACH ROW EXECUTE PROCEDURE hid_terreno_suj_inundacao_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_edif_religiosa_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_religiosa_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_religiosa_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifrelig,ensino,religiao,id_org_religiosa) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifrelig,NEW.ensino,NEW.religiao,NEW.id_org_religiosa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_religiosa_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_religiosa_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_religiosa_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_religiosa_p_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_edif_pub_civil_p_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_civil_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_civil_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifcivil,tipousoedif,id_org_pub_civil) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcivil,NEW.tipousoedif,NEW.id_org_pub_civil ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_civil_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_civil_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_civil_p
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_civil_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_trecho_energia_l_avoid_multi () RETURNS TRIGGER AS $enc_trecho_energia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_trecho_energia_l(nome,nomeabrev,geometriaaproximada,especie,posicaorelativa,operacional,situacaofisica,emduto,tensaoeletrica,numcircuitos,id_org_comerc_serv,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.especie,NEW.posicaorelativa,NEW.operacional,NEW.situacaofisica,NEW.emduto,NEW.tensaoeletrica,NEW.numcircuitos,NEW.id_org_comerc_serv,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_trecho_energia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_trecho_energia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_trecho_energia_l
    FOR EACH ROW EXECUTE PROCEDURE enc_trecho_energia_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_metro_ferroviaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_metro_ferroviaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_metro_ferroviaria_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,funcaoedifmetroferrov,multimodal,administracao,id_estrut_apoio) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.funcaoedifmetroferrov,NEW.multimodal,NEW.administracao,NEW.id_estrut_apoio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_metro_ferroviaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_metro_ferroviaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_metro_ferroviaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_metro_ferroviaria_p_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_tunel_l_avoid_multi () RETURNS TRIGGER AS $tra_tunel_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_tunel_l(geometriaaproximada,nome,nomeabrev,tipotunel,modaluso,matconstr,operacional,situacaofisica,nrpistas,nrfaixas,posicaopista,altura,extensao,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.tipotunel,NEW.modaluso,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.nrpistas,NEW.nrfaixas,NEW.posicaopista,NEW.altura,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_tunel_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_tunel_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_tunel_l
    FOR EACH ROW EXECUTE PROCEDURE tra_tunel_l_avoid_multi ();
CREATE OR REPLACE FUNCTION adm_edif_pub_civil_a_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_civil_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_civil_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifcivil,tipousoedif,id_org_pub_civil) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcivil,NEW.tipousoedif,NEW.id_org_pub_civil ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_civil_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_civil_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_civil_a
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_civil_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_edif_metro_ferroviaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_metro_ferroviaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_metro_ferroviaria_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,funcaoedifmetroferrov,multimodal,administracao,id_estrut_apoio) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.funcaoedifmetroferrov,NEW.multimodal,NEW.administracao,NEW.id_estrut_apoio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_metro_ferroviaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_metro_ferroviaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_metro_ferroviaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_metro_ferroviaria_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_quebramar_molhe_a_avoid_multi () RETURNS TRIGGER AS $hid_quebramar_molhe_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_quebramar_molhe_a(nome,nomeabrev,geometriaaproximada,tipoquebramolhe,matconstr,situamare,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoquebramolhe,NEW.matconstr,NEW.situamare,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_quebramar_molhe_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_quebramar_molhe_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_quebramar_molhe_a
    FOR EACH ROW EXECUTE PROCEDURE hid_quebramar_molhe_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_quebramar_molhe_l_avoid_multi () RETURNS TRIGGER AS $hid_quebramar_molhe_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_quebramar_molhe_l(nome,nomeabrev,geometriaaproximada,tipoquebramolhe,matconstr,situamare,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoquebramolhe,NEW.matconstr,NEW.situamare,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_quebramar_molhe_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_quebramar_molhe_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_quebramar_molhe_l
    FOR EACH ROW EXECUTE PROCEDURE hid_quebramar_molhe_l_avoid_multi ();
CREATE OR REPLACE FUNCTION veg_mangue_a_avoid_multi () RETURNS TRIGGER AS $veg_mangue_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_mangue_a(nome,nomeabrev,geometriaaproximada,denso,antropizada,geom,classificacaoporte) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_mangue_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_mangue_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_mangue_a
    FOR EACH ROW EXECUTE PROCEDURE veg_mangue_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_queda_dagua_p_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_p(nome,nomeabrev,geometriaaproximada,tipoqueda,altura,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoqueda,NEW.altura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_p_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_edif_abast_agua_p_avoid_multi () RETURNS TRIGGER AS $asb_edif_abast_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_abast_agua_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifabast,id_complexo_abast_agua) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifabast,NEW.id_complexo_abast_agua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_abast_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_abast_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_abast_agua_p
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_abast_agua_p_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_queda_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_a(nome,nomeabrev,geometriaaproximada,tipoqueda,altura,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoqueda,NEW.altura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION asb_edif_abast_agua_a_avoid_multi () RETURNS TRIGGER AS $asb_edif_abast_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_abast_agua_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifabast,id_complexo_abast_agua) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifabast,NEW.id_complexo_abast_agua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_abast_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_abast_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_abast_agua_a
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_abast_agua_a_avoid_multi ();
CREATE OR REPLACE FUNCTION hid_queda_dagua_l_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_l(nome,nomeabrev,geometriaaproximada,tipoqueda,altura,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoqueda,NEW.altura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_l
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_l_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_p_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_p(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_p
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_equip_agropec_a_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoequipagropec,matconstr,id_org_agrop_ext_veg_pesca,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoequipagropec,NEW.matconstr,NEW.id_org_agrop_ext_veg_pesca,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_a
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_arquibancada_a_avoid_multi () RETURNS TRIGGER AS $edu_arquibancada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_arquibancada_a(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_arquibancada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_arquibancada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_arquibancada_a
    FOR EACH ROW EXECUTE PROCEDURE edu_arquibancada_a_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_cremalheira_p_avoid_multi () RETURNS TRIGGER AS $tra_cremalheira_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_cremalheira_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_cremalheira_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_cremalheira_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_cremalheira_p
    FOR EACH ROW EXECUTE PROCEDURE tra_cremalheira_p_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_equip_agropec_l_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoequipagropec,matconstr,id_org_agrop_ext_veg_pesca,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoequipagropec,NEW.matconstr,NEW.id_org_agrop_ext_veg_pesca,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_l
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_l_avoid_multi ();
CREATE OR REPLACE FUNCTION tra_cremalheira_l_avoid_multi () RETURNS TRIGGER AS $tra_cremalheira_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_cremalheira_l(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_cremalheira_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_cremalheira_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_cremalheira_l
    FOR EACH ROW EXECUTE PROCEDURE tra_cremalheira_l_avoid_multi ();
CREATE OR REPLACE FUNCTION eco_equip_agropec_p_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoequipagropec,matconstr,id_org_agrop_ext_veg_pesca,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoequipagropec,NEW.matconstr,NEW.id_org_agrop_ext_veg_pesca,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_p
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_a_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_a(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_a
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_a_avoid_multi ();
CREATE OR REPLACE FUNCTION edu_arquibancada_p_avoid_multi () RETURNS TRIGGER AS $edu_arquibancada_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_arquibancada_p(nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_arquibancada_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_arquibancada_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_arquibancada_p
    FOR EACH ROW EXECUTE PROCEDURE edu_arquibancada_p_avoid_multi ();
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_l_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_l(nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,id_complexo_gerad_energ_eletr,geom) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_l
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_l_avoid_multi ();