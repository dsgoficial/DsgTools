# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DSGTools
                                 A QGIS plugin
 Creates UTM and geopgraphic symbology and labels for given bounding feature.
                              -------------------
        begin                : 2019-04-21
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Joao Felipe Aguiar Guimaraes
        email                : joao.felipe@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from builtins import abs, range, round, str
from math import floor

from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFillSymbol,
    QgsGeometry,
    QgsGeometryGeneratorSymbolLayer,
    QgsInvertedPolygonRenderer,
    QgsLineSymbol,
    QgsMapLayer,
    QgsPalLayerSettings,
    QgsPoint,
    QgsProject,
    QgsPropertyCollection,
    QgsRenderContext,
    QgsRuleBasedLabeling,
    QgsRuleBasedRenderer,
    QgsSimpleFillSymbolLayer,
    QgsSingleSymbolRenderer,
    QgsSymbolLayerId,
    QgsSymbolLayerReference,
    QgsTextFormat,
    QgsVectorLayer,
    QgsVectorLayerSimpleLabeling,
)
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtGui import QColor, QFont


class GridAndLabelCreator(QObject):
    def __init__(self, parent=None):
        super(GridAndLabelCreator, self).__init__()

    def reset(self, layer):
        layer_rst = layer
        properties = {"color": "black"}
        grid_symb = QgsFillSymbol.createSimple(properties)
        symb_out = QgsSimpleFillSymbolLayer()
        symb_out.setFillColor(QColor("white"))
        grid_symb.changeSymbolLayer(0, symb_out)
        render_base = QgsSingleSymbolRenderer(grid_symb)
        layer_rst.setRenderer(render_base)
        root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
        rules = QgsRuleBasedLabeling(root_rule)
        layer_rst.setLabeling(rules)
        layer_rst.setLabelsEnabled(False)
        layer_rst.triggerRepaint()
        return

    def crossLinegenerator(
        self, utmSRID, x_geo, y_geo, px, py, u, t, dx, dy, trLLUTM, linwidth_geo, color
    ):
        p1 = QgsPoint(x_geo + px * u, y_geo + py * t)
        p2 = QgsPoint(x_geo + px * u + dx, y_geo + py * t + dy)
        p1.transform(trLLUTM)
        p2.transform(trLLUTM)
        properties = {"color": color.name()}
        line_temp = QgsLineSymbol.createSimple(properties)
        line_temp.setWidth(linwidth_geo)
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(Qgis.SymbolType.Line)
        symb.setSubSymbol(line_temp)

        symb.setGeometryExpression(
            "transform(make_line(make_point({}, {}), make_point({}, {})), 'EPSG:{}', @map_crs)".format(
                p1.x(), p1.y(), p2.x(), p2.y(), utmSRID
            )
        )
        return symb

    def gridLinesymbolMaker(
        self,
        x1,
        y1,
        x2,
        y2,
        xmax_geo,
        xmin_geo,
        ymax_geo,
        ymin_geo,
        trUTMLL,
        trLLUTM,
        isVertical,
    ):
        a1 = QgsPoint(x1, y1)
        a2 = QgsPoint(x2, y2)
        a1.transform(trUTMLL)
        a2.transform(trUTMLL)
        if isVertical:
            p1 = QgsPoint(a1.x(), ymin_geo)
            p2 = QgsPoint(a2.x(), ymax_geo)

        else:
            p1 = QgsPoint(xmin_geo, a1.y())
            p2 = QgsPoint(xmax_geo, a2.y())
        p1.transform(trLLUTM)
        p2.transform(trLLUTM)
        return [a1, a2, p1, p2]

    def utm_Symb_Generator(
        self,
        layer_bound,
        grid_spacing,
        trUTMLL,
        trLLUTM,
        grid_symb,
        properties,
        UTM_num_x,
        UTM_num_y,
        t,
        u,
        extentsGeo,
        extentsUTM,
        linwidth_utm,
        color,
    ):
        test_line = [None] * 2
        properties = {"color": color.name()}
        line_temp = QgsLineSymbol.createSimple(properties)
        line_temp.setWidth(linwidth_utm)
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(Qgis.SymbolType.Line)
        symb.setSubSymbol(line_temp)

        # Test First And Last Grid Lines
        # Vertical
        if (t == 1 and u == 0) or (t == UTM_num_x and u == 0):

            # Symbol vertices
            auxPointlist = self.gridLinesymbolMaker(
                ((floor(extentsUTM[0] / grid_spacing) + t) * grid_spacing),
                extentsUTM[1],
                ((floor(extentsUTM[0] / grid_spacing) + t) * grid_spacing),
                extentsUTM[3],
                extentsGeo[2],
                extentsGeo[0],
                extentsGeo[3],
                extentsGeo[1],
                trUTMLL,
                trLLUTM,
                True,
            )

            # 0: left bound; 1: right bound
            test_line[0] = QgsGeometry.fromWkt(
                "LINESTRING ("
                + str(extentsGeo[0])
                + " "
                + str(extentsGeo[1])
                + ","
                + str(extentsGeo[0])
                + " "
                + str(extentsGeo[3])
                + ")"
            )
            test_line[1] = QgsGeometry.fromWkt(
                "LINESTRING ("
                + str(extentsGeo[2])
                + " "
                + str(extentsGeo[1])
                + ","
                + str(extentsGeo[2])
                + " "
                + str(extentsGeo[3])
                + ")"
            )
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0], auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].x() > auxPointlist[1].x():
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})), 'EPSG:{}', @map_crs)".format(
                            auxPointlist[2].x(),
                            auxPointlist[2].y(),
                            mid_point.x(),
                            mid_point.y(),
                            layer_bound,
                        )
                    )
                else:
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})), 'EPSG:{}', @map_crs)".format(
                            mid_point.x(),
                            mid_point.y(),
                            auxPointlist[3].x(),
                            auxPointlist[3].y(),
                            layer_bound,
                        )
                    )
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].x() < auxPointlist[1].x():
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            auxPointlist[2].x(),
                            auxPointlist[2].y(),
                            mid_point.x(),
                            mid_point.y(),
                            layer_bound,
                        )
                    )
                else:
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            mid_point.x(),
                            mid_point.y(),
                            auxPointlist[3].x(),
                            auxPointlist[3].y(),
                            layer_bound,
                        )
                    )
            else:
                symb.setGeometryExpression(
                    "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                        auxPointlist[2].x(),
                        auxPointlist[2].y(),
                        auxPointlist[3].x(),
                        auxPointlist[3].y(),
                        layer_bound,
                    )
                )

        # Horizontal
        elif (u == 1 and t == 0) or (u == UTM_num_y and t == 0):

            # Symbol vertices
            auxPointlist = self.gridLinesymbolMaker(
                extentsUTM[0],
                ((floor(extentsUTM[1] / grid_spacing) + u) * grid_spacing),
                extentsUTM[2],
                ((floor(extentsUTM[1] / grid_spacing) + u) * grid_spacing),
                extentsGeo[2],
                extentsGeo[0],
                extentsGeo[3],
                extentsGeo[1],
                trUTMLL,
                trLLUTM,
                False,
            )

            # 0: bottom bound; 1: upper bound
            test_line[0] = QgsGeometry.fromWkt(
                "LINESTRING ("
                + str(extentsGeo[0])
                + " "
                + str(extentsGeo[1])
                + ","
                + str(extentsGeo[2])
                + " "
                + str(extentsGeo[1])
                + ")"
            )
            test_line[1] = QgsGeometry.fromWkt(
                "LINESTRING ("
                + str(extentsGeo[0])
                + " "
                + str(extentsGeo[3])
                + ","
                + str(extentsGeo[2])
                + " "
                + str(extentsGeo[3])
                + ")"
            )
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0], auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].y() > auxPointlist[1].y():
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            auxPointlist[2].x(),
                            auxPointlist[2].y(),
                            mid_point.x(),
                            mid_point.y(),
                            layer_bound,
                        )
                    )
                else:
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            mid_point.x(),
                            mid_point.y(),
                            auxPointlist[3].x(),
                            auxPointlist[3].y(),
                            layer_bound,
                        )
                    )
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].y() < auxPointlist[1].y():
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            auxPointlist[2].x(),
                            auxPointlist[2].y(),
                            mid_point.x(),
                            mid_point.y(),
                            layer_bound,
                        )
                    )
                else:
                    symb.setGeometryExpression(
                        "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                            mid_point.x(),
                            mid_point.y(),
                            auxPointlist[3].x(),
                            auxPointlist[3].y(),
                            layer_bound,
                        )
                    )
            else:
                symb.setGeometryExpression(
                    "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                        auxPointlist[2].x(),
                        auxPointlist[2].y(),
                        auxPointlist[3].x(),
                        auxPointlist[3].y(),
                        layer_bound,
                    )
                )

        # Inner Grid Lines
        # Vertical
        elif (not (t == 1)) and (not (t == UTM_num_x)) and u == 0:
            auxPointlist = self.gridLinesymbolMaker(
                ((floor(extentsUTM[0] / grid_spacing) + t) * grid_spacing),
                extentsUTM[1],
                ((floor(extentsUTM[0] / grid_spacing) + t) * grid_spacing),
                extentsUTM[3],
                extentsGeo[2],
                extentsGeo[0],
                extentsGeo[3],
                extentsGeo[1],
                trUTMLL,
                trLLUTM,
                True,
            )
            symb.setGeometryExpression(
                "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                    auxPointlist[2].x(),
                    auxPointlist[2].y(),
                    auxPointlist[3].x(),
                    auxPointlist[3].y(),
                    layer_bound,
                )
            )

        # Horizontal
        elif (not (u == 1)) and (not (u == UTM_num_y)) and t == 0:
            auxPointlist = self.gridLinesymbolMaker(
                extentsUTM[0],
                ((floor(extentsUTM[1] / grid_spacing) + u) * grid_spacing),
                extentsUTM[2],
                ((floor(extentsUTM[1] / grid_spacing) + u) * grid_spacing),
                extentsGeo[2],
                extentsGeo[0],
                extentsGeo[3],
                extentsGeo[1],
                trUTMLL,
                trLLUTM,
                False,
            )
            symb.setGeometryExpression(
                "transform(make_line(make_point({}, {}), make_point({}, {})),'EPSG:{}', @map_crs)".format(
                    auxPointlist[2].x(),
                    auxPointlist[2].y(),
                    auxPointlist[3].x(),
                    auxPointlist[3].y(),
                    layer_bound,
                )
            )

        grid_symb.appendSymbolLayer(symb)
        return grid_symb

    def grid_labeler(
        self,
        coord_base_x,
        coord_base_y,
        px,
        py,
        u,
        t,
        dx,
        dy,
        desc,
        fSize,
        fontType,
        expression_str,
        trLLUTM,
        llcolor,
        layer_bound,
        trUTMLL,
        discourage_placement=False,
    ):
        pgrid = QgsPoint(coord_base_x + px * u, coord_base_y + py * t)
        pgrid.transform(trLLUTM)
        pgrid = QgsPoint(pgrid.x() + dx, pgrid.y() + dy)
        if layer_bound.crs().isGeographic() == True:
            pgrid.transform(trUTMLL)
        # Label Format Settings
        settings = QgsPalLayerSettings()
        settings.placement = (
            1 if Qgis.QGIS_VERSION_INT <= 32600 else Qgis.LabelPlacement.OverPoint
        )
        settings.isExpression = True
        textprop = QgsTextFormat()
        textprop.setColor(llcolor)
        textprop.setSizeUnit(
            4 if Qgis.QGIS_VERSION_INT <= 32600 else Qgis.RenderUnit.Points
        )
        textprop.setSize(fSize * 2.8346)
        textprop.setFont(QFont(fontType))
        textprop.setLineHeight(1)
        settings.setFormat(textprop)
        settings.fieldName = expression_str

        # Label Position
        settings.geometryGeneratorEnabled = True
        settings.geometryGenerator = "make_point({}, {})".format(pgrid.x(), pgrid.y())
        datadefined = QgsPropertyCollection()
        datadefined.property(20).setExpressionString("True")
        datadefined.property(20).setActive(True)
        datadefined.property(15).setExpressionString("True")
        datadefined.property(15).setActive(True)
        datadefined.property(77).setExpressionString("2")
        datadefined.property(77).setActive(True)

        # Creating and Activating Labeling Rule
        settings.setDataDefinedProperties(datadefined)
        rule = QgsRuleBasedLabeling.Rule(settings)
        rule.setDescription(desc)
        rule.setActive(True)

        return rule

    def utm_grid_labeler(
        self,
        root_rule,
        x_UTM,
        y_UTM,
        x_geo,
        y_geo,
        x_min,
        y_min,
        px,
        py,
        trUTMLL,
        trLLUTM,
        u,
        isVertical,
        dx,
        dy,
        dyO,
        dy1,
        desc,
        fSize,
        fontType,
        grid_spacing,
        scale,
        rangetest,
        geo_bb_or,
        layer_bound,
        discourage_placement=False,
    ):
        # x_colec = [float(geo_bb_or.split()[2*i]) for i in range(1,5)]
        # x_colec.sort()
        # y_colec = [float(geo_bb_or.split()[2*i+1]) for i in range(1,5)]
        # y_colec.sort()
        # ang = float(geo_bb_or.split()[13])
        # if ang > 0:
        #     if 'Bot' in desc:
        #         x_min_test = x_colec[0]
        #         x_max_test = x_colec[2]
        #     elif 'Up' in desc:
        #         x_min_test = x_colec[1]
        #         x_max_test = x_colec[3]
        #     elif 'Left' in desc:
        #         y_min_test = y_colec[1]
        #         y_max_test = y_colec[3]
        #     elif 'Right' in desc:
        #         y_min_test = y_colec[0]
        #         y_max_test = y_colec[2]
        # elif ang <= 0:
        #     if 'Bot' in desc:
        #         x_min_test = x_colec[1]
        #         x_max_test = x_colec[3]
        #     elif 'Up' in desc:
        #         x_min_test = x_colec[0]
        #         x_max_test = x_colec[2]
        #     elif 'Left' in desc:
        #         y_min_test = y_colec[0]
        #         y_max_test = y_colec[2]
        #     elif 'Right' in desc:
        #         y_min_test = y_colec[1]
        #         y_max_test = y_colec[3]
        x_min_test = geo_bb_or.xMinimum()
        x_max_test = geo_bb_or.xMaximum()
        y_min_test = geo_bb_or.yMinimum()
        y_max_test = geo_bb_or.yMaximum()

        # Check if is labeling grid's vertical lines
        if isVertical:
            # Displacing UTM Label that overlaps Geo Label
            dx0 = 0
            test_plac = QgsPoint(
                ((floor(x_UTM / grid_spacing) + u) * grid_spacing), y_UTM
            )
            test_plac.transform(trUTMLL)
            ancX = QgsPoint(
                ((floor(x_UTM / grid_spacing) + u) * grid_spacing) + dx, y_UTM
            )
            ancX.transform(trUTMLL)
            ancY = QgsPoint(ancX.x(), y_geo)
            ancY.transform(trLLUTM)
            test = QgsPoint(((floor(x_UTM / grid_spacing) + u) * grid_spacing), y_UTM)
            test.transform(trUTMLL)
            if u == 1 and "Up" in desc:
                deltaDneg = 0.0022
                deltaDpos = 0.0011
            elif u == 1 and "Bot" in desc:
                deltaDneg = 0.0011
                deltaDpos = 0.0011
            else:
                deltaDneg = 0.0009
                deltaDpos = 0.0009
            testif = abs(
                floor(
                    abs(
                        round(test.x(), 4)
                        - (x_min % (px))
                        - (deltaDneg * (fSize / 1.5) * scale / 10)
                    )
                    / px
                )
                - floor(
                    abs(
                        round(test.x(), 4)
                        - (x_min % (px))
                        + (deltaDpos * (fSize / 1.5) * scale / 10)
                    )
                    / px
                )
            )
            if testif >= 1:
                ancY = QgsPoint(ancY.x(), ancY.y() + dyO)
            else:
                ancY = QgsPoint(ancY.x(), ancY.y() + dy)
            x = ancX.x() + dx0
            ancY.transform(trUTMLL)
            y = ancY.y()
            full_label = str((floor(x_UTM / grid_spacing) + u) * grid_spacing)
            if test_plac.x() < (x_min_test) or test_plac.x() > (x_max_test):
                rule_fake = self.grid_labeler(
                    x,
                    y,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    desc,
                    fSize,
                    fontType,
                    "fail",
                    trLLUTM,
                    QColor("black"),
                    layer_bound,
                    trUTMLL,
                    discourage_placement=discourage_placement,
                )
                root_rule.appendChild(rule_fake)
                return root_rule

        # Labeling grid's horizontal lines
        else:
            test_plac = QgsPoint(
                x_UTM, (floor(y_UTM / grid_spacing) + u) * grid_spacing
            )
            test_plac.transform(trUTMLL)
            ancX = QgsPoint(x_UTM, (floor(y_UTM / grid_spacing) + u) * grid_spacing)
            ancX.transform(trUTMLL)
            ancX = QgsPoint(x_geo, ancX.y())
            ancY = QgsPoint(x_geo, ancX.y())
            ancY.transform(trLLUTM)
            test = QgsPoint(x_UTM, (floor(y_UTM / grid_spacing) + u) * grid_spacing)
            test.transform(trUTMLL)
            testif = abs(
                floor(
                    abs(
                        round(test.y(), 4)
                        - (y_min % (py))
                        - (0.0004 * (fSize / 1.5) * scale / 10)
                    )
                    / py
                )
                - floor(abs(round(test.y(), 4) - (y_min % (py))) / py)
            )
            if testif >= 1:
                ancY = QgsPoint(ancY.x(), ancY.y() + dy1)
            else:
                testif2 = abs(
                    floor(abs(round(test.y(), 4) - (y_min % (py))) / py)
                    - floor(
                        abs(
                            round(test.y(), 4)
                            - (y_min % (py))
                            + (0.0004 * (fSize / 1.5) * scale / 10)
                        )
                        / py
                    )
                )
                if testif2 >= 1:
                    ancY = QgsPoint(ancY.x(), ancY.y() + dyO)
                else:
                    ancY = QgsPoint(ancY.x(), ancY.y() + dy)
            dx0 = 0
            ancX.transform(trLLUTM)
            ancX = QgsPoint(ancX.x() + dx, ancX.y())
            ancX.transform(trUTMLL)
            ancY.transform(trUTMLL)
            x = ancX.x() + dx0
            y = ancY.y()
            full_label = str((floor(y_UTM / grid_spacing) + u) * grid_spacing)
            utmLabelPoint = QgsPoint(ancY.x(), ancY.y())
            utmLabelPoint.transform(trLLUTM)
            if (
                test_plac.y() < (y_min_test)
                or test_plac.y() > (y_max_test)
                or abs(utmLabelPoint.y() - float(full_label)) < 5
            ):
                rule_fake = self.grid_labeler(
                    x,
                    y,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    desc,
                    fSize,
                    fontType,
                    "fail",
                    trLLUTM,
                    QColor("black"),
                    layer_bound,
                    trUTMLL,
                    discourage_placement=discourage_placement,
                )
                root_rule.appendChild(rule_fake)
                return root_rule

        ctrl_uni = {
            0: "\u2070",
            1: "\u00B9",
            2: "\u00B2",
            3: "\u00B3",
            4: "\u2074",
            5: "\u2075",
            6: "\u2076",
            7: "\u2077",
            8: "\u2078",
            9: "\u2079",
        }
        if not (full_label == "0"):
            full_label = [char for char in full_label]
            for j in range(0, len(full_label)):
                if not (j == len(full_label) - 5 or j == len(full_label) - 4):
                    full_label[j] = ctrl_uni[int(full_label[j])]
            full_label = "".join(full_label)
        expression_str = str("'") + full_label + str("'")
        fontType.setWeight(50)
        fSizeAlt = fSize * 5 / 3
        plac = QgsPoint(x, y)
        plac.transform(trLLUTM)
        if u == min(rangetest) and any(
            spec_lbl in desc for spec_lbl in ("Bot", "Left")
        ):
            extra_label = "N"
            dyT = 1.4 * scale * fSize / 1.5
            dxT = 7.2 * scale * fSize / 1.5
            dxH = 8.2 * scale * fSize / 1.5
            if isVertical:
                extra_label = "E"
                dyT = 1.6 * scale * fSize / 1.5
                dxT = 7.2 * scale * fSize / 1.5
                dxH = 8.1 * scale * fSize / 1.5

            plac_new = QgsPoint(plac.x() + dxT, plac.y() + dyT)
            plac_new.transform(trUTMLL)
            plac_hem = QgsPoint(plac.x() + dxH, plac.y())
            plac_hem.transform(trUTMLL)

            ruleUTM2 = self.grid_labeler(
                plac_new.x(),
                plac_new.y(),
                0,
                0,
                0,
                0,
                0,
                0,
                desc + "m",
                fSize * 4 / 5,
                fontType,
                str("'m'"),
                trLLUTM,
                QColor("black"),
                layer_bound,
                trUTMLL,
                discourage_placement=discourage_placement,
            )
            root_rule.appendChild(ruleUTM2)
            ruleUTM3 = self.grid_labeler(
                plac_hem.x(),
                plac_hem.y(),
                0,
                0,
                0,
                0,
                0,
                0,
                desc + " " + extra_label,
                fSizeAlt,
                fontType,
                "'" + extra_label + "'",
                trLLUTM,
                QColor("black"),
                layer_bound,
                trUTMLL,
                discourage_placement=discourage_placement,
            )
            root_rule.appendChild(ruleUTM3)

        dxS = 0
        if any(spec_lbl in desc for spec_lbl in ("Bot", "Left", "Up")):
            if len(expression_str) == 3:
                dxS = 5.4 * scale * fSize / 1.5
            elif len(expression_str) == 6:
                dxS = 3.2 * scale * fSize / 1.5
            elif len(expression_str) == 7:
                dxS = 1.6 * scale * fSize / 1.5
            elif len(expression_str) == 8:
                dxS = 0.7 * scale * fSize / 1.5

        plac_size = QgsPoint(plac.x() + dxS, plac.y())
        plac_size.transform(trUTMLL)
        ruleUTM = self.grid_labeler(
            plac_size.x(),
            plac_size.y(),
            0,
            0,
            0,
            0,
            0,
            0,
            desc,
            fSizeAlt,
            fontType,
            expression_str,
            trLLUTM,
            QColor("black"),
            layer_bound,
            trUTMLL,
            discourage_placement=discourage_placement,
        )
        root_rule.appendChild(ruleUTM)
        return root_rule

    def conv_dec_gms(
        self,
        base_coord,
        u,
        neg_character,
        pos_character,
        extentsGeo,
        isVertical,
        geo_number_x,
        geo_number_y,
    ):
        if not isVertical:
            coord_spacing = (round(extentsGeo[3], 6) - round(extentsGeo[1], 6)) / (
                geo_number_y + 1
            )
        else:
            coord_spacing = (round(extentsGeo[2], 6) - round(extentsGeo[0], 6)) / (
                geo_number_x + 1
            )
        xbase = base_coord + coord_spacing * u
        x = round(abs(xbase), 6)
        xdeg = int(x)
        xmin = int((round((x - xdeg), 6) * 60))
        xseg = round((round((x - xdeg - round((xmin / 60), 6)), 6)) * 3600)
        if xbase < 0:
            xhem = neg_character
        else:
            xhem = pos_character
        conv_exp_str = "'{}º {}\\' {}\" {}'".format(
            str(xdeg).rjust(2, "0"),
            str(xmin).rjust(2, "0"),
            str(xseg).rjust(2, "0"),
            xhem,
        )

        return conv_exp_str

    def geoGridcreator(
        self,
        utmSRID,
        grid_symb,
        extentsGeo,
        px,
        py,
        geo_number_x,
        geo_number_y,
        scale,
        trLLUTM,
        linwidth_geo,
        color,
    ):
        for u in range(1, (geo_number_x + 2)):
            for t in range(0, (geo_number_y + 2)):
                symb_cross = self.crossLinegenerator(
                    utmSRID,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    u,
                    t,
                    -0.00002145 * scale,
                    0,
                    trLLUTM,
                    linwidth_geo,
                    color,
                )
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x + 2)):
            for t in range(1, (geo_number_y + 2)):
                symb_cross = self.crossLinegenerator(
                    utmSRID,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    u,
                    t,
                    0,
                    -0.00002145 * scale,
                    trLLUTM,
                    linwidth_geo,
                    color,
                )
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x + 1)):
            for t in range(0, (geo_number_y + 2)):
                symb_cross = self.crossLinegenerator(
                    utmSRID,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    u,
                    t,
                    0.00002145 * scale,
                    0,
                    trLLUTM,
                    linwidth_geo,
                    color,
                )
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x + 2)):
            for t in range(0, (geo_number_y + 1)):
                symb_cross = self.crossLinegenerator(
                    utmSRID,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    u,
                    t,
                    0,
                    0.00002145 * scale,
                    trLLUTM,
                    linwidth_geo,
                    color,
                )
                grid_symb.appendSymbolLayer(symb_cross)

        return grid_symb

    def geoGridlabelPlacer(
        self,
        extentsGeo,
        px,
        py,
        geo_number_x,
        geo_number_y,
        dx,
        dy,
        fSize,
        LLfontType,
        trLLUTM,
        llcolor,
        scale,
        layer_bound,
        trUTMLL,
    ):
        root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())

        # Upper
        for u in range(0, geo_number_x + 2):
            if u == 0:
                ruletemp = self.grid_labeler(
                    extentsGeo[0],
                    extentsGeo[3],
                    px,
                    py,
                    u,
                    0,
                    dx[2],
                    dy[0],
                    "Up " + str(u + 1),
                    fSize,
                    LLfontType,
                    str(
                        self.conv_dec_gms(
                            extentsGeo[0],
                            u,
                            "W",
                            "E",
                            extentsGeo,
                            True,
                            geo_number_x,
                            geo_number_y,
                        )
                    )
                    + "+'. GREENWICH'",
                    trLLUTM,
                    llcolor,
                    layer_bound,
                    trUTMLL,
                )
                root_rule.appendChild(ruletemp)
            else:
                ruletemp = self.grid_labeler(
                    extentsGeo[0],
                    extentsGeo[3],
                    px,
                    py,
                    u,
                    0,
                    dx[3],
                    dy[0],
                    "Up " + str(u + 1),
                    fSize,
                    LLfontType,
                    self.conv_dec_gms(
                        extentsGeo[0],
                        u,
                        "W",
                        "E",
                        extentsGeo,
                        True,
                        geo_number_x,
                        geo_number_y,
                    ),
                    trLLUTM,
                    llcolor,
                    layer_bound,
                    trUTMLL,
                )
                root_rule.appendChild(ruletemp)
        # Bottom
        for b in range(0, geo_number_x + 2):
            ruletemp = self.grid_labeler(
                extentsGeo[0],
                extentsGeo[1],
                px,
                py,
                b,
                0,
                dx[3],
                dy[1],
                "Bot " + str(b + 1),
                fSize,
                LLfontType,
                self.conv_dec_gms(
                    extentsGeo[0],
                    b,
                    "W",
                    "E",
                    extentsGeo,
                    True,
                    geo_number_x,
                    geo_number_y,
                ),
                trLLUTM,
                llcolor,
                layer_bound,
                trUTMLL,
            )
            root_rule.appendChild(ruletemp)
        # Right
        for r in range(0, geo_number_y + 2):
            ruletemp = self.grid_labeler(
                extentsGeo[2],
                extentsGeo[1],
                px,
                py,
                0,
                r,
                dx[0],
                dy[2],
                "Right " + str(r + 1),
                fSize,
                LLfontType,
                self.conv_dec_gms(
                    extentsGeo[1],
                    r,
                    "S",
                    "N",
                    extentsGeo,
                    False,
                    geo_number_x,
                    geo_number_y,
                ),
                trLLUTM,
                llcolor,
                layer_bound,
                trUTMLL,
            )
            root_rule.appendChild(ruletemp)
        # Left
        for l in range(0, geo_number_y + 2):
            ruletemp = self.grid_labeler(
                extentsGeo[0],
                extentsGeo[1],
                px,
                py,
                0,
                l,
                dx[1],
                dy[3],
                "Left " + str(l + 1),
                fSize,
                LLfontType,
                self.conv_dec_gms(
                    extentsGeo[1],
                    l,
                    "S",
                    "N",
                    extentsGeo,
                    False,
                    geo_number_x,
                    geo_number_y,
                ),
                trLLUTM,
                llcolor,
                layer_bound,
                trUTMLL,
            )
            root_rule.appendChild(ruletemp)

        return root_rule

    def utmGridlabelPlacer(
        self,
        root_rule,
        grid_spacing,
        extentsGeo,
        extentsUTM,
        px,
        py,
        UTM_num_x,
        UTM_num_y,
        trUTMLL,
        trLLUTM,
        dx,
        dy,
        dy0,
        dy1,
        fSize,
        fontType,
        scale,
        geo_bb_or,
        layer_bound,
    ):
        if grid_spacing > 0:
            # Bottom
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler(
                ruletest,
                extentsUTM[0],
                extentsUTM[1],
                0,
                extentsGeo[1],
                extentsGeo[0],
                extentsGeo[1],
                px,
                py,
                trUTMLL,
                trLLUTM,
                1,
                True,
                dx[0],
                dy[1],
                dy0[1],
                0,
                "UTMBotTest",
                fSize,
                fontType,
                grid_spacing,
                scale,
                range(1),
                geo_bb_or,
                layer_bound,
            )
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == "fail":
                rangeUD = range(2, UTM_num_x + 1)
            else:
                rangeUD = range(1, UTM_num_x + 1)

            for u in rangeUD:
                root_rule = self.utm_grid_labeler(
                    root_rule,
                    extentsUTM[0],
                    extentsUTM[1],
                    0,
                    extentsGeo[1],
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    trUTMLL,
                    trLLUTM,
                    u,
                    True,
                    dx[0],
                    dy[1],
                    dy0[1] + 0.4 * (scale) * fSize / 1.5,
                    0,
                    "UTMBot" + str(u),
                    fSize,
                    fontType,
                    grid_spacing,
                    scale,
                    rangeUD,
                    geo_bb_or,
                    layer_bound,
                )

            # Upper
            rangeUD = range(1, UTM_num_x + 1)
            for u in rangeUD:
                root_rule = self.utm_grid_labeler(
                    root_rule,
                    extentsUTM[0],
                    extentsUTM[3],
                    0,
                    extentsGeo[3],
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    trUTMLL,
                    trLLUTM,
                    u,
                    True,
                    dx[1],
                    dy[0],
                    dy0[0] - 1.3 * (scale) * fSize / 1.5,
                    0,
                    "UTMUp" + str(u),
                    fSize,
                    fontType,
                    grid_spacing,
                    scale,
                    rangeUD,
                    geo_bb_or,
                    layer_bound,
                )

            # Left
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler(
                ruletest,
                extentsUTM[0],
                extentsUTM[1],
                extentsGeo[0],
                0,
                extentsGeo[0],
                extentsGeo[1],
                px,
                py,
                trUTMLL,
                trLLUTM,
                1,
                False,
                dx[2],
                dy[3],
                dy0[3],
                dy1[1],
                "UTMLeftTest",
                fSize,
                fontType,
                grid_spacing,
                scale,
                range(1),
                geo_bb_or,
                layer_bound,
            )
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == "fail":
                rangeLat = range(2, UTM_num_y + 1)
            else:
                rangeLat = range(1, UTM_num_y + 1)
            minRange, maxRange = min(rangeLat), max(rangeLat)
            for u in rangeLat:
                if u == min(rangeLat):
                    extra_dist = -3.2 * scale * fSize / 1.5
                else:
                    extra_dist = 0
                discorage_placement = u in (minRange, maxRange)
                root_rule = self.utm_grid_labeler(
                    root_rule,
                    extentsUTM[0],
                    extentsUTM[1],
                    extentsGeo[0],
                    0,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    trUTMLL,
                    trLLUTM,
                    u,
                    False,
                    dx[2] + extra_dist,
                    dy[3],
                    dy0[3],
                    dy1[1],
                    "UTMLeft" + str(u),
                    fSize,
                    fontType,
                    grid_spacing,
                    scale,
                    rangeLat,
                    geo_bb_or,
                    layer_bound,
                    discourage_placement=discorage_placement,
                )

            # Right
            rangeLat = range(1, UTM_num_y + 1)
            for u in rangeLat:
                root_rule = self.utm_grid_labeler(
                    root_rule,
                    extentsUTM[2],
                    extentsUTM[1],
                    extentsGeo[2],
                    0,
                    extentsGeo[0],
                    extentsGeo[1],
                    px,
                    py,
                    trUTMLL,
                    trLLUTM,
                    u,
                    False,
                    dx[3],
                    dy[3],
                    dy0[3],
                    dy1[1],
                    "UTMRight" + str(1),
                    fSize,
                    fontType,
                    grid_spacing,
                    scale,
                    rangeLat,
                    geo_bb_or,
                    layer_bound,
                )

        return root_rule

    def apply_masks(self, layer_bound):
        layers = QgsProject.instance().mapLayers().values()
        mask_dict = {}

        # Creating symbol layer reference list
        grid_symbol_ref_list = []
        renderer = layer_bound.renderer()
        grid_symbol_rule_id = renderer.rootRule().children()[0].ruleKey()
        layer_id = layer_bound.id()
        symbol_list = renderer.symbols(QgsRenderContext())
        symbol_layer_list = symbol_list[0].symbolLayers()
        for smb in range(1, len(symbol_layer_list)):
            idx_list = []
            idx_list.append(smb)
            idx_list.append(0)
            symbol_id = QgsSymbolLayerId(grid_symbol_rule_id, idx_list)
            temp = QgsSymbolLayerReference(layer_id, symbol_id)
            grid_symbol_ref_list.append(temp)

        # Listing available label masks
        for layer in layers:
            if not layer.type() == QgsMapLayer.VectorLayer:
                continue
            labels = layer.labeling()
            if not labels:
                continue
            providers = []
            if isinstance(labels, QgsVectorLayerSimpleLabeling):
                providers.append("--SINGLE--RULE--")
            if isinstance(labels, QgsRuleBasedLabeling):
                providers = [x.ruleKey() for x in labels.rootRule().children()]

            for provider in providers:
                if provider == "--SINGLE--RULE--":
                    label_settings = labels.settings()
                else:
                    label_settings = labels.settings(provider)
                label_format = label_settings.format()
                masks = label_format.mask()
                if not masks.enabled():
                    continue

                # Applying available lable masks to grid layer symbology
                mask_symbol_list = masks.maskedSymbolLayers()
                new_symbol_mask = []
                for item in mask_symbol_list:
                    if item.layerId() == layer_id:
                        continue
                    new_symbol_mask.append(item)
                for item in grid_symbol_ref_list:
                    new_symbol_mask.append(item)

                masks.setMaskedSymbolLayers(new_symbol_mask)
                label_format.setMask(masks)
                label_settings.setFormat(label_format)
                if provider == "--SINGLE--RULE--":
                    labels.setSettings(label_settings)
                else:
                    labels.setSettings(label_settings, provider)

            layer.setLabeling(labels)

        return

    def styleCreator(
        self,
        feature_geometry,
        layer_bound,
        utmSRID,
        id_attr,
        id_value,
        spacing,
        crossX,
        crossY,
        scale,
        fontSize,
        font,
        fontLL,
        llcolor,
        linwidth_geo,
        linwidth_utm,
        linwidth_buffer_geo,
        linwidth_buffer_utm,
        geo_grid_color,
        utm_grid_color,
        geo_grid_buffer_color,
        utm_grid_buffer_color,
        masks_check,
    ):
        """Getting Input Data For Grid Generation"""
        linwidth_buffer_utm += linwidth_utm
        linwidth_buffer_geo += linwidth_geo
        grid_spacing = spacing
        geo_number_x = crossX
        geo_number_y = crossY
        fSize = fontSize
        fontType = font
        LLfontType = fontLL

        # Defining CRSs Transformations
        trLLUTM = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:4326"),
            QgsCoordinateReferenceSystem("EPSG:" + str(utmSRID)),
            QgsProject.instance(),
        )
        trUTMLL = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("EPSG:" + str(utmSRID)),
            QgsCoordinateReferenceSystem("EPSG:4326"),
            QgsProject.instance(),
        )

        # Transforming to Geographic and defining bounding boxes
        feature_bbox = feature_geometry.boundingBox()
        bound_UTM_bb = str(feature_bbox).replace(",", "").replace(">", "")
        feature_geometry.transform(trUTMLL)
        feature_geo_bbox = feature_geometry.boundingBox()
        # feature_bbox_or = feature_geometry.orientedMinimumBoundingBox()
        geo_bound_bb = str(feature_geo_bbox).replace(",", "").replace(">", "")
        # oriented_geo_bb = str(feature_bbox_or).replace(',','').replace('>','').replace('((','').replace('))','')
        oriented_geo_bb = feature_geometry.boundingBox()

        # Defining UTM Grid Symbology Type
        properties = {"color": "black"}
        grid_symb = QgsFillSymbol.createSimple(properties)

        """ Creating UTM Grid """
        extentsUTM = (
            float(bound_UTM_bb.split()[1]),
            float(bound_UTM_bb.split()[2]),
            float(bound_UTM_bb.split()[3]),
            float(bound_UTM_bb.split()[4]),
        )
        extentsGeo = (
            float(geo_bound_bb.split()[1]),
            float(geo_bound_bb.split()[2]),
            float(geo_bound_bb.split()[3]),
            float(geo_bound_bb.split()[4]),
        )
        if grid_spacing > 0:
            UTM_num_x = floor(extentsUTM[2] / grid_spacing) - floor(
                extentsUTM[0] / grid_spacing
            )
            UTM_num_y = floor(extentsUTM[3] / grid_spacing) - floor(
                extentsUTM[1] / grid_spacing
            )

            if linwidth_buffer_utm != linwidth_utm:
                # Generating Buffer Vertical Lines
                for x in range(1, UTM_num_x + 1):
                    grid_symb = self.utm_Symb_Generator(
                        utmSRID,
                        grid_spacing,
                        trUTMLL,
                        trLLUTM,
                        grid_symb,
                        properties,
                        UTM_num_x,
                        UTM_num_y,
                        x,
                        0,
                        extentsGeo,
                        extentsUTM,
                        linwidth_buffer_utm,
                        utm_grid_buffer_color,
                    )

                # Generating Buffer Horizontal Lines
                for y in range(1, UTM_num_y + 1):
                    grid_symb = self.utm_Symb_Generator(
                        utmSRID,
                        grid_spacing,
                        trUTMLL,
                        trLLUTM,
                        grid_symb,
                        properties,
                        UTM_num_x,
                        UTM_num_y,
                        0,
                        y,
                        extentsGeo,
                        extentsUTM,
                        linwidth_buffer_utm,
                        utm_grid_buffer_color,
                    )

            # Generating Vertical Lines
            for x in range(1, UTM_num_x + 1):
                grid_symb = self.utm_Symb_Generator(
                    utmSRID,
                    grid_spacing,
                    trUTMLL,
                    trLLUTM,
                    grid_symb,
                    properties,
                    UTM_num_x,
                    UTM_num_y,
                    x,
                    0,
                    extentsGeo,
                    extentsUTM,
                    linwidth_utm,
                    utm_grid_color,
                )

            # Generating Horizontal Lines
            for y in range(1, UTM_num_y + 1):
                grid_symb = self.utm_Symb_Generator(
                    utmSRID,
                    grid_spacing,
                    trUTMLL,
                    trLLUTM,
                    grid_symb,
                    properties,
                    UTM_num_x,
                    UTM_num_y,
                    0,
                    y,
                    extentsGeo,
                    extentsUTM,
                    linwidth_utm,
                    utm_grid_color,
                )

        """ Creating Geo Grid """
        px = (round(extentsGeo[2], 6) - round(extentsGeo[0], 6)) / (geo_number_x + 1)
        py = (round(extentsGeo[3], 6) - round(extentsGeo[1], 6)) / (geo_number_y + 1)
        if linwidth_buffer_geo != linwidth_geo:
            grid_symb = self.geoGridcreator(
                utmSRID,
                grid_symb,
                extentsGeo,
                px,
                py,
                geo_number_x,
                geo_number_y,
                scale,
                trLLUTM,
                linwidth_buffer_geo,
                geo_grid_buffer_color,
            )
        grid_symb = self.geoGridcreator(
            utmSRID,
            grid_symb,
            extentsGeo,
            px,
            py,
            geo_number_x,
            geo_number_y,
            scale,
            trLLUTM,
            linwidth_geo,
            geo_grid_color,
        )

        """ Rendering UTM and Geographic Grid """
        # Changing UTM Grid Color
        grid_symb.deleteSymbolLayer(0)

        # Creating Rule Based Renderer (Rule For The Selected Feature, Root Rule)
        symb_new = QgsRuleBasedRenderer.Rule(grid_symb)
        symb_new.setFilterExpression('"' + str(id_attr) + '" = ' + str(id_value))
        symb_new.setLabel("layer")

        # Appending rules to symbol root rule
        root_symbol_rule = QgsRuleBasedRenderer.Rule(None)
        root_symbol_rule.setFilterExpression("")
        root_symbol_rule.appendChild(symb_new)

        # Applying New Renderer
        render_base = QgsRuleBasedRenderer(root_symbol_rule)
        layer_bound.setRenderer(render_base)

        """Rendering outside area"""
        # Duplicating original layer
        layers_names = [i.name() for i in QgsProject.instance().mapLayers().values()]
        if (layer_bound.name() + "_outside") not in layers_names:
            outside_bound_layer = QgsVectorLayer(
                layer_bound.source(),
                layer_bound.name() + "_outside",
                layer_bound.providerType(),
            )
            if layer_bound.providerType() == "memory":
                feats = [feat for feat in layer_bound.getFeatures()]
                outside_bound_layer_data = outside_bound_layer.dataProvider()
                outside_bound_layer_data.addFeatures(feats)
            QgsProject.instance().addMapLayer(outside_bound_layer)
        else:
            outside_bound_layer = QgsProject.instance().mapLayersByName(
                layer_bound.name() + "_outside"
            )[0]

        # Creating Rule Based Renderer (Rule For The Other Features)
        properties = {"color": "white"}
        ext_grid_symb = QgsFillSymbol.createSimple(properties)
        symb_out = QgsSimpleFillSymbolLayer()
        symb_out.setFillColor(QColor("white"))
        symb_out.setStrokeWidth(linwidth_utm)
        ext_grid_symb.changeSymbolLayer(0, symb_out)
        rule_out = QgsRuleBasedRenderer.Rule(ext_grid_symb)
        rule_out.setFilterExpression('"' + str(id_attr) + '" = ' + str(id_value))
        rule_out.setLabel("outside")

        root_symbol_rule_out = QgsRuleBasedRenderer.Rule(None)
        root_symbol_rule_out.appendChild(rule_out)

        render_base_out = QgsRuleBasedRenderer(root_symbol_rule_out)
        new_renderer = QgsInvertedPolygonRenderer.convertFromRenderer(render_base_out)
        outside_bound_layer.setRenderer(new_renderer)

        """ Labeling Geo Grid """
        dx = [2.0, -11.0, -8.0, -3.6]
        dx = [i * scale * fSize / 1.5 for i in dx]
        dy = [1.7, -3.8, -0.8, -0.8]
        dy = [i * scale * fSize / 1.5 for i in dy]

        root_rule = self.geoGridlabelPlacer(
            extentsGeo,
            px,
            py,
            geo_number_x,
            geo_number_y,
            dx,
            dy,
            fSize,
            LLfontType,
            trLLUTM,
            llcolor,
            scale,
            layer_bound,
            trUTMLL,
        )

        """ Labeling UTM Grid"""
        dx = [-2.9, -2.9, -8.9, 2.0]
        dx = [i * scale * fSize / 1.5 for i in dx]
        dy = [1.4, -4.6, -0.5, -1.5]
        dy = [i * scale * fSize / 1.5 for i in dy]
        dy0 = [5.0, -7.2, -3.2, -4.2]
        dy0 = [i * scale * fSize / 1.5 for i in dy0]
        dy1 = [2.15, 1.2]
        dy1 = [i * scale * fSize / 1.5 for i in dy1]

        root_rule = self.utmGridlabelPlacer(
            root_rule,
            grid_spacing,
            extentsGeo,
            extentsUTM,
            px,
            py,
            UTM_num_x,
            UTM_num_y,
            trUTMLL,
            trLLUTM,
            dx,
            dy,
            dy0,
            dy1,
            fSize,
            fontType,
            scale,
            oriented_geo_bb,
            layer_bound,
        )

        """ Activating Labels """
        rules = QgsRuleBasedLabeling(root_rule)
        layer_bound.setLabeling(rules)
        layer_bound.setLabelsEnabled(True)

        if masks_check:
            self.apply_masks(layer_bound)

        layer_bound.triggerRepaint()

        return
