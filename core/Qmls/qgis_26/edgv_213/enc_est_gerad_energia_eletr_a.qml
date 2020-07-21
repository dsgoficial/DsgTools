<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" simplifyDrawingHints="0" readOnly="0" simplifyDrawingTol="1" version="3.7.0-Master" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" minScale="1e+8" simplifyLocal="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="fill" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" locked="0" enabled="1" class="SimpleFill">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="183,72,75,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
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
      <Option value="" type="QString"/>
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
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoestgerad">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="5" type="QString" name="Eólica"/>
              <Option value="7" type="QString" name="Maré-motriz"/>
              <Option value="99" type="QString" name="Outros"/>
              <Option value="6" type="QString" name="Solar"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="operacional">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacaofisica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="1" type="QString" name="Abandonada"/>
              <Option value="5" type="QString" name="Construída"/>
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="2" type="QString" name="Destruída"/>
              <Option value="3" type="QString" name="Em Construção"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="destenergelet">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="Auto-Produção com Comercialização de Excedente (APE-COM)"/>
              <Option value="1" type="QString" name="Auto-Produção de Energia (APE)"/>
              <Option value="3" type="QString" name="Comercialização de Energia (COM)"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="4" type="QString" name="Produção Independente de Energia (PIE)"/>
              <Option value="5" type="QString" name="Serviço Público (SP)"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="codigoestacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="potenciaoutorgada">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="potenciafiscalizada">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_complexo_gerad_energ_eletr">
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
    <alias field="id" index="0" name=""/>
    <alias field="nome" index="1" name=""/>
    <alias field="nomeabrev" index="2" name=""/>
    <alias field="geometriaaproximada" index="3" name=""/>
    <alias field="tipoestgerad" index="4" name=""/>
    <alias field="operacional" index="5" name=""/>
    <alias field="situacaofisica" index="6" name=""/>
    <alias field="destenergelet" index="7" name=""/>
    <alias field="codigoestacao" index="8" name=""/>
    <alias field="potenciaoutorgada" index="9" name=""/>
    <alias field="potenciafiscalizada" index="10" name=""/>
    <alias field="id_complexo_gerad_energ_eletr" index="11" name=""/>
    <alias field="area_otf" index="12" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="tipoestgerad" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="destenergelet" expression=""/>
    <default applyOnUpdate="0" field="codigoestacao" expression=""/>
    <default applyOnUpdate="0" field="potenciaoutorgada" expression=""/>
    <default applyOnUpdate="0" field="potenciafiscalizada" expression=""/>
    <default applyOnUpdate="0" field="id_complexo_gerad_energ_eletr" expression=""/>
    <default applyOnUpdate="0" field="area_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipoestgerad" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="operacional" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="destenergelet" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="codigoestacao" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="potenciaoutorgada" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="potenciafiscalizada" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_complexo_gerad_energ_eletr" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="area_otf" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="tipoestgerad"/>
    <constraint exp="" desc="" field="operacional"/>
    <constraint exp="" desc="" field="situacaofisica"/>
    <constraint exp="" desc="" field="destenergelet"/>
    <constraint exp="" desc="" field="codigoestacao"/>
    <constraint exp="" desc="" field="potenciaoutorgada"/>
    <constraint exp="" desc="" field="potenciafiscalizada"/>
    <constraint exp="" desc="" field="id_complexo_gerad_energ_eletr"/>
    <constraint exp="" desc="" field="area_otf"/>
  </constraintExpressions>
  <expressionfields>
    <field precision="0" comment="" length="0" typeName="" expression="$area" type="6" name="area_otf" subType="0"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
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
