CREATE OR REPLACE FUNCTION edu_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $edu_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_descontinuidade_geometrica_l(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE asb_area_saneamento_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_comerc_serv_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_comerc_serv_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_comerc_serv_p(finalidade,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifcomercserv,id_org_comerc_serv) SELECT NEW.finalidade,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcomercserv,NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_comerc_serv_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_comerc_serv_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_comerc_serv_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_comerc_serv_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $edu_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_descontinuidade_geometrica_a(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_comerc_serv_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_comerc_serv_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_comerc_serv_a(id_org_comerc_serv,matconstr,nome,situacaofisica,operacional,geom,tipoedifcomercserv,finalidade,nomeabrev,geometriaaproximada) SELECT NEW.id_org_comerc_serv,NEW.matconstr,NEW.nome,NEW.situacaofisica,NEW.operacional,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcomercserv,NEW.finalidade,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_comerc_serv_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_comerc_serv_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_comerc_serv_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_comerc_serv_a_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE edu_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_l_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_l(geom,tipoelemnat,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoelemnat,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_l
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_area_pub_militar_a_avoid_multi () RETURNS TRIGGER AS $adm_area_pub_militar_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_area_pub_militar_a(id_org_pub_militar,geometriaaproximada,geom) SELECT NEW.id_org_pub_militar,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_area_pub_militar_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_area_pub_militar_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_area_pub_militar_a
    FOR EACH ROW EXECUTE PROCEDURE adm_area_pub_militar_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_campo_quadra_p_avoid_multi () RETURNS TRIGGER AS $edu_campo_quadra_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_campo_quadra_p(nome,geom,id_complexo_lazer,tipocampoquadra,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer,NEW.tipocampoquadra,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_campo_quadra_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_campo_quadra_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_campo_quadra_p
    FOR EACH ROW EXECUTE PROCEDURE edu_campo_quadra_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_a_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_a(geometriaaproximada,tipoelemnat,geom,nomeabrev,nome) SELECT NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_a
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_particular_a_avoid_multi () RETURNS TRIGGER AS $lim_area_particular_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_particular_a(geometriaaproximada,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_particular_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_particular_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_particular_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_particular_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_campo_quadra_a_avoid_multi () RETURNS TRIGGER AS $edu_campo_quadra_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_campo_quadra_a(operacional,nome,nomeabrev,geometriaaproximada,situacaofisica,tipocampoquadra,id_complexo_lazer,geom) SELECT NEW.operacional,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.situacaofisica,NEW.tipocampoquadra,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_campo_quadra_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_campo_quadra_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_campo_quadra_a
    FOR EACH ROW EXECUTE PROCEDURE edu_campo_quadra_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_elemento_fisiog_natural_p_avoid_multi () RETURNS TRIGGER AS $rel_elemento_fisiog_natural_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_elemento_fisiog_natural_p(nome,geom,tipoelemnat,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoelemnat,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_elemento_fisiog_natural_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_elemento_fisiog_natural_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_elemento_fisiog_natural_p
    FOR EACH ROW EXECUTE PROCEDURE rel_elemento_fisiog_natural_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_delimitacao_fisica_l_avoid_multi () RETURNS TRIGGER AS $lim_delimitacao_fisica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_delimitacao_fisica_l(tipodelimfis,eletrificada,matconstr,nome,geometriaaproximada,nomeabrev,geom) SELECT NEW.tipodelimfis,NEW.eletrificada,NEW.matconstr,NEW.nome,NEW.geometriaaproximada,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_delimitacao_fisica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_delimitacao_fisica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_delimitacao_fisica_l
    FOR EACH ROW EXECUTE PROCEDURE lim_delimitacao_fisica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_hab_indigena_p_avoid_multi () RETURNS TRIGGER AS $loc_hab_indigena_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_hab_indigena_p(isolada,coletiva,geometriaaproximada,nomeabrev,nome,geom,id_aldeia_indigena) SELECT NEW.isolada,NEW.coletiva,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_aldeia_indigena ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_hab_indigena_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_hab_indigena_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_hab_indigena_p
    FOR EACH ROW EXECUTE PROCEDURE loc_hab_indigena_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE edu_area_lazer_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_terra_indigena_p_avoid_multi () RETURNS TRIGGER AS $lim_terra_indigena_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_indigena_p(nomeabrev,geom,perimetrooficial,areaoficialha,grupoetnico,datasituacaojuridica,situacaojuridica,nometi,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.perimetrooficial,NEW.areaoficialha,NEW.grupoetnico,NEW.datasituacaojuridica,NEW.situacaojuridica,NEW.nometi,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_indigena_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_indigena_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_indigena_p
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_indigena_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_piscina_a_avoid_multi () RETURNS TRIGGER AS $edu_piscina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_piscina_a(geom,id_complexo_lazer,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_piscina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_piscina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_piscina_a
    FOR EACH ROW EXECUTE PROCEDURE edu_piscina_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_hab_indigena_a_avoid_multi () RETURNS TRIGGER AS $loc_hab_indigena_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_hab_indigena_a(geometriaaproximada,nome,nomeabrev,coletiva,isolada,id_aldeia_indigena,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.coletiva,NEW.isolada,NEW.id_aldeia_indigena,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_hab_indigena_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_hab_indigena_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_hab_indigena_a
    FOR EACH ROW EXECUTE PROCEDURE loc_hab_indigena_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_edif_comunic_a_avoid_multi () RETURNS TRIGGER AS $enc_edif_comunic_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_comunic_a(nome,id_complexo_comunicacao,tipoedifcomunic,modalidade,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.id_complexo_comunicacao,NEW.tipoedifcomunic,NEW.modalidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_comunic_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_comunic_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_comunic_a
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_comunic_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_terra_indigena_a_avoid_multi () RETURNS TRIGGER AS $lim_terra_indigena_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_indigena_a(nome,nomeabrev,geometriaaproximada,nometi,situacaojuridica,areaoficialha,perimetrooficial,geom,datasituacaojuridica,grupoetnico) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.nometi,NEW.situacaojuridica,NEW.areaoficialha,NEW.perimetrooficial,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.datasituacaojuridica,NEW.grupoetnico ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_indigena_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_indigena_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_indigena_a
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_indigena_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_condutor_hidrico_l_avoid_multi () RETURNS TRIGGER AS $tra_condutor_hidrico_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_condutor_hidrico_l(tipotrechoduto,mattransp,setor,id_complexo_gerad_energ_eletr,matconstr,ndutos,situacaoespacial,operacional,situacaofisica,id_duto,geom,tipocondutor,nome,nomeabrev,geometriaaproximada,posicaorelativa) SELECT NEW.tipotrechoduto,NEW.mattransp,NEW.setor,NEW.id_complexo_gerad_energ_eletr,NEW.matconstr,NEW.ndutos,NEW.situacaoespacial,NEW.operacional,NEW.situacaofisica,NEW.id_duto,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocondutor,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.posicaorelativa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_condutor_hidrico_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_condutor_hidrico_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_condutor_hidrico_l
    FOR EACH ROW EXECUTE PROCEDURE tra_condutor_hidrico_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_foz_maritima_p_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_p(nome,geom,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_p
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_foz_maritima_l_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_l(nome,geom,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_l
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_foz_maritima_a_avoid_multi () RETURNS TRIGGER AS $hid_foz_maritima_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_foz_maritima_a(geometriaaproximada,geom,nomeabrev,nome) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_foz_maritima_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_foz_maritima_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_foz_maritima_a
    FOR EACH ROW EXECUTE PROCEDURE hid_foz_maritima_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_ponte_p_avoid_multi () RETURNS TRIGGER AS $tra_ponte_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponte_p(largura,matconstr,operacional,situacaofisica,vaolivrehoriz,vaolivrevertical,cargasuportmaxima,nrfaixas,nrpistas,posicaopista,modaluso,extensao,geom,tipoponte,geometriaaproximada,nomeabrev,nome) SELECT NEW.largura,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaolivrevertical,NEW.cargasuportmaxima,NEW.nrfaixas,NEW.nrpistas,NEW.posicaopista,NEW.modaluso,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoponte,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponte_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponte_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponte_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponte_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_ponte_l_avoid_multi () RETURNS TRIGGER AS $tra_ponte_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponte_l(nome,nomeabrev,geom,extensao,largura,posicaopista,nrpistas,nrfaixas,cargasuportmaxima,vaolivrevertical,vaolivrehoriz,situacaofisica,operacional,matconstr,modaluso,tipoponte,geometriaaproximada) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.extensao,NEW.largura,NEW.posicaopista,NEW.nrpistas,NEW.nrfaixas,NEW.cargasuportmaxima,NEW.vaolivrevertical,NEW.vaolivrehoriz,NEW.situacaofisica,NEW.operacional,NEW.matconstr,NEW.modaluso,NEW.tipoponte,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponte_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponte_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponte_l
    FOR EACH ROW EXECUTE PROCEDURE tra_ponte_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_sinalizacao_p_avoid_multi () RETURNS TRIGGER AS $tra_sinalizacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_sinalizacao_p(nomeabrev,geom,nome,situacaofisica,operacional,tiposinal,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.situacaofisica,NEW.operacional,NEW.tiposinal,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_sinalizacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_sinalizacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_sinalizacao_p
    FOR EACH ROW EXECUTE PROCEDURE tra_sinalizacao_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_pto_controle_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_controle_p(materializado,outrarefplan,orgaoenteresp,codponto,obs,geom,tipoptocontrole,codprojeto,nomeabrev,geometriaaproximada,tiporef,latitude,longitude,altitudeortometrica,sistemageodesico,referencialaltim,outrarefalt) SELECT NEW.materializado,NEW.outrarefplan,NEW.orgaoenteresp,NEW.codponto,NEW.obs,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoptocontrole,NEW.codprojeto,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tiporef,NEW.latitude,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.referencialaltim,NEW.outrarefalt ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_controle_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_controle_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_conserv_nao_snuc_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_conserv_nao_snuc_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_conserv_nao_snuc_a(geometriaaproximada,nomeabrev,classificacao,administracao,geom,atolegal,sigla,anocriacao,areaoficial,nome) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.classificacao,NEW.administracao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.atolegal,NEW.sigla,NEW.anocriacao,NEW.areaoficial,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_conserv_nao_snuc_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_conserv_nao_snuc_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_conserv_nao_snuc_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_conserv_nao_snuc_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_aglomerado_rural_isolado_p_avoid_multi () RETURNS TRIGGER AS $loc_aglomerado_rural_isolado_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglomerado_rural_isolado_p(nomeabrev,longitude_gms,longitude,latitude_gms,latitude,identificador,geocodigo,geometriaaproximada,nome,tipoaglomrurisol,geom) SELECT NEW.nomeabrev,NEW.longitude_gms,NEW.longitude,NEW.latitude_gms,NEW.latitude,NEW.identificador,NEW.geocodigo,NEW.geometriaaproximada,NEW.nome,NEW.tipoaglomrurisol,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglomerado_rural_isolado_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglomerado_rural_isolado_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglomerado_rural_isolado_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglomerado_rural_isolado_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_massa_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_massa_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_massa_dagua_a(salinidade,nome,regime,geom,geometriaaproximada,nomeabrev,tipomassadagua) SELECT NEW.salinidade,NEW.nome,NEW.regime,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.tipomassadagua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_massa_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_massa_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_massa_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_massa_dagua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_conserv_nao_snuc_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_conserv_nao_snuc_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_conserv_nao_snuc_p(nome,geometriaaproximada,geom,atolegal,administracao,classificacao,anocriacao,sigla,areaoficial,nomeabrev) SELECT NEW.nome,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.atolegal,NEW.administracao,NEW.classificacao,NEW.anocriacao,NEW.sigla,NEW.areaoficial,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_conserv_nao_snuc_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_conserv_nao_snuc_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_conserv_nao_snuc_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_conserv_nao_snuc_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_ext_mineral_a(nomeabrev,nome,operacional,situacaofisica,tipoextmin,tipoprodutoresiduo,tipopocomina,procextracao,formaextracao,atividade,id_org_ext_mineral,geom,tiposecaocnae,geometriaaproximada) SELECT NEW.nomeabrev,NEW.nome,NEW.operacional,NEW.situacaofisica,NEW.tipoextmin,NEW.tipoprodutoresiduo,NEW.tipopocomina,NEW.procextracao,NEW.formaextracao,NEW.atividade,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tiposecaocnae,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_ext_mineral_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_ext_mineral_p_avoid_multi () RETURNS TRIGGER AS $eco_ext_mineral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_ext_mineral_p(nomeabrev,atividade,formaextracao,procextracao,tipopocomina,tipoprodutoresiduo,tipoextmin,situacaofisica,operacional,tiposecaocnae,id_org_ext_mineral,geom,nome,geometriaaproximada) SELECT NEW.nomeabrev,NEW.atividade,NEW.formaextracao,NEW.procextracao,NEW.tipopocomina,NEW.tipoprodutoresiduo,NEW.tipoextmin,NEW.situacaofisica,NEW.operacional,NEW.tiposecaocnae,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_ext_mineral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_ext_mineral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_ext_mineral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_ext_mineral_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_area_comunicacao_a_avoid_multi () RETURNS TRIGGER AS $enc_area_comunicacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_area_comunicacao_a(id_complexo_comunicacao,geometriaaproximada,geom) SELECT NEW.id_complexo_comunicacao,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_area_comunicacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_area_comunicacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_area_comunicacao_a
    FOR EACH ROW EXECUTE PROCEDURE enc_area_comunicacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_vegetacao_a_avoid_multi () RETURNS TRIGGER AS $veg_vegetacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_vegetacao_a(geom,nome,nomeabrev,geometriaaproximada,denso,antropizada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_vegetacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_vegetacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_vegetacao_a
    FOR EACH ROW EXECUTE PROCEDURE veg_vegetacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_nome_local_p_avoid_multi () RETURNS TRIGGER AS $loc_nome_local_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_nome_local_p(geometriaaproximada,nome,geom) SELECT NEW.geometriaaproximada,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_nome_local_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_nome_local_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_nome_local_p
    FOR EACH ROW EXECUTE PROCEDURE loc_nome_local_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_aglomerado_rural_p_avoid_multi () RETURNS TRIGGER AS $loc_aglomerado_rural_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglomerado_rural_p(nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,geom,longitude,longitude_gms) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.longitude,NEW.longitude_gms ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglomerado_rural_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglomerado_rural_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglomerado_rural_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglomerado_rural_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_ruina_a_avoid_multi () RETURNS TRIGGER AS $edu_ruina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_ruina_a(id_complexo_lazer,geometriaaproximada,nomeabrev,nome,geom) SELECT NEW.id_complexo_lazer,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_ruina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_ruina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_ruina_a
    FOR EACH ROW EXECUTE PROCEDURE edu_ruina_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_industrial_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_industrial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_industrial_a(nomeabrev,geometriaaproximada,nome,id_org_industrial,tipodivisaocnae,chamine,geom,matconstr,situacaofisica,operacional) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.nome,NEW.id_org_industrial,NEW.tipodivisaocnae,NEW.chamine,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_industrial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_industrial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_industrial_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_industrial_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_ruina_p_avoid_multi () RETURNS TRIGGER AS $edu_ruina_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_ruina_p(nome,nomeabrev,geom,id_complexo_lazer,geometriaaproximada) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_ruina_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_ruina_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_ruina_p
    FOR EACH ROW EXECUTE PROCEDURE edu_ruina_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_industrial_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_industrial_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_industrial_p(geom,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,chamine,tipodivisaocnae,id_org_industrial) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,NEW.chamine,NEW.tipodivisaocnae,NEW.id_org_industrial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_industrial_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_industrial_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_industrial_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_industrial_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $pto_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_descontinuidade_geometrica_p(motivodescontinuidade,geom,geometriaaproximada) SELECT NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE pto_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_rocha_em_agua_a_avoid_multi () RETURNS TRIGGER AS $hid_rocha_em_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_rocha_em_agua_a(nomeabrev,situacaoemagua,nome,geom,alturalamina) SELECT NEW.nomeabrev,NEW.situacaoemagua,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.alturalamina ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_rocha_em_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_rocha_em_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_rocha_em_agua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_rocha_em_agua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_cerrado_cerradao_a_avoid_multi () RETURNS TRIGGER AS $veg_cerrado_cerradao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_cerrado_cerradao_a(nome,classificacaoporte,tipocerr,geom,antropizada,denso,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.classificacaoporte,NEW.tipocerr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_cerrado_cerradao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_cerrado_cerradao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_cerrado_cerradao_a
    FOR EACH ROW EXECUTE PROCEDURE veg_cerrado_cerradao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $pto_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_descontinuidade_geometrica_a(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE pto_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_rocha_em_agua_p_avoid_multi () RETURNS TRIGGER AS $hid_rocha_em_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_rocha_em_agua_p(situacaoemagua,nome,nomeabrev,alturalamina,geom) SELECT NEW.situacaoemagua,NEW.nome,NEW.nomeabrev,NEW.alturalamina,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_rocha_em_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_rocha_em_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_rocha_em_agua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_rocha_em_agua_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_estepe_a_avoid_multi () RETURNS TRIGGER AS $veg_estepe_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_estepe_a(geometriaaproximada,alturamediaindividuos,geom,antropizada,denso,nomeabrev,nome) SELECT NEW.geometriaaproximada,NEW.alturamediaindividuos,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_estepe_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_estepe_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_estepe_a
    FOR EACH ROW EXECUTE PROCEDURE veg_estepe_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_tunel_p_avoid_multi () RETURNS TRIGGER AS $tra_tunel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_tunel_p(nome,extensao,altura,posicaopista,nrfaixas,nrpistas,situacaofisica,operacional,matconstr,modaluso,tipotunel,geometriaaproximada,nomeabrev,geom) SELECT NEW.nome,NEW.extensao,NEW.altura,NEW.posicaopista,NEW.nrfaixas,NEW.nrpistas,NEW.situacaofisica,NEW.operacional,NEW.matconstr,NEW.modaluso,NEW.tipotunel,NEW.geometriaaproximada,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_tunel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_tunel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_tunel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_tunel_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_p_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_p(geometriaaproximada,nome,nomeabrev,tipoobst,situacaoemagua,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.tipoobst,NEW.situacaoemagua,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_p
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_grupo_transformadores_p_avoid_multi () RETURNS TRIGGER AS $enc_grupo_transformadores_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_grupo_transformadores_p(nomeabrev,geom,id_subestacao_ener_eletr,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_subestacao_ener_eletr,NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_grupo_transformadores_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_grupo_transformadores_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_grupo_transformadores_p
    FOR EACH ROW EXECUTE PROCEDURE enc_grupo_transformadores_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_pto_ref_geod_topo_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_ref_geod_topo_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_ref_geod_topo_p(datavisita,geom,obs,codponto,geometriaaproximada,tiporef,latitude,longitude,altitudeortometrica,sistemageodesico,referencialaltim,outrarefalt,nomeabrev,outrarefplan,orgaoenteresp,nome,proximidade,tipoptorefgeodtopo,rede,referencialgrav,situacaomarco) SELECT NEW.datavisita,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.obs,NEW.codponto,NEW.geometriaaproximada,NEW.tiporef,NEW.latitude,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.referencialaltim,NEW.outrarefalt,NEW.nomeabrev,NEW.outrarefplan,NEW.orgaoenteresp,NEW.nome,NEW.proximidade,NEW.tipoptorefgeodtopo,NEW.rede,NEW.referencialgrav,NEW.situacaomarco ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_ref_geod_topo_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_ref_geod_topo_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_ref_geod_topo_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_ref_geod_topo_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_a_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_a(nomeabrev,geometriaaproximada,tipoobst,situacaoemagua,geom,nome) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoobst,NEW.situacaoemagua,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_a
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_grupo_transformadores_a_avoid_multi () RETURNS TRIGGER AS $enc_grupo_transformadores_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_grupo_transformadores_a(geometriaaproximada,nomeabrev,id_subestacao_ener_eletr,geom,nome) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.id_subestacao_ener_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_grupo_transformadores_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_grupo_transformadores_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_grupo_transformadores_a
    FOR EACH ROW EXECUTE PROCEDURE enc_grupo_transformadores_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_obstaculo_navegacao_l_avoid_multi () RETURNS TRIGGER AS $tra_obstaculo_navegacao_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_obstaculo_navegacao_l(situacaoemagua,tipoobst,geometriaaproximada,nomeabrev,nome,geom) SELECT NEW.situacaoemagua,NEW.tipoobst,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_obstaculo_navegacao_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_obstaculo_navegacao_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_obstaculo_navegacao_l
    FOR EACH ROW EXECUTE PROCEDURE tra_obstaculo_navegacao_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_edif_saneamento_a_avoid_multi () RETURNS TRIGGER AS $asb_edif_saneamento_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_saneamento_a(geometriaaproximada,nome,nomeabrev,operacional,situacaofisica,matconstr,geom,tipoedifsaneam,id_complexo_saneamento) SELECT NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifsaneam,NEW.id_complexo_saneamento ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_saneamento_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_saneamento_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_saneamento_a
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_saneamento_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_edif_saude_a_avoid_multi () RETURNS TRIGGER AS $sau_edif_saude_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_saude_a(nome,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoclassecnae,nivelatencao,id_org_saude,nomeabrev) SELECT NEW.nome,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoclassecnae,NEW.nivelatencao,NEW.id_org_saude,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_saude_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_saude_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_saude_a
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_saude_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_edif_saneamento_p_avoid_multi () RETURNS TRIGGER AS $asb_edif_saneamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_saneamento_p(tipoedifsaneam,nome,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,id_complexo_saneamento) SELECT NEW.tipoedifsaneam,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.id_complexo_saneamento ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_saneamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_saneamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_saneamento_p
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_saneamento_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_edif_saude_p_avoid_multi () RETURNS TRIGGER AS $sau_edif_saude_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_saude_p(matconstr,nivelatencao,id_org_saude,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoclassecnae,geom) SELECT NEW.matconstr,NEW.nivelatencao,NEW.id_org_saude,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoclassecnae,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_saude_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_saude_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_saude_p
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_saude_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_area_energia_eletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_area_energia_eletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_area_energia_eletrica_a(id_subestacao_ener_eletr,geometriaaproximada,geom,id_complexo_gerad_energ_eletr) SELECT NEW.id_subestacao_ener_eletr,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_area_energia_eletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_area_energia_eletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_area_energia_eletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_area_energia_eletrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_edif_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_edif_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_comunic_p(nome,id_complexo_comunicacao,tipoedifcomunic,modalidade,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.id_complexo_comunicacao,NEW.tipoedifcomunic,NEW.modalidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_comunic_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_campinarana_a_avoid_multi () RETURNS TRIGGER AS $veg_campinarana_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_campinarana_a(classificacaoporte,alturamediaindividuos,geom,antropizada,denso,geometriaaproximada,nome,nomeabrev) SELECT NEW.classificacaoporte,NEW.alturamediaindividuos,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_campinarana_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_campinarana_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_campinarana_a
    FOR EACH ROW EXECUTE PROCEDURE veg_campinarana_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_brejo_pantano_a_avoid_multi () RETURNS TRIGGER AS $veg_brejo_pantano_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_brejo_pantano_a(nomeabrev,antropizada,geom,classificacaoporte,alturamediaindividuos,tipobrejopantano,nome,denso,geometriaaproximada) SELECT NEW.nomeabrev,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacaoporte,NEW.alturamediaindividuos,NEW.tipobrejopantano,NEW.nome,NEW.denso,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_brejo_pantano_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_brejo_pantano_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_brejo_pantano_a
    FOR EACH ROW EXECUTE PROCEDURE veg_brejo_pantano_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_ponto_drenagem_p_avoid_multi () RETURNS TRIGGER AS $hid_ponto_drenagem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ponto_drenagem_p(nome,geom,relacionado,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.relacionado,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ponto_drenagem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ponto_drenagem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ponto_drenagem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ponto_drenagem_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_limite_massa_dagua_l_avoid_multi () RETURNS TRIGGER AS $hid_limite_massa_dagua_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_limite_massa_dagua_l(nomeabrev,geometriaaproximada,materialpredominante,alturamediamargem,tipolimmassa,geom) SELECT NEW.nomeabrev,NEW.geometriaaproximada,NEW.materialpredominante,NEW.alturamediamargem,NEW.tipolimmassa,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_limite_massa_dagua_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_limite_massa_dagua_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_limite_massa_dagua_l
    FOR EACH ROW EXECUTE PROCEDURE hid_limite_massa_dagua_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_coreto_tribuna_a_avoid_multi () RETURNS TRIGGER AS $edu_coreto_tribuna_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_coreto_tribuna_a(geometriaaproximada,nome,operacional,nomeabrev,situacaofisica,id_complexo_lazer,geom) SELECT NEW.geometriaaproximada,NEW.nome,NEW.operacional,NEW.nomeabrev,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_coreto_tribuna_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_coreto_tribuna_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_coreto_tribuna_a
    FOR EACH ROW EXECUTE PROCEDURE edu_coreto_tribuna_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_alter_fisiog_antropica_a_avoid_multi () RETURNS TRIGGER AS $rel_alter_fisiog_antropica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_alter_fisiog_antropica_a(nome,nomeabrev,geom,tipoalterantrop,geometriaaproximada) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoalterantrop,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_alter_fisiog_antropica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_alter_fisiog_antropica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_alter_fisiog_antropica_a
    FOR EACH ROW EXECUTE PROCEDURE rel_alter_fisiog_antropica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_alter_fisiog_antropica_l_avoid_multi () RETURNS TRIGGER AS $rel_alter_fisiog_antropica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_alter_fisiog_antropica_l(geom,geometriaaproximada,nomeabrev,tipoalterantrop,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.tipoalterantrop,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_alter_fisiog_antropica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_alter_fisiog_antropica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_alter_fisiog_antropica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_alter_fisiog_antropica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_coreto_tribuna_p_avoid_multi () RETURNS TRIGGER AS $edu_coreto_tribuna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_coreto_tribuna_p(geom,geometriaaproximada,operacional,situacaofisica,id_complexo_lazer,nome,nomeabrev) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_coreto_tribuna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_coreto_tribuna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_coreto_tribuna_p
    FOR EACH ROW EXECUTE PROCEDURE edu_coreto_tribuna_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_edificacao_a_avoid_multi () RETURNS TRIGGER AS $loc_edificacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edificacao_a(geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edificacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edificacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edificacao_a
    FOR EACH ROW EXECUTE PROCEDURE loc_edificacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_pto_geod_topo_controle_p_avoid_multi () RETURNS TRIGGER AS $pto_pto_geod_topo_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_pto_geod_topo_controle_p(latitude,geom,obs,codponto,orgaoenteresp,outrarefplan,outrarefalt,referencialaltim,sistemageodesico,altitudeortometrica,longitude,tiporef,geometriaaproximada,nomeabrev) SELECT NEW.latitude,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.obs,NEW.codponto,NEW.orgaoenteresp,NEW.outrarefplan,NEW.outrarefalt,NEW.referencialaltim,NEW.sistemageodesico,NEW.altitudeortometrica,NEW.longitude,NEW.tiporef,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_pto_geod_topo_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_pto_geod_topo_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_pto_geod_topo_controle_p
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_geod_topo_controle_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_edificacao_p_avoid_multi () RETURNS TRIGGER AS $loc_edificacao_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edificacao_p(nomeabrev,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edificacao_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edificacao_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edificacao_p
    FOR EACH ROW EXECUTE PROCEDURE loc_edificacao_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_bairro_a_avoid_multi () RETURNS TRIGGER AS $lim_bairro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_bairro_a(nomeabrev,geom,anodereferencia,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anodereferencia,NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_bairro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_bairro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_bairro_a
    FOR EACH ROW EXECUTE PROCEDURE lim_bairro_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_terra_publica_a_avoid_multi () RETURNS TRIGGER AS $lim_terra_publica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_publica_a(nomeabrev,nome,geometriaaproximada,geom,classificacao) SELECT NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_publica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_publica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_publica_a
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_publica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_limite_intra_munic_adm_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_intra_munic_adm_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_intra_munic_adm_l(geometriaaproximada,coincidecomdentrode,nomeabrev,tipolimintramun,obssituacao,nome,geom,extensao) SELECT NEW.geometriaaproximada,NEW.coincidecomdentrode,NEW.nomeabrev,NEW.tipolimintramun,NEW.obssituacao,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.extensao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_intra_munic_adm_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_intra_munic_adm_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_intra_munic_adm_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_intra_munic_adm_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_eclusa_l_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_l(situacaofisica,geom,nome,nomeabrev,geometriaaproximada,desnivel,largura,extensao,calado,matconstr,operacional) SELECT NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.desnivel,NEW.largura,NEW.extensao,NEW.calado,NEW.matconstr,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_l
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_atracadouro_l_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_l(geometriaaproximada,tipoatracad,administracao,matconstr,operacional,nome,situacaofisica,id_complexo_portuario,geom,nomeabrev) SELECT NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.matconstr,NEW.operacional,NEW.nome,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_barragem_p_avoid_multi () RETURNS TRIGGER AS $hid_barragem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_p(nome,geom,id_complexo_gerad_energ_eletr,situacaofisica,operacional,usoprincipal,matconstr,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.situacaofisica,NEW.operacional,NEW.usoprincipal,NEW.matconstr,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_atracadouro_a_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_a(nome,operacional,situacaofisica,id_complexo_portuario,geom,nomeabrev,geometriaaproximada,tipoatracad,administracao,matconstr) SELECT NEW.nome,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.matconstr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_a
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $lim_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_descontinuidade_geometrica_a(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE lim_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_ponto_inicio_drenagem_p_avoid_multi () RETURNS TRIGGER AS $hid_ponto_inicio_drenagem_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ponto_inicio_drenagem_p(nascente,geom,nome,nomeabrev,geometriaaproximada,relacionado) SELECT NEW.nascente,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.relacionado ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ponto_inicio_drenagem_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ponto_inicio_drenagem_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ponto_inicio_drenagem_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ponto_inicio_drenagem_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $eco_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_descontinuidade_geometrica_l(motivodescontinuidade,geom,geometriaaproximada) SELECT NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE eco_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_linha_de_limite_l_avoid_multi () RETURNS TRIGGER AS $lim_linha_de_limite_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_linha_de_limite_l(geom,extensao,geometriaaproximada,coincidecomdentrode,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.extensao,NEW.geometriaaproximada,NEW.coincidecomdentrode,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_linha_de_limite_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_linha_de_limite_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_linha_de_limite_l
    FOR EACH ROW EXECUTE PROCEDURE lim_linha_de_limite_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_eclusa_p_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_p(largura,nome,nomeabrev,geometriaaproximada,desnivel,extensao,calado,matconstr,operacional,situacaofisica,geom) SELECT NEW.largura,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.desnivel,NEW.extensao,NEW.calado,NEW.matconstr,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_p
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_atracadouro_p_avoid_multi () RETURNS TRIGGER AS $tra_atracadouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_atracadouro_p(matconstr,nome,nomeabrev,geometriaaproximada,tipoatracad,administracao,operacional,situacaofisica,id_complexo_portuario,geom) SELECT NEW.matconstr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoatracad,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_atracadouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_atracadouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_atracadouro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_atracadouro_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_sumidouro_vertedouro_p_avoid_multi () RETURNS TRIGGER AS $hid_sumidouro_vertedouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_sumidouro_vertedouro_p(geometriaaproximada,tiposumvert,causa,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,NEW.tiposumvert,NEW.causa,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_sumidouro_vertedouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_sumidouro_vertedouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_sumidouro_vertedouro_p
    FOR EACH ROW EXECUTE PROCEDURE hid_sumidouro_vertedouro_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_p(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_limite_politico_adm_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_politico_adm_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_politico_adm_l(geometriaaproximada,obssituacao,tipolimpol,geom,extensao,coincidecomdentrode,nomeabrev,nome) SELECT NEW.geometriaaproximada,NEW.obssituacao,NEW.tipolimpol,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.extensao,NEW.coincidecomdentrode,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_politico_adm_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_politico_adm_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_politico_adm_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_politico_adm_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_l(motivodescontinuidade,geometriaaproximada,geom) SELECT NEW.motivodescontinuidade,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $tra_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_descontinuidade_geometrica_a(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE tra_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_rodoviaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_rodoviaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_rodoviaria_p(tipoedifrod,id_estrut_apoio,operacional,situacaofisica,matconstr,geom,administracao,nome,nomeabrev,geometriaaproximada) SELECT NEW.tipoedifrod,NEW.id_estrut_apoio,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.administracao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_rodoviaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_rodoviaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_rodoviaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_rodoviaria_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_area_abast_agua_a_avoid_multi () RETURNS TRIGGER AS $asb_area_abast_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_area_abast_agua_a(geom,geometriaaproximada,id_complexo_abast_agua) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.id_complexo_abast_agua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_area_abast_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_area_abast_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_area_abast_agua_a
    FOR EACH ROW EXECUTE PROCEDURE asb_area_abast_agua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_limite_operacional_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_operacional_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_operacional_l(coincidecomdentrode,extensao,geom,tipolimoper,obssituacao,nome,nomeabrev,geometriaaproximada) SELECT NEW.coincidecomdentrode,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolimoper,NEW.obssituacao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_operacional_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_operacional_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_operacional_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_operacional_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_cemiterio_p_avoid_multi () RETURNS TRIGGER AS $asb_cemiterio_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_cemiterio_p(tipocemiterio,geometriaaproximada,nomeabrev,nome,geom,denominacaoassociada) SELECT NEW.tipocemiterio,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.denominacaoassociada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_cemiterio_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_cemiterio_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_cemiterio_p
    FOR EACH ROW EXECUTE PROCEDURE asb_cemiterio_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_outras_unid_protegidas_a_avoid_multi () RETURNS TRIGGER AS $lim_outras_unid_protegidas_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_outras_unid_protegidas_a(geometriaaproximada,nomeabrev,nome,geom,tipooutunidprot,anocriacao,historicomodificacao,sigla,areaoficial,administracao) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipooutunidprot,NEW.anocriacao,NEW.historicomodificacao,NEW.sigla,NEW.areaoficial,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_outras_unid_protegidas_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_outras_unid_protegidas_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_outras_unid_protegidas_a
    FOR EACH ROW EXECUTE PROCEDURE lim_outras_unid_protegidas_a_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_hidroviario_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_rodoviaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_rodoviaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_rodoviaria_a(situacaofisica,geometriaaproximada,id_estrut_apoio,administracao,nomeabrev,nome,operacional,tipoedifrod,geom,matconstr) SELECT NEW.situacaofisica,NEW.geometriaaproximada,NEW.id_estrut_apoio,NEW.administracao,NEW.nomeabrev,NEW.nome,NEW.operacional,NEW.tipoedifrod,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_rodoviaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_rodoviaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_rodoviaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_rodoviaria_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_outras_unid_protegidas_p_avoid_multi () RETURNS TRIGGER AS $lim_outras_unid_protegidas_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_outras_unid_protegidas_p(anocriacao,tipooutunidprot,geom,administracao,areaoficial,sigla,historicomodificacao,geometriaaproximada,nomeabrev,nome) SELECT NEW.anocriacao,NEW.tipooutunidprot,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.administracao,NEW.areaoficial,NEW.sigla,NEW.historicomodificacao,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_outras_unid_protegidas_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_outras_unid_protegidas_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_outras_unid_protegidas_p
    FOR EACH ROW EXECUTE PROCEDURE lim_outras_unid_protegidas_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_cemiterio_a_avoid_multi () RETURNS TRIGGER AS $asb_cemiterio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_cemiterio_a(denominacaoassociada,geometriaaproximada,nomeabrev,nome,geom,tipocemiterio) SELECT NEW.denominacaoassociada,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocemiterio ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_cemiterio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_cemiterio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_cemiterio_a
    FOR EACH ROW EXECUTE PROCEDURE asb_cemiterio_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_comporta_p_avoid_multi () RETURNS TRIGGER AS $hid_comporta_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_comporta_p(situacaofisica,nome,nomeabrev,geometriaaproximada,operacional,geom) SELECT NEW.situacaofisica,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_comporta_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_comporta_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_comporta_p
    FOR EACH ROW EXECUTE PROCEDURE hid_comporta_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_trecho_ferroviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_ferroviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_ferroviario_l(nomeabrev,geom,id_via_ferrea,cargasuportmaxima,situacaofisica,operacional,concessionaria,administracao,jurisdicao,emarruamento,nrlinhas,eletrificada,bitola,tipotrechoferrov,posicaorelativa,codtrechoferrov,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_via_ferrea,NEW.cargasuportmaxima,NEW.situacaofisica,NEW.operacional,NEW.concessionaria,NEW.administracao,NEW.jurisdicao,NEW.emarruamento,NEW.nrlinhas,NEW.eletrificada,NEW.bitola,NEW.tipotrechoferrov,NEW.posicaorelativa,NEW.codtrechoferrov,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_ferroviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_ferroviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_ferroviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_ferroviario_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_hidreletrica_p_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_p(operacional,geometriaaproximada,nomeabrev,nome,codigohidreletrica,destenergelet,situacaofisica,tipoestgerad,geom,id_complexo_gerad_energ_eletr,potenciafiscalizada,potenciaoutorgada,codigoestacao) SELECT NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.codigohidreletrica,NEW.destenergelet,NEW.situacaofisica,NEW.tipoestgerad,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.potenciaoutorgada,NEW.codigoestacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_p
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_comporta_l_avoid_multi () RETURNS TRIGGER AS $hid_comporta_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_comporta_l(geom,situacaofisica,nome,nomeabrev,geometriaaproximada,operacional) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_comporta_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_comporta_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_comporta_l
    FOR EACH ROW EXECUTE PROCEDURE hid_comporta_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_constr_portuaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_portuaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_portuaria_a(id_complexo_portuario,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifport,administracao) SELECT NEW.id_complexo_portuario,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifport,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_portuaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_portuaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_portuaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_portuaria_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_trecho_drenagem_l_avoid_multi () RETURNS TRIGGER AS $hid_trecho_drenagem_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_trecho_drenagem_l(eixoprincipal,compartilhado,dentrodepoligono,coincidecomdentrode,geometriaaproximada,nomeabrev,nome,profundidademedia,id_trecho_curso_dagua,velocidademedcorrente,geom,larguramedia,regime,caladomax,navegabilidade) SELECT NEW.eixoprincipal,NEW.compartilhado,NEW.dentrodepoligono,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.profundidademedia,NEW.id_trecho_curso_dagua,NEW.velocidademedcorrente,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.larguramedia,NEW.regime,NEW.caladomax,NEW.navegabilidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_trecho_drenagem_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_trecho_drenagem_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_trecho_drenagem_l
    FOR EACH ROW EXECUTE PROCEDURE hid_trecho_drenagem_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_deposito_geral_p_avoid_multi () RETURNS TRIGGER AS $eco_deposito_geral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_deposito_geral_p(tratamento,valorvolume,unidadevolume,tipoconteudo,tipoprodutoresiduo,tipoexposicao,id_org_comerc_serv,id_org_ext_mineral,id_org_agropec_ext_veg_pesca,id_complexo_gerad_energ_eletr,nome,nomeabrev,geometriaaproximada,tipodepgeral,matconstr,operacional,situacaofisica,id_estrut_transporte,id_org_industrial,geom) SELECT NEW.tratamento,NEW.valorvolume,NEW.unidadevolume,NEW.tipoconteudo,NEW.tipoprodutoresiduo,NEW.tipoexposicao,NEW.id_org_comerc_serv,NEW.id_org_ext_mineral,NEW.id_org_agropec_ext_veg_pesca,NEW.id_complexo_gerad_energ_eletr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepgeral,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,NEW.id_org_industrial,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_deposito_geral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_deposito_geral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_deposito_geral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_deposito_geral_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_constr_portuaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_portuaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_portuaria_p(nome,id_complexo_portuario,administracao,tipoedifport,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.id_complexo_portuario,NEW.administracao,NEW.tipoedifport,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_portuaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_portuaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_portuaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_portuaria_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_travessia_l_avoid_multi () RETURNS TRIGGER AS $tra_travessia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_l(geometriaaproximada,tipotravessia,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,NEW.tipotravessia,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_l
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_travessia_p_avoid_multi () RETURNS TRIGGER AS $tra_travessia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_p(geometriaaproximada,tipotravessia,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,NEW.tipotravessia,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_p
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_duna_p_avoid_multi () RETURNS TRIGGER AS $rel_duna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_duna_p(tipoelemnat,nome,nomeabrev,geometriaaproximada,fixa,geom) SELECT NEW.tipoelemnat,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.fixa,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_duna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_duna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_duna_p
    FOR EACH ROW EXECUTE PROCEDURE rel_duna_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_plataforma_a_avoid_multi () RETURNS TRIGGER AS $eco_plataforma_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_plataforma_a(geom,tipoplataforma,nome,geometriaaproximada,nomeabrev) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoplataforma,NEW.nome,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_plataforma_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_plataforma_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_plataforma_a
    FOR EACH ROW EXECUTE PROCEDURE eco_plataforma_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_plataforma_p_avoid_multi () RETURNS TRIGGER AS $eco_plataforma_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_plataforma_p(geom,tipoplataforma,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoplataforma,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_plataforma_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_plataforma_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_plataforma_p
    FOR EACH ROW EXECUTE PROCEDURE eco_plataforma_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_torre_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_torre_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_torre_energia_p(situacaofisica,ovgd,alturaestimada,tipotorre,arranjofases,geom,nome,nomeabrev,geometriaaproximada,operacional) SELECT NEW.situacaofisica,NEW.ovgd,NEW.alturaestimada,NEW.tipotorre,NEW.arranjofases,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_torre_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_torre_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_torre_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_torre_energia_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE pto_pto_est_med_fenomenos_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_const_lazer_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_lazer_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_lazer_a(nomeabrev,nome,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoediflazer,id_complexo_lazer) SELECT NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoediflazer,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_lazer_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_lazer_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_lazer_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_lazer_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_deposito_geral_a_avoid_multi () RETURNS TRIGGER AS $eco_deposito_geral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_deposito_geral_a(valorvolume,geom,id_org_industrial,id_estrut_transporte,id_complexo_gerad_energ_eletr,id_org_agropec_ext_veg_pesca,id_org_ext_mineral,id_org_comerc_serv,tratamento,unidadevolume,tipoconteudo,tipoprodutoresiduo,tipoexposicao,matconstr,tipodepgeral,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome) SELECT NEW.valorvolume,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_industrial,NEW.id_estrut_transporte,NEW.id_complexo_gerad_energ_eletr,NEW.id_org_agropec_ext_veg_pesca,NEW.id_org_ext_mineral,NEW.id_org_comerc_serv,NEW.tratamento,NEW.unidadevolume,NEW.tipoconteudo,NEW.tipoprodutoresiduo,NEW.tipoexposicao,NEW.matconstr,NEW.tipodepgeral,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_deposito_geral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_deposito_geral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_deposito_geral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_deposito_geral_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_ponto_ferroviario_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_ferroviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_ferroviario_p(geom,relacionado,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.relacionado,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_ferroviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_ferroviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_ferroviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_ferroviario_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_const_lazer_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_lazer_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_lazer_p(situacaofisica,matconstr,geom,tipoediflazer,id_complexo_lazer,nome,nomeabrev,geometriaaproximada,operacional) SELECT NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoediflazer,NEW.id_complexo_lazer,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_lazer_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_lazer_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_lazer_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_lazer_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE sau_area_servico_social_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_area_duto_a_avoid_multi () RETURNS TRIGGER AS $tra_area_duto_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_area_duto_a(geom,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_area_duto_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_area_duto_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_area_duto_a
    FOR EACH ROW EXECUTE PROCEDURE tra_area_duto_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_marco_de_limite_p_avoid_multi () RETURNS TRIGGER AS $lim_marco_de_limite_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_marco_de_limite_p(referencialaltim,outrarefalt,orgresp,geom,latitude,longitude_gms,longitude,altitudeortometrica,sistemageodesico,outrarefplan,nome,nomeabrev,geometriaaproximada,tipomarcolim,latitude_gms) SELECT NEW.referencialaltim,NEW.outrarefalt,NEW.orgresp,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.latitude,NEW.longitude_gms,NEW.longitude,NEW.altitudeortometrica,NEW.sistemageodesico,NEW.outrarefplan,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipomarcolim,NEW.latitude_gms ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_marco_de_limite_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_marco_de_limite_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_marco_de_limite_p
    FOR EACH ROW EXECUTE PROCEDURE lim_marco_de_limite_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_duna_a_avoid_multi () RETURNS TRIGGER AS $rel_duna_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_duna_a(fixa,nome,nomeabrev,geometriaaproximada,tipoelemnat,geom) SELECT NEW.fixa,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_duna_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_duna_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_duna_a
    FOR EACH ROW EXECUTE PROCEDURE rel_duna_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_arruamento_l_avoid_multi () RETURNS TRIGGER AS $tra_arruamento_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_arruamento_l(nomeabrev,geom,canteirodivisorio,trafego,situacaofisica,nrfaixas,operacional,revestimento,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.canteirodivisorio,NEW.trafego,NEW.situacaofisica,NEW.nrfaixas,NEW.operacional,NEW.revestimento,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_arruamento_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_arruamento_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_arruamento_l
    FOR EACH ROW EXECUTE PROCEDURE tra_arruamento_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_recife_a_avoid_multi () RETURNS TRIGGER AS $hid_recife_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_a(situamare,tiporecife,geometriaaproximada,nomeabrev,nome,geom,situacaocosta) SELECT NEW.situamare,NEW.tiporecife,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaocosta ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_a
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_recife_l_avoid_multi () RETURNS TRIGGER AS $hid_recife_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_l(situacaocosta,tiporecife,geometriaaproximada,nomeabrev,nome,geom,situamare) SELECT NEW.situacaocosta,NEW.tiporecife,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situamare ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_l
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_recife_p_avoid_multi () RETURNS TRIGGER AS $hid_recife_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_recife_p(tiporecife,geometriaaproximada,nomeabrev,nome,geom,situacaocosta,situamare) SELECT NEW.tiporecife,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaocosta,NEW.situamare ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_recife_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_recife_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_recife_p
    FOR EACH ROW EXECUTE PROCEDURE hid_recife_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_area_urbana_isolada_a_avoid_multi () RETURNS TRIGGER AS $loc_area_urbana_isolada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_urbana_isolada_a(geom,nomeabrev,nome,geometriaaproximada,tipoassociado) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,NEW.tipoassociado ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_urbana_isolada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_urbana_isolada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_urbana_isolada_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_urbana_isolada_a_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE lim_pais_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_curva_batimetrica_l_avoid_multi () RETURNS TRIGGER AS $rel_curva_batimetrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_curva_batimetrica_l(geom,profundidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.profundidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_curva_batimetrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_curva_batimetrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_curva_batimetrica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_curva_batimetrica_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE rel_ponto_cotado_batimetrico_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_dep_abast_agua_p_avoid_multi () RETURNS TRIGGER AS $asb_dep_abast_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_abast_agua_p(tipodepabast,id_org_agropec_ext_veg_pesca,id_org_ext_mineral,id_complexo_abast_agua,operacional,situacaofisica,finalidade,matconstr,construcao,situacaoagua,nome,nomeabrev,geometriaaproximada,geom,id_org_industrial,id_org_comerc_serv) SELECT NEW.tipodepabast,NEW.id_org_agropec_ext_veg_pesca,NEW.id_org_ext_mineral,NEW.id_complexo_abast_agua,NEW.operacional,NEW.situacaofisica,NEW.finalidade,NEW.matconstr,NEW.construcao,NEW.situacaoagua,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_industrial,NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_abast_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_abast_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_abast_agua_p
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_abast_agua_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_gruta_caverna_p_avoid_multi () RETURNS TRIGGER AS $rel_gruta_caverna_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_gruta_caverna_p(tipogrutacaverna,nome,tipoelemnat,nomeabrev,geometriaaproximada,geom) SELECT NEW.tipogrutacaverna,NEW.nome,NEW.tipoelemnat,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_gruta_caverna_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_gruta_caverna_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_gruta_caverna_p
    FOR EACH ROW EXECUTE PROCEDURE rel_gruta_caverna_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_dep_abast_agua_a_avoid_multi () RETURNS TRIGGER AS $asb_dep_abast_agua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_abast_agua_a(id_org_comerc_serv,nome,nomeabrev,geometriaaproximada,tipodepabast,situacaoagua,construcao,matconstr,finalidade,situacaofisica,operacional,id_complexo_abast_agua,id_org_ext_mineral,id_org_agropec_ext_veg_pesca,geom,id_org_industrial) SELECT NEW.id_org_comerc_serv,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepabast,NEW.situacaoagua,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.situacaofisica,NEW.operacional,NEW.id_complexo_abast_agua,NEW.id_org_ext_mineral,NEW.id_org_agropec_ext_veg_pesca,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_industrial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_abast_agua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_abast_agua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_abast_agua_a
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_abast_agua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_a(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_l(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_caatinga_a_avoid_multi () RETURNS TRIGGER AS $veg_caatinga_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_caatinga_a(denso,nome,nomeabrev,geometriaaproximada,classificacaoporte,alturamediaindividuos,geom,antropizada) SELECT NEW.denso,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.classificacaoporte,NEW.alturamediaindividuos,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_caatinga_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_caatinga_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_caatinga_a
    FOR EACH ROW EXECUTE PROCEDURE veg_caatinga_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $rel_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_descontinuidade_geometrica_p(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE rel_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_dep_saneamento_a_avoid_multi () RETURNS TRIGGER AS $asb_dep_saneamento_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_saneamento_a(tipodepsaneam,geom,id_complexo_saneamento,tiporesiduo,residuo,situacaofisica,operacional,finalidade,matconstr,construcao,geometriaaproximada,nomeabrev,nome) SELECT NEW.tipodepsaneam,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_saneamento,NEW.tiporesiduo,NEW.residuo,NEW.situacaofisica,NEW.operacional,NEW.finalidade,NEW.matconstr,NEW.construcao,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_saneamento_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_saneamento_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_saneamento_a
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_saneamento_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_galeria_bueiro_l_avoid_multi () RETURNS TRIGGER AS $tra_galeria_bueiro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_galeria_bueiro_l(matconstr,operacional,situacaofisica,geom,nome,nomeabrev,pesosuportmaximo) SELECT NEW.matconstr,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.pesosuportmaximo ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_galeria_bueiro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_galeria_bueiro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_galeria_bueiro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_galeria_bueiro_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $sau_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_descontinuidade_geometrica_a(motivodescontinuidade,geom,geometriaaproximada) SELECT NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE sau_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_edif_habitacional_p_avoid_multi () RETURNS TRIGGER AS $loc_edif_habitacional_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edif_habitacional_p(nome,geometriaaproximada,operacional,situacaofisica,matconstr,geom,id_complexo_habitacional,nomeabrev) SELECT NEW.nome,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_habitacional,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edif_habitacional_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edif_habitacional_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edif_habitacional_p
    FOR EACH ROW EXECUTE PROCEDURE loc_edif_habitacional_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_galeria_bueiro_p_avoid_multi () RETURNS TRIGGER AS $tra_galeria_bueiro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_galeria_bueiro_p(nome,geom,situacaofisica,operacional,pesosuportmaximo,matconstr,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.operacional,NEW.pesosuportmaximo,NEW.matconstr,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_galeria_bueiro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_galeria_bueiro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_galeria_bueiro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_galeria_bueiro_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_politico_adm_a_avoid_multi () RETURNS TRIGGER AS $lim_area_politico_adm_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_politico_adm_a(nomeabrev,geom,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_politico_adm_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_politico_adm_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_politico_adm_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_politico_adm_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_edif_habitacional_a_avoid_multi () RETURNS TRIGGER AS $loc_edif_habitacional_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_edif_habitacional_a(geometriaaproximada,geom,id_complexo_habitacional,nomeabrev,nome,operacional,situacaofisica,matconstr) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_habitacional,NEW.nomeabrev,NEW.nome,NEW.operacional,NEW.situacaofisica,NEW.matconstr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_edif_habitacional_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_edif_habitacional_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_edif_habitacional_a
    FOR EACH ROW EXECUTE PROCEDURE loc_edif_habitacional_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $sau_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_descontinuidade_geometrica_p(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE sau_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_fundeadouro_p_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_p(id_complexo_portuario,nome,nomeabrev,geometriaaproximada,destinacaofundeadouro,administracao,geom) SELECT NEW.id_complexo_portuario,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.destinacaofundeadouro,NEW.administracao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_p
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_agrop_ext_veg_pesca_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_agrop_ext_veg_pesca_p(tipoedifagropec,matconstr,situacaofisica,operacional,nomeabrev,geometriaaproximada,nome,geom,id_org_agropec_ext_veg_pesca) SELECT NEW.tipoedifagropec,NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.nomeabrev,NEW.geometriaaproximada,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_agropec_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_agrop_ext_veg_pesca_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_agrop_ext_veg_pesca_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_agrop_ext_veg_pesca_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_constr_aeroportuaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_aeroportuaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_aeroportuaria_a(id_complexo_aeroportuario,administracao,tipoedifaero,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome) SELECT NEW.id_complexo_aeroportuario,NEW.administracao,NEW.tipoedifaero,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_aeroportuaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_aeroportuaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_aeroportuaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_aeroportuaria_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_area_ruinas_a_avoid_multi () RETURNS TRIGGER AS $edu_area_ruinas_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_ruinas_a(geom,id_complexo_lazer,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_lazer,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_ruinas_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_ruinas_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_ruinas_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_ruinas_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_fundeadouro_l_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_l(destinacaofundeadouro,geometriaaproximada,nomeabrev,geom,nome,id_complexo_portuario,administracao) SELECT NEW.destinacaofundeadouro,NEW.geometriaaproximada,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.id_complexo_portuario,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_l
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_agrop_ext_veg_pesca_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_agrop_ext_veg_pesca_a(matconstr,nomeabrev,geometriaaproximada,operacional,situacaofisica,nome,geom,tipoedifagropec,id_org_agropec_ext_veg_pesca) SELECT NEW.matconstr,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifagropec,NEW.id_org_agropec_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_agrop_ext_veg_pesca_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_agrop_ext_veg_pesca_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_agrop_ext_veg_pesca_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_fundeadouro_a_avoid_multi () RETURNS TRIGGER AS $tra_fundeadouro_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_fundeadouro_a(geometriaaproximada,destinacaofundeadouro,administracao,id_complexo_portuario,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,NEW.destinacaofundeadouro,NEW.administracao,NEW.id_complexo_portuario,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_fundeadouro_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_fundeadouro_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_fundeadouro_a
    FOR EACH ROW EXECUTE PROCEDURE tra_fundeadouro_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_constr_aeroportuaria_p_avoid_multi () RETURNS TRIGGER AS $tra_edif_constr_aeroportuaria_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_constr_aeroportuaria_p(id_complexo_aeroportuario,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifaero,administracao) SELECT NEW.id_complexo_aeroportuario,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifaero,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_constr_aeroportuaria_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_constr_aeroportuaria_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_constr_aeroportuaria_p
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_constr_aeroportuaria_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_de_litigio_a_avoid_multi () RETURNS TRIGGER AS $lim_area_de_litigio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_de_litigio_a(descricao,nome,nomeabrev,geometriaaproximada,geom) SELECT NEW.descricao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_de_litigio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_de_litigio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_de_litigio_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_de_litigio_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_edif_constr_est_med_fen_a_avoid_multi () RETURNS TRIGGER AS $pto_edif_constr_est_med_fen_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_edif_constr_est_med_fen_a(matconstr,geom,nomeabrev,operacional,geometriaaproximada,nome,situacaofisica) SELECT NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.operacional,NEW.geometriaaproximada,NEW.nome,NEW.situacaofisica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_edif_constr_est_med_fen_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_edif_constr_est_med_fen_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_edif_constr_est_med_fen_a
    FOR EACH ROW EXECUTE PROCEDURE pto_edif_constr_est_med_fen_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_edif_constr_est_med_fen_p_avoid_multi () RETURNS TRIGGER AS $pto_edif_constr_est_med_fen_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_edif_constr_est_med_fen_p(nomeabrev,geom,matconstr,situacaofisica,operacional,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_edif_constr_est_med_fen_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_edif_constr_est_med_fen_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_edif_constr_est_med_fen_p
    FOR EACH ROW EXECUTE PROCEDURE pto_edif_constr_est_med_fen_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_area_edificada_a_avoid_multi () RETURNS TRIGGER AS $loc_area_edificada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_edificada_a(geom,nome,nomeabrev,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_edificada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_edificada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_edificada_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_edificada_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_terra_publica_p_avoid_multi () RETURNS TRIGGER AS $lim_terra_publica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_terra_publica_p(nome,nomeabrev,classificacao,geom,geometriaaproximada) SELECT NEW.nome,NEW.nomeabrev,NEW.classificacao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_terra_publica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_terra_publica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_terra_publica_p
    FOR EACH ROW EXECUTE PROCEDURE lim_terra_publica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $adm_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_descontinuidade_geometrica_a(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE adm_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_caminho_aereo_l_avoid_multi () RETURNS TRIGGER AS $tra_caminho_aereo_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_caminho_aereo_l(nome,operacional,situacaofisica,geom,id_org_ext_mineral,id_complexo_lazer,nomeabrev,geometriaaproximada,tipocaminhoaereo,tipousocaminhoaer) SELECT NEW.nome,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_ext_mineral,NEW.id_complexo_lazer,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipocaminhoaereo,NEW.tipousocaminhoaer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_caminho_aereo_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_caminho_aereo_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_caminho_aereo_l
    FOR EACH ROW EXECUTE PROCEDURE tra_caminho_aereo_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_ciclovia_l_avoid_multi () RETURNS TRIGGER AS $tra_ciclovia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ciclovia_l(administracao,revestimento,operacional,situacaofisica,trafego,geom,nome,nomeabrev,geometriaaproximada) SELECT NEW.administracao,NEW.revestimento,NEW.operacional,NEW.situacaofisica,NEW.trafego,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ciclovia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ciclovia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ciclovia_l
    FOR EACH ROW EXECUTE PROCEDURE tra_ciclovia_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_ponto_cotado_altimetrico_p_avoid_multi () RETURNS TRIGGER AS $rel_ponto_cotado_altimetrico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_ponto_cotado_altimetrico_p(cotacomprovada,geometriaaproximada,geom,cota) SELECT NEW.cotacomprovada,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.cota ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_ponto_cotado_altimetrico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_ponto_cotado_altimetrico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_ponto_cotado_altimetrico_p
    FOR EACH ROW EXECUTE PROCEDURE rel_ponto_cotado_altimetrico_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_ponto_duto_p_avoid_multi () RETURNS TRIGGER AS $tra_ponto_duto_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_ponto_duto_p(relacionado,geometriaaproximada,geom) SELECT NEW.relacionado,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_ponto_duto_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_ponto_duto_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_ponto_duto_p
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_duto_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE adm_area_pub_civil_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_regiao_administrativa_a_avoid_multi () RETURNS TRIGGER AS $lim_regiao_administrativa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_regiao_administrativa_a(anodereferencia,geom,geometriaaproximada,nomeabrev,nome) SELECT NEW.anodereferencia,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_regiao_administrativa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_regiao_administrativa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_regiao_administrativa_a
    FOR EACH ROW EXECUTE PROCEDURE lim_regiao_administrativa_a_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $loc_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_descontinuidade_geometrica_l(motivodescontinuidade,geom,geometriaaproximada) SELECT NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_posto_combustivel_a_avoid_multi () RETURNS TRIGGER AS $tra_posto_combustivel_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_posto_combustivel_a(geom,id_estrut_transporte,matconstr,situacaofisica,operacional,administracao,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_estrut_transporte,NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.administracao,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_posto_combustivel_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_posto_combustivel_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_posto_combustivel_a
    FOR EACH ROW EXECUTE PROCEDURE tra_posto_combustivel_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_edif_energia_a_avoid_multi () RETURNS TRIGGER AS $enc_edif_energia_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_energia_a(geom,id_subestacao_ener_eletr,id_complexo_gerad_energ_eletr,tipoedifenergia,operacional,matconstr,situacaofisica,nome,nomeabrev,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_subestacao_ener_eletr,NEW.id_complexo_gerad_energ_eletr,NEW.tipoedifenergia,NEW.operacional,NEW.matconstr,NEW.situacaofisica,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_energia_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_energia_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_energia_a
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_energia_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $loc_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_descontinuidade_geometrica_p(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE loc_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_edif_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_edif_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_edif_energia_p(operacional,situacaofisica,matconstr,geom,tipoedifenergia,id_complexo_gerad_energ_eletr,id_subestacao_ener_eletr,nome,nomeabrev,geometriaaproximada) SELECT NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifenergia,NEW.id_complexo_gerad_energ_eletr,NEW.id_subestacao_ener_eletr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_edif_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_edif_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_edif_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_edif_energia_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_posto_combustivel_p_avoid_multi () RETURNS TRIGGER AS $tra_posto_combustivel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_posto_combustivel_p(matconstr,nome,nomeabrev,geometriaaproximada,administracao,operacional,situacaofisica,id_estrut_transporte,geom) SELECT NEW.matconstr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_posto_combustivel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_posto_combustivel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_posto_combustivel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_posto_combustivel_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_bacia_hidrografica_a_avoid_multi () RETURNS TRIGGER AS $hid_bacia_hidrografica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_bacia_hidrografica_a(nivelotto,geom,nome,nomeabrev,geometriaaproximada,codigootto) SELECT NEW.nivelotto,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.codigootto ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_bacia_hidrografica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_bacia_hidrografica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_bacia_hidrografica_a
    FOR EACH ROW EXECUTE PROCEDURE hid_bacia_hidrografica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_veg_area_contato_a_avoid_multi () RETURNS TRIGGER AS $veg_veg_area_contato_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_veg_area_contato_a(denso,nome,geometriaaproximada,classificacaoporte,nomeabrev,alturamediaindividuos,antropizada,geom) SELECT NEW.denso,NEW.nome,NEW.geometriaaproximada,NEW.classificacaoporte,NEW.nomeabrev,NEW.alturamediaindividuos,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_veg_area_contato_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_veg_area_contato_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_veg_area_contato_a
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_area_contato_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_uso_sustentavel_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_uso_sustentavel_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_uso_sustentavel_a(geometriaaproximada,geom,anocriacao,sigla,nome,nomeabrev,tipounidusosust,administracao,atolegal,areaoficialha) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.sigla,NEW.nome,NEW.nomeabrev,NEW.tipounidusosust,NEW.administracao,NEW.atolegal,NEW.areaoficialha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_uso_sustentavel_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_uso_sustentavel_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_uso_sustentavel_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_uso_sustentavel_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_uso_comunitario_p_avoid_multi () RETURNS TRIGGER AS $lim_area_uso_comunitario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_uso_comunitario_p(geometriaaproximada,tipoareausocomun,nome,nomeabrev,geom) SELECT NEW.geometriaaproximada,NEW.tipoareausocomun,NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_uso_comunitario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_uso_comunitario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_uso_comunitario_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_uso_comunitario_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_floresta_a_avoid_multi () RETURNS TRIGGER AS $veg_floresta_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_floresta_a(nomeabrev,nome,classificacaoporte,alturamediaindividuos,caracteristicafloresta,especiepredominante,geom,antropizada,denso,geometriaaproximada) SELECT NEW.nomeabrev,NEW.nome,NEW.classificacaoporte,NEW.alturamediaindividuos,NEW.caracteristicafloresta,NEW.especiepredominante,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_floresta_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_floresta_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_floresta_a
    FOR EACH ROW EXECUTE PROCEDURE veg_floresta_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_uso_comunitario_a_avoid_multi () RETURNS TRIGGER AS $lim_area_uso_comunitario_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_uso_comunitario_a(geometriaaproximada,tipoareausocomun,nome,nomeabrev,geom) SELECT NEW.geometriaaproximada,NEW.tipoareausocomun,NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_uso_comunitario_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_uso_comunitario_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_uso_comunitario_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_uso_comunitario_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $adm_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_descontinuidade_geometrica_p(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE adm_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_especial_p_avoid_multi () RETURNS TRIGGER AS $lim_area_especial_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_especial_p(geom,nome,nomeabrev,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_especial_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_especial_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_especial_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_especial_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_area_ensino_a_avoid_multi () RETURNS TRIGGER AS $edu_area_ensino_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_ensino_a(id_org_ensino,geom,geometriaaproximada) SELECT NEW.id_org_ensino,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_ensino_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_ensino_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_ensino_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_ensino_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_travessia_pedestre_l_avoid_multi () RETURNS TRIGGER AS $tra_travessia_pedestre_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_pedestre_l(geom,tipotravessiaped,matconstr,geometriaaproximada,nomeabrev,nome,operacional,situacaofisica,largura,extensao) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipotravessiaped,NEW.matconstr,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.operacional,NEW.situacaofisica,NEW.largura,NEW.extensao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_pedestre_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_pedestre_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_pedestre_l
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_pedestre_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_especial_a_avoid_multi () RETURNS TRIGGER AS $lim_area_especial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_especial_a(nomeabrev,geom,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_especial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_especial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_especial_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_especial_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_dep_saneamento_p_avoid_multi () RETURNS TRIGGER AS $asb_dep_saneamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_dep_saneamento_p(nome,residuo,tiporesiduo,id_complexo_saneamento,geom,nomeabrev,geometriaaproximada,tipodepsaneam,construcao,matconstr,finalidade,operacional,situacaofisica) SELECT NEW.nome,NEW.residuo,NEW.tiporesiduo,NEW.id_complexo_saneamento,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipodepsaneam,NEW.construcao,NEW.matconstr,NEW.finalidade,NEW.operacional,NEW.situacaofisica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_dep_saneamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_dep_saneamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_dep_saneamento_p
    FOR EACH ROW EXECUTE PROCEDURE asb_dep_saneamento_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_aglom_rural_de_ext_urbana_p_avoid_multi () RETURNS TRIGGER AS $loc_aglom_rural_de_ext_urbana_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_aglom_rural_de_ext_urbana_p(longitude,nome,nomeabrev,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude_gms,geom) SELECT NEW.longitude,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_aglom_rural_de_ext_urbana_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_aglom_rural_de_ext_urbana_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_aglom_rural_de_ext_urbana_p
    FOR EACH ROW EXECUTE PROCEDURE loc_aglom_rural_de_ext_urbana_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_travessia_pedestre_p_avoid_multi () RETURNS TRIGGER AS $tra_travessia_pedestre_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_travessia_pedestre_p(extensao,nome,nomeabrev,geometriaaproximada,tipotravessiaped,matconstr,operacional,situacaofisica,largura,geom) SELECT NEW.extensao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipotravessiaped,NEW.matconstr,NEW.operacional,NEW.situacaofisica,NEW.largura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_travessia_pedestre_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_travessia_pedestre_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_travessia_pedestre_p
    FOR EACH ROW EXECUTE PROCEDURE tra_travessia_pedestre_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_passag_elevada_viaduto_l_avoid_multi () RETURNS TRIGGER AS $tra_passag_elevada_viaduto_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passag_elevada_viaduto_l(nomeabrev,geom,largura,extensao,posicaopista,nrfaixas,nrpistas,cargasuportmaxima,gabvertsup,gabhorizsup,vaovertical,vaolivrehoriz,situacaofisica,operacional,matconstr,modaluso,tipopassagviad,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.largura,NEW.extensao,NEW.posicaopista,NEW.nrfaixas,NEW.nrpistas,NEW.cargasuportmaxima,NEW.gabvertsup,NEW.gabhorizsup,NEW.vaovertical,NEW.vaolivrehoriz,NEW.situacaofisica,NEW.operacional,NEW.matconstr,NEW.modaluso,NEW.tipopassagviad,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passag_elevada_viaduto_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passag_elevada_viaduto_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passag_elevada_viaduto_l
    FOR EACH ROW EXECUTE PROCEDURE tra_passag_elevada_viaduto_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_p(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_uso_sustentavel_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_uso_sustentavel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_uso_sustentavel_p(atolegal,administracao,tipounidusosust,geom,anocriacao,sigla,geometriaaproximada,nomeabrev,nome,areaoficialha) SELECT NEW.atolegal,NEW.administracao,NEW.tipounidusosust,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.anocriacao,NEW.sigla,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.areaoficialha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_uso_sustentavel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_uso_sustentavel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_uso_sustentavel_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_uso_sustentavel_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_l(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE tra_ponto_rodoviario_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION aux_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $aux_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.aux_descontinuidade_geometrica_a(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$aux_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER aux_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.aux_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE aux_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_protecao_integral_p_avoid_multi () RETURNS TRIGGER AS $lim_unidade_protecao_integral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_protecao_integral_p(geometriaaproximada,anocriacao,areaoficial,tipounidprotinteg,administracao,atolegal,sigla,nome,nomeabrev,geom) SELECT NEW.geometriaaproximada,NEW.anocriacao,NEW.areaoficial,NEW.tipounidprotinteg,NEW.administracao,NEW.atolegal,NEW.sigla,NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_protecao_integral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_protecao_integral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_protecao_integral_p
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_protecao_integral_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_area_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_area_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_ext_mineral_a(geometriaaproximada,geom,id_org_ext_mineral) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_ext_mineral ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_ext_mineral_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_protecao_integral_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_protecao_integral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_protecao_integral_a(anocriacao,nome,nomeabrev,geometriaaproximada,tipounidprotinteg,geom,sigla,administracao,atolegal,areaoficial) SELECT NEW.anocriacao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipounidprotinteg,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.sigla,NEW.administracao,NEW.atolegal,NEW.areaoficial ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_protecao_integral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_protecao_integral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_protecao_integral_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_protecao_integral_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_natureza_fundo_p_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_p(materialpredominante,nome,nomeabrev,geometriaaproximada,espessalgas,geom) SELECT NEW.materialpredominante,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.espessalgas,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_p
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_a_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_a(tipopista,nome,geom,id_complexo_aeroportuario,extensao,largura,situacaofisica,operacional,homologacao,usopista,revestimento,geometriaaproximada,nomeabrev) SELECT NEW.tipopista,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_aeroportuario,NEW.extensao,NEW.largura,NEW.situacaofisica,NEW.operacional,NEW.homologacao,NEW.usopista,NEW.revestimento,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_a
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $hid_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_descontinuidade_geometrica_p(motivodescontinuidade,geom,geometriaaproximada) SELECT NEW.motivodescontinuidade,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE hid_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_patio_p_avoid_multi () RETURNS TRIGGER AS $tra_patio_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_patio_p(geom,operacional,situacaofisica,id_estrut_transporte,id_org_ext_mineral,id_org_comerc_serv,id_org_agropec_ext_veg_pesca,id_org_industrial,id_org_ensino,id_complexo_lazer,geometriaaproximada,nomeabrev,nome,modaluso,administracao) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,NEW.id_org_ext_mineral,NEW.id_org_comerc_serv,NEW.id_org_agropec_ext_veg_pesca,NEW.id_org_industrial,NEW.id_org_ensino,NEW.id_complexo_lazer,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.modaluso,NEW.administracao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_patio_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_patio_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_patio_p
    FOR EACH ROW EXECUTE PROCEDURE tra_patio_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_dolina_a_avoid_multi () RETURNS TRIGGER AS $rel_dolina_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_dolina_a(geom,tipoelemnat,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoelemnat,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_dolina_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_dolina_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_dolina_a
    FOR EACH ROW EXECUTE PROCEDURE rel_dolina_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_l_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_l(largura,geom,id_complexo_aeroportuario,extensao,nome,nomeabrev,geometriaaproximada,tipopista,revestimento,usopista,homologacao,operacional,situacaofisica) SELECT NEW.largura,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_aeroportuario,NEW.extensao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipopista,NEW.revestimento,NEW.usopista,NEW.homologacao,NEW.operacional,NEW.situacaofisica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_l
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_natureza_fundo_a_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_a(geom,nome,nomeabrev,geometriaaproximada,materialpredominante,espessalgas) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.materialpredominante,NEW.espessalgas ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_a
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_pista_ponto_pouso_p_avoid_multi () RETURNS TRIGGER AS $tra_pista_ponto_pouso_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_pista_ponto_pouso_p(nome,geom,id_complexo_aeroportuario,extensao,largura,situacaofisica,operacional,homologacao,usopista,revestimento,tipopista,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_aeroportuario,NEW.extensao,NEW.largura,NEW.situacaofisica,NEW.operacional,NEW.homologacao,NEW.usopista,NEW.revestimento,NEW.tipopista,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_pista_ponto_pouso_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_pista_ponto_pouso_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_pista_ponto_pouso_p
    FOR EACH ROW EXECUTE PROCEDURE tra_pista_ponto_pouso_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_patio_a_avoid_multi () RETURNS TRIGGER AS $tra_patio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_patio_a(id_org_ext_mineral,nome,nomeabrev,geometriaaproximada,modaluso,administracao,operacional,situacaofisica,id_estrut_transporte,id_org_comerc_serv,id_org_agropec_ext_veg_pesca,id_org_industrial,id_org_ensino,id_complexo_lazer,geom) SELECT NEW.id_org_ext_mineral,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.modaluso,NEW.administracao,NEW.operacional,NEW.situacaofisica,NEW.id_estrut_transporte,NEW.id_org_comerc_serv,NEW.id_org_agropec_ext_veg_pesca,NEW.id_org_industrial,NEW.id_org_ensino,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_patio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_patio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_patio_a
    FOR EACH ROW EXECUTE PROCEDURE tra_patio_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_fonte_dagua_p_avoid_multi () RETURNS TRIGGER AS $hid_fonte_dagua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_fonte_dagua_p(qualidagua,geometriaaproximada,nomeabrev,nome,geom,regime,tipofontedagua) SELECT NEW.qualidagua,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.regime,NEW.tipofontedagua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_fonte_dagua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_fonte_dagua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_fonte_dagua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_fonte_dagua_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_eclusa_a_avoid_multi () RETURNS TRIGGER AS $tra_eclusa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_eclusa_a(extensao,largura,desnivel,nomeabrev,nome,geom,situacaofisica,operacional,geometriaaproximada,matconstr,calado) SELECT NEW.extensao,NEW.largura,NEW.desnivel,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.matconstr,NEW.calado ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_eclusa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_eclusa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_eclusa_a
    FOR EACH ROW EXECUTE PROCEDURE tra_eclusa_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_dolina_p_avoid_multi () RETURNS TRIGGER AS $rel_dolina_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_dolina_p(tipoelemnat,geom,geometriaaproximada,nomeabrev,nome) SELECT NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_dolina_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_dolina_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_dolina_p
    FOR EACH ROW EXECUTE PROCEDURE rel_dolina_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_pista_competicao_l_avoid_multi () RETURNS TRIGGER AS $edu_pista_competicao_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_pista_competicao_l(id_complexo_lazer,tipopista,geom,operacional,geometriaaproximada,nomeabrev,situacaofisica,nome) SELECT NEW.id_complexo_lazer,NEW.tipopista,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.situacaofisica,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_pista_competicao_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_pista_competicao_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_pista_competicao_l
    FOR EACH ROW EXECUTE PROCEDURE edu_pista_competicao_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_ilha_p_avoid_multi () RETURNS TRIGGER AS $hid_ilha_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_p(nome,tipoilha,geom,tipoelemnat,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.tipoilha,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoelemnat,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_p
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_area_industrial_a_avoid_multi () RETURNS TRIGGER AS $eco_area_industrial_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_industrial_a(id_org_industrial,geom,geometriaaproximada) SELECT NEW.id_org_industrial,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_industrial_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_industrial_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_industrial_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_industrial_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_ilha_l_avoid_multi () RETURNS TRIGGER AS $hid_ilha_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_l(tipoelemnat,tipoilha,geom,geometriaaproximada,nomeabrev,nome) SELECT NEW.tipoelemnat,NEW.tipoilha,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_l
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_area_religiosa_a_avoid_multi () RETURNS TRIGGER AS $edu_area_religiosa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_area_religiosa_a(geom,geometriaaproximada,id_org_religiosa) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.id_org_religiosa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_area_religiosa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_area_religiosa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_area_religiosa_a
    FOR EACH ROW EXECUTE PROCEDURE edu_area_religiosa_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_ilha_a_avoid_multi () RETURNS TRIGGER AS $hid_ilha_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_ilha_a(geom,nome,nomeabrev,geometriaaproximada,tipoelemnat,tipoilha) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoelemnat,NEW.tipoilha ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_ilha_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_ilha_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_ilha_a
    FOR EACH ROW EXECUTE PROCEDURE hid_ilha_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_barragem_a_avoid_multi () RETURNS TRIGGER AS $hid_barragem_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_a(geom,geometriaaproximada,nomeabrev,nome,id_complexo_gerad_energ_eletr,situacaofisica,operacional,usoprincipal,matconstr) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.id_complexo_gerad_energ_eletr,NEW.situacaofisica,NEW.operacional,NEW.usoprincipal,NEW.matconstr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_a
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_area_saude_a_avoid_multi () RETURNS TRIGGER AS $sau_area_saude_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_area_saude_a(geom,geometriaaproximada,id_org_saude) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.id_org_saude ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_area_saude_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_area_saude_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_area_saude_a
    FOR EACH ROW EXECUTE PROCEDURE sau_area_saude_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_barragem_l_avoid_multi () RETURNS TRIGGER AS $hid_barragem_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_barragem_l(nome,nomeabrev,geometriaaproximada,matconstr,usoprincipal,operacional,geom,id_complexo_gerad_energ_eletr,situacaofisica) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.matconstr,NEW.usoprincipal,NEW.operacional,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.situacaofisica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_barragem_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_barragem_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_barragem_l
    FOR EACH ROW EXECUTE PROCEDURE hid_barragem_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE lim_outros_limites_oficiais_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_edif_pub_militar_a_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_militar_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_militar_a(tipousoedif,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifmil,id_org_pub_militar) SELECT NEW.tipousoedif,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifmil,NEW.id_org_pub_militar ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_militar_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_militar_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_militar_a
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_militar_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_area_agrop_ext_veg_pesca_a_avoid_multi () RETURNS TRIGGER AS $eco_area_agrop_ext_veg_pesca_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_agrop_ext_veg_pesca_a(id_org_agropec_ext_veg_pesca,destinadoa,geometriaaproximada,geom) SELECT NEW.id_org_agropec_ext_veg_pesca,NEW.destinadoa,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_agrop_ext_veg_pesca_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_agrop_ext_veg_pesca_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_agrop_ext_veg_pesca_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_agrop_ext_veg_pesca_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $lim_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_descontinuidade_geometrica_p(geom,motivodescontinuidade,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE lim_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_edif_pub_militar_p_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_militar_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_militar_p(tipousoedif,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,tipoedifmil,id_org_pub_militar,nome) SELECT NEW.tipousoedif,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifmil,NEW.id_org_pub_militar,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_militar_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_militar_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_militar_p
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_militar_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE enc_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_trecho_hidroviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_hidroviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_hidroviario_l(geometriaaproximada,nomeabrev,id_hidrovia,geom,caladomaxseca,extensaotrecho,regime,situacaofisica,nome,operacional) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.id_hidrovia,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.caladomaxseca,NEW.extensaotrecho,NEW.regime,NEW.situacaofisica,NEW.nome,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_hidroviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_hidroviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_hidroviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_hidroviario_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_cultivada_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_identific_trecho_rod_p_avoid_multi () RETURNS TRIGGER AS $tra_identific_trecho_rod_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_identific_trecho_rod_p(nomeabrev,nome,id_via_rodoviaria,geom,sigla) SELECT NEW.nomeabrev,NEW.nome,NEW.id_via_rodoviaria,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.sigla ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_identific_trecho_rod_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_identific_trecho_rod_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_identific_trecho_rod_p
    FOR EACH ROW EXECUTE PROCEDURE tra_identific_trecho_rod_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $enc_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_descontinuidade_geometrica_a(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_curva_nivel_l_avoid_multi () RETURNS TRIGGER AS $rel_curva_nivel_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_curva_nivel_l(geom,indice,depressao,cota,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.indice,NEW.depressao,NEW.cota,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_curva_nivel_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_curva_nivel_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_curva_nivel_l
    FOR EACH ROW EXECUTE PROCEDURE rel_curva_nivel_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_trecho_massa_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_trecho_massa_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_trecho_massa_dagua_a(nome,tipotrechomassa,regime,salinidade,id_trecho_curso_dagua,geom,nomeabrev) SELECT NEW.nome,NEW.tipotrechomassa,NEW.regime,NEW.salinidade,NEW.id_trecho_curso_dagua,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_trecho_massa_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_trecho_massa_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_trecho_massa_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_trecho_massa_dagua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_reservatorio_hidrico_a_avoid_multi () RETURNS TRIGGER AS $hid_reservatorio_hidrico_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_reservatorio_hidrico_a(geometriaaproximada,usoprincipal,volumeutil,namaximomaximorum,namaximooperacional,id_complexo_gerad_energ_eletr,geom,nome,nomeabrev) SELECT NEW.geometriaaproximada,NEW.usoprincipal,NEW.volumeutil,NEW.namaximomaximorum,NEW.namaximooperacional,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_reservatorio_hidrico_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_reservatorio_hidrico_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_reservatorio_hidrico_a
    FOR EACH ROW EXECUTE PROCEDURE hid_reservatorio_hidrico_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_antena_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_antena_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_antena_comunic_p(nomeabrev,id_complexo_comunicacao,geom,posicaoreledific,geometriaaproximada,nome) SELECT NEW.nomeabrev,NEW.id_complexo_comunicacao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.posicaoreledific,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_antena_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_antena_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_antena_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_antena_comunic_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_edif_servico_social_p_avoid_multi () RETURNS TRIGGER AS $sau_edif_servico_social_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_servico_social_p(nomeabrev,operacional,situacaofisica,matconstr,geom,nome,id_org_servico_social,tipoclassecnae,geometriaaproximada) SELECT NEW.nomeabrev,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.id_org_servico_social,NEW.tipoclassecnae,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_servico_social_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_servico_social_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_servico_social_p
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_servico_social_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION sau_edif_servico_social_a_avoid_multi () RETURNS TRIGGER AS $sau_edif_servico_social_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.sau_edif_servico_social_a(tipoclassecnae,geom,nome,nomeabrev,matconstr,situacaofisica,operacional,geometriaaproximada,id_org_servico_social) SELECT NEW.tipoclassecnae,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.id_org_servico_social ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$sau_edif_servico_social_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER sau_edif_servico_social_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.sau_edif_servico_social_a
    FOR EACH ROW EXECUTE PROCEDURE sau_edif_servico_social_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_entroncamento_p_avoid_multi () RETURNS TRIGGER AS $tra_entroncamento_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_entroncamento_p(geom,tipoentroncamento,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoentroncamento,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_entroncamento_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_entroncamento_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_entroncamento_p
    FOR EACH ROW EXECUTE PROCEDURE tra_entroncamento_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_trecho_rodoviario_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_rodoviario_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_rodoviario_l(administracao,operacional,revestimento,concessionaria,jurisdicao,tipotrechorod,codtrechorodov,geometriaaproximada,situacaofisica,nrpistas,nrfaixas,trafego,canteirodivisorio,geom,id_via_rodoviaria) SELECT NEW.administracao,NEW.operacional,NEW.revestimento,NEW.concessionaria,NEW.jurisdicao,NEW.tipotrechorod,NEW.codtrechorodov,NEW.geometriaaproximada,NEW.situacaofisica,NEW.nrpistas,NEW.nrfaixas,NEW.trafego,NEW.canteirodivisorio,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_via_rodoviaria ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_rodoviario_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_rodoviario_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_rodoviario_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_rodoviario_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_confluencia_p_avoid_multi () RETURNS TRIGGER AS $hid_confluencia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_confluencia_p(geom,relacionado,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.relacionado,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_confluencia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_confluencia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_confluencia_p
    FOR EACH ROW EXECUTE PROCEDURE hid_confluencia_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_trecho_duto_l_avoid_multi () RETURNS TRIGGER AS $tra_trecho_duto_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trecho_duto_l(situacaoespacial,operacional,setor,situacaofisica,id_duto,posicaorelativa,geom,matconstr,ndutos,mattransp,tipotrechoduto,geometriaaproximada,nomeabrev,nome) SELECT NEW.situacaoespacial,NEW.operacional,NEW.setor,NEW.situacaofisica,NEW.id_duto,NEW.posicaorelativa,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.ndutos,NEW.mattransp,NEW.tipotrechoduto,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trecho_duto_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trecho_duto_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trecho_duto_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trecho_duto_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_pico_p_avoid_multi () RETURNS TRIGGER AS $rel_pico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_pico_p(nomeabrev,geom,nome,geometriaaproximada,tipoelemnat) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada,NEW.tipoelemnat ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_pico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_pico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_pico_p
    FOR EACH ROW EXECUTE PROCEDURE rel_pico_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_ext_mineral_p_avoid_multi () RETURNS TRIGGER AS $eco_edif_ext_mineral_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_ext_mineral_p(nome,id_org_ext_mineral,tipodivisaocnae,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.id_org_ext_mineral,NEW.tipodivisaocnae,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_ext_mineral_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_ext_mineral_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_ext_mineral_p
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_ext_mineral_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_cidade_p_avoid_multi () RETURNS TRIGGER AS $loc_cidade_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_cidade_p(nomeabrev,nome,geometriaaproximada,geocodigo,identificador,latitude,latitude_gms,longitude,longitude_gms,geom) SELECT NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,NEW.geocodigo,NEW.identificador,NEW.latitude,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_cidade_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_cidade_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_cidade_p
    FOR EACH ROW EXECUTE PROCEDURE loc_cidade_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_capital_p_avoid_multi () RETURNS TRIGGER AS $loc_capital_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_capital_p(latitude,geocodigo,geometriaaproximada,nomeabrev,nome,latitude_gms,longitude,longitude_gms,geom,tipocapital,identificador) SELECT NEW.latitude,NEW.geocodigo,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.latitude_gms,NEW.longitude,NEW.longitude_gms,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipocapital,NEW.identificador ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_capital_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_capital_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_capital_p
    FOR EACH ROW EXECUTE PROCEDURE loc_capital_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_edif_ext_mineral_a_avoid_multi () RETURNS TRIGGER AS $eco_edif_ext_mineral_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_edif_ext_mineral_a(nome,id_org_ext_mineral,tipodivisaocnae,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,NEW.id_org_ext_mineral,NEW.tipodivisaocnae,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_edif_ext_mineral_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_edif_ext_mineral_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_edif_ext_mineral_a
    FOR EACH ROW EXECUTE PROCEDURE eco_edif_ext_mineral_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_distrito_a_avoid_multi () RETURNS TRIGGER AS $lim_distrito_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_distrito_a(nome,geom,geocodigo,anodereferencia,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geocodigo,NEW.anodereferencia,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_distrito_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_distrito_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_distrito_a
    FOR EACH ROW EXECUTE PROCEDURE lim_distrito_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_passag_elevada_viaduto_p_avoid_multi () RETURNS TRIGGER AS $tra_passag_elevada_viaduto_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passag_elevada_viaduto_p(largura,extensao,posicaopista,modaluso,matconstr,situacaofisica,vaolivrehoriz,vaovertical,gabhorizsup,operacional,gabvertsup,cargasuportmaxima,geometriaaproximada,nomeabrev,nome,nrpistas,nrfaixas,geom,tipopassagviad) SELECT NEW.largura,NEW.extensao,NEW.posicaopista,NEW.modaluso,NEW.matconstr,NEW.situacaofisica,NEW.vaolivrehoriz,NEW.vaovertical,NEW.gabhorizsup,NEW.operacional,NEW.gabvertsup,NEW.cargasuportmaxima,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.nrpistas,NEW.nrfaixas,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipopassagviad ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passag_elevada_viaduto_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passag_elevada_viaduto_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passag_elevada_viaduto_p
    FOR EACH ROW EXECUTE PROCEDURE tra_passag_elevada_viaduto_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_torre_comunic_p_avoid_multi () RETURNS TRIGGER AS $enc_torre_comunic_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_torre_comunic_p(geom,geometriaaproximada,nomeabrev,nome,situacaofisica,posicaoreledific,ovgd,alturaestimada,id_complexo_comunicacao,operacional) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.situacaofisica,NEW.posicaoreledific,NEW.ovgd,NEW.alturaestimada,NEW.id_complexo_comunicacao,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_torre_comunic_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_torre_comunic_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_torre_comunic_p
    FOR EACH ROW EXECUTE PROCEDURE enc_torre_comunic_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_const_turistica_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_turistica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_turistica_a(situacaofisica,operacional,id_complexo_lazer,ovgd,tipoedifturist,geom,matconstr,nome,nomeabrev,geometriaaproximada) SELECT NEW.situacaofisica,NEW.operacional,NEW.id_complexo_lazer,NEW.ovgd,NEW.tipoedifturist,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_turistica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_turistica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_turistica_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_turistica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_terreno_exposto_a_avoid_multi () RETURNS TRIGGER AS $rel_terreno_exposto_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_terreno_exposto_a(geometriaaproximada,geom,causaexposicao,tipoterrexp) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.causaexposicao,NEW.tipoterrexp ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_terreno_exposto_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_terreno_exposto_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_terreno_exposto_a
    FOR EACH ROW EXECUTE PROCEDURE rel_terreno_exposto_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_posto_pol_rod_p_avoid_multi () RETURNS TRIGGER AS $adm_posto_pol_rod_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_pol_rod_p(tipopostopol,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,id_org_pub_militar,id_org_pub_civil,geom) SELECT NEW.tipopostopol,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.id_org_pub_militar,NEW.id_org_pub_civil,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_pol_rod_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_pol_rod_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_pol_rod_p
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_pol_rod_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_girador_ferroviario_p_avoid_multi () RETURNS TRIGGER AS $tra_girador_ferroviario_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_girador_ferroviario_p(id_estrut_apoio,administracao,geometriaaproximada,nomeabrev,nome,operacional,situacaofisica,geom) SELECT NEW.id_estrut_apoio,NEW.administracao,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.operacional,NEW.situacaofisica,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_girador_ferroviario_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_girador_ferroviario_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_girador_ferroviario_p
    FOR EACH ROW EXECUTE PROCEDURE tra_girador_ferroviario_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_trilha_picada_l_avoid_multi () RETURNS TRIGGER AS $tra_trilha_picada_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_trilha_picada_l(geom,nome,nomeabrev,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_trilha_picada_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_trilha_picada_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_trilha_picada_l
    FOR EACH ROW EXECUTE PROCEDURE tra_trilha_picada_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION pto_area_est_med_fenom_a_avoid_multi () RETURNS TRIGGER AS $pto_area_est_med_fenom_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.pto_area_est_med_fenom_a(geometriaaproximada,geom,id_est_med_fenomenos) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_est_med_fenomenos ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$pto_area_est_med_fenom_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER pto_area_est_med_fenom_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.pto_area_est_med_fenom_a
    FOR EACH ROW EXECUTE PROCEDURE pto_area_est_med_fenom_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_const_turistica_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_const_turistica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_const_turistica_p(situacaofisica,nome,nomeabrev,geometriaaproximada,operacional,geom,matconstr,id_complexo_lazer,ovgd,tipoedifturist) SELECT NEW.situacaofisica,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.id_complexo_lazer,NEW.ovgd,NEW.tipoedifturist ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_const_turistica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_const_turistica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_const_turistica_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_const_turistica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_posto_pol_rod_a_avoid_multi () RETURNS TRIGGER AS $adm_posto_pol_rod_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_pol_rod_a(nomeabrev,nome,geom,id_org_pub_civil,id_org_pub_militar,situacaofisica,operacional,geometriaaproximada,tipopostopol) SELECT NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_pub_civil,NEW.id_org_pub_militar,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.tipopostopol ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_pol_rod_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_pol_rod_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_pol_rod_a
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_pol_rod_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_trecho_comunic_l_avoid_multi () RETURNS TRIGGER AS $enc_trecho_comunic_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_trecho_comunic_l(id_org_comerc_serv,geom,geometriaaproximada,nomeabrev,nome,matconstr,posicaorelativa,tipotrechocomunic,operacional,situacaofisica,emduto) SELECT NEW.id_org_comerc_serv,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.matconstr,NEW.posicaorelativa,NEW.tipotrechocomunic,NEW.operacional,NEW.situacaofisica,NEW.emduto ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_trecho_comunic_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_trecho_comunic_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_trecho_comunic_l
    FOR EACH ROW EXECUTE PROCEDURE enc_trecho_comunic_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_banco_areia_a_avoid_multi () RETURNS TRIGGER AS $hid_banco_areia_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_banco_areia_a(situacaoemagua,materialpredominante,geom,nome,nomeabrev,geometriaaproximada,tipobanco) SELECT NEW.situacaoemagua,NEW.materialpredominante,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipobanco ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_banco_areia_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_banco_areia_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_banco_areia_a
    FOR EACH ROW EXECUTE PROCEDURE hid_banco_areia_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_banco_areia_l_avoid_multi () RETURNS TRIGGER AS $hid_banco_areia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_banco_areia_l(materialpredominante,geom,nomeabrev,nome,geometriaaproximada,tipobanco,situacaoemagua) SELECT NEW.materialpredominante,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,NEW.tipobanco,NEW.situacaoemagua ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_banco_areia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_banco_areia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_banco_areia_l
    FOR EACH ROW EXECUTE PROCEDURE hid_banco_areia_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_veg_restinga_a_avoid_multi () RETURNS TRIGGER AS $veg_veg_restinga_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_veg_restinga_a(alturamediaindividuos,classificacaoporte,nome,nomeabrev,geometriaaproximada,denso,antropizada,geom) SELECT NEW.alturamediaindividuos,NEW.classificacaoporte,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.denso,NEW.antropizada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_veg_restinga_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_veg_restinga_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_veg_restinga_a
    FOR EACH ROW EXECUTE PROCEDURE veg_veg_restinga_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_corredeira_p_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_p(geom,geometriaaproximada,nomeabrev,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_p
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_p_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE tra_faixa_seguranca_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_ensino_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_ensino_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_ensino_a(nomeabrev,nome,id_org_ensino,tipoclassecnae,geom,matconstr,situacaofisica,operacional,geometriaaproximada) SELECT NEW.nomeabrev,NEW.nome,NEW.id_org_ensino,NEW.tipoclassecnae,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_ensino_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_ensino_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_ensino_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_ensino_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_corredeira_a_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_a(geometriaaproximada,nome,geom,nomeabrev) SELECT NEW.geometriaaproximada,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_a
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_ensino_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_ensino_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_ensino_p(tipoclassecnae,geom,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome,id_org_ensino) SELECT NEW.tipoclassecnae,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.id_org_ensino ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_ensino_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_ensino_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_ensino_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_ensino_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_ponto_trecho_energia_p_avoid_multi () RETURNS TRIGGER AS $enc_ponto_trecho_energia_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_ponto_trecho_energia_p(geometriaaproximada,geom,tipoptoenergia) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoptoenergia ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_ponto_trecho_energia_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_ponto_trecho_energia_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_ponto_trecho_energia_p
    FOR EACH ROW EXECUTE PROCEDURE enc_ponto_trecho_energia_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $hid_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_descontinuidade_geometrica_l(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE hid_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $veg_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_descontinuidade_geometrica_l(geom,geometriaaproximada,motivodescontinuidade) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE veg_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_corredeira_l_avoid_multi () RETURNS TRIGGER AS $hid_corredeira_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_corredeira_l(geom,geometriaaproximada,nome,nomeabrev) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_corredeira_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_corredeira_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_corredeira_l
    FOR EACH ROW EXECUTE PROCEDURE hid_corredeira_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_desenv_controle_a_avoid_multi () RETURNS TRIGGER AS $lim_area_desenv_controle_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_desenv_controle_a(geom,classificacao,nome,nomeabrev,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.classificacao,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_desenv_controle_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_desenv_controle_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_desenv_controle_a
    FOR EACH ROW EXECUTE PROCEDURE lim_area_desenv_controle_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_posto_fiscal_a_avoid_multi () RETURNS TRIGGER AS $adm_posto_fiscal_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_fiscal_a(situacaofisica,geometriaaproximada,nomeabrev,geom,nome,id_org_pub_civil,tipopostofisc,operacional) SELECT NEW.situacaofisica,NEW.geometriaaproximada,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.id_org_pub_civil,NEW.tipopostofisc,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_fiscal_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_fiscal_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_fiscal_a
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_fiscal_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_natureza_fundo_l_avoid_multi () RETURNS TRIGGER AS $hid_natureza_fundo_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_natureza_fundo_l(geometriaaproximada,nomeabrev,nome,geom,espessalgas,materialpredominante) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.espessalgas,NEW.materialpredominante ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_natureza_fundo_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_natureza_fundo_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_natureza_fundo_l
    FOR EACH ROW EXECUTE PROCEDURE hid_natureza_fundo_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_area_desenv_controle_p_avoid_multi () RETURNS TRIGGER AS $lim_area_desenv_controle_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_area_desenv_controle_p(geometriaaproximada,classificacao,nome,nomeabrev,geom) SELECT NEW.geometriaaproximada,NEW.classificacao,NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_area_desenv_controle_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_area_desenv_controle_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_area_desenv_controle_p
    FOR EACH ROW EXECUTE PROCEDURE lim_area_desenv_controle_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_posto_fiscal_p_avoid_multi () RETURNS TRIGGER AS $adm_posto_fiscal_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_posto_fiscal_p(geom,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipopostofisc,id_org_pub_civil) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipopostofisc,NEW.id_org_pub_civil ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_posto_fiscal_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_posto_fiscal_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_posto_fiscal_p
    FOR EACH ROW EXECUTE PROCEDURE adm_posto_fiscal_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_passagem_nivel_p_avoid_multi () RETURNS TRIGGER AS $tra_passagem_nivel_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_passagem_nivel_p(nomeabrev,geom,nome,geometriaaproximada) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_passagem_nivel_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_passagem_nivel_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_passagem_nivel_p
    FOR EACH ROW EXECUTE PROCEDURE tra_passagem_nivel_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_zona_linhas_energia_com_a_avoid_multi () RETURNS TRIGGER AS $enc_zona_linhas_energia_com_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_zona_linhas_energia_com_a(nome,geom,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_zona_linhas_energia_com_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_zona_linhas_energia_com_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_zona_linhas_energia_com_a
    FOR EACH ROW EXECUTE PROCEDURE enc_zona_linhas_energia_com_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_sub_distrito_a_avoid_multi () RETURNS TRIGGER AS $lim_sub_distrito_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_sub_distrito_a(nomeabrev,geocodigo,anodereferencia,geometriaaproximada,geom,nome) SELECT NEW.nomeabrev,NEW.geocodigo,NEW.anodereferencia,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_sub_distrito_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_sub_distrito_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_sub_distrito_a
    FOR EACH ROW EXECUTE PROCEDURE lim_sub_distrito_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_rocha_a_avoid_multi () RETURNS TRIGGER AS $rel_rocha_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_rocha_a(geom,tiporocha,nome,geometriaaproximada,nomeabrev,tipoelemnat) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tiporocha,NEW.nome,NEW.geometriaaproximada,NEW.nomeabrev,NEW.tipoelemnat ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_rocha_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_rocha_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_rocha_a
    FOR EACH ROW EXECUTE PROCEDURE rel_rocha_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_area_estrut_transporte_a_avoid_multi () RETURNS TRIGGER AS $tra_area_estrut_transporte_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_area_estrut_transporte_a(geom,id_estrut_transporte,geometriaaproximada) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_estrut_transporte,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_area_estrut_transporte_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_area_estrut_transporte_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_area_estrut_transporte_a
    FOR EACH ROW EXECUTE PROCEDURE tra_area_estrut_transporte_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_area_umida_a_avoid_multi () RETURNS TRIGGER AS $hid_area_umida_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_area_umida_a(geom,nomeabrev,geometriaaproximada,tipoareaumida,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoareaumida,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_area_umida_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_area_umida_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_area_umida_a
    FOR EACH ROW EXECUTE PROCEDURE hid_area_umida_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_termeletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_termeletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_termeletrica_a(id_complexo_gerad_energ_eletr,nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,potenciafiscalizada,geracao,tipomaqtermica,combrenovavel,tipocombustivel,geom) SELECT NEW.id_complexo_gerad_energ_eletr,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.potenciafiscalizada,NEW.geracao,NEW.tipomaqtermica,NEW.combrenovavel,NEW.tipocombustivel,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_termeletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_termeletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_termeletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_termeletrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_termeletrica_p_avoid_multi () RETURNS TRIGGER AS $enc_termeletrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_termeletrica_p(operacional,tipoestgerad,geometriaaproximada,nomeabrev,tipomaqtermica,nome,geracao,combrenovavel,tipocombustivel,geom,id_complexo_gerad_energ_eletr,potenciafiscalizada,potenciaoutorgada,codigoestacao,destenergelet,situacaofisica) SELECT NEW.operacional,NEW.tipoestgerad,NEW.geometriaaproximada,NEW.nomeabrev,NEW.tipomaqtermica,NEW.nome,NEW.geracao,NEW.combrenovavel,NEW.tipocombustivel,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.potenciaoutorgada,NEW.codigoestacao,NEW.destenergelet,NEW.situacaofisica ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_termeletrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_termeletrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_termeletrica_p
    FOR EACH ROW EXECUTE PROCEDURE enc_termeletrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_hidreletrica_l_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_l(geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,geom,id_complexo_gerad_energ_eletr,potenciafiscalizada,nome,potenciaoutorgada,codigoestacao,codigohidreletrica,nomeabrev) SELECT NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.nome,NEW.potenciaoutorgada,NEW.codigoestacao,NEW.codigohidreletrica,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_l
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_area_comerc_serv_a_avoid_multi () RETURNS TRIGGER AS $eco_area_comerc_serv_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_area_comerc_serv_a(id_org_comerc_serv,geom,geometriaaproximada) SELECT NEW.id_org_comerc_serv,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_area_comerc_serv_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_area_comerc_serv_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_area_comerc_serv_a
    FOR EACH ROW EXECUTE PROCEDURE eco_area_comerc_serv_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_hidreletrica_a_avoid_multi () RETURNS TRIGGER AS $enc_hidreletrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_hidreletrica_a(destenergelet,codigohidreletrica,geom,id_complexo_gerad_energ_eletr,potenciafiscalizada,potenciaoutorgada,codigoestacao,situacaofisica,operacional,tipoestgerad,geometriaaproximada,nomeabrev,nome) SELECT NEW.destenergelet,NEW.codigohidreletrica,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.potenciaoutorgada,NEW.codigoestacao,NEW.situacaofisica,NEW.operacional,NEW.tipoestgerad,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_hidreletrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_hidreletrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_hidreletrica_a
    FOR EACH ROW EXECUTE PROCEDURE enc_hidreletrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_campo_a_avoid_multi () RETURNS TRIGGER AS $veg_campo_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_campo_a(nome,geom,ocorrenciaem,tipocampo,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.ocorrenciaem,NEW.tipocampo,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_campo_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_campo_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_campo_a
    FOR EACH ROW EXECUTE PROCEDURE veg_campo_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_vila_p_avoid_multi () RETURNS TRIGGER AS $loc_vila_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_vila_p(longitude_gms,longitude,latitude_gms,latitude,identificador,geocodigo,geometriaaproximada,nomeabrev,nome,geom) SELECT NEW.longitude_gms,NEW.longitude,NEW.latitude_gms,NEW.latitude,NEW.identificador,NEW.geocodigo,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_vila_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_vila_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_vila_p
    FOR EACH ROW EXECUTE PROCEDURE loc_vila_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_funicular_p_avoid_multi () RETURNS TRIGGER AS $tra_funicular_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_funicular_p(id_complexo_lazer,id_org_ext_mineral,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome,geom) SELECT NEW.id_complexo_lazer,NEW.id_org_ext_mineral,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_funicular_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_funicular_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_funicular_p
    FOR EACH ROW EXECUTE PROCEDURE tra_funicular_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_p(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_descontinuidade_geometrica_p_avoid_multi () RETURNS TRIGGER AS $veg_descontinuidade_geometrica_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_descontinuidade_geometrica_p(motivodescontinuidade,geometriaaproximada,geom) SELECT NEW.motivodescontinuidade,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_descontinuidade_geometrica_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_descontinuidade_geometrica_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_descontinuidade_geometrica_p
    FOR EACH ROW EXECUTE PROCEDURE veg_descontinuidade_geometrica_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_unidade_federacao_a_avoid_multi () RETURNS TRIGGER AS $lim_unidade_federacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_unidade_federacao_a(geometriaaproximada,nomeabrev,nome,geocodigo,sigla,geom) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.geocodigo,NEW.sigla,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_unidade_federacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_unidade_federacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_unidade_federacao_a
    FOR EACH ROW EXECUTE PROCEDURE lim_unidade_federacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_limite_area_especial_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_area_especial_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_area_especial_l(tipolimareaesp,nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom,obssituacao) SELECT NEW.tipolimareaesp,NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.obssituacao ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_area_especial_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_area_especial_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_area_especial_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_area_especial_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_a_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_a(geometriaaproximada,geom,motivodescontinuidade) SELECT NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.motivodescontinuidade ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_a
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_funicular_l_avoid_multi () RETURNS TRIGGER AS $tra_funicular_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_funicular_l(geometriaaproximada,nomeabrev,nome,id_complexo_lazer,operacional,situacaofisica,id_org_ext_mineral,geom) SELECT NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.id_complexo_lazer,NEW.operacional,NEW.situacaofisica,NEW.id_org_ext_mineral,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_funicular_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_funicular_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_funicular_l
    FOR EACH ROW EXECUTE PROCEDURE tra_funicular_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_descontinuidade_geometrica_l_avoid_multi () RETURNS TRIGGER AS $asb_descontinuidade_geometrica_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_descontinuidade_geometrica_l(motivodescontinuidade,geometriaaproximada,geom) SELECT NEW.motivodescontinuidade,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_descontinuidade_geometrica_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_descontinuidade_geometrica_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_descontinuidade_geometrica_l
    FOR EACH ROW EXECUTE PROCEDURE asb_descontinuidade_geometrica_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION rel_rocha_p_avoid_multi () RETURNS TRIGGER AS $rel_rocha_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.rel_rocha_p(nomeabrev,tipoelemnat,geom,tiporocha,nome,geometriaaproximada) SELECT NEW.nomeabrev,NEW.tipoelemnat,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tiporocha,NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$rel_rocha_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER rel_rocha_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.rel_rocha_p
    FOR EACH ROW EXECUTE PROCEDURE rel_rocha_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_local_critico_p_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_p(nomeabrev,geometriaaproximada,geom,tipolocalcrit,nome) SELECT NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipolocalcrit,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_p
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_area_habitacional_a_avoid_multi () RETURNS TRIGGER AS $loc_area_habitacional_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_area_habitacional_a(geom,nomeabrev,geometriaaproximada,id_complexo_habitacional,nome) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_complexo_habitacional,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_area_habitacional_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_area_habitacional_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_area_habitacional_a
    FOR EACH ROW EXECUTE PROCEDURE loc_area_habitacional_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION loc_localidade_p_avoid_multi () RETURNS TRIGGER AS $loc_localidade_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.loc_localidade_p(latitude_gms,identificador,geocodigo,nomeabrev,geometriaaproximada,latitude,geom,longitude_gms,longitude,nome) SELECT NEW.latitude_gms,NEW.identificador,NEW.geocodigo,NEW.nomeabrev,NEW.geometriaaproximada,NEW.latitude,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.longitude_gms,NEW.longitude,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$loc_localidade_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER loc_localidade_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.loc_localidade_p
    FOR EACH ROW EXECUTE PROCEDURE loc_localidade_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_local_critico_a_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_a(nome,nomeabrev,geom,geometriaaproximada,tipolocalcrit) SELECT NEW.nome,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.tipolocalcrit ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_a
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_macega_chavascal_a_avoid_multi () RETURNS TRIGGER AS $veg_macega_chavascal_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_macega_chavascal_a(alturamediaindividuos,tipomacchav,geom,antropizada,denso,geometriaaproximada,nomeabrev,nome,classificacaoporte) SELECT NEW.alturamediaindividuos,NEW.tipomacchav,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_macega_chavascal_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_macega_chavascal_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_macega_chavascal_a
    FOR EACH ROW EXECUTE PROCEDURE veg_macega_chavascal_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_local_critico_l_avoid_multi () RETURNS TRIGGER AS $tra_local_critico_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_local_critico_l(geom,nome,nomeabrev,geometriaaproximada,tipolocalcrit) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipolocalcrit ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_local_critico_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_local_critico_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_local_critico_l
    FOR EACH ROW EXECUTE PROCEDURE tra_local_critico_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_religiosa_a_avoid_multi () RETURNS TRIGGER AS $edu_edif_religiosa_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_religiosa_a(religiao,id_org_religiosa,geom,tipoedifrelig,matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome,ensino) SELECT NEW.religiao,NEW.id_org_religiosa,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifrelig,NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.ensino ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_religiosa_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_religiosa_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_religiosa_a
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_religiosa_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_terreno_suj_inundacao_a_avoid_multi () RETURNS TRIGGER AS $hid_terreno_suj_inundacao_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_terreno_suj_inundacao_a(periodicidadeinunda,nomeabrev,geom,geometriaaproximada,nome) SELECT NEW.periodicidadeinunda,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_terreno_suj_inundacao_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_terreno_suj_inundacao_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_terreno_suj_inundacao_a
    FOR EACH ROW EXECUTE PROCEDURE hid_terreno_suj_inundacao_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_edif_religiosa_p_avoid_multi () RETURNS TRIGGER AS $edu_edif_religiosa_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_edif_religiosa_p(tipoedifrelig,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,matconstr,geom,ensino,religiao,id_org_religiosa) SELECT NEW.tipoedifrelig,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.ensino,NEW.religiao,NEW.id_org_religiosa ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_edif_religiosa_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_edif_religiosa_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_edif_religiosa_p
    FOR EACH ROW EXECUTE PROCEDURE edu_edif_religiosa_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_edif_pub_civil_p_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_civil_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_civil_p(nome,nomeabrev,geometriaaproximada,id_org_pub_civil,operacional,situacaofisica,matconstr,geom,tipoedifcivil,tipousoedif) SELECT NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.id_org_pub_civil,NEW.operacional,NEW.situacaofisica,NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifcivil,NEW.tipousoedif ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_civil_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_civil_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_civil_p
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_civil_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_trecho_energia_l_avoid_multi () RETURNS TRIGGER AS $enc_trecho_energia_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_trecho_energia_l(tensaoeletrica,numcircuitos,emduto,situacaofisica,operacional,posicaorelativa,especie,geometriaaproximada,nomeabrev,nome,geom,id_org_comerc_serv) SELECT NEW.tensaoeletrica,NEW.numcircuitos,NEW.emduto,NEW.situacaofisica,NEW.operacional,NEW.posicaorelativa,NEW.especie,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_comerc_serv ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_trecho_energia_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_trecho_energia_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_trecho_energia_l
    FOR EACH ROW EXECUTE PROCEDURE enc_trecho_energia_l_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_metro_ferroviaria_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_tunel_l_avoid_multi () RETURNS TRIGGER AS $tra_tunel_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_tunel_l(situacaofisica,matconstr,modaluso,tipotunel,geometriaaproximada,nomeabrev,nome,geom,extensao,altura,posicaopista,nrfaixas,nrpistas,operacional) SELECT NEW.situacaofisica,NEW.matconstr,NEW.modaluso,NEW.tipotunel,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.extensao,NEW.altura,NEW.posicaopista,NEW.nrfaixas,NEW.nrpistas,NEW.operacional ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_tunel_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_tunel_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_tunel_l
    FOR EACH ROW EXECUTE PROCEDURE tra_tunel_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION adm_edif_pub_civil_a_avoid_multi () RETURNS TRIGGER AS $adm_edif_pub_civil_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.adm_edif_pub_civil_a(geom,situacaofisica,operacional,geometriaaproximada,nomeabrev,nome,tipousoedif,tipoedifcivil,id_org_pub_civil,matconstr) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.tipousoedif,NEW.tipoedifcivil,NEW.id_org_pub_civil,NEW.matconstr ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$adm_edif_pub_civil_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER adm_edif_pub_civil_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.adm_edif_pub_civil_a
    FOR EACH ROW EXECUTE PROCEDURE adm_edif_pub_civil_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_limite_particular_l_avoid_multi () RETURNS TRIGGER AS $lim_limite_particular_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_limite_particular_l(obssituacao,nome,nomeabrev,coincidecomdentrode,geometriaaproximada,extensao,geom) SELECT NEW.obssituacao,NEW.nome,NEW.nomeabrev,NEW.coincidecomdentrode,NEW.geometriaaproximada,NEW.extensao,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_limite_particular_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_limite_particular_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_limite_particular_l
    FOR EACH ROW EXECUTE PROCEDURE lim_limite_particular_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_edif_metro_ferroviaria_a_avoid_multi () RETURNS TRIGGER AS $tra_edif_metro_ferroviaria_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_edif_metro_ferroviaria_a(nomeabrev,nome,id_estrut_apoio,administracao,multimodal,funcaoedifmetroferrov,geom,matconstr,situacaofisica,operacional,geometriaaproximada) SELECT NEW.nomeabrev,NEW.nome,NEW.id_estrut_apoio,NEW.administracao,NEW.multimodal,NEW.funcaoedifmetroferrov,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_edif_metro_ferroviaria_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_edif_metro_ferroviaria_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_edif_metro_ferroviaria_a
    FOR EACH ROW EXECUTE PROCEDURE tra_edif_metro_ferroviaria_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_quebramar_molhe_a_avoid_multi () RETURNS TRIGGER AS $hid_quebramar_molhe_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_quebramar_molhe_a(tipoquebramolhe,geom,situacaofisica,operacional,situamare,matconstr,geometriaaproximada,nomeabrev,nome) SELECT NEW.tipoquebramolhe,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.operacional,NEW.situamare,NEW.matconstr,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_quebramar_molhe_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_quebramar_molhe_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_quebramar_molhe_a
    FOR EACH ROW EXECUTE PROCEDURE hid_quebramar_molhe_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_quebramar_molhe_l_avoid_multi () RETURNS TRIGGER AS $hid_quebramar_molhe_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_quebramar_molhe_l(nomeabrev,nome,geom,situacaofisica,operacional,situamare,matconstr,tipoquebramolhe,geometriaaproximada) SELECT NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.operacional,NEW.situamare,NEW.matconstr,NEW.tipoquebramolhe,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_quebramar_molhe_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_quebramar_molhe_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_quebramar_molhe_l
    FOR EACH ROW EXECUTE PROCEDURE hid_quebramar_molhe_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_arquibancada_a_avoid_multi () RETURNS TRIGGER AS $edu_arquibancada_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_arquibancada_a(geometriaaproximada,operacional,nomeabrev,nome,geom,situacaofisica,id_complexo_lazer) SELECT NEW.geometriaaproximada,NEW.operacional,NEW.nomeabrev,NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.situacaofisica,NEW.id_complexo_lazer ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_arquibancada_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_arquibancada_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_arquibancada_a
    FOR EACH ROW EXECUTE PROCEDURE edu_arquibancada_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION veg_mangue_a_avoid_multi () RETURNS TRIGGER AS $veg_mangue_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.veg_mangue_a(geom,antropizada,denso,geometriaaproximada,nomeabrev,nome,classificacaoporte) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.antropizada,NEW.denso,NEW.geometriaaproximada,NEW.nomeabrev,NEW.nome,NEW.classificacaoporte ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$veg_mangue_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER veg_mangue_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.veg_mangue_a
    FOR EACH ROW EXECUTE PROCEDURE veg_mangue_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_queda_dagua_p_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_p(geom,nome,nomeabrev,geometriaaproximada,tipoqueda,altura) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoqueda,NEW.altura ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_p
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION asb_edif_abast_agua_p_avoid_multi () RETURNS TRIGGER AS $asb_edif_abast_agua_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.asb_edif_abast_agua_p(matconstr,situacaofisica,operacional,geometriaaproximada,nomeabrev,geom,tipoedifabast,id_complexo_abast_agua,nome) SELECT NEW.matconstr,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.tipoedifabast,NEW.id_complexo_abast_agua,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$asb_edif_abast_agua_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER asb_edif_abast_agua_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.asb_edif_abast_agua_p
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_abast_agua_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_queda_dagua_a_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_a(tipoqueda,geometriaaproximada,altura,geom,nome,nomeabrev) SELECT NEW.tipoqueda,NEW.geometriaaproximada,NEW.altura,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_a
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_a_avoid_multi ()#
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
    FOR EACH ROW EXECUTE PROCEDURE asb_edif_abast_agua_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION hid_queda_dagua_l_avoid_multi () RETURNS TRIGGER AS $hid_queda_dagua_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.hid_queda_dagua_l(nomeabrev,nome,geometriaaproximada,tipoqueda,altura,geom) SELECT NEW.nomeabrev,NEW.nome,NEW.geometriaaproximada,NEW.tipoqueda,NEW.altura,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$hid_queda_dagua_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER hid_queda_dagua_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.hid_queda_dagua_l
    FOR EACH ROW EXECUTE PROCEDURE hid_queda_dagua_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_p_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_p(nomeabrev,geom,id_complexo_gerad_energ_eletr,potenciafiscalizada,potenciaoutorgada,codigoestacao,destenergelet,situacaofisica,operacional,tipoestgerad,geometriaaproximada,nome) SELECT NEW.nomeabrev,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.potenciaoutorgada,NEW.codigoestacao,NEW.destenergelet,NEW.situacaofisica,NEW.operacional,NEW.tipoestgerad,NEW.geometriaaproximada,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_p
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_equip_agropec_a_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_a(geom,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoequipagropec,matconstr,id_org_agropec_ext_veg_pesca) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoequipagropec,NEW.matconstr,NEW.id_org_agropec_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_a
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION lim_municipio_a_avoid_multi () RETURNS TRIGGER AS $lim_municipio_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.lim_municipio_a(anodereferencia,nome,nomeabrev,geometriaaproximada,geom,geocodigo) SELECT NEW.anodereferencia,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.geocodigo ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$lim_municipio_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER lim_municipio_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.lim_municipio_a
    FOR EACH ROW EXECUTE PROCEDURE lim_municipio_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_cremalheira_p_avoid_multi () RETURNS TRIGGER AS $tra_cremalheira_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_cremalheira_p(situacaofisica,nome,nomeabrev,geometriaaproximada,operacional,geom) SELECT NEW.situacaofisica,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_cremalheira_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_cremalheira_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_cremalheira_p
    FOR EACH ROW EXECUTE PROCEDURE tra_cremalheira_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_equip_agropec_l_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_l(nome,geom,id_org_agropec_ext_veg_pesca,matconstr,tipoequipagropec,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT NEW.nome,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.id_org_agropec_ext_veg_pesca,NEW.matconstr,NEW.tipoequipagropec,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_l
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION tra_cremalheira_l_avoid_multi () RETURNS TRIGGER AS $tra_cremalheira_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.tra_cremalheira_l(geom,nome,situacaofisica,operacional,geometriaaproximada,nomeabrev) SELECT ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.situacaofisica,NEW.operacional,NEW.geometriaaproximada,NEW.nomeabrev ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$tra_cremalheira_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER tra_cremalheira_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.tra_cremalheira_l
    FOR EACH ROW EXECUTE PROCEDURE tra_cremalheira_l_avoid_multi ()#
CREATE OR REPLACE FUNCTION eco_equip_agropec_p_avoid_multi () RETURNS TRIGGER AS $eco_equip_agropec_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.eco_equip_agropec_p(matconstr,geom,nome,nomeabrev,geometriaaproximada,operacional,situacaofisica,tipoequipagropec,id_org_agropec_ext_veg_pesca) SELECT NEW.matconstr,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.operacional,NEW.situacaofisica,NEW.tipoequipagropec,NEW.id_org_agropec_ext_veg_pesca ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$eco_equip_agropec_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER eco_equip_agropec_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.eco_equip_agropec_p
    FOR EACH ROW EXECUTE PROCEDURE eco_equip_agropec_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_a_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_a_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_a(potenciafiscalizada,nome,nomeabrev,geometriaaproximada,tipoestgerad,operacional,situacaofisica,destenergelet,codigoestacao,potenciaoutorgada,id_complexo_gerad_energ_eletr,geom) SELECT NEW.potenciafiscalizada,NEW.nome,NEW.nomeabrev,NEW.geometriaaproximada,NEW.tipoestgerad,NEW.operacional,NEW.situacaofisica,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.id_complexo_gerad_energ_eletr,ST_Multi((ST_Dump(NEW.geom)).geom) ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_a_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_a_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_a
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_a_avoid_multi ()#
CREATE OR REPLACE FUNCTION edu_arquibancada_p_avoid_multi () RETURNS TRIGGER AS $edu_arquibancada_p_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.edu_arquibancada_p(nomeabrev,operacional,situacaofisica,id_complexo_lazer,geom,nome,geometriaaproximada) SELECT NEW.nomeabrev,NEW.operacional,NEW.situacaofisica,NEW.id_complexo_lazer,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.nome,NEW.geometriaaproximada ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$edu_arquibancada_p_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER edu_arquibancada_p_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.edu_arquibancada_p
    FOR EACH ROW EXECUTE PROCEDURE edu_arquibancada_p_avoid_multi ()#
CREATE OR REPLACE FUNCTION enc_est_gerad_energia_eletr_l_avoid_multi () RETURNS TRIGGER AS $enc_est_gerad_energia_eletr_l_avoid_multi_return$
    DECLARE
    BEGIN
        IF pg_trigger_depth() <> 1 AND ST_NumGeometries(NEW.geom) =1 THEN
		RETURN NEW;
	END IF;
	IF ST_NumGeometries(NEW.geom) > 1 THEN
		INSERT INTO cb.enc_est_gerad_energia_eletr_l(tipoestgerad,geom,operacional,situacaofisica,geometriaaproximada,destenergelet,codigoestacao,potenciaoutorgada,id_complexo_gerad_energ_eletr,potenciafiscalizada,nomeabrev,nome) SELECT NEW.tipoestgerad,ST_Multi((ST_Dump(NEW.geom)).geom),NEW.operacional,NEW.situacaofisica,NEW.geometriaaproximada,NEW.destenergelet,NEW.codigoestacao,NEW.potenciaoutorgada,NEW.id_complexo_gerad_energ_eletr,NEW.potenciafiscalizada,NEW.nomeabrev,NEW.nome ;
		RETURN NULL;
	ELSE
		RETURN NEW;
	END IF;
	RETURN NULL;
    END;
$enc_est_gerad_energia_eletr_l_avoid_multi_return$ LANGUAGE plpgsql#
CREATE TRIGGER enc_est_gerad_energia_eletr_l_avoid_multi_return
BEFORE INSERT OR UPDATE ON cb.enc_est_gerad_energia_eletr_l
    FOR EACH ROW EXECUTE PROCEDURE enc_est_gerad_energia_eletr_l_avoid_multi ()#