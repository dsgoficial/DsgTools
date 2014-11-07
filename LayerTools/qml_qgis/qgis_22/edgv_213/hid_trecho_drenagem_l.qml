<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.2.0-Valmiera" minimumScale="1" maximumScale="1" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <renderer-v2 symbollevels="0" type="RuleRenderer">
    <rules>
      <rule filter="eixoprincipal = 1 and dentrodepoligono = 1 and compartilhado = 1" symbol="0" label="Sim, Sim, Sim"/>
      <rule filter="eixoprincipal = 1 and dentrodepoligono = 1 and compartilhado = 2" symbol="1" label="Sim, Sim, Não"/>
      <rule filter="eixoprincipal = 1 and dentrodepoligono = 2 and compartilhado = 2" symbol="2" label="Sim, Não, Não"/>
      <rule filter="eixoprincipal = 2 and dentrodepoligono = 1 and compartilhado = 1" symbol="3" label="Não, Sim, Sim"/>
      <rule filter="eixoprincipal = 2 and dentrodepoligono = 1 and compartilhado = 2" symbol="4" label="Não, Sim, Não"/>
      <rule filter="not(eixoprincipal = 1 and dentrodepoligono = 1 and compartilhado = 1) and not(eixoprincipal = 1 and dentrodepoligono = 1 and compartilhado = 2) and not(eixoprincipal = 1 and dentrodepoligono = 2 and compartilhado = 2) and not(eixoprincipal = 2 and dentrodepoligono = 1 and compartilhado = 1) and not(eixoprincipal = 2 and dentrodepoligono = 1 and compartilhado = 2)" symbol="5" label="Outros Valores"/>
    </rules>
    <symbols>
      <symbol alpha="1" type="line" name="0">
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="168,56,0,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="solid"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="1"/>
          <prop k="width_unit" v="MM"/>
        </layer>
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="3"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="rotate" v="1"/>
          <symbol alpha="1" type="marker" name="@0@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="168,56,0,255"/>
              <prop k="color_border" v="168,56,0,255"/>
              <prop k="horizontal_anchor_point" v="0"/>
              <prop k="name" v="filled_arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="4"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="1">
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="38,115,0,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="solid"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="2"/>
          <prop k="width_unit" v="MM"/>
        </layer>
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="3"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="rotate" v="1"/>
          <symbol alpha="1" type="marker" name="@1@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="38,115,0,255"/>
              <prop k="color_border" v="38,115,0,255"/>
              <prop k="horizontal_anchor_point" v="0"/>
              <prop k="name" v="filled_arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="5"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="2">
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="3"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="rotate" v="1"/>
          <symbol alpha="1" type="marker" name="@2@0">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="0,169,230,255"/>
              <prop k="color_border" v="0,169,230,255"/>
              <prop k="horizontal_anchor_point" v="0"/>
              <prop k="name" v="filled_arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="4"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="0,197,255,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="solid"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="0.26"/>
          <prop k="width_unit" v="MM"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="3">
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="3"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="rotate" v="1"/>
          <symbol alpha="1" type="marker" name="@3@0">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="color_border" v="0,0,0,255"/>
              <prop k="horizontal_anchor_point" v="0"/>
              <prop k="name" v="filled_arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="5"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="0,77,168,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="solid"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="0.26"/>
          <prop k="width_unit" v="MM"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="4">
        <layer pass="0" class="MarkerLine" locked="0">
          <prop k="interval" v="3"/>
          <prop k="interval_unit" v="MM"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="placement" v="centralpoint"/>
          <prop k="rotate" v="1"/>
          <symbol alpha="1" type="marker" name="@4@0">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="0,76,115,255"/>
              <prop k="color_border" v="0,76,115,255"/>
              <prop k="horizontal_anchor_point" v="0"/>
              <prop k="name" v="filled_arrowhead"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="4"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="132,0,168,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="dash"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="0.26"/>
          <prop k="width_unit" v="MM"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="line" name="5">
        <layer pass="0" class="SimpleLine" locked="0">
          <prop k="capstyle" v="square"/>
          <prop k="color" v="230,0,169,255"/>
          <prop k="customdash" v="5;2"/>
          <prop k="customdash_unit" v="MM"/>
          <prop k="draw_inside_polygon" v="0"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="penstyle" v="solid"/>
          <prop k="use_custom_dash" v="0"/>
          <prop k="width" v="0.26"/>
          <prop k="width_unit" v="MM"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <customproperties>
    <property key="labeling" value="pal"/>
    <property key="labeling/addDirectionSymbol" value="false"/>
    <property key="labeling/angleOffset" value="0"/>
    <property key="labeling/blendMode" value="0"/>
    <property key="labeling/bufferBlendMode" value="0"/>
    <property key="labeling/bufferColorA" value="255"/>
    <property key="labeling/bufferColorB" value="255"/>
    <property key="labeling/bufferColorG" value="255"/>
    <property key="labeling/bufferColorR" value="255"/>
    <property key="labeling/bufferDraw" value="false"/>
    <property key="labeling/bufferJoinStyle" value="64"/>
    <property key="labeling/bufferNoFill" value="false"/>
    <property key="labeling/bufferSize" value="1"/>
    <property key="labeling/bufferSizeInMapUnits" value="false"/>
    <property key="labeling/bufferTransp" value="0"/>
    <property key="labeling/centroidWhole" value="false"/>
    <property key="labeling/decimals" value="3"/>
    <property key="labeling/displayAll" value="false"/>
    <property key="labeling/dist" value="0"/>
    <property key="labeling/distInMapUnits" value="false"/>
    <property key="labeling/enabled" value="false"/>
    <property key="labeling/fieldName" value=""/>
    <property key="labeling/fontBold" value="false"/>
    <property key="labeling/fontCapitals" value="0"/>
    <property key="labeling/fontFamily" value="MS Shell Dlg 2"/>
    <property key="labeling/fontItalic" value="false"/>
    <property key="labeling/fontLetterSpacing" value="0"/>
    <property key="labeling/fontLimitPixelSize" value="false"/>
    <property key="labeling/fontMaxPixelSize" value="10000"/>
    <property key="labeling/fontMinPixelSize" value="3"/>
    <property key="labeling/fontSize" value="8.25"/>
    <property key="labeling/fontSizeInMapUnits" value="false"/>
    <property key="labeling/fontStrikeout" value="false"/>
    <property key="labeling/fontUnderline" value="false"/>
    <property key="labeling/fontWeight" value="50"/>
    <property key="labeling/fontWordSpacing" value="0"/>
    <property key="labeling/formatNumbers" value="false"/>
    <property key="labeling/isExpression" value="false"/>
    <property key="labeling/labelOffsetInMapUnits" value="true"/>
    <property key="labeling/labelPerPart" value="false"/>
    <property key="labeling/leftDirectionSymbol" value="&lt;"/>
    <property key="labeling/limitNumLabels" value="false"/>
    <property key="labeling/maxCurvedCharAngleIn" value="20"/>
    <property key="labeling/maxCurvedCharAngleOut" value="-20"/>
    <property key="labeling/maxNumLabels" value="2000"/>
    <property key="labeling/mergeLines" value="false"/>
    <property key="labeling/minFeatureSize" value="0"/>
    <property key="labeling/multilineAlign" value="0"/>
    <property key="labeling/multilineHeight" value="1"/>
    <property key="labeling/namedStyle" value="Normal"/>
    <property key="labeling/obstacle" value="true"/>
    <property key="labeling/placeDirectionSymbol" value="0"/>
    <property key="labeling/placement" value="2"/>
    <property key="labeling/placementFlags" value="10"/>
    <property key="labeling/plussign" value="false"/>
    <property key="labeling/preserveRotation" value="true"/>
    <property key="labeling/previewBkgrdColor" value="#ffffff"/>
    <property key="labeling/priority" value="5"/>
    <property key="labeling/quadOffset" value="4"/>
    <property key="labeling/reverseDirectionSymbol" value="false"/>
    <property key="labeling/rightDirectionSymbol" value=">"/>
    <property key="labeling/scaleMax" value="10000000"/>
    <property key="labeling/scaleMin" value="1"/>
    <property key="labeling/scaleVisibility" value="false"/>
    <property key="labeling/shadowBlendMode" value="6"/>
    <property key="labeling/shadowColorB" value="0"/>
    <property key="labeling/shadowColorG" value="0"/>
    <property key="labeling/shadowColorR" value="0"/>
    <property key="labeling/shadowDraw" value="false"/>
    <property key="labeling/shadowOffsetAngle" value="135"/>
    <property key="labeling/shadowOffsetDist" value="1"/>
    <property key="labeling/shadowOffsetGlobal" value="true"/>
    <property key="labeling/shadowOffsetUnits" value="1"/>
    <property key="labeling/shadowRadius" value="1.5"/>
    <property key="labeling/shadowRadiusAlphaOnly" value="false"/>
    <property key="labeling/shadowRadiusUnits" value="1"/>
    <property key="labeling/shadowScale" value="100"/>
    <property key="labeling/shadowTransparency" value="30"/>
    <property key="labeling/shadowUnder" value="0"/>
    <property key="labeling/shapeBlendMode" value="0"/>
    <property key="labeling/shapeBorderColorA" value="255"/>
    <property key="labeling/shapeBorderColorB" value="128"/>
    <property key="labeling/shapeBorderColorG" value="128"/>
    <property key="labeling/shapeBorderColorR" value="128"/>
    <property key="labeling/shapeBorderWidth" value="0"/>
    <property key="labeling/shapeBorderWidthUnits" value="1"/>
    <property key="labeling/shapeDraw" value="false"/>
    <property key="labeling/shapeFillColorA" value="255"/>
    <property key="labeling/shapeFillColorB" value="255"/>
    <property key="labeling/shapeFillColorG" value="255"/>
    <property key="labeling/shapeFillColorR" value="255"/>
    <property key="labeling/shapeJoinStyle" value="64"/>
    <property key="labeling/shapeOffsetUnits" value="1"/>
    <property key="labeling/shapeOffsetX" value="0"/>
    <property key="labeling/shapeOffsetY" value="0"/>
    <property key="labeling/shapeRadiiUnits" value="1"/>
    <property key="labeling/shapeRadiiX" value="0"/>
    <property key="labeling/shapeRadiiY" value="0"/>
    <property key="labeling/shapeRotation" value="0"/>
    <property key="labeling/shapeRotationType" value="0"/>
    <property key="labeling/shapeSVGFile" value=""/>
    <property key="labeling/shapeSizeType" value="0"/>
    <property key="labeling/shapeSizeUnits" value="1"/>
    <property key="labeling/shapeSizeX" value="0"/>
    <property key="labeling/shapeSizeY" value="0"/>
    <property key="labeling/shapeTransparency" value="0"/>
    <property key="labeling/shapeType" value="0"/>
    <property key="labeling/textColorA" value="255"/>
    <property key="labeling/textColorB" value="0"/>
    <property key="labeling/textColorG" value="0"/>
    <property key="labeling/textColorR" value="0"/>
    <property key="labeling/textTransp" value="0"/>
    <property key="labeling/upsidedownLabels" value="0"/>
    <property key="labeling/wrapChar" value=""/>
    <property key="labeling/xOffset" value="0"/>
    <property key="labeling/yOffset" value="0"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerTransparency>0</layerTransparency>
  <displayfield>geodb_subtype_name</displayfield>
  <label>0</label>
  <labelattributes>
    <label fieldname="" text="Label"/>
    <family fieldname="" name="MS Shell Dlg 2"/>
    <size fieldname="" units="pt" value="12"/>
    <bold fieldname="" on="0"/>
    <italic fieldname="" on="0"/>
    <underline fieldname="" on="0"/>
    <strikeout fieldname="" on="0"/>
    <color fieldname="" red="0" blue="0" green="0"/>
    <x fieldname=""/>
    <y fieldname=""/>
    <offset x="0" y="0" units="pt" yfieldname="" xfieldname=""/>
    <angle fieldname="" value="0" auto="0"/>
    <alignment fieldname="" value="center"/>
    <buffercolor fieldname="" red="255" blue="255" green="255"/>
    <buffersize fieldname="" units="pt" value="1"/>
    <bufferenabled fieldname="" on=""/>
    <multilineenabled fieldname="" on=""/>
    <selectedonly on=""/>
  </labelattributes>
  <edittypes>
    <edittype labelontop="0" editable="1" type="0" name="OGC_FID"/>
    <edittype labelontop="0" editable="1" type="0" name="caladomax"/>
    <edittype labelontop="0" editable="1" type="3" name="coincidecomdentrode">
      <valuepair key="Barragem" value="19"/>
      <valuepair key="Canal" value="2"/>
      <valuepair key="Corredeira" value="13"/>
      <valuepair key="Eclusa" value="14"/>
      <valuepair key="Foz marítima" value="16"/>
      <valuepair key="Laguna" value="9"/>
      <valuepair key="Não aplicável" value="97"/>
      <valuepair key="Queda dágua" value="12"/>
      <valuepair key="Represa/açude" value="10"/>
      <valuepair key="Rio" value="1"/>
      <valuepair key="Terreno sujeito a inundação" value="15"/>
      <valuepair key="Vala" value="11"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="3" name="compartilhado">
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="3" name="dentrodepoligono">
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="3" name="eixoprincipal">
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="0" type="0" name="geodb_oid"/>
    <edittype labelontop="0" editable="0" type="0" name="geodb_subtype_name"/>
    <edittype labelontop="0" editable="1" type="3" name="geometriaaproximada">
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="0" name="id_trecho_curso_dagua"/>
    <edittype labelontop="0" editable="1" type="0" name="larguramedia"/>
    <edittype labelontop="0" editable="1" type="0" name="metadado"/>
    <edittype labelontop="0" editable="1" type="3" name="navegabilidade">
      <valuepair key="Desconhecida" value="0"/>
      <valuepair key="Navegável" value="1"/>
      <valuepair key="Não navegável" value="2"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="0" name="nome"/>
    <edittype labelontop="0" editable="1" type="0" name="nomeabrev"/>
    <edittype labelontop="0" editable="0" type="0" name="objectid"/>
    <edittype labelontop="0" editable="1" type="0" name="profundidademedia"/>
    <edittype labelontop="0" editable="1" type="3" name="regime">
      <valuepair key="Permanente" value="1"/>
      <valuepair key="Permanente com grande variação" value="2"/>
      <valuepair key="Seco" value="5"/>
      <valuepair key="Temporário" value="3"/>
      <valuepair key="Temporário com leito permanente" value="4"/>
    </edittype>
    <edittype labelontop="0" editable="0" type="0" name="shape_length"/>
    <edittype labelontop="0" editable="1" type="0" name="velocidademedcorrente"/>
  </edittypes>
  <editform></editform>
  <editforminit></editforminit>
  <featformsuppress>0</featformsuppress>
  <annotationform></annotationform>
  <editorlayout>generatedlayout</editorlayout>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <attributeactions/>
</qgis>
