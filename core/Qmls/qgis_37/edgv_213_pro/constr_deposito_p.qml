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
          <prop k="color" v="125,139,143,255"/>
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
    <field name="tipo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Abast água - Caixa de água" type="QString" value="202"/>
              <Option name="Abast água - Cisterna" type="QString" value="203"/>
              <Option name="Abast água - Outros" type="QString" value="298"/>
              <Option name="Abast água - Tanque de água" type="QString" value="201"/>
              <Option name="Geral - Armazém" type="QString" value="132"/>
              <Option name="Geral - Composteira" type="QString" value="110"/>
              <Option name="Geral - Depósito frigorífico" type="QString" value="111"/>
              <Option name="Geral - Galpão" type="QString" value="108"/>
              <Option name="Geral - Outros" type="QString" value="198"/>
              <Option name="Geral - Silo" type="QString" value="109"/>
              <Option name="San - Aterro controlado" type="QString" value="306"/>
              <Option name="San - Aterro sanitário" type="QString" value="305"/>
              <Option name="San - Depósito de lixo" type="QString" value="304"/>
              <Option name="San - Outros" type="QString" value="398"/>
              <Option name="San - Tanque de saneamento" type="QString" value="301"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_exposicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Coberto" type="QString" value="4"/>
              <Option name="Céu aberto" type="QString" value="5"/>
              <Option name="Fechado" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacao_fisica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Abandonada" type="QString" value="1"/>
              <Option name="Construída" type="QString" value="3"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Destruída" type="QString" value="2"/>
              <Option name="Em construção" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="material_construcao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="98"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="finalidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Armazenamento" type="QString" value="8"/>
              <Option name="Distribuição" type="QString" value="4"/>
              <Option name="Recalque" type="QString" value="3"/>
              <Option name="Tratamento" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_produto_residuo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Bauxita" type="QString" value="25"/>
              <Option name="Carvão mineral" type="QString" value="33"/>
              <Option name="Cascalho" type="QString" value="18"/>
              <Option name="Chorume" type="QString" value="15"/>
              <Option name="Cobre" type="QString" value="32"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Escória" type="QString" value="36"/>
              <Option name="Esgoto" type="QString" value="9"/>
              <Option name="Estrume" type="QString" value="17"/>
              <Option name="Ferro" type="QString" value="35"/>
              <Option name="Folhagens" type="QString" value="21"/>
              <Option name="Forragem" type="QString" value="41"/>
              <Option name="Gasolina" type="QString" value="29"/>
              <Option name="Granito" type="QString" value="23"/>
              <Option name="Grãos" type="QString" value="6"/>
              <Option name="Gás" type="QString" value="5"/>
              <Option name="Inseticida" type="QString" value="20"/>
              <Option name="Lixo domiciliar e comercial" type="QString" value="12"/>
              <Option name="Lixo séptico" type="QString" value="14"/>
              <Option name="Lixo tóxico" type="QString" value="13"/>
              <Option name="Manganês" type="QString" value="26"/>
              <Option name="Misto" type="QString" value="95"/>
              <Option name="Mármore" type="QString" value="24"/>
              <Option name="Outros" type="QString" value="98"/>
              <Option name="Pedra (brita)" type="QString" value="22"/>
              <Option name="Querosene" type="QString" value="31"/>
              <Option name="Sal" type="QString" value="34"/>
              <Option name="Semente" type="QString" value="19"/>
              <Option name="Talco" type="QString" value="27"/>
              <Option name="Vinhoto" type="QString" value="16"/>
              <Option name="Água" type="QString" value="1"/>
              <Option name="Álcool" type="QString" value="30"/>
              <Option name="Óleo diesel" type="QString" value="28"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_comprovacao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Confirmado em campo" type="QString" value="1"/>
              <Option name="Feição não necessita de confirmação" type="QString" value="3"/>
              <Option name="Não possível de confirmar em campo" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_insumo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Aquisição em campo" type="QString" value="4"/>
              <Option name="Fotointerpretado" type="QString" value="1"/>
              <Option name="Insumo externo" type="QString" value="2"/>
              <Option name="Mapeamento anterior" type="QString" value="5"/>
              <Option name="Processo automático" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="observacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_modificacao">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="controle_id">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ultimo_usuario">
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
    <alias name="" index="2" field="tipo"/>
    <alias name="" index="3" field="tipo_exposicao"/>
    <alias name="" index="4" field="situacao_fisica"/>
    <alias name="" index="5" field="material_construcao"/>
    <alias name="" index="6" field="finalidade"/>
    <alias name="" index="7" field="tipo_produto_residuo"/>
    <alias name="" index="8" field="tipo_comprovacao"/>
    <alias name="" index="9" field="tipo_insumo"/>
    <alias name="" index="10" field="observacao"/>
    <alias name="" index="11" field="data_modificacao"/>
    <alias name="" index="12" field="controle_id"/>
    <alias name="" index="13" field="ultimo_usuario"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="tipo_exposicao" expression=""/>
    <default applyOnUpdate="0" field="situacao_fisica" expression=""/>
    <default applyOnUpdate="0" field="material_construcao" expression=""/>
    <default applyOnUpdate="0" field="finalidade" expression=""/>
    <default applyOnUpdate="0" field="tipo_produto_residuo" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_exposicao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacao_fisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="material_construcao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="finalidade" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_produto_residuo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="tipo_exposicao" desc=""/>
    <constraint exp="" field="situacao_fisica" desc=""/>
    <constraint exp="" field="material_construcao" desc=""/>
    <constraint exp="" field="finalidade" desc=""/>
    <constraint exp="" field="tipo_produto_residuo" desc=""/>
    <constraint exp="" field="tipo_comprovacao" desc=""/>
    <constraint exp="" field="tipo_insumo" desc=""/>
    <constraint exp="" field="observacao" desc=""/>
    <constraint exp="" field="data_modificacao" desc=""/>
    <constraint exp="" field="controle_id" desc=""/>
    <constraint exp="" field="ultimo_usuario" desc=""/>
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
