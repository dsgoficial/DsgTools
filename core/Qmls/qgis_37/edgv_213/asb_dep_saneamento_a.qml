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
          <prop k="color" v="232,113,141,255"/>
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
    <field name="tipodepsaneam">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Aterro controlado" type="QString" value="6"/>
              <Option name="Aterro sanitário" type="QString" value="5"/>
              <Option name="Depósito de lixo" type="QString" value="4"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Tanque" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="construcao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Aberta" type="QString" value="2"/>
              <Option name="Fechada" type="QString" value="1"/>
              <Option name="Não aplicável" type="QString" value="97"/>
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
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não Aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Rocha" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="finalidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Armazenamento" type="QString" value="8"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Tratamento" type="QString" value="2"/>
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
    <field name="residuo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Líquido" type="QString" value="1"/>
              <Option name="Sólido" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tiporesiduo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Chorume" type="QString" value="15"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Esgoto" type="QString" value="9"/>
              <Option name="Lixo domiciliar e comercial" type="QString" value="12"/>
              <Option name="Lixo séptico" type="QString" value="14"/>
              <Option name="Lixo tóxico" type="QString" value="13"/>
              <Option name="Misto" type="QString" value="98"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Vinhoto" type="QString" value="16"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_complexo_saneamento">
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
    <alias name="" index="4" field="tipodepsaneam"/>
    <alias name="" index="5" field="construcao"/>
    <alias name="" index="6" field="matconstr"/>
    <alias name="" index="7" field="finalidade"/>
    <alias name="" index="8" field="operacional"/>
    <alias name="" index="9" field="situacaofisica"/>
    <alias name="" index="10" field="residuo"/>
    <alias name="" index="11" field="tiporesiduo"/>
    <alias name="" index="12" field="id_complexo_saneamento"/>
    <alias name="" index="13" field="area_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="tipodepsaneam" expression=""/>
    <default applyOnUpdate="0" field="construcao" expression=""/>
    <default applyOnUpdate="0" field="matconstr" expression=""/>
    <default applyOnUpdate="0" field="finalidade" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="residuo" expression=""/>
    <default applyOnUpdate="0" field="tiporesiduo" expression=""/>
    <default applyOnUpdate="0" field="id_complexo_saneamento" expression=""/>
    <default applyOnUpdate="0" field="area_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipodepsaneam" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="construcao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="matconstr" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="finalidade" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="residuo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tiporesiduo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_complexo_saneamento" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="area_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="tipodepsaneam" desc=""/>
    <constraint exp="" field="construcao" desc=""/>
    <constraint exp="" field="matconstr" desc=""/>
    <constraint exp="" field="finalidade" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="residuo" desc=""/>
    <constraint exp="" field="tiporesiduo" desc=""/>
    <constraint exp="" field="id_complexo_saneamento" desc=""/>
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
