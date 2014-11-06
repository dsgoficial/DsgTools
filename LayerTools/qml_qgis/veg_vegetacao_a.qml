<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="2.2.0-Valmiera" minimumScale="1" maximumScale="1" simplifyDrawingHints="1" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <renderer-v2 symbollevels="0" type="RuleRenderer">
    <rules>
      <rule filter="not(tipovegetacao = 21) and not (tipovegetacao = 20) and not(tipovegetacao = 18) and not(tipovegetacao = 7) and not(tipovegetacao = 14) and not (tipovegetacao = 5) and not(tipovegetacao = 13) and not(tipovegetacao = 0) and not(tipovegetacao = 19 and geometriaaproximada = 2 and classificacaoporte = 0) and not(tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 2 and not(tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 1) and not(tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 98) and not(tipovegetacao = 15 and geometriaaproximada = 2 and classificacaoporte = 1) and not(tipovegetacao = 15 and geometriaaproximada = 1 and classificacaoporte = 1) " symbol="0" label="Outros Valores"/>
      <rule filter="tipovegetacao = 21" symbol="1" label="Vegetação de area de contato"/>
      <rule filter="tipovegetacao = 20" symbol="2" label="Vegetação de restinga"/>
      <rule filter="tipovegetacao = 18" symbol="3" label="Mangue"/>
      <rule filter="tipovegetacao = 7" symbol="4" label="Estepe"/>
      <rule filter="tipovegetacao = 14" symbol="5" label="Macega ou Chavascal"/>
      <rule filter="tipovegetacao = 5" symbol="6" label="Brejo"/>
      <rule filter="tipovegetacao = 13" symbol="7" label="Cerrado ou Cerradão"/>
      <rule filter="tipovegetacao = 0" symbol="8" label="Desconhecido"/>
      <rule filter="tipovegetacao = 19 and geometriaaproximada = 2 and classificacaoporte = 0" symbol="9" label="Campinarana, Não, Desconhecido"/>
      <rule filter="tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 2" symbol="10" label="Campinarana, Sim, Arbustiva"/>
      <rule filter="tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 1" symbol="11" label="Campinarana, Sim, Arbórea"/>
      <rule filter="tipovegetacao = 19 and geometriaaproximada = 1 and classificacaoporte = 98" symbol="12" label="Campinarana, Sim, Misto"/>
      <rule filter="tipovegetacao = 15 and geometriaaproximada = 2 and classificacaoporte = 1" symbol="13" label="Floresta, Não, Arbórea"/>
      <rule filter="tipovegetacao = 15 and geometriaaproximada = 1 and classificacaoporte = 1" symbol="14" label="Floresta, Sim, Arbórea"/>
    </rules>
    <symbols>
      <symbol alpha="1" type="fill" name="0">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,41,248,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="no"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="1">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="1.5"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@1@1">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="255,255,0,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="solid"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="3"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@1@2">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="dot"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="0.4"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="2.8"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@1@3">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="0,0,0,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="dash dot dot"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="0.4"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="10">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="186,221,105,255"/>
          <prop k="color_border" v="128,152,72,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="PointPatternFill" locked="0">
          <prop k="displacement_x" v="1"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="0"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="2"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="2"/>
          <prop k="distance_y_unit" v="MM"/>
          <symbol alpha="1" type="marker" name="@10@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="255,0,0,255"/>
              <prop k="color_border" v="87,104,49,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="name" v="line"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="1"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="11">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="189,247,135,255"/>
          <prop k="color_border" v="227,158,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="PointPatternFill" locked="0">
          <prop k="displacement_x" v="0"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="1"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="1.5"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="2"/>
          <prop k="distance_y_unit" v="MM"/>
          <symbol alpha="1" type="marker" name="@11@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="38,115,0,255"/>
              <prop k="color_border" v="0,0,0,0"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="0.6"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="12">
        <layer pass="0" class="SVGFill" locked="0">
          <prop k="angle" v="0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="pattern_width_unit" v="MM"/>
          <prop k="svgFile" v="symbol/landuse_swamp.svg"/>
          <prop k="svgFillColor" v="#55aa00"/>
          <prop k="svgOutlineColor" v="#000000"/>
          <prop k="svgOutlineWidth" v="1"/>
          <prop k="svgOutlineWidth_expression" v="svgOutlineWidth_expression"/>
          <prop k="svg_outline_width_unit" v="MM"/>
          <prop k="width" v="20"/>
          <symbol alpha="1" type="line" name="@12@0">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="0,76,115,255"/>
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
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="13">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="76,115,0,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="no"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="14">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="0,115,76,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="no"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="2">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,190,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="3">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="color_border" v="85,170,255,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@3@1">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="85,170,255,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="solid"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="0.5"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="4">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="0,0,0,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="GradientFill" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color1" v="0,0,255,255"/>
          <prop k="color2" v="0,255,0,255"/>
          <prop k="color_type" v="0"/>
          <prop k="coordinate_mode" v="0"/>
          <prop k="discrete" v="0"/>
          <prop k="gradient_color" v="255,255,127,255"/>
          <prop k="gradient_color2" v="255,255,255,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="reference_point1" v="0,0"/>
          <prop k="reference_point1_iscentroid" v="1"/>
          <prop k="reference_point2" v="1,1"/>
          <prop k="reference_point2_iscentroid" v="0"/>
          <prop k="spread" v="0"/>
          <prop k="type" v="1"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="5">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="246,197,103,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="6">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="color_border" v="23,168,232,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="PointPatternFill" locked="0">
          <prop k="displacement_x" v="0"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="1"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="1.5"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="2"/>
          <prop k="distance_y_unit" v="MM"/>
          <symbol alpha="1" type="marker" name="@6@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="23,168,232,255"/>
              <prop k="color_border" v="0,0,0,0"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="0.6"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="7">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="color_border" v="188,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="0"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@7@1">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="255,188,0,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="solid"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="2.4"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
        <layer pass="0" class="LinePatternFill" locked="0">
          <prop k="color" v="0,0,0,255"/>
          <prop k="distance" v="5"/>
          <prop k="distance_unit" v="MM"/>
          <prop k="line_width_unit" v="MM"/>
          <prop k="lineangle" v="45"/>
          <prop k="linewidth" v="0.5"/>
          <prop k="offset" v="1.5"/>
          <prop k="offset_unit" v="MM"/>
          <symbol alpha="1" type="line" name="@7@2">
            <layer pass="0" class="SimpleLine" locked="0">
              <prop k="capstyle" v="square"/>
              <prop k="color" v="188,0,0,255"/>
              <prop k="customdash" v="5;2"/>
              <prop k="customdash_unit" v="MM"/>
              <prop k="draw_inside_polygon" v="0"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="offset" v="0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="penstyle" v="solid"/>
              <prop k="use_custom_dash" v="0"/>
              <prop k="width" v="0.4"/>
              <prop k="width_unit" v="MM"/>
            </layer>
          </symbol>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="8">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="214,133,137,255"/>
          <prop k="color_border" v="0,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
      </symbol>
      <symbol alpha="1" type="fill" name="9">
        <layer pass="0" class="SimpleFill" locked="0">
          <prop k="border_width_unit" v="MM"/>
          <prop k="color" v="255,255,255,255"/>
          <prop k="color_border" v="85,0,0,255"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <prop k="style_border" v="solid"/>
          <prop k="width_border" v="0.26"/>
        </layer>
        <layer pass="0" class="PointPatternFill" locked="0">
          <prop k="displacement_x" v="0"/>
          <prop k="displacement_x_unit" v="MM"/>
          <prop k="displacement_y" v="1"/>
          <prop k="displacement_y_unit" v="MM"/>
          <prop k="distance_x" v="1.5"/>
          <prop k="distance_x_unit" v="MM"/>
          <prop k="distance_y" v="2"/>
          <prop k="distance_y_unit" v="MM"/>
          <symbol alpha="1" type="marker" name="@9@1">
            <layer pass="0" class="SimpleMarker" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="144,112,76,255"/>
              <prop k="color_border" v="0,0,0,0"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="area"/>
              <prop k="size" v="0.6"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
            </layer>
          </symbol>
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
    <property key="labeling/placement" value="0"/>
    <property key="labeling/placementFlags" value="0"/>
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
    <edittype labelontop="0" editable="1" type="0" name="alturamediaindividuos"/>
    <edittype labelontop="0" editable="1" type="3" name="antropizada">
      <valuepair key="Desconhecido" value="0"/>
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="0" name="caracteristicavegetacao"/>
    <edittype labelontop="0" editable="1" type="3" name="classificacaoporte">
      <valuepair key="Arbustiva" value="2"/>
      <valuepair key="Arbórea" value="1"/>
      <valuepair key="Desconhecido" value="0"/>
      <valuepair key="Misto" value="98"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="3" name="denso">
      <valuepair key="Desconhecido" value="0"/>
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="0" name="especiepredominante"/>
    <edittype labelontop="0" editable="1" type="0" name="geodb_oid"/>
    <edittype labelontop="0" editable="1" type="0" name="geodb_subtype_name"/>
    <edittype labelontop="0" editable="1" type="3" name="geometriaaproximada">
      <valuepair key="Não" value="2"/>
      <valuepair key="Sim" value="1"/>
    </edittype>
    <edittype labelontop="0" editable="1" type="0" name="metadado"/>
    <edittype labelontop="0" editable="1" type="0" name="nome"/>
    <edittype labelontop="0" editable="1" type="0" name="nomeabrev"/>
    <edittype labelontop="0" editable="1" type="0" name="objectid"/>
    <edittype labelontop="0" editable="1" type="0" name="shape_area"/>
    <edittype labelontop="0" editable="1" type="0" name="shape_length"/>
    <edittype labelontop="0" editable="1" type="3" name="tipovegetacao">
      <valuepair key="Brejo ou pântano" value="5"/>
      <valuepair key="Caatinga" value="6"/>
      <valuepair key="Campinarana" value="19"/>
      <valuepair key="Cerrado ou cerradão" value="13"/>
      <valuepair key="Desconhecido" value="0"/>
      <valuepair key="Estepe" value="7"/>
      <valuepair key="Floresta" value="15"/>
      <valuepair key="Macega ou chavascal" value="14"/>
      <valuepair key="Mangue" value="18"/>
      <valuepair key="Vegetação de Restinga" value="20"/>
      <valuepair key="Vegetação de Área de Contato" value="21"/>
    </edittype>
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
