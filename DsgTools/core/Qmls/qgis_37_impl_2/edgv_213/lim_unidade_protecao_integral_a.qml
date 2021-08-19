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
          <prop k="color" v="255,158,23,255"/>
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
    <field name="tipounidprotinteg">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="1" name="Estação Ecológica - ESEC"/>
              <Option type="QString" value="3" name="Monumento batural - MONA"/>
              <Option type="QString" value="2" name="Parque - PAR"/>
              <Option type="QString" value="5" name="Refúgio de Vida Silvestre - RVS"/>
              <Option type="QString" value="4" name="Reserva Biológica - REBIO"/>
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
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="5" name="Distrital"/>
              <Option type="QString" value="2" name="Estadual"/>
              <Option type="QString" value="1" name="Federal"/>
              <Option type="QString" value="3" name="Municipal"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="atolegal">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="areaoficial">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="anocriacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sigla">
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
    <alias field="tipounidprotinteg" name="" index="4"/>
    <alias field="administracao" name="" index="5"/>
    <alias field="atolegal" name="" index="6"/>
    <alias field="areaoficial" name="" index="7"/>
    <alias field="anocriacao" name="" index="8"/>
    <alias field="sigla" name="" index="9"/>
    <alias field="area_otf" name="" index="10"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="tipounidprotinteg" expression="" applyOnUpdate="0"/>
    <default field="administracao" expression="" applyOnUpdate="0"/>
    <default field="atolegal" expression="" applyOnUpdate="0"/>
    <default field="areaoficial" expression="" applyOnUpdate="0"/>
    <default field="anocriacao" expression="" applyOnUpdate="0"/>
    <default field="sigla" expression="" applyOnUpdate="0"/>
    <default field="area_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipounidprotinteg" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="administracao" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="atolegal" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="areaoficial" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="anocriacao" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="sigla" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="area_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="tipounidprotinteg" desc="" exp=""/>
    <constraint field="administracao" desc="" exp=""/>
    <constraint field="atolegal" desc="" exp=""/>
    <constraint field="areaoficial" desc="" exp=""/>
    <constraint field="anocriacao" desc="" exp=""/>
    <constraint field="sigla" desc="" exp=""/>
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
