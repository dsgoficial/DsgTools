<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.16.0-Nødebo" simplifyAlgorithm="0" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="id">
      <widgetv2config IsMultiline="0" fieldEditable="0" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="nome">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="nomeabrev">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="coincidecomdentrode">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Contorno Massa D`Água" value="2"/>
        <value key="Costa Visível da Carta" value="5"/>
        <value key="Cumeada" value="3"/>
        <value key="Ferrovia" value="7"/>
        <value key="Linha Seca" value="4"/>
        <value key="Massa D`Água" value="9"/>
        <value key="Não Identificado" value="96"/>
        <value key="Rodovia" value="6"/>
        <value key="Trecho de Drenagem" value="8"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="extensao">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tipolimareaesp">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Amazônia legal" value="5"/>
        <value key="Area Militar" value="36"/>
        <value key="Assentamento rural" value="4"/>
        <value key="Corredor ecológico" value="12"/>
        <value key="Distrito florestal" value="11"/>
        <value key="Estação Ecológica - ESEC" value="31"/>
        <value key="Estação biológica" value="19"/>
        <value key="Estrada parque" value="21"/>
        <value key="Faixa de fronteira" value="6"/>
        <value key="Floresta - FLO" value="26"/>
        <value key="Floresta Extrativista" value="23"/>
        <value key="Floresta de rendimento sustentável" value="22"/>
        <value key="Floresta pública" value="13"/>
        <value key="Horto florestal" value="20"/>
        <value key="Monumento Natural - MONA" value="33"/>
        <value key="Mosaico" value="10"/>
        <value key="Outros" value="99"/>
        <value key="Parque - PAR" value="32"/>
        <value key="Polígono das secas" value="7"/>
        <value key="Quilombo" value="3"/>
        <value key="Refúgio de Vida Silvestre - RVS" value="35"/>
        <value key="Reserva Biológica - REBIO" value="34"/>
        <value key="Reserva Extrativista - RESEX" value="28"/>
        <value key="Reserva Particular do Patrimônio Natural - RPPN" value="30"/>
        <value key="Reserva da biosfera" value="16"/>
        <value key="Reserva de Desenvolvimento Sustentável - RDS" value="27"/>
        <value key="Reserva de Fauna - REFAU" value="29"/>
        <value key="Reserva ecológica" value="18"/>
        <value key="Reserva florestal" value="17"/>
        <value key="Reserva legal" value="9"/>
        <value key="Sítios RAMSAR" value="14"/>
        <value key="Sítios do patrimônio" value="15"/>
        <value key="Terra indígena" value="2"/>
        <value key="Terra pública" value="1"/>
        <value key="Área de Relevante Interesse Ecológico - ARIE" value="25"/>
        <value key="Área de preservação permanente" value="8"/>
        <value key="Área de proteção ambiental - APA" value="24"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="obssituacao">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="comprimento_otf">
      <widgetv2config IsMultiline="0" fieldEditable="0" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
  </edittypes>
  <renderer-v2 forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="line" name="0">
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v=""/>
          <prop k="customdash_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="0,220,220,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.1"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="0,0,0,0,0,0"/>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale scalemethod="diameter"/>
  </renderer-v2>
  <labeling type="simple"/>
  <customproperties/>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerTransparency>0</layerTransparency>
  <displayfield>id</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Label"/>
    <family fieldname="" name="Ubuntu"/>
    <size fieldname="" units="pt" value="12"/>
    <bold fieldname="" on="0"/>
    <italic fieldname="" on="0"/>
    <underline fieldname="" on="0"/>
    <strikeout fieldname="" on="0"/>
    <color fieldname="" red="0" blue="0" green="0"/>
    <x fieldname=""/>
    <y fieldname=""/>
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
    <angle fieldname="" value="0" auto="0"/>
    <alignment fieldname="" value="center"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="1"/>
    <bufferenabled fieldname="" on=""/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <annotationform></annotationform>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <attributeactions default="-1"/>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="" sortOrder="0">
    <columns/>
  </attributetableconfig>
  <editform></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <widgets/>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <layerGeometryType>1</layerGeometryType>
</qgis>
