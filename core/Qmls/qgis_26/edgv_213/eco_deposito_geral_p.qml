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
          <prop v="232,113,141,255" k="color"/>
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
    <field name="tipodepgeral">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="32" type="QString" name="Armazém"/>
              <Option value="10" type="QString" name="Composteira"/>
              <Option value="11" type="QString" name="Depósito frigorífico"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="8" type="QString" name="Galpão"/>
              <Option value="99" type="QString" name="Outros"/>
              <Option value="19" type="QString" name="Reservatório de Combustível"/>
              <Option value="9" type="QString" name="Silo"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="matconstr">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="1" type="QString" name="Alvenaria"/>
              <Option value="2" type="QString" name="Concreto"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="5" type="QString" name="Madeira"/>
              <Option value="3" type="QString" name="Metal"/>
              <Option value="97" type="QString" name="Não Aplicável"/>
              <Option value="99" type="QString" name="Outros"/>
              <Option value="4" type="QString" name="Rocha"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoexposicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="4" type="QString" name="Coberto"/>
              <Option value="5" type="QString" name="Céu aberto"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="3" type="QString" name="Fechado"/>
              <Option value="99" type="QString" name="Outros"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoprodutoresiduo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="25" type="QString" name="Bauxita"/>
              <Option value="33" type="QString" name="Carvão"/>
              <Option value="18" type="QString" name="Cascalho"/>
              <Option value="32" type="QString" name="Cobre"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="36" type="QString" name="Escória"/>
              <Option value="17" type="QString" name="Estrume"/>
              <Option value="35" type="QString" name="Ferro"/>
              <Option value="21" type="QString" name="Folhagens"/>
              <Option value="41" type="QString" name="Forragem"/>
              <Option value="29" type="QString" name="Gasolina"/>
              <Option value="23" type="QString" name="Granito"/>
              <Option value="6" type="QString" name="Grãos"/>
              <Option value="5" type="QString" name="Gás"/>
              <Option value="20" type="QString" name="Inseticida"/>
              <Option value="26" type="QString" name="Manganês"/>
              <Option value="98" type="QString" name="Misto"/>
              <Option value="24" type="QString" name="Mármore"/>
              <Option value="99" type="QString" name="Outros"/>
              <Option value="22" type="QString" name="Pedra"/>
              <Option value="3" type="QString" name="Petróleo"/>
              <Option value="31" type="QString" name="Querosene"/>
              <Option value="34" type="QString" name="Sal"/>
              <Option value="19" type="QString" name="Semente"/>
              <Option value="27" type="QString" name="Talco"/>
              <Option value="16" type="QString" name="Vinhoto"/>
              <Option value="30" type="QString" name="Álcool"/>
              <Option value="28" type="QString" name="Óleo diesel"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoconteudo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="1" type="QString" name="Insumo"/>
              <Option value="2" type="QString" name="Produto"/>
              <Option value="3" type="QString" name="Resíduo"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="unidadevolume">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="1" type="QString" name="Litro"/>
              <Option value="2" type="QString" name="Metro cúbico"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="valorvolume">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tratamento">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Não"/>
              <Option value="97" type="QString" name="Não aplicável"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_org_comerc_serv">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_org_ext_mineral">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_org_agropec_ext_veg_pesca">
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
    <field name="id_estrut_transporte">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_org_industrial">
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
    <alias field="operacional" index="4" name=""/>
    <alias field="situacaofisica" index="5" name=""/>
    <alias field="tipodepgeral" index="6" name=""/>
    <alias field="matconstr" index="7" name=""/>
    <alias field="tipoexposicao" index="8" name=""/>
    <alias field="tipoprodutoresiduo" index="9" name=""/>
    <alias field="tipoconteudo" index="10" name=""/>
    <alias field="unidadevolume" index="11" name=""/>
    <alias field="valorvolume" index="12" name=""/>
    <alias field="tratamento" index="13" name=""/>
    <alias field="id_org_comerc_serv" index="14" name=""/>
    <alias field="id_org_ext_mineral" index="15" name=""/>
    <alias field="id_org_agropec_ext_veg_pesca" index="16" name=""/>
    <alias field="id_complexo_gerad_energ_eletr" index="17" name=""/>
    <alias field="id_estrut_transporte" index="18" name=""/>
    <alias field="id_org_industrial" index="19" name=""/>
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
    <default applyOnUpdate="0" field="tipodepgeral" expression=""/>
    <default applyOnUpdate="0" field="matconstr" expression=""/>
    <default applyOnUpdate="0" field="tipoexposicao" expression=""/>
    <default applyOnUpdate="0" field="tipoprodutoresiduo" expression=""/>
    <default applyOnUpdate="0" field="tipoconteudo" expression=""/>
    <default applyOnUpdate="0" field="unidadevolume" expression=""/>
    <default applyOnUpdate="0" field="valorvolume" expression=""/>
    <default applyOnUpdate="0" field="tratamento" expression=""/>
    <default applyOnUpdate="0" field="id_org_comerc_serv" expression=""/>
    <default applyOnUpdate="0" field="id_org_ext_mineral" expression=""/>
    <default applyOnUpdate="0" field="id_org_agropec_ext_veg_pesca" expression=""/>
    <default applyOnUpdate="0" field="id_complexo_gerad_energ_eletr" expression=""/>
    <default applyOnUpdate="0" field="id_estrut_transporte" expression=""/>
    <default applyOnUpdate="0" field="id_org_industrial" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="operacional" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipodepgeral" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="matconstr" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipoexposicao" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipoprodutoresiduo" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipoconteudo" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="unidadevolume" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="valorvolume" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="tratamento" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="id_org_comerc_serv" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_org_ext_mineral" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_org_agropec_ext_veg_pesca" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_complexo_gerad_energ_eletr" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_estrut_transporte" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_org_industrial" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="operacional"/>
    <constraint exp="" desc="" field="situacaofisica"/>
    <constraint exp="" desc="" field="tipodepgeral"/>
    <constraint exp="" desc="" field="matconstr"/>
    <constraint exp="" desc="" field="tipoexposicao"/>
    <constraint exp="" desc="" field="tipoprodutoresiduo"/>
    <constraint exp="" desc="" field="tipoconteudo"/>
    <constraint exp="" desc="" field="unidadevolume"/>
    <constraint exp="" desc="" field="valorvolume"/>
    <constraint exp="" desc="" field="tratamento"/>
    <constraint exp="" desc="" field="id_org_comerc_serv"/>
    <constraint exp="" desc="" field="id_org_ext_mineral"/>
    <constraint exp="" desc="" field="id_org_agropec_ext_veg_pesca"/>
    <constraint exp="" desc="" field="id_complexo_gerad_energ_eletr"/>
    <constraint exp="" desc="" field="id_estrut_transporte"/>
    <constraint exp="" desc="" field="id_org_industrial"/>
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
