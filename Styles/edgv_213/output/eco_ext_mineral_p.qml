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
    <edittype widgetv2type="ValueMap" name="tiposecaocnae">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="C - Indústrias Extrativas" value="1"/>
        <value key="Desconhecido" value="0"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="operacional">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="situacaofisica">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Abandonada" value="1"/>
        <value key="Construída" value="5"/>
        <value key="Desconhecida" value="0"/>
        <value key="Destruída" value="2"/>
        <value key="Em Construção" value="3"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tipoextmin">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Garimpo" value="5"/>
        <value key="Mina" value="4"/>
        <value key="Outros" value="99"/>
        <value key="Pedreira" value="7"/>
        <value key="Ponto de Prospecção" value="8"/>
        <value key="Poço" value="1"/>
        <value key="Salina" value="6"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tipoprodutoresiduo">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Areia" value="42"/>
        <value key="Bauxita" value="25"/>
        <value key="Carvão" value="33"/>
        <value key="Cascalho" value="18"/>
        <value key="Cobre" value="32"/>
        <value key="Desconhecido" value="0"/>
        <value key="Diamante" value="38"/>
        <value key="Ferro" value="35"/>
        <value key="Granito" value="23"/>
        <value key="Gás" value="5"/>
        <value key="Manganês" value="26"/>
        <value key="Misto" value="98"/>
        <value key="Mármore" value="24"/>
        <value key="Ouro" value="37"/>
        <value key="Outros" value="99"/>
        <value key="Pedra" value="22"/>
        <value key="Pedras preciosas" value="40"/>
        <value key="Petróleo" value="3"/>
        <value key="Piçarra" value="44"/>
        <value key="Prata" value="39"/>
        <value key="Saibro" value="43"/>
        <value key="Sal" value="34"/>
        <value key="Talco" value="27"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tipopocomina">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Horizontal" value="2"/>
        <value key="Não aplicável" value="97"/>
        <value key="Vertical" value="3"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="procextracao">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Manual" value="2"/>
        <value key="Mecanizado" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="formaextracao">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Céu aberto" value="5"/>
        <value key="Desconhecida" value="0"/>
        <value key="Subterrâneo" value="6"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="atividade">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Produção" value="10"/>
        <value key="Prospecção" value="9"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_org_ext_mineral">
      <widgetv2config IsMultiline="0" fieldEditable="0" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
  </edittypes>
  <renderer-v2 forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" type="marker" name="0">
        <layer pass="0" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="no"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="0.3"/>
          <prop k="size_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
