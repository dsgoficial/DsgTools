<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="133,182,111,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.26"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties/>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks type="StringList">
      <Option type="QString" value=""/>
    </activeChecks>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nome">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Passagem elevada" type="QString" value="301"/>
              <Option name="Ponte fixa" type="QString" value="203"/>
              <Option name="Ponte móvel" type="QString" value="201"/>
              <Option name="Ponte pênsil" type="QString" value="202"/>
              <Option name="Travessia - Balsa" type="QString" value="404"/>
              <Option name="Travessia - Bote transportador" type="QString" value="403"/>
              <Option name="Travessia - Vau construído" type="QString" value="402"/>
              <Option name="Travessia - Vau natural" type="QString" value="401"/>
              <Option name="Túnel" type="QString" value="101"/>
              <Option name="Túnel - Passagem subterrânea sob via" type="QString" value="102"/>
              <Option name="Viaduto" type="QString" value="302"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="material_construcao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Arame" type="QString" value="6"/>
              <Option name="Cerca viva" type="QString" value="8"/>
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="98"/>
              <Option name="Rocha" type="QString" value="4"/>
              <Option name="Tela ou alambrado" type="QString" value="7"/>
              <Option name="Terra" type="QString" value="23"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="modal_uso">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Aeroportuário" type="QString" value="9"/>
              <Option name="Ferroviário" type="QString" value="5"/>
              <Option name="Metroviário" type="QString" value="6"/>
              <Option name="Rodoferroviário" type="QString" value="8"/>
              <Option name="Rodoviário" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_faixas">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nr_pistas">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="posicao_pista">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Adjacentes" type="QString" value="12"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Superpostas" type="QString" value="13"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacao_fisica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Abandonada" type="QString" value="1"/>
              <Option name="Construída" type="QString" value="3"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Destruída" type="QString" value="2"/>
              <Option name="Em construção" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_comprovacao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Confirmado em campo" type="QString" value="1"/>
              <Option name="Feição não necessita de confirmação" type="QString" value="3"/>
              <Option name="Não possível de confirmar em campo" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_insumo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Aquisição em campo" type="QString" value="4"/>
              <Option name="Fotointerpretado" type="QString" value="1"/>
              <Option name="Insumo externo" type="QString" value="2"/>
              <Option name="Mapeamento anterior" type="QString" value="5"/>
              <Option name="Processo automático" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="observacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_modificacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="controle_id">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ultimo_usuario">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="length_otf">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="tipo"/>
    <alias name="" index="3" field="material_construcao"/>
    <alias name="" index="4" field="modal_uso"/>
    <alias name="" index="5" field="nr_faixas"/>
    <alias name="" index="6" field="nr_pistas"/>
    <alias name="" index="7" field="posicao_pista"/>
    <alias name="" index="8" field="situacao_fisica"/>
    <alias name="" index="9" field="tipo_comprovacao"/>
    <alias name="" index="10" field="tipo_insumo"/>
    <alias name="" index="11" field="observacao"/>
    <alias name="" index="12" field="data_modificacao"/>
    <alias name="" index="13" field="controle_id"/>
    <alias name="" index="14" field="ultimo_usuario"/>
    <alias name="" index="15" field="length_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="material_construcao" expression=""/>
    <default applyOnUpdate="0" field="modal_uso" expression=""/>
    <default applyOnUpdate="0" field="nr_faixas" expression=""/>
    <default applyOnUpdate="0" field="nr_pistas" expression=""/>
    <default applyOnUpdate="0" field="posicao_pista" expression=""/>
    <default applyOnUpdate="0" field="situacao_fisica" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression=""/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="material_construcao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="modal_uso" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nr_faixas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nr_pistas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="posicao_pista" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacao_fisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="material_construcao" desc=""/>
    <constraint exp="" field="modal_uso" desc=""/>
    <constraint exp="" field="nr_faixas" desc=""/>
    <constraint exp="" field="nr_pistas" desc=""/>
    <constraint exp="" field="posicao_pista" desc=""/>
    <constraint exp="" field="situacao_fisica" desc=""/>
    <constraint exp="" field="tipo_comprovacao" desc=""/>
    <constraint exp="" field="tipo_insumo" desc=""/>
    <constraint exp="" field="observacao" desc=""/>
    <constraint exp="" field="data_modificacao" desc=""/>
    <constraint exp="" field="controle_id" desc=""/>
    <constraint exp="" field="ultimo_usuario" desc=""/>
    <constraint exp="" field="length_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns/>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable/>
  <labelOnTop/>
  <widgets/>
  <previewExpression></previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
