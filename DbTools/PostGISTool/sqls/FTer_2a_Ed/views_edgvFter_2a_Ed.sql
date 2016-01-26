DROP SCHEMA IF EXISTS views CASCADE#
CREATE SCHEMA views#
DROP VIEW IF EXISTS views.edf_edif_constr_lazer_a#CREATE [VIEW] views.edf_edif_constr_lazer_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_lazer_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_lazer_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_lazer_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_lazer_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_lazer_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_lazer_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_lazer_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_lazer_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoediflazer.code_name as tipoediflazer,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.edf_edif_constr_lazer_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_lazer_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_lazer_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_lazer_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_lazer_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_lazer_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_lazer_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_lazer_a.proprioadm 
	left join dominios.tipo_edif_lazer as dominio_tipoediflazer on dominio_tipoediflazer.code = edf_edif_constr_lazer_a.tipoediflazer
#
DROP VIEW IF EXISTS views.edf_edif_industrial_p#CREATE [VIEW] views.edf_edif_industrial_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_industrial_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_industrial_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_industrial_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_industrial_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_industrial_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_industrial_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_industrial_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_industrial_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_chamine.code_name as chamine,
	id_org_industrial as id_org_industrial
    [FROM]
        ge.edf_edif_industrial_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_industrial_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_industrial_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_industrial_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_industrial_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_industrial_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_industrial_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_industrial_p.proprioadm 
	left join dominios.booleano as dominio_chamine on dominio_chamine.code = edf_edif_industrial_p.chamine
#
DROP VIEW IF EXISTS views.edf_edif_servico_social_p#CREATE [VIEW] views.edf_edif_servico_social_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_servico_social_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_servico_social_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_servico_social_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_servico_social_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_servico_social_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_servico_social_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_servico_social_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_servico_social_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_servico_social as id_org_servico_social
    [FROM]
        ge.edf_edif_servico_social_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_servico_social_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_servico_social_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_servico_social_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_servico_social_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_servico_social_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_servico_social_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_servico_social_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_desenv_social_a#CREATE [VIEW] views.cb_area_desenv_social_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_area_desenv_social_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_desenv_social_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_industrial_a#CREATE [VIEW] views.edf_edif_industrial_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_industrial_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_industrial_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_industrial_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_industrial_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_industrial_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_industrial_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_industrial_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_industrial_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_chamine.code_name as chamine,
	id_org_industrial as id_org_industrial
    [FROM]
        ge.edf_edif_industrial_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_industrial_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_industrial_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_industrial_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_industrial_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_industrial_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_industrial_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_industrial_a.proprioadm 
	left join dominios.booleano as dominio_chamine on dominio_chamine.code = edf_edif_industrial_a.chamine
#
DROP VIEW IF EXISTS views.edf_edif_servico_social_a#CREATE [VIEW] views.edf_edif_servico_social_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_servico_social_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_servico_social_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_servico_social_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_servico_social_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_servico_social_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_servico_social_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_servico_social_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_servico_social_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_servico_social as id_org_servico_social
    [FROM]
        ge.edf_edif_servico_social_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_servico_social_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_servico_social_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_servico_social_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_servico_social_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_servico_social_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_servico_social_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_servico_social_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_posto_policia_militar_p#CREATE [VIEW] views.edf_posto_policia_militar_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_policia_militar_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_policia_militar_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_policia_militar_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_policia_militar_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_policia_militar_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_policia_militar_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_policia_militar_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_policia_militar_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipoinstalmilitar.code_name as tipoinstalmilitar,
	organizacao as organizacao
    [FROM]
        ge.edf_posto_policia_militar_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_policia_militar_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_policia_militar_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_policia_militar_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_policia_militar_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_policia_militar_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_policia_militar_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_policia_militar_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_policia_militar_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_policia_militar_p.jurisdicao 
	left join dominios.tipo_instal_militar as dominio_tipoinstalmilitar on dominio_tipoinstalmilitar.code = edf_posto_policia_militar_p.tipoinstalmilitar
#
DROP VIEW IF EXISTS views.cb_area_de_propriedade_particular_a#CREATE [VIEW] views.cb_area_de_propriedade_particular_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_area_de_propriedade_particular_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_de_propriedade_particular_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_ext_mineral_a#CREATE [VIEW] views.edf_edif_ext_mineral_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_ext_mineral_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_ext_mineral_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_ext_mineral_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_ext_mineral_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_ext_mineral_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_ext_mineral_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_ext_mineral_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_ext_mineral_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        ge.edf_edif_ext_mineral_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_ext_mineral_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_ext_mineral_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_ext_mineral_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_ext_mineral_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_ext_mineral_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_ext_mineral_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_ext_mineral_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_constr_turistica_p#CREATE [VIEW] views.edf_edif_constr_turistica_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_turistica_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_turistica_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_turistica_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_turistica_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_turistica_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_turistica_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_turistica_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_turistica_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifturist.code_name as tipoedifturist,
	dominio_ovgd.code_name as ovgd,
	dominio_tombada.code_name as tombada,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.edf_edif_constr_turistica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_turistica_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_turistica_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_turistica_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_turistica_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_turistica_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_turistica_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_turistica_p.proprioadm 
	left join dominios.tipo_edif_turist as dominio_tipoedifturist on dominio_tipoedifturist.code = edf_edif_constr_turistica_p.tipoedifturist 
	left join dominios.booleano_estendido as dominio_ovgd on dominio_ovgd.code = edf_edif_constr_turistica_p.ovgd 
	left join dominios.booleano as dominio_tombada on dominio_tombada.code = edf_edif_constr_turistica_p.tombada
#
DROP VIEW IF EXISTS views.cb_area_ext_mineral_a#CREATE [VIEW] views.cb_area_ext_mineral_a as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        ge.cb_area_ext_mineral_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_ext_mineral_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_ext_mineral_p#CREATE [VIEW] views.edf_edif_ext_mineral_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_ext_mineral_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_ext_mineral_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_ext_mineral_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_ext_mineral_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_ext_mineral_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_ext_mineral_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_ext_mineral_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_ext_mineral_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        ge.edf_edif_ext_mineral_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_ext_mineral_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_ext_mineral_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_ext_mineral_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_ext_mineral_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_ext_mineral_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_ext_mineral_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_ext_mineral_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_ensino_a#CREATE [VIEW] views.cb_area_ensino_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_ensino as id_org_ensino
    [FROM]
        ge.cb_area_ensino_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_ensino_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_area_servico_social_a#CREATE [VIEW] views.cb_area_servico_social_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_servico_social as id_org_servico_social
    [FROM]
        ge.cb_area_servico_social_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_servico_social_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_saude_p#CREATE [VIEW] views.edf_edif_saude_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_saude_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_saude_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_saude_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_saude_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_saude_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_saude_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_saude_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_saude_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_nivelatencao.code_name as nivelatencao,
	id_org_saude as id_org_saude
    [FROM]
        ge.edf_edif_saude_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_saude_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_saude_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_saude_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_saude_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_saude_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_saude_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_saude_p.proprioadm 
	left join dominios.nivel_atencao as dominio_nivelatencao on dominio_nivelatencao.code = edf_edif_saude_p.nivelatencao
#
DROP VIEW IF EXISTS views.cb_area_est_med_fenomenos_a#CREATE [VIEW] views.cb_area_est_med_fenomenos_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_est_med_fenomenos as id_est_med_fenomenos,
	geom as geom
    [FROM]
        ge.cb_area_est_med_fenomenos_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_est_med_fenomenos_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_descontinuidade_geometrica_a#CREATE [VIEW] views.cb_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.cb_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = cb_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.ver_descontinuidade_geometrica_l#CREATE [VIEW] views.ver_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.ver_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ver_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = ver_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.cb_descontinuidade_geometrica_l#CREATE [VIEW] views.cb_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.cb_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = cb_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_posto_combustivel_p#CREATE [VIEW] views.edf_posto_combustivel_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_comerc_serv dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.tipoedifcomercserv and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as tipoedifcomercserv,
	array_to_string( array(select code_name from dominios.finalidade dom join ge.edf_posto_combustivel_p tn on (array[dom.code] <@ tn.finalidade and tn.id=ge.edf_posto_combustivel_p.id)),',' ) as finalidade,
	id_estrut_transporte as id_estrut_transporte,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        ge.edf_posto_combustivel_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_combustivel_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_combustivel_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_combustivel_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_combustivel_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_combustivel_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_combustivel_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_combustivel_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_energia_eletrica_a#CREATE [VIEW] views.cb_area_energia_eletrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_subest_transm_distrib_energia_eletrica as id_subest_transm_distrib_energia_eletrica,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica
    [FROM]
        ge.cb_area_energia_eletrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_energia_eletrica_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_posto_policia_rod_federal_a#CREATE [VIEW] views.edf_posto_policia_rod_federal_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_policia_rod_federal_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_policia_rod_federal_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_policia_rod_federal_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_policia_rod_federal_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_policia_rod_federal_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_policia_rod_federal_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_policia_rod_federal_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_policia_rod_federal_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_policia_rod_federal_a tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_policia_rod_federal_a.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_posto_policia_rod_federal_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_policia_rod_federal_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_policia_rod_federal_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_policia_rod_federal_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_policia_rod_federal_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_policia_rod_federal_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_policia_rod_federal_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_policia_rod_federal_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_policia_rod_federal_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_policia_rod_federal_a.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_saude_a#CREATE [VIEW] views.edf_edif_saude_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_saude_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_saude_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_saude_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_saude_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_saude_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_saude_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_saude_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_saude_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_nivelatencao.code_name as nivelatencao,
	id_org_saude as id_org_saude
    [FROM]
        ge.edf_edif_saude_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_saude_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_saude_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_saude_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_saude_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_saude_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_saude_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_saude_a.proprioadm 
	left join dominios.nivel_atencao as dominio_nivelatencao on dominio_nivelatencao.code = edf_edif_saude_a.nivelatencao
#
DROP VIEW IF EXISTS views.cb_descontinuidade_geometrica_p#CREATE [VIEW] views.cb_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.cb_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = cb_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_posto_combustivel_a#CREATE [VIEW] views.edf_posto_combustivel_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_comerc_serv dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.tipoedifcomercserv and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as tipoedifcomercserv,
	array_to_string( array(select code_name from dominios.finalidade dom join ge.edf_posto_combustivel_a tn on (array[dom.code] <@ tn.finalidade and tn.id=ge.edf_posto_combustivel_a.id)),',' ) as finalidade,
	id_estrut_transporte as id_estrut_transporte,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        ge.edf_posto_combustivel_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_combustivel_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_combustivel_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_combustivel_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_combustivel_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_combustivel_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_combustivel_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_combustivel_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_agropec_ext_veg_pesca_p#CREATE [VIEW] views.edf_edif_agropec_ext_veg_pesca_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_agropec_ext_veg_pesca_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_agropec_ext_veg_pesca_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_agropec dom join ge.edf_edif_agropec_ext_veg_pesca_p tn on (array[dom.code] <@ tn.tipoedifagropec and tn.id=ge.edf_edif_agropec_ext_veg_pesca_p.id)),',' ) as tipoedifagropec,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        ge.edf_edif_agropec_ext_veg_pesca_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_agropec_ext_veg_pesca_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_agropec_ext_veg_pesca_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_agropec_ext_veg_pesca_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_agropec_ext_veg_pesca_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_agropec_ext_veg_pesca_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_agropec_ext_veg_pesca_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_agropec_ext_veg_pesca_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_meio_fio_l#CREATE [VIEW] views.cb_meio_fio_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_comsargeta.code_name as comsargeta,
	geom as geom
    [FROM]
        ge.cb_meio_fio_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_meio_fio_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_comsargeta on dominio_comsargeta.code = cb_meio_fio_l.comsargeta
#
DROP VIEW IF EXISTS views.laz_arquibancada_l#CREATE [VIEW] views.laz_arquibancada_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_arquibancada_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_arquibancada_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_arquibancada_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_arquibancada_l.situacaofisica
#
DROP VIEW IF EXISTS views.edf_posto_guarda_municipal_p#CREATE [VIEW] views.edf_posto_guarda_municipal_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_guarda_municipal_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_guarda_municipal_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_guarda_municipal_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_guarda_municipal_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_guarda_municipal_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_guarda_municipal_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_guarda_municipal_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_guarda_municipal_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_guarda_municipal_p tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_guarda_municipal_p.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_posto_guarda_municipal_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_guarda_municipal_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_guarda_municipal_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_guarda_municipal_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_guarda_municipal_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_guarda_municipal_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_guarda_municipal_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_guarda_municipal_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_guarda_municipal_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_guarda_municipal_p.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_constr_lazer_p#CREATE [VIEW] views.edf_edif_constr_lazer_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_lazer_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_lazer_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_lazer_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_lazer_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_lazer_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_lazer_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_lazer_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_lazer_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoediflazer.code_name as tipoediflazer,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.edf_edif_constr_lazer_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_lazer_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_lazer_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_lazer_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_lazer_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_lazer_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_lazer_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_lazer_p.proprioadm 
	left join dominios.tipo_edif_lazer as dominio_tipoediflazer on dominio_tipoediflazer.code = edf_edif_constr_lazer_p.tipoediflazer
#
DROP VIEW IF EXISTS views.laz_arquibancada_a#CREATE [VIEW] views.laz_arquibancada_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_arquibancada_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_arquibancada_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_arquibancada_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_arquibancada_a.situacaofisica
#
DROP VIEW IF EXISTS views.laz_pista_competicao_p#CREATE [VIEW] views.laz_pista_competicao_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopistacomp.code_name as tipopistacomp,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_pista_competicao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_pista_competicao_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_pista_competicao_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_pista_competicao_p.situacaofisica 
	left join dominios.tipo_pista_comp as dominio_tipopistacomp on dominio_tipopistacomp.code = laz_pista_competicao_p.tipopistacomp
#
DROP VIEW IF EXISTS views.edf_edif_constr_portuaria_p#CREATE [VIEW] views.edf_edif_constr_portuaria_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_portuaria_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_portuaria_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_portuaria_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_portuaria_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_portuaria_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_portuaria_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_portuaria_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_portuaria_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifport.code_name as tipoedifport,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_complexo_portuario as id_complexo_portuario,
	id_org_industrial as id_org_industrial
    [FROM]
        ge.edf_edif_constr_portuaria_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_portuaria_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_portuaria_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_portuaria_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_portuaria_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_portuaria_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_portuaria_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_portuaria_p.proprioadm 
	left join dominios.tipo_edif_port as dominio_tipoedifport on dominio_tipoedifport.code = edf_edif_constr_portuaria_p.tipoedifport 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_constr_portuaria_p.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_agropec_ext_veg_pesca_a#CREATE [VIEW] views.edf_edif_agropec_ext_veg_pesca_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_agropec_ext_veg_pesca_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_agropec_ext_veg_pesca_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_agropec_ext_veg_pesca_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_agropec_ext_veg_pesca_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_agropec dom join ge.edf_edif_agropec_ext_veg_pesca_a tn on (array[dom.code] <@ tn.tipoedifagropec and tn.id=ge.edf_edif_agropec_ext_veg_pesca_a.id)),',' ) as tipoedifagropec,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        ge.edf_edif_agropec_ext_veg_pesca_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_agropec_ext_veg_pesca_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_agropec_ext_veg_pesca_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_agropec_ext_veg_pesca_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_agropec_ext_veg_pesca_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_agropec_ext_veg_pesca_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_agropec_ext_veg_pesca_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_agropec_ext_veg_pesca_a.proprioadm
#
DROP VIEW IF EXISTS views.laz_pista_competicao_l#CREATE [VIEW] views.laz_pista_competicao_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopistacomp.code_name as tipopistacomp,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_pista_competicao_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_pista_competicao_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_pista_competicao_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_pista_competicao_l.situacaofisica 
	left join dominios.tipo_pista_comp as dominio_tipopistacomp on dominio_tipopistacomp.code = laz_pista_competicao_l.tipopistacomp
#
DROP VIEW IF EXISTS views.cb_trecho_arruamento_a#CREATE [VIEW] views.cb_trecho_arruamento_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_trafego.code_name as trafego,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	dominio_tipoarruamento.code_name as tipoarruamento,
	array_to_string( array(select code_name from dominios.tipo_pavimentacao dom join ge.cb_trecho_arruamento_a tn on (array[dom.code] <@ tn.tipopavimentacao and tn.id=ge.cb_trecho_arruamento_a.id)),',' ) as tipopavimentacao,
	dominio_meiofio.code_name as meiofio,
	dominio_sargeta.code_name as sargeta,
	id_arruamento as id_arruamento,
	geom as geom
    [FROM]
        ge.cb_trecho_arruamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_trecho_arruamento_a.geometriaaproximada 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = cb_trecho_arruamento_a.revestimento 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_trecho_arruamento_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_trecho_arruamento_a.situacaofisica 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = cb_trecho_arruamento_a.trafego 
	left join dominios.booleano_estendido as dominio_canteirodivisorio on dominio_canteirodivisorio.code = cb_trecho_arruamento_a.canteirodivisorio 
	left join dominios.tipo_arruamento as dominio_tipoarruamento on dominio_tipoarruamento.code = cb_trecho_arruamento_a.tipoarruamento 
	left join dominios.booleano as dominio_meiofio on dominio_meiofio.code = cb_trecho_arruamento_a.meiofio 
	left join dominios.booleano as dominio_sargeta on dominio_sargeta.code = cb_trecho_arruamento_a.sargeta
#
DROP VIEW IF EXISTS views.edf_posto_guarda_municipal_a#CREATE [VIEW] views.edf_posto_guarda_municipal_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_guarda_municipal_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_guarda_municipal_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_guarda_municipal_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_guarda_municipal_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_guarda_municipal_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_guarda_municipal_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_guarda_municipal_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_guarda_municipal_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_guarda_municipal_a tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_guarda_municipal_a.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_posto_guarda_municipal_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_guarda_municipal_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_guarda_municipal_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_guarda_municipal_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_guarda_municipal_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_guarda_municipal_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_guarda_municipal_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_guarda_municipal_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_guarda_municipal_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_guarda_municipal_a.jurisdicao
#
DROP VIEW IF EXISTS views.laz_pista_competicao_a#CREATE [VIEW] views.laz_pista_competicao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipopistacomp.code_name as tipopistacomp,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_pista_competicao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_pista_competicao_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_pista_competicao_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_pista_competicao_a.situacaofisica 
	left join dominios.tipo_pista_comp as dominio_tipopistacomp on dominio_tipopistacomp.code = laz_pista_competicao_a.tipopistacomp
#
DROP VIEW IF EXISTS views.laz_arquibancada_p#CREATE [VIEW] views.laz_arquibancada_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_arquibancada_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_arquibancada_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_arquibancada_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_arquibancada_p.situacaofisica
#
DROP VIEW IF EXISTS views.cb_trecho_arruamento_l#CREATE [VIEW] views.cb_trecho_arruamento_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_trafego.code_name as trafego,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	dominio_tipoarruamento.code_name as tipoarruamento,
	array_to_string( array(select code_name from dominios.tipo_pavimentacao dom join ge.cb_trecho_arruamento_l tn on (array[dom.code] <@ tn.tipopavimentacao and tn.id=ge.cb_trecho_arruamento_l.id)),',' ) as tipopavimentacao,
	dominio_meiofio.code_name as meiofio,
	dominio_sargeta.code_name as sargeta,
	id_arruamento as id_arruamento,
	geom as geom
    [FROM]
        ge.cb_trecho_arruamento_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_trecho_arruamento_l.geometriaaproximada 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = cb_trecho_arruamento_l.revestimento 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_trecho_arruamento_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_trecho_arruamento_l.situacaofisica 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = cb_trecho_arruamento_l.trafego 
	left join dominios.booleano_estendido as dominio_canteirodivisorio on dominio_canteirodivisorio.code = cb_trecho_arruamento_l.canteirodivisorio 
	left join dominios.tipo_arruamento as dominio_tipoarruamento on dominio_tipoarruamento.code = cb_trecho_arruamento_l.tipoarruamento 
	left join dominios.booleano as dominio_meiofio on dominio_meiofio.code = cb_trecho_arruamento_l.meiofio 
	left join dominios.booleano as dominio_sargeta on dominio_sargeta.code = cb_trecho_arruamento_l.sargeta
#
DROP VIEW IF EXISTS views.ppb_faixa_dominio_arruamento_a#CREATE [VIEW] views.ppb_faixa_dominio_arruamento_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	largurapartireixo as largurapartireixo
    [FROM]
        ge.ppb_faixa_dominio_arruamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ppb_faixa_dominio_arruamento_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = ppb_faixa_dominio_arruamento_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = ppb_faixa_dominio_arruamento_a.jurisdicao
#
DROP VIEW IF EXISTS views.laz_ruina_p#CREATE [VIEW] views.laz_ruina_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_ruina_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_ruina_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = laz_ruina_p.turistica 
	left join dominios.booleano as dominio_cultura on dominio_cultura.code = laz_ruina_p.cultura
#
DROP VIEW IF EXISTS views.edf_posto_fiscal_a#CREATE [VIEW] views.edf_posto_fiscal_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_fiscal_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_fiscal_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_fiscal_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_fiscal_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_fiscal_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_fiscal_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_fiscal_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_fiscal_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_fiscal_a tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_fiscal_a.id)),',' ) as tipoedifpubcivil,
	dominio_tipopostofisc.code_name as tipopostofisc,
	concessionaria as concessionaria,
	id_estrut_transporte as id_estrut_transporte
    [FROM]
        ge.edf_posto_fiscal_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_fiscal_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_fiscal_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_fiscal_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_fiscal_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_fiscal_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_fiscal_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_fiscal_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_fiscal_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_fiscal_a.jurisdicao 
	left join dominios.tipo_posto_fisc as dominio_tipopostofisc on dominio_tipopostofisc.code = edf_posto_fiscal_a.tipopostofisc
#
DROP VIEW IF EXISTS views.edf_edificacao_a#CREATE [VIEW] views.edf_edificacao_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edificacao_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edificacao_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edificacao_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edificacao_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edificacao_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edificacao_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edificacao_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edificacao_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edificacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edificacao_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edificacao_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edificacao_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edificacao_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edificacao_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edificacao_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edificacao_a.proprioadm
#
DROP VIEW IF EXISTS views.laz_ruina_a#CREATE [VIEW] views.laz_ruina_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_ruina_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_ruina_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = laz_ruina_a.turistica 
	left join dominios.booleano as dominio_cultura on dominio_cultura.code = laz_ruina_a.cultura
#
DROP VIEW IF EXISTS views.edf_posto_fiscal_p#CREATE [VIEW] views.edf_posto_fiscal_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_fiscal_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_fiscal_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_fiscal_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_fiscal_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_fiscal_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_fiscal_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_fiscal_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_fiscal_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_fiscal_p tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_fiscal_p.id)),',' ) as tipoedifpubcivil,
	dominio_tipopostofisc.code_name as tipopostofisc,
	concessionaria as concessionaria,
	id_estrut_transporte as id_estrut_transporte
    [FROM]
        ge.edf_posto_fiscal_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_fiscal_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_fiscal_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_fiscal_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_fiscal_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_fiscal_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_fiscal_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_fiscal_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_fiscal_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_fiscal_p.jurisdicao 
	left join dominios.tipo_posto_fisc as dominio_tipopostofisc on dominio_tipopostofisc.code = edf_posto_fiscal_p.tipopostofisc
#
DROP VIEW IF EXISTS views.cb_praca_a#CREATE [VIEW] views.cb_praca_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_turistica.code_name as turistica,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.cb_praca_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_praca_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = cb_praca_a.turistica
#
DROP VIEW IF EXISTS views.edf_edificacao_p#CREATE [VIEW] views.edf_edificacao_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edificacao_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edificacao_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edificacao_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edificacao_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edificacao_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edificacao_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edificacao_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edificacao_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edificacao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edificacao_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edificacao_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edificacao_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edificacao_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edificacao_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edificacao_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edificacao_p.proprioadm
#
DROP VIEW IF EXISTS views.emu_descontinuidade_geometrica_a#CREATE [VIEW] views.emu_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.emu_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = emu_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_descontinuidade_geometrica_a#CREATE [VIEW] views.edf_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.edf_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edf_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_edif_residencial_p#CREATE [VIEW] views.edf_edif_residencial_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_residencial_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_residencial_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_residencial_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_residencial_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_residencial_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_residencial_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_residencial_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_residencial_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edif_residencial_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_residencial_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_residencial_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_residencial_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_residencial_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_residencial_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_residencial_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_residencial_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_urbana_isolada_a#CREATE [VIEW] views.cb_area_urbana_isolada_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoassociado.code_name as tipoassociado,
	geom as geom
    [FROM]
        ge.cb_area_urbana_isolada_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_urbana_isolada_a.geometriaaproximada 
	left join dominios.tipo_associado as dominio_tipoassociado on dominio_tipoassociado.code = cb_area_urbana_isolada_a.tipoassociado
#
DROP VIEW IF EXISTS views.edf_descontinuidade_geometrica_l#CREATE [VIEW] views.edf_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.edf_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edf_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.cb_retorno_p#CREATE [VIEW] views.cb_retorno_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_retorno_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_retorno_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_descontinuidade_geometrica_l#CREATE [VIEW] views.emu_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.emu_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = emu_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.cb_retorno_l#CREATE [VIEW] views.cb_retorno_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_retorno_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_retorno_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_descontinuidade_geometrica_p#CREATE [VIEW] views.emu_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.emu_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = emu_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_edif_residencial_a#CREATE [VIEW] views.edf_edif_residencial_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_residencial_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_residencial_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_residencial_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_residencial_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_residencial_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_residencial_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_residencial_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_residencial_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edif_residencial_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_residencial_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_residencial_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_residencial_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_residencial_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_residencial_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_residencial_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_residencial_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_descontinuidade_geometrica_p#CREATE [VIEW] views.edf_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.edf_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = edf_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_edif_religiosa_a#CREATE [VIEW] views.edf_edif_religiosa_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_religiosa_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_religiosa_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_religiosa_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_religiosa_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_religiosa_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_religiosa_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_religiosa_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_religiosa_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifrelig.code_name as tipoedifrelig,
	dominio_ensino.code_name as ensino,
	religiao as religiao,
	id_org_religiosa as id_org_religiosa,
	dominio_crista.code_name as crista
    [FROM]
        ge.edf_edif_religiosa_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_religiosa_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_religiosa_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_religiosa_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_religiosa_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_religiosa_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_religiosa_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_religiosa_a.proprioadm 
	left join dominios.tipo_edif_relig as dominio_tipoedifrelig on dominio_tipoedifrelig.code = edf_edif_religiosa_a.tipoedifrelig 
	left join dominios.booleano as dominio_ensino on dominio_ensino.code = edf_edif_religiosa_a.ensino 
	left join dominios.booleano as dominio_crista on dominio_crista.code = edf_edif_religiosa_a.crista
#
DROP VIEW IF EXISTS views.cb_retorno_a#CREATE [VIEW] views.cb_retorno_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_retorno_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_retorno_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_area_saude_a#CREATE [VIEW] views.cb_area_saude_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_saude as id_org_saude
    [FROM]
        ge.cb_area_saude_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_saude_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_banheiro_publico_p#CREATE [VIEW] views.edf_banheiro_publico_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_banheiro_publico_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_banheiro_publico_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_banheiro_publico_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_banheiro_publico_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_banheiro_publico_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_banheiro_publico_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_banheiro_publico_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_banheiro_publico_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_banheiro_publico_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_banheiro_publico_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_banheiro_publico_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_banheiro_publico_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_banheiro_publico_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_banheiro_publico_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_banheiro_publico_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_banheiro_publico_p.proprioadm
#
DROP VIEW IF EXISTS views.cb_largo_a#CREATE [VIEW] views.cb_largo_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.cb_largo_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_largo_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.laz_descontinuidade_geometrica_a#CREATE [VIEW] views.laz_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.laz_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = laz_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.cb_area_industrial_a#CREATE [VIEW] views.cb_area_industrial_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        ge.cb_area_industrial_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_industrial_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.laz_descontinuidade_geometrica_l#CREATE [VIEW] views.laz_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.laz_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = laz_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_edif_habitacional_p#CREATE [VIEW] views.edf_edif_habitacional_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_habitacional_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_habitacional_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_habitacional_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_habitacional_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_habitacional_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_habitacional_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_habitacional_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_habitacional_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edif_habitacional_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_habitacional_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_habitacional_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_habitacional_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_habitacional_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_habitacional_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_habitacional_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_habitacional_p.proprioadm
#
DROP VIEW IF EXISTS views.edf_banheiro_publico_a#CREATE [VIEW] views.edf_banheiro_publico_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_banheiro_publico_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_banheiro_publico_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_banheiro_publico_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_banheiro_publico_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_banheiro_publico_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_banheiro_publico_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_banheiro_publico_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_banheiro_publico_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_banheiro_publico_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_banheiro_publico_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_banheiro_publico_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_banheiro_publico_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_banheiro_publico_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_banheiro_publico_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_banheiro_publico_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_banheiro_publico_a.proprioadm
#
DROP VIEW IF EXISTS views.laz_descontinuidade_geometrica_p#CREATE [VIEW] views.laz_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.laz_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = laz_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.edf_edif_abast_agua_a#CREATE [VIEW] views.edf_edif_abast_agua_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_abast_agua_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_abast_agua_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_abast_agua_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_abast_agua_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_abast_agua_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_abast_agua_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_abast_agua_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_abast_agua_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifabast.code_name as tipoedifabast,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        ge.edf_edif_abast_agua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_abast_agua_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_abast_agua_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_abast_agua_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_abast_agua_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_abast_agua_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_abast_agua_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_abast_agua_a.proprioadm 
	left join dominios.tipo_edif_abast as dominio_tipoedifabast on dominio_tipoedifabast.code = edf_edif_abast_agua_a.tipoedifabast
