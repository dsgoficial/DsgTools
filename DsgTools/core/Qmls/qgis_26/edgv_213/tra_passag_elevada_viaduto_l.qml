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
          <prop v="225,89,137,255" k="line_color"/>
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
    <field name="tipopassagviad">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="5" type="QString" name="Passagem elevada"/>
              <Option value="6" type="QString" name="Viaduto"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="modaluso">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="9" type="QString" name="Aeroportuário"/>
              <Option value="5" type="QString" name="Ferroviário"/>
              <Option value="8" type="QString" name="Rodoferroviário"/>
              <Option value="4" type="QString" name="Rodoviário"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="matconstr">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="1" type="QString" name="Alvenaria"/>
              <Option value="2" type="QString" name="Concreto"/>
              <Option value="0" type="QString" name="Desconhecido"/>
              <Option value="5" type="QString" name="Madeira"/>
              <Option value="3" type="QString" name="Metal"/>
              <Option value="99" type="QString" name="Outros"/>
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
    <field name="vaolivrehoriz">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="vaovertical">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="gabhorizsup">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="gabvertsup">
      <editWidget type="">
        <config>
          <Option/>
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
    <field name="posicaopista">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option value="12" type="QString" name="Adjacentes"/>
              <Option value="0" type="QString" name="Desconhecida"/>
              <Option value="97" type="QString" name="Não Aplicável"/>
              <Option value="13" type="QString" name="Superpostas"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="extensao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="largura">
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
    <alias field="nome" index="1" name=""/>
    <alias field="nomeabrev" index="2" name=""/>
    <alias field="geometriaaproximada" index="3" name=""/>
    <alias field="tipopassagviad" index="4" name=""/>
    <alias field="modaluso" index="5" name=""/>
    <alias field="matconstr" index="6" name=""/>
    <alias field="operacional" index="7" name=""/>
    <alias field="situacaofisica" index="8" name=""/>
    <alias field="vaolivrehoriz" index="9" name=""/>
    <alias field="vaovertical" index="10" name=""/>
    <alias field="gabhorizsup" index="11" name=""/>
    <alias field="gabvertsup" index="12" name=""/>
    <alias field="cargasuportmaxima" index="13" name=""/>
    <alias field="nrpistas" index="14" name=""/>
    <alias field="nrfaixas" index="15" name=""/>
    <alias field="posicaopista" index="16" name=""/>
    <alias field="extensao" index="17" name=""/>
    <alias field="largura" index="18" name=""/>
    <alias field="length_otf" index="19" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="tipopassagviad" expression=""/>
    <default applyOnUpdate="0" field="modaluso" expression=""/>
    <default applyOnUpdate="0" field="matconstr" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="vaolivrehoriz" expression=""/>
    <default applyOnUpdate="0" field="vaovertical" expression=""/>
    <default applyOnUpdate="0" field="gabhorizsup" expression=""/>
    <default applyOnUpdate="0" field="gabvertsup" expression=""/>
    <default applyOnUpdate="0" field="cargasuportmaxima" expression=""/>
    <default applyOnUpdate="0" field="nrpistas" expression=""/>
    <default applyOnUpdate="0" field="nrfaixas" expression=""/>
    <default applyOnUpdate="0" field="posicaopista" expression=""/>
    <default applyOnUpdate="0" field="extensao" expression=""/>
    <default applyOnUpdate="0" field="largura" expression=""/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="id" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="nome" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="tipopassagviad" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="modaluso" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="matconstr" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="operacional" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="vaolivrehoriz" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="vaovertical" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="gabhorizsup" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="gabvertsup" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="cargasuportmaxima" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nrpistas" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="nrfaixas" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="posicaopista" constraints="1" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="extensao" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="largura" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="length_otf" constraints="0" exp_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="nome"/>
    <constraint exp="" desc="" field="nomeabrev"/>
    <constraint exp="" desc="" field="geometriaaproximada"/>
    <constraint exp="" desc="" field="tipopassagviad"/>
    <constraint exp="" desc="" field="modaluso"/>
    <constraint exp="" desc="" field="matconstr"/>
    <constraint exp="" desc="" field="operacional"/>
    <constraint exp="" desc="" field="situacaofisica"/>
    <constraint exp="" desc="" field="vaolivrehoriz"/>
    <constraint exp="" desc="" field="vaovertical"/>
    <constraint exp="" desc="" field="gabhorizsup"/>
    <constraint exp="" desc="" field="gabvertsup"/>
    <constraint exp="" desc="" field="cargasuportmaxima"/>
    <constraint exp="" desc="" field="nrpistas"/>
    <constraint exp="" desc="" field="nrfaixas"/>
    <constraint exp="" desc="" field="posicaopista"/>
    <constraint exp="" desc="" field="extensao"/>
    <constraint exp="" desc="" field="largura"/>
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
