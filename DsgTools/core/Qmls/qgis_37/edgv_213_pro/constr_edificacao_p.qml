<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="0" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="0" symbollevels="1">
    <rules key="{c9911b9e-bb56-40e2-a389-66ee7f9b30d9}">
      <rule label="Edificacao_P" key="{1d0efa6a-67d2-4371-a0e5-576843c8bfe6}" symbol="0"/>
      <rule scalemaxdenom="2000" label="Limite de afastamento" scalemindenom="1" key="{5d21023a-a0ce-4ace-a4f3-cabf602342d3}" symbol="1"/>
    </rules>
    <symbols>
      <symbol name="0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="1" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="35,35,35,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="5"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MapUnit"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleMarker" enabled="1" pass="2" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="square"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.5"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="4"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="1" force_rhr="0" type="marker" alpha="0.553" clip_to_extent="1">
        <layer class="FilledMarker" enabled="1" pass="0" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="255,247,0,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="10"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MapUnit"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@0" force_rhr="0" type="fill" alpha="0.481" clip_to_extent="1">
            <layer class="SimpleFill" enabled="1" pass="0" locked="0">
              <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="color" v="255,247,0,255"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0.26"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="style" v="solid"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory opacity="1" maxScaleDenominator="1e+8" barWidth="5" sizeType="MM" minimumSize="0" penAlpha="255" width="15" backgroundColor="#ffffff" enabled="0" sizeScale="3x:0,0,0,0,0,0" penColor="#000000" lineSizeType="MM" labelPlacementMethod="XHeight" penWidth="0" scaleBasedVisibility="0" scaleDependency="Area" rotationOffset="270" diagramOrientation="Up" height="15" minScaleDenominator="0" lineSizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255">
      <fontProperties description="Noto Sans,10,-1,0,50,0,0,0,0,0,Regular" style="Regular"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" zIndex="0" priority="0" obstacle="0" placement="0" dist="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nome">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="tipo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Abast - Edificação de captação de água" type="QString" value="301"/>
              <Option name="Abast - Edificação de recalque de água" type="QString" value="303"/>
              <Option name="Abast - Edificação de tratamento de água" type="QString" value="302"/>
              <Option name="Abast - Mista" type="QString" value="395"/>
              <Option name="Abast - Outros" type="QString" value="398"/>
              <Option name="Aero - Hangar" type="QString" value="2429"/>
              <Option name="Aero - Outros" type="QString" value="2498"/>
              <Option name="Aero - Terminal de cargas" type="QString" value="2427"/>
              <Option name="Aero - Terminal de passageiros" type="QString" value="2426"/>
              <Option name="Aero - Torre de controle" type="QString" value="2428"/>
              <Option name="Agro - Apiário" type="QString" value="1214"/>
              <Option name="Agro - Aviário" type="QString" value="1213"/>
              <Option name="Agro - Curral" type="QString" value="1218"/>
              <Option name="Agro - Outros" type="QString" value="1298"/>
              <Option name="Agro - Pocilga" type="QString" value="1217"/>
              <Option name="Agro - Sede operacional de fazenda" type="QString" value="1212"/>
              <Option name="Agro - Viveiro de plantas" type="QString" value="1215"/>
              <Option name="Agro - Viveiro para aquicultura" type="QString" value="1216"/>
              <Option name="Com - Central de comutação e transmissão" type="QString" value="102"/>
              <Option name="Com - Centro de operações de comunicação" type="QString" value="101"/>
              <Option name="Com - Estação repetidora" type="QString" value="104"/>
              <Option name="Com - Estação rádio-base" type="QString" value="103"/>
              <Option name="Comerc - Centro comercial" type="QString" value="903"/>
              <Option name="Comerc - Centro de convenções" type="QString" value="905"/>
              <Option name="Comerc - Feira" type="QString" value="906"/>
              <Option name="Comerc - Hotel / motel / pousada" type="QString" value="907"/>
              <Option name="Comerc - Mercado" type="QString" value="904"/>
              <Option name="Comerc - Outros" type="QString" value="998"/>
              <Option name="Edificação de energia" type="QString" value="201"/>
              <Option name="Edificação de medição de fenômenos" type="QString" value="1501"/>
              <Option name="Edificação destruída" type="QString" value="1"/>
              <Option name="Edificação genérica" type="QString" value="0"/>
              <Option name="Edificação habitacional" type="QString" value="2701"/>
              <Option name="Ens - Edificação de educação infantil - pré-escola" type="QString" value="517"/>
              <Option name="Ens - Edificação de educação infantil – creche" type="QString" value="516"/>
              <Option name="Ens - Edificação de educação professional de nível técnico" type="QString" value="523"/>
              <Option name="Ens - Edificação de educação profissional de nível tecnológico" type="QString" value="524"/>
              <Option name="Ens - Edificação de educação superior – Graduação" type="QString" value="520"/>
              <Option name="Ens - Edificação de educação superior – graduação e pós-graduação" type="QString" value="521"/>
              <Option name="Ens - Edificação de educação superior – pós-graduação e extensão" type="QString" value="522"/>
              <Option name="Ens - Edificação de ensino fundamental" type="QString" value="518"/>
              <Option name="Ens - Edificação de ensino médio" type="QString" value="519"/>
              <Option name="Ens - Misto" type="QString" value="595"/>
              <Option name="Ens - Outras atividades de ensino" type="QString" value="525"/>
              <Option name="Estação Agroclimatológica" type="QString" value="1603"/>
              <Option name="Estação Climatológica Auxiliar" type="QString" value="1602"/>
              <Option name="Estação Climatológica Principal" type="QString" value="1601"/>
              <Option name="Estação Evaporimétrica" type="QString" value="1606"/>
              <Option name="Estação Eólica" type="QString" value="1605"/>
              <Option name="Estação Fluviométrica" type="QString" value="1610"/>
              <Option name="Estação Maregráfica" type="QString" value="1611"/>
              <Option name="Estação Pluviométrica" type="QString" value="1604"/>
              <Option name="Estação Solarimétrica" type="QString" value="1607"/>
              <Option name="Estação de Marés Terrestre - Crosta" type="QString" value="1612"/>
              <Option name="Estação de Radar Metereológico" type="QString" value="1608"/>
              <Option name="Estação de Radiossonda" type="QString" value="1609"/>
              <Option name="Ext Min - Extração de carvão mineral" type="QString" value="1110"/>
              <Option name="Ext Min - Extração de minerais metálicos" type="QString" value="1113"/>
              <Option name="Ext Min - Extração de minerais não-metálicos" type="QString" value="1114"/>
              <Option name="Ext Min - Extração de petróleo e serviços relacionados" type="QString" value="1111"/>
              <Option name="Ext Min - Outros" type="QString" value="1198"/>
              <Option name="Ferrov - Estação ferroviária de passageiros" type="QString" value="2316"/>
              <Option name="Ferrov - Estação metroviária" type="QString" value="2317"/>
              <Option name="Ferrov - Oficina de manutenção" type="QString" value="2320"/>
              <Option name="Ferrov - Outros" type="QString" value="2398"/>
              <Option name="Ferrov - Terminal ferroviário de cargas" type="QString" value="2318"/>
              <Option name="Ferrov - Terminal ferroviário de passageiros e cargas" type="QString" value="2319"/>
              <Option name="Habitacão indigena" type="QString" value="1401"/>
              <Option name="Ind - Confecção de artigos de vestuário e acessórios" type="QString" value="1018"/>
              <Option name="Ind - Fabriação de máquinas de escritório e equipamentos de informática" type="QString" value="1030"/>
              <Option name="Ind - Fabricação alimentícia e bebidas" type="QString" value="1015"/>
              <Option name="Ind - Fabricação de artigos de borracha e material plástico" type="QString" value="1025"/>
              <Option name="Ind - Fabricação de celulose, papel e produtos de papel" type="QString" value="1021"/>
              <Option name="Ind - Fabricação de coque, refino de petróleo, elaboração de combustíveis nucleares e produção de álcool" type="QString" value="1023"/>
              <Option name="Ind - Fabricação de equipamentos de instrumentação médico-hospitalares, instrumentos de precisão e ópticos, automação industrial, cronômetros e relógios" type="QString" value="1033"/>
              <Option name="Ind - Fabricação de material eletrônico, de aparelhos e equipamentos de comunicações" type="QString" value="1032"/>
              <Option name="Ind - Fabricação de máquinas e equipamentos" type="QString" value="1029"/>
              <Option name="Ind - Fabricação de máquinas, aparelhos e materiais elétricos" type="QString" value="1031"/>
              <Option name="Ind - Fabricação de móveis e indústrias diversas" type="QString" value="1036"/>
              <Option name="Ind - Fabricação de outros equipamentos de transporte" type="QString" value="1035"/>
              <Option name="Ind - Fabricação de produtos de madeira e celulose" type="QString" value="1020"/>
              <Option name="Ind - Fabricação de produtos de metal" type="QString" value="1028"/>
              <Option name="Ind - Fabricação de produtos de minerais não-metálicos" type="QString" value="1026"/>
              <Option name="Ind - Fabricação de produtos do fumo" type="QString" value="1016"/>
              <Option name="Ind - Fabricação de produtos químicos" type="QString" value="1024"/>
              <Option name="Ind - Fabricação de produtos têxteis" type="QString" value="1017"/>
              <Option name="Ind - Fabricação e montagem de veículos automotores, reboques e carrocerias" type="QString" value="1034"/>
              <Option name="Ind - Industria de edição, impressão e reprodução de gravações" type="QString" value="1022"/>
              <Option name="Ind - Indústria de construção" type="QString" value="1045"/>
              <Option name="Ind - Indústria de metalurgia básica" type="QString" value="1027"/>
              <Option name="Ind - Indústria reciclagem" type="QString" value="1037"/>
              <Option name="Ind - Outros" type="QString" value="1098"/>
              <Option name="Ind - Preparação de couros, artefatos de couro, artigos de viagem e calçados" type="QString" value="1019"/>
              <Option name="Laz - Anfiteatro" type="QString" value="805"/>
              <Option name="Laz - Centro cultural" type="QString" value="807"/>
              <Option name="Laz - Cinema" type="QString" value="806"/>
              <Option name="Laz - Estádio" type="QString" value="801"/>
              <Option name="Laz - Ginásio" type="QString" value="802"/>
              <Option name="Laz - Museu" type="QString" value="803"/>
              <Option name="Laz - Outros" type="QString" value="898"/>
              <Option name="Laz - Plataforma de pesca" type="QString" value="808"/>
              <Option name="Laz - Teatro" type="QString" value="804"/>
              <Option name="Pol Rod - Posto polícia rodoviária federal" type="QString" value="1821"/>
              <Option name="Pol Rod - Posto polícia rodoviária militar" type="QString" value="1820"/>
              <Option name="Port - Carreira portuária" type="QString" value="2536"/>
              <Option name="Port - Dique de estaleiro" type="QString" value="2534"/>
              <Option name="Port - Estaleiro" type="QString" value="2533"/>
              <Option name="Port - Outros" type="QString" value="2598"/>
              <Option name="Port - Rampa portuária" type="QString" value="2535"/>
              <Option name="Port - Terminal de cargas" type="QString" value="2527"/>
              <Option name="Port - Terminal de passageiros" type="QString" value="2526"/>
              <Option name="Posto Fisc - Fiscalização" type="QString" value="1911"/>
              <Option name="Posto Fisc - Misto" type="QString" value="1995"/>
              <Option name="Posto Fisc - Tributação" type="QString" value="1910"/>
              <Option name="Posto de combustivel" type="QString" value="2601"/>
              <Option name="Pub Civ - Assembléia legislativa" type="QString" value="1309"/>
              <Option name="Pub Civ - Cartorial" type="QString" value="1303"/>
              <Option name="Pub Civ - Câmara municipal" type="QString" value="1308"/>
              <Option name="Pub Civ - Eleitoral" type="QString" value="1305"/>
              <Option name="Pub Civ - Gestão pública" type="QString" value="1304"/>
              <Option name="Pub Civ - Outros" type="QString" value="1398"/>
              <Option name="Pub Civ - Policial" type="QString" value="1301"/>
              <Option name="Pub Civ - Prefeitura" type="QString" value="1322"/>
              <Option name="Pub Civ - Prisional" type="QString" value="1302"/>
              <Option name="Pub Civ - Produção ou pequisa pública" type="QString" value="1306"/>
              <Option name="Pub Civ - Seguridade social" type="QString" value="1307"/>
              <Option name="Pub Mil - Aquartelamento" type="QString" value="1712"/>
              <Option name="Pub Mil - Delegacia de serviço militar" type="QString" value="1718"/>
              <Option name="Pub Mil - Hotel de trânsito" type="QString" value="1717"/>
              <Option name="Pub Mil - Outros" type="QString" value="1798"/>
              <Option name="Pub Mil - Posto policial militar" type="QString" value="1719"/>
              <Option name="Rel - Centro religioso" type="QString" value="603"/>
              <Option name="Rel - Convento" type="QString" value="605"/>
              <Option name="Rel - Igreja" type="QString" value="601"/>
              <Option name="Rel - Mesquita" type="QString" value="606"/>
              <Option name="Rel - Mosteiro" type="QString" value="604"/>
              <Option name="Rel - Outros" type="QString" value="698"/>
              <Option name="Rel - Sinagoga" type="QString" value="607"/>
              <Option name="Rel - Templo" type="QString" value="602"/>
              <Option name="Rod - Outros" type="QString" value="2298"/>
              <Option name="Rod - Parada interestadual" type="QString" value="2210"/>
              <Option name="Rod - Posto de fiscalização rodoviária" type="QString" value="2214"/>
              <Option name="Rod - Posto de pedágio" type="QString" value="2213"/>
              <Option name="Rod - Posto de pesagem" type="QString" value="2212"/>
              <Option name="Rod - Terminal interestadual" type="QString" value="2208"/>
              <Option name="Rod - Terminal urbano" type="QString" value="2209"/>
              <Option name="SSoc - Alojamento" type="QString" value="2132"/>
              <Option name="SSoc - Misto" type="QString" value="2195"/>
              <Option name="SSoc - Serviços sociais" type="QString" value="2133"/>
              <Option name="Saneam - Edificação de recalque de resíduos" type="QString" value="403"/>
              <Option name="Saneam - Edificação de tratamento de esgoto" type="QString" value="405"/>
              <Option name="Saneam - Incinerador de resíduos" type="QString" value="407"/>
              <Option name="Saneam - Outros" type="QString" value="498"/>
              <Option name="Saneam - Usina de reciclagem" type="QString" value="406"/>
              <Option name="Sau - Atendimento a urgência e emergências (pronto socorro)" type="QString" value="2027"/>
              <Option name="Sau - Atendimento hospitalar" type="QString" value="2025"/>
              <Option name="Sau - Atendimento hospitalar especializado" type="QString" value="2026"/>
              <Option name="Sau - Atenção ambulatorial (posto e centro de saúde)" type="QString" value="2028"/>
              <Option name="Sau - Outras atividades relacionadas com a atenção à saúde (instituto de pesquisa)" type="QString" value="2030"/>
              <Option name="Sau - Serviços de complementação diagnóstica ou terapêutica" type="QString" value="2029"/>
              <Option name="Sau - Serviços veterinários" type="QString" value="2031"/>
              <Option name="Tur - Cruzeiro" type="QString" value="709"/>
              <Option name="Tur - Estátua" type="QString" value="710"/>
              <Option name="Tur - Mirante" type="QString" value="711"/>
              <Option name="Tur - Monumento" type="QString" value="712"/>
              <Option name="Tur - Outros" type="QString" value="798"/>
              <Option name="Tur - Panteão" type="QString" value="713"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="material_construcao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Alvenaria" type="QString" value="1"/>
              <Option name="Concreto" type="QString" value="2"/>
              <Option name="Desconhecido" type="QString" value="0"/>
              <Option name="Madeira" type="QString" value="5"/>
              <Option name="Metal" type="QString" value="3"/>
              <Option name="Não aplicável" type="QString" value="97"/>
              <Option name="Outros" type="QString" value="98"/>
              <Option name="Rocha" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_comprovacao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Confirmado em campo" type="QString" value="1"/>
              <Option name="Feição não necessita de confirmação" type="QString" value="3"/>
              <Option name="Não possível de confirmar em campo" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="tipo_insumo">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Aquisição em campo" type="QString" value="4"/>
              <Option name="Fotointerpretado" type="QString" value="1"/>
              <Option name="Insumo externo" type="QString" value="2"/>
              <Option name="Mapeamento anterior" type="QString" value="5"/>
              <Option name="Processo automático" type="QString" value="3"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="observacao">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="data_modificacao">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="controle_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ultimo_usuario">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="id"/>
    <alias name="" index="1" field="nome"/>
    <alias name="" index="2" field="tipo"/>
    <alias name="" index="3" field="material_construcao"/>
    <alias name="" index="4" field="tipo_comprovacao"/>
    <alias name="" index="5" field="tipo_insumo"/>
    <alias name="" index="6" field="observacao"/>
    <alias name="" index="7" field="data_modificacao"/>
    <alias name="" index="8" field="controle_id"/>
    <alias name="" index="9" field="ultimo_usuario"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="material_construcao" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="material_construcao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="material_construcao" desc=""/>
    <constraint exp="" field="tipo_comprovacao" desc=""/>
    <constraint exp="" field="tipo_insumo" desc=""/>
    <constraint exp="" field="observacao" desc=""/>
    <constraint exp="" field="data_modificacao" desc=""/>
    <constraint exp="" field="controle_id" desc=""/>
    <constraint exp="" field="ultimo_usuario" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="nome" type="field" hidden="0" width="-1"/>
      <column name="tipo" type="field" hidden="0" width="-1"/>
      <column name="material_construcao" type="field" hidden="0" width="-1"/>
      <column name="tipo_comprovacao" type="field" hidden="0" width="-1"/>
      <column name="tipo_insumo" type="field" hidden="0" width="-1"/>
      <column name="observacao" type="field" hidden="0" width="-1"/>
      <column name="data_modificacao" type="field" hidden="0" width="-1"/>
      <column name="controle_id" type="field" hidden="0" width="-1"/>
      <column name="ultimo_usuario" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="controle_id" editable="1"/>
    <field name="data_modificacao" editable="1"/>
    <field name="id" editable="1"/>
    <field name="material_construcao" editable="1"/>
    <field name="nome" editable="1"/>
    <field name="observacao" editable="1"/>
    <field name="tipo" editable="1"/>
    <field name="tipo_comprovacao" editable="1"/>
    <field name="tipo_insumo" editable="1"/>
    <field name="ultimo_usuario" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="controle_id"/>
    <field labelOnTop="0" name="data_modificacao"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="material_construcao"/>
    <field labelOnTop="0" name="nome"/>
    <field labelOnTop="0" name="observacao"/>
    <field labelOnTop="0" name="tipo"/>
    <field labelOnTop="0" name="tipo_comprovacao"/>
    <field labelOnTop="0" name="tipo_insumo"/>
    <field labelOnTop="0" name="ultimo_usuario"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
