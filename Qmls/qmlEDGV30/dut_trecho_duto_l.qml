<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_duto"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipotrechoduto">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Calha" value="1"/>
        <value key="Duto" value="2"/>
        <value key="Correia transportadora" value="3"/>
        <value key="Galeria ou bueiro" value="5"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="mattransp">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Querosene" value="1"/>
        <value key="Álcool" value="2"/>
        <value key="Nafta" value="3"/>
        <value key="Minério" value="4"/>
        <value key="Grãos" value="5"/>
        <value key="Gasolina" value="6"/>
        <value key="Gás" value="7"/>
        <value key="Óleo" value="8"/>
        <value key="Efluentes" value="9"/>
        <value key="Esgoto" value="29"/>
        <value key="Água" value="30"/>
        <value key="Petróleo" value="31"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="setor">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Econômico" value="1"/>
        <value key="Abastecimento de água" value="2"/>
        <value key="Saneamento básico" value="3"/>
        <value key="Energético" value="4"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="posicaorelativa">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Emersa" value="1"/>
        <value key="Subterrânea" value="2"/>
        <value key="Desconhecida" value="3"/>
        <value key="Elevada" value="4"/>
        <value key="Superfície" value="5"/>
        <value key="Submersa" value="6"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="matconstr">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Alvenaria" value="2"/>
        <value key="Concreto" value="3"/>
        <value key="Metal" value="4"/>
        <value key="Rocha" value="5"/>
        <value key="Madeira" value="6"/>
        <value key="Terra" value="7"/>
        <value key="Fibra" value="8"/>
        <value key="Desconhecido" value="95"/>
        <value key="Não aplicável" value="97"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="situacaoespacial">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Subterrânea" value="1"/>
        <value key="Superposta nivel 1" value="2"/>
        <value key="Superposta nivel 2" value="3"/>
        <value key="Nivel do solo" value="4"/>
        <value key="Adjacente" value="5"/>
        <value key="Superposta nivel 3" value="6"/>
        <value key="Desconhecida" value="95"/>
        <value key="Não aplicável" value="97"/>
        <value key="Outra" value="99"/>
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
  </edittypes>
</qgis>