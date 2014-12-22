<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_complexo_portuario"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="modaluso">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Portuário" value="5"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="administracao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Federal" value="1"/>
        <value key="Estadual/Distrital" value="2"/>
        <value key="Municipal" value="3"/>
        <value key="Concessionada" value="4"/>
        <value key="Privada" value="5"/>
        <value key="Não aplicável" value="6"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="jurisdicao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Internacional" value="1"/>
        <value key="Propriedade particular" value="2"/>
        <value key="Federal" value="3"/>
        <value key="Estadual/Distrital" value="4"/>
        <value key="Municipal" value="5"/>
        <value key="Desconhecida" value="95"/>
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
    <edittype widgetv2type="ValueMap" name="tipotransporte">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Passageiro" value="1"/>
        <value key="Carga" value="3"/>
        <value key="Desconhecido" value="95"/>
        <value key="Misto" value="98"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipocomplexoportuario">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Instalação portuária" value="8"/>
        <value key="Porto organizado" value="9"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="portosempapel">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
  </edittypes>
</qgis>