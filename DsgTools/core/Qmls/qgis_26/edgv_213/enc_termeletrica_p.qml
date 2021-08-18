<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" simplifyDrawingHints="0" readOnly="0" simplifyDrawingTol="1" version="3.7.0-Master" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" minScale="1e+8" simplifyLocal="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="marker" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" locked="0" enabled="1" class="SimpleMarker">
          <prop v="0" k="angle"/>
          <prop v="196,60,57,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="circle" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="35,35,35,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="diameter" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
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
    <field name="tipocombustivel">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="33" type="QString" name="Carvão"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="3" type="QString" name="Diesel"/>
              <Option value="5" type="QString" name="Gás"/>
              <Option value="98" type="QString" name="Misto"/>
              <Option value="1" type="QString" name="Nuclear"/>
              <Option value="99" type="QString" name="Outros"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="combrenovavel">
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
    <field name="tipomaqtermica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="3" type="QString" name="Ciclo combinado (CLCB)"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="4" type="QString" name="Motor de Combustão Interna (NCIA)"/>
              <Option value="1" type="QString" name="Turbina à gás (TBGS)"/>
              <Option value="2" type="QString" name="Turbina à vapor (TBVP)"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="geracao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="2" type="QString" name="CoGeração"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="1" type="QString" name="Eletricidade - GER 0"/>
            </Option>
          </Option>
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
    <alias field="tipocombustivel" index="12" name=""/>
    <alias field="combrenovavel" index="13" name=""/>
    <alias field="tipomaqtermica" index="14" name=""/>
    <alias field="geracao" index="15" name=""/>
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
    <default applyOnUpdate="0" field="tipocombustivel" expression=""/>
    <default applyOnUpdate="0" field="combrenovavel" expression=""/>
    <default applyOnUpdate="0" field="tipomaqtermica" expression=""/>
    <default applyOnUpdate="0" field="geracao" expression=""/>
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
    <constraint unique_strength="0" field="tipocombustivel" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="combrenovavel" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipomaqtermica" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="geracao" constraints="1" exp_strength="0" notnull_strength="1"/>
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
    <constraint exp="" desc="" field="tipocombustivel"/>
    <constraint exp="" desc="" field="combrenovavel"/>
    <constraint exp="" desc="" field="tipomaqtermica"/>
    <constraint exp="" desc="" field="geracao"/>
  </constraintExpressions>
  <expressionfields/>
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