#
DROP VIEW IF EXISTS views.edf_edif_habitacional_a#CREATE [VIEW] views.edf_edif_habitacional_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_habitacional_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_habitacional_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_habitacional_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_habitacional_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_habitacional_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_habitacional_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_habitacional_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_habitacional_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom
    [FROM]
        ge.edf_edif_habitacional_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_habitacional_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_habitacional_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_habitacional_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_habitacional_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_habitacional_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_habitacional_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_habitacional_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_rodoviaria_p#CREATE [VIEW] views.edf_edif_rodoviaria_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_rodoviaria_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_rodoviaria_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_rodoviaria_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_rodoviaria_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_rodoviaria_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_rodoviaria_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_rodoviaria_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_rodoviaria_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_rod dom join ge.edf_edif_rodoviaria_p tn on (array[dom.code] <@ tn.tipoedifrod and tn.id=ge.edf_edif_rodoviaria_p.id)),',' ) as tipoedifrod,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        ge.edf_edif_rodoviaria_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_rodoviaria_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_rodoviaria_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_rodoviaria_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_rodoviaria_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_rodoviaria_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_rodoviaria_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_rodoviaria_p.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_rodoviaria_p.jurisdicao
#
DROP VIEW IF EXISTS views.ppb_faixa_dominio_ferrovia_a#CREATE [VIEW] views.ppb_faixa_dominio_ferrovia_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	largurapartireixo as largurapartireixo
    [FROM]
        ge.ppb_faixa_dominio_ferrovia_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ppb_faixa_dominio_ferrovia_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = ppb_faixa_dominio_ferrovia_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = ppb_faixa_dominio_ferrovia_a.jurisdicao
#
DROP VIEW IF EXISTS views.cb_tunel_a#CREATE [VIEW] views.cb_tunel_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join ge.cb_tunel_a tn on (array[dom.code] <@ tn.modaluso and tn.id=ge.cb_tunel_a.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join ge.cb_tunel_a tn on (array[dom.code] <@ tn.matconstr and tn.id=ge.cb_tunel_a.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	altura as altura,
	dominio_tipotunel.code_name as tipotunel,
	geom as geom
    [FROM]
        ge.cb_tunel_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_tunel_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_tunel_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_tunel_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = cb_tunel_a.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = cb_tunel_a.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = cb_tunel_a.tipopavimentacao 
	left join dominios.tipo_tunel as dominio_tipotunel on dominio_tipotunel.code = cb_tunel_a.tipotunel
#
DROP VIEW IF EXISTS views.edf_edif_constr_portuaria_a#CREATE [VIEW] views.edf_edif_constr_portuaria_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_portuaria_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_portuaria_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_portuaria_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_portuaria_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_portuaria_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_portuaria_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_portuaria_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_portuaria_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_port dom join ge.edf_edif_constr_portuaria_a tn on (array[dom.code] <@ tn.tipoedifport and tn.id=ge.edf_edif_constr_portuaria_a.id)),',' ) as tipoedifport,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_complexo_portuario as id_complexo_portuario,
	id_org_industrial as id_org_industrial
    [FROM]
        ge.edf_edif_constr_portuaria_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_portuaria_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_portuaria_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_portuaria_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_portuaria_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_portuaria_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_portuaria_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_portuaria_a.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_constr_portuaria_a.jurisdicao
#
DROP VIEW IF EXISTS views.emu_poste_sinalizacao_p#CREATE [VIEW] views.emu_poste_sinalizacao_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codident as codident,
	dominio_matconstr.code_name as matconstr,
	array_to_string( array(select code_name from dominios.tipo_poste dom join ge.emu_poste_sinalizacao_p tn on (array[dom.code] <@ tn.tipoposte and tn.id=ge.emu_poste_sinalizacao_p.id)),',' ) as tipoposte,
	geom as geom
    [FROM]
        ge.emu_poste_sinalizacao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_poste_sinalizacao_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_poste_sinalizacao_p.matconstr
#
DROP VIEW IF EXISTS views.edf_edif_rodoviaria_a#CREATE [VIEW] views.edf_edif_rodoviaria_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_rodoviaria_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_rodoviaria_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_rodoviaria_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_rodoviaria_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_rodoviaria_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_rodoviaria_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_rodoviaria_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_rodoviaria_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_rod dom join ge.edf_edif_rodoviaria_a tn on (array[dom.code] <@ tn.tipoedifrod and tn.id=ge.edf_edif_rodoviaria_a.id)),',' ) as tipoedifrod,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        ge.edf_edif_rodoviaria_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_rodoviaria_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_rodoviaria_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_rodoviaria_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_rodoviaria_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_rodoviaria_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_rodoviaria_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_rodoviaria_a.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_rodoviaria_a.jurisdicao
#
DROP VIEW IF EXISTS views.emu_ciclovia_l#CREATE [VIEW] views.emu_ciclovia_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_revestimento.code_name as revestimento,
	geom as geom
    [FROM]
        ge.emu_ciclovia_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_ciclovia_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_ciclovia_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_ciclovia_l.situacaofisica 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = emu_ciclovia_l.revestimento
#
DROP VIEW IF EXISTS views.cb_area_lazer_a#CREATE [VIEW] views.cb_area_lazer_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.cb_area_lazer_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_lazer_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_pub_civil_a#CREATE [VIEW] views.edf_edif_pub_civil_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_pub_civil_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_pub_civil_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_pub_civil_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_pub_civil_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_pub_civil_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_pub_civil_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_pub_civil_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_pub_civil_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_edif_pub_civil_a tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_edif_pub_civil_a.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_edif_pub_civil_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_pub_civil_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_pub_civil_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_pub_civil_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_pub_civil_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_pub_civil_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_pub_civil_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_pub_civil_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_pub_civil_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_pub_civil_a.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_comunic_a#CREATE [VIEW] views.edf_edif_comunic_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_comunic_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_comunic_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_comunic_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_comunic_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_energia dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.tipoedifcomunic and tn.id=ge.edf_edif_comunic_a.id)),',' ) as tipoedifcomunic,
	array_to_string( array(select code_name from dominios.modalidade dom join ge.edf_edif_comunic_a tn on (array[dom.code] <@ tn.modalidade and tn.id=ge.edf_edif_comunic_a.id)),',' ) as modalidade,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        ge.edf_edif_comunic_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_comunic_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_comunic_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_comunic_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_comunic_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_comunic_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_comunic_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_comunic_a.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_duto_a#CREATE [VIEW] views.cb_area_duto_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_areavalvulas.code_name as areavalvulas,
	dominio_bombeamento.code_name as bombeamento,
	geom as geom
    [FROM]
        ge.cb_area_duto_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_duto_a.geometriaaproximada 
	left join dominios.booleano as dominio_areavalvulas on dominio_areavalvulas.code = cb_area_duto_a.areavalvulas 
	left join dominios.booleano as dominio_bombeamento on dominio_bombeamento.code = cb_area_duto_a.bombeamento
#
DROP VIEW IF EXISTS views.ver_jardim_a#CREATE [VIEW] views.ver_jardim_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_tipolavoura.code_name as tipolavoura,
	dominio_finalidade.code_name as finalidade,
	dominio_terreno.code_name as terreno,
	array_to_string( array(select code_name from dominios.cultivo_predominante dom join ge.ver_jardim_a tn on (array[dom.code] <@ tn.cultivopredominante and tn.id=ge.ver_jardim_a.id)),',' ) as cultivopredominante
    [FROM]
        ge.ver_jardim_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ver_jardim_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = ver_jardim_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = ver_jardim_a.classificacaoporte 
	left join dominios.tipo_lavoura as dominio_tipolavoura on dominio_tipolavoura.code = ver_jardim_a.tipolavoura 
	left join dominios.finalidade_cultura as dominio_finalidade on dominio_finalidade.code = ver_jardim_a.finalidade 
	left join dominios.condicao_terreno as dominio_terreno on dominio_terreno.code = ver_jardim_a.terreno
#
DROP VIEW IF EXISTS views.edf_edif_comunic_p#CREATE [VIEW] views.edf_edif_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_comunic_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_comunic_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_comunic_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_comunic_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_energia dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.tipoedifcomunic and tn.id=ge.edf_edif_comunic_p.id)),',' ) as tipoedifcomunic,
	array_to_string( array(select code_name from dominios.modalidade dom join ge.edf_edif_comunic_p tn on (array[dom.code] <@ tn.modalidade and tn.id=ge.edf_edif_comunic_p.id)),',' ) as modalidade,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        ge.edf_edif_comunic_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_comunic_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_comunic_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_comunic_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_comunic_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_comunic_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_comunic_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_comunic_p.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_pub_civil_p#CREATE [VIEW] views.edf_edif_pub_civil_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_pub_civil_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_pub_civil_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_pub_civil_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_pub_civil_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_pub_civil_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_pub_civil_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_pub_civil_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_pub_civil_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_edif_pub_civil_p tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_edif_pub_civil_p.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_edif_pub_civil_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_pub_civil_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_pub_civil_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_pub_civil_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_pub_civil_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_pub_civil_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_pub_civil_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_pub_civil_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_pub_civil_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_pub_civil_p.jurisdicao
#
DROP VIEW IF EXISTS views.cb_canteiro_central_l#CREATE [VIEW] views.cb_canteiro_central_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.cb_canteiro_central_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_canteiro_central_l.geometriaaproximada 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = cb_canteiro_central_l.situacaoespacial
#
DROP VIEW IF EXISTS views.cb_canteiro_central_a#CREATE [VIEW] views.cb_canteiro_central_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.cb_canteiro_central_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_canteiro_central_a.geometriaaproximada 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = cb_canteiro_central_a.situacaoespacial
#
DROP VIEW IF EXISTS views.cb_area_ruinas_a#CREATE [VIEW] views.cb_area_ruinas_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.cb_area_ruinas_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_ruinas_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_escadaria_l#CREATE [VIEW] views.emu_escadaria_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_escadaria_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_escadaria_l.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_escadaria_l.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_escadaria_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_escadaria_l.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_escadaria_l.situacaoespacial
#
DROP VIEW IF EXISTS views.edf_edif_saneamento_p#CREATE [VIEW] views.edf_edif_saneamento_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_saneamento_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_saneamento_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_saneamento_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_saneamento_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_saneamento_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_saneamento_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_saneamento_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_saneamento_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifsaneam.code_name as tipoedifsaneam,
	id_complexo_saneamento as id_complexo_saneamento
    [FROM]
        ge.edf_edif_saneamento_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_saneamento_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_saneamento_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_saneamento_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_saneamento_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_saneamento_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_saneamento_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_saneamento_p.proprioadm 
	left join dominios.tipo_edif_saneam as dominio_tipoedifsaneam on dominio_tipoedifsaneam.code = edf_edif_saneamento_p.tipoedifsaneam
#
DROP VIEW IF EXISTS views.edf_edif_abast_agua_p#CREATE [VIEW] views.edf_edif_abast_agua_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_abast_agua_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_abast_agua_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_abast_agua_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_abast_agua_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_abast_agua_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_abast_agua_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_abast_agua_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_abast_agua_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifabast.code_name as tipoedifabast,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        ge.edf_edif_abast_agua_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_abast_agua_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_abast_agua_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_abast_agua_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_abast_agua_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_abast_agua_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_abast_agua_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_abast_agua_p.proprioadm 
	left join dominios.tipo_edif_abast as dominio_tipoedifabast on dominio_tipoedifabast.code = edf_edif_abast_agua_p.tipoedifabast
#
DROP VIEW IF EXISTS views.edf_edif_energia_p#CREATE [VIEW] views.edf_edif_energia_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_energia_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_energia_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_energia_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_energia_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_energia_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_energia_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_energia_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_energia_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_energia dom join ge.edf_edif_energia_p tn on (array[dom.code] <@ tn.tipoedifenergia and tn.id=ge.edf_edif_energia_p.id)),',' ) as tipoedifenergia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	id_subest_transm_distrib_energia_eletrica as id_subest_transm_distrib_energia_eletrica
    [FROM]
        ge.edf_edif_energia_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_energia_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_energia_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_energia_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_energia_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_energia_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_energia_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_energia_p.proprioadm
#
DROP VIEW IF EXISTS views.laz_campo_quadra_a#CREATE [VIEW] views.laz_campo_quadra_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipocampoquadra.code_name as tipocampoquadra,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_campo_quadra_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_campo_quadra_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_campo_quadra_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_campo_quadra_a.situacaofisica 
	left join dominios.tipo_campo_quadra as dominio_tipocampoquadra on dominio_tipocampoquadra.code = laz_campo_quadra_a.tipocampoquadra
#
DROP VIEW IF EXISTS views.emu_escadaria_a#CREATE [VIEW] views.emu_escadaria_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_escadaria_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_escadaria_a.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_escadaria_a.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_escadaria_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_escadaria_a.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_escadaria_a.situacaoespacial
#
DROP VIEW IF EXISTS views.laz_sitio_arqueologico_p#CREATE [VIEW] views.laz_sitio_arqueologico_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	geom as geom
    [FROM]
        ge.laz_sitio_arqueologico_p 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = laz_sitio_arqueologico_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_sitio_arqueologico_p.cultura
#
DROP VIEW IF EXISTS views.edf_edif_saneamento_a#CREATE [VIEW] views.edf_edif_saneamento_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_saneamento_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_saneamento_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_saneamento_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_saneamento_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_saneamento_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_saneamento_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_saneamento_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_saneamento_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifsaneam.code_name as tipoedifsaneam,
	id_complexo_saneamento as id_complexo_saneamento
    [FROM]
        ge.edf_edif_saneamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_saneamento_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_saneamento_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_saneamento_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_saneamento_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_saneamento_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_saneamento_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_saneamento_a.proprioadm 
	left join dominios.tipo_edif_saneam as dominio_tipoedifsaneam on dominio_tipoedifsaneam.code = edf_edif_saneamento_a.tipoedifsaneam
#
DROP VIEW IF EXISTS views.edf_edif_energia_a#CREATE [VIEW] views.edf_edif_energia_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_energia_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_energia_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_energia_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_energia_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_energia_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_energia_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_energia_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_energia_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_energia dom join ge.edf_edif_energia_a tn on (array[dom.code] <@ tn.tipoedifenergia and tn.id=ge.edf_edif_energia_a.id)),',' ) as tipoedifenergia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	id_subest_transm_distrib_energia_eletrica as id_subest_transm_distrib_energia_eletrica
    [FROM]
        ge.edf_edif_energia_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_energia_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_energia_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_energia_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_energia_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_energia_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_energia_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_energia_a.proprioadm
#
DROP VIEW IF EXISTS views.laz_campo_quadra_p#CREATE [VIEW] views.laz_campo_quadra_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipocampoquadra.code_name as tipocampoquadra,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	geom as geom
    [FROM]
        ge.laz_campo_quadra_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_campo_quadra_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_campo_quadra_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_campo_quadra_p.situacaofisica 
	left join dominios.tipo_campo_quadra as dominio_tipocampoquadra on dominio_tipocampoquadra.code = laz_campo_quadra_p.tipocampoquadra
#
DROP VIEW IF EXISTS views.cb_ponte_a#CREATE [VIEW] views.cb_ponte_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join ge.cb_ponte_a tn on (array[dom.code] <@ tn.modaluso and tn.id=ge.cb_ponte_a.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join ge.cb_ponte_a tn on (array[dom.code] <@ tn.matconstr and tn.id=ge.cb_ponte_a.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipoponte.code_name as tipoponte,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        ge.cb_ponte_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_ponte_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_ponte_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_ponte_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = cb_ponte_a.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = cb_ponte_a.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = cb_ponte_a.tipopavimentacao 
	left join dominios.tipo_ponte as dominio_tipoponte on dominio_tipoponte.code = cb_ponte_a.tipoponte
#
DROP VIEW IF EXISTS views.cb_area_abast_agua_a#CREATE [VIEW] views.cb_area_abast_agua_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_abast_agua as id_complexo_abast_agua
    [FROM]
        ge.cb_area_abast_agua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_abast_agua_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_area_habitacional_a#CREATE [VIEW] views.cb_area_habitacional_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional
    [FROM]
        ge.cb_area_habitacional_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_habitacional_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_escadaria_p#CREATE [VIEW] views.emu_escadaria_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_escadaria_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_escadaria_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_escadaria_p.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_escadaria_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_escadaria_p.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_escadaria_p.situacaoespacial
#
DROP VIEW IF EXISTS views.ppb_area_dominial_a#CREATE [VIEW] views.ppb_area_dominial_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao
    [FROM]
        ge.ppb_area_dominial_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ppb_area_dominial_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = ppb_area_dominial_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = ppb_area_dominial_a.jurisdicao
#
DROP VIEW IF EXISTS views.cb_area_comerc_serv_a#CREATE [VIEW] views.cb_area_comerc_serv_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        ge.cb_area_comerc_serv_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_comerc_serv_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_poste_p#CREATE [VIEW] views.cb_poste_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codident as codident,
	dominio_matconstr.code_name as matconstr,
	array_to_string( array(select code_name from dominios.tipo_poste dom join ge.cb_poste_p tn on (array[dom.code] <@ tn.tipoposte and tn.id=ge.cb_poste_p.id)),',' ) as tipoposte,
	geom as geom
    [FROM]
        ge.cb_poste_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_poste_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = cb_poste_p.matconstr
#
DROP VIEW IF EXISTS views.cb_passeio_l#CREATE [VIEW] views.cb_passeio_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	largura as largura,
	dominio_calcada.code_name as calcada,
	array_to_string( array(select code_name from dominios.tipo_pavimentacao dom join ge.cb_passeio_l tn on (array[dom.code] <@ tn.pavimentacao and tn.id=ge.cb_passeio_l.id)),',' ) as pavimentacao,
	geom as geom
    [FROM]
        ge.cb_passeio_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_passeio_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_calcada on dominio_calcada.code = cb_passeio_l.calcada
#
DROP VIEW IF EXISTS views.edf_edif_policia_a#CREATE [VIEW] views.edf_edif_policia_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_policia_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_policia_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_policia_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_policia_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_policia_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_policia_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_policia_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_policia_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_edif_policia_a tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_edif_policia_a.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_edif_policia_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_policia_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_policia_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_policia_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_policia_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_policia_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_policia_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_policia_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_policia_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_policia_a.jurisdicao
#
DROP VIEW IF EXISTS views.cb_passeio_a#CREATE [VIEW] views.cb_passeio_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	largura as largura,
	dominio_calcada.code_name as calcada,
	array_to_string( array(select code_name from dominios.tipo_pavimentacao dom join ge.cb_passeio_a tn on (array[dom.code] <@ tn.pavimentacao and tn.id=ge.cb_passeio_a.id)),',' ) as pavimentacao,
	geom as geom
    [FROM]
        ge.cb_passeio_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_passeio_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_calcada on dominio_calcada.code = cb_passeio_a.calcada
#
DROP VIEW IF EXISTS views.edf_representacao_diplomatica_a#CREATE [VIEW] views.edf_representacao_diplomatica_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_representacao_diplomatica_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_representacao_diplomatica_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_representacao_diplomatica_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_representacao_diplomatica_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_representacao_diplomatica_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_representacao_diplomatica_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_representacao_diplomatica_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_representacao_diplomatica_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tiporepdiplomatica.code_name as tiporepdiplomatica
    [FROM]
        ge.edf_representacao_diplomatica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_representacao_diplomatica_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_representacao_diplomatica_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_representacao_diplomatica_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_representacao_diplomatica_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_representacao_diplomatica_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_representacao_diplomatica_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_representacao_diplomatica_a.proprioadm 
	left join dominios.tipo_rep_diplomatica as dominio_tiporepdiplomatica on dominio_tiporepdiplomatica.code = edf_representacao_diplomatica_a.tiporepdiplomatica
#
DROP VIEW IF EXISTS views.cb_quadra_a#CREATE [VIEW] views.cb_quadra_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_quadra_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_quadra_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_policia_p#CREATE [VIEW] views.edf_edif_policia_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_policia_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_policia_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_policia_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_policia_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_policia_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_policia_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_policia_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_policia_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_edif_policia_p tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_edif_policia_p.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_edif_policia_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_policia_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_policia_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_policia_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_policia_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_policia_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_policia_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_policia_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_policia_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_policia_p.jurisdicao
#
DROP VIEW IF EXISTS views.edf_representacao_diplomatica_p#CREATE [VIEW] views.edf_representacao_diplomatica_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_representacao_diplomatica_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_representacao_diplomatica_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_representacao_diplomatica_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_representacao_diplomatica_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_representacao_diplomatica_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_representacao_diplomatica_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_representacao_diplomatica_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_representacao_diplomatica_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tiporepdiplomatica.code_name as tiporepdiplomatica
    [FROM]
        ge.edf_representacao_diplomatica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_representacao_diplomatica_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_representacao_diplomatica_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_representacao_diplomatica_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_representacao_diplomatica_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_representacao_diplomatica_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_representacao_diplomatica_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_representacao_diplomatica_p.proprioadm 
	left join dominios.tipo_rep_diplomatica as dominio_tiporepdiplomatica on dominio_tiporepdiplomatica.code = edf_representacao_diplomatica_p.tiporepdiplomatica
#
DROP VIEW IF EXISTS views.edf_edif_comerc_serv_p#CREATE [VIEW] views.edf_edif_comerc_serv_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_comerc_serv dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.tipoedifcomercserv and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as tipoedifcomercserv,
	array_to_string( array(select code_name from dominios.finalidade dom join ge.edf_edif_comerc_serv_p tn on (array[dom.code] <@ tn.finalidade and tn.id=ge.edf_edif_comerc_serv_p.id)),',' ) as finalidade,
	id_estrut_transporte as id_estrut_transporte,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        ge.edf_edif_comerc_serv_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_comerc_serv_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_comerc_serv_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_comerc_serv_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_comerc_serv_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_comerc_serv_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_comerc_serv_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_comerc_serv_p.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_constr_est_med_fen_a#CREATE [VIEW] views.edf_edif_constr_est_med_fen_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_est_med_fen_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_est_med_fen_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_est_med_fen_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_est_med_fen_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_est_med_fen_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_est_med_fen_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_est_med_fen_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_est_med_fen_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_est_med_fenomenos as id_est_med_fenomenos
    [FROM]
        ge.edf_edif_constr_est_med_fen_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_est_med_fen_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_est_med_fen_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_est_med_fen_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_est_med_fen_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_est_med_fen_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_est_med_fen_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_est_med_fen_a.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_constr_turistica_a#CREATE [VIEW] views.edf_edif_constr_turistica_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_turistica_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_turistica_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_turistica_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_turistica_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_turistica_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_turistica_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_turistica_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_turistica_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifturist.code_name as tipoedifturist,
	dominio_ovgd.code_name as ovgd,
	dominio_tombada.code_name as tombada,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.edf_edif_constr_turistica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_turistica_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_turistica_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_turistica_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_turistica_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_turistica_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_turistica_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_turistica_a.proprioadm 
	left join dominios.tipo_edif_turist as dominio_tipoedifturist on dominio_tipoedifturist.code = edf_edif_constr_turistica_a.tipoedifturist 
	left join dominios.booleano_estendido as dominio_ovgd on dominio_ovgd.code = edf_edif_constr_turistica_a.ovgd 
	left join dominios.booleano as dominio_tombada on dominio_tombada.code = edf_edif_constr_turistica_a.tombada
#
DROP VIEW IF EXISTS views.emu_rampa_p#CREATE [VIEW] views.emu_rampa_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_rampa_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_rampa_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_rampa_p.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_rampa_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_rampa_p.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_rampa_p.situacaoespacial
#
DROP VIEW IF EXISTS views.emu_rampa_l#CREATE [VIEW] views.emu_rampa_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_rampa_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_rampa_l.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_rampa_l.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_rampa_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_rampa_l.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_rampa_l.situacaoespacial
#
DROP VIEW IF EXISTS views.edf_edif_constr_est_med_fen_p#CREATE [VIEW] views.edf_edif_constr_est_med_fen_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_est_med_fen_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_est_med_fen_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_est_med_fen_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_est_med_fen_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_est_med_fen_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_est_med_fen_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_est_med_fen_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_est_med_fen_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_est_med_fenomenos as id_est_med_fenomenos
    [FROM]
        ge.edf_edif_constr_est_med_fen_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_est_med_fen_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_est_med_fen_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_est_med_fen_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_est_med_fen_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_est_med_fen_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_est_med_fen_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_est_med_fen_p.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_comerc_serv_a#CREATE [VIEW] views.edf_edif_comerc_serv_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_comerc_serv dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.tipoedifcomercserv and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as tipoedifcomercserv,
	array_to_string( array(select code_name from dominios.finalidade dom join ge.edf_edif_comerc_serv_a tn on (array[dom.code] <@ tn.finalidade and tn.id=ge.edf_edif_comerc_serv_a.id)),',' ) as finalidade,
	id_estrut_transporte as id_estrut_transporte,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        ge.edf_edif_comerc_serv_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_comerc_serv_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_comerc_serv_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_comerc_serv_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_comerc_serv_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_comerc_serv_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_comerc_serv_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_comerc_serv_a.proprioadm
#
DROP VIEW IF EXISTS views.emu_rampa_a#CREATE [VIEW] views.emu_rampa_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_rampa_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_rampa_a.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_rampa_a.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_rampa_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_rampa_a.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_rampa_a.situacaoespacial
#
DROP VIEW IF EXISTS views.cb_delimitacao_fisica_l#CREATE [VIEW] views.cb_delimitacao_fisica_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipodelimfis.code_name as tipodelimfis,
	array_to_string( array(select code_name from dominios.mat_constr dom join ge.cb_delimitacao_fisica_l tn on (array[dom.code] <@ tn.matconstr and tn.id=ge.cb_delimitacao_fisica_l.id)),',' ) as matconstr,
	dominio_eletrificada.code_name as eletrificada,
	geom as geom
    [FROM]
        ge.cb_delimitacao_fisica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_delimitacao_fisica_l.geometriaaproximada 
	left join dominios.tipo_delim_fis as dominio_tipodelimfis on dominio_tipodelimfis.code = cb_delimitacao_fisica_l.tipodelimfis 
	left join dominios.booleano_estendido as dominio_eletrificada on dominio_eletrificada.code = cb_delimitacao_fisica_l.eletrificada
#
DROP VIEW IF EXISTS views.cb_area_estrut_transporte_a#CREATE [VIEW] views.cb_area_estrut_transporte_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_estrut_transporte as id_estrut_transporte,
	geom as geom
    [FROM]
        ge.cb_area_estrut_transporte_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_estrut_transporte_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_acesso_p#CREATE [VIEW] views.emu_acesso_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_acesso_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_acesso_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_acesso_p.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_acesso_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_acesso_p.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_acesso_p.situacaoespacial
#
DROP VIEW IF EXISTS views.emu_elevador_l#CREATE [VIEW] views.emu_elevador_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom,
	dominio_tipoelevador.code_name as tipoelevador
    [FROM]
        ge.emu_elevador_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_elevador_l.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_elevador_l.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_elevador_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_elevador_l.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_elevador_l.situacaoespacial 
	left join dominios.tipo_elevador as dominio_tipoelevador on dominio_tipoelevador.code = emu_elevador_l.tipoelevador
#
DROP VIEW IF EXISTS views.cb_entroncamento_area_a#CREATE [VIEW] views.cb_entroncamento_area_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoentroncamento.code_name as tipoentroncamento,
	geom as geom,
	id_entroncamento as id_entroncamento
    [FROM]
        ge.cb_entroncamento_area_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_entroncamento_area_a.geometriaaproximada 
	left join dominios.tipo_entroncamento as dominio_tipoentroncamento on dominio_tipoentroncamento.code = cb_entroncamento_area_a.tipoentroncamento
#
DROP VIEW IF EXISTS views.emu_elevador_a#CREATE [VIEW] views.emu_elevador_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom,
	dominio_tipoelevador.code_name as tipoelevador
    [FROM]
        ge.emu_elevador_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_elevador_a.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_elevador_a.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_elevador_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_elevador_a.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_elevador_a.situacaoespacial 
	left join dominios.tipo_elevador as dominio_tipoelevador on dominio_tipoelevador.code = emu_elevador_a.tipoelevador
