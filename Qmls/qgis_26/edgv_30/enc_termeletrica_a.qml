<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_complexo_gerad_energ_eletr"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoestgerad">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Termelétrica" value="2"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="operacional">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="situacaofisica">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Planejada" value="1"/>
        <value key="Construída" value="2"/>
        <value key="Abandonada" value="3"/>
        <value key="Destruída" value="4"/>
        <value key="Em construção" value="5"/>
        <value key="Construída, mas em obras" value="6"/>
        <value key="Desconhecida" value="95"/>
        <value key="Não aplicável" value="97"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="destenergelet">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Serviço público (SP)" value="1"/>
        <value key="Auto-produção de energia (APE)" value="2"/>
        <value key="Auto-produção com comercialização de excedente (APE-COM)" value="3"/>
        <value key="Comercialização de energia (COM)" value="4"/>
        <value key="Produção independente de energia (PIE)" value="5"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="geracao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Eletricidade - GER 0" value="1"/>
        <value key="Cogeração" value="2"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipocombustivel">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Nuclear" value="14"/>
        <value key="Diesel" value="15"/>
        <value key="Gás" value="16"/>
        <value key="Carvão" value="17"/>
        <value key="Desconhecido" value="95"/>
        <value key="Misto" value="98"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="combrenovavel">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipomaqtermica">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Ciclo combinado (CLCB)" value="5"/>
        <value key="Motor de combustão interna (MCIA)" value="6"/>
        <value key="Turbina a gás (TBGS)" value="7"/>
        <value key="Turbina a vapor (TBVP)" value="8"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
  </edittypes>
</qgis>