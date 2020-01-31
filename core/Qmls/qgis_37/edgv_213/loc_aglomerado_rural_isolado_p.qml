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
          <prop k="color" v="213,180,60,255"/>
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
    <field name="geocodigo">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="identificador">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="latitude">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="latitude_gms">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="longitude">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="longitude_gms">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipoaglomrurisol">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Aglomerado Rural Isolado - Núcleo" type="QString" value="6"/>
              <Option name="Aglomerado Rural Isolado - Povoado" type="QString" value="5"/>
              <Option name="Outros Aglomerados Rurais Isolados" type="QString" value="7"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="geocodigo"/>
    <alias name="" index="5" field="identificador"/>
    <alias name="" index="6" field="latitude"/>
    <alias name="" index="7" field="latitude_gms"/>
    <alias name="" index="8" field="longitude"/>
    <alias name="" index="9" field="longitude_gms"/>
    <alias name="" index="10" field="tipoaglomrurisol"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="geocodigo" expression=""/>
    <default applyOnUpdate="0" field="identificador" expression=""/>
    <default applyOnUpdate="0" field="latitude" expression=""/>
    <default applyOnUpdate="0" field="latitude_gms" expression=""/>
    <default applyOnUpdate="0" field="longitude" expression=""/>
    <default applyOnUpdate="0" field="longitude_gms" expression=""/>
    <default applyOnUpdate="0" field="tipoaglomrurisol" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="geocodigo" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="identificador" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="latitude" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="latitude_gms" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="longitude" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="longitude_gms" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipoaglomrurisol" constraints="1" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="geocodigo" desc=""/>
    <constraint exp="" field="identificador" desc=""/>
    <constraint exp="" field="latitude" desc=""/>
    <constraint exp="" field="latitude_gms" desc=""/>
    <constraint exp="" field="longitude" desc=""/>
    <constraint exp="" field="longitude_gms" desc=""/>
    <constraint exp="" field="tipoaglomrurisol" desc=""/>
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
