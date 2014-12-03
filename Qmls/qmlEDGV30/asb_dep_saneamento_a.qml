<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_complexo_saneamento"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
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
    <edittype widgetv2type="ValueMap" name="tipodep">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Composteira" value="3"/>
        <value key="Aterro controlado" value="4"/>
        <value key="Depósito de lixo" value="5"/>
        <value key="Depósito frigorífico" value="7"/>
        <value key="Outros" value="99"/>
        <value key="Aterro sanitário" value="29"/>
        <value key="Desconhecido" value="95"/>
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
    <edittype widgetv2type="ValueMap" name="tipoexposicao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Coberto" value="1"/>
        <value key="Céu aberto" value="2"/>
        <value key="Fechado" value="3"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoprodutoresiduo">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Estrume" value="39"/>
        <value key="Inseticida" value="42"/>
        <value key="Folhagem" value="43"/>
        <value key="Chorume" value="51"/>
        <value key="Esgoto" value="71"/>
        <value key="Lixo domiciliar e comercial" value="79"/>
        <value key="Lixo séptico" value="80"/>
        <value key="Lixo tóxico" value="81"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoconteudo">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Insumo" value="11"/>
        <value key="Produto" value="12"/>
        <value key="Resíduo" value="32"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="unidadevolume">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Litro" value="6"/>
        <value key="Metro cúbico" value="7"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="estadofisico">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sólido" value="0"/>
        <value key="Misto" value="1"/>
        <value key="Gasoso" value="2"/>
        <value key="Líquido" value="4"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tratamento">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="finalidadedep">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Tratamento" value="1"/>
        <value key="Recalque" value="2"/>
        <value key="Distribuição" value="3"/>
        <value key="Armazenamento" value="4"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
  </edittypes>
</qgis>