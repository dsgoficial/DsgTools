<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="OGC_FID">
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tiporef">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Altimétrico" value="1"/>
        <value key="Planimétrico" value="2"/>
        <value key="Planialtimétrico" value="3"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="materializado">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="sistemageodesico">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="SAD-69" value="1"/>
        <value key="SIRGAS" value="2"/>
        <value key="WGS-84" value="3"/>
        <value key="Córrego Alegre" value="4"/>
        <value key="Astro Chuá" value="5"/>
        <value key="Outra referência" value="6"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="referencialaltim">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Torres" value="1"/>
        <value key="Imbituba" value="2"/>
        <value key="Santana" value="3"/>
        <value key="Local" value="4"/>
        <value key="Outra referência" value="5"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="tipoptocontrole">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Ponto de Controle" value="9"/>
        <value key="Ponto Perspectivo" value="12"/>
        <value key="Ponto Fotogramétrico" value="13"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype>  </edittypes>
</qgis>