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
    <field name="coincidecomdentrode">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Barragem" type="QString" value="19"/>
              <Option name="Canal" type="QString" value="2"/>
              <Option name="Corredeira" type="QString" value="13"/>
              <Option name="Eclusa" type="QString" value="14"/>
              <Option name="Foz marítima" type="QString" value="16"/>
              <Option name="Laguna" type="QString" value="9"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Queda d´água" type="QString" value="12"/>
              <Option name="Represa/açude" type="QString" value="10"/>
              <Option name="Rio" type="QString" value="1"/>
              <Option name="Terreno sujeito a inundação" type="QString" value="15"/>
              <Option name="Vala" type="QString" value="11"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dentrodepoligono">
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
    <field name="compartilhado">
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
    <field name="eixoprincipal">
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
    <field name="navegabilidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Navegável" type="QString" value="1"/>
              <Option name="Não navegável" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="caladomax">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="regime">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Permanente" type="QString" value="1"/>
              <Option name="Permanente com grande variação" type="QString" value="2"/>
              <Option name="Seco" type="QString" value="5"/>
              <Option name="Temporário" type="QString" value="3"/>
              <Option name="Temporário com leito permanente" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="larguramedia">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="velocidademedcorrente">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="profundidademedia">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_trecho_curso_dagua">
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
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="coincidecomdentrode"/>
    <alias name="" index="5" field="dentrodepoligono"/>
    <alias name="" index="6" field="compartilhado"/>
    <alias name="" index="7" field="eixoprincipal"/>
    <alias name="" index="8" field="navegabilidade"/>
    <alias name="" index="9" field="caladomax"/>
    <alias name="" index="10" field="regime"/>
    <alias name="" index="11" field="larguramedia"/>
    <alias name="" index="12" field="velocidademedcorrente"/>
    <alias name="" index="13" field="profundidademedia"/>
    <alias name="" index="14" field="id_trecho_curso_dagua"/>
    <alias name="" index="15" field="lenght_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="coincidecomdentrode" expression=""/>
    <default applyOnUpdate="0" field="dentrodepoligono" expression=""/>
    <default applyOnUpdate="0" field="compartilhado" expression=""/>
    <default applyOnUpdate="0" field="eixoprincipal" expression=""/>
    <default applyOnUpdate="0" field="navegabilidade" expression=""/>
    <default applyOnUpdate="0" field="caladomax" expression=""/>
    <default applyOnUpdate="0" field="regime" expression=""/>
    <default applyOnUpdate="0" field="larguramedia" expression=""/>
    <default applyOnUpdate="0" field="velocidademedcorrente" expression=""/>
    <default applyOnUpdate="0" field="profundidademedia" expression=""/>
    <default applyOnUpdate="0" field="id_trecho_curso_dagua" expression=""/>
    <default applyOnUpdate="0" field="lenght_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="coincidecomdentrode" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="dentrodepoligono" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="compartilhado" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="eixoprincipal" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="navegabilidade" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="caladomax" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="regime" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="larguramedia" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="velocidademedcorrente" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="profundidademedia" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_trecho_curso_dagua" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="lenght_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="coincidecomdentrode" desc=""/>
    <constraint exp="" field="dentrodepoligono" desc=""/>
    <constraint exp="" field="compartilhado" desc=""/>
    <constraint exp="" field="eixoprincipal" desc=""/>
    <constraint exp="" field="navegabilidade" desc=""/>
    <constraint exp="" field="caladomax" desc=""/>
    <constraint exp="" field="regime" desc=""/>
    <constraint exp="" field="larguramedia" desc=""/>
    <constraint exp="" field="velocidademedcorrente" desc=""/>
    <constraint exp="" field="profundidademedia" desc=""/>
    <constraint exp="" field="id_trecho_curso_dagua" desc=""/>
    <constraint exp="" field="lenght_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="lenght_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
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