#
DROP VIEW IF EXISTS views.emu_acesso_a#CREATE [VIEW] views.emu_acesso_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_acesso_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_acesso_a.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_acesso_a.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_acesso_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_acesso_a.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_acesso_a.situacaoespacial
#
DROP VIEW IF EXISTS views.edf_posto_policia_rod_federal_p#CREATE [VIEW] views.edf_posto_policia_rod_federal_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_policia_rod_federal_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_policia_rod_federal_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_policia_rod_federal_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_policia_rod_federal_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_policia_rod_federal_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_policia_rod_federal_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_policia_rod_federal_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_policia_rod_federal_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	organizacao as organizacao,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer,
	array_to_string( array(select code_name from dominios.tipo_org_civil dom join ge.edf_posto_policia_rod_federal_p tn on (array[dom.code] <@ tn.tipoedifpubcivil and tn.id=ge.edf_posto_policia_rod_federal_p.id)),',' ) as tipoedifpubcivil
    [FROM]
        ge.edf_posto_policia_rod_federal_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_policia_rod_federal_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_policia_rod_federal_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_policia_rod_federal_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_policia_rod_federal_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_policia_rod_federal_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_policia_rod_federal_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_policia_rod_federal_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_policia_rod_federal_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_policia_rod_federal_p.jurisdicao
#
DROP VIEW IF EXISTS views.laz_sitio_arqueologico_a#CREATE [VIEW] views.laz_sitio_arqueologico_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	geom as geom
    [FROM]
        ge.laz_sitio_arqueologico_a 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = laz_sitio_arqueologico_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_sitio_arqueologico_a.cultura
#
DROP VIEW IF EXISTS views.ver_descontinuidade_geometrica_a#CREATE [VIEW] views.ver_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.ver_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ver_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = ver_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.ver_arvore_isolada_p#CREATE [VIEW] views.ver_arvore_isolada_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_area_verde as id_area_verde
    [FROM]
        ge.ver_arvore_isolada_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ver_arvore_isolada_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.emu_elevador_p#CREATE [VIEW] views.emu_elevador_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom,
	dominio_tipoelevador.code_name as tipoelevador
    [FROM]
        ge.emu_elevador_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_elevador_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_elevador_p.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_elevador_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_elevador_p.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_elevador_p.situacaoespacial 
	left join dominios.tipo_elevador as dominio_tipoelevador on dominio_tipoelevador.code = emu_elevador_p.tipoelevador
#
DROP VIEW IF EXISTS views.cb_passagem_elevada_viaduto_a#CREATE [VIEW] views.cb_passagem_elevada_viaduto_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join ge.cb_passagem_elevada_viaduto_a tn on (array[dom.code] <@ tn.modaluso and tn.id=ge.cb_passagem_elevada_viaduto_a.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join ge.cb_passagem_elevada_viaduto_a tn on (array[dom.code] <@ tn.matconstr and tn.id=ge.cb_passagem_elevada_viaduto_a.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipopassagviad.code_name as tipopassagviad,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	gabhorizsup as gabhorizsup,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        ge.cb_passagem_elevada_viaduto_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_passagem_elevada_viaduto_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_passagem_elevada_viaduto_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_passagem_elevada_viaduto_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = cb_passagem_elevada_viaduto_a.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = cb_passagem_elevada_viaduto_a.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = cb_passagem_elevada_viaduto_a.tipopavimentacao 
	left join dominios.tipo_passag_viad as dominio_tipopassagviad on dominio_tipopassagviad.code = cb_passagem_elevada_viaduto_a.tipopassagviad
#
DROP VIEW IF EXISTS views.cb_area_religiosa_a#CREATE [VIEW] views.cb_area_religiosa_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_area_religiosa_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_religiosa_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_ensino_a#CREATE [VIEW] views.edf_edif_ensino_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_ensino_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_ensino_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_ensino_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_ensino_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_ensino_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_ensino_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_ensino_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_ensino_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_ensino as id_org_ensino
    [FROM]
        ge.edf_edif_ensino_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_ensino_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_ensino_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_ensino_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_ensino_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_ensino_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_ensino_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_ensino_a.proprioadm
#
DROP VIEW IF EXISTS views.cb_area_comunicacao_a#CREATE [VIEW] views.cb_area_comunicacao_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        ge.cb_area_comunicacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_comunicacao_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_desenv_social_p#CREATE [VIEW] views.edf_edif_desenv_social_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_desenv_social_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_desenv_social_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_desenv_social_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_desenv_social_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_desenv_social_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_desenv_social_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_desenv_social_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_desenv_social_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	sigla as sigla,
	codequipdesenvsocial as codequipdesenvsocial,
	dominio_tipoequipdesenvsocial.code_name as tipoequipdesenvsocial,
	dominio_localizacaoequipdesenvsocial.code_name as localizacaoequipdesenvsocial
    [FROM]
        ge.edf_edif_desenv_social_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_desenv_social_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_desenv_social_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_desenv_social_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_desenv_social_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_desenv_social_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_desenv_social_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_desenv_social_p.proprioadm 
	left join dominios.tipo_equip_desenv_social as dominio_tipoequipdesenvsocial on dominio_tipoequipdesenvsocial.code = edf_edif_desenv_social_p.tipoequipdesenvsocial 
	left join dominios.local_equip_desenv_social as dominio_localizacaoequipdesenvsocial on dominio_localizacaoequipdesenvsocial.code = edf_edif_desenv_social_p.localizacaoequipdesenvsocial
#
DROP VIEW IF EXISTS views.edf_edif_metro_ferroviaria_p#CREATE [VIEW] views.edf_edif_metro_ferroviaria_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_metro_ferroviaria_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_metro_ferroviaria_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_metro_ferroviaria_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_metro_ferroviaria_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_metro_ferroviaria_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_metro_ferroviaria_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_metro_ferroviaria_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_metro_ferroviaria_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_metro_ferrov dom join ge.edf_edif_metro_ferroviaria_p tn on (array[dom.code] <@ tn.tipoedifmetroferrov and tn.id=ge.edf_edif_metro_ferroviaria_p.id)),',' ) as tipoedifmetroferrov,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        ge.edf_edif_metro_ferroviaria_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_metro_ferroviaria_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_metro_ferroviaria_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_metro_ferroviaria_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_metro_ferroviaria_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_metro_ferroviaria_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_metro_ferroviaria_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_metro_ferroviaria_p.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_metro_ferroviaria_p.jurisdicao
#
DROP VIEW IF EXISTS views.laz_piscina_a#CREATE [VIEW] views.laz_piscina_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        ge.laz_piscina_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = laz_piscina_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_piscina_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = laz_piscina_a.situacaofisica
#
DROP VIEW IF EXISTS views.emu_acesso_l#CREATE [VIEW] views.emu_acesso_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	geom as geom
    [FROM]
        ge.emu_acesso_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = emu_acesso_l.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = emu_acesso_l.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_acesso_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_acesso_l.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = emu_acesso_l.situacaoespacial
#
DROP VIEW IF EXISTS views.edf_edif_ensino_p#CREATE [VIEW] views.edf_edif_ensino_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_ensino_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_ensino_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_ensino_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_ensino_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_ensino_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_ensino_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_ensino_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_ensino_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	id_org_ensino as id_org_ensino
    [FROM]
        ge.edf_edif_ensino_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_ensino_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_ensino_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_ensino_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_ensino_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_ensino_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_ensino_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_ensino_p.proprioadm
#
DROP VIEW IF EXISTS views.edf_edif_desenv_social_a#CREATE [VIEW] views.edf_edif_desenv_social_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_desenv_social_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_desenv_social_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_desenv_social_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_desenv_social_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_desenv_social_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_desenv_social_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_desenv_social_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_desenv_social_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	sigla as sigla,
	codequipdesenvsocial as codequipdesenvsocial,
	dominio_tipoequipdesenvsocial.code_name as tipoequipdesenvsocial,
	dominio_localizacaoequipdesenvsocial.code_name as localizacaoequipdesenvsocial
    [FROM]
        ge.edf_edif_desenv_social_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_desenv_social_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_desenv_social_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_desenv_social_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_desenv_social_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_desenv_social_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_desenv_social_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_desenv_social_a.proprioadm 
	left join dominios.tipo_equip_desenv_social as dominio_tipoequipdesenvsocial on dominio_tipoequipdesenvsocial.code = edf_edif_desenv_social_a.tipoequipdesenvsocial 
	left join dominios.local_equip_desenv_social as dominio_localizacaoequipdesenvsocial on dominio_localizacaoequipdesenvsocial.code = edf_edif_desenv_social_a.localizacaoequipdesenvsocial
#
DROP VIEW IF EXISTS views.edf_edif_metro_ferroviaria_a#CREATE [VIEW] views.edf_edif_metro_ferroviaria_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_metro_ferroviaria_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_metro_ferroviaria_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_metro_ferroviaria_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_metro_ferroviaria_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_metro_ferroviaria_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_metro_ferroviaria_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_metro_ferroviaria_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_metro_ferroviaria_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_metro_ferrov dom join ge.edf_edif_metro_ferroviaria_a tn on (array[dom.code] <@ tn.tipoedifmetroferrov and tn.id=ge.edf_edif_metro_ferroviaria_a.id)),',' ) as tipoedifmetroferrov,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_estrut_apoio as id_estrut_apoio
    [FROM]
        ge.edf_edif_metro_ferroviaria_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_metro_ferroviaria_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_metro_ferroviaria_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_metro_ferroviaria_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_metro_ferroviaria_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_metro_ferroviaria_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_metro_ferroviaria_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_metro_ferroviaria_a.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_metro_ferroviaria_a.jurisdicao
#
DROP VIEW IF EXISTS views.ppb_faixa_dominio_rodovia_a#CREATE [VIEW] views.ppb_faixa_dominio_rodovia_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	largurapartireixo as largurapartireixo
    [FROM]
        ge.ppb_faixa_dominio_rodovia_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ppb_faixa_dominio_rodovia_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = ppb_faixa_dominio_rodovia_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = ppb_faixa_dominio_rodovia_a.jurisdicao
#
DROP VIEW IF EXISTS views.edf_posto_policia_militar_a#CREATE [VIEW] views.edf_posto_policia_militar_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_posto_policia_militar_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_posto_policia_militar_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_posto_policia_militar_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_posto_policia_militar_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_posto_policia_militar_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_posto_policia_militar_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_posto_policia_militar_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_posto_policia_militar_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipoinstalmilitar.code_name as tipoinstalmilitar,
	organizacao as organizacao
    [FROM]
        ge.edf_posto_policia_militar_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_posto_policia_militar_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_posto_policia_militar_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_posto_policia_militar_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_posto_policia_militar_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_posto_policia_militar_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_posto_policia_militar_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_posto_policia_militar_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_posto_policia_militar_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_posto_policia_militar_a.jurisdicao 
	left join dominios.tipo_instal_militar as dominio_tipoinstalmilitar on dominio_tipoinstalmilitar.code = edf_posto_policia_militar_a.tipoinstalmilitar
#
DROP VIEW IF EXISTS views.edf_hab_indigena_p#CREATE [VIEW] views.edf_hab_indigena_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_hab_indigena_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_hab_indigena_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_hab_indigena_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_hab_indigena_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_hab_indigena_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_hab_indigena_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_hab_indigena_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_hab_indigena_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_coletiva.code_name as coletiva,
	dominio_isolada.code_name as isolada,
	id_aldeia_indigena as id_aldeia_indigena
    [FROM]
        ge.edf_hab_indigena_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_hab_indigena_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_hab_indigena_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_hab_indigena_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_hab_indigena_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_hab_indigena_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_hab_indigena_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_hab_indigena_p.proprioadm 
	left join dominios.booleano_estendido as dominio_coletiva on dominio_coletiva.code = edf_hab_indigena_p.coletiva 
	left join dominios.booleano_estendido as dominio_isolada on dominio_isolada.code = edf_hab_indigena_p.isolada
#
DROP VIEW IF EXISTS views.cb_trecho_rodoviario_a#CREATE [VIEW] views.cb_trecho_rodoviario_a as 
	SELECT
	id as id,
	nome as nome,
	sigla as sigla,
	codtrechorodov as codtrechorodov,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechorod.code_name as tipotrechorod,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_administracao.code_name as administracao,
	concessionaria as concessionaria,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_trafego.code_name as trafego,
	limitevelocidade as limitevelocidade,
	dominio_trechoemperimetrourbano.code_name as trechoemperimetrourbano,
	dominio_acostamento.code_name as acostamento,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	geom as geom
    [FROM]
        ge.cb_trecho_rodoviario_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_trecho_rodoviario_a.geometriaaproximada 
	left join dominios.tipo_trecho_rod as dominio_tipotrechorod on dominio_tipotrechorod.code = cb_trecho_rodoviario_a.tipotrechorod 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = cb_trecho_rodoviario_a.jurisdicao 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = cb_trecho_rodoviario_a.administracao 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = cb_trecho_rodoviario_a.revestimento 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_trecho_rodoviario_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_trecho_rodoviario_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_canteirodivisorio on dominio_canteirodivisorio.code = cb_trecho_rodoviario_a.canteirodivisorio 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = cb_trecho_rodoviario_a.trafego 
	left join dominios.booleano as dominio_trechoemperimetrourbano on dominio_trechoemperimetrourbano.code = cb_trecho_rodoviario_a.trechoemperimetrourbano 
	left join dominios.booleano as dominio_acostamento on dominio_acostamento.code = cb_trecho_rodoviario_a.acostamento 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = cb_trecho_rodoviario_a.tipopavimentacao
#
DROP VIEW IF EXISTS views.cb_area_saneamento_a#CREATE [VIEW] views.cb_area_saneamento_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        ge.cb_area_saneamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_saneamento_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_hab_indigena_a#CREATE [VIEW] views.edf_hab_indigena_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_hab_indigena_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_hab_indigena_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_hab_indigena_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_hab_indigena_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_hab_indigena_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_hab_indigena_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_hab_indigena_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_hab_indigena_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_coletiva.code_name as coletiva,
	dominio_isolada.code_name as isolada,
	id_aldeia_indigena as id_aldeia_indigena
    [FROM]
        ge.edf_hab_indigena_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_hab_indigena_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_hab_indigena_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_hab_indigena_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_hab_indigena_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_hab_indigena_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_hab_indigena_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_hab_indigena_a.proprioadm 
	left join dominios.booleano_estendido as dominio_coletiva on dominio_coletiva.code = edf_hab_indigena_a.coletiva 
	left join dominios.booleano_estendido as dominio_isolada on dominio_isolada.code = edf_hab_indigena_a.isolada
#
DROP VIEW IF EXISTS views.cb_travessia_pedrestre_a#CREATE [VIEW] views.cb_travessia_pedrestre_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_tipotravessiaped.code_name as tipotravessiaped,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        ge.cb_travessia_pedrestre_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_travessia_pedrestre_a.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = cb_travessia_pedrestre_a.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_travessia_pedrestre_a.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_travessia_pedrestre_a.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = cb_travessia_pedrestre_a.situacaoespacial 
	left join dominios.tipo_travessia_ped as dominio_tipotravessiaped on dominio_tipotravessiaped.code = cb_travessia_pedrestre_a.tipotravessiaped
#
DROP VIEW IF EXISTS views.cb_area_agropec_ext_veg_pesca_a#CREATE [VIEW] views.cb_area_agropec_ext_veg_pesca_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_destinadoa.code_name as destinadoa,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        ge.cb_area_agropec_ext_veg_pesca_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_area_agropec_ext_veg_pesca_a.geometriaaproximada 
	left join dominios.destinado_a as dominio_destinadoa on dominio_destinadoa.code = cb_area_agropec_ext_veg_pesca_a.destinadoa
#
DROP VIEW IF EXISTS views.edf_edif_constr_aeroportuaria_p#CREATE [VIEW] views.edf_edif_constr_aeroportuaria_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_aeroportuaria_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_aeroportuaria_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_aeroportuaria_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_aeroportuaria_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_aeroportuaria_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_aero dom join ge.edf_edif_constr_aeroportuaria_p tn on (array[dom.code] <@ tn.tipoedifaero and tn.id=ge.edf_edif_constr_aeroportuaria_p.id)),',' ) as tipoedifaero,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_complexo_aeroportuario as id_complexo_aeroportuario
    [FROM]
        ge.edf_edif_constr_aeroportuaria_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_aeroportuaria_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_aeroportuaria_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_aeroportuaria_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_aeroportuaria_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_aeroportuaria_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_aeroportuaria_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_aeroportuaria_p.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_constr_aeroportuaria_p.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_pub_militar_p#CREATE [VIEW] views.edf_edif_pub_militar_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_pub_militar_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_pub_militar_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_pub_militar_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_pub_militar_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_pub_militar_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_pub_militar_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_pub_militar_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_pub_militar_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipoinstalmilitar.code_name as tipoinstalmilitar,
	organizacao as organizacao
    [FROM]
        ge.edf_edif_pub_militar_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_pub_militar_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_pub_militar_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_pub_militar_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_pub_militar_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_pub_militar_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_pub_militar_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_pub_militar_p.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_pub_militar_p.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_pub_militar_p.jurisdicao 
	left join dominios.tipo_instal_militar as dominio_tipoinstalmilitar on dominio_tipoinstalmilitar.code = edf_edif_pub_militar_p.tipoinstalmilitar
#
DROP VIEW IF EXISTS views.cb_estacionamento_a#CREATE [VIEW] views.cb_estacionamento_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join ge.cb_estacionamento_a tn on (array[dom.code] <@ tn.modaluso and tn.id=ge.cb_estacionamento_a.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.administracao dom join ge.cb_estacionamento_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.cb_estacionamento_a.id)),',' ) as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.finalidade_patio dom join ge.cb_estacionamento_a tn on (array[dom.code] <@ tn.finalidadepatio and tn.id=ge.cb_estacionamento_a.id)),',' ) as finalidadepatio,
	id_estrut_transporte as id_estrut_transporte,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_industrial as id_org_industrial,
	id_org_ensino as id_org_ensino,
	geom as geom,
	dominio_publico.code_name as publico
    [FROM]
        ge.cb_estacionamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_estacionamento_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = cb_estacionamento_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = cb_estacionamento_a.situacaofisica 
	left join dominios.booleano as dominio_publico on dominio_publico.code = cb_estacionamento_a.publico
#
DROP VIEW IF EXISTS views.cb_espelho_dagua_a#CREATE [VIEW] views.cb_espelho_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	codident as codident,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        ge.cb_espelho_dagua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = cb_espelho_dagua_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.edf_edif_religiosa_p#CREATE [VIEW] views.edf_edif_religiosa_p as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_religiosa_p tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_religiosa_p.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_religiosa_p tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_religiosa_p.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_religiosa_p tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_religiosa_p.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_religiosa_p tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_religiosa_p.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipoedifrelig.code_name as tipoedifrelig,
	dominio_ensino.code_name as ensino,
	religiao as religiao,
	id_org_religiosa as id_org_religiosa,
	dominio_crista.code_name as crista
    [FROM]
        ge.edf_edif_religiosa_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_religiosa_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_religiosa_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_religiosa_p.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_religiosa_p.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_religiosa_p.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_religiosa_p.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_religiosa_p.proprioadm 
	left join dominios.tipo_edif_relig as dominio_tipoedifrelig on dominio_tipoedifrelig.code = edf_edif_religiosa_p.tipoedifrelig 
	left join dominios.booleano as dominio_ensino on dominio_ensino.code = edf_edif_religiosa_p.ensino 
	left join dominios.booleano as dominio_crista on dominio_crista.code = edf_edif_religiosa_p.crista
#
DROP VIEW IF EXISTS views.edf_edif_constr_aeroportuaria_a#CREATE [VIEW] views.edf_edif_constr_aeroportuaria_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_constr_aeroportuaria_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_constr_aeroportuaria_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_constr_aeroportuaria_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_constr_aeroportuaria_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_constr_aeroportuaria_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_constr_aeroportuaria_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_edif_aero dom join ge.edf_edif_constr_aeroportuaria_a tn on (array[dom.code] <@ tn.tipoedifaero and tn.id=ge.edf_edif_constr_aeroportuaria_a.id)),',' ) as tipoedifaero,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	id_complexo_aeroportuario as id_complexo_aeroportuario
    [FROM]
        ge.edf_edif_constr_aeroportuaria_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_constr_aeroportuaria_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_constr_aeroportuaria_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_constr_aeroportuaria_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_constr_aeroportuaria_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_constr_aeroportuaria_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_constr_aeroportuaria_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_constr_aeroportuaria_a.proprioadm 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_constr_aeroportuaria_a.jurisdicao
#
DROP VIEW IF EXISTS views.edf_edif_pub_militar_a#CREATE [VIEW] views.edf_edif_pub_militar_a as 
	SELECT
	id as id,
	nome as nome,
	numero as numero,
	bloco as bloco,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_matconstr.code_name as matconstr,
	numeropavimento as numeropavimento,
	dominio_turistica.code_name as turistica,
	dominio_cultura.code_name as cultura,
	array_to_string( array(select code_name from dominios.administracao dom join ge.edf_edif_pub_militar_a tn on (array[dom.code] <@ tn.administracao and tn.id=ge.edf_edif_pub_militar_a.id)),',' ) as administracao,
	array_to_string( array(select code_name from dominios.classe_ativ_econ dom join ge.edf_edif_pub_militar_a tn on (array[dom.code] <@ tn.classeativecon and tn.id=ge.edf_edif_pub_militar_a.id)),',' ) as classeativecon,
	array_to_string( array(select code_name from dominios.divisao_ativ_econ dom join ge.edf_edif_pub_militar_a tn on (array[dom.code] <@ tn.divisaoativecon and tn.id=ge.edf_edif_pub_militar_a.id)),',' ) as divisaoativecon,
	array_to_string( array(select code_name from dominios.grupo_ativ_econ dom join ge.edf_edif_pub_militar_a tn on (array[dom.code] <@ tn.grupoativecon and tn.id=ge.edf_edif_pub_militar_a.id)),',' ) as grupoativecon,
	dominio_proprioadm.code_name as proprioadm,
	numerosequencial as numerosequencial,
	numerometrico as numerometrico,
	cep as cep,
	pais as pais,
	unidadefederacao as unidadefederacao,
	municipio as municipio,
	bairro as bairro,
	logradouro as logradouro,
	id_assentamento_precario as id_assentamento_precario,
	id_complexo_habitacional as id_complexo_habitacional,
	geom as geom,
	dominio_tipousoedif.code_name as tipousoedif,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipoinstalmilitar.code_name as tipoinstalmilitar,
	organizacao as organizacao
    [FROM]
        ge.edf_edif_pub_militar_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = edf_edif_pub_militar_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = edf_edif_pub_militar_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = edf_edif_pub_militar_a.situacaofisica 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = edf_edif_pub_militar_a.matconstr 
	left join dominios.booleano_estendido as dominio_turistica on dominio_turistica.code = edf_edif_pub_militar_a.turistica 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = edf_edif_pub_militar_a.cultura 
	left join dominios.booleano as dominio_proprioadm on dominio_proprioadm.code = edf_edif_pub_militar_a.proprioadm 
	left join dominios.tipo_uso_edif as dominio_tipousoedif on dominio_tipousoedif.code = edf_edif_pub_militar_a.tipousoedif 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edf_edif_pub_militar_a.jurisdicao 
	left join dominios.tipo_instal_militar as dominio_tipoinstalmilitar on dominio_tipoinstalmilitar.code = edf_edif_pub_militar_a.tipoinstalmilitar
#
DROP VIEW IF EXISTS views.ver_descontinuidade_geometrica_p#CREATE [VIEW] views.ver_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        ge.ver_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = ver_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = ver_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.laz_parque_urbano#CREATE [VIEW] views.laz_parque_urbano as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_parque_urbano 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_parque_urbano.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_parque_urbano.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_parque_urbano.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_parque_urbano.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_parque_urbano.cultura
#
DROP VIEW IF EXISTS views.sau_org_saude#CREATE [VIEW] views.sau_org_saude as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	numeroleitos as numeroleitos,
	numeroleitosuti as numeroleitosuti
    [FROM]
        complexos.sau_org_saude 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_saude.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_saude.classeativecon
#
DROP VIEW IF EXISTS views.laz_hipica#CREATE [VIEW] views.laz_hipica as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_hipica 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_hipica.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_hipica.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_hipica.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_hipica.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_hipica.cultura
#
DROP VIEW IF EXISTS views.laz_complexo_desportivo#CREATE [VIEW] views.laz_complexo_desportivo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_complexo_desportivo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_complexo_desportivo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_complexo_desportivo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_complexo_desportivo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_complexo_desportivo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_complexo_desportivo.cultura
#
DROP VIEW IF EXISTS views.eco_frigorifico_matadouro#CREATE [VIEW] views.eco_frigorifico_matadouro as 
	SELECT
	id as id,
	nome as nome,
	dominio_secaoativecon.code_name as secaoativecon,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar,
	dominio_frigorifico.code_name as frigorifico,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        complexos.eco_frigorifico_matadouro 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = eco_frigorifico_matadouro.secaoativecon 
	left join dominios.booleano as dominio_frigorifico on dominio_frigorifico.code = eco_frigorifico_matadouro.frigorifico
#
DROP VIEW IF EXISTS views.edu_org_ensino_religiosa#CREATE [VIEW] views.edu_org_ensino_religiosa as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_jurisdicao.code_name as jurisdicao,
	id_org_religiosa as id_org_religiosa
    [FROM]
        complexos.edu_org_ensino_religiosa 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_religiosa.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = edu_org_ensino_religiosa.grupoativecon 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edu_org_ensino_religiosa.jurisdicao
#
DROP VIEW IF EXISTS views.lpal_localidade#CREATE [VIEW] views.lpal_localidade as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms
    [FROM]
        complexos.lpal_localidade 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_localidade.geometriaaproximada
#
DROP VIEW IF EXISTS views.adm_org_comerc_serv#CREATE [VIEW] views.adm_org_comerc_serv as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_finalidade.code_name as finalidade,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.adm_org_comerc_serv 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = adm_org_comerc_serv.divisaoativecon 
	left join dominios.finalidade as dominio_finalidade on dominio_finalidade.code = adm_org_comerc_serv.finalidade
#
DROP VIEW IF EXISTS views.laz_estande_de_tiro#CREATE [VIEW] views.laz_estande_de_tiro as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_estande_de_tiro 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_estande_de_tiro.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_estande_de_tiro.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_estande_de_tiro.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_estande_de_tiro.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_estande_de_tiro.cultura
#
DROP VIEW IF EXISTS views.lpal_aglomerado_rural_isolado#CREATE [VIEW] views.lpal_aglomerado_rural_isolado as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms,
	dominio_tipoaglomrurisol.code_name as tipoaglomrurisol
    [FROM]
        complexos.lpal_aglomerado_rural_isolado 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_aglomerado_rural_isolado.geometriaaproximada 
	left join dominios.tipo_aglom_rur_isol as dominio_tipoaglomrurisol on dominio_tipoaglomrurisol.code = lpal_aglomerado_rural_isolado.tipoaglomrurisol
#
DROP VIEW IF EXISTS views.cb_assentamento_precario#CREATE [VIEW] views.cb_assentamento_precario as 
	SELECT
	id as id,
	dominio_tipoassprec.code_name as tipoassprec
    [FROM]
        complexos.cb_assentamento_precario 
	left join dominios.tipo_assentamento_precario as dominio_tipoassprec on dominio_tipoassprec.code = cb_assentamento_precario.tipoassprec
#
DROP VIEW IF EXISTS views.lpal_capital#CREATE [VIEW] views.lpal_capital as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms,
	dominio_tipocapital.code_name as tipocapital
    [FROM]
        complexos.lpal_capital 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_capital.geometriaaproximada 
	left join dominios.tipo_capital as dominio_tipocapital on dominio_tipocapital.code = lpal_capital.tipocapital
#
DROP VIEW IF EXISTS views.enc_complexo_comunicacao#CREATE [VIEW] views.enc_complexo_comunicacao as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.enc_complexo_comunicacao 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = enc_complexo_comunicacao.classeativecon
#
DROP VIEW IF EXISTS views.dut_duto#CREATE [VIEW] views.dut_duto as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.dut_duto
#
DROP VIEW IF EXISTS views.adm_org_pub_civil#CREATE [VIEW] views.adm_org_pub_civil as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_administracao.code_name as administracao,
	dominio_tipoorgcivil.code_name as tipoorgcivil,
	dominio_poderpublico.code_name as poderpublico,
	dominio_administracaodireta.code_name as administracaodireta,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.adm_org_pub_civil 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = adm_org_pub_civil.classeativecon 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = adm_org_pub_civil.administracao 
	left join dominios.tipo_org_civil as dominio_tipoorgcivil on dominio_tipoorgcivil.code = adm_org_pub_civil.tipoorgcivil 
	left join dominios.poder_publico as dominio_poderpublico on dominio_poderpublico.code = adm_org_pub_civil.poderpublico 
	left join dominios.booleano as dominio_administracaodireta on dominio_administracaodireta.code = adm_org_pub_civil.administracaodireta
