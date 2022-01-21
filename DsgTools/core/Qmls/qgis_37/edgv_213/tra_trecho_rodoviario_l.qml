<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="183,72,75,255"/>
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
            <Option name="map" type="Map">
              <Option name="Acesso" type="QString" value="1"/>
              <Option name="Auto-estrada" type="QString" value="4"/>
              <Option name="Caminho carroçável" type="QString" value="3"/>
              <Option name="Rodovia" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="jurisdicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Estadual" type="QString" value="2"/>
              <Option name="Estadual/Municipal" type="QString" value="11"/>
              <Option name="Federal" type="QString" value="1"/>
              <Option name="Federal/Estadual" type="QString" value="9"/>
              <Option name="Federal/Estadual/Municipal" type="QString" value="12"/>
              <Option name="Federal/Municipal" type="QString" value="10"/>
              <Option name="Municipal" type="QString" value="3"/>
              <Option name="Propriedade particular" type="QString" value="8"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="administracao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Concessionada" type="QString" value="7"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Estadual" type="QString" value="2"/>
              <Option name="Estadual/Municipal" type="QString" value="11"/>
              <Option name="Federal" type="QString" value="1"/>
              <Option name="Federal/Estadual" type="QString" value="9"/>
              <Option name="Federal/Estadual/Municipal" type="QString" value="12"/>
              <Option name="Federal/Municipal" type="QString" value="10"/>
              <Option name="Municipal" type="QString" value="3"/>
              <Option name="Particular" type="QString" value="6"/>
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
            <Option name="map" type="Map">
              <Option name="Calçado" type="QString" value="4"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Leito natural" type="QString" value="1"/>
              <Option name="Pavimentado" type="QString" value="3"/>
              <Option name="Revestimento primário" type="QString" value="2"/>
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
              <Option name="Planejada" type="QString" value="4"/>
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
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Periódico" type="QString" value="2"/>
              <Option name="Permanente" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="canteirodivisorio">
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
    <field name="id_via_rodoviaria">
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
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="geometriaaproximada"/>
    <alias name="" index="2" field="codtrechorodov"/>
    <alias name="" index="3" field="tipotrechorod"/>
    <alias name="" index="4" field="jurisdicao"/>
    <alias name="" index="5" field="administracao"/>
    <alias name="" index="6" field="concessionaria"/>
    <alias name="" index="7" field="revestimento"/>
    <alias name="" index="8" field="operacional"/>
    <alias name="" index="9" field="situacaofisica"/>
    <alias name="" index="10" field="nrpistas"/>
    <alias name="" index="11" field="nrfaixas"/>
    <alias name="" index="12" field="trafego"/>
    <alias name="" index="13" field="canteirodivisorio"/>
    <alias name="" index="14" field="id_via_rodoviaria"/>
    <alias name="" index="15" field="length_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="codtrechorodov" expression=""/>
    <default applyOnUpdate="0" field="tipotrechorod" expression=""/>
    <default applyOnUpdate="0" field="jurisdicao" expression=""/>
    <default applyOnUpdate="0" field="administracao" expression=""/>
    <default applyOnUpdate="0" field="concessionaria" expression=""/>
    <default applyOnUpdate="0" field="revestimento" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="nrpistas" expression=""/>
    <default applyOnUpdate="0" field="nrfaixas" expression=""/>
    <default applyOnUpdate="0" field="trafego" expression=""/>
    <default applyOnUpdate="0" field="canteirodivisorio" expression=""/>
    <default applyOnUpdate="0" field="id_via_rodoviaria" expression=""/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="codtrechorodov" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipotrechorod" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="jurisdicao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="administracao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="concessionaria" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="revestimento" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nrpistas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nrfaixas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="trafego" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="canteirodivisorio" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_via_rodoviaria" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="codtrechorodov" desc=""/>
    <constraint exp="" field="tipotrechorod" desc=""/>
    <constraint exp="" field="jurisdicao" desc=""/>
    <constraint exp="" field="administracao" desc=""/>
    <constraint exp="" field="concessionaria" desc=""/>
    <constraint exp="" field="revestimento" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="nrpistas" desc=""/>
    <constraint exp="" field="nrfaixas" desc=""/>
    <constraint exp="" field="trafego" desc=""/>
    <constraint exp="" field="canteirodivisorio" desc=""/>
    <constraint exp="" field="id_via_rodoviaria" desc=""/>
    <constraint exp="" field="length_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
  </expressionfields>
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
  <layerGeometryType>1</layerGeometryType>
</qgis>
