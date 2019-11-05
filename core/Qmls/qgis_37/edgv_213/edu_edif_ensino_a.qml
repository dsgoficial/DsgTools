<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="fill" alpha="1" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="190,207,80,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
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
    <field name="nomeabrev">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="geometriaaproximada">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Não" type="QString" value="2"/>
              <Option name="Sim" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="operacional">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Não" type="QString" value="2"/>
              <Option name="Sim" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacaofisica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Abandonada" type="QString" value="1"/>
              <Option name="Construída" type="QString" value="5"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Destruída" type="QString" value="2"/>
              <Option name="Em Construção" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="matconstr">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Cerca viva" type="QString" value="8"/>
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não Aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Rocha" type="QString" value="4"/>
              <Option name="Tela ou Alambrado" type="QString" value="7"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoclassecnae">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="80.13-6 - Educação Infantil - Creche" type="QString" value="16"/>
              <Option name="80.14-4 - Educação Infantil - Pré-Escola" type="QString" value="17"/>
              <Option name="80.15-2 - Ensino Fundamental" type="QString" value="18"/>
              <Option name="80.20-9 - Ensino Médio" type="QString" value="19"/>
              <Option name="80.31-4 - Educação Superior - Graduação" type="QString" value="20"/>
              <Option name="80.32-2 - Educação Superior - Graduação e Pós-Graduação" type="QString" value="21"/>
              <Option name="80.33-0 - Educação Superior - Pós-Graduação e Extensão" type="QString" value="22"/>
              <Option name="80.96-9 - Educação Profissional de Nível Técnico" type="QString" value="23"/>
              <Option name="80.97-7 - Educação Profissional de Nível Tecnológico" type="QString" value="24"/>
              <Option name="80.99-3 - Outras Atividades de Ensino" type="QString" value="25"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Misto" type="QString" value="98"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_org_ensino">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="area_otf">
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
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="operacional"/>
    <alias name="" index="5" field="situacaofisica"/>
    <alias name="" index="6" field="matconstr"/>
    <alias name="" index="7" field="tipoclassecnae"/>
    <alias name="" index="8" field="id_org_ensino"/>
    <alias name="" index="9" field="area_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="matconstr" expression=""/>
    <default applyOnUpdate="0" field="tipoclassecnae" expression=""/>
    <default applyOnUpdate="0" field="id_org_ensino" expression=""/>
    <default applyOnUpdate="0" field="area_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="matconstr" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipoclassecnae" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_ensino" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="area_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="matconstr" desc=""/>
    <constraint exp="" field="tipoclassecnae" desc=""/>
    <constraint exp="" field="id_org_ensino" desc=""/>
    <constraint exp="" field="area_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="area_otf" typeName="" type="6" subType="0" length="0" expression="$area"/>
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
  <layerGeometryType>2</layerGeometryType>
</qgis>
