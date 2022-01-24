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
          <prop k="line_color" v="152,125,183,255"/>
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
            <Option name="map" type="Map">
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Elevado" type="QString" value="3"/>
              <Option name="Subterrâneo" type="QString" value="6"/>
              <Option name="Superfície" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipotrechoferrov">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Aeromóvel" type="QString" value="6"/>
              <Option name="Bonde" type="QString" value="5"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Ferrovia" type="QString" value="7"/>
              <Option name="Metrovia" type="QString" value="8"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bitola">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Internacional" type="QString" value="2"/>
              <Option name="Larga" type="QString" value="3"/>
              <Option name="Mista Internacional Larga" type="QString" value="6"/>
              <Option name="Mista Métrica Internacional" type="QString" value="4"/>
              <Option name="Mista Métrica Larga" type="QString" value="5"/>
              <Option name="Métrica" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="eletrificada">
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
    <field name="nrlinhas">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Dupla" type="QString" value="2"/>
              <Option name="Múltipla" type="QString" value="3"/>
              <Option name="Simples" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="emarruamento">
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
    <field name="jurisdicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Estadual" type="QString" value="2"/>
              <Option name="Federal" type="QString" value="1"/>
              <Option name="Municipal" type="QString" value="3"/>
              <Option name="Particular" type="QString" value="6"/>
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
              <Option name="Federal" type="QString" value="1"/>
              <Option name="Municipal" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
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
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="codtrechoferrov"/>
    <alias name="" index="5" field="posicaorelativa"/>
    <alias name="" index="6" field="tipotrechoferrov"/>
    <alias name="" index="7" field="bitola"/>
    <alias name="" index="8" field="eletrificada"/>
    <alias name="" index="9" field="nrlinhas"/>
    <alias name="" index="10" field="emarruamento"/>
    <alias name="" index="11" field="jurisdicao"/>
    <alias name="" index="12" field="administracao"/>
    <alias name="" index="13" field="concessionaria"/>
    <alias name="" index="14" field="operacional"/>
    <alias name="" index="15" field="situacaofisica"/>
    <alias name="" index="16" field="cargasuportmaxima"/>
    <alias name="" index="17" field="id_via_ferrea"/>
    <alias name="" index="18" field="length_otf"/>
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
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="codtrechoferrov" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="posicaorelativa" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipotrechoferrov" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="bitola" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="eletrificada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="nrlinhas" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="emarruamento" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="jurisdicao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="administracao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="concessionaria" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="cargasuportmaxima" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_via_ferrea" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="codtrechoferrov" desc=""/>
    <constraint exp="" field="posicaorelativa" desc=""/>
    <constraint exp="" field="tipotrechoferrov" desc=""/>
    <constraint exp="" field="bitola" desc=""/>
    <constraint exp="" field="eletrificada" desc=""/>
    <constraint exp="" field="nrlinhas" desc=""/>
    <constraint exp="" field="emarruamento" desc=""/>
    <constraint exp="" field="jurisdicao" desc=""/>
    <constraint exp="" field="administracao" desc=""/>
    <constraint exp="" field="concessionaria" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="cargasuportmaxima" desc=""/>
    <constraint exp="" field="id_via_ferrea" desc=""/>
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
