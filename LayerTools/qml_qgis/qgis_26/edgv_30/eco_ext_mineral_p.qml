<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0"> 
  <edittypes> 
     <edittype widgetv2type="TextEdit" name="OGC_FID"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype> 
    <edittype widgetv2type="TextEdit" name="id"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="TextEdit" name="id_org_ext_mineral"> 
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/> 
    </edittype>
    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Não" value="0"/>
        <value key="Sim" value="1"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoalterantrop">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Extrativismo mineral" value="27"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="secaoativecon">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Indústrias de transformação" value="1"/>
        <value key="Construção" value="2"/>
        <value key="Indústrias extrativas" value="3"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
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
    <edittype widgetv2type="ValueMap" name="tipoextmin">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Poço de petróleo" value="1"/>
        <value key="Mina" value="2"/>
        <value key="Poço para água subterrânea" value="3"/>
        <value key="Salina" value="4"/>
        <value key="Garimpo" value="5"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipoproduto">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sal-gema" value="1"/>
        <value key="Terras raras" value="2"/>
        <value key="Titânio" value="3"/>
        <value key="Topázio" value="4"/>
        <value key="Tungstênio" value="5"/>
        <value key="Turmalina" value="6"/>
        <value key="Tório" value="7"/>
        <value key="Urânio" value="8"/>
        <value key="Opala" value="9"/>
        <value key="Zinco" value="10"/>
        <value key="Zircônio" value="11"/>
        <value key="Níquel" value="12"/>
        <value key="Querosene" value="13"/>
        <value key="Água mineral" value="14"/>
        <value key="Óleo diesel" value="15"/>
        <value key="Vermiculita" value="16"/>
        <value key="Ágata" value="17"/>
        <value key="Água" value="18"/>
        <value key="Nióbio" value="19"/>
        <value key="Rocha ornamental" value="20"/>
        <value key="Ouro" value="24"/>
        <value key="Petróleo" value="25"/>
        <value key="Pedra preciosa" value="26"/>
        <value key="Gás" value="27"/>
        <value key="Grão" value="28"/>
        <value key="Alexandrita" value="29"/>
        <value key="Ametista" value="30"/>
        <value key="Amianto" value="31"/>
        <value key="Argila" value="32"/>
        <value key="Barita" value="33"/>
        <value key="Bentonita" value="34"/>
        <value key="Calcário" value="35"/>
        <value key="Carvão vegetal" value="36"/>
        <value key="Caulim" value="37"/>
        <value key="Vinhoto" value="38"/>
        <value key="Estrume" value="39"/>
        <value key="Cascalho" value="40"/>
        <value key="Chumbo" value="41"/>
        <value key="Inseticida" value="42"/>
        <value key="Folhagem" value="43"/>
        <value key="Água marinha" value="44"/>
        <value key="Pedra (brita)" value="45"/>
        <value key="Granito" value="46"/>
        <value key="Mármore" value="47"/>
        <value key="Bauxita" value="48"/>
        <value key="Manganês" value="49"/>
        <value key="Talco" value="50"/>
        <value key="Chorume" value="51"/>
        <value key="Gasolina" value="52"/>
        <value key="Álcool" value="53"/>
        <value key="Citrino" value="54"/>
        <value key="Cobre" value="55"/>
        <value key="Carvão mineral" value="56"/>
        <value key="Sal" value="57"/>
        <value key="Turfa" value="58"/>
        <value key="Escória" value="59"/>
        <value key="Ferro" value="60"/>
        <value key="Crisoberilo" value="61"/>
        <value key="Prata" value="62"/>
        <value key="Cristal de rocha" value="63"/>
        <value key="Forragem" value="64"/>
        <value key="Saibro/piçarra" value="65"/>
        <value key="Areia" value="66"/>
        <value key="Cromo" value="67"/>
        <value key="Diamante" value="68"/>
        <value key="Diatomita" value="69"/>
        <value key="Dolomito" value="70"/>
        <value key="Esgoto" value="71"/>
        <value key="Esmeralda" value="72"/>
        <value key="Estanho" value="73"/>
        <value key="Feldspato" value="74"/>
        <value key="Fosfato" value="75"/>
        <value key="Gipsita" value="76"/>
        <value key="Grafita" value="77"/>
        <value key="Granada" value="78"/>
        <value key="Lixo domiciliar e comercial" value="79"/>
        <value key="Lixo séptico" value="80"/>
        <value key="Lixo tóxico" value="81"/>
        <value key="Lítio" value="82"/>
        <value key="Magnesita" value="83"/>
        <value key="Mica" value="84"/>
        <value key="Desconhecido" value="95"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="tipopocomina">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Horizontal" value="3"/>
        <value key="Vertical" value="4"/>
        <value key="Desconhecido" value="95"/>
        <value key="Não aplicável" value="97"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="procextracao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Manual" value="1"/>
        <value key="Mecanizado" value="2"/>
        <value key="Desconhecido" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="atividade">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Prospecção" value="9"/>
        <value key="Produção" value="10"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
    <edittype widgetv2type="ValueMap" name="formaextracao">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="A céu aberto" value="1"/>
        <value key="Subterrânea" value="2"/>
        <value key="Desconhecida" value="95"/>
      </widgetv2config>
    </edittype> 
  </edittypes>
</qgis>