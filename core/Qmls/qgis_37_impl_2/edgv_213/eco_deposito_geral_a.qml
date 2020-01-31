<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyMaxScale="1" simplifyDrawingHints="0" simplifyLocal="1" version="3.7.0-Master" simplifyAlgorithm="0" styleCategories="AllStyleCategories" minScale="1e+8" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol type="fill" clip_to_extent="1" alpha="1" name="0" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleFill" locked="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="225,89,137,255"/>
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
              <Option type="QString" value="" name="name"/>
              <Option name="properties"/>
              <Option type="QString" value="collection" name="type"/>
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
            <Option type="Map" name="map">
              <Option type="QString" value="2" name="Não"/>
              <Option type="QString" value="1" name="Sim"/>
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
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Não"/>
              <Option type="QString" value="1" name="Sim"/>
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
              <Option type="QString" value="1" name="Abandonada"/>
              <Option type="QString" value="5" name="Construída"/>
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="2" name="Destruída"/>
              <Option type="QString" value="3" name="Em Construção"/>
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
              <Option type="QString" value="32" name="Armazém"/>
              <Option type="QString" value="10" name="Composteira"/>
              <Option type="QString" value="11" name="Depósito frigorífico"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="8" name="Galpão"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="19" name="Reservatório de Combustível"/>
              <Option type="QString" value="9" name="Silo"/>
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
              <Option type="QString" value="1" name="Alvenaria"/>
              <Option type="QString" value="2" name="Concreto"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="5" name="Madeira"/>
              <Option type="QString" value="3" name="Metal"/>
              <Option type="QString" value="97" name="Não Aplicável"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="4" name="Rocha"/>
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
              <Option type="QString" value="4" name="Coberto"/>
              <Option type="QString" value="5" name="Céu aberto"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="3" name="Fechado"/>
              <Option type="QString" value="99" name="Outros"/>
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
              <Option type="QString" value="25" name="Bauxita"/>
              <Option type="QString" value="33" name="Carvão"/>
              <Option type="QString" value="18" name="Cascalho"/>
              <Option type="QString" value="32" name="Cobre"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="36" name="Escória"/>
              <Option type="QString" value="17" name="Estrume"/>
              <Option type="QString" value="35" name="Ferro"/>
              <Option type="QString" value="21" name="Folhagens"/>
              <Option type="QString" value="41" name="Forragem"/>
              <Option type="QString" value="29" name="Gasolina"/>
              <Option type="QString" value="23" name="Granito"/>
              <Option type="QString" value="6" name="Grãos"/>
              <Option type="QString" value="5" name="Gás"/>
              <Option type="QString" value="20" name="Inseticida"/>
              <Option type="QString" value="26" name="Manganês"/>
              <Option type="QString" value="98" name="Misto"/>
              <Option type="QString" value="24" name="Mármore"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="22" name="Pedra"/>
              <Option type="QString" value="3" name="Petróleo"/>
              <Option type="QString" value="31" name="Querosene"/>
              <Option type="QString" value="34" name="Sal"/>
              <Option type="QString" value="19" name="Semente"/>
              <Option type="QString" value="27" name="Talco"/>
              <Option type="QString" value="16" name="Vinhoto"/>
              <Option type="QString" value="30" name="Álcool"/>
              <Option type="QString" value="28" name="Óleo diesel"/>
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
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="1" name="Insumo"/>
              <Option type="QString" value="2" name="Produto"/>
              <Option type="QString" value="3" name="Resíduo"/>
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
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="1" name="Litro"/>
              <Option type="QString" value="2" name="Metro cúbico"/>
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
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Não"/>
              <Option type="QString" value="97" name="Não aplicável"/>
              <Option type="QString" value="1" name="Sim"/>
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
    <field name="area_otf">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" name="" index="0"/>
    <alias field="nome" name="" index="1"/>
    <alias field="nomeabrev" name="" index="2"/>
    <alias field="geometriaaproximada" name="" index="3"/>
    <alias field="operacional" name="" index="4"/>
    <alias field="situacaofisica" name="" index="5"/>
    <alias field="tipodepgeral" name="" index="6"/>
    <alias field="matconstr" name="" index="7"/>
    <alias field="tipoexposicao" name="" index="8"/>
    <alias field="tipoprodutoresiduo" name="" index="9"/>
    <alias field="tipoconteudo" name="" index="10"/>
    <alias field="unidadevolume" name="" index="11"/>
    <alias field="valorvolume" name="" index="12"/>
    <alias field="tratamento" name="" index="13"/>
    <alias field="id_org_comerc_serv" name="" index="14"/>
    <alias field="id_org_ext_mineral" name="" index="15"/>
    <alias field="id_org_agropec_ext_veg_pesca" name="" index="16"/>
    <alias field="id_complexo_gerad_energ_eletr" name="" index="17"/>
    <alias field="id_estrut_transporte" name="" index="18"/>
    <alias field="id_org_industrial" name="" index="19"/>
    <alias field="area_otf" name="" index="20"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="operacional" expression="" applyOnUpdate="0"/>
    <default field="situacaofisica" expression="" applyOnUpdate="0"/>
    <default field="tipodepgeral" expression="" applyOnUpdate="0"/>
    <default field="matconstr" expression="" applyOnUpdate="0"/>
    <default field="tipoexposicao" expression="" applyOnUpdate="0"/>
    <default field="tipoprodutoresiduo" expression="" applyOnUpdate="0"/>
    <default field="tipoconteudo" expression="" applyOnUpdate="0"/>
    <default field="unidadevolume" expression="" applyOnUpdate="0"/>
    <default field="valorvolume" expression="" applyOnUpdate="0"/>
    <default field="tratamento" expression="" applyOnUpdate="0"/>
    <default field="id_org_comerc_serv" expression="" applyOnUpdate="0"/>
    <default field="id_org_ext_mineral" expression="" applyOnUpdate="0"/>
    <default field="id_org_agropec_ext_veg_pesca" expression="" applyOnUpdate="0"/>
    <default field="id_complexo_gerad_energ_eletr" expression="" applyOnUpdate="0"/>
    <default field="id_estrut_transporte" expression="" applyOnUpdate="0"/>
    <default field="id_org_industrial" expression="" applyOnUpdate="0"/>
    <default field="area_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="operacional" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="situacaofisica" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipodepgeral" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="matconstr" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipoexposicao" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipoprodutoresiduo" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipoconteudo" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="unidadevolume" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="valorvolume" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="tratamento" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_org_comerc_serv" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_org_ext_mineral" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_org_agropec_ext_veg_pesca" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_complexo_gerad_energ_eletr" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_estrut_transporte" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_org_industrial" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="area_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="operacional" desc="" exp=""/>
    <constraint field="situacaofisica" desc="" exp=""/>
    <constraint field="tipodepgeral" desc="" exp=""/>
    <constraint field="matconstr" desc="" exp=""/>
    <constraint field="tipoexposicao" desc="" exp=""/>
    <constraint field="tipoprodutoresiduo" desc="" exp=""/>
    <constraint field="tipoconteudo" desc="" exp=""/>
    <constraint field="unidadevolume" desc="" exp=""/>
    <constraint field="valorvolume" desc="" exp=""/>
    <constraint field="tratamento" desc="" exp=""/>
    <constraint field="id_org_comerc_serv" desc="" exp=""/>
    <constraint field="id_org_ext_mineral" desc="" exp=""/>
    <constraint field="id_org_agropec_ext_veg_pesca" desc="" exp=""/>
    <constraint field="id_complexo_gerad_energ_eletr" desc="" exp=""/>
    <constraint field="id_estrut_transporte" desc="" exp=""/>
    <constraint field="id_org_industrial" desc="" exp=""/>
    <constraint field="area_otf" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field expression="$area" type="6" typeName="" length="0" subType="0" precision="0" comment="" name="area_otf"/>
  </expressionfields>
  <attributeactions/>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
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
