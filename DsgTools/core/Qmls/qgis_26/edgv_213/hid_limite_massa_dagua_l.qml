<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis maxScale="0" simplifyDrawingHints="0" readOnly="0" simplifyDrawingTol="1" version="3.7.0-Master" labelsEnabled="0" hasScaleBasedVisibilityFlag="0" styleCategories="AllStyleCategories" simplifyMaxScale="1" minScale="1e+8" simplifyLocal="1" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="line" name="0" clip_to_extent="1" force_rhr="0">
        <layer pass="0" locked="0" enabled="1" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="190,178,151,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.26" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
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
    <field name="tipolimmassa">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="1" type="QString" name="Costa visível da carta"/>
              <Option value="6" type="QString" name="Limite com elemento artificial"/>
              <Option value="7" type="QString" name="Limite interno com foz marítima"/>
              <Option value="5" type="QString" name="Limite interno entre massas e/ou trechos"/>
              <Option value="2" type="QString" name="Margem de massa d`água"/>
              <Option value="4" type="QString" name="Margem direita de trechos de massa d`água"/>
              <Option value="3" type="QString" name="Margem esquerda de trechos de massa d`água"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="materialpredominante">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="12" type="QString" name="Areia"/>
              <Option value="13" type="QString" name="Areia Fina"/>
              <Option value="15" type="QString" name="Argila"/>
              <Option value="18" type="QString" name="Cascalho"/>
              <Option value="21" type="QString" name="Concha"/>
              <Option value="20" type="QString" name="Coral"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="14" type="QString" name="Lama"/>
              <Option value="16" type="QString" name="Lodo"/>
              <Option value="98" type="QString" name="Misto"/>
              <Option value="97" type="QString" name="Não Aplicável"/>
              <Option value="50" type="QString" name="Pedra"/>
              <Option value="4" type="QString" name="Rocha"/>
              <Option value="19" type="QString" name="Seixo"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="alturamediamargem">
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
    <field name="length_otf">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" index="0" name=""/>
    <alias field="geometriaaproximada" index="1" name=""/>
    <alias field="tipolimmassa" index="2" name=""/>
    <alias field="materialpredominante" index="3" name=""/>
    <alias field="alturamediamargem" index="4" name=""/>
    <alias field="nomeabrev" index="5" name=""/>
    <alias field="length_otf" index="6" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="tipolimmassa" expression=""/>
    <default applyOnUpdate="0" field="materialpredominante" expression=""/>
    <default applyOnUpdate="0" field="alturamediamargem" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipolimmassa" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="materialpredominante" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="alturamediamargem" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="length_otf" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="tipolimmassa"/>
    <constraint exp="" desc="" field="materialpredominante"/>
    <constraint exp="" desc="" field="alturamediamargem"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="length_otf"/>
  </constraintExpressions>
  <expressionfields>
    <field precision="0" comment="" length="0" typeName="" expression="$length" type="6" name="length_otf" subType="0"/>
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
  <layerGeometryType>1</layerGeometryType>
</qgis>
