<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="243,166,178,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
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
    <field name="tipodepgeral">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Armazém" type="QString" value="32"/>
              <Option name="Composteira" type="QString" value="10"/>
              <Option name="Depósito frigorífico" type="QString" value="11"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Galpão" type="QString" value="8"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Reservatório de Combustível" type="QString" value="19"/>
              <Option name="Silo" type="QString" value="9"/>
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
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não Aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Rocha" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoexposicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Coberto" type="QString" value="4"/>
              <Option name="Céu aberto" type="QString" value="5"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Fechado" type="QString" value="3"/>
              <Option name="Outros" type="QString" value="99"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoprodutoresiduo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Bauxita" type="QString" value="25"/>
              <Option name="Carvão" type="QString" value="33"/>
              <Option name="Cascalho" type="QString" value="18"/>
              <Option name="Cobre" type="QString" value="32"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Escória" type="QString" value="36"/>
              <Option name="Estrume" type="QString" value="17"/>
              <Option name="Ferro" type="QString" value="35"/>
              <Option name="Folhagens" type="QString" value="21"/>
              <Option name="Forragem" type="QString" value="41"/>
              <Option name="Gasolina" type="QString" value="29"/>
              <Option name="Granito" type="QString" value="23"/>
              <Option name="Grãos" type="QString" value="6"/>
              <Option name="Gás" type="QString" value="5"/>
              <Option name="Inseticida" type="QString" value="20"/>
              <Option name="Manganês" type="QString" value="26"/>
              <Option name="Misto" type="QString" value="98"/>
              <Option name="Mármore" type="QString" value="24"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Pedra" type="QString" value="22"/>
              <Option name="Petróleo" type="QString" value="3"/>
              <Option name="Querosene" type="QString" value="31"/>
              <Option name="Sal" type="QString" value="34"/>
              <Option name="Semente" type="QString" value="19"/>
              <Option name="Talco" type="QString" value="27"/>
              <Option name="Vinhoto" type="QString" value="16"/>
              <Option name="Álcool" type="QString" value="30"/>
              <Option name="Óleo diesel" type="QString" value="28"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoconteudo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Insumo" type="QString" value="1"/>
              <Option name="Produto" type="QString" value="2"/>
              <Option name="Resíduo" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="unidadevolume">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Litro" type="QString" value="1"/>
              <Option name="Metro cúbico" type="QString" value="2"/>
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
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Não" type="QString" value="2"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Sim" type="QString" value="1"/>
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
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="operacional"/>
    <alias name="" index="5" field="situacaofisica"/>
    <alias name="" index="6" field="tipodepgeral"/>
    <alias name="" index="7" field="matconstr"/>
    <alias name="" index="8" field="tipoexposicao"/>
    <alias name="" index="9" field="tipoprodutoresiduo"/>
    <alias name="" index="10" field="tipoconteudo"/>
    <alias name="" index="11" field="unidadevolume"/>
    <alias name="" index="12" field="valorvolume"/>
    <alias name="" index="13" field="tratamento"/>
    <alias name="" index="14" field="id_org_comerc_serv"/>
    <alias name="" index="15" field="id_org_ext_mineral"/>
    <alias name="" index="16" field="id_org_agropec_ext_veg_pesca"/>
    <alias name="" index="17" field="id_complexo_gerad_energ_eletr"/>
    <alias name="" index="18" field="id_estrut_transporte"/>
    <alias name="" index="19" field="id_org_industrial"/>
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
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipodepgeral" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="matconstr" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipoexposicao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipoprodutoresiduo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipoconteudo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="unidadevolume" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="valorvolume" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tratamento" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_comerc_serv" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_ext_mineral" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_agropec_ext_veg_pesca" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_complexo_gerad_energ_eletr" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_estrut_transporte" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_industrial" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="tipodepgeral" desc=""/>
    <constraint exp="" field="matconstr" desc=""/>
    <constraint exp="" field="tipoexposicao" desc=""/>
    <constraint exp="" field="tipoprodutoresiduo" desc=""/>
    <constraint exp="" field="tipoconteudo" desc=""/>
    <constraint exp="" field="unidadevolume" desc=""/>
    <constraint exp="" field="valorvolume" desc=""/>
    <constraint exp="" field="tratamento" desc=""/>
    <constraint exp="" field="id_org_comerc_serv" desc=""/>
    <constraint exp="" field="id_org_ext_mineral" desc=""/>
    <constraint exp="" field="id_org_agropec_ext_veg_pesca" desc=""/>
    <constraint exp="" field="id_complexo_gerad_energ_eletr" desc=""/>
    <constraint exp="" field="id_estrut_transporte" desc=""/>
    <constraint exp="" field="id_org_industrial" desc=""/>
  </constraintExpressions>
  <expressionfields/>
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
