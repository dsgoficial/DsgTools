<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="singleSymbol" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="fill" alpha="1" clip_to_extent="1">
        <layer class="SimpleFill" enabled="1" pass="0" locked="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="255,158,23,255"/>
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
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="matconstr">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Cerca viva" type="QString" value="8"/>
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não Aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Rocha" type="QString" value="4"/>
              <Option name="Tela ou Alambrado" type="QString" value="7"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="chamine">
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
    <field name="tipodivisaocnae">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="Confecção de Artigos do Vestuário e Acessórios" type="QString" value="18"/>
              <Option name="Construção" type="QString" value="45"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Edição Impressão e Reprodução de Gravações" type="QString" value="22"/>
              <Option name="Fabricação Alimentícia e Bebidas" type="QString" value="15"/>
              <Option name="Fabricação de Artigos de Borracha e Material Plástico" type="QString" value="25"/>
              <Option name="Fabricação de Celulose Papel e Produtos de Papel" type="QString" value="21"/>
              <Option name="Fabricação de Coque Refino de Petróleo Elaboração de Combustíveis Nucleares e Produção de Álcool" type="QString" value="23"/>
              <Option name="Fabricação de Equipamentos de Instrumentação Médico-Hospitalares Instumentos de Precisão e Ópticos Equipamentos para Automação Industrial Cronômetros e Relógios" type="QString" value="33"/>
              <Option name="Fabricação de Material Eletrônicode Aparelhos e Equipamentos de Comunicações" type="QString" value="32"/>
              <Option name="Fabricação de Máquinas Aparelhos e Materiais Elétricos" type="QString" value="31"/>
              <Option name="Fabricação de Máquinas de Escritório e Equipamentos de Informática" type="QString" value="30"/>
              <Option name="Fabricação de Máquinas e Equipamentos" type="QString" value="29"/>
              <Option name="Fabricação de Móveis e Industrias Diversas" type="QString" value="36"/>
              <Option name="Fabricação de Outros Equipamentos de Transporte" type="QString" value="35"/>
              <Option name="Fabricação de Produtos Químicos" type="QString" value="24"/>
              <Option name="Fabricação de Produtos Têxteis" type="QString" value="17"/>
              <Option name="Fabricação de Produtos de Metal Exclusive Máquinas e Equipamentos" type="QString" value="28"/>
              <Option name="Fabricação de Produtos de Minerais Não-Metálicos" type="QString" value="26"/>
              <Option name="Fabricação de Produtos do Fumo" type="QString" value="16"/>
              <Option name="Fabricação de produtos de Madeira e Celulose" type="QString" value="20"/>
              <Option name="Fabricação e Montagem de Veículos Automotores Reboques e Carrocerias" type="QString" value="34"/>
              <Option name="Metalurgia Básica" type="QString" value="27"/>
              <Option name="Outros" type="QString" value="99"/>
              <Option name="Preparação de couros e Fabricação de Artefatos de Couro Artigos de Viagem e Calçados" type="QString" value="19"/>
              <Option name="Reciclagem" type="QString" value="37"/>
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
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="nomeabrev"/>
    <alias name="" index="3" field="geometriaaproximada"/>
    <alias name="" index="4" field="operacional"/>
    <alias name="" index="5" field="situacaofisica"/>
    <alias name="" index="6" field="matconstr"/>
    <alias name="" index="7" field="chamine"/>
    <alias name="" index="8" field="tipodivisaocnae"/>
    <alias name="" index="9" field="id_org_industrial"/>
    <alias name="" index="10" field="area_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="nomeabrev" expression=""/>
    <default applyOnUpdate="0" field="geometriaaproximada" expression=""/>
    <default applyOnUpdate="0" field="operacional" expression=""/>
    <default applyOnUpdate="0" field="situacaofisica" expression=""/>
    <default applyOnUpdate="0" field="matconstr" expression=""/>
    <default applyOnUpdate="0" field="chamine" expression=""/>
    <default applyOnUpdate="0" field="tipodivisaocnae" expression=""/>
    <default applyOnUpdate="0" field="id_org_industrial" expression=""/>
    <default applyOnUpdate="0" field="area_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nomeabrev" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="geometriaaproximada" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="operacional" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacaofisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="matconstr" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="chamine" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipodivisaocnae" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="id_org_industrial" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="area_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="nomeabrev" desc=""/>
    <constraint exp="" field="geometriaaproximada" desc=""/>
    <constraint exp="" field="operacional" desc=""/>
    <constraint exp="" field="situacaofisica" desc=""/>
    <constraint exp="" field="matconstr" desc=""/>
    <constraint exp="" field="chamine" desc=""/>
    <constraint exp="" field="tipodivisaocnae" desc=""/>
    <constraint exp="" field="id_org_industrial" desc=""/>
    <constraint exp="" field="area_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="area_otf" typeName="" type="6" subType="0" length="0" expression="$area"/>
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
  <layerGeometryType>2</layerGeometryType>
</qgis>