#
DROP VIEW IF EXISTS views.laz_complexo_recreativo#CREATE [VIEW] views.laz_complexo_recreativo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_complexo_recreativo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_complexo_recreativo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_complexo_recreativo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_complexo_recreativo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_complexo_recreativo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_complexo_recreativo.cultura
#
DROP VIEW IF EXISTS views.sau_org_saude_militar#CREATE [VIEW] views.sau_org_saude_militar as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	numeroleitos as numeroleitos,
	numeroleitosuti as numeroleitosuti,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.sau_org_saude_militar 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude_militar.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_saude_militar.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_saude_militar.classeativecon
#
DROP VIEW IF EXISTS views.adm_org_pub_militar#CREATE [VIEW] views.adm_org_pub_militar as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_tipoorgmilitar.code_name as tipoorgmilitar,
	dominio_administracao.code_name as administracao,
	id_org_pub_militar as id_org_pub_militar,
	id_instituicao_publica as id_instituicao_publica
    [FROM]
        complexos.adm_org_pub_militar 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = adm_org_pub_militar.classeativecon 
	left join dominios.tipo_org_militar as dominio_tipoorgmilitar on dominio_tipoorgmilitar.code = adm_org_pub_militar.tipoorgmilitar 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = adm_org_pub_militar.administracao
#
DROP VIEW IF EXISTS views.emu_terminal_ferroviario#CREATE [VIEW] views.emu_terminal_ferroviario as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.emu_terminal_ferroviario tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.emu_terminal_ferroviario.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.emu_terminal_ferroviario 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = emu_terminal_ferroviario.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = emu_terminal_ferroviario.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_terminal_ferroviario.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_terminal_ferroviario.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = emu_terminal_ferroviario.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = emu_terminal_ferroviario.tipoexposicao
#
DROP VIEW IF EXISTS views.laz_kartodromo#CREATE [VIEW] views.laz_kartodromo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_kartodromo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_kartodromo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_kartodromo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_kartodromo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_kartodromo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_kartodromo.cultura
#
DROP VIEW IF EXISTS views.adm_org_agropec_ext_veg_pesca#CREATE [VIEW] views.adm_org_agropec_ext_veg_pesca as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	id_org_industrial as id_org_industrial
    [FROM]
        complexos.adm_org_agropec_ext_veg_pesca 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = adm_org_agropec_ext_veg_pesca.divisaoativecon
#
DROP VIEW IF EXISTS views.cb_complexo_habitacional#CREATE [VIEW] views.cb_complexo_habitacional as 
	SELECT
	id as id,
	nome as nome,
	id_localidade as id_localidade
    [FROM]
        complexos.cb_complexo_habitacional
#
DROP VIEW IF EXISTS views.adm_org_religiosa#CREATE [VIEW] views.adm_org_religiosa as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_cultura.code_name as cultura
    [FROM]
        complexos.adm_org_religiosa 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = adm_org_religiosa.classeativecon 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = adm_org_religiosa.cultura
#
DROP VIEW IF EXISTS views.laz_autodromo#CREATE [VIEW] views.laz_autodromo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_autodromo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_autodromo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_autodromo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_autodromo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_autodromo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_autodromo.cultura
#
DROP VIEW IF EXISTS views.rtr_via_ferrea#CREATE [VIEW] views.rtr_via_ferrea as 
	SELECT
	id as id,
	nome as nome,
	codviaferrov as codviaferrov
    [FROM]
        complexos.rtr_via_ferrea
#
DROP VIEW IF EXISTS views.rod_estacao_rodoviaria#CREATE [VIEW] views.rod_estacao_rodoviaria as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.rod_estacao_rodoviaria tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.rod_estacao_rodoviaria.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.rod_estacao_rodoviaria 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = rod_estacao_rodoviaria.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = rod_estacao_rodoviaria.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = rod_estacao_rodoviaria.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = rod_estacao_rodoviaria.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = rod_estacao_rodoviaria.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = rod_estacao_rodoviaria.tipoexposicao
#
DROP VIEW IF EXISTS views.ver_area_verde_urbana#CREATE [VIEW] views.ver_area_verde_urbana as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.ver_area_verde_urbana
#
DROP VIEW IF EXISTS views.sau_org_servico_social_pub#CREATE [VIEW] views.sau_org_servico_social_pub as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	dominio_tipoorgsvsocial.code_name as tipoorgsvsocial,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sau_org_servico_social_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_servico_social_pub.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_servico_social_pub.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_servico_social_pub.classeativecon 
	left join dominios.tipo_org_sv_social as dominio_tipoorgsvsocial on dominio_tipoorgsvsocial.code = sau_org_servico_social_pub.tipoorgsvsocial
#
DROP VIEW IF EXISTS views.lpal_aglom_rural_de_ext_urbana#CREATE [VIEW] views.lpal_aglom_rural_de_ext_urbana as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms
    [FROM]
        complexos.lpal_aglom_rural_de_ext_urbana 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_aglom_rural_de_ext_urbana.geometriaaproximada
#
DROP VIEW IF EXISTS views.laz_hipodromo#CREATE [VIEW] views.laz_hipodromo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_hipodromo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_hipodromo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_hipodromo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_hipodromo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_hipodromo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_hipodromo.cultura
#
DROP VIEW IF EXISTS views.hid_arquipelago#CREATE [VIEW] views.hid_arquipelago as 
	SELECT
	id as id,
	nome as nome,
	dominio_jurisdicao.code_name as jurisdicao
    [FROM]
        complexos.hid_arquipelago 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = hid_arquipelago.jurisdicao
#
DROP VIEW IF EXISTS views.laz_marina#CREATE [VIEW] views.laz_marina as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_marina 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_marina.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_marina.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_marina.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_marina.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_marina.cultura
#
DROP VIEW IF EXISTS views.rdr_curso_dagua#CREATE [VIEW] views.rdr_curso_dagua as 
	SELECT
	id as id,
	nome as nome,
	dominio_dominialidade.code_name as dominialidade
    [FROM]
        complexos.rdr_curso_dagua 
	left join dominios.jurisdicao as dominio_dominialidade on dominio_dominialidade.code = rdr_curso_dagua.dominialidade
#
DROP VIEW IF EXISTS views.laz_velodromo#CREATE [VIEW] views.laz_velodromo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_velodromo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_velodromo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_velodromo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_velodromo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_velodromo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_velodromo.cultura
#
DROP VIEW IF EXISTS views.lpal_vila#CREATE [VIEW] views.lpal_vila as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms
    [FROM]
        complexos.lpal_vila 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_vila.geometriaaproximada
#
DROP VIEW IF EXISTS views.laz_jardim_zoologico#CREATE [VIEW] views.laz_jardim_zoologico as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_jardim_zoologico 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_jardim_zoologico.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_jardim_zoologico.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_jardim_zoologico.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_jardim_zoologico.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_jardim_zoologico.cultura
#
DROP VIEW IF EXISTS views.cb_area_subnormal#CREATE [VIEW] views.cb_area_subnormal as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.cb_area_subnormal
#
DROP VIEW IF EXISTS views.cb_conjunto_habitacional#CREATE [VIEW] views.cb_conjunto_habitacional as 
	SELECT
	id as id,
	nome as nome,
	id_localidade as id_localidade,
	id_assentamento_precario as id_assentamento_precario
    [FROM]
        complexos.cb_conjunto_habitacional
#
DROP VIEW IF EXISTS views.emu_terminal_rodoviario#CREATE [VIEW] views.emu_terminal_rodoviario as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.emu_terminal_rodoviario tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.emu_terminal_rodoviario.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.emu_terminal_rodoviario 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = emu_terminal_rodoviario.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = emu_terminal_rodoviario.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_terminal_rodoviario.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_terminal_rodoviario.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = emu_terminal_rodoviario.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = emu_terminal_rodoviario.tipoexposicao
#
DROP VIEW IF EXISTS views.laz_parque_tematico#CREATE [VIEW] views.laz_parque_tematico as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_parque_tematico 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_parque_tematico.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_parque_tematico.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_parque_tematico.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_parque_tematico.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_parque_tematico.cultura
#
DROP VIEW IF EXISTS views.laz_campo_aeromodelismo#CREATE [VIEW] views.laz_campo_aeromodelismo as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_campo_aeromodelismo 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_campo_aeromodelismo.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_campo_aeromodelismo.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_campo_aeromodelismo.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_campo_aeromodelismo.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_campo_aeromodelismo.cultura
#
DROP VIEW IF EXISTS views.sau_especialidade_medica#CREATE [VIEW] views.sau_especialidade_medica as 
	SELECT
	id as id,
	dominio_nomeespecialidade.code_name as nomeespecialidade,
	numeromedicos as numeromedicos,
	id_org_saude as id_org_saude
    [FROM]
        complexos.sau_especialidade_medica 
	left join dominios.nome_especialidade as dominio_nomeespecialidade on dominio_nomeespecialidade.code = sau_especialidade_medica.nomeespecialidade
#
DROP VIEW IF EXISTS views.edu_org_ensino_privada#CREATE [VIEW] views.edu_org_ensino_privada as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_jurisdicao.code_name as jurisdicao,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.edu_org_ensino_privada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_privada.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = edu_org_ensino_privada.grupoativecon 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edu_org_ensino_privada.jurisdicao
#
DROP VIEW IF EXISTS views.hdv_complexo_portuario#CREATE [VIEW] views.hdv_complexo_portuario as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.hdv_complexo_portuario tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.hdv_complexo_portuario.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipotransporte.code_name as tipotransporte,
	dominio_tipocomplexoportuario.code_name as tipocomplexoportuario,
	dominio_portosempapel.code_name as portosempapel,
	id_complexo_portuario as id_complexo_portuario
    [FROM]
        complexos.hdv_complexo_portuario 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_complexo_portuario.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = hdv_complexo_portuario.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_complexo_portuario.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_complexo_portuario.situacaofisica 
	left join dominios.tipo_transporte as dominio_tipotransporte on dominio_tipotransporte.code = hdv_complexo_portuario.tipotransporte 
	left join dominios.tipo_complexo_portuario as dominio_tipocomplexoportuario on dominio_tipocomplexoportuario.code = hdv_complexo_portuario.tipocomplexoportuario 
	left join dominios.booleano_estendido as dominio_portosempapel on dominio_portosempapel.code = hdv_complexo_portuario.portosempapel
#
DROP VIEW IF EXISTS views.rdr_sub_bacia_hidrografica#CREATE [VIEW] views.rdr_sub_bacia_hidrografica as 
	SELECT
	id as id,
	id_bacia_hidrografica as id_bacia_hidrografica
    [FROM]
        complexos.rdr_sub_bacia_hidrografica
#
DROP VIEW IF EXISTS views.enc_complexo_gerador_energia_eletrica#CREATE [VIEW] views.enc_complexo_gerador_energia_eletrica as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	id_org_comerc_serv as id_org_comerc_serv,
	dominio_operacional.code_name as operacional
    [FROM]
        complexos.enc_complexo_gerador_energia_eletrica 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = enc_complexo_gerador_energia_eletrica.classeativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_complexo_gerador_energia_eletrica.operacional
#
DROP VIEW IF EXISTS views.laz_campo_de_golfe#CREATE [VIEW] views.laz_campo_de_golfe as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_campo_de_golfe 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_campo_de_golfe.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_campo_de_golfe.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_campo_de_golfe.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_campo_de_golfe.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_campo_de_golfe.cultura
#
DROP VIEW IF EXISTS views.adm_instituicao_publica#CREATE [VIEW] views.adm_instituicao_publica as 
	SELECT
	id as id,
	nome as nome,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_administracao.code_name as administracao,
	dominio_poderpublico.code_name as poderpublico,
	id_instituicao_publica as id_instituicao_publica,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.adm_instituicao_publica 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = adm_instituicao_publica.grupoativecon 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = adm_instituicao_publica.administracao 
	left join dominios.poder_publico as dominio_poderpublico on dominio_poderpublico.code = adm_instituicao_publica.poderpublico
#
DROP VIEW IF EXISTS views.tra_entroncamento#CREATE [VIEW] views.tra_entroncamento as 
	SELECT
	id as id,
	nome as nome,
	dominio_tipoentroncamento.code_name as tipoentroncamento
    [FROM]
        complexos.tra_entroncamento 
	left join dominios.tipo_entroncamento as dominio_tipoentroncamento on dominio_tipoentroncamento.code = tra_entroncamento.tipoentroncamento
#
DROP VIEW IF EXISTS views.eco_madeireira#CREATE [VIEW] views.eco_madeireira as 
	SELECT
	id as id,
	nome as nome,
	dominio_secaoativecon.code_name as secaoativecon,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca
    [FROM]
        complexos.eco_madeireira 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = eco_madeireira.secaoativecon
#
DROP VIEW IF EXISTS views.sb_complexo_abast_agua#CREATE [VIEW] views.sb_complexo_abast_agua as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sb_complexo_abast_agua 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sb_complexo_abast_agua.classeativecon 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sb_complexo_abast_agua.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_complexo_abast_agua.operacional
#
DROP VIEW IF EXISTS views.sau_org_saude_privada#CREATE [VIEW] views.sau_org_saude_privada as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	numeroleitos as numeroleitos,
	numeroleitosuti as numeroleitosuti,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        complexos.sau_org_saude_privada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude_privada.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_saude_privada.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_saude_privada.classeativecon
#
DROP VIEW IF EXISTS views.laz_parque_aquatico#CREATE [VIEW] views.laz_parque_aquatico as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_parque_aquatico 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_parque_aquatico.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_parque_aquatico.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_parque_aquatico.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_parque_aquatico.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_parque_aquatico.cultura
#
DROP VIEW IF EXISTS views.adm_org_industrial#CREATE [VIEW] views.adm_org_industrial as 
	SELECT
	id as id,
	nome as nome,
	dominio_secaoativecon.code_name as secaoativecon,
	id_org_pub_civil as id_org_pub_civil,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.adm_org_industrial 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = adm_org_industrial.secaoativecon
#
DROP VIEW IF EXISTS views.rdr_arruamento#CREATE [VIEW] views.rdr_arruamento as 
	SELECT
	id as id
    [FROM]
        complexos.rdr_arruamento
#
DROP VIEW IF EXISTS views.lpal_aglomerado_rural#CREATE [VIEW] views.lpal_aglomerado_rural as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms
    [FROM]
        complexos.lpal_aglomerado_rural 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_aglomerado_rural.geometriaaproximada
#
DROP VIEW IF EXISTS views.laz_jardim_botanico#CREATE [VIEW] views.laz_jardim_botanico as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_jardim_botanico 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_jardim_botanico.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_jardim_botanico.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_jardim_botanico.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_jardim_botanico.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_jardim_botanico.cultura
#
DROP VIEW IF EXISTS views.laz_clube_social#CREATE [VIEW] views.laz_clube_social as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_clube_social 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_clube_social.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_clube_social.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_clube_social.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_clube_social.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_clube_social.cultura
#
DROP VIEW IF EXISTS views.rdr_trecho_curso_dagua#CREATE [VIEW] views.rdr_trecho_curso_dagua as 
	SELECT
	id as id,
	nome as nome,
	id_curso_dagua as id_curso_dagua,
	id_elemento_hidrografico as id_elemento_hidrografico
    [FROM]
        complexos.rdr_trecho_curso_dagua
#
DROP VIEW IF EXISTS views.tra_estrut_apoio#CREATE [VIEW] views.tra_estrut_apoio as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.tra_estrut_apoio tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.tra_estrut_apoio.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.tra_estrut_apoio 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_estrut_apoio.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = tra_estrut_apoio.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_estrut_apoio.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_estrut_apoio.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = tra_estrut_apoio.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = tra_estrut_apoio.tipoexposicao
#
DROP VIEW IF EXISTS views.sb_complexo_saneamento#CREATE [VIEW] views.sb_complexo_saneamento as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sb_complexo_saneamento 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sb_complexo_saneamento.classeativecon 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sb_complexo_saneamento.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_complexo_saneamento.operacional
#
DROP VIEW IF EXISTS views.fer_estacao_metroviaria#CREATE [VIEW] views.fer_estacao_metroviaria as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.fer_estacao_metroviaria tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.fer_estacao_metroviaria.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.fer_estacao_metroviaria 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = fer_estacao_metroviaria.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = fer_estacao_metroviaria.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_estacao_metroviaria.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_estacao_metroviaria.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = fer_estacao_metroviaria.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = fer_estacao_metroviaria.tipoexposicao
#
DROP VIEW IF EXISTS views.edu_org_ensino_pub#CREATE [VIEW] views.edu_org_ensino_pub as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_jurisdicao.code_name as jurisdicao,
	id_org_pub_militar as id_org_pub_militar,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.edu_org_ensino_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_pub.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = edu_org_ensino_pub.grupoativecon 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edu_org_ensino_pub.jurisdicao
#
DROP VIEW IF EXISTS views.sau_org_saude_pub#CREATE [VIEW] views.sau_org_saude_pub as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	numeroleitos as numeroleitos,
	numeroleitosuti as numeroleitosuti,
	id_org_pub_civil as id_org_pub_civil
    [FROM]
        complexos.sau_org_saude_pub 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_saude_pub.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_saude_pub.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_saude_pub.classeativecon
#
DROP VIEW IF EXISTS views.cb_favela#CREATE [VIEW] views.cb_favela as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.cb_favela
#
DROP VIEW IF EXISTS views.edu_org_ensino_militar#CREATE [VIEW] views.edu_org_ensino_militar as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_jurisdicao.code_name as jurisdicao,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.edu_org_ensino_militar 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino_militar.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = edu_org_ensino_militar.grupoativecon 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edu_org_ensino_militar.jurisdicao
#
DROP VIEW IF EXISTS views.rdr_elemento_hidrografico#CREATE [VIEW] views.rdr_elemento_hidrografico as 
	SELECT
	id as id,
	id_sub_bacia_hidrografica as id_sub_bacia_hidrografica
    [FROM]
        complexos.rdr_elemento_hidrografico
#
DROP VIEW IF EXISTS views.cb_palafitas#CREATE [VIEW] views.cb_palafitas as 
	SELECT
	id as id,
	nome as nome
    [FROM]
        complexos.cb_palafitas
#
DROP VIEW IF EXISTS views.ver_area_verde#CREATE [VIEW] views.ver_area_verde as 
	SELECT
	id as id,
	nome as nome,
	dominio_paisagismo.code_name as paisagismo,
	dominio_administracao.code_name as administracao,
	id_area_verde_urbana as id_area_verde_urbana,
	id_complexo_desportivo_lazer as id_complexo_desportivo_lazer
    [FROM]
        complexos.ver_area_verde 
	left join dominios.booleano as dominio_paisagismo on dominio_paisagismo.code = ver_area_verde.paisagismo 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = ver_area_verde.administracao
#
DROP VIEW IF EXISTS views.lpal_cidade#CREATE [VIEW] views.lpal_cidade as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geocodigo as geocodigo,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms
    [FROM]
        complexos.lpal_cidade 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_cidade.geometriaaproximada
#
DROP VIEW IF EXISTS views.cb_condominio#CREATE [VIEW] views.cb_condominio as 
	SELECT
	id as id,
	nome as nome,
	id_localidade as id_localidade
    [FROM]
        complexos.cb_condominio
#
DROP VIEW IF EXISTS views.enc_subest_transm_distrib_energia_eletrica#CREATE [VIEW] views.enc_subest_transm_distrib_energia_eletrica as 
	SELECT
	id as id,
	nome as nome,
	dominio_classeativecon.code_name as classeativecon,
	dominio_operacional.code_name as operacional,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica
    [FROM]
        complexos.enc_subest_transm_distrib_energia_eletrica 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = enc_subest_transm_distrib_energia_eletrica.classeativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_subest_transm_distrib_energia_eletrica.operacional
#
DROP VIEW IF EXISTS views.pto_est_med_fenomenos#CREATE [VIEW] views.pto_est_med_fenomenos as 
	SELECT
	id as id,
	nome as nome,
	orgaoenteresp as orgaoenteresp,
	id_est_med_fenomenos as id_est_med_fenomenos
    [FROM]
        complexos.pto_est_med_fenomenos
#
DROP VIEW IF EXISTS views.laz_pesque_pague#CREATE [VIEW] views.laz_pesque_pague as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_pesque_pague 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_pesque_pague.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_pesque_pague.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_pesque_pague.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_pesque_pague.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_pesque_pague.cultura
#
DROP VIEW IF EXISTS views.edu_org_ensino#CREATE [VIEW] views.edu_org_ensino as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_jurisdicao.code_name as jurisdicao
    [FROM]
        complexos.edu_org_ensino 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = edu_org_ensino.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = edu_org_ensino.grupoativecon 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = edu_org_ensino.jurisdicao
#
DROP VIEW IF EXISTS views.fer_estacao_ferroviaria#CREATE [VIEW] views.fer_estacao_ferroviaria as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.fer_estacao_ferroviaria tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.fer_estacao_ferroviaria.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.fer_estacao_ferroviaria 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = fer_estacao_ferroviaria.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = fer_estacao_ferroviaria.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_estacao_ferroviaria.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_estacao_ferroviaria.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = fer_estacao_ferroviaria.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = fer_estacao_ferroviaria.tipoexposicao
#
DROP VIEW IF EXISTS views.tra_estrut_transporte#CREATE [VIEW] views.tra_estrut_transporte as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.tra_estrut_transporte tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.tra_estrut_transporte.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica
    [FROM]
        complexos.tra_estrut_transporte 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = tra_estrut_transporte.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = tra_estrut_transporte.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_estrut_transporte.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_estrut_transporte.situacaofisica
#
DROP VIEW IF EXISTS views.sau_org_servico_social#CREATE [VIEW] views.sau_org_servico_social as 
	SELECT
	id as id,
	nome as nome,
	dominio_administracao.code_name as administracao,
	dominio_grupoativecon.code_name as grupoativecon,
	dominio_classeativecon.code_name as classeativecon,
	dominio_tipoorgsvsocial.code_name as tipoorgsvsocial
    [FROM]
        complexos.sau_org_servico_social 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = sau_org_servico_social.administracao 
	left join dominios.grupo_ativ_econ as dominio_grupoativecon on dominio_grupoativecon.code = sau_org_servico_social.grupoativecon 
	left join dominios.classe_ativ_econ as dominio_classeativecon on dominio_classeativecon.code = sau_org_servico_social.classeativecon 
	left join dominios.tipo_org_sv_social as dominio_tipoorgsvsocial on dominio_tipoorgsvsocial.code = sau_org_servico_social.tipoorgsvsocial
#
DROP VIEW IF EXISTS views.aer_complexo_aeroportuario#CREATE [VIEW] views.aer_complexo_aeroportuario as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.aer_complexo_aeroportuario tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.aer_complexo_aeroportuario.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	siglaicao as siglaicao,
	dominio_tipocomplexoaero.code_name as tipocomplexoaero,
	dominio_classificacao.code_name as classificacao,
	latoficial as latoficial,
	altitude as altitude,
	siglaiata as siglaiata,
	longoficial as longoficial
    [FROM]
        complexos.aer_complexo_aeroportuario 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = aer_complexo_aeroportuario.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = aer_complexo_aeroportuario.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = aer_complexo_aeroportuario.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = aer_complexo_aeroportuario.situacaofisica 
	left join dominios.tipo_complexo_aeroportuario as dominio_tipocomplexoaero on dominio_tipocomplexoaero.code = aer_complexo_aeroportuario.tipocomplexoaero 
	left join dominios.classificacao as dominio_classificacao on dominio_classificacao.code = aer_complexo_aeroportuario.classificacao
#
DROP VIEW IF EXISTS views.lpal_aldeia_indigena#CREATE [VIEW] views.lpal_aldeia_indigena as 
	SELECT
	id as id,
	nome as nome,
	id_localidade as id_localidade,
	codigofunai as codigofunai,
	terraindigena as terraindigena,
	etnia as etnia
    [FROM]
        complexos.lpal_aldeia_indigena
#
DROP VIEW IF EXISTS views.rdr_bacia_hidrografica#CREATE [VIEW] views.rdr_bacia_hidrografica as 
	SELECT
	id as id
    [FROM]
        complexos.rdr_bacia_hidrografica
#
DROP VIEW IF EXISTS views.laz_complexo_desportivo_lazer#CREATE [VIEW] views.laz_complexo_desportivo_lazer as 
	SELECT
	id as id,
	nome as nome,
	dominio_divisaoativecon.code_name as divisaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_administracao.code_name as administracao,
	dominio_turistico.code_name as turistico,
	dominio_cultura.code_name as cultura,
	id_org_religiosa as id_org_religiosa,
	id_org_pub_civil as id_org_pub_civil,
	id_org_ensino as id_org_ensino,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        complexos.laz_complexo_desportivo_lazer 
	left join dominios.divisao_ativ_econ as dominio_divisaoativecon on dominio_divisaoativecon.code = laz_complexo_desportivo_lazer.divisaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = laz_complexo_desportivo_lazer.operacional 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = laz_complexo_desportivo_lazer.administracao 
	left join dominios.booleano_estendido as dominio_turistico on dominio_turistico.code = laz_complexo_desportivo_lazer.turistico 
	left join dominios.booleano_estendido as dominio_cultura on dominio_cultura.code = laz_complexo_desportivo_lazer.cultura
#
DROP VIEW IF EXISTS views.emu_terminal_hidroviario#CREATE [VIEW] views.emu_terminal_hidroviario as 
	SELECT
	id as id,
	nome as nome,
	array_to_string( array(select code_name from dominios.modal_uso dom join complexos.emu_terminal_hidroviario tn on (array[dom.code] <@ tn.modaluso and tn.id=complexos.emu_terminal_hidroviario.id)),',' ) as modaluso,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoestrut.code_name as tipoestrut,
	dominio_tipoexposicao.code_name as tipoexposicao
    [FROM]
        complexos.emu_terminal_hidroviario 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = emu_terminal_hidroviario.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = emu_terminal_hidroviario.jurisdicao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = emu_terminal_hidroviario.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = emu_terminal_hidroviario.situacaofisica 
	left join dominios.tipo_estrut as dominio_tipoestrut on dominio_tipoestrut.code = emu_terminal_hidroviario.tipoestrut 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = emu_terminal_hidroviario.tipoexposicao
#
DROP VIEW IF EXISTS views.adm_org_ext_mineral#CREATE [VIEW] views.adm_org_ext_mineral as 
	SELECT
	id as id,
	nome as nome,
	dominio_secaoativecon.code_name as secaoativecon
    [FROM]
        complexos.adm_org_ext_mineral 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = adm_org_ext_mineral.secaoativecon
#
DROP VIEW IF EXISTS views.hdv_eclusa_p#CREATE [VIEW] views.hdv_eclusa_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_eclusa_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_eclusa_p.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hdv_eclusa_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_eclusa_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_eclusa_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_eclusa_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_recife_p#CREATE [VIEW] views.hid_recife_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        pe.hid_recife_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_p.geometriaaproximada 
	left join dominios.tipo_recife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_p.tiporecife 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_recife_p.situacaoemagua 
	left join dominios.situacao_costa as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_p.situacaocosta
#
DROP VIEW IF EXISTS views.lpal_unidade_protegida_a#CREATE [VIEW] views.lpal_unidade_protegida_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_protegida_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_protegida_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_protegida_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_protegida_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_protegida_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.dut_galeria_bueiro_l#CREATE [VIEW] views.dut_galeria_bueiro_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	array_to_string( array(select code_name from dominios.mat_transp dom join pe.dut_galeria_bueiro_l tn on (array[dom.code] <@ tn.mattransp and tn.id=pe.dut_galeria_bueiro_l.id)),',' ) as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.dut_galeria_bueiro_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.dut_galeria_bueiro_l.id)),',' ) as matconstr,
	nrdutos as nrdutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom,
	dominio_finalidade.code_name as finalidade,
	pesosuportmaximo as pesosuportmaximo,
	id_via_ferrea as id_via_ferrea
    [FROM]
        pe.dut_galeria_bueiro_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_galeria_bueiro_l.geometriaaproximada 
	left join dominios.tipo_trecho_duto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = dut_galeria_bueiro_l.tipotrechoduto 
	left join dominios.setor as dominio_setor on dominio_setor.code = dut_galeria_bueiro_l.setor 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = dut_galeria_bueiro_l.posicaorelativa 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = dut_galeria_bueiro_l.situacaoespacial 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = dut_galeria_bueiro_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = dut_galeria_bueiro_l.situacaofisica 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = dut_galeria_bueiro_l.finalidade
