<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyMaxScale="1" simplifyDrawingHints="0" simplifyLocal="1" version="3.7.0-Master" simplifyAlgorithm="0" styleCategories="AllStyleCategories" minScale="1e+8" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol type="line" clip_to_extent="1" alpha="1" name="0" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="125,139,143,255"/>
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
    <field name="tipotrechoduto">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="2" name="Calha"/>
              <Option type="QString" value="3" name="Correia transportadora"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="1" name="Duto"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="mattransp">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="8" name="Efluentes"/>
              <Option type="QString" value="9" name="Esgoto"/>
              <Option type="QString" value="29" name="Gasolina"/>
              <Option type="QString" value="6" name="Grãos"/>
              <Option type="QString" value="5" name="Gás"/>
              <Option type="QString" value="7" name="Minério"/>
              <Option type="QString" value="4" name="Nafta"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="3" name="Petróleo"/>
              <Option type="QString" value="31" name="Querosene"/>
              <Option type="QString" value="1" name="Água"/>
              <Option type="QString" value="30" name="Álcool"/>
              <Option type="QString" value="2" name="Óleo"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="setor">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="3" name="Abastecimento de água"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Econômico"/>
              <Option type="QString" value="1" name="Energético"/>
              <Option type="QString" value="4" name="Saneamento básico"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="posicaorelativa">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="3" name="Elevado"/>
              <Option type="QString" value="4" name="Emerso"/>
              <Option type="QString" value="5" name="Submerso"/>
              <Option type="QString" value="6" name="Subterrâneo"/>
              <Option type="QString" value="2" name="Superfície"/>
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
              <Option type="QString" value="3" name="Metal"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="4" name="Rocha"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="ndutos">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="situacaoespacial">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="12" name="Adjacentes"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="13" name="Superpostos"/>
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
              <Option type="QString" value="4" name="Planejada"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_duto">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipocondutor">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="2" name="Calha"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="4" name="Tubulação"/>
            </Option>
          </Option>
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
    <field name="lenght_otf">
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
    <alias field="tipotrechoduto" name="" index="4"/>
    <alias field="mattransp" name="" index="5"/>
    <alias field="setor" name="" index="6"/>
    <alias field="posicaorelativa" name="" index="7"/>
    <alias field="matconstr" name="" index="8"/>
    <alias field="ndutos" name="" index="9"/>
    <alias field="situacaoespacial" name="" index="10"/>
    <alias field="operacional" name="" index="11"/>
    <alias field="situacaofisica" name="" index="12"/>
    <alias field="id_duto" name="" index="13"/>
    <alias field="tipocondutor" name="" index="14"/>
    <alias field="id_complexo_gerad_energ_eletr" name="" index="15"/>
    <alias field="lenght_otf" name="" index="16"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="tipotrechoduto" expression="" applyOnUpdate="0"/>
    <default field="mattransp" expression="" applyOnUpdate="0"/>
    <default field="setor" expression="" applyOnUpdate="0"/>
    <default field="posicaorelativa" expression="" applyOnUpdate="0"/>
    <default field="matconstr" expression="" applyOnUpdate="0"/>
    <default field="ndutos" expression="" applyOnUpdate="0"/>
    <default field="situacaoespacial" expression="" applyOnUpdate="0"/>
    <default field="operacional" expression="" applyOnUpdate="0"/>
    <default field="situacaofisica" expression="" applyOnUpdate="0"/>
    <default field="id_duto" expression="" applyOnUpdate="0"/>
    <default field="tipocondutor" expression="" applyOnUpdate="0"/>
    <default field="id_complexo_gerad_energ_eletr" expression="" applyOnUpdate="0"/>
    <default field="lenght_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipotrechoduto" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="mattransp" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="setor" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="posicaorelativa" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="matconstr" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="ndutos" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="situacaoespacial" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="operacional" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="situacaofisica" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_duto" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="tipocondutor" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_complexo_gerad_energ_eletr" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="lenght_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="tipotrechoduto" desc="" exp=""/>
    <constraint field="mattransp" desc="" exp=""/>
    <constraint field="setor" desc="" exp=""/>
    <constraint field="posicaorelativa" desc="" exp=""/>
    <constraint field="matconstr" desc="" exp=""/>
    <constraint field="ndutos" desc="" exp=""/>
    <constraint field="situacaoespacial" desc="" exp=""/>
    <constraint field="operacional" desc="" exp=""/>
    <constraint field="situacaofisica" desc="" exp=""/>
    <constraint field="id_duto" desc="" exp=""/>
    <constraint field="tipocondutor" desc="" exp=""/>
    <constraint field="id_complexo_gerad_energ_eletr" desc="" exp=""/>
    <constraint field="lenght_otf" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field expression="$length" type="6" typeName="" length="0" subType="0" precision="0" comment="" name="lenght_otf"/>
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
  <layerGeometryType>1</layerGeometryType>
</qgis>
