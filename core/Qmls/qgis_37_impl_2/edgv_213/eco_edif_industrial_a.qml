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
          <prop k="color" v="125,139,143,255"/>
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
    <field name="operacional">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Não"/>
              <Option type="QString" value="1" name="Sim"/>
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
              <Option type="QString" value="1" name="Abandonada"/>
              <Option type="QString" value="5" name="Construída"/>
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="2" name="Destruída"/>
              <Option type="QString" value="3" name="Em Construção"/>
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
              <Option type="QString" value="1" name="Alvenaria"/>
              <Option type="QString" value="8" name="Cerca viva"/>
              <Option type="QString" value="2" name="Concreto"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="5" name="Madeira"/>
              <Option type="QString" value="3" name="Metal"/>
              <Option type="QString" value="97" name="Não Aplicável"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="4" name="Rocha"/>
              <Option type="QString" value="7" name="Tela ou Alambrado"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="chamine">
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
    <field name="tipodivisaocnae">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="18" name="Confecção de Artigos do Vestuário e Acessórios"/>
              <Option type="QString" value="45" name="Construção"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="22" name="Edição Impressão e Reprodução de Gravações"/>
              <Option type="QString" value="15" name="Fabricação Alimentícia e Bebidas"/>
              <Option type="QString" value="25" name="Fabricação de Artigos de Borracha e Material Plástico"/>
              <Option type="QString" value="21" name="Fabricação de Celulose Papel e Produtos de Papel"/>
              <Option type="QString" value="23" name="Fabricação de Coque Refino de Petróleo Elaboração de Combustíveis Nucleares e Produção de Álcool"/>
              <Option type="QString" value="33" name="Fabricação de Equipamentos de Instrumentação Médico-Hospitalares Instumentos de Precisão e Ópticos Equipamentos para Automação Industrial Cronômetros e Relógios"/>
              <Option type="QString" value="32" name="Fabricação de Material Eletrônicode Aparelhos e Equipamentos de Comunicações"/>
              <Option type="QString" value="31" name="Fabricação de Máquinas Aparelhos e Materiais Elétricos"/>
              <Option type="QString" value="30" name="Fabricação de Máquinas de Escritório e Equipamentos de Informática"/>
              <Option type="QString" value="29" name="Fabricação de Máquinas e Equipamentos"/>
              <Option type="QString" value="36" name="Fabricação de Móveis e Industrias Diversas"/>
              <Option type="QString" value="35" name="Fabricação de Outros Equipamentos de Transporte"/>
              <Option type="QString" value="24" name="Fabricação de Produtos Químicos"/>
              <Option type="QString" value="17" name="Fabricação de Produtos Têxteis"/>
              <Option type="QString" value="28" name="Fabricação de Produtos de Metal Exclusive Máquinas e Equipamentos"/>
              <Option type="QString" value="26" name="Fabricação de Produtos de Minerais Não-Metálicos"/>
              <Option type="QString" value="16" name="Fabricação de Produtos do Fumo"/>
              <Option type="QString" value="20" name="Fabricação de produtos de Madeira e Celulose"/>
              <Option type="QString" value="34" name="Fabricação e Montagem de Veículos Automotores Reboques e Carrocerias"/>
              <Option type="QString" value="27" name="Metalurgia Básica"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="19" name="Preparação de couros e Fabricação de Artefatos de Couro Artigos de Viagem e Calçados"/>
              <Option type="QString" value="37" name="Reciclagem"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id_org_industrial">
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
    <alias field="operacional" name="" index="4"/>
    <alias field="situacaofisica" name="" index="5"/>
    <alias field="matconstr" name="" index="6"/>
    <alias field="chamine" name="" index="7"/>
    <alias field="tipodivisaocnae" name="" index="8"/>
    <alias field="id_org_industrial" name="" index="9"/>
    <alias field="area_otf" name="" index="10"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="operacional" expression="" applyOnUpdate="0"/>
    <default field="situacaofisica" expression="" applyOnUpdate="0"/>
    <default field="matconstr" expression="" applyOnUpdate="0"/>
    <default field="chamine" expression="" applyOnUpdate="0"/>
    <default field="tipodivisaocnae" expression="" applyOnUpdate="0"/>
    <default field="id_org_industrial" expression="" applyOnUpdate="0"/>
    <default field="area_otf" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="operacional" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="situacaofisica" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="matconstr" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="chamine" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipodivisaocnae" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="id_org_industrial" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="area_otf" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="operacional" desc="" exp=""/>
    <constraint field="situacaofisica" desc="" exp=""/>
    <constraint field="matconstr" desc="" exp=""/>
    <constraint field="chamine" desc="" exp=""/>
    <constraint field="tipodivisaocnae" desc="" exp=""/>
    <constraint field="id_org_industrial" desc="" exp=""/>
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