#
DROP VIEW IF EXISTS views.rel_pico_p#CREATE [VIEW] views.rel_pico_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_pico_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_pico_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_pico_p.tipoelemnat
#
DROP VIEW IF EXISTS views.hdv_eclusa_l#CREATE [VIEW] views.hdv_eclusa_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_eclusa_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_eclusa_l.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hdv_eclusa_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_eclusa_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_eclusa_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_eclusa_l.situacaofisica
#
DROP VIEW IF EXISTS views.lpal_municipio_a#CREATE [VIEW] views.lpal_municipio_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	geocodigo as geocodigo,
	anodereferencia as anodereferencia
    [FROM]
        pe.lpal_municipio_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_municipio_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.hdv_eclusa_a#CREATE [VIEW] views.hdv_eclusa_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	desnivel as desnivel,
	largura as largura,
	extensao as extensao,
	calado as calado,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_eclusa_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_eclusa_a.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hdv_eclusa_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_eclusa_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_eclusa_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_eclusa_a.situacaofisica
#
DROP VIEW IF EXISTS views.pto_pto_controle_p#CREATE [VIEW] views.pto_pto_controle_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	altitudegeometrica as altitudegeometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	outrarefplan as outrarefplan,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom,
	dominio_tipoptocontrole.code_name as tipoptocontrole,
	dominio_materializado.code_name as materializado,
	codprojeto as codprojeto
    [FROM]
        pe.pto_pto_controle_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_controle_p.geometriaaproximada 
	left join dominios.tipo_ref as dominio_tiporef on dominio_tiporef.code = pto_pto_controle_p.tiporef 
	left join dominios.sistema_geodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_controle_p.sistemageodesico 
	left join dominios.referencial_altim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_controle_p.referencialaltim 
	left join dominios.tipo_pto_controle as dominio_tipoptocontrole on dominio_tipoptocontrole.code = pto_pto_controle_p.tipoptocontrole 
	left join dominios.booleano_estendido as dominio_materializado on dominio_materializado.code = pto_pto_controle_p.materializado
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_l#CREATE [VIEW] views.rel_elemento_fisiog_natural_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_elemento_fisiog_natural_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_l.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_l.tipoelemnat
#
DROP VIEW IF EXISTS views.hid_barragem_p#CREATE [VIEW] views.hid_barragem_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_barragem_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_barragem_p.id)),',' ) as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.hid_barragem_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_p.geometriaaproximada 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_p.usoprincipal 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_barragem_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_p.situacaofisica
#
DROP VIEW IF EXISTS views.rod_trecho_rodoviario_l#CREATE [VIEW] views.rod_trecho_rodoviario_l as 
	SELECT
	id as id,
	nome as nome,
	sigla as sigla,
	codtrechorodov as codtrechorodov,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechorod.code_name as tipotrechorod,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_administracao.code_name as administracao,
	concessionaria as concessionaria,
	dominio_revestimento.code_name as revestimento,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_canteirodivisorio.code_name as canteirodivisorio,
	nrpistas as nrpistas,
	nrfaixas as nrfaixas,
	dominio_trafego.code_name as trafego,
	limitevelocidade as limitevelocidade,
	dominio_trechoemperimetrourbano.code_name as trechoemperimetrourbano,
	dominio_acostamento.code_name as acostamento,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	geom as geom
    [FROM]
        pe.rod_trecho_rodoviario_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_trecho_rodoviario_l.geometriaaproximada 
	left join dominios.tipo_trecho_rod as dominio_tipotrechorod on dominio_tipotrechorod.code = rod_trecho_rodoviario_l.tipotrechorod 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = rod_trecho_rodoviario_l.jurisdicao 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = rod_trecho_rodoviario_l.administracao 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = rod_trecho_rodoviario_l.revestimento 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = rod_trecho_rodoviario_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = rod_trecho_rodoviario_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_canteirodivisorio on dominio_canteirodivisorio.code = rod_trecho_rodoviario_l.canteirodivisorio 
	left join dominios.trafego as dominio_trafego on dominio_trafego.code = rod_trecho_rodoviario_l.trafego 
	left join dominios.booleano as dominio_trechoemperimetrourbano on dominio_trechoemperimetrourbano.code = rod_trecho_rodoviario_l.trechoemperimetrourbano 
	left join dominios.booleano as dominio_acostamento on dominio_acostamento.code = rod_trecho_rodoviario_l.acostamento 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = rod_trecho_rodoviario_l.tipopavimentacao
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_p#CREATE [VIEW] views.eco_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.eco_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_a#CREATE [VIEW] views.rel_elemento_fisiog_natural_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_elemento_fisiog_natural_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_a.tipoelemnat
#
DROP VIEW IF EXISTS views.veg_veg_natural_a#CREATE [VIEW] views.veg_veg_natural_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_veg_natural_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_natural_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_veg_natural_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_natural_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_veg_natural_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_veg_natural_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_veg_natural_a.densidade
#
DROP VIEW IF EXISTS views.lpal_linha_de_limite_l#CREATE [VIEW] views.lpal_linha_de_limite_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_referenciallegal.code_name as referenciallegal,
	obssituacao as obssituacao,
	extensao as extensao,
	geom as geom
    [FROM]
        pe.lpal_linha_de_limite_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_linha_de_limite_l.geometriaaproximada 
	left join dominios.referencial_legal as dominio_referenciallegal on dominio_referenciallegal.code = lpal_linha_de_limite_l.referenciallegal
#
DROP VIEW IF EXISTS views.hid_ponto_inicio_drenagem_p#CREATE [VIEW] views.hid_ponto_inicio_drenagem_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom,
	dominio_nascente.code_name as nascente
    [FROM]
        pe.hid_ponto_inicio_drenagem_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ponto_inicio_drenagem_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = hid_ponto_inicio_drenagem_p.relacionado 
	left join dominios.booleano_estendido as dominio_nascente on dominio_nascente.code = hid_ponto_inicio_drenagem_p.nascente
#
DROP VIEW IF EXISTS views.hid_barragem_a#CREATE [VIEW] views.hid_barragem_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_barragem_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_barragem_a.id)),',' ) as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.hid_barragem_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_a.geometriaaproximada 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_a.usoprincipal 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_barragem_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_a.situacaofisica
#
DROP VIEW IF EXISTS views.tra_caminho_aereo_l#CREATE [VIEW] views.tra_caminho_aereo_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocaminhoaereo.code_name as tipocaminhoaereo,
	dominio_tipousocaminhoaer.code_name as tipousocaminhoaer,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        pe.tra_caminho_aereo_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_caminho_aereo_l.geometriaaproximada 
	left join dominios.tipo_caminho_aereo as dominio_tipocaminhoaereo on dominio_tipocaminhoaereo.code = tra_caminho_aereo_l.tipocaminhoaereo 
	left join dominios.tipo_transporte as dominio_tipousocaminhoaer on dominio_tipousocaminhoaer.code = tra_caminho_aereo_l.tipousocaminhoaer 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_caminho_aereo_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_caminho_aereo_l.situacaofisica
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_a#CREATE [VIEW] views.eco_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.eco_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.veg_brejo_pantano_a#CREATE [VIEW] views.veg_brejo_pantano_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_brejo_pantano_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_brejo_pantano_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_brejo_pantano_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_brejo_pantano_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_brejo_pantano_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_brejo_pantano_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_brejo_pantano_a.densidade
#
DROP VIEW IF EXISTS views.rel_elemento_fisiog_natural_p#CREATE [VIEW] views.rel_elemento_fisiog_natural_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_elemento_fisiog_natural_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_elemento_fisiog_natural_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_elemento_fisiog_natural_p.tipoelemnat
#
DROP VIEW IF EXISTS views.enc_torre_comunic_p#CREATE [VIEW] views.enc_torre_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_posicaoreledific.code_name as posicaoreledific,
	dominio_ovgd.code_name as ovgd,
	alturaestimada as alturaestimada,
	array_to_string( array(select code_name from dominios.modalidade dom join pe.enc_torre_comunic_p tn on (array[dom.code] <@ tn.modalidade and tn.id=pe.enc_torre_comunic_p.id)),',' ) as modalidade,
	id_complexo_comunicacao as id_complexo_comunicacao,
	geom as geom
    [FROM]
        pe.enc_torre_comunic_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_torre_comunic_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_torre_comunic_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_torre_comunic_p.situacaofisica 
	left join dominios.posicao_rel_edific as dominio_posicaoreledific on dominio_posicaoreledific.code = enc_torre_comunic_p.posicaoreledific 
	left join dominios.booleano_estendido as dominio_ovgd on dominio_ovgd.code = enc_torre_comunic_p.ovgd
#
DROP VIEW IF EXISTS views.rel_terreno_exposto_a#CREATE [VIEW] views.rel_terreno_exposto_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoterrexp.code_name as tipoterrexp,
	dominio_causaexposicao.code_name as causaexposicao,
	geom as geom
    [FROM]
        pe.rel_terreno_exposto_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_terreno_exposto_a.geometriaaproximada 
	left join dominios.tipo_terreno_exposto as dominio_tipoterrexp on dominio_tipoterrexp.code = rel_terreno_exposto_a.tipoterrexp 
	left join dominios.causa_exposicao as dominio_causaexposicao on dominio_causaexposicao.code = rel_terreno_exposto_a.causaexposicao
#
DROP VIEW IF EXISTS views.rel_terreno_erodido_a#CREATE [VIEW] views.rel_terreno_erodido_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_situacaoterreno.code_name as situacaoterreno,
	dominio_tipoerosao.code_name as tipoerosao,
	geom as geom
    [FROM]
        pe.rel_terreno_erodido_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_terreno_erodido_a.geometriaaproximada 
	left join dominios.situacao_terreno as dominio_situacaoterreno on dominio_situacaoterreno.code = rel_terreno_erodido_a.situacaoterreno 
	left join dominios.tipo_erosao as dominio_tipoerosao on dominio_tipoerosao.code = rel_terreno_erodido_a.tipoerosao
#
DROP VIEW IF EXISTS views.sb_cemiterio_a#CREATE [VIEW] views.sb_cemiterio_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocemiterio.code_name as tipocemiterio,
	dominio_denominacaoassociada.code_name as denominacaoassociada,
	dominio_destinacaocemiterio.code_name as destinacaocemiterio,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        pe.sb_cemiterio_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_cemiterio_a.geometriaaproximada 
	left join dominios.tipo_cemiterio as dominio_tipocemiterio on dominio_tipocemiterio.code = sb_cemiterio_a.tipocemiterio 
	left join dominios.denominacao_associada as dominio_denominacaoassociada on dominio_denominacaoassociada.code = sb_cemiterio_a.denominacaoassociada 
	left join dominios.destinacao_cemiterio as dominio_destinacaocemiterio on dominio_destinacaocemiterio.code = sb_cemiterio_a.destinacaocemiterio
#
DROP VIEW IF EXISTS views.aer_descontinuidade_geometrica_p#CREATE [VIEW] views.aer_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.aer_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aer_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_p#CREATE [VIEW] views.tra_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	geometriaaproximada as geometriaaproximada,
	motivodescontinuidade as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.tra_descontinuidade_geometrica_p
#
DROP VIEW IF EXISTS views.tra_trilha_picada_l#CREATE [VIEW] views.tra_trilha_picada_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.tra_trilha_picada_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_trilha_picada_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_ponto_cotado_altimetrico_p#CREATE [VIEW] views.rel_ponto_cotado_altimetrico_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_cotacomprovada.code_name as cotacomprovada,
	cota as cota,
	geom as geom
    [FROM]
        pe.rel_ponto_cotado_altimetrico_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_ponto_cotado_altimetrico_p.geometriaaproximada 
	left join dominios.booleano as dominio_cotacomprovada on dominio_cotacomprovada.code = rel_ponto_cotado_altimetrico_p.cotacomprovada
#
DROP VIEW IF EXISTS views.hid_confluencia_p#CREATE [VIEW] views.hid_confluencia_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        pe.hid_confluencia_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_confluencia_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = hid_confluencia_p.relacionado
#
DROP VIEW IF EXISTS views.dut_ramificacao_p#CREATE [VIEW] views.dut_ramificacao_p as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_duto as id_duto,
	dominio_relacionado.code_name as relacionado
    [FROM]
        pe.dut_ramificacao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_ramificacao_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = dut_ramificacao_p.relacionado
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_a#CREATE [VIEW] views.tra_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	geometriaaproximada as geometriaaproximada,
	motivodescontinuidade as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.tra_descontinuidade_geometrica_a
#
DROP VIEW IF EXISTS views.aer_descontinuidade_geometrica_a#CREATE [VIEW] views.aer_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.aer_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aer_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.enc_trecho_comunic_l#CREATE [VIEW] views.enc_trecho_comunic_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechocomunic.code_name as tipotrechocomunic,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_matconstr.code_name as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_emduto.code_name as emduto,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv,
	geom as geom
    [FROM]
        pe.enc_trecho_comunic_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_trecho_comunic_l.geometriaaproximada 
	left join dominios.tipo_trecho_comunic as dominio_tipotrechocomunic on dominio_tipotrechocomunic.code = enc_trecho_comunic_l.tipotrechocomunic 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = enc_trecho_comunic_l.posicaorelativa 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = enc_trecho_comunic_l.matconstr 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_trecho_comunic_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_trecho_comunic_l.situacaofisica 
	left join dominios.booleano as dominio_emduto on dominio_emduto.code = enc_trecho_comunic_l.emduto
#
DROP VIEW IF EXISTS views.hid_canal_vala_l#CREATE [VIEW] views.hid_canal_vala_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_canal_vala_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_canal_vala_l.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_usoprincipal.code_name as usoprincipal
    [FROM]
        pe.hid_canal_vala_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_canal_vala_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_canal_vala_l.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_canal_vala_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_canal_vala_l.situacaofisica 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_canal_vala_l.finalidade 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_canal_vala_l.usoprincipal
#
DROP VIEW IF EXISTS views.sb_dep_abast_agua_p#CREATE [VIEW] views.sb_dep_abast_agua_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.sb_dep_abast_agua_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.sb_dep_abast_agua_p.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_situacaoagua.code_name as situacaoagua,
	dominio_tratamento.code_name as tratamento,
	dominio_finalidadedep.code_name as finalidadedep,
	sigla as sigla,
	codequipdesenvsocial as codequipdesenvsocial,
	dominio_tipoequipdesenvsocial.code_name as tipoequipdesenvsocial,
	dominio_localizacaoequipdesenvsocial.code_name as localizacaoequipdesenvsocial,
	id_complexo_abast_agua as id_complexo_abast_agua,
	geom as geom
    [FROM]
        pe.sb_dep_abast_agua_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_dep_abast_agua_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_dep_abast_agua_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = sb_dep_abast_agua_p.situacaofisica 
	left join dominios.tipo_dep_geral as dominio_tipodepgeral on dominio_tipodepgeral.code = sb_dep_abast_agua_p.tipodepgeral 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = sb_dep_abast_agua_p.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = sb_dep_abast_agua_p.unidadevolume 
	left join dominios.situacao_agua as dominio_situacaoagua on dominio_situacaoagua.code = sb_dep_abast_agua_p.situacaoagua 
	left join dominios.booleano_estendido as dominio_tratamento on dominio_tratamento.code = sb_dep_abast_agua_p.tratamento 
	left join dominios.finalidade_deposito as dominio_finalidadedep on dominio_finalidadedep.code = sb_dep_abast_agua_p.finalidadedep 
	left join dominios.tipo_equip_desenv_social as dominio_tipoequipdesenvsocial on dominio_tipoequipdesenvsocial.code = sb_dep_abast_agua_p.tipoequipdesenvsocial 
	left join dominios.local_equip_desenv_social as dominio_localizacaoequipdesenvsocial on dominio_localizacaoequipdesenvsocial.code = sb_dep_abast_agua_p.localizacaoequipdesenvsocial
#
DROP VIEW IF EXISTS views.hid_banco_areia_a#CREATE [VIEW] views.hid_banco_areia_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipobanco.code_name as tipobanco,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_materialpredominante.code_name as materialpredominante,
	geom as geom
    [FROM]
        pe.hid_banco_areia_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_banco_areia_a.geometriaaproximada 
	left join dominios.tipo_banco as dominio_tipobanco on dominio_tipobanco.code = hid_banco_areia_a.tipobanco 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_banco_areia_a.situacaoemagua 
	left join dominios.material_predominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_banco_areia_a.materialpredominante
#
DROP VIEW IF EXISTS views.fer_descontinuidade_geometrica_p#CREATE [VIEW] views.fer_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.fer_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = fer_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.sb_descontinuidade_geometrica_p#CREATE [VIEW] views.sb_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.sb_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = sb_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_canal_vala_a#CREATE [VIEW] views.hid_canal_vala_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_usoprincipal.code_name as usoprincipal,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_canal_vala_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_canal_vala_a.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade
    [FROM]
        pe.hid_canal_vala_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_canal_vala_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_canal_vala_a.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_canal_vala_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_canal_vala_a.situacaofisica 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_canal_vala_a.usoprincipal 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_canal_vala_a.finalidade
#
DROP VIEW IF EXISTS views.sb_dep_saneamento_p#CREATE [VIEW] views.sb_dep_saneamento_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.sb_dep_saneamento_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.sb_dep_saneamento_p.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.sb_dep_saneamento_p tn on (array[dom.code] <@ tn.tipoprodutoresiduo and tn.id=pe.sb_dep_saneamento_p.id)),',' ) as tipoprodutoresiduo,
	array_to_string( array(select code_name from dominios.tipo_conteudo dom join pe.sb_dep_saneamento_p tn on (array[dom.code] <@ tn.tipoconteudo and tn.id=pe.sb_dep_saneamento_p.id)),',' ) as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_tratamento.code_name as tratamento,
	dominio_estadofisico.code_name as estadofisico,
	dominio_finalidadedep.code_name as finalidadedep,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        pe.sb_dep_saneamento_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_dep_saneamento_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_dep_saneamento_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = sb_dep_saneamento_p.situacaofisica 
	left join dominios.tipo_dep_geral as dominio_tipodepgeral on dominio_tipodepgeral.code = sb_dep_saneamento_p.tipodepgeral 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = sb_dep_saneamento_p.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = sb_dep_saneamento_p.unidadevolume 
	left join dominios.booleano_estendido as dominio_tratamento on dominio_tratamento.code = sb_dep_saneamento_p.tratamento 
	left join dominios.estado_fisico as dominio_estadofisico on dominio_estadofisico.code = sb_dep_saneamento_p.estadofisico 
	left join dominios.finalidade_deposito as dominio_finalidadedep on dominio_finalidadedep.code = sb_dep_saneamento_p.finalidadedep
#
DROP VIEW IF EXISTS views.hid_banco_areia_l#CREATE [VIEW] views.hid_banco_areia_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipobanco.code_name as tipobanco,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_materialpredominante.code_name as materialpredominante,
	geom as geom
    [FROM]
        pe.hid_banco_areia_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_banco_areia_l.geometriaaproximada 
	left join dominios.tipo_banco as dominio_tipobanco on dominio_tipobanco.code = hid_banco_areia_l.tipobanco 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_banco_areia_l.situacaoemagua 
	left join dominios.material_predominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_banco_areia_l.materialpredominante
#
DROP VIEW IF EXISTS views.hid_foz_maritima_p#CREATE [VIEW] views.hid_foz_maritima_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_foz_maritima_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.pto_pto_ref_geod_topo_p#CREATE [VIEW] views.pto_pto_ref_geod_topo_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	altitudegeometrica as altitudegeometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	outrarefplan as outrarefplan,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom,
	nome as nome,
	dominio_proximidade.code_name as proximidade,
	dominio_tipoptorefgeodtopo.code_name as tipoptorefgeodtopo,
	dominio_redereferencia.code_name as redereferencia,
	dominio_referencialgrav.code_name as referencialgrav,
	dominio_situacaomarco.code_name as situacaomarco,
	datavisita as datavisita,
	datamedicao as datamedicao
    [FROM]
        pe.pto_pto_ref_geod_topo_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_ref_geod_topo_p.geometriaaproximada 
	left join dominios.tipo_ref as dominio_tiporef on dominio_tiporef.code = pto_pto_ref_geod_topo_p.tiporef 
	left join dominios.sistema_geodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_ref_geod_topo_p.sistemageodesico 
	left join dominios.referencial_altim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_ref_geod_topo_p.referencialaltim 
	left join dominios.proximidade as dominio_proximidade on dominio_proximidade.code = pto_pto_ref_geod_topo_p.proximidade 
	left join dominios.tipo_pto_ref_geod_topo as dominio_tipoptorefgeodtopo on dominio_tipoptorefgeodtopo.code = pto_pto_ref_geod_topo_p.tipoptorefgeodtopo 
	left join dominios.rede_referencia as dominio_redereferencia on dominio_redereferencia.code = pto_pto_ref_geod_topo_p.redereferencia 
	left join dominios.referencial_grav as dominio_referencialgrav on dominio_referencialgrav.code = pto_pto_ref_geod_topo_p.referencialgrav 
	left join dominios.situacao_marco as dominio_situacaomarco on dominio_situacaomarco.code = pto_pto_ref_geod_topo_p.situacaomarco
#
DROP VIEW IF EXISTS views.hid_foz_maritima_l#CREATE [VIEW] views.hid_foz_maritima_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_foz_maritima_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.lpal_area_politico_adm_a#CREATE [VIEW] views.lpal_area_politico_adm_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.lpal_area_politico_adm_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_area_politico_adm_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.dut_galeria_l#CREATE [VIEW] views.dut_galeria_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	array_to_string( array(select code_name from dominios.mat_transp dom join pe.dut_galeria_l tn on (array[dom.code] <@ tn.mattransp and tn.id=pe.dut_galeria_l.id)),',' ) as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.dut_galeria_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.dut_galeria_l.id)),',' ) as matconstr,
	nrdutos as nrdutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom,
	dominio_finalidade.code_name as finalidade,
	pesosuportmaximo as pesosuportmaximo,
	id_via_ferrea as id_via_ferrea,
	largura as largura
    [FROM]
        pe.dut_galeria_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_galeria_l.geometriaaproximada 
	left join dominios.tipo_trecho_duto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = dut_galeria_l.tipotrechoduto 
	left join dominios.setor as dominio_setor on dominio_setor.code = dut_galeria_l.setor 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = dut_galeria_l.posicaorelativa 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = dut_galeria_l.situacaoespacial 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = dut_galeria_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = dut_galeria_l.situacaofisica 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = dut_galeria_l.finalidade
#
DROP VIEW IF EXISTS views.hid_trecho_massa_dagua_a#CREATE [VIEW] views.hid_trecho_massa_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipomassadagua.code_name as tipomassadagua,
	dominio_regime.code_name as regime,
	dominio_salgada.code_name as salgada,
	dominio_dominialidade.code_name as dominialidade,
	dominio_artificial.code_name as artificial,
	geom as geom,
	id_elemento_hidrografico as id_elemento_hidrografico,
	dominio_tipotrechomassadagua.code_name as tipotrechomassadagua,
	id_trecho_curso_dagua as id_trecho_curso_dagua
    [FROM]
        pe.hid_trecho_massa_dagua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_trecho_massa_dagua_a.geometriaaproximada 
	left join dominios.tipo_massa_dagua as dominio_tipomassadagua on dominio_tipomassadagua.code = hid_trecho_massa_dagua_a.tipomassadagua 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_trecho_massa_dagua_a.regime 
	left join dominios.booleano_estendido as dominio_salgada on dominio_salgada.code = hid_trecho_massa_dagua_a.salgada 
	left join dominios.jurisdicao as dominio_dominialidade on dominio_dominialidade.code = hid_trecho_massa_dagua_a.dominialidade 
	left join dominios.booleano_estendido as dominio_artificial on dominio_artificial.code = hid_trecho_massa_dagua_a.artificial 
	left join dominios.tipo_trecho_massa as dominio_tipotrechomassadagua on dominio_tipotrechomassadagua.code = hid_trecho_massa_dagua_a.tipotrechomassadagua
#
DROP VIEW IF EXISTS views.sb_descontinuidade_geometrica_a#CREATE [VIEW] views.sb_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.sb_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = sb_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.fer_descontinuidade_geometrica_l#CREATE [VIEW] views.fer_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.fer_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = fer_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.sb_descontinuidade_geometrica_l#CREATE [VIEW] views.sb_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.sb_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = sb_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.sb_dep_saneamento_a#CREATE [VIEW] views.sb_dep_saneamento_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.sb_dep_saneamento_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.sb_dep_saneamento_a.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.sb_dep_saneamento_a tn on (array[dom.code] <@ tn.tipoprodutoresiduo and tn.id=pe.sb_dep_saneamento_a.id)),',' ) as tipoprodutoresiduo,
	array_to_string( array(select code_name from dominios.tipo_conteudo dom join pe.sb_dep_saneamento_a tn on (array[dom.code] <@ tn.tipoconteudo and tn.id=pe.sb_dep_saneamento_a.id)),',' ) as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_tratamento.code_name as tratamento,
	dominio_estadofisico.code_name as estadofisico,
	dominio_finalidadedep.code_name as finalidadedep,
	id_complexo_saneamento as id_complexo_saneamento,
	geom as geom
    [FROM]
        pe.sb_dep_saneamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_dep_saneamento_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_dep_saneamento_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = sb_dep_saneamento_a.situacaofisica 
	left join dominios.tipo_dep_geral as dominio_tipodepgeral on dominio_tipodepgeral.code = sb_dep_saneamento_a.tipodepgeral 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = sb_dep_saneamento_a.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = sb_dep_saneamento_a.unidadevolume 
	left join dominios.booleano_estendido as dominio_tratamento on dominio_tratamento.code = sb_dep_saneamento_a.tratamento 
	left join dominios.estado_fisico as dominio_estadofisico on dominio_estadofisico.code = sb_dep_saneamento_a.estadofisico 
	left join dominios.finalidade_deposito as dominio_finalidadedep on dominio_finalidadedep.code = sb_dep_saneamento_a.finalidadedep
#
DROP VIEW IF EXISTS views.hid_foz_maritima_a#CREATE [VIEW] views.hid_foz_maritima_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_foz_maritima_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_foz_maritima_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.pto_pto_est_med_fenomenos_p#CREATE [VIEW] views.pto_pto_est_med_fenomenos_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoptoestmed.code_name as tipoptoestmed,
	codestacao as codestacao,
	id_est_med_fenomenos as id_est_med_fenomenos,
	geom as geom
    [FROM]
        pe.pto_pto_est_med_fenomenos_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_est_med_fenomenos_p.geometriaaproximada 
	left join dominios.tipo_pto_est_med as dominio_tipoptoestmed on dominio_tipoptoestmed.code = pto_pto_est_med_fenomenos_p.tipoptoestmed
#
DROP VIEW IF EXISTS views.hdv_obstaculo_navegacao_l#CREATE [VIEW] views.hdv_obstaculo_navegacao_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        pe.hdv_obstaculo_navegacao_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_obstaculo_navegacao_l.geometriaaproximada 
	left join dominios.tipo_obst as dominio_tipoobst on dominio_tipoobst.code = hdv_obstaculo_navegacao_l.tipoobst 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hdv_obstaculo_navegacao_l.situacaoemagua
#
DROP VIEW IF EXISTS views.hid_comporta_p#CREATE [VIEW] views.hid_comporta_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hid_comporta_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_comporta_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_comporta_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_comporta_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_corredeira_p#CREATE [VIEW] views.hid_corredeira_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_corredeira_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.veg_campo_a#CREATE [VIEW] views.veg_campo_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade,
	dominio_tipocampo.code_name as tipocampo
    [FROM]
        pe.veg_campo_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_campo_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_campo_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_campo_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_campo_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_campo_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_campo_a.densidade 
	left join dominios.tipo_campo as dominio_tipocampo on dominio_tipocampo.code = veg_campo_a.tipocampo
#
DROP VIEW IF EXISTS views.veg_descontinuidade_geometrica_p#CREATE [VIEW] views.veg_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.veg_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = veg_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_corte_p#CREATE [VIEW] views.rel_corte_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_corte_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_corte_p.id)),',' ) as matconstr
    [FROM]
        pe.rel_corte_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_corte_p.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_corte_p.tipoalterantrop
#
DROP VIEW IF EXISTS views.tra_ponte_p#CREATE [VIEW] views.tra_ponte_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_ponte_p tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_ponte_p.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_ponte_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_ponte_p.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipoponte.code_name as tipoponte,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        pe.tra_ponte_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponte_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_ponte_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_ponte_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_ponte_p.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_ponte_p.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_ponte_p.tipopavimentacao 
	left join dominios.tipo_ponte as dominio_tipoponte on dominio_tipoponte.code = tra_ponte_p.tipoponte
#
DROP VIEW IF EXISTS views.hdv_obstaculo_navegacao_a#CREATE [VIEW] views.hdv_obstaculo_navegacao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        pe.hdv_obstaculo_navegacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_obstaculo_navegacao_a.geometriaaproximada 
	left join dominios.tipo_obst as dominio_tipoobst on dominio_tipoobst.code = hdv_obstaculo_navegacao_a.tipoobst 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hdv_obstaculo_navegacao_a.situacaoemagua
