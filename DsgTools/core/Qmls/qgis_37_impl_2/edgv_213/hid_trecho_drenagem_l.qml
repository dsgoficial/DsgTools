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
    <field name="coincidecomdentrode">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="19" name="Barragem"/>
              <Option type="QString" value="2" name="Canal"/>
              <Option type="QString" value="13" name="Corredeira"/>
              <Option type="QString" value="14" name="Eclusa"/>
              <Option type="QString" value="16" name="Foz marítima"/>
              <Option type="QString" value="9" name="Laguna"/>
              <Option type="QString" value="97" name="Não aplicável"/>
              <Option type="QString" value="12" name="Queda d´água"/>
              <Option type="QString" value="10" name="Represa/açude"/>
              <Option type="QString" value="1" name="Rio"/>
              <Option type="QString" value="15" name="Terreno sujeito a inundação"/>
              <Option type="QString" value="11" name="Vala"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dentrodepoligono">
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
    <field name="compartilhado">
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
    <field name="eixoprincipal">
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
    <field name="navegabilidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="1" name="Navegável"/>
              <Option type="QString" value="2" name="Não navegável"/>
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
            <Option type="Map" name="map">
              <Option type="QString" value="1" name="Permanente"/>
              <Option type="QString" value="2" name="Permanente com grande variação"/>
              <Option type="QString" value="5" name="Seco"/>
              <Option type="QString" value="3" name="Temporário"/>
              <Option type="QString" value="4" name="Temporário com leito permanente"/>
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
    <field name="length_otf">
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
    <alias field="coincidecomdentrode" name="" index="4"/>
    <alias field="dentrodepoligono" name="" index="5"/>
    <alias field="compartilhado" name="" index="6"/>
    <alias field="eixoprincipal" name="" index="7"/>
    <alias field="navegabilidade" name="" index="8"/>
    <alias field="caladomax" name="" index="9"/>
    <alias field="regime" name="" index="10"/>
    <alias field="larguramedia" name="" index="11"/>
    <alias field="velocidademedcorrente" name="" index="12"/>
    <alias field="profundidademedia" name="" index="13"/>
    <alias field="id_trecho_curso_dagua" name="" index="14"/>
    <alias field="length_otf" name="" index="15"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="coincidecomdentrode" expression="" applyOnUpdate="0"/>
    <default field="dentrodepoligono" expression="" applyOnUpdate="0"/>
    <default field="compartilhado" expression="" applyOnUpdate="0"/>
    <default field="eixoprincipal" expression="" applyOnUpdate="0"/>
    <default field="navegabilidade" expression="" applyOnUpdate="0"/>
    <default field="caladomax" expression="" applyOnUpdate="0"/>
    <default field="regime" expression="" applyOnUpdate="0"/>
    <default field="larguramedia" expression="" applyOnUpdate="0"/>
    <default field="velocidademedcorrente" expression="" applyOnUpdate="0"/>
    <default field="profundidademedia" expression="" applyOnUpdate="0"/>
    <default field="id_trecho_curso_dagua" expression="" applyOnUpdate="0"/>
    <default field="length_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="coincidecomdentrode" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="dentrodepoligono" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="compartilhado" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="eixoprincipal" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="navegabilidade" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="caladomax" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="regime" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="larguramedia" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="velocidademedcorrente" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="profundidademedia" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="id_trecho_curso_dagua" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="length_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="coincidecomdentrode" desc="" exp=""/>
    <constraint field="dentrodepoligono" desc="" exp=""/>
    <constraint field="compartilhado" desc="" exp=""/>
    <constraint field="eixoprincipal" desc="" exp=""/>
    <constraint field="navegabilidade" desc="" exp=""/>
    <constraint field="caladomax" desc="" exp=""/>
    <constraint field="regime" desc="" exp=""/>
    <constraint field="larguramedia" desc="" exp=""/>
    <constraint field="velocidademedcorrente" desc="" exp=""/>
    <constraint field="profundidademedia" desc="" exp=""/>
    <constraint field="id_trecho_curso_dagua" desc="" exp=""/>
    <constraint field="length_otf" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields>
    <field expression="$length" type="6" typeName="" length="0" subType="0" precision="0" comment="" name="length_otf"/>
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
