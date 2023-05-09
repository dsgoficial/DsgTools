<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyLocal="1" readOnly="0" labelsEnabled="1" simplifyDrawingTol="1" simplifyMaxScale="1" version="3.7.0-Master" styleCategories="AllStyleCategories" maxScale="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" minScale="1e+8" simplifyAlgorithm="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" type="RuleRenderer" enableorderby="1" symbollevels="1">
    <rules key="{476b00ae-9e30-4fcd-abca-9b3b763fb2e2}">
      <rule label="Via_Deslocamento_L" key="{00a04e05-92e3-4c46-8869-45ea428a2099}">
        <rule description="Est/Est" label="Est/Est" key="{cea5d30c-4ca2-41dd-819b-5f323c91ff80}" filter="&quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2 and (&quot;tipo&quot;  = 4 or  &quot;tipo&quot; =2)" symbol="0"/>
        <rule description="Fed/Fed" label="Fed/Fed" key="{9a7a3e1f-eb40-4ef8-ba8e-b2e4ee88f0a6}" filter="&quot;jurisdicao&quot;  = 1 and &quot;administracao&quot;  = 1 and (&quot;tipo&quot;  = 4 or  &quot;tipo&quot; =2)" symbol="1"/>
        <rule description="Autoestrada" label="Autoestrada" key="{b5c6778e-09d6-44d6-988b-ec6bafbc17cf}" filter="&quot;tipo&quot; = 4">
          <rule description="Auto-estrada/Pav/Perm/CD_nao/Constr/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Autoestrada/Pav/Perm/CD_nao/Constr" key="{103c7822-6060-4db1-aa47-7ae3b95f0ea6}" filter="&quot;tipo&quot; = 4 and  &quot;revestimento&quot;  = 3 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; and  (&quot;jurisdicao&quot;  =  1 and &quot;administracao&quot;  =  1 or &quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2)" symbol="2"/>
          <rule key="{20767ae4-49b7-45fd-b8d5-581a197cd926}" filter="ELSE" symbol="3"/>
        </rule>
        <rule description="Estrada/Rodovia" label="Estrada/Rodovia" key="{81fe3d5c-3775-4e39-bc96-67592c727f36}" filter="&quot;tipo&quot; = 2">
          <rule description="COM cantereiro divisório" label="COM cantereiro divisório" key="{8fe414fd-6200-4ac9-b418-b8bc3a3b3987}" filter="&quot;canteiro_divisorio&quot; = 1">
            <rule description="Rod_Est/Pav/Perm/CD_sim/Constr/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/Pav/Perm/CD_sim/Constr" key="{178f9cee-9997-4d00-886a-77c0a70ae4fa}" filter="&quot;revestimento&quot;  = 3 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  1  and &quot;situacao_fisica&quot;  = 3 and &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; and  (&quot;jurisdicao&quot;  =  1 and &quot;administracao&quot;  =  1 or &quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2)" symbol="4"/>
            <rule description="Rod_Est/LeitoNat/Perm/CD_sim/Constr/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/LeitoNat/Perm/CD_sim/Constr" key="{6e0079ab-0dca-4998-a4c7-b06a2a3222ad}" filter="&quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  1  and &quot;situacao_fisica&quot;  = 3 and &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot;  and  (&quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2 or &quot;jurisdicao&quot;  =  1 and &quot;administracao&quot;  =  1)" symbol="5"/>
            <rule description="Rod_Est/LeitoNat/Perm/CD_sim/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/LeitoNat/Perm/CD_sim/Constr/Desc/Desc" key="{5984f220-86b0-423a-9345-21cb8eab2533}" filter="&quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  1  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="6"/>
            <rule key="{7aabd399-73fb-40ed-af9e-0ecdab323ddf}" filter="ELSE" symbol="7"/>
          </rule>
          <rule description="SEM cantereiro divisório" label="SEM cantereiro divisório" key="{d707627a-5f01-4a77-aaa6-090a849a4884}" filter="&quot;canteiro_divisorio&quot; = 2">
            <rule description="Rod_Est/Pav/Perm/CD_nao/Constr/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/Pav/Perm/CD_nao/Constr" key="{d97ecb99-c857-421c-8900-0de6c153d305}" filter="&quot;revestimento&quot;  = 3 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot;  and  (&quot;jurisdicao&quot;  =  1 and &quot;administracao&quot;  =  1 or &quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2)" symbol="8"/>
            <rule description="Rod_Est/LeitoNat/Perm/CD_nao/Constr/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/LeitoNat/Perm/CD_nao/Constr" key="{e6290508-64a0-4cbb-9cf1-916d101d4cf9}" filter=" &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot;  and  (&quot;jurisdicao&quot;  =  1 and &quot;administracao&quot;  =  1 or &quot;jurisdicao&quot;  =  2 and &quot;administracao&quot;  =  2)" symbol="9"/>
            <rule description="Rod_Est/LeitoNat/Perm/CD_nao/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/LeitoNat/Perm/CD_nao/Constr/Desc/Desc" key="{55ec8a80-1b14-4650-8097-b211b02b1a06}" filter=" &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="10"/>
            <rule description="Rod_Est/LeitoNat/Period/CD_nao/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Rod_Est/LeitoNat/Period/CD_nao/Constr/Desc/Desc" key="{b96ef928-f1a9-4cb7-b257-a13d53c62eea}" filter=" &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  2 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="11"/>
            <rule key="{8ae9f24d-98f0-4f13-9176-2ae2cf63c129}" filter="ELSE" symbol="12"/>
          </rule>
          <rule key="{8c004560-12e0-4bed-b20d-e0266b60e9f3}" filter="ELSE" symbol="13"/>
        </rule>
        <rule label="Arruamento" key="{b6b6e525-a6d6-44d3-9289-969936a18c19}" filter="&quot;tipo&quot; = 5 ">
          <rule label="COM canteiro divisório" key="{c7cb1067-f6f1-46aa-b3dc-6b97a9ed797e}" filter="&quot;canteiro_divisorio&quot; = 1">
            <rule description="Arruamento/Pav/Perm/CD_sim/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Arruamento/Pav/Perm/CD_sim/Constr/Desc/Desc" key="{df2df683-71aa-43c0-b124-9cc0acbbad78}" filter="&quot;tipo&quot; = 5 and  &quot;revestimento&quot;  = 3 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  1  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="14"/>
            <rule description="Arruamento/LeitoNat/Perm/CD_sim/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Arruamento/LeitoNat/Perm/CD_sim/Constr/Desc/Desc" key="{eae29897-49e5-449f-94f7-25cf84a94a90}" filter="&quot;tipo&quot; = 5 and  &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  1  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="15"/>
            <rule key="{8ccd9047-7810-4a89-8e6c-de5024e0fe28}" filter="ELSE" symbol="16"/>
          </rule>
          <rule label="SEM canteiro divisório" key="{24c3c354-32da-4d8d-8716-1f0a8b8b11b8}" filter="&quot;canteiro_divisorio&quot; = 2">
            <rule description="Arruamento/Pav/Perm/CD_nao/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Arruamento/Pav/Perm/CD_nao/Constr/Desc/Desc" key="{ed7f6286-169e-4b91-a865-7f46a5a4b56b}" filter="&quot;tipo&quot; = 5 and  &quot;revestimento&quot;  = 3 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="17"/>
            <rule description="Arruamento/LeitoNat/Perm/CD_nao/Constr/Desc/Desc/NrPistas e NrFaixas&lt;>0/NrPistas&lt;NrFaixas" label="Arruamento/LeitoNat/Perm/CD_nao/Constr/Desc/Desc" key="{f04c4fa0-bcf1-440d-b76f-b2d315fe2aed}" filter="&quot;tipo&quot; = 5 and  &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  1 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; &lt;> 0 and  &quot;nr_pistas&quot;  &lt;> 0 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="18"/>
            <rule key="{ab99345c-1e6f-491b-a624-060b7840e9ab}" filter="ELSE" symbol="19"/>
          </rule>
          <rule key="{6390b670-9396-4b0b-921e-0f9ae5a5c273}" filter="ELSE" symbol="20"/>
        </rule>
        <rule description="CaminhoCarroc/LeitoNat/Period/CD_nao/Constr/Desc/Desc/NrPistas e NrFaixas = 1/NrPistas&lt;NrFaixas" label="CaminhoCarroc/LeitoNat/Period/CD_nao/Constr/Desc/Desc" key="{8bc5e54f-218a-4175-b436-f3dd7e29f948}" filter="&quot;tipo&quot; = 3 and  &quot;revestimento&quot;  = 1 and  &quot;trafego&quot;  =  2 and  &quot;canteiro_divisorio&quot;  =  2  and &quot;situacao_fisica&quot;  = 3 and &quot;jurisdicao&quot;  =  0 and &quot;administracao&quot;  =  0 and  &quot;nr_faixas&quot; = 1 and  &quot;nr_pistas&quot;  = 1 and  &quot;nr_pistas&quot; &lt;= &quot;nr_faixas&quot; " symbol="21"/>
        <rule key="{f7f6eccc-cc27-46ee-9401-62ade195a6d6}" filter="ELSE" symbol="22"/>
      </rule>
      <rule key="{abf69010-200c-4263-a5b7-46ad7ac79675}" filter="ELSE" symbol="23"/>
    </rules>
    <symbols>
      <symbol name="0" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="MarkerLine" enabled="1" pass="2" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@0@0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
            <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="35,255,35,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="254,24,66,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="6"/>
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
        </layer>
      </symbol>
      <symbol name="1" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="MarkerLine" enabled="1" pass="2" locked="0">
          <prop k="average_angle_length" v="4"/>
          <prop k="average_angle_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="average_angle_unit" v="MM"/>
          <prop k="interval" v="3"/>
          <prop k="interval_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_along_line" v="0"/>
          <prop k="offset_along_line_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_along_line_unit" v="MM"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="ring_filter" v="0"/>
          <prop k="rotate" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
          <symbol name="@1@0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
            <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,255,35,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="pentagon"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="254,24,66,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="6"/>
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
        </layer>
      </symbol>
      <symbol name="10" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.06311"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="11" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="dot"/>
          <prop k="line_width" v="1.06311"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="12" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="13" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="14" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.312"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="15" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,127,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.312"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="16" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="17" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="18" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,127,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="19" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="2" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="4.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="227,26,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="3"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="dot"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="20" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="21" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="0.66;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="1"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="22" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="23" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="3" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="4" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="227,26,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.3"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="1">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="0,0,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="5" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,127,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.3"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="6" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,255,255,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="2.3"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="7" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="251,12,180,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="0.66"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="8" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="227,26,28,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.06311"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol name="9" force_rhr="0" type="line" alpha="1" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="line_color" v="35,35,35,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.5"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop k="capstyle" v="round"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="round"/>
          <prop k="line_color" v="255,127,0,255"/>
          <prop k="line_style" v="solid"/>
          <prop k="line_width" v="1.06311"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="ring_filter" v="0"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <orderby>
      <orderByClause nullsFirst="0" asc="1">"tipo"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"revestimento"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"trafego"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"canteiro_divisorio"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"situacao_fisica"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"jurisdicao"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"administracao"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"tipo_comprovacao"</orderByClause>
      <orderByClause nullsFirst="0" asc="1">"tipo_insumo"</orderByClause>
    </orderby>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{00adbf2b-b0e6-4b57-880f-0dbaac522e97}">
      <rule description="Nome e/ou sigla de rodovias e autoestradas" key="{c5ad99cf-d07a-43eb-9a61-c6a67bdc1812}" filter="&quot;tipo&quot; = 2 or &quot;tipo&quot; = 4">
        <settings calloutType="simple">
          <text-style fontSize="10" previewBkgrdColor="255,255,255,255" fontStrikeout="0" fontSizeUnit="Point" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontWordSpacing="0" textColor="0,0,0,255" fontFamily="Noto Sans" fontLetterSpacing="0" blendMode="0" fontItalic="0" namedStyle="Normal" fontUnderline="0" isExpression="1" textOpacity="1" multilineHeight="1" fontCapitals="0" fieldName=" 'sigla='||&quot;sigla&quot;|| '\n nome='||&quot;nome&quot;" fontWeight="50">
            <text-buffer bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="1" bufferOpacity="1" bufferDraw="1" bufferBlendMode="0" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferNoFill="1"/>
            <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="Point" shapeOffsetX="0" shapeBlendMode="0" shapeSVGFile="" shapeDraw="0" shapeRotation="0" shapeOpacity="1" shapeOffsetY="0" shapeType="0" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeRadiiY="0" shapeRadiiX="0" shapeOffsetUnit="Point" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeSizeUnit="Point" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeBorderWidthUnit="Point"/>
            <shadow shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowScale="100" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowUnder="0" shadowDraw="0" shadowRadius="1.5" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format placeDirectionSymbol="0" multilineAlign="4294967295" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" addDirectionSymbol="0" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" decimals="3" plussign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1"/>
          <placement distMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" distUnits="MM" preserveRotation="1" centroidWhole="0" fitInPolygonOnly="0" layerType="UnknownGeometry" rotationAngle="0" offsetType="0" quadOffset="4" centroidInside="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" xOffset="0" maxCurvedCharAngleIn="25" placement="2" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" placementFlags="9" repeatDistance="0" dist="1.9" offsetUnits="MM" yOffset="0" priority="5" repeatDistanceUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering scaleMax="0" zIndex="0" fontMaxPixelSize="10000" minFeatureSize="0" obstacle="1" limitNumLabels="0" obstacleType="0" displayAll="0" labelPerPart="0" maxNumLabels="2000" scaleVisibility="0" mergeLines="0" scaleMin="0" fontLimitPixelSize="0" fontMinPixelSize="3" drawLabels="1" upsidedownLabels="0" obstacleFactor="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule description="Número de pistas e faixas de rodovias e autoestradas" key="{c84eec31-49bf-40de-9d40-c0397d6d1c91}" filter="&quot;tipo&quot; = 2 or &quot;tipo&quot; = 4">
        <settings calloutType="simple">
          <text-style fontSize="10" previewBkgrdColor="255,255,255,255" fontStrikeout="0" fontSizeUnit="Point" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontWordSpacing="0" textColor="0,0,0,255" fontFamily="Noto Sans" fontLetterSpacing="0" blendMode="0" fontItalic="0" namedStyle="Normal" fontUnderline="0" isExpression="1" textOpacity="1" multilineHeight="1" fontCapitals="0" fieldName="'faixas='||&quot;nr_faixas&quot;  ||  '\n n_pistas=' || &quot;nr_pistas&quot; " fontWeight="50">
            <text-buffer bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="1" bufferOpacity="1" bufferDraw="1" bufferBlendMode="0" bufferColor="255,255,255,255" bufferJoinStyle="128" bufferNoFill="1"/>
            <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="Point" shapeOffsetX="0" shapeBlendMode="0" shapeSVGFile="" shapeDraw="0" shapeRotation="0" shapeOpacity="1" shapeOffsetY="0" shapeType="0" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeRadiiY="0" shapeRadiiX="0" shapeOffsetUnit="Point" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeSizeUnit="Point" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeBorderWidthUnit="Point"/>
            <shadow shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowScale="100" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowUnder="0" shadowDraw="0" shadowRadius="1.5" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format placeDirectionSymbol="0" multilineAlign="4294967295" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" addDirectionSymbol="0" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" decimals="3" plussign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1"/>
          <placement distMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" distUnits="MM" preserveRotation="1" centroidWhole="0" fitInPolygonOnly="0" layerType="UnknownGeometry" rotationAngle="0" offsetType="0" quadOffset="4" centroidInside="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" xOffset="0" maxCurvedCharAngleIn="25" placement="2" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" placementFlags="9" repeatDistance="0" dist="1.9" offsetUnits="MM" yOffset="0" priority="5" repeatDistanceUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering scaleMax="0" zIndex="0" fontMaxPixelSize="10000" minFeatureSize="0" obstacle="1" limitNumLabels="0" obstacleType="0" displayAll="0" labelPerPart="0" maxNumLabels="2000" scaleVisibility="0" mergeLines="0" scaleMin="0" fontLimitPixelSize="0" fontMinPixelSize="3" drawLabels="1" upsidedownLabels="0" obstacleFactor="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
      <rule description="nome" key="{268a2b51-a949-42b7-9fbe-d2c1e692e20e}" filter="ELSE">
        <settings calloutType="simple">
          <text-style fontSize="10" previewBkgrdColor="255,255,255,255" fontStrikeout="0" fontSizeUnit="Point" fontSizeMapUnitScale="3x:0,0,0,0,0,0" useSubstitutions="0" fontWordSpacing="0" textColor="0,0,0,255" fontFamily="Noto Sans" fontLetterSpacing="0" blendMode="0" fontItalic="0" namedStyle="Normal" fontUnderline="0" isExpression="0" textOpacity="1" multilineHeight="1" fontCapitals="0" fieldName="nome" fontWeight="50">
            <text-buffer bufferSizeUnits="MM" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferSize="1" bufferOpacity="1" bufferDraw="1" bufferBlendMode="0" bufferColor="254,24,66,255" bufferJoinStyle="128" bufferNoFill="1"/>
            <background shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="Point" shapeOffsetX="0" shapeBlendMode="0" shapeSVGFile="" shapeDraw="0" shapeRotation="0" shapeOpacity="1" shapeOffsetY="0" shapeType="0" shapeRotationType="0" shapeBorderColor="128,128,128,255" shapeSizeType="0" shapeSizeX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0" shapeRadiiY="0" shapeRadiiX="0" shapeOffsetUnit="Point" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeJoinStyle="64" shapeSizeUnit="Point" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeBorderWidthUnit="Point"/>
            <shadow shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowOffsetDist="1" shadowOffsetUnit="MM" shadowScale="100" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowUnder="0" shadowDraw="0" shadowRadius="1.5" shadowOffsetGlobal="1" shadowRadiusUnit="MM" shadowOpacity="0.7" shadowBlendMode="6"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format placeDirectionSymbol="0" multilineAlign="4294967295" leftDirectionSymbol="&lt;" rightDirectionSymbol=">" addDirectionSymbol="0" reverseDirectionSymbol="0" formatNumbers="0" wrapChar="" decimals="3" plussign="0" autoWrapLength="0" useMaxLineLengthForAutoWrap="1"/>
          <placement distMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" distUnits="MM" preserveRotation="1" centroidWhole="0" fitInPolygonOnly="0" layerType="UnknownGeometry" rotationAngle="0" offsetType="0" quadOffset="4" centroidInside="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" xOffset="0" maxCurvedCharAngleIn="25" placement="2" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" placementFlags="9" repeatDistance="0" dist="0" offsetUnits="MM" yOffset="0" priority="2" repeatDistanceUnits="MM" labelOffsetMapUnitScale="3x:0,0,0,0,0,0"/>
          <rendering scaleMax="0" zIndex="0" fontMaxPixelSize="10000" minFeatureSize="0" obstacle="1" limitNumLabels="0" obstacleType="0" displayAll="0" labelPerPart="0" maxNumLabels="2000" scaleVisibility="0" mergeLines="0" scaleMin="0" fontLimitPixelSize="0" fontMinPixelSize="3" drawLabels="1" upsidedownLabels="0" obstacleFactor="1"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option name="ddProperties" type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
              <Option name="enabled" type="QString" value="0"/>
              <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer class=&quot;SimpleLine&quot; enabled=&quot;1&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
              <Option name="minLength" type="double" value="0"/>
              <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="minLengthUnit" type="QString" value="MM"/>
              <Option name="offsetFromAnchor" type="double" value="0"/>
              <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
              <Option name="offsetFromLabel" type="double" value="0"/>
              <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
              <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
  </labeling>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames">
      <value>area_trabalho_nome</value>
      <value>area_trabalho_poligono</value>
      <value>uiData</value>
    </property>
    <property key="variableValues">
      <value>2721-2_1_0</value>
      <value>SRID=31981;POLYGON((692877.818253784 7510620.34874696,692703.951825066 7496778.36983556,679854.081152441 7496934.8003752,679908.262664453 7501548.5887931,679908.266911518 7501548.95076501,679962.349270598 7506162.35552804,680016.340943531 7510776.10061159,684303.430094289 7510725.37846421,688590.252309319 7510673.46533418,688590.588659248 7510673.46121416,692877.818253784 7510620.34874696))</value>
      <value>{"uiData": {"layer_data": {"layer_schema": "edgv", "layer_name": "infra_via_deslocamento_l", "layer_geom_type": "MULTILINESTRING", "layer_fields": {"canteiro_divisorio": {"valueMap": {"Sim": 1, "Não": 2, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "situacao_fisica": {"valueMap": {"Abandonada": 1, "Destruída": 2, "Construída": 3, "Em construção": 4, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "observacao": {}, "nr_faixas": {}, "revestimento": {"valueMap": {"Leito natural": 1, "Revestimento primário (solto)": 2, "Pavimentado": 3, "Calçado": 4, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "sigla": {}, "controle_id": {}, "ultimo_usuario": {}, "concessionaria": {}, "tipo": {"valueMap": {"Estrada/Rodovia": 2, "Caminho carroçável": 3, "Auto-estrada": 4, "Arruamento": 5, "Trilha ou Picada": 6, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "tipo_insumo": {"valueMap": {"Fotointerpretado": 1, "Insumo externo": 2, "Processo automático": 3, "Aquisição em campo": 4, "Mapeamento anterior": 5, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "trafego": {"valueMap": {"Permanente": 1, "Periódico": 2, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "nr_pistas": {}, "data_modificacao": {}, "nome": {}, "jurisdicao": {"valueMap": {"Desconhecida": 0, "Federal": 1, "Estadual": 2, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "tipo_comprovacao": {"valueMap": {"Confirmado em campo": 1, "Não possível de confirmar em campo": 2, "Feição não necessita de confirmação": 3, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}, "administracao": {"valueMap": {"Desconhecida": 0, "Federal": 1, "Estadual": 2, "Concessionada": 7, "A SER PREENCHIDO": 999, "IGNORAR": 10000}}}, "group_geom": "LINHA", "group_class": "infra"}, "fields_sorted": ["nome", "canteiro_divisorio", "situacao_fisica", "observacao", "nr_faixas", "revestimento", "sigla", "controle_id", "ultimo_usuario", "concessionaria", "tipo", "tipo_insumo", "trafego", "nr_pistas", "data_modificacao", "jurisdicao", "tipo_comprovacao", "administracao"], "form_name": "C:/Users/proc/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins\\Ferramentas_Producao\\Tools\\LoadData\\forms\\sisfron_sirgas2000_utm_21S_infra_via_deslocamento_l.ui"}}</value>
    </property>
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
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" zIndex="0" priority="0" obstacle="0" placement="2" dist="0">
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
              <Option name="Arruamento" type="QString" value="5"/>
              <Option name="Auto-estrada" type="QString" value="4"/>
              <Option name="Caminho carroçável" type="QString" value="3"/>
              <Option name="Estrada/Rodovia" type="QString" value="2"/>
              <Option name="Trilha ou Picada" type="QString" value="6"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="revestimento">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Calçado" type="QString" value="4"/>
              <Option name="Leito natural" type="QString" value="1"/>
              <Option name="Pavimentado" type="QString" value="3"/>
              <Option name="Revestimento primário (solto)" type="QString" value="2"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="trafego">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Periódico" type="QString" value="2"/>
              <Option name="Permanente" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_faixas">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="nr_pistas">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="canteiro_divisorio">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Não" type="QString" value="2"/>
              <Option name="Sim" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="situacao_fisica">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Abandonada" type="QString" value="1"/>
              <Option name="Construída" type="QString" value="3"/>
              <Option name="Destruída" type="QString" value="2"/>
              <Option name="Em construção" type="QString" value="4"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="jurisdicao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Estadual" type="QString" value="2"/>
              <Option name="Federal" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="sigla">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="administracao">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="Map">
              <Option name="A SER PREENCHIDO" type="QString" value="999"/>
              <Option name="Concessionada" type="QString" value="7"/>
              <Option name="Desconhecida" type="QString" value="0"/>
              <Option name="Estadual" type="QString" value="2"/>
              <Option name="Federal" type="QString" value="1"/>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="concessionaria">
      <editWidget type="TextEdit">
        <config>
          <Option/>
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
    <field name="length_otf">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="length_otf">
      <editWidget type="">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="id" index="0" field="id"/>
    <alias name="nome" index="1" field="nome"/>
    <alias name="tipo" index="2" field="tipo"/>
    <alias name="revestimento" index="3" field="revestimento"/>
    <alias name="trafego" index="4" field="trafego"/>
    <alias name="nr_faixas" index="5" field="nr_faixas"/>
    <alias name="nr_pistas" index="6" field="nr_pistas"/>
    <alias name="canteiro_divisorio" index="7" field="canteiro_divisorio"/>
    <alias name="situacao_fisica" index="8" field="situacao_fisica"/>
    <alias name="jurisdicao" index="9" field="jurisdicao"/>
    <alias name="sigla" index="10" field="sigla"/>
    <alias name="administracao" index="11" field="administracao"/>
    <alias name="concessionaria" index="12" field="concessionaria"/>
    <alias name="tipo_comprovacao" index="13" field="tipo_comprovacao"/>
    <alias name="tipo_insumo" index="14" field="tipo_insumo"/>
    <alias name="observacao" index="15" field="observacao"/>
    <alias name="data_modificacao" index="16" field="data_modificacao"/>
    <alias name="controle_id" index="17" field="controle_id"/>
    <alias name="ultimo_usuario" index="18" field="ultimo_usuario"/>
    <alias name="length_otf" index="19" field="length_otf"/>
    <alias name="" index="20" field="length_otf"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="id" expression=""/>
    <default applyOnUpdate="0" field="nome" expression=""/>
    <default applyOnUpdate="0" field="tipo" expression=""/>
    <default applyOnUpdate="0" field="revestimento" expression=""/>
    <default applyOnUpdate="0" field="trafego" expression=""/>
    <default applyOnUpdate="0" field="nr_faixas" expression=""/>
    <default applyOnUpdate="0" field="nr_pistas" expression=""/>
    <default applyOnUpdate="0" field="canteiro_divisorio" expression=""/>
    <default applyOnUpdate="0" field="situacao_fisica" expression=""/>
    <default applyOnUpdate="0" field="jurisdicao" expression=""/>
    <default applyOnUpdate="0" field="sigla" expression=""/>
    <default applyOnUpdate="0" field="administracao" expression=""/>
    <default applyOnUpdate="0" field="concessionaria" expression=""/>
    <default applyOnUpdate="0" field="tipo_comprovacao" expression=""/>
    <default applyOnUpdate="0" field="tipo_insumo" expression=""/>
    <default applyOnUpdate="0" field="observacao" expression=""/>
    <default applyOnUpdate="0" field="data_modificacao" expression=""/>
    <default applyOnUpdate="0" field="controle_id" expression=""/>
    <default applyOnUpdate="0" field="ultimo_usuario" expression="'6'"/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
    <default applyOnUpdate="0" field="length_otf" expression=""/>
  </defaults>
  <constraints>
    <constraint notnull_strength="1" unique_strength="1" field="id" constraints="3" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nome" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="revestimento" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="trafego" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nr_faixas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="nr_pistas" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="canteiro_divisorio" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="situacao_fisica" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="jurisdicao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="sigla" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="administracao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="concessionaria" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_comprovacao" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="1" unique_strength="0" field="tipo_insumo" constraints="1" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="observacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="data_modificacao" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="controle_id" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="ultimo_usuario" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
    <constraint notnull_strength="0" unique_strength="0" field="length_otf" constraints="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="nome" desc=""/>
    <constraint exp="" field="tipo" desc=""/>
    <constraint exp="" field="revestimento" desc=""/>
    <constraint exp="" field="trafego" desc=""/>
    <constraint exp="" field="nr_faixas" desc=""/>
    <constraint exp="" field="nr_pistas" desc=""/>
    <constraint exp="" field="canteiro_divisorio" desc=""/>
    <constraint exp="" field="situacao_fisica" desc=""/>
    <constraint exp="" field="jurisdicao" desc=""/>
    <constraint exp="" field="sigla" desc=""/>
    <constraint exp="" field="administracao" desc=""/>
    <constraint exp="" field="concessionaria" desc=""/>
    <constraint exp="" field="tipo_comprovacao" desc=""/>
    <constraint exp="" field="tipo_insumo" desc=""/>
    <constraint exp="" field="observacao" desc=""/>
    <constraint exp="" field="data_modificacao" desc=""/>
    <constraint exp="" field="controle_id" desc=""/>
    <constraint exp="" field="ultimo_usuario" desc=""/>
    <constraint exp="" field="length_otf" desc=""/>
    <constraint exp="" field="length_otf" desc=""/>
  </constraintExpressions>
  <expressionfields>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
    <field comment="" precision="0" name="length_otf" typeName="" type="6" subType="0" length="0" expression="$length"/>
  </expressionfields>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column name="id" type="field" hidden="0" width="-1"/>
      <column name="nome" type="field" hidden="0" width="-1"/>
      <column name="tipo" type="field" hidden="0" width="-1"/>
      <column name="revestimento" type="field" hidden="0" width="-1"/>
      <column name="trafego" type="field" hidden="0" width="-1"/>
      <column name="nr_faixas" type="field" hidden="0" width="-1"/>
      <column name="nr_pistas" type="field" hidden="0" width="-1"/>
      <column name="canteiro_divisorio" type="field" hidden="0" width="-1"/>
      <column name="situacao_fisica" type="field" hidden="0" width="-1"/>
      <column name="jurisdicao" type="field" hidden="0" width="-1"/>
      <column name="sigla" type="field" hidden="0" width="-1"/>
      <column name="administracao" type="field" hidden="0" width="-1"/>
      <column name="concessionaria" type="field" hidden="0" width="-1"/>
      <column name="tipo_comprovacao" type="field" hidden="0" width="-1"/>
      <column name="tipo_insumo" type="field" hidden="0" width="-1"/>
      <column name="observacao" type="field" hidden="0" width="-1"/>
      <column name="data_modificacao" type="field" hidden="0" width="-1"/>
      <column name="controle_id" type="field" hidden="0" width="-1"/>
      <column name="ultimo_usuario" type="field" hidden="0" width="-1"/>
      <column name="length_otf" type="field" hidden="0" width="-1"/>
      <column type="actions" hidden="1" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1">C:/Users/proc/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\Ferramentas_Producao\Tools\LoadData\forms\sisfron_sirgas2000_utm_21S_infra_via_deslocamento_l.ui</editform>
  <editforminit>formOpen</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis import core, gui
import re
global a

class ValidateForm:
	def __init__(self, layer, formValues, logBrowser):
		self.layer = layer
		self.formValues = formValues
		self.rules = []
		self.logBrowser = logBrowser
		self.validateForm()

	def calculateExpression(self, exp):
		for field in self.formValues:
			if field != 'filter':
				if len(self.formValues[field]) == 3:
					value = self.formValues[field][1][self.formValues[field][0]]
				else:
					value = self.formValues[field][0]
				exp = exp.replace('"{0}"'.format(field), "'{0}'".format(str(value)))
				exp = exp.replace("'NULL'".format(field), "NULL")
		r = QgsExpression(exp)
		return r.evaluate()

	def validateForm(self):
		self.cleanRulesOnForm()
		logText = ""
		for rule in self.rules:
			for field in rule:
				if field in self.formValues:
					for exp in reversed(rule[field]):
						try:
							result = self.calculateExpression(exp['rule'])
							if bool(result):
								if len(self.formValues[field]) == 3:
									self.formValues[field][2].setStyleSheet(
										"QWidget {background-color: rgb(%s)}"%(
											exp["cor_rgb"]
										)
									)
								else:
									self.formValues[field][1].setStyleSheet(
										"QWidget {background-color: rgb(%s)}"%(
											exp["cor_rgb"]
										)
									)
								logText += u"<p>{0}</p>".format(exp["descricao"])
						except:
							pass
		self.logBrowser.setText(logText)

	def cleanRulesOnForm(self):
		for field in self.formValues:
			if len(self.formValues[field]) == 3:
				self.formValues[field][2].setStyleSheet("")
			else:
				self.formValues[field][1].setStyleSheet("")

class ManagerForm(QtCore.QObject):
    def __init__(self, dialog, layer, feature):
        super(ManagerForm, self).__init__()
        self.myDialog = dialog
        self.lyr = layer
        self.validadeForm = ""
        self.logBrowser = dialog.findChild(QLabel, "logLabel")
        self.logFrame = dialog.findChild(QFrame, "logFrame")
        self.logFrame.hide()
        self.logBtn = dialog.findChild(QPushButton, "logBtn")
        self.logBtn.setCheckable(True)
        self.logBtn.clicked.connect(self.showLog)
        buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
        buttonBox.rejected.connect(self.finishedForm)
        buttonBox.accepted.connect(self.finishedForm)
        button_ok = buttonBox.button(QDialogButtonBox.Ok)
        button_ok.setAutoDefault(True)
        button_ok.setDefault(True)
        button_cancel = buttonBox.button(QDialogButtonBox.Cancel)
        button_cancel.setAutoDefault(False)
        button_cancel.setDefault(False)
        self.myDialog.installEventFilter(self)

    def showLog(self, state):
        if state:
            self.logFrame.show()
        else:
            self.logFrame.hide()

    def eventFilter(self, o, event):
        if event.type() in [7, 10, 11, 100]:
            self.validateLayerByRules()
        return False

    def validateLayerByRules(self):
        formValues = {}
        for cb in self.myDialog.findChildren(QComboBox):
            idx = self.lyr.fields().indexOf(cb.objectName())
            formValues[cb.objectName()] = [
                cb.currentText(),
                self.lyr.editorWidgetSetup(idx).config()['map'] if idx > 0 else self.optFilter.keys(),
                cb
            ]
        for le in self.myDialog.findChildren(QLineEdit):
                formValues[le.objectName()] = [
                le.text(),
                le
            ]
        self.validadeForm = ValidateForm(self.lyr, formValues, self.logBrowser)

    def finishedForm(self):
        pass

def formOpen(dialog, layer, featureid):
    try:
        global a
        a = ManagerForm(dialog, layer, featureid)
    except:
        pass]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <editable>
    <field name="administracao" editable="1"/>
    <field name="canteiro_divisorio" editable="1"/>
    <field name="concessionaria" editable="1"/>
    <field name="controle_id" editable="1"/>
    <field name="data_modificacao" editable="1"/>
    <field name="id" editable="1"/>
    <field name="jurisdicao" editable="1"/>
    <field name="length_otf" editable="0"/>
    <field name="nome" editable="1"/>
    <field name="nr_faixas" editable="1"/>
    <field name="nr_pistas" editable="1"/>
    <field name="observacao" editable="1"/>
    <field name="revestimento" editable="1"/>
    <field name="sigla" editable="1"/>
    <field name="situacao_fisica" editable="1"/>
    <field name="tipo" editable="1"/>
    <field name="tipo_comprovacao" editable="1"/>
    <field name="tipo_insumo" editable="1"/>
    <field name="trafego" editable="1"/>
    <field name="ultimo_usuario" editable="1"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="administracao"/>
    <field labelOnTop="0" name="canteiro_divisorio"/>
    <field labelOnTop="0" name="concessionaria"/>
    <field labelOnTop="0" name="controle_id"/>
    <field labelOnTop="0" name="data_modificacao"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="jurisdicao"/>
    <field labelOnTop="0" name="length_otf"/>
    <field labelOnTop="0" name="nome"/>
    <field labelOnTop="0" name="nr_faixas"/>
    <field labelOnTop="0" name="nr_pistas"/>
    <field labelOnTop="0" name="observacao"/>
    <field labelOnTop="0" name="revestimento"/>
    <field labelOnTop="0" name="sigla"/>
    <field labelOnTop="0" name="situacao_fisica"/>
    <field labelOnTop="0" name="tipo"/>
    <field labelOnTop="0" name="tipo_comprovacao"/>
    <field labelOnTop="0" name="tipo_insumo"/>
    <field labelOnTop="0" name="trafego"/>
    <field labelOnTop="0" name="ultimo_usuario"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