#
DROP VIEW IF EXISTS views.dut_trecho_duto_l#CREATE [VIEW] views.dut_trecho_duto_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	array_to_string( array(select code_name from dominios.mat_transp dom join pe.dut_trecho_duto_l tn on (array[dom.code] <@ tn.mattransp and tn.id=pe.dut_trecho_duto_l.id)),',' ) as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.dut_trecho_duto_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.dut_trecho_duto_l.id)),',' ) as matconstr,
	nrdutos as nrdutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom
    [FROM]
        pe.dut_trecho_duto_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_trecho_duto_l.geometriaaproximada 
	left join dominios.tipo_trecho_duto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = dut_trecho_duto_l.tipotrechoduto 
	left join dominios.setor as dominio_setor on dominio_setor.code = dut_trecho_duto_l.setor 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = dut_trecho_duto_l.posicaorelativa 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = dut_trecho_duto_l.situacaoespacial 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = dut_trecho_duto_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = dut_trecho_duto_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_corredeira_a#CREATE [VIEW] views.hid_corredeira_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_corredeira_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_queda_dagua_p#CREATE [VIEW] views.hid_queda_dagua_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        pe.hid_queda_dagua_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_p.geometriaaproximada 
	left join dominios.tipo_queda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_p.tipoqueda
#
DROP VIEW IF EXISTS views.rel_corte_a#CREATE [VIEW] views.rel_corte_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_corte_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_corte_a.id)),',' ) as matconstr
    [FROM]
        pe.rel_corte_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_corte_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_corte_a.tipoalterantrop
#
DROP VIEW IF EXISTS views.hid_fonte_dagua_p#CREATE [VIEW] views.hid_fonte_dagua_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipofontedagua.code_name as tipofontedagua,
	dominio_qualidagua.code_name as qualidagua,
	dominio_regime.code_name as regime,
	geom as geom
    [FROM]
        pe.hid_fonte_dagua_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_fonte_dagua_p.geometriaaproximada 
	left join dominios.tipo_fonte_dagua as dominio_tipofontedagua on dominio_tipofontedagua.code = hid_fonte_dagua_p.tipofontedagua 
	left join dominios.qualid_agua as dominio_qualidagua on dominio_qualidagua.code = hid_fonte_dagua_p.qualidagua 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_fonte_dagua_p.regime
#
DROP VIEW IF EXISTS views.tra_entroncamento_pto_p#CREATE [VIEW] views.tra_entroncamento_pto_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoentroncamento.code_name as tipoentroncamento,
	geom as geom,
	id_entroncamento as id_entroncamento
    [FROM]
        pe.tra_entroncamento_pto_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_entroncamento_pto_p.geometriaaproximada 
	left join dominios.tipo_entroncamento as dominio_tipoentroncamento on dominio_tipoentroncamento.code = tra_entroncamento_pto_p.tipoentroncamento
#
DROP VIEW IF EXISTS views.veg_descontinuidade_geometrica_l#CREATE [VIEW] views.veg_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.veg_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = veg_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_corte_l#CREATE [VIEW] views.rel_corte_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_corte_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_corte_l.id)),',' ) as matconstr
    [FROM]
        pe.rel_corte_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_corte_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_corte_l.tipoalterantrop
#
DROP VIEW IF EXISTS views.hdv_obstaculo_navegacao_p#CREATE [VIEW] views.hdv_obstaculo_navegacao_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoobst.code_name as tipoobst,
	dominio_situacaoemagua.code_name as situacaoemagua,
	geom as geom
    [FROM]
        pe.hdv_obstaculo_navegacao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_obstaculo_navegacao_p.geometriaaproximada 
	left join dominios.tipo_obst as dominio_tipoobst on dominio_tipoobst.code = hdv_obstaculo_navegacao_p.tipoobst 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hdv_obstaculo_navegacao_p.situacaoemagua
#
DROP VIEW IF EXISTS views.hid_comporta_l#CREATE [VIEW] views.hid_comporta_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hid_comporta_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_comporta_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_comporta_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_comporta_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_corredeira_l#CREATE [VIEW] views.hid_corredeira_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.hid_corredeira_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_corredeira_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.hdv_atracadouro_terminal_p#CREATE [VIEW] views.hdv_atracadouro_terminal_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_atracadouro_terminal_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_atracadouro_terminal_p.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.aptidao_operacional_atracadouro dom join pe.hdv_atracadouro_terminal_p tn on (array[dom.code] <@ tn.aptidaooperacional and tn.id=pe.hdv_atracadouro_terminal_p.id)),',' ) as aptidaooperacional,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        pe.hdv_atracadouro_terminal_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_atracadouro_terminal_p.geometriaaproximada 
	left join dominios.tipo_atracad as dominio_tipoatracad on dominio_tipoatracad.code = hdv_atracadouro_terminal_p.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_atracadouro_terminal_p.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_atracadouro_terminal_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_atracadouro_terminal_p.situacaofisica
#
DROP VIEW IF EXISTS views.lpal_descontinuidade_geometrica_l#CREATE [VIEW] views.lpal_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.lpal_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = lpal_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hdv_descontinuidade_geometrica_a#CREATE [VIEW] views.hdv_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.hdv_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hdv_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lpal_descontinuidade_geometrica_a#CREATE [VIEW] views.lpal_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.lpal_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = lpal_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_travessia_pedestre_l#CREATE [VIEW] views.tra_travessia_pedestre_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_tipotravessiaped.code_name as tipotravessiaped,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        pe.tra_travessia_pedestre_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_pedestre_l.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = tra_travessia_pedestre_l.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_travessia_pedestre_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_travessia_pedestre_l.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = tra_travessia_pedestre_l.situacaoespacial 
	left join dominios.tipo_travessia_ped as dominio_tipotravessiaped on dominio_tipotravessiaped.code = tra_travessia_pedestre_l.tipotravessiaped
#
DROP VIEW IF EXISTS views.hid_trecho_drenagem_l#CREATE [VIEW] views.hid_trecho_drenagem_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechodrenagem.code_name as tipotrechodrenagem,
	dominio_navegavel.code_name as navegavel,
	larguramedia as larguramedia,
	dominio_regime.code_name as regime,
	dominio_encoberto.code_name as encoberto,
	geom as geom,
	id_trecho_curso_dagua as id_trecho_curso_dagua
    [FROM]
        pe.hid_trecho_drenagem_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_trecho_drenagem_l.geometriaaproximada 
	left join dominios.tipo_trecho_drenagem as dominio_tipotrechodrenagem on dominio_tipotrechodrenagem.code = hid_trecho_drenagem_l.tipotrechodrenagem 
	left join dominios.booleano_estendido as dominio_navegavel on dominio_navegavel.code = hid_trecho_drenagem_l.navegavel 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_trecho_drenagem_l.regime 
	left join dominios.booleano as dominio_encoberto on dominio_encoberto.code = hid_trecho_drenagem_l.encoberto
#
DROP VIEW IF EXISTS views.lpal_posic_geo_localidade_p#CREATE [VIEW] views.lpal_posic_geo_localidade_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolocalidade.code_name as tipolocalidade,
	identificador as identificador,
	latitude as latitude,
	latitudegms as latitudegms,
	longitude as longitude,
	longitudegms as longitudegms,
	id_localidade as id_localidade,
	geom as geom
    [FROM]
        pe.lpal_posic_geo_localidade_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_posic_geo_localidade_p.geometriaaproximada 
	left join dominios.tipo_localidade as dominio_tipolocalidade on dominio_tipolocalidade.code = lpal_posic_geo_localidade_p.tipolocalidade
#
DROP VIEW IF EXISTS views.rod_ponto_rodoviario_p#CREATE [VIEW] views.rod_ponto_rodoviario_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        pe.rod_ponto_rodoviario_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_ponto_rodoviario_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = rod_ponto_rodoviario_p.relacionado
#
DROP VIEW IF EXISTS views.hdv_atracadouro_terminal_a#CREATE [VIEW] views.hdv_atracadouro_terminal_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_atracadouro_terminal_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_atracadouro_terminal_a.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.aptidao_operacional_atracadouro dom join pe.hdv_atracadouro_terminal_a tn on (array[dom.code] <@ tn.aptidaooperacional and tn.id=pe.hdv_atracadouro_terminal_a.id)),',' ) as aptidaooperacional,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        pe.hdv_atracadouro_terminal_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_atracadouro_terminal_a.geometriaaproximada 
	left join dominios.tipo_atracad as dominio_tipoatracad on dominio_tipoatracad.code = hdv_atracadouro_terminal_a.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_atracadouro_terminal_a.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_atracadouro_terminal_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_atracadouro_terminal_a.situacaofisica
#
DROP VIEW IF EXISTS views.hdv_descontinuidade_geometrica_p#CREATE [VIEW] views.hdv_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.hdv_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hdv_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lpal_distrito_a#CREATE [VIEW] views.lpal_distrito_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	geocodigo as geocodigo,
	anodereferencia as anodereferencia
    [FROM]
        pe.lpal_distrito_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_distrito_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lpal_descontinuidade_geometrica_p#CREATE [VIEW] views.lpal_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.lpal_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = lpal_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.fer_descontinuidade_geometrica_a#CREATE [VIEW] views.fer_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.fer_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = fer_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lpal_limite_area_especial_l#CREATE [VIEW] views.lpal_limite_area_especial_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_referenciallegal.code_name as referenciallegal,
	obssituacao as obssituacao,
	extensao as extensao,
	geom as geom,
	dominio_tipolimareaesp.code_name as tipolimareaesp
    [FROM]
        pe.lpal_limite_area_especial_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_limite_area_especial_l.geometriaaproximada 
	left join dominios.referencial_legal as dominio_referenciallegal on dominio_referenciallegal.code = lpal_limite_area_especial_l.referenciallegal 
	left join dominios.tipo_lim_area_esp as dominio_tipolimareaesp on dominio_tipolimareaesp.code = lpal_limite_area_especial_l.tipolimareaesp
#
DROP VIEW IF EXISTS views.hid_massa_dagua_a#CREATE [VIEW] views.hid_massa_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipomassadagua.code_name as tipomassadagua,
	dominio_regime.code_name as regime,
	dominio_salgada.code_name as salgada,
	dominio_dominialidade.code_name as dominialidade,
	dominio_artificial.code_name as artificial,
	geom as geom,
	id_elemento_hidrografico as id_elemento_hidrografico
    [FROM]
        pe.hid_massa_dagua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_massa_dagua_a.geometriaaproximada 
	left join dominios.tipo_massa_dagua as dominio_tipomassadagua on dominio_tipomassadagua.code = hid_massa_dagua_a.tipomassadagua 
	left join dominios.regime as dominio_regime on dominio_regime.code = hid_massa_dagua_a.regime 
	left join dominios.booleano_estendido as dominio_salgada on dominio_salgada.code = hid_massa_dagua_a.salgada 
	left join dominios.jurisdicao as dominio_dominialidade on dominio_dominialidade.code = hid_massa_dagua_a.dominialidade 
	left join dominios.booleano_estendido as dominio_artificial on dominio_artificial.code = hid_massa_dagua_a.artificial
#
DROP VIEW IF EXISTS views.hdv_atracadouro_terminal_l#CREATE [VIEW] views.hdv_atracadouro_terminal_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoatracad.code_name as tipoatracad,
	dominio_administracao.code_name as administracao,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hdv_atracadouro_terminal_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hdv_atracadouro_terminal_l.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.aptidao_operacional_atracadouro dom join pe.hdv_atracadouro_terminal_l tn on (array[dom.code] <@ tn.aptidaooperacional and tn.id=pe.hdv_atracadouro_terminal_l.id)),',' ) as aptidaooperacional,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        pe.hdv_atracadouro_terminal_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_atracadouro_terminal_l.geometriaaproximada 
	left join dominios.tipo_atracad as dominio_tipoatracad on dominio_tipoatracad.code = hdv_atracadouro_terminal_l.tipoatracad 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_atracadouro_terminal_l.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_atracadouro_terminal_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_atracadouro_terminal_l.situacaofisica
#
DROP VIEW IF EXISTS views.veg_veg_restinga_a#CREATE [VIEW] views.veg_veg_restinga_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_veg_restinga_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_restinga_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_veg_restinga_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_restinga_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_veg_restinga_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_veg_restinga_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_veg_restinga_a.densidade
#
DROP VIEW IF EXISTS views.eco_ext_mineral_l#CREATE [VIEW] views.eco_ext_mineral_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_secaoativecon.code_name as secaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoextmin.code_name as tipoextmin,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.eco_ext_mineral_l tn on (array[dom.code] <@ tn.tipoproduto and tn.id=pe.eco_ext_mineral_l.id)),',' ) as tipoproduto,
	dominio_tipopocomina.code_name as tipopocomina,
	dominio_procextracao.code_name as procextracao,
	dominio_formaextracao.code_name as formaextracao,
	dominio_atividade.code_name as atividade,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        pe.eco_ext_mineral_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_ext_mineral_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = eco_ext_mineral_l.tipoalterantrop 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = eco_ext_mineral_l.secaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_ext_mineral_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_ext_mineral_l.situacaofisica 
	left join dominios.tipo_ext_min as dominio_tipoextmin on dominio_tipoextmin.code = eco_ext_mineral_l.tipoextmin 
	left join dominios.tipo_poco_mina as dominio_tipopocomina on dominio_tipopocomina.code = eco_ext_mineral_l.tipopocomina 
	left join dominios.proc_extracao as dominio_procextracao on dominio_procextracao.code = eco_ext_mineral_l.procextracao 
	left join dominios.forma_extracao as dominio_formaextracao on dominio_formaextracao.code = eco_ext_mineral_l.formaextracao 
	left join dominios.atividade as dominio_atividade on dominio_atividade.code = eco_ext_mineral_l.atividade
#
DROP VIEW IF EXISTS views.aer_pista_ponto_pouso_a#CREATE [VIEW] views.aer_pista_ponto_pouso_a as 
	SELECT
	id as id,
	nome as nome,
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
        pe.aer_pista_ponto_pouso_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_pista_ponto_pouso_a.geometriaaproximada 
	left join dominios.tipo_pista as dominio_tipopista on dominio_tipopista.code = aer_pista_ponto_pouso_a.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = aer_pista_ponto_pouso_a.revestimento 
	left join dominios.uso_pista as dominio_usopista on dominio_usopista.code = aer_pista_ponto_pouso_a.usopista 
	left join dominios.booleano_estendido as dominio_homologacao on dominio_homologacao.code = aer_pista_ponto_pouso_a.homologacao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = aer_pista_ponto_pouso_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = aer_pista_ponto_pouso_a.situacaofisica
#
DROP VIEW IF EXISTS views.aer_pista_ponto_pouso_l#CREATE [VIEW] views.aer_pista_ponto_pouso_l as 
	SELECT
	id as id,
	nome as nome,
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
        pe.aer_pista_ponto_pouso_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_pista_ponto_pouso_l.geometriaaproximada 
	left join dominios.tipo_pista as dominio_tipopista on dominio_tipopista.code = aer_pista_ponto_pouso_l.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = aer_pista_ponto_pouso_l.revestimento 
	left join dominios.uso_pista as dominio_usopista on dominio_usopista.code = aer_pista_ponto_pouso_l.usopista 
	left join dominios.booleano_estendido as dominio_homologacao on dominio_homologacao.code = aer_pista_ponto_pouso_l.homologacao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = aer_pista_ponto_pouso_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = aer_pista_ponto_pouso_l.situacaofisica
#
DROP VIEW IF EXISTS views.eco_ext_mineral_a#CREATE [VIEW] views.eco_ext_mineral_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_secaoativecon.code_name as secaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoextmin.code_name as tipoextmin,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.eco_ext_mineral_a tn on (array[dom.code] <@ tn.tipoproduto and tn.id=pe.eco_ext_mineral_a.id)),',' ) as tipoproduto,
	dominio_tipopocomina.code_name as tipopocomina,
	dominio_procextracao.code_name as procextracao,
	dominio_formaextracao.code_name as formaextracao,
	dominio_atividade.code_name as atividade,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        pe.eco_ext_mineral_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_ext_mineral_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = eco_ext_mineral_a.tipoalterantrop 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = eco_ext_mineral_a.secaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_ext_mineral_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_ext_mineral_a.situacaofisica 
	left join dominios.tipo_ext_min as dominio_tipoextmin on dominio_tipoextmin.code = eco_ext_mineral_a.tipoextmin 
	left join dominios.tipo_poco_mina as dominio_tipopocomina on dominio_tipopocomina.code = eco_ext_mineral_a.tipopocomina 
	left join dominios.proc_extracao as dominio_procextracao on dominio_procextracao.code = eco_ext_mineral_a.procextracao 
	left join dominios.forma_extracao as dominio_formaextracao on dominio_formaextracao.code = eco_ext_mineral_a.formaextracao 
	left join dominios.atividade as dominio_atividade on dominio_atividade.code = eco_ext_mineral_a.atividade
#
DROP VIEW IF EXISTS views.enc_zona_linhas_energia_com_a#CREATE [VIEW] views.enc_zona_linhas_energia_com_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.enc_zona_linhas_energia_com_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_zona_linhas_energia_com_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lpal_area_construida_a#CREATE [VIEW] views.lpal_area_construida_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_localidade as id_localidade,
	geom as geom
    [FROM]
        pe.lpal_area_construida_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_area_construida_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.aer_pista_ponto_pouso_p#CREATE [VIEW] views.aer_pista_ponto_pouso_p as 
	SELECT
	id as id,
	nome as nome,
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
        pe.aer_pista_ponto_pouso_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_pista_ponto_pouso_p.geometriaaproximada 
	left join dominios.tipo_pista as dominio_tipopista on dominio_tipopista.code = aer_pista_ponto_pouso_p.tipopista 
	left join dominios.revestimento as dominio_revestimento on dominio_revestimento.code = aer_pista_ponto_pouso_p.revestimento 
	left join dominios.uso_pista as dominio_usopista on dominio_usopista.code = aer_pista_ponto_pouso_p.usopista 
	left join dominios.booleano_estendido as dominio_homologacao on dominio_homologacao.code = aer_pista_ponto_pouso_p.homologacao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = aer_pista_ponto_pouso_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = aer_pista_ponto_pouso_p.situacaofisica
#
DROP VIEW IF EXISTS views.rel_rocha_a#CREATE [VIEW] views.rel_rocha_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_formarocha.code_name as formarocha
    [FROM]
        pe.rel_rocha_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_rocha_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_rocha_a.tipoelemnat 
	left join dominios.forma_rocha as dominio_formarocha on dominio_formarocha.code = rel_rocha_a.formarocha
#
DROP VIEW IF EXISTS views.tra_travessia_p#CREATE [VIEW] views.tra_travessia_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessia.code_name as tipotravessia,
	dominio_tipouso.code_name as tipouso,
	dominio_tipoembarcacao.code_name as tipoembarcacao,
	geom as geom
    [FROM]
        pe.tra_travessia_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_p.geometriaaproximada 
	left join dominios.tipo_travessia as dominio_tipotravessia on dominio_tipotravessia.code = tra_travessia_p.tipotravessia 
	left join dominios.tipo_transporte as dominio_tipouso on dominio_tipouso.code = tra_travessia_p.tipouso 
	left join dominios.tipo_embarcacao as dominio_tipoembarcacao on dominio_tipoembarcacao.code = tra_travessia_p.tipoembarcacao
#
DROP VIEW IF EXISTS views.hid_area_umida_a#CREATE [VIEW] views.hid_area_umida_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoareaumida.code_name as tipoareaumida,
	geom as geom
    [FROM]
        pe.hid_area_umida_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_area_umida_a.geometriaaproximada 
	left join dominios.tipo_area_umida as dominio_tipoareaumida on dominio_tipoareaumida.code = hid_area_umida_a.tipoareaumida
#
DROP VIEW IF EXISTS views.rel_duna_p#CREATE [VIEW] views.rel_duna_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_fixa.code_name as fixa
    [FROM]
        pe.rel_duna_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_duna_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_duna_p.tipoelemnat 
	left join dominios.booleano as dominio_fixa on dominio_fixa.code = rel_duna_p.fixa
#
DROP VIEW IF EXISTS views.fer_ponto_ferroviario_p#CREATE [VIEW] views.fer_ponto_ferroviario_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        pe.fer_ponto_ferroviario_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_ponto_ferroviario_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = fer_ponto_ferroviario_p.relacionado
#
DROP VIEW IF EXISTS views.tra_passagem_elevada_viaduto_p#CREATE [VIEW] views.tra_passagem_elevada_viaduto_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_passagem_elevada_viaduto_p tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_passagem_elevada_viaduto_p.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_passagem_elevada_viaduto_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_passagem_elevada_viaduto_p.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipopassagviad.code_name as tipopassagviad,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	gabhorizsup as gabhorizsup,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        pe.tra_passagem_elevada_viaduto_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_passagem_elevada_viaduto_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_passagem_elevada_viaduto_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_passagem_elevada_viaduto_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_passagem_elevada_viaduto_p.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_passagem_elevada_viaduto_p.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_passagem_elevada_viaduto_p.tipopavimentacao 
	left join dominios.tipo_passag_viad as dominio_tipopassagviad on dominio_tipopassagviad.code = tra_passagem_elevada_viaduto_p.tipopassagviad
#
DROP VIEW IF EXISTS views.lpal_nome_local_p#CREATE [VIEW] views.lpal_nome_local_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.lpal_nome_local_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_nome_local_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.eco_plataforma_p#CREATE [VIEW] views.eco_plataforma_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoplataforma.code_name as tipoplataforma,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        pe.eco_plataforma_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_plataforma_p.geometriaaproximada 
	left join dominios.tipo_plataforma as dominio_tipoplataforma on dominio_tipoplataforma.code = eco_plataforma_p.tipoplataforma
#
DROP VIEW IF EXISTS views.fer_trecho_ferroviario_l#CREATE [VIEW] views.fer_trecho_ferroviario_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codtrechoferrov as codtrechoferrov,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_tipotrechoferrov.code_name as tipotrechoferrov,
	dominio_bitola.code_name as bitola,
	dominio_eletrificada.code_name as eletrificada,
	dominio_nrlinhas.code_name as nrlinhas,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_administracao.code_name as administracao,
	concessionaria as concessionaria,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	cargasuportmaxima as cargasuportmaxima,
	id_via_ferrea as id_via_ferrea,
	geom as geom
    [FROM]
        pe.fer_trecho_ferroviario_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_trecho_ferroviario_l.geometriaaproximada 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = fer_trecho_ferroviario_l.posicaorelativa 
	left join dominios.tipo_trecho_ferrov as dominio_tipotrechoferrov on dominio_tipotrechoferrov.code = fer_trecho_ferroviario_l.tipotrechoferrov 
	left join dominios.bitola as dominio_bitola on dominio_bitola.code = fer_trecho_ferroviario_l.bitola 
	left join dominios.booleano_estendido as dominio_eletrificada on dominio_eletrificada.code = fer_trecho_ferroviario_l.eletrificada 
	left join dominios.nr_linhas as dominio_nrlinhas on dominio_nrlinhas.code = fer_trecho_ferroviario_l.nrlinhas 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = fer_trecho_ferroviario_l.jurisdicao 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = fer_trecho_ferroviario_l.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_trecho_ferroviario_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_trecho_ferroviario_l.situacaofisica
#
DROP VIEW IF EXISTS views.enc_termeletrica_p#CREATE [VIEW] views.enc_termeletrica_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom,
	dominio_tipocombustivel.code_name as tipocombustivel
    [FROM]
        pe.enc_termeletrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_termeletrica_p.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_termeletrica_p.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_termeletrica_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_termeletrica_p.situacaofisica 
	left join dominios.tipo_combustivel as dominio_tipocombustivel on dominio_tipocombustivel.code = enc_termeletrica_p.tipocombustivel
#
DROP VIEW IF EXISTS views.enc_torre_energia_p#CREATE [VIEW] views.enc_torre_energia_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_ovgd.code_name as ovgd,
	alturaestimada as alturaestimada,
	geom as geom
    [FROM]
        pe.enc_torre_energia_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_torre_energia_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_torre_energia_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_torre_energia_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_ovgd on dominio_ovgd.code = enc_torre_energia_p.ovgd
#
DROP VIEW IF EXISTS views.lpal_unidade_conservacao_nao_snuc_a#CREATE [VIEW] views.lpal_unidade_conservacao_nao_snuc_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_conservacao_nao_snuc_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_conservacao_nao_snuc_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_conservacao_nao_snuc_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_conservacao_nao_snuc_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_conservacao_nao_snuc_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.enc_hidreletrica_l#CREATE [VIEW] views.enc_hidreletrica_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_hidreletrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_l.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_l.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_hidreletrica_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_descontinuidade_geometrica_p#CREATE [VIEW] views.hid_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.hid_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hid_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_patio_p#CREATE [VIEW] views.tra_patio_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_patio_p tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_patio_p.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.administracao dom join pe.tra_patio_p tn on (array[dom.code] <@ tn.administracao and tn.id=pe.tra_patio_p.id)),',' ) as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.finalidade_patio dom join pe.tra_patio_p tn on (array[dom.code] <@ tn.finalidadepatio and tn.id=pe.tra_patio_p.id)),',' ) as finalidadepatio,
	id_estrut_transporte as id_estrut_transporte,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_industrial as id_org_industrial,
	id_org_ensino as id_org_ensino,
	geom as geom
    [FROM]
        pe.tra_patio_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_patio_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_patio_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_patio_p.situacaofisica
#
DROP VIEW IF EXISTS views.enc_hidreletrica_a#CREATE [VIEW] views.enc_hidreletrica_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_hidreletrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_a.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_a.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_hidreletrica_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_a.situacaofisica
#
DROP VIEW IF EXISTS views.rel_dolina_a#CREATE [VIEW] views.rel_dolina_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_dolina_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_dolina_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_dolina_a.tipoelemnat
#
DROP VIEW IF EXISTS views.eco_deposito_geral_a#CREATE [VIEW] views.eco_deposito_geral_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.tipo_dep_geral dom join pe.eco_deposito_geral_a tn on (array[dom.code] <@ tn.tipodepgeral and tn.id=pe.eco_deposito_geral_a.id)),',' ) as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.eco_deposito_geral_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.eco_deposito_geral_a.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.eco_deposito_geral_a tn on (array[dom.code] <@ tn.tipoprodutoresiduo and tn.id=pe.eco_deposito_geral_a.id)),',' ) as tipoprodutoresiduo,
	array_to_string( array(select code_name from dominios.tipo_conteudo dom join pe.eco_deposito_geral_a tn on (array[dom.code] <@ tn.tipoconteudo and tn.id=pe.eco_deposito_geral_a.id)),',' ) as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	id_estrut_transporte as id_estrut_transporte,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        pe.eco_deposito_geral_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_deposito_geral_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_deposito_geral_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_deposito_geral_a.situacaofisica 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = eco_deposito_geral_a.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = eco_deposito_geral_a.unidadevolume
#
DROP VIEW IF EXISTS views.lpal_unidade_federacao_a#CREATE [VIEW] views.lpal_unidade_federacao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	dominio_sigla.code_name as sigla,
	geocodigo as geocodigo
    [FROM]
        pe.lpal_unidade_federacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_federacao_a.geometriaaproximada 
	left join dominios.sigla_uf as dominio_sigla on dominio_sigla.code = lpal_unidade_federacao_a.sigla
#
DROP VIEW IF EXISTS views.sb_dep_abast_agua_a#CREATE [VIEW] views.sb_dep_abast_agua_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipodepgeral.code_name as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.sb_dep_abast_agua_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.sb_dep_abast_agua_a.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	dominio_situacaoagua.code_name as situacaoagua,
	dominio_tratamento.code_name as tratamento,
	dominio_finalidadedep.code_name as finalidadedep,
	sigla as sigla,
	codequipdesenvsocial as codequipdesenvsocial,
	dominio_tipoequipdesenvsocial.code_name as tipoequipdesenvsocial,
	dominio_localizacaoequipdesenvsocial.code_name as localizacaoequipdesenvsocial,
	id_complexo_abast_agua as id_complexo_abast_agua,
	geom as geom
    [FROM]
        pe.sb_dep_abast_agua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_dep_abast_agua_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = sb_dep_abast_agua_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = sb_dep_abast_agua_a.situacaofisica 
	left join dominios.tipo_dep_geral as dominio_tipodepgeral on dominio_tipodepgeral.code = sb_dep_abast_agua_a.tipodepgeral 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = sb_dep_abast_agua_a.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = sb_dep_abast_agua_a.unidadevolume 
	left join dominios.situacao_agua as dominio_situacaoagua on dominio_situacaoagua.code = sb_dep_abast_agua_a.situacaoagua 
	left join dominios.booleano_estendido as dominio_tratamento on dominio_tratamento.code = sb_dep_abast_agua_a.tratamento 
	left join dominios.finalidade_deposito as dominio_finalidadedep on dominio_finalidadedep.code = sb_dep_abast_agua_a.finalidadedep 
	left join dominios.tipo_equip_desenv_social as dominio_tipoequipdesenvsocial on dominio_tipoequipdesenvsocial.code = sb_dep_abast_agua_a.tipoequipdesenvsocial 
	left join dominios.local_equip_desenv_social as dominio_localizacaoequipdesenvsocial on dominio_localizacaoequipdesenvsocial.code = sb_dep_abast_agua_a.localizacaoequipdesenvsocial
