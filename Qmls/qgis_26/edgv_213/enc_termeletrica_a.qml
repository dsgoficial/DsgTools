<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="OGC_FID">
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tipomaqtermica">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecido" value="0"/>
        <value key="Turbina à gás (TBGS)" value="1"/>
        <value key="Turbina à vapor (TBVP)" value="2"/>
        <value key="Ciclo combinado (CLCB)" value="3"/>
        <value key="Motor de Combustão Interna (NCIA)" value="4"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="tipocombustivel">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecido" value="0"/>
        <value key="Nuclear" value="1"/>
        <value key="Diesel" value="3"/>
        <value key="Outros" value="99"/>
        <value key="Carvão" value="33"/>
        <value key="Gás" value="5"/>
        <value key="Misto" value="98"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="geracao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecido" value="0"/>
        <value key="Eletricidade - GER 0" value="1"/>
        <value key="CoGeração" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="operacional">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Desconhecido" value="0"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="situacaofisica">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecida" value="0"/>
        <value key="Abandonada" value="1"/>
        <value key="Destruída" value="2"/>
        <value key="Em construção" value="3"/>
        <value key="Construída" value="5"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="combrenovavel">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>  </edittypes>
</qgis>