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
          <prop v="133,182,111,255" k="line_color"/>
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
    <field name="codtrechoferrov">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="posicaorelativa">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="3" type="QString" name="Elevado"/>
              <Option value="6" type="QString" name="Subterrâneo"/>
              <Option value="2" type="QString" name="Superfície"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipotrechoferrov">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="6" type="QString" name="Aeromóvel"/>
              <Option value="5" type="QString" name="Bonde"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="7" type="QString" name="Ferrovia"/>
              <Option value="8" type="QString" name="Metrovia"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bitola">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Internacional"/>
              <Option value="3" type="QString" name="Larga"/>
              <Option value="6" type="QString" name="Mista Internacional Larga"/>
              <Option value="4" type="QString" name="Mista Métrica Internacional"/>
              <Option value="5" type="QString" name="Mista Métrica Larga"/>
              <Option value="1" type="QString" name="Métrica"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="eletrificada">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nrlinhas">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Dupla"/>
              <Option value="3" type="QString" name="Múltipla"/>
              <Option value="1" type="QString" name="Simples"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="emarruamento">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
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
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="2" type="QString" name="Estadual"/>
              <Option value="1" type="QString" name="Federal"/>
              <Option value="3" type="QString" name="Municipal"/>
              <Option value="6" type="QString" name="Particular"/>
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
              <Option value="7" type="QString" name="Concessionada"/>
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="2" type="QString" name="Estadual"/>
              <Option value="1" type="QString" name="Federal"/>
              <Option value="3" type="QString" name="Municipal"/>
              <Option value="97" type="QString" name="Não aplicável"/>
              <Option value="6" type="QString" name="Particular"/>
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
    <field name="operacional">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="2" type="QString" name="Não"/>
              <Option value="1" type="QString" name="Sim"/>
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
              <Option value="1" type="QString" name="Abandonada"/>
              <Option value="5" type="QString" name="Construída"/>
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="2" type="QString" name="Destruída"/>
              <Option value="3" type="QString" name="Em Construção"/>
              <Option value="4" type="QString" name="Planejada"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cargasuportmaxima">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id_via_ferrea">
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
    <alias field="id" index="0" name=""/>
    <alias field="nome" index="1" name=""/>
    <alias field="nomeabrev" index="2" name=""/>
    <alias field="geometriaaproximada" index="3" name=""/>
    <alias field="codtrechoferrov" index="4" name=""/>
    <alias field="posicaorelativa" index="5" name=""/>
    <alias field="tipotrechoferrov" index="6" name=""/>
    <alias field="bitola" index="7" name=""/>
    <alias field="eletrificada" index="8" name=""/>
    <alias field="nrlinhas" index="9" name=""/>
    <alias field="emarruamento" index="10" name=""/>
    <alias field="jurisdicao" index="11" name=""/>
    <alias field="administracao" index="12" name=""/>
    <alias field="concessionaria" index="13" name=""/>
    <alias field="operacional" index="14" name=""/>
    <alias field="situacaofisica" index="15" name=""/>
    <alias field="cargasuportmaxima" index="16" name=""/>
    <alias field="id_via_ferrea" index="17" name=""/>
    <alias field="lenght_otf" index="18" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="codtrechoferrov" expression=""/>
    <default applyOnUpdate="0" field="posicaorelativa" expression=""/>
    <default applyOnUpdate="0" field="tipotrechoferrov" expression=""/>
    <default applyOnUpdate="0" field="bitola" expression=""/>
    <default applyOnUpdate="0" field="eletrificada" expression=""/>
    <default applyOnUpdate="0" field="nrlinhas" expression=""/>
    <default applyOnUpdate="0" field="emarruamento" expression=""/>
    <default applyOnUpdate="0" field="jurisdicao" expression=""/>
    <default applyOnUpdate="0" field="administracao" expression=""/>
    <default applyOnUpdate="0" field="concessionaria" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="cargasuportmaxima" expression=""/>
    <default applyOnUpdate="0" field="id_via_ferrea" expression=""/>
    <default applyOnUpdate="0" field="lenght_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="codtrechoferrov" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="posicaorelativa" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipotrechoferrov" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="bitola" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="eletrificada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nrlinhas" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="emarruamento" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="jurisdicao" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="administracao" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="concessionaria" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="operacional" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="cargasuportmaxima" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="id_via_ferrea" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="lenght_otf" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="codtrechoferrov"/>
    <constraint exp="" desc="" field="posicaorelativa"/>
    <constraint exp="" desc="" field="tipotrechoferrov"/>
    <constraint exp="" desc="" field="bitola"/>
    <constraint exp="" desc="" field="eletrificada"/>
    <constraint exp="" desc="" field="nrlinhas"/>
    <constraint exp="" desc="" field="emarruamento"/>
    <constraint exp="" desc="" field="jurisdicao"/>
    <constraint exp="" desc="" field="administracao"/>
    <constraint exp="" desc="" field="concessionaria"/>
    <constraint exp="" desc="" field="operacional"/>
    <constraint exp="" desc="" field="situacaofisica"/>
    <constraint exp="" desc="" field="cargasuportmaxima"/>
    <constraint exp="" desc="" field="id_via_ferrea"/>
    <constraint exp="" desc="" field="lenght_otf"/>
  </constraintExpressions>
  <expressionfields>
    <field precision="0" comment="" length="0" typeName="" expression="$length" type="6" name="lenght_otf" subType="0"/>
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
