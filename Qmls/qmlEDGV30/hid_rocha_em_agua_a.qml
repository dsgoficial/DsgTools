<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="situacaoemagua">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Emerso" value="5"/>
        <value key="Cobre e descobre" value="6"/>
        <value key="Submerso" value="7"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="formarocha">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Área rochosa - lajedo" value="2"/>
        <value key="Penedo isolado" value="3"/>
        <value key="Matacão - pedra" value="4"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoelemnat">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Rocha" value="12"/>
      </widgetv2config>
    </edittype> 
  </edittypes>
</qgis>