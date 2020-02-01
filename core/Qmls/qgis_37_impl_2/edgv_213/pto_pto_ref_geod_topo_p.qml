<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis labelsEnabled="0" simplifyMaxScale="1" simplifyDrawingHints="0" simplifyLocal="1" version="3.7.0-Master" simplifyAlgorithm="0" styleCategories="AllStyleCategories" minScale="1e+8" readOnly="0" hasScaleBasedVisibilityFlag="0" simplifyDrawingTol="1" maxScale="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol type="marker" clip_to_extent="1" alpha="1" name="0" force_rhr="0">
        <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="213,180,60,255"/>
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
    <field name="tiporef">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="1" name="Altimétrico"/>
              <Option type="QString" value="4" name="Gravimétrico"/>
              <Option type="QString" value="3" name="Planialtimétrico"/>
              <Option type="QString" value="2" name="Planimétrico"/>
            </Option>
          </Option>
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
    <field name="altitudeortometrica">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="sistemageodesico">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="5" name="Astro Chuá"/>
              <Option type="QString" value="4" name="Córrego Alegre"/>
              <Option type="QString" value="6" name="Outra referência"/>
              <Option type="QString" value="1" name="SAD-69"/>
              <Option type="QString" value="2" name="SIRGAS"/>
              <Option type="QString" value="3" name="WGS-84"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencialaltim">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="2" name="Imbituba"/>
              <Option type="QString" value="4" name="Local"/>
              <Option type="QString" value="5" name="Outra referência"/>
              <Option type="QString" value="3" name="Santana"/>
              <Option type="QString" value="1" name="Torres"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="outrarefalt">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="outrarefplan">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="orgaoenteresp">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="codponto">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="obs">
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
    <field name="proximidade">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="15" name="Adjacente"/>
              <Option type="QString" value="16" name="Coincidente"/>
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="14" name="Isolado"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipoptorefgeodtopo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="3" name="Estação Gravimétrica - EG"/>
              <Option type="QString" value="4" name="Estação de Poligonal - EP"/>
              <Option type="QString" value="99" name="Outros"/>
              <Option type="QString" value="5" name="Ponto Astronômico - PA"/>
              <Option type="QString" value="7" name="Ponto Trigonométrico - RV"/>
              <Option type="QString" value="6" name="Ponto barométrico - B"/>
              <Option type="QString" value="8" name="Ponto de Satélite - SAT"/>
              <Option type="QString" value="2" name="Referência de Nível - RN"/>
              <Option type="QString" value="1" name="Vértice de Triangulação - VT"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="rede">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="0" name="Desconhecida"/>
              <Option type="QString" value="2" name="Estadual"/>
              <Option type="QString" value="3" name="Municipal"/>
              <Option type="QString" value="14" name="Nacional"/>
              <Option type="QString" value="15" name="Privada"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="referencialgrav">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="3" name="Absoluto"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="IGSN71"/>
              <Option type="QString" value="4" name="Local"/>
              <Option type="QString" value="97" name="Não Aplicável"/>
              <Option type="QString" value="1" name="Postdam 1930"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacaomarco">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="Map" name="map">
              <Option type="QString" value="1" name="Bom"/>
              <Option type="QString" value="0" name="Desconhecido"/>
              <Option type="QString" value="2" name="Destruído"/>
              <Option type="QString" value="4" name="Destruído com chapa danificada"/>
              <Option type="QString" value="3" name="Destruído sem chapa"/>
              <Option type="QString" value="7" name="Não construído"/>
              <Option type="QString" value="5" name="Não encontrado"/>
              <Option type="QString" value="6" name="Não visitado"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="datavisita">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="id" name="" index="0"/>
    <alias field="nomeabrev" name="" index="1"/>
    <alias field="geometriaaproximada" name="" index="2"/>
    <alias field="tiporef" name="" index="3"/>
    <alias field="latitude" name="" index="4"/>
    <alias field="longitude" name="" index="5"/>
    <alias field="altitudeortometrica" name="" index="6"/>
    <alias field="sistemageodesico" name="" index="7"/>
    <alias field="referencialaltim" name="" index="8"/>
    <alias field="outrarefalt" name="" index="9"/>
    <alias field="outrarefplan" name="" index="10"/>
    <alias field="orgaoenteresp" name="" index="11"/>
    <alias field="codponto" name="" index="12"/>
    <alias field="obs" name="" index="13"/>
    <alias field="nome" name="" index="14"/>
    <alias field="proximidade" name="" index="15"/>
    <alias field="tipoptorefgeodtopo" name="" index="16"/>
    <alias field="rede" name="" index="17"/>
    <alias field="referencialgrav" name="" index="18"/>
    <alias field="situacaomarco" name="" index="19"/>
    <alias field="datavisita" name="" index="20"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="nomeabrev" expression="" applyOnUpdate="0"/>
    <default field="geometriaaproximada" expression="" applyOnUpdate="0"/>
    <default field="tiporef" expression="" applyOnUpdate="0"/>
    <default field="latitude" expression="" applyOnUpdate="0"/>
    <default field="longitude" expression="" applyOnUpdate="0"/>
    <default field="altitudeortometrica" expression="" applyOnUpdate="0"/>
    <default field="sistemageodesico" expression="" applyOnUpdate="0"/>
    <default field="referencialaltim" expression="" applyOnUpdate="0"/>
    <default field="outrarefalt" expression="" applyOnUpdate="0"/>
    <default field="outrarefplan" expression="" applyOnUpdate="0"/>
    <default field="orgaoenteresp" expression="" applyOnUpdate="0"/>
    <default field="codponto" expression="" applyOnUpdate="0"/>
    <default field="obs" expression="" applyOnUpdate="0"/>
    <default field="nome" expression="" applyOnUpdate="0"/>
    <default field="proximidade" expression="" applyOnUpdate="0"/>
    <default field="tipoptorefgeodtopo" expression="" applyOnUpdate="0"/>
    <default field="rede" expression="" applyOnUpdate="0"/>
    <default field="referencialgrav" expression="" applyOnUpdate="0"/>
    <default field="situacaomarco" expression="" applyOnUpdate="0"/>
    <default field="datavisita" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="id" unique_strength="1" exp_strength="0" constraints="3" notnull_strength="1"/>
    <constraint field="nomeabrev" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="geometriaaproximada" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tiporef" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="latitude" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="longitude" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="altitudeortometrica" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="sistemageodesico" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="referencialaltim" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="outrarefalt" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="outrarefplan" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="orgaoenteresp" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="codponto" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="obs" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="nome" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
    <constraint field="proximidade" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="tipoptorefgeodtopo" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="rede" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="referencialgrav" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="situacaomarco" unique_strength="0" exp_strength="0" constraints="1" notnull_strength="1"/>
    <constraint field="datavisita" unique_strength="0" exp_strength="0" constraints="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="id" desc="" exp=""/>
    <constraint field="nomeabrev" desc="" exp=""/>
    <constraint field="geometriaaproximada" desc="" exp=""/>
    <constraint field="tiporef" desc="" exp=""/>
    <constraint field="latitude" desc="" exp=""/>
    <constraint field="longitude" desc="" exp=""/>
    <constraint field="altitudeortometrica" desc="" exp=""/>
    <constraint field="sistemageodesico" desc="" exp=""/>
    <constraint field="referencialaltim" desc="" exp=""/>
    <constraint field="outrarefalt" desc="" exp=""/>
    <constraint field="outrarefplan" desc="" exp=""/>
    <constraint field="orgaoenteresp" desc="" exp=""/>
    <constraint field="codponto" desc="" exp=""/>
    <constraint field="obs" desc="" exp=""/>
    <constraint field="nome" desc="" exp=""/>
    <constraint field="proximidade" desc="" exp=""/>
    <constraint field="tipoptorefgeodtopo" desc="" exp=""/>
    <constraint field="rede" desc="" exp=""/>
    <constraint field="referencialgrav" desc="" exp=""/>
    <constraint field="situacaomarco" desc="" exp=""/>
    <constraint field="datavisita" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
