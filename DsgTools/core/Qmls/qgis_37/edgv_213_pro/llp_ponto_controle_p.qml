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
          <prop k="color" v="232,113,141,255"/>
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
    <field name="cod_ponto">
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
              <Option name="Centro perspectivo" type="QString" value="12"/>
              <Option name="Estação Gravimétrica – EG" type="QString" value="3"/>
              <Option name="Estação de Poligonal – EP" type="QString" value="4"/>
              <Option name="Marco estadual" type="QString" value="15"/>
              <Option name="Marco internacional" type="QString" value="14"/>
              <Option name="Marco municipal" type="QString" value="16"/>
              <Option name="Ponto Astronômico – PA" type="QString" value="5"/>
              <Option name="Ponto Barométrico – B" type="QString" value="6"/>
              <Option name="Ponto Trigonométrico – RV" type="QString" value="7"/>
              <Option name="Ponto de Satélite – SAT" type="QString" value="8"/>
              <Option name="Ponto de controle" type="QString" value="9"/>
              <Option name="Ponto fotogramétrico" type="QString" value="13"/>
              <Option name="Referëncia de Nível – RN" type="QString" value="2"/>
              <Option name="Vértice de Triangulação – VT" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_ref">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Altimétrico" type="QString" value="1"/>
              <Option name="Gravimétrico" type="QString" value="4"/>
              <Option name="Planialtimétrico" type="QString" value="3"/>
              <Option name="Planimétrico" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="altitude_ortometrica">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sistema_geodesico">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Astro Chuá" type="QString" value="5"/>
              <Option name="Córrego Alegre" type="QString" value="4"/>
              <Option name="SAD 69" type="QString" value="1"/>
              <Option name="SIRGAS 2000" type="QString" value="2"/>
              <Option name="WGS-84" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencial_altim">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Imbituba" type="QString" value="2"/>
              <Option name="Local" type="QString" value="4"/>
              <Option name="Santana" type="QString" value="3"/>
              <Option name="Torres" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencial_grav">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Absoluto" type="QString" value="3"/>
              <Option name="IGSN71" type="QString" value="2"/>
              <Option name="Local" type="QString" value="4"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Postdam 1930" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacao_marco">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Bom" type="QString" value="1"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Destruído" type="QString" value="2"/>
              <Option name="Destruído com chapa danificada" type="QString" value="4"/>
              <Option name="Destruído sem chapa" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Não encontrado" type="QString" value="5"/>
              <Option name="Não visitado" type="QString" value="6"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="orgao_responsavel">
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
    <field name="longitude">
      <editWidget type="">
        <config>
          <Option/>
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
    <alias name="" index="1" field="cod_ponto"/>
    <alias name="" index="2" field="tipo"/>
    <alias name="" index="3" field="tipo_ref"/>
    <alias name="" index="4" field="altitude_ortometrica"/>
    <alias name="" index="5" field="sistema_geodesico"/>
    <alias name="" index="6" field="referencial_altim"/>
    <alias name="" index="7" field="referencial_grav"/>
    <alias name="" index="8" field="situacao_marco"/>
    <alias name="" index="9" field="orgao_responsavel"/>
    <alias name="" index="10" field="latitude"/>
    <alias name="" index="11" field="longitude"/>
    <alias name="" index="12" field="tipo_comprovacao"/>
    <alias name="" index="13" field="tipo_insumo"/>
    <alias name="" index="14" field="observacao"/>
    <alias name="" index="15" field="data_modificacao"/>
    <alias name="" index="16" field="controle_id"/>
    <alias name="" index="17" field="ultimo_usuario"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="cod_ponto" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="tipo_ref" expression=""/>
    <default applyOnUpdate="0" field="altitude_ortometrica" expression=""/>
    <default applyOnUpdate="0" field="sistema_geodesico" expression=""/>
    <default applyOnUpdate="0" field="referencial_altim" expression=""/>
    <default applyOnUpdate="0" field="referencial_grav" expression=""/>
    <default applyOnUpdate="0" field="situacao_marco" expression=""/>
    <default applyOnUpdate="0" field="orgao_responsavel" expression=""/>
    <default applyOnUpdate="0" field="latitude" expression=""/>
    <default applyOnUpdate="0" field="longitude" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="cod_ponto" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_ref" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="altitude_ortometrica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="sistema_geodesico" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="referencial_altim" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="referencial_grav" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacao_marco" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="orgao_responsavel" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="latitude" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="longitude" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="cod_ponto" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="tipo_ref" desc=""/>
    <constraint exp="" field="altitude_ortometrica" desc=""/>
    <constraint exp="" field="sistema_geodesico" desc=""/>
    <constraint exp="" field="referencial_altim" desc=""/>
    <constraint exp="" field="referencial_grav" desc=""/>
    <constraint exp="" field="situacao_marco" desc=""/>
    <constraint exp="" field="orgao_responsavel" desc=""/>
    <constraint exp="" field="latitude" desc=""/>
    <constraint exp="" field="longitude" desc=""/>
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