#
DROP VIEW IF EXISTS views.tra_patio_a#CREATE [VIEW] views.tra_patio_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_patio_a tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_patio_a.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.administracao dom join pe.tra_patio_a tn on (array[dom.code] <@ tn.administracao and tn.id=pe.tra_patio_a.id)),',' ) as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.finalidade_patio dom join pe.tra_patio_a tn on (array[dom.code] <@ tn.finalidadepatio and tn.id=pe.tra_patio_a.id)),',' ) as finalidadepatio,
	id_estrut_transporte as id_estrut_transporte,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_industrial as id_org_industrial,
	id_org_ensino as id_org_ensino,
	geom as geom
    [FROM]
        pe.tra_patio_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_patio_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_patio_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_patio_a.situacaofisica
#
DROP VIEW IF EXISTS views.enc_hidreletrica_p#CREATE [VIEW] views.enc_hidreletrica_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_hidreletrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_hidreletrica_p.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_hidreletrica_p.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_hidreletrica_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_hidreletrica_p.situacaofisica
#
DROP VIEW IF EXISTS views.hid_descontinuidade_geometrica_l#CREATE [VIEW] views.hid_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.hid_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hid_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_dolina_p#CREATE [VIEW] views.rel_dolina_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_dolina_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_dolina_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_dolina_p.tipoelemnat
#
DROP VIEW IF EXISTS views.eco_deposito_geral_p#CREATE [VIEW] views.eco_deposito_geral_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.tipo_dep_geral dom join pe.eco_deposito_geral_p tn on (array[dom.code] <@ tn.tipodepgeral and tn.id=pe.eco_deposito_geral_p.id)),',' ) as tipodepgeral,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.eco_deposito_geral_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.eco_deposito_geral_p.id)),',' ) as matconstr,
	dominio_tipoexposicao.code_name as tipoexposicao,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.eco_deposito_geral_p tn on (array[dom.code] <@ tn.tipoprodutoresiduo and tn.id=pe.eco_deposito_geral_p.id)),',' ) as tipoprodutoresiduo,
	array_to_string( array(select code_name from dominios.tipo_conteudo dom join pe.eco_deposito_geral_p tn on (array[dom.code] <@ tn.tipoconteudo and tn.id=pe.eco_deposito_geral_p.id)),',' ) as tipoconteudo,
	dominio_unidadevolume.code_name as unidadevolume,
	valorvolume as valorvolume,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_ext_mineral as id_org_ext_mineral,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	id_estrut_transporte as id_estrut_transporte,
	id_org_industrial as id_org_industrial,
	geom as geom
    [FROM]
        pe.eco_deposito_geral_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_deposito_geral_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_deposito_geral_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_deposito_geral_p.situacaofisica 
	left join dominios.tipo_exposicao as dominio_tipoexposicao on dominio_tipoexposicao.code = eco_deposito_geral_p.tipoexposicao 
	left join dominios.unidade_volume as dominio_unidadevolume on dominio_unidadevolume.code = eco_deposito_geral_p.unidadevolume
#
DROP VIEW IF EXISTS views.pto_marco_de_limite_p#CREATE [VIEW] views.pto_marco_de_limite_p as 
	SELECT
	id as id,
	nome as nome,
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
	codigo as codigo,
	geom as geom
    [FROM]
        pe.pto_marco_de_limite_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_marco_de_limite_p.geometriaaproximada 
	left join dominios.tipo_hierarquia as dominio_tipomarcolim on dominio_tipomarcolim.code = pto_marco_de_limite_p.tipomarcolim 
	left join dominios.sistema_geodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_marco_de_limite_p.sistemageodesico 
	left join dominios.referencial_altim as dominio_referencialaltim on dominio_referencialaltim.code = pto_marco_de_limite_p.referencialaltim
#
DROP VIEW IF EXISTS views.veg_cerrado_a#CREATE [VIEW] views.veg_cerrado_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade,
	dominio_vereda.code_name as vereda
    [FROM]
        pe.veg_cerrado_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_cerrado_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_cerrado_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_cerrado_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_cerrado_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_cerrado_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_cerrado_a.densidade 
	left join dominios.booleano as dominio_vereda on dominio_vereda.code = veg_cerrado_a.vereda
#
DROP VIEW IF EXISTS views.tra_funicular_p#CREATE [VIEW] views.tra_funicular_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        pe.tra_funicular_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_funicular_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_funicular_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_funicular_p.situacaofisica
#
DROP VIEW IF EXISTS views.hdv_descontinuidade_geometrica_l#CREATE [VIEW] views.hdv_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.hdv_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = hdv_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hdv_fundeadouro_a#CREATE [VIEW] views.hdv_fundeadouro_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipofundeadouro.code_name as tipofundeadouro,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        pe.hdv_fundeadouro_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_fundeadouro_a.geometriaaproximada 
	left join dominios.tipo_fundeadouro as dominio_tipofundeadouro on dominio_tipofundeadouro.code = hdv_fundeadouro_a.tipofundeadouro 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_fundeadouro_a.administracao
#
DROP VIEW IF EXISTS views.hid_ilha_p#CREATE [VIEW] views.hid_ilha_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha,
	id_arquipelago as id_arquipelago
    [FROM]
        pe.hid_ilha_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_p.tipoelemnat 
	left join dominios.tipo_ilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_p.tipoilha
#
DROP VIEW IF EXISTS views.hid_ilha_l#CREATE [VIEW] views.hid_ilha_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha,
	id_arquipelago as id_arquipelago
    [FROM]
        pe.hid_ilha_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_l.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_l.tipoelemnat 
	left join dominios.tipo_ilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_l.tipoilha
#
DROP VIEW IF EXISTS views.rel_duna_a#CREATE [VIEW] views.rel_duna_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_fixa.code_name as fixa
    [FROM]
        pe.rel_duna_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_duna_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_duna_a.tipoelemnat 
	left join dominios.booleano as dominio_fixa on dominio_fixa.code = rel_duna_a.fixa
#
DROP VIEW IF EXISTS views.rel_aterro_p#CREATE [VIEW] views.rel_aterro_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_aterro_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_aterro_p.id)),',' ) as matconstr
    [FROM]
        pe.rel_aterro_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_aterro_p.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_aterro_p.tipoalterantrop
#
DROP VIEW IF EXISTS views.rel_duna_l#CREATE [VIEW] views.rel_duna_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_fixa.code_name as fixa
    [FROM]
        pe.rel_duna_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_duna_l.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_duna_l.tipoelemnat 
	left join dominios.booleano as dominio_fixa on dominio_fixa.code = rel_duna_l.fixa
#
DROP VIEW IF EXISTS views.lpal_unidade_protecao_integral_a#CREATE [VIEW] views.lpal_unidade_protecao_integral_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_protecao_integral_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_protecao_integral_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_protecao_integral_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_protecao_integral_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_protecao_integral_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.veg_reflorestamento_a#CREATE [VIEW] views.veg_reflorestamento_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_tipolavoura.code_name as tipolavoura,
	dominio_finalidade.code_name as finalidade,
	dominio_terreno.code_name as terreno,
	array_to_string( array(select code_name from dominios.cultivo_predominante dom join pe.veg_reflorestamento_a tn on (array[dom.code] <@ tn.cultivopredominante and tn.id=pe.veg_reflorestamento_a.id)),',' ) as cultivopredominante,
	espacamentoindividuos as espacamentoindividuos,
	espessura as espessura,
	alturamediaindividuos as alturamediaindividuos
    [FROM]
        pe.veg_reflorestamento_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_reflorestamento_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_reflorestamento_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_reflorestamento_a.classificacaoporte 
	left join dominios.tipo_lavoura as dominio_tipolavoura on dominio_tipolavoura.code = veg_reflorestamento_a.tipolavoura 
	left join dominios.finalidade_cultura as dominio_finalidade on dominio_finalidade.code = veg_reflorestamento_a.finalidade 
	left join dominios.condicao_terreno as dominio_terreno on dominio_terreno.code = veg_reflorestamento_a.terreno
#
DROP VIEW IF EXISTS views.hid_ilha_a#CREATE [VIEW] views.hid_ilha_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_tipoilha.code_name as tipoilha,
	id_arquipelago as id_arquipelago
    [FROM]
        pe.hid_ilha_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ilha_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_ilha_a.tipoelemnat 
	left join dominios.tipo_ilha as dominio_tipoilha on dominio_tipoilha.code = hid_ilha_a.tipoilha
#
DROP VIEW IF EXISTS views.eco_descontinuidade_geometrica_l#CREATE [VIEW] views.eco_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.eco_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = eco_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.pto_descontinuidade_geometrica_p#CREATE [VIEW] views.pto_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.pto_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = pto_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_rocha_em_agua_a#CREATE [VIEW] views.hid_rocha_em_agua_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_formarocha.code_name as formarocha,
	dominio_situacaoemagua.code_name as situacaoemagua,
	alturalamina as alturalamina
    [FROM]
        pe.hid_rocha_em_agua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_rocha_em_agua_a.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_rocha_em_agua_a.tipoelemnat 
	left join dominios.forma_rocha as dominio_formarocha on dominio_formarocha.code = hid_rocha_em_agua_a.formarocha 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_rocha_em_agua_a.situacaoemagua
#
DROP VIEW IF EXISTS views.fer_cremalheira_l#CREATE [VIEW] views.fer_cremalheira_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.fer_cremalheira_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_cremalheira_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_cremalheira_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_cremalheira_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_recife_a#CREATE [VIEW] views.hid_recife_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        pe.hid_recife_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_a.geometriaaproximada 
	left join dominios.tipo_recife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_a.tiporecife 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_recife_a.situacaoemagua 
	left join dominios.situacao_costa as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_a.situacaocosta
#
DROP VIEW IF EXISTS views.sb_barragem_calcadao_a#CREATE [VIEW] views.sb_barragem_calcadao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoequipdesenvsocial.code_name as tipoequipdesenvsocial,
	sigla as sigla,
	codequipdesenvsocial as codequipdesenvsocial,
	dominio_localizacaoequipdesenvsocial.code_name as localizacaoequipdesenvsocial,
	geom as geom
    [FROM]
        pe.sb_barragem_calcadao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_barragem_calcadao_a.geometriaaproximada 
	left join dominios.tipo_equip_desenv_social as dominio_tipoequipdesenvsocial on dominio_tipoequipdesenvsocial.code = sb_barragem_calcadao_a.tipoequipdesenvsocial 
	left join dominios.local_equip_desenv_social as dominio_localizacaoequipdesenvsocial on dominio_localizacaoequipdesenvsocial.code = sb_barragem_calcadao_a.localizacaoequipdesenvsocial
#
DROP VIEW IF EXISTS views.hid_recife_l#CREATE [VIEW] views.hid_recife_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporecife.code_name as tiporecife,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_situacaocosta.code_name as situacaocosta,
	geom as geom
    [FROM]
        pe.hid_recife_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_recife_l.geometriaaproximada 
	left join dominios.tipo_recife as dominio_tiporecife on dominio_tiporecife.code = hid_recife_l.tiporecife 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_recife_l.situacaoemagua 
	left join dominios.situacao_costa as dominio_situacaocosta on dominio_situacaocosta.code = hid_recife_l.situacaocosta
#
DROP VIEW IF EXISTS views.tra_descontinuidade_geometrica_l#CREATE [VIEW] views.tra_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	geometriaaproximada as geometriaaproximada,
	motivodescontinuidade as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.tra_descontinuidade_geometrica_l
#
DROP VIEW IF EXISTS views.pto_descontinuidade_geometrica_a#CREATE [VIEW] views.pto_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.pto_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = pto_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_barragem_l#CREATE [VIEW] views.hid_barragem_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_barragem_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_barragem_l.id)),',' ) as matconstr,
	dominio_usoprincipal.code_name as usoprincipal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.hid_barragem_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_barragem_l.geometriaaproximada 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_barragem_l.usoprincipal 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_barragem_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_barragem_l.situacaofisica
#
DROP VIEW IF EXISTS views.hid_rocha_em_agua_p#CREATE [VIEW] views.hid_rocha_em_agua_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_formarocha.code_name as formarocha,
	dominio_situacaoemagua.code_name as situacaoemagua,
	alturalamina as alturalamina
    [FROM]
        pe.hid_rocha_em_agua_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_rocha_em_agua_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = hid_rocha_em_agua_p.tipoelemnat 
	left join dominios.forma_rocha as dominio_formarocha on dominio_formarocha.code = hid_rocha_em_agua_p.formarocha 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_rocha_em_agua_p.situacaoemagua
#
DROP VIEW IF EXISTS views.dut_ponto_inicio_fim_duto_p#CREATE [VIEW] views.dut_ponto_inicio_fim_duto_p as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_duto as id_duto,
	dominio_relacionado.code_name as relacionado
    [FROM]
        pe.dut_ponto_inicio_fim_duto_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_ponto_inicio_fim_duto_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = dut_ponto_inicio_fim_duto_p.relacionado
#
DROP VIEW IF EXISTS views.tra_funicular_l#CREATE [VIEW] views.tra_funicular_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        pe.tra_funicular_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_funicular_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_funicular_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_funicular_l.situacaofisica
#
DROP VIEW IF EXISTS views.fer_cremalheira_p#CREATE [VIEW] views.fer_cremalheira_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.fer_cremalheira_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_cremalheira_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_cremalheira_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_cremalheira_p.situacaofisica
#
DROP VIEW IF EXISTS views.tra_tunel_p#CREATE [VIEW] views.tra_tunel_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_tunel_p tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_tunel_p.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_tunel_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_tunel_p.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	altura as altura,
	dominio_tipotunel.code_name as tipotunel,
	geom as geom
    [FROM]
        pe.tra_tunel_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_tunel_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_tunel_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_tunel_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_tunel_p.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_tunel_p.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_tunel_p.tipopavimentacao 
	left join dominios.tipo_tunel as dominio_tipotunel on dominio_tipotunel.code = tra_tunel_p.tipotunel
#
DROP VIEW IF EXISTS views.enc_termeletrica_l#CREATE [VIEW] views.enc_termeletrica_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom,
	dominio_tipocombustivel.code_name as tipocombustivel
    [FROM]
        pe.enc_termeletrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_termeletrica_l.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_termeletrica_l.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_termeletrica_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_termeletrica_l.situacaofisica 
	left join dominios.tipo_combustivel as dominio_tipocombustivel on dominio_tipocombustivel.code = enc_termeletrica_l.tipocombustivel
#
DROP VIEW IF EXISTS views.fer_girador_ferroviario_p#CREATE [VIEW] views.fer_girador_ferroviario_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_administracao.code_name as administracao,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_estacao_ferroviaria as id_estacao_ferroviaria,
	id_estacao_metroviaria as id_estacao_metroviaria
    [FROM]
        pe.fer_girador_ferroviario_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = fer_girador_ferroviario_p.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = fer_girador_ferroviario_p.administracao 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = fer_girador_ferroviario_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = fer_girador_ferroviario_p.situacaofisica
#
DROP VIEW IF EXISTS views.veg_floresta_a#CREATE [VIEW] views.veg_floresta_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade,
	dominio_especiepredominante.code_name as especiepredominante
    [FROM]
        pe.veg_floresta_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_floresta_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_floresta_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_floresta_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_floresta_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_floresta_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_floresta_a.densidade 
	left join dominios.especie as dominio_especiepredominante on dominio_especiepredominante.code = veg_floresta_a.especiepredominante
#
DROP VIEW IF EXISTS views.enc_grupo_transformadores_p#CREATE [VIEW] views.enc_grupo_transformadores_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_subest_transm_distrib_energia_eletrica as id_subest_transm_distrib_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_grupo_transformadores_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_grupo_transformadores_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_terreno_suj_inundacao_a#CREATE [VIEW] views.hid_terreno_suj_inundacao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	periodicidadeinunda as periodicidadeinunda,
	geom as geom
    [FROM]
        pe.hid_terreno_suj_inundacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_terreno_suj_inundacao_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_curva_batimetrica_l#CREATE [VIEW] views.rel_curva_batimetrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	profundidade as profundidade,
	geom as geom
    [FROM]
        pe.rel_curva_batimetrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_curva_batimetrica_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.dut_ponto_duto_p#CREATE [VIEW] views.dut_ponto_duto_p as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_duto as id_duto,
	dominio_relacionado.code_name as relacionado
    [FROM]
        pe.dut_ponto_duto_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_ponto_duto_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = dut_ponto_duto_p.relacionado
#
DROP VIEW IF EXISTS views.lpal_area_desenv_controle_a#CREATE [VIEW] views.lpal_area_desenv_controle_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao
    [FROM]
        pe.lpal_area_desenv_controle_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_area_desenv_controle_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.lpal_terra_publica_a#CREATE [VIEW] views.lpal_terra_publica_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao
    [FROM]
        pe.lpal_terra_publica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_terra_publica_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_terra_publica_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_terra_publica_a.jurisdicao
#
DROP VIEW IF EXISTS views.rel_ponto_cotado_batimetrico_p#CREATE [VIEW] views.rel_ponto_cotado_batimetrico_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	profundidade as profundidade,
	geom as geom
    [FROM]
        pe.rel_ponto_cotado_batimetrico_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_ponto_cotado_batimetrico_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.enc_termeletrica_a#CREATE [VIEW] views.enc_termeletrica_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom,
	dominio_tipocombustivel.code_name as tipocombustivel
    [FROM]
        pe.enc_termeletrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_termeletrica_a.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_termeletrica_a.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_termeletrica_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_termeletrica_a.situacaofisica 
	left join dominios.tipo_combustivel as dominio_tipocombustivel on dominio_tipocombustivel.code = enc_termeletrica_a.tipocombustivel
#
DROP VIEW IF EXISTS views.enc_grupo_transformadores_a#CREATE [VIEW] views.enc_grupo_transformadores_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	id_subest_transm_distrib_energia_eletrica as id_subest_transm_distrib_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_grupo_transformadores_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_grupo_transformadores_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.hid_canal_l#CREATE [VIEW] views.hid_canal_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_canal_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_canal_l.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_usoprincipal.code_name as usoprincipal
    [FROM]
        pe.hid_canal_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_canal_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_canal_l.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_canal_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_canal_l.situacaofisica 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_canal_l.finalidade 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_canal_l.usoprincipal
#
DROP VIEW IF EXISTS views.hdv_fundeadouro_p#CREATE [VIEW] views.hdv_fundeadouro_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipofundeadouro.code_name as tipofundeadouro,
	dominio_administracao.code_name as administracao,
	id_complexo_portuario as id_complexo_portuario,
	geom as geom
    [FROM]
        pe.hdv_fundeadouro_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_fundeadouro_p.geometriaaproximada 
	left join dominios.tipo_fundeadouro as dominio_tipofundeadouro on dominio_tipofundeadouro.code = hdv_fundeadouro_p.tipofundeadouro 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = hdv_fundeadouro_p.administracao
#
DROP VIEW IF EXISTS views.hid_canal_a#CREATE [VIEW] views.hid_canal_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_usoprincipal.code_name as usoprincipal,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_canal_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_canal_a.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade
    [FROM]
        pe.hid_canal_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_canal_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_canal_a.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_canal_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_canal_a.situacaofisica 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_canal_a.usoprincipal 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_canal_a.finalidade
#
DROP VIEW IF EXISTS views.tra_travessia_l#CREATE [VIEW] views.tra_travessia_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotravessia.code_name as tipotravessia,
	dominio_tipouso.code_name as tipouso,
	dominio_tipoembarcacao.code_name as tipoembarcacao,
	geom as geom
    [FROM]
        pe.tra_travessia_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_l.geometriaaproximada 
	left join dominios.tipo_travessia as dominio_tipotravessia on dominio_tipotravessia.code = tra_travessia_l.tipotravessia 
	left join dominios.tipo_transporte as dominio_tipouso on dominio_tipouso.code = tra_travessia_l.tipouso 
	left join dominios.tipo_embarcacao as dominio_tipoembarcacao on dominio_tipoembarcacao.code = tra_travessia_l.tipoembarcacao
#
DROP VIEW IF EXISTS views.lpal_terra_indigena_a#CREATE [VIEW] views.lpal_terra_indigena_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_situacaojuridica.code_name as situacaojuridica,
	datasituacaojuridica as datasituacaojuridica,
	grupoetnico as grupoetnico,
	perimetrooficial as perimetrooficial
    [FROM]
        pe.lpal_terra_indigena_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_terra_indigena_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_terra_indigena_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_terra_indigena_a.jurisdicao 
	left join dominios.situacao_juridica as dominio_situacaojuridica on dominio_situacaojuridica.code = lpal_terra_indigena_a.situacaojuridica
#
DROP VIEW IF EXISTS views.rel_gruta_caverna_l#CREATE [VIEW] views.rel_gruta_caverna_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_gruta_caverna_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_gruta_caverna_l.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_gruta_caverna_l.tipoelemnat
#
DROP VIEW IF EXISTS views.enc_trecho_energia_l#CREATE [VIEW] views.enc_trecho_energia_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_especie.code_name as especie,
	dominio_posicaorelativa.code_name as posicaorelativa,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom,
	id_org_comerc_serv as id_org_comerc_serv
    [FROM]
        pe.enc_trecho_energia_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_trecho_energia_l.geometriaaproximada 
	left join dominios.especie_trecho_energia as dominio_especie on dominio_especie.code = enc_trecho_energia_l.especie 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = enc_trecho_energia_l.posicaorelativa 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_trecho_energia_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_trecho_energia_l.situacaofisica
#
DROP VIEW IF EXISTS views.tra_ponte_l#CREATE [VIEW] views.tra_ponte_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_ponte_l tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_ponte_l.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_ponte_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_ponte_l.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipoponte.code_name as tipoponte,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        pe.tra_ponte_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_ponte_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_ponte_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_ponte_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_ponte_l.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_ponte_l.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_ponte_l.tipopavimentacao 
	left join dominios.tipo_ponte as dominio_tipoponte on dominio_tipoponte.code = tra_ponte_l.tipoponte
#
DROP VIEW IF EXISTS views.hdv_sinalizacao_p#CREATE [VIEW] views.hdv_sinalizacao_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposinal.code_name as tiposinal,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hdv_sinalizacao_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hdv_sinalizacao_p.geometriaaproximada 
	left join dominios.tipo_sinal as dominio_tiposinal on dominio_tiposinal.code = hdv_sinalizacao_p.tiposinal 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hdv_sinalizacao_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hdv_sinalizacao_p.situacaofisica
#
DROP VIEW IF EXISTS views.enc_descontinuidade_geometrica_p#CREATE [VIEW] views.enc_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.enc_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = enc_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lpal_pais_a#CREATE [VIEW] views.lpal_pais_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom,
	sigla as sigla,
	codiso3166 as codiso3166
    [FROM]
        pe.lpal_pais_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_pais_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.tra_tunel_l#CREATE [VIEW] views.tra_tunel_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_tunel_l tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_tunel_l.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_tunel_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_tunel_l.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	altura as altura,
	dominio_tipotunel.code_name as tipotunel,
	geom as geom
    [FROM]
        pe.tra_tunel_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_tunel_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_tunel_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_tunel_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_tunel_l.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_tunel_l.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_tunel_l.tipopavimentacao 
	left join dominios.tipo_tunel as dominio_tipotunel on dominio_tipotunel.code = tra_tunel_l.tipotunel
#
DROP VIEW IF EXISTS views.veg_veg_cultivada_a#CREATE [VIEW] views.veg_veg_cultivada_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_tipolavoura.code_name as tipolavoura,
	dominio_finalidade.code_name as finalidade,
	dominio_terreno.code_name as terreno,
	array_to_string( array(select code_name from dominios.cultivo_predominante dom join pe.veg_veg_cultivada_a tn on (array[dom.code] <@ tn.cultivopredominante and tn.id=pe.veg_veg_cultivada_a.id)),',' ) as cultivopredominante
    [FROM]
        pe.veg_veg_cultivada_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_cultivada_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_veg_cultivada_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_cultivada_a.classificacaoporte 
	left join dominios.tipo_lavoura as dominio_tipolavoura on dominio_tipolavoura.code = veg_veg_cultivada_a.tipolavoura 
	left join dominios.finalidade_cultura as dominio_finalidade on dominio_finalidade.code = veg_veg_cultivada_a.finalidade 
	left join dominios.condicao_terreno as dominio_terreno on dominio_terreno.code = veg_veg_cultivada_a.terreno
#
DROP VIEW IF EXISTS views.hid_vala_a#CREATE [VIEW] views.hid_vala_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_usoprincipal.code_name as usoprincipal,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_vala_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_vala_a.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade
    [FROM]
        pe.hid_vala_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_vala_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_vala_a.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_vala_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_vala_a.situacaofisica 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_vala_a.usoprincipal 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_vala_a.finalidade
#
DROP VIEW IF EXISTS views.veg_refugio_ecologico_a#CREATE [VIEW] views.veg_refugio_ecologico_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_refugio_ecologico_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_refugio_ecologico_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_refugio_ecologico_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_refugio_ecologico_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_refugio_ecologico_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_refugio_ecologico_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_refugio_ecologico_a.densidade
#
DROP VIEW IF EXISTS views.enc_descontinuidade_geometrica_a#CREATE [VIEW] views.enc_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.enc_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = enc_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_ext_mineral_p#CREATE [VIEW] views.eco_ext_mineral_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_secaoativecon.code_name as secaoativecon,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoextmin.code_name as tipoextmin,
	array_to_string( array(select code_name from dominios.tipo_produto_residuo dom join pe.eco_ext_mineral_p tn on (array[dom.code] <@ tn.tipoproduto and tn.id=pe.eco_ext_mineral_p.id)),',' ) as tipoproduto,
	dominio_tipopocomina.code_name as tipopocomina,
	dominio_procextracao.code_name as procextracao,
	dominio_formaextracao.code_name as formaextracao,
	dominio_atividade.code_name as atividade,
	id_org_ext_mineral as id_org_ext_mineral
    [FROM]
        pe.eco_ext_mineral_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_ext_mineral_p.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = eco_ext_mineral_p.tipoalterantrop 
	left join dominios.secao_ativ_econ as dominio_secaoativecon on dominio_secaoativecon.code = eco_ext_mineral_p.secaoativecon 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_ext_mineral_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_ext_mineral_p.situacaofisica 
	left join dominios.tipo_ext_min as dominio_tipoextmin on dominio_tipoextmin.code = eco_ext_mineral_p.tipoextmin 
	left join dominios.tipo_poco_mina as dominio_tipopocomina on dominio_tipopocomina.code = eco_ext_mineral_p.tipopocomina 
	left join dominios.proc_extracao as dominio_procextracao on dominio_procextracao.code = eco_ext_mineral_p.procextracao 
	left join dominios.forma_extracao as dominio_formaextracao on dominio_formaextracao.code = eco_ext_mineral_p.formaextracao 
	left join dominios.atividade as dominio_atividade on dominio_atividade.code = eco_ext_mineral_p.atividade
#
DROP VIEW IF EXISTS views.rel_gruta_caverna_p#CREATE [VIEW] views.rel_gruta_caverna_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom
    [FROM]
        pe.rel_gruta_caverna_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_gruta_caverna_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_gruta_caverna_p.tipoelemnat
#
DROP VIEW IF EXISTS views.hid_vala_l#CREATE [VIEW] views.hid_vala_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_vala_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_vala_l.id)),',' ) as matconstr,
	dominio_finalidade.code_name as finalidade,
	dominio_usoprincipal.code_name as usoprincipal
    [FROM]
        pe.hid_vala_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_vala_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = hid_vala_l.tipoalterantrop 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_vala_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_vala_l.situacaofisica 
	left join dominios.finalidade_galeria_bueiro as dominio_finalidade on dominio_finalidade.code = hid_vala_l.finalidade 
	left join dominios.uso_principal as dominio_usoprincipal on dominio_usoprincipal.code = hid_vala_l.usoprincipal
#
DROP VIEW IF EXISTS views.rod_passagem_nivel_p#CREATE [VIEW] views.rod_passagem_nivel_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom,
	nome as nome
    [FROM]
        pe.rod_passagem_nivel_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_passagem_nivel_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = rod_passagem_nivel_p.relacionado
