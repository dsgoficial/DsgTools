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
          <prop v="190,178,151,255" k="color"/>
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
    <field name="tipocemiterio">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="4" type="QString" name="Comum"/>
              <Option value="1" type="QString" name="Crematório"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="98" type="QString" name="Misto"/>
              <Option value="99" type="QString" name="Outros"/>
              <Option value="2" type="QString" name="Parque"/>
              <Option value="5" type="QString" name="Túmulo Isolado"/>
              <Option value="3" type="QString" name="Vertical"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="denominacaoassociada">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="5" type="QString" name="Cristã"/>
              <Option value="6" type="QString" name="Israelita"/>
              <Option value="7" type="QString" name="Muçulmana"/>
              <Option value="99" type="QString" name="Outras"/>
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
    <alias field="tipocemiterio" index="4" name=""/>
    <alias field="denominacaoassociada" index="5" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="tipocemiterio" expression=""/>
    <default applyOnUpdate="0" field="denominacaoassociada" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipocemiterio" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="denominacaoassociada" constraints="1" exp_strength="0" notnull_strength="1"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="tipocemiterio"/>
    <constraint exp="" desc="" field="denominacaoassociada"/>
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
