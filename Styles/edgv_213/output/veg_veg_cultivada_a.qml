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
    <edittype widgetv2type="ValueMap" name="tipolavoura">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Anual" value="3"/>
        <value key="Desconhecido" value="0"/>
        <value key="Perene" value="1"/>
        <value key="Semi-perene" value="2"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="finalidade">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Conservação ambiental" value="3"/>
        <value key="Desconhecido" value="0"/>
        <value key="Exploração econômica" value="1"/>
        <value key="Outros" value="99"/>
        <value key="Subistência" value="2"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="terreno">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Inundado" value="3"/>
        <value key="Irrigado" value="2"/>
        <value key="Seco" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="ValueMap" name="classificacaoporte">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Arbustiva" value="2"/>
        <value key="Desconhecido" value="0"/>
        <value key="Herbácea" value="3"/>
        <value key="Misto" value="98"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="espacamentoindividuos">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="TextEdit" name="espessuradap">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="denso">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype>
    <edittype widgetv2type="TextEdit" name="alturamediaindividuos">
      <widgetv2config IsMultiline="0" fieldEditable="1" constraint="" UseHtml="0" labelOnTop="0" constraintDescription="" notNull="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="cultivopredominante">
      <widgetv2config fieldEditable="1" constraint="" labelOnTop="0" constraintDescription="" notNull="0">
        <value key="Acácia" value="21"/>
        <value key="Algaroba" value="22"/>
        <value key="Algodão herbáceo" value="6"/>
        <value key="Araucária" value="27"/>
        <value key="Arroz" value="13"/>
        <value key="Açaí" value="18"/>
        <value key="Banana" value="2"/>
        <value key="Batata inglesa" value="10"/>
        <value key="Bracatinga" value="26"/>
        <value key="Cacau" value="15"/>
        <value key="Café" value="14"/>
        <value key="Cana-de-Açúcar" value="7"/>
        <value key="Carnauba" value="28"/>
        <value key="Cebola" value="33"/>
        <value key="Erva-mate" value="16"/>
        <value key="Eucalipto" value="20"/>
        <value key="Feijão" value="12"/>
        <value key="Fumo" value="8"/>
        <value key="Hortaliças" value="25"/>
        <value key="Juta" value="32"/>
        <value key="Laranja" value="3"/>
        <value key="Mandioca" value="11"/>
        <value key="Maçã" value="30"/>
        <value key="Milho" value="1"/>
        <value key="Misto" value="98"/>
        <value key="Não identificado" value="96"/>
        <value key="Outros" value="99"/>
        <value key="Palmeira" value="17"/>
        <value key="Pastagem cultivada" value="24"/>
        <value key="Pera" value="29"/>
        <value key="Pinus" value="23"/>
        <value key="Pêssego" value="31"/>
        <value key="Seringueira" value="19"/>
        <value key="Soja" value="9"/>
        <value key="Trigo" value="4"/>
        <value key="Videira" value="42"/>
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
          <prop k="color" v="170,255,127,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,170,0,255"/>
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