#
DROP VIEW IF EXISTS views.veg_campinarana_a#CREATE [VIEW] views.veg_campinarana_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_campinarana_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_campinarana_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_campinarana_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_campinarana_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_campinarana_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_campinarana_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_campinarana_a.densidade
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_a#CREATE [VIEW] views.rel_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rel_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.hid_quebramar_molhe_a#CREATE [VIEW] views.hid_quebramar_molhe_a as 
	SELECT
	id as id,
	dominio_tipoquebramolhe.code_name as tipoquebramolhe,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_quebramar_molhe_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_quebramar_molhe_a.id)),',' ) as matconstr,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hid_quebramar_molhe_a 
	left join dominios.tipo_quebra_molhe as dominio_tipoquebramolhe on dominio_tipoquebramolhe.code = hid_quebramar_molhe_a.tipoquebramolhe 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_quebramar_molhe_a.geometriaaproximada 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_quebramar_molhe_a.situacaoemagua 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_quebramar_molhe_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_quebramar_molhe_a.situacaofisica
#
DROP VIEW IF EXISTS views.rel_terreno_erodido_l#CREATE [VIEW] views.rel_terreno_erodido_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_situacaoterreno.code_name as situacaoterreno,
	dominio_tipoerosao.code_name as tipoerosao,
	geom as geom
    [FROM]
        pe.rel_terreno_erodido_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_terreno_erodido_l.geometriaaproximada 
	left join dominios.situacao_terreno as dominio_situacaoterreno on dominio_situacaoterreno.code = rel_terreno_erodido_l.situacaoterreno 
	left join dominios.tipo_erosao as dominio_tipoerosao on dominio_tipoerosao.code = rel_terreno_erodido_l.tipoerosao
#
DROP VIEW IF EXISTS views.rel_curva_nivel_l#CREATE [VIEW] views.rel_curva_nivel_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	cota as cota,
	dominio_depressao.code_name as depressao,
	dominio_tipocurvanivel.code_name as tipocurvanivel,
	geom as geom
    [FROM]
        pe.rel_curva_nivel_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_curva_nivel_l.geometriaaproximada 
	left join dominios.booleano as dominio_depressao on dominio_depressao.code = rel_curva_nivel_l.depressao 
	left join dominios.tipo_curva_nivel as dominio_tipocurvanivel on dominio_tipocurvanivel.code = rel_curva_nivel_l.tipocurvanivel
#
DROP VIEW IF EXISTS views.hid_quebramar_molhe_l#CREATE [VIEW] views.hid_quebramar_molhe_l as 
	SELECT
	id as id,
	dominio_tipoquebramolhe.code_name as tipoquebramolhe,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_quebramar_molhe_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_quebramar_molhe_l.id)),',' ) as matconstr,
	dominio_situacaoemagua.code_name as situacaoemagua,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	geom as geom
    [FROM]
        pe.hid_quebramar_molhe_l 
	left join dominios.tipo_quebra_molhe as dominio_tipoquebramolhe on dominio_tipoquebramolhe.code = hid_quebramar_molhe_l.tipoquebramolhe 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_quebramar_molhe_l.geometriaaproximada 
	left join dominios.situacao_em_agua as dominio_situacaoemagua on dominio_situacaoemagua.code = hid_quebramar_molhe_l.situacaoemagua 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = hid_quebramar_molhe_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = hid_quebramar_molhe_l.situacaofisica
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_l#CREATE [VIEW] views.rel_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rel_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.lpal_limite_politico_adm_l#CREATE [VIEW] views.lpal_limite_politico_adm_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_referenciallegal.code_name as referenciallegal,
	obssituacao as obssituacao,
	extensao as extensao,
	geom as geom,
	array_to_string( array(select code_name from dominios.tipo_lim_pol dom join pe.lpal_limite_politico_adm_l tn on (array[dom.code] <@ tn.tipolimpol and tn.id=pe.lpal_limite_politico_adm_l.id)),',' ) as tipolimpol
    [FROM]
        pe.lpal_limite_politico_adm_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_limite_politico_adm_l.geometriaaproximada 
	left join dominios.referencial_legal as dominio_referenciallegal on dominio_referenciallegal.code = lpal_limite_politico_adm_l.referenciallegal
#
DROP VIEW IF EXISTS views.veg_caatinga_a#CREATE [VIEW] views.veg_caatinga_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade
    [FROM]
        pe.veg_caatinga_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_caatinga_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_caatinga_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_caatinga_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_caatinga_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_caatinga_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_caatinga_a.densidade
#
DROP VIEW IF EXISTS views.lpal_unidade_conservacao_a#CREATE [VIEW] views.lpal_unidade_conservacao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_conservacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_conservacao_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_conservacao_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_conservacao_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_conservacao_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.veg_vegetacao_a#CREATE [VIEW] views.veg_vegetacao_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde
    [FROM]
        pe.veg_vegetacao_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_vegetacao_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_vegetacao_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_vegetacao_a.classificacaoporte
#
DROP VIEW IF EXISTS views.hid_ponto_drenagem_p#CREATE [VIEW] views.hid_ponto_drenagem_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_relacionado.code_name as relacionado,
	geom as geom
    [FROM]
        pe.hid_ponto_drenagem_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_ponto_drenagem_p.geometriaaproximada 
	left join dominios.relacionado as dominio_relacionado on dominio_relacionado.code = hid_ponto_drenagem_p.relacionado
#
DROP VIEW IF EXISTS views.rel_descontinuidade_geometrica_p#CREATE [VIEW] views.rel_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rel_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rel_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.tra_passagem_elevada_viaduto_l#CREATE [VIEW] views.tra_passagem_elevada_viaduto_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.modal_uso dom join pe.tra_passagem_elevada_viaduto_l tn on (array[dom.code] <@ tn.modaluso and tn.id=pe.tra_passagem_elevada_viaduto_l.id)),',' ) as modaluso,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.tra_passagem_elevada_viaduto_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.tra_passagem_elevada_viaduto_l.id)),',' ) as matconstr,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_necessitamanutencao.code_name as necessitamanutencao,
	largura as largura,
	entensao as entensao,
	nrfaixas as nrfaixas,
	nrpistas as nrpistas,
	dominio_posicaopista.code_name as posicaopista,
	id_via_ferrea as id_via_ferrea,
	dominio_tipopavimentacao.code_name as tipopavimentacao,
	dominio_tipopassagviad.code_name as tipopassagviad,
	vaolivrehoriz as vaolivrehoriz,
	vaovertical as vaovertical,
	gabhorizsup as gabhorizsup,
	cargasuportmaxima as cargasuportmaxima,
	geom as geom
    [FROM]
        pe.tra_passagem_elevada_viaduto_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_passagem_elevada_viaduto_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_passagem_elevada_viaduto_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_passagem_elevada_viaduto_l.situacaofisica 
	left join dominios.booleano_estendido as dominio_necessitamanutencao on dominio_necessitamanutencao.code = tra_passagem_elevada_viaduto_l.necessitamanutencao 
	left join dominios.situacao_espacial as dominio_posicaopista on dominio_posicaopista.code = tra_passagem_elevada_viaduto_l.posicaopista 
	left join dominios.tipo_pavimentacao as dominio_tipopavimentacao on dominio_tipopavimentacao.code = tra_passagem_elevada_viaduto_l.tipopavimentacao 
	left join dominios.tipo_passag_viad as dominio_tipopassagviad on dominio_tipopassagviad.code = tra_passagem_elevada_viaduto_l.tipopassagviad
#
DROP VIEW IF EXISTS views.dut_condutor_hidrico_l#CREATE [VIEW] views.dut_condutor_hidrico_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipotrechoduto.code_name as tipotrechoduto,
	array_to_string( array(select code_name from dominios.mat_transp dom join pe.dut_condutor_hidrico_l tn on (array[dom.code] <@ tn.mattransp and tn.id=pe.dut_condutor_hidrico_l.id)),',' ) as mattransp,
	dominio_setor.code_name as setor,
	dominio_posicaorelativa.code_name as posicaorelativa,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.dut_condutor_hidrico_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.dut_condutor_hidrico_l.id)),',' ) as matconstr,
	nrdutos as nrdutos,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	id_duto as id_duto,
	geom as geom,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica
    [FROM]
        pe.dut_condutor_hidrico_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_condutor_hidrico_l.geometriaaproximada 
	left join dominios.tipo_trecho_duto as dominio_tipotrechoduto on dominio_tipotrechoduto.code = dut_condutor_hidrico_l.tipotrechoduto 
	left join dominios.setor as dominio_setor on dominio_setor.code = dut_condutor_hidrico_l.setor 
	left join dominios.posicao_relativa as dominio_posicaorelativa on dominio_posicaorelativa.code = dut_condutor_hidrico_l.posicaorelativa 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = dut_condutor_hidrico_l.situacaoespacial 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = dut_condutor_hidrico_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = dut_condutor_hidrico_l.situacaofisica
#
DROP VIEW IF EXISTS views.lpal_unidade_uso_sustentavel_a#CREATE [VIEW] views.lpal_unidade_uso_sustentavel_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_uso_sustentavel_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_uso_sustentavel_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_uso_sustentavel_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_uso_sustentavel_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_uso_sustentavel_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.veg_mangue_a#CREATE [VIEW] views.veg_mangue_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade,
	dominio_tipomanguezal.code_name as tipomanguezal
    [FROM]
        pe.veg_mangue_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_mangue_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_mangue_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_mangue_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_mangue_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_mangue_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_mangue_a.densidade 
	left join dominios.tipo_manguezal as dominio_tipomanguezal on dominio_tipomanguezal.code = veg_mangue_a.tipomanguezal
#
DROP VIEW IF EXISTS views.hid_limite_massa_dagua_l#CREATE [VIEW] views.hid_limite_massa_dagua_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipolimmassa.code_name as tipolimmassa,
	dominio_materialpredominante.code_name as materialpredominante,
	dominio_revestida.code_name as revestida,
	geom as geom
    [FROM]
        pe.hid_limite_massa_dagua_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_limite_massa_dagua_l.geometriaaproximada 
	left join dominios.tipo_lim_massa as dominio_tipolimmassa on dominio_tipolimmassa.code = hid_limite_massa_dagua_l.tipolimmassa 
	left join dominios.material_predominante as dominio_materialpredominante on dominio_materialpredominante.code = hid_limite_massa_dagua_l.materialpredominante 
	left join dominios.booleano_estendido as dominio_revestida on dominio_revestida.code = hid_limite_massa_dagua_l.revestida
#
DROP VIEW IF EXISTS views.aer_descontinuidade_geometrica_l#CREATE [VIEW] views.aer_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.aer_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = aer_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = aer_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rel_aterro_l#CREATE [VIEW] views.rel_aterro_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_aterro_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_aterro_l.id)),',' ) as matconstr
    [FROM]
        pe.rel_aterro_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_aterro_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_aterro_l.tipoalterantrop
#
DROP VIEW IF EXISTS views.rel_rocha_l#CREATE [VIEW] views.rel_rocha_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_formarocha.code_name as formarocha
    [FROM]
        pe.rel_rocha_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_rocha_l.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_rocha_l.tipoelemnat 
	left join dominios.forma_rocha as dominio_formarocha on dominio_formarocha.code = rel_rocha_l.formarocha
#
DROP VIEW IF EXISTS views.rel_alter_fisiog_antropica_a#CREATE [VIEW] views.rel_alter_fisiog_antropica_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom
    [FROM]
        pe.rel_alter_fisiog_antropica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_alter_fisiog_antropica_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_alter_fisiog_antropica_a.tipoalterantrop
#
DROP VIEW IF EXISTS views.tra_caminho_carrocavel_l#CREATE [VIEW] views.tra_caminho_carrocavel_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	geom as geom
    [FROM]
        pe.tra_caminho_carrocavel_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_caminho_carrocavel_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_rocha_p#CREATE [VIEW] views.rel_rocha_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoelemnat.code_name as tipoelemnat,
	geom as geom,
	dominio_formarocha.code_name as formarocha
    [FROM]
        pe.rel_rocha_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_rocha_p.geometriaaproximada 
	left join dominios.tipo_elem_nat as dominio_tipoelemnat on dominio_tipoelemnat.code = rel_rocha_p.tipoelemnat 
	left join dominios.forma_rocha as dominio_formarocha on dominio_formarocha.code = rel_rocha_p.formarocha
#
DROP VIEW IF EXISTS views.rel_alter_fisiog_antropica_l#CREATE [VIEW] views.rel_alter_fisiog_antropica_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom
    [FROM]
        pe.rel_alter_fisiog_antropica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_alter_fisiog_antropica_l.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_alter_fisiog_antropica_l.tipoalterantrop
#
DROP VIEW IF EXISTS views.sb_cemiterio_p#CREATE [VIEW] views.sb_cemiterio_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipocemiterio.code_name as tipocemiterio,
	dominio_denominacaoassociada.code_name as denominacaoassociada,
	dominio_destinacaocemiterio.code_name as destinacaocemiterio,
	organizacao as organizacao,
	id_org_comerc_serv as id_org_comerc_serv,
	id_org_pub_civil as id_org_pub_civil,
	geom as geom
    [FROM]
        pe.sb_cemiterio_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = sb_cemiterio_p.geometriaaproximada 
	left join dominios.tipo_cemiterio as dominio_tipocemiterio on dominio_tipocemiterio.code = sb_cemiterio_p.tipocemiterio 
	left join dominios.denominacao_associada as dominio_denominacaoassociada on dominio_denominacaoassociada.code = sb_cemiterio_p.denominacaoassociada 
	left join dominios.destinacao_cemiterio as dominio_destinacaocemiterio on dominio_destinacaocemiterio.code = sb_cemiterio_p.destinacaocemiterio
#
DROP VIEW IF EXISTS views.rel_aterro_a#CREATE [VIEW] views.rel_aterro_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.rel_aterro_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.rel_aterro_a.id)),',' ) as matconstr
    [FROM]
        pe.rel_aterro_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_aterro_a.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_aterro_a.tipoalterantrop
#
DROP VIEW IF EXISTS views.hid_sumidouro_vertedouro_p#CREATE [VIEW] views.hid_sumidouro_vertedouro_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiposumvert.code_name as tiposumvert,
	dominio_causa.code_name as causa,
	geom as geom
    [FROM]
        pe.hid_sumidouro_vertedouro_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_sumidouro_vertedouro_p.geometriaaproximada 
	left join dominios.tipo_sum_vert as dominio_tiposumvert on dominio_tiposumvert.code = hid_sumidouro_vertedouro_p.tiposumvert 
	left join dominios.causa as dominio_causa on dominio_causa.code = hid_sumidouro_vertedouro_p.causa
#
DROP VIEW IF EXISTS views.hid_queda_dagua_a#CREATE [VIEW] views.hid_queda_dagua_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        pe.hid_queda_dagua_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_a.geometriaaproximada 
	left join dominios.tipo_queda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_a.tipoqueda
#
DROP VIEW IF EXISTS views.rel_alter_fisiog_antropica_p#CREATE [VIEW] views.rel_alter_fisiog_antropica_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoalterantrop.code_name as tipoalterantrop,
	geom as geom
    [FROM]
        pe.rel_alter_fisiog_antropica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_alter_fisiog_antropica_p.geometriaaproximada 
	left join dominios.tipo_alter_antrop as dominio_tipoalterantrop on dominio_tipoalterantrop.code = rel_alter_fisiog_antropica_p.tipoalterantrop
#
DROP VIEW IF EXISTS views.dut_faixa_dominial_duto_a#CREATE [VIEW] views.dut_faixa_dominial_duto_a as 
	SELECT
	id as id,
	geom as geom,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	largura as largura
    [FROM]
        pe.dut_faixa_dominial_duto_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_faixa_dominial_duto_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.enc_antena_comunic_p#CREATE [VIEW] views.enc_antena_comunic_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_posicaoreledific.code_name as posicaoreledific,
	geom as geom,
	id_complexo_comunicacao as id_complexo_comunicacao
    [FROM]
        pe.enc_antena_comunic_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_antena_comunic_p.geometriaaproximada 
	left join dominios.posicao_rel_edific as dominio_posicaoreledific on dominio_posicaoreledific.code = enc_antena_comunic_p.posicaoreledific
#
DROP VIEW IF EXISTS views.hid_queda_dagua_l#CREATE [VIEW] views.hid_queda_dagua_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoqueda.code_name as tipoqueda,
	altura as altura,
	geom as geom
    [FROM]
        pe.hid_queda_dagua_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_queda_dagua_l.geometriaaproximada 
	left join dominios.tipo_queda as dominio_tipoqueda on dominio_tipoqueda.code = hid_queda_dagua_l.tipoqueda
#
DROP VIEW IF EXISTS views.rod_descontinuidade_geometrica_l#CREATE [VIEW] views.rod_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rod_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rod_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_p#CREATE [VIEW] views.enc_est_gerad_energia_eletr_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_est_gerad_energia_eletr_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_p.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_p.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_p.situacaofisica
#
DROP VIEW IF EXISTS views.eco_equip_agropec_a#CREATE [VIEW] views.eco_equip_agropec_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.eco_equip_agropec_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.eco_equip_agropec_a.id)),',' ) as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        pe.eco_equip_agropec_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_a.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_equip_agropec_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_a.situacaofisica 
	left join dominios.tipo_equip_agropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_a.tipoequipagropec
#
DROP VIEW IF EXISTS views.eco_plataforma_a#CREATE [VIEW] views.eco_plataforma_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoplataforma.code_name as tipoplataforma,
	id_org_ext_mineral as id_org_ext_mineral,
	geom as geom
    [FROM]
        pe.eco_plataforma_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_plataforma_a.geometriaaproximada 
	left join dominios.tipo_plataforma as dominio_tipoplataforma on dominio_tipoplataforma.code = eco_plataforma_a.tipoplataforma
#
DROP VIEW IF EXISTS views.hid_dique_a#CREATE [VIEW] views.hid_dique_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_dique_a tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_dique_a.id)),',' ) as matconstr,
	geom as geom
    [FROM]
        pe.hid_dique_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_dique_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.veg_veg_area_contato_a#CREATE [VIEW] views.veg_veg_area_contato_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoveg.code_name as tipoveg,
	dominio_classificacaoporte.code_name as classificacaoporte,
	geom as geom,
	id_area_verde as id_area_verde,
	dominio_antropizada.code_name as antropizada,
	dominio_secundaria.code_name as secundaria,
	dominio_densidade.code_name as densidade,
	array_to_string( array(select code_name from dominios.tipo_vegetacao dom join pe.veg_veg_area_contato_a tn on (array[dom.code] <@ tn.tipovegcontato and tn.id=pe.veg_veg_area_contato_a.id)),',' ) as tipovegcontato
    [FROM]
        pe.veg_veg_area_contato_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = veg_veg_area_contato_a.geometriaaproximada 
	left join dominios.tipo_vegetacao as dominio_tipoveg on dominio_tipoveg.code = veg_veg_area_contato_a.tipoveg 
	left join dominios.classificacao_porte as dominio_classificacaoporte on dominio_classificacaoporte.code = veg_veg_area_contato_a.classificacaoporte 
	left join dominios.booleano_estendido as dominio_antropizada on dominio_antropizada.code = veg_veg_area_contato_a.antropizada 
	left join dominios.booleano_estendido as dominio_secundaria on dominio_secundaria.code = veg_veg_area_contato_a.secundaria 
	left join dominios.densidade as dominio_densidade on dominio_densidade.code = veg_veg_area_contato_a.densidade
#
DROP VIEW IF EXISTS views.lpal_unidade_conservacao_snuc_a#CREATE [VIEW] views.lpal_unidade_conservacao_snuc_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	anocriacao as anocriacao,
	historicomodificacoes as historicomodificacoes,
	sigla as sigla,
	atolegal as atolegal,
	areaoficial as areaoficial,
	dominio_administracao.code_name as administracao,
	classificacao as classificacao,
	dominio_jurisdicao.code_name as jurisdicao,
	dominio_tipounidprotegida.code_name as tipounidprotegida
    [FROM]
        pe.lpal_unidade_conservacao_snuc_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_unidade_conservacao_snuc_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_unidade_conservacao_snuc_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_unidade_conservacao_snuc_a.jurisdicao 
	left join dominios.tipo_unid_protegida as dominio_tipounidprotegida on dominio_tipounidprotegida.code = lpal_unidade_conservacao_snuc_a.tipounidprotegida
#
DROP VIEW IF EXISTS views.hid_dique_l#CREATE [VIEW] views.hid_dique_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_dique_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_dique_l.id)),',' ) as matconstr,
	geom as geom
    [FROM]
        pe.hid_dique_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_dique_l.geometriaaproximada
#
DROP VIEW IF EXISTS views.pto_pto_geod_topo_controle_p#CREATE [VIEW] views.pto_pto_geod_topo_controle_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tiporef.code_name as tiporef,
	latitude as latitude,
	longitude as longitude,
	altitudeortometrica as altitudeortometrica,
	altitudegeometrica as altitudegeometrica,
	dominio_sistemageodesico.code_name as sistemageodesico,
	outrarefplan as outrarefplan,
	dominio_referencialaltim.code_name as referencialaltim,
	outrarefalt as outrarefalt,
	orgaoenteresp as orgaoenteresp,
	codponto as codponto,
	obs as obs,
	geom as geom
    [FROM]
        pe.pto_pto_geod_topo_controle_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = pto_pto_geod_topo_controle_p.geometriaaproximada 
	left join dominios.tipo_ref as dominio_tiporef on dominio_tiporef.code = pto_pto_geod_topo_controle_p.tiporef 
	left join dominios.sistema_geodesico as dominio_sistemageodesico on dominio_sistemageodesico.code = pto_pto_geod_topo_controle_p.sistemageodesico 
	left join dominios.referencial_altim as dominio_referencialaltim on dominio_referencialaltim.code = pto_pto_geod_topo_controle_p.referencialaltim
#
DROP VIEW IF EXISTS views.lpal_area_pub_militar_a#CREATE [VIEW] views.lpal_area_pub_militar_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom,
	classificacao as classificacao,
	dominio_administracao.code_name as administracao,
	dominio_jurisdicao.code_name as jurisdicao,
	id_org_pub_militar as id_org_pub_militar
    [FROM]
        pe.lpal_area_pub_militar_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_area_pub_militar_a.geometriaaproximada 
	left join dominios.administracao as dominio_administracao on dominio_administracao.code = lpal_area_pub_militar_a.administracao 
	left join dominios.jurisdicao as dominio_jurisdicao on dominio_jurisdicao.code = lpal_area_pub_militar_a.jurisdicao
#
DROP VIEW IF EXISTS views.rod_descontinuidade_geometrica_a#CREATE [VIEW] views.rod_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rod_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rod_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.dut_descontinuidade_geometrica_p#CREATE [VIEW] views.dut_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.dut_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = dut_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_equip_agropec_l#CREATE [VIEW] views.eco_equip_agropec_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.eco_equip_agropec_l tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.eco_equip_agropec_l.id)),',' ) as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        pe.eco_equip_agropec_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_l.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_equip_agropec_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_l.situacaofisica 
	left join dominios.tipo_equip_agropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_l.tipoequipagropec
#
DROP VIEW IF EXISTS views.dut_descontinuidade_geometrica_l#CREATE [VIEW] views.dut_descontinuidade_geometrica_l as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.dut_descontinuidade_geometrica_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_descontinuidade_geometrica_l.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = dut_descontinuidade_geometrica_l.motivodescontinuidade
#
DROP VIEW IF EXISTS views.eco_equip_agropec_p#CREATE [VIEW] views.eco_equip_agropec_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_tipoequipagropec.code_name as tipoequipagropec,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.eco_equip_agropec_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.eco_equip_agropec_p.id)),',' ) as matconstr,
	id_org_agropec_ext_veg_pesca as id_org_agropec_ext_veg_pesca,
	geom as geom
    [FROM]
        pe.eco_equip_agropec_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = eco_equip_agropec_p.geometriaaproximada 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = eco_equip_agropec_p.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = eco_equip_agropec_p.situacaofisica 
	left join dominios.tipo_equip_agropec as dominio_tipoequipagropec on dominio_tipoequipagropec.code = eco_equip_agropec_p.tipoequipagropec
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_a#CREATE [VIEW] views.enc_est_gerad_energia_eletr_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_est_gerad_energia_eletr_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_a.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_a.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_a.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_a.situacaofisica
#
DROP VIEW IF EXISTS views.hid_dique_p#CREATE [VIEW] views.hid_dique_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	array_to_string( array(select code_name from dominios.mat_constr dom join pe.hid_dique_p tn on (array[dom.code] <@ tn.matconstr and tn.id=pe.hid_dique_p.id)),',' ) as matconstr,
	geom as geom
    [FROM]
        pe.hid_dique_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = hid_dique_p.geometriaaproximada
#
DROP VIEW IF EXISTS views.lpal_area_especial_a#CREATE [VIEW] views.lpal_area_especial_a as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	codidentificadorunico as codidentificadorunico,
	geom as geom
    [FROM]
        pe.lpal_area_especial_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = lpal_area_especial_a.geometriaaproximada
#
DROP VIEW IF EXISTS views.rel_terreno_erodido_p#CREATE [VIEW] views.rel_terreno_erodido_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_situacaoterreno.code_name as situacaoterreno,
	dominio_tipoerosao.code_name as tipoerosao,
	geom as geom
    [FROM]
        pe.rel_terreno_erodido_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rel_terreno_erodido_p.geometriaaproximada 
	left join dominios.situacao_terreno as dominio_situacaoterreno on dominio_situacaoterreno.code = rel_terreno_erodido_p.situacaoterreno 
	left join dominios.tipo_erosao as dominio_tipoerosao on dominio_tipoerosao.code = rel_terreno_erodido_p.tipoerosao
#
DROP VIEW IF EXISTS views.dut_descontinuidade_geometrica_a#CREATE [VIEW] views.dut_descontinuidade_geometrica_a as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.dut_descontinuidade_geometrica_a 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = dut_descontinuidade_geometrica_a.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = dut_descontinuidade_geometrica_a.motivodescontinuidade
#
DROP VIEW IF EXISTS views.rod_descontinuidade_geometrica_p#CREATE [VIEW] views.rod_descontinuidade_geometrica_p as 
	SELECT
	id as id,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_motivodescontinuidade.code_name as motivodescontinuidade,
	geom as geom
    [FROM]
        pe.rod_descontinuidade_geometrica_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = rod_descontinuidade_geometrica_p.geometriaaproximada 
	left join dominios.motivodescontinuidade as dominio_motivodescontinuidade on dominio_motivodescontinuidade.code = rod_descontinuidade_geometrica_p.motivodescontinuidade
#
DROP VIEW IF EXISTS views.enc_est_gerad_energia_eletr_l#CREATE [VIEW] views.enc_est_gerad_energia_eletr_l as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_tipoestgerad.code_name as tipoestgerad,
	dominio_operacional.code_name as operacional,
	dominio_situacaofisica.code_name as situacaofisica,
	potencia as potencia,
	id_complexo_gerador_energia_eletrica as id_complexo_gerador_energia_eletrica,
	geom as geom
    [FROM]
        pe.enc_est_gerad_energia_eletr_l 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = enc_est_gerad_energia_eletr_l.geometriaaproximada 
	left join dominios.tipo_est_gerad as dominio_tipoestgerad on dominio_tipoestgerad.code = enc_est_gerad_energia_eletr_l.tipoestgerad 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = enc_est_gerad_energia_eletr_l.operacional 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = enc_est_gerad_energia_eletr_l.situacaofisica
#
DROP VIEW IF EXISTS views.tra_travessia_pedestre_p#CREATE [VIEW] views.tra_travessia_pedestre_p as 
	SELECT
	id as id,
	nome as nome,
	dominio_geometriaaproximada.code_name as geometriaaproximada,
	dominio_matconstr.code_name as matconstr,
	dominio_situacaofisica.code_name as situacaofisica,
	dominio_operacional.code_name as operacional,
	dominio_situacaoespacial.code_name as situacaoespacial,
	dominio_tipotravessiaped.code_name as tipotravessiaped,
	largura as largura,
	extensao as extensao,
	geom as geom
    [FROM]
        pe.tra_travessia_pedestre_p 
	left join dominios.booleano as dominio_geometriaaproximada on dominio_geometriaaproximada.code = tra_travessia_pedestre_p.geometriaaproximada 
	left join dominios.mat_constr as dominio_matconstr on dominio_matconstr.code = tra_travessia_pedestre_p.matconstr 
	left join dominios.situacao_fisica as dominio_situacaofisica on dominio_situacaofisica.code = tra_travessia_pedestre_p.situacaofisica 
	left join dominios.booleano_estendido as dominio_operacional on dominio_operacional.code = tra_travessia_pedestre_p.operacional 
	left join dominios.situacao_espacial as dominio_situacaoespacial on dominio_situacaoespacial.code = tra_travessia_pedestre_p.situacaoespacial 
	left join dominios.tipo_travessia_ped as dominio_tipotravessiaped on dominio_tipotravessiaped.code = tra_travessia_pedestre_p.tipotravessiaped