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
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="denso">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="antropizada">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="especiepredominante">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Araucária" value="27"/>
        <value key="Babaçu" value="41"/>
        <value key="Bambu" value="11"/>
        <value key="Cipó" value="10"/>
        <value key="Misto" value="98"/>
        <value key="Não identificado" value="96"/>
        <value key="Palmeira" value="17"/>
        <value key="Sororoca" value="12"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="caracteristicafloresta">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Bosque" value="3"/>
        <value key="Desconhecido" value="0"/>
        <value key="Floresta" value="1"/>
        <value key="Mata" value="2"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="alturamediaindividuos">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="classificacaoporte">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Arbustiva" value="2"/>
        <value key="Arbórea" value="1"/>
        <value key="Desconhecido" value="0"/>
        <value key="Misto" value="98"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="area_otf">
      <widgetv2config IsMultiline="0" fieldEditable="0" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
  </edittypes>
  <renderer-v2 forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="fill" name="0">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="color" v="0,100,0,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,100,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.1"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
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
  <layerGeometryType>2</layerGeometryType>
</qgis>
