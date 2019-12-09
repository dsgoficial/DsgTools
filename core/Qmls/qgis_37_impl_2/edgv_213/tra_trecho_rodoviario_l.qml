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
          <prop k="line_color" v="145,82,45,255"/>
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
    <field name="codtrechorodov">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipotrechorod">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="1" name="Acesso"/>
              <Option type="QString" value="4" name="Auto-estrada"/>
              <Option type="QString" value="3" name="Caminho carroçável"/>
              <Option type="QString" value="2" name="Rodovia"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="jurisdicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="2" name="Estadual"/>
              <Option type="QString" value="11" name="Estadual/Municipal"/>
              <Option type="QString" value="1" name="Federal"/>
              <Option type="QString" value="9" name="Federal/Estadual"/>
              <Option type="QString" value="12" name="Federal/Estadual/Municipal"/>
              <Option type="QString" value="10" name="Federal/Municipal"/>
              <Option type="QString" value="3" name="Municipal"/>
              <Option type="QString" value="8" name="Propriedade particular"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="administracao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="7" name="Concessionada"/>
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="2" name="Estadual"/>
              <Option type="QString" value="11" name="Estadual/Municipal"/>
              <Option type="QString" value="1" name="Federal"/>
              <Option type="QString" value="9" name="Federal/Estadual"/>
              <Option type="QString" value="12" name="Federal/Estadual/Municipal"/>
              <Option type="QString" value="10" name="Federal/Municipal"/>
              <Option type="QString" value="3" name="Municipal"/>
              <Option type="QString" value="6" name="Particular"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="concessionaria">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="revestimento">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="4" name="Calçado"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="1" name="Leito natural"/>
              <Option type="QString" value="3" name="Pavimentado"/>
              <Option type="QString" value="2" name="Revestimento primário"/>
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
    <field name="nrpistas">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nrfaixas">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="trafego">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Periódico"/>
              <Option type="QString" value="1" name="Permanente"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="canteirodivisorio">
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
    <field name="id_via_rodoviaria">
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
    <alias field="geometriaaproximada" name="" index="1"/>
    <alias field="codtrechorodov" name="" index="2"/>
    <alias field="tipotrechorod" name="" index="3"/>
    <alias field="jurisdicao" name="" index="4"/>
    <alias field="administracao" name="" index="5"/>
    <alias field="concessionaria" name="" index="6"/>
    <alias field="revestimento" name="" index="7"/>
    <alias field="operacional" name="" index="8"/>
    <alias field="situacaofisica" name="" index="9"/>
    <alias field="nrpistas" name="" index="10"/>
    <alias field="nrfaixas" name="" index="11"/>
    <alias field="trafego" name="" index="12"/>
    <alias field="canteirodivisorio" name="" index="13"/>
    <alias field="id_via_rodoviaria" name="" index="14"/>
    <alias field="lenght_otf" name="" index="15"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="codtrechorodov" expression="" applyOnUpdate="0"/>
    <default field="tipotrechorod" expression="" applyOnUpdate="0"/>
    <default field="jurisdicao" expression="" applyOnUpdate="0"/>
    <default field="administracao" expression="" applyOnUpdate="0"/>
    <default field="concessionaria" expression="" applyOnUpdate="0"/>
    <default field="revestimento" expression="" applyOnUpdate="0"/>
    <default field="operacional" expression="" applyOnUpdate="0"/>
    <default field="situacaofisica" expression="" applyOnUpdate="0"/>
    <default field="nrpistas" expression="" applyOnUpdate="0"/>
    <default field="nrfaixas" expression="" applyOnUpdate="0"/>
    <default field="trafego" expression="" applyOnUpdate="0"/>
    <default field="canteirodivisorio" expression="" applyOnUpdate="0"/>
    <default field="id_via_rodoviaria" expression="" applyOnUpdate="0"/>
    <default field="lenght_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="codtrechorodov" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="tipotrechorod" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="jurisdicao" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="administracao" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="concessionaria" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="revestimento" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="operacional" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="situacaofisica" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="nrpistas" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nrfaixas" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="trafego" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="canteirodivisorio" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_via_rodoviaria" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="lenght_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="codtrechorodov" desc="" exp=""/>
    <constraint field="tipotrechorod" desc="" exp=""/>
    <constraint field="jurisdicao" desc="" exp=""/>
    <constraint field="administracao" desc="" exp=""/>
    <constraint field="concessionaria" desc="" exp=""/>
    <constraint field="revestimento" desc="" exp=""/>
    <constraint field="operacional" desc="" exp=""/>
    <constraint field="situacaofisica" desc="" exp=""/>
    <constraint field="nrpistas" desc="" exp=""/>
    <constraint field="nrfaixas" desc="" exp=""/>
    <constraint field="trafego" desc="" exp=""/>
    <constraint field="canteirodivisorio" desc="" exp=""/>
    <constraint field="id_via_rodoviaria" desc="" exp=""/>
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
