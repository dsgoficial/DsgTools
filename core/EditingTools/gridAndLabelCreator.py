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
from builtins import str, range, abs, round
from math import floor, ceil, pow
from qgis.core import QgsProject, QgsVectorLayer, QgsCoordinateTransform, \
                      QgsCoordinateReferenceSystem, QgsFillSymbol, QgsLineSymbol, \
                      QgsSimpleFillSymbolLayer, QgsSingleSymbolRenderer, \
                      QgsInvertedPolygonRenderer, QgsRuleBasedRenderer, QgsPoint,\
                      QgsPointXY, QgsGeometry, QgsGeometryGeneratorSymbolLayer
from qgis.core import QgsRuleBasedLabeling, QgsPalLayerSettings, QgsTextFormat, \
                      QgsPropertyCollection, QgsLabelingResults, QgsLabelPosition
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QMessageBox


class GridAndLabelCreator(QObject):
    def __init__(self, parent=None):
        super(GridAndLabelCreator, self).__init__()
    
    def geo_test(self, layer, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor):
        if layer.crs().isGeographic() == False:
            testFeature = layer.getFeatures('"' + id_attr + '"' + '=' + str(id_value))
            featureList =  [i for i in testFeature]
            if not featureList:
                QMessageBox.critical(None, u"Erro", u"Escolha um valor existente do atributo '%s'"%(str(id_attr)))
                return            
            else:
                self.styleCreator(layer, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor)
        else:
            QMessageBox.critical(None, u"Erro", u"A camada desejada deve estar projetada.")
            return
        pass

    def crossLinegenerator(self, layer_bound, x_geo, y_geo, px, py, u, t, dx, dy, trLLUTM):
        p1 = QgsPoint(x_geo+px*u, y_geo+py*t)
        p2 = QgsPoint(x_geo+px*u+dx, y_geo+py*t+dy)
        p1.transform(trLLUTM)
        p2.transform(trLLUTM)
        properties = {'color': 'black'}
        line_temp = QgsLineSymbol.createSimple(properties)
        line_temp.setWidth(0.05)
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(1)
        symb.setSubSymbol(line_temp)
        
        symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(p1.x(), p1.y(), p2.x(), p2.y(), layer_bound.sourceName()))
        return symb

    def gridLinesymbolMaker(self, x1, y1, x2, y2, xmax_geo, xmin_geo, ymax_geo, ymin_geo, trUTMLL, trLLUTM, isVertical):
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
        return [a1,a2,p1,p2]

    def utm_Symb_Generator(self, layer_bound, grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, UTM_num_x, UTM_num_y, t, u, extentsGeo, extentsUTM):
        test_line = [None]*2
        properties = {'color': 'black'}
        line_temp = QgsLineSymbol.createSimple(properties)
        line_temp.setWidth(0.05)
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(1)
        symb.setSubSymbol(line_temp)

        #Test First And Last Grid Lines
        #Vertical
        if (t == 1 and u == 0) or (t == UTM_num_x and u == 0):

            #Symbol vertices
            auxPointlist = self.gridLinesymbolMaker(((floor(extentsUTM[0]/grid_spacing)+t)*grid_spacing), extentsUTM[1], ((floor(extentsUTM[0]/grid_spacing)+t)*grid_spacing), extentsUTM[3], extentsGeo[2], extentsGeo[0], extentsGeo[3], extentsGeo[1], trUTMLL, trLLUTM, True)

            #0: left bound; 1: right bound
            test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(extentsGeo[0])+' '+str(extentsGeo[1])+','+str(extentsGeo[0])+' '+str(extentsGeo[3])+')')
            test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(extentsGeo[2])+' '+str(extentsGeo[1])+','+str(extentsGeo[2])+' '+str(extentsGeo[3])+')')
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0],auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].x() > auxPointlist[1].x():
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), mid_point.x(), mid_point.y(), layer_bound.sourceName()))
                else:
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(mid_point.x(), mid_point.y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].x() < auxPointlist[1].x():
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), mid_point.x(), mid_point.y(), layer_bound.sourceName()))
                else:
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(mid_point.x(), mid_point.y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))
            else:
                symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))

        #Horizontal
        elif (u == 1 and t == 0) or (u == UTM_num_y and t == 0):

            #Symbol vertices
            auxPointlist = self.gridLinesymbolMaker(extentsUTM[0], ((floor(extentsUTM[1]/grid_spacing)+u)*grid_spacing), extentsUTM[2], ((floor(extentsUTM[1]/grid_spacing)+u)*grid_spacing), extentsGeo[2], extentsGeo[0], extentsGeo[3], extentsGeo[1], trUTMLL, trLLUTM, False)

            #0: bottom bound; 1: upper bound
            test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(extentsGeo[0])+' '+str(extentsGeo[1])+','+str(extentsGeo[2])+' '+str(extentsGeo[1])+')')
            test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(extentsGeo[0])+' '+str(extentsGeo[3])+','+str(extentsGeo[2])+' '+str(extentsGeo[3])+')')
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0],auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].y() > auxPointlist[1].y():
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), mid_point.x(), mid_point.y(), layer_bound.sourceName()))
                else:
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(mid_point.x(), mid_point.y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                mid_point.transform(trLLUTM)
                if auxPointlist[0].y() < auxPointlist[1].y():
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), mid_point.x(), mid_point.y(), layer_bound.sourceName()))
                else:
                    symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(mid_point.x(), mid_point.y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))
            else:
                symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))

        #Inner Grid Lines
        #Vertical
        elif (not(t == 1)) and (not(t == UTM_num_x)) and u == 0:
            auxPointlist = self.gridLinesymbolMaker(((floor(extentsUTM[0]/grid_spacing)+t)*grid_spacing), extentsUTM[1], ((floor(extentsUTM[0]/grid_spacing)+t)*grid_spacing), extentsUTM[3], extentsGeo[2], extentsGeo[0], extentsGeo[3], extentsGeo[1], trUTMLL, trLLUTM, True)
            symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))

        #Horizontal
        elif (not(u == 1)) and (not(u == UTM_num_y)) and t == 0:
            auxPointlist = self.gridLinesymbolMaker(extentsUTM[0], ((floor(extentsUTM[1]/grid_spacing)+u)*grid_spacing), extentsUTM[2], ((floor(extentsUTM[1]/grid_spacing)+u)*grid_spacing), extentsGeo[2], extentsGeo[0], extentsGeo[3], extentsGeo[1], trUTMLL, trLLUTM, False)
            symb.setGeometryExpression("transform(make_line(make_point({}, {}), make_point({}, {})), layer_property('{}', 'crs'), @map_crs)".format(auxPointlist[2].x(), auxPointlist[2].y(), auxPointlist[3].x(), auxPointlist[3].y(), layer_bound.sourceName()))

        grid_symb.appendSymbolLayer(symb)
        return grid_symb

    def grid_labeler(self, coord_base_x, coord_base_y, px, py, u, t, dx, dy, desc, fSize, fontType, expression_str, trLLUTM, llcolor):
        pgrid = QgsPoint(coord_base_x + px*u, coord_base_y + py*t)
        pgrid.transform(trLLUTM)
        pgrid = QgsPoint(pgrid.x()+ dx, pgrid.y()+ dy)

        #Label Format Settings
        settings = QgsPalLayerSettings()
        settings.Placement = QgsPalLayerSettings.Horizontal
        settings.isExpression = True
        textprop = QgsTextFormat()
        textprop.setColor(llcolor)
        textprop.setSizeUnit(4)
        textprop.setSize(fSize*2.8346)
        textprop.setFont(QFont(fontType))
        textprop.setLineHeight(1)
        settings.setFormat(textprop)
        settings.fieldName = expression_str

        #Label Position
        settings.geometryGeneratorEnabled = True
        settings.geometryGenerator = ('make_point(' + str(pgrid.x()) + ',' + str(pgrid.y()) + ')')
        datadefined = QgsPropertyCollection()
        datadefined.property(20).setExpressionString('True')
        datadefined.property(20).setActive(True)
        datadefined.property(15).setExpressionString('True')
        datadefined.property(15).setActive(True)

        #Creating and Activating Labeling Rule
        settings.setDataDefinedProperties(datadefined)
        rule = QgsRuleBasedLabeling.Rule(settings)
        rule.setDescription(desc)
        rule.setActive(True)

        return rule

    def utm_grid_labeler(self, root_rule, x_UTM, y_UTM, x_geo, y_geo, x_min, y_min, px, py, trUTMLL, trLLUTM, u, isVertical, dx, dy, dyO, dy1, desc, fSize, fontType, grid_spacing, scale, rangetest, geo_bb_or):
        x_colec = [float(geo_bb_or.split()[2*i]) for i in range(1,5)]
        x_colec.sort()
        y_colec = [float(geo_bb_or.split()[2*i+1]) for i in range(1,5)]
        y_colec.sort()
        ang = float(geo_bb_or.split()[13])
        if ang > 0:
            if 'Bot' in desc:
                x_min_test = x_colec[0]
                x_max_test = x_colec[2]
            elif 'Up' in desc:
                x_min_test = x_colec[1]
                x_max_test = x_colec[3]
            elif 'Left' in desc:
                y_min_test = y_colec[1]
                y_max_test = y_colec[3]
            elif 'Right' in desc:
                y_min_test = y_colec[0]
                y_max_test = y_colec[2]
        elif ang <= 0:
            if 'Bot' in desc:
                x_min_test = x_colec[1]
                x_max_test = x_colec[3]
            elif 'Up' in desc:
                x_min_test = x_colec[0]
                x_max_test = x_colec[2]
            elif 'Left' in desc:
                y_min_test = y_colec[0]
                y_max_test = y_colec[2]
            elif 'Right' in desc:
                y_min_test = y_colec[1]
                y_max_test = y_colec[3]

        # Check if is labeling grid's vertical lines
        if isVertical:
            # Displacing UTM Label that overlaps Geo Label
            dx0 = 0
            test_plac = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            test_plac.transform(trUTMLL)
            ancX = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing)+dx,y_UTM)
            ancX.transform(trUTMLL)
            ancY = QgsPoint(ancX.x(),y_geo)
            ancY.transform(trLLUTM)
            test = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            test.transform(trUTMLL)
            if u == 1 and 'Up' in desc:
                deltaDneg = 0.0022
                deltaDpos = 0.0011
            elif u == 1 and 'Bot' in desc:
                deltaDneg = 0.0011
                deltaDpos = 0.0011
            else:
                deltaDneg = 0.0009
                deltaDpos = 0.0009
            testif = abs(floor(abs(round(test.x(), 4) - (x_min % (px)) - (deltaDneg*(fSize/1.5) *scale/10))/px) - floor(abs(round(test.x(), 4) - (x_min % (px)) + (deltaDpos*(fSize/1.5) *scale/10))/px))
            if testif >= 1:
                ancY = QgsPoint(ancY.x(),ancY.y()+dyO)
            else:
                ancY = QgsPoint(ancY.x(),ancY.y()+dy)
            x = ancX.x() + dx0
            ancY.transform(trUTMLL)
            y =ancY.y()
            full_label = str((floor(x_UTM/grid_spacing)+u)*grid_spacing)
            if test_plac.x() < (x_min_test) or test_plac.x() > (x_max_test):
                rule_fake = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, desc, fSize, fontType, 'fail', trLLUTM, QColor('black'))
                root_rule.appendChild(rule_fake)
                return root_rule

        # Labeling grid's horizontal lines
        else:
            test_plac = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            test_plac.transform(trUTMLL)
            ancX = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            ancX.transform(trUTMLL)
            ancX = QgsPoint(x_geo, ancX.y())
            ancY = QgsPoint(x_geo, ancX.y())
            ancY.transform(trLLUTM)
            test = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            test.transform(trUTMLL)
            testif = abs(floor(abs(round(test.y(), 4) - (y_min % (py)) - (0.0004*(fSize/1.5) * scale/10))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)))/py))
            if testif >= 1:
                ancY = QgsPoint(ancY.x(),ancY.y()+dy1)
            else:
                testif2 = abs(floor(abs(round(test.y(), 4) - (y_min % (py)))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)) + (0.0004*(fSize/1.5) *scale/10))/py))
                if testif2 >= 1:
                    ancY = QgsPoint(ancY.x(),ancY.y()+dyO)
                else:
                    ancY = QgsPoint(ancY.x(),ancY.y()+dy)
            dx0 = 0
            ancX.transform(trLLUTM)
            ancX = QgsPoint(ancX.x()+dx, ancX.y())
            ancX.transform(trUTMLL)
            ancY.transform(trUTMLL)
            x = ancX.x() + dx0
            y = ancY.y()
            full_label = str((floor(y_UTM/grid_spacing)+u)*grid_spacing)
            if test_plac.y() < (y_min_test) or test_plac.y() > (y_max_test):
                rule_fake = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, desc, fSize, fontType, 'fail', trLLUTM, QColor('black'))
                root_rule.appendChild(rule_fake)
                return root_rule

        ctrl_uni = {0:u'\u2070',1:u'\u00B9',2:u'\u00B2',3:u'\u00B3',4:u'\u2074',5:u'\u2075',6:u'\u2076',7:u'\u2077',8:u'\u2078',9:u'\u2079'}
        if not (full_label == '0'):
            full_label = [char for char in full_label]
            for j in range(0,len(full_label)):
                if not (j == len(full_label)-5 or j == len(full_label)-4):
                    full_label[j] = ctrl_uni[int(full_label[j])]
            full_label = ''.join(full_label)
        expression_str = str('\'') + full_label + str('\'')
        fontType.setWeight(50)
        fSizeAlt = fSize * 5/3
        plac = QgsPoint(x,y)
        plac.transform(trLLUTM)
        if u == min(rangetest) and any(spec_lbl in desc for spec_lbl in ('Bot','Left')):
            extra_label = 'N'
            dyT = 1.4*scale*fSize/1.5
            dxT = 6.8*scale*fSize/1.5
            dxH = 8.1*scale*fSize/1.5
            if isVertical:
                extra_label = 'E'
                dyT = 1.6*scale*fSize/1.5
                dxT = 6.4*scale*fSize/1.5
                dxH = 7.6*scale*fSize/1.5

            plac_new = QgsPoint(plac.x()+dxT, plac.y()+dyT)
            plac_new.transform(trUTMLL)
            plac_hem = QgsPoint(plac.x()+dxH, plac.y())
            plac_hem.transform(trUTMLL)

            ruleUTM2 = self.grid_labeler(plac_new.x(), plac_new.y(), 0, 0, 0, 0, 0, 0, desc+'m', fSize*4/5, fontType, str('\'m\''), trLLUTM, QColor('black'))
            root_rule.appendChild(ruleUTM2)
            ruleUTM3 = self.grid_labeler(plac_hem.x(), plac_hem.y(), 0, 0, 0, 0, 0, 0, desc+' '+extra_label, fSizeAlt, fontType, '\''+extra_label+'\'', trLLUTM, QColor('black'))
            root_rule.appendChild(ruleUTM3)

        dxS = 0
        if any(spec_lbl in desc for spec_lbl in ('Bot','Left','Up')):
            if len(expression_str) == 3:
                dxS = 5.4*scale*fSize/1.5
            elif len(expression_str) == 6:
                dxS = 3.2*scale*fSize/1.5
            elif len(expression_str) == 7:
                dxS = 1.6*scale*fSize/1.5
            elif len(expression_str) == 8:
                dxS = 0.7*scale*fSize/1.5

        plac_size = QgsPoint(plac.x()+dxS, plac.y())
        plac_size.transform(trUTMLL)
        ruleUTM = self.grid_labeler(plac_size.x(), plac_size.y(), 0, 0, 0, 0, 0, 0, desc, fSizeAlt, fontType, expression_str, trLLUTM, QColor('black'))
        root_rule.appendChild(ruleUTM)
        return root_rule

    def conv_dec_gms(self, base_coord, u, neg_character, pos_character, extentsGeo, isVertical, geo_number_x, geo_number_y):
        if isVertical:
            coord_spacing = (round(extentsGeo[3],6) - round(extentsGeo[1],6))/(geo_number_y+1)
        else:
            coord_spacing = (round(extentsGeo[2],6) - round(extentsGeo[0],6))/(geo_number_x+1)
        xbase = base_coord + coord_spacing*u
        if isVertical:
            x = abs(((round(extentsGeo[3],6) - round(extentsGeo[1],6))/(geo_number_y+1))*round(xbase/((round(extentsGeo[3],6) - round(extentsGeo[1],6))/(geo_number_y+1))))
        else:
            x = abs(((round(extentsGeo[2],6) - round(extentsGeo[0],6))/(geo_number_x+1))*round(xbase/((round(extentsGeo[2],6) - round(extentsGeo[0],6))/(geo_number_x+1))))
        xdeg = int(x)
        xmin = int(((x - xdeg)*60))
        xseg = int(((x - xdeg - xmin/60)*3600))
        if xbase < 0:
            xhem = neg_character
        else:
            xhem = pos_character
        conv_exp_str = u"'{}º {}\\' {}\" {}'".format(str(xdeg).rjust(2,'0'), str(xmin).rjust(2,'0'), str(xseg).rjust(2,'0'), xhem)
        
        return conv_exp_str

    def geoGridcreator(self, layer_bound, grid_symb, extentsGeo, px, py, geo_number_x, geo_number_y, scale, trLLUTM):
        for u in range(1, (geo_number_x+2)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(layer_bound, extentsGeo[0], extentsGeo[1], px, py, u, t, -0.00002145*scale, 0, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(1, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(layer_bound,extentsGeo[0], extentsGeo[1], px, py, u, t, 0, -0.00002145*scale, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+1)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(layer_bound,extentsGeo[0], extentsGeo[1], px, py, u, t, 0.00002145*scale, 0, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(0, (geo_number_y+1)):
                symb_cross = self.crossLinegenerator(layer_bound,extentsGeo[0], extentsGeo[1], px, py, u, t, 0, 0.00002145*scale, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        
        return grid_symb

    def geoGridlabelPlacer(self, extentsGeo, px, py, geo_number_x, geo_number_y, dx, dy, fSize, LLfontType, trLLUTM, llcolor, scale):
        root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
    
        #Upper
        for u in range(0, geo_number_x+2):
            if u ==0:
                ruletemp = self.grid_labeler(extentsGeo[0], extentsGeo[3], px, py, u, 0, dx[2], dy[0], 'Up '+str(u+1), fSize, LLfontType, str(self.conv_dec_gms(extentsGeo[0], u, 'W', 'E', extentsGeo, True, geo_number_x, geo_number_y))+'+\'. GREENWICH\'', trLLUTM, llcolor)
                root_rule.appendChild(ruletemp)
            else:
                ruletemp = self.grid_labeler(extentsGeo[0], extentsGeo[3], px, py, u, 0, dx[3], dy[0], 'Up '+str(u+1), fSize, LLfontType, self.conv_dec_gms(extentsGeo[0], u, 'W', 'E', extentsGeo, True, geo_number_x, geo_number_y), trLLUTM, llcolor)
                root_rule.appendChild(ruletemp)
        #Bottom
        for b in range(0, geo_number_x+2):
            ruletemp = self.grid_labeler(extentsGeo[0], extentsGeo[1], px, py, b, 0, dx[3], dy[1], 'Bot '+str(b+1), fSize, LLfontType, self.conv_dec_gms(extentsGeo[0], b, 'W', 'E', extentsGeo, True, geo_number_x, geo_number_y), trLLUTM, llcolor)
            root_rule.appendChild(ruletemp)
        #Right
        for r in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler(extentsGeo[2], extentsGeo[1], px, py, 0, r, dx[0], dy[2], 'Right '+str(r+1), fSize, LLfontType, self.conv_dec_gms(extentsGeo[1], r, 'S', 'N', extentsGeo, False, geo_number_x, geo_number_y), trLLUTM, llcolor)
            root_rule.appendChild(ruletemp)
        #Left
        for l in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler(extentsGeo[0], extentsGeo[1], px, py, 0, l, dx[1], dy[3], 'Left '+str(l+1), fSize, LLfontType, self.conv_dec_gms(extentsGeo[1], l, 'S', 'N', extentsGeo, False, geo_number_x, geo_number_y), trLLUTM, llcolor)
            root_rule.appendChild(ruletemp)
    
        return root_rule

    def utmGridlabelPlacer(self, root_rule, grid_spacing, extentsGeo, extentsUTM, px, py, UTM_num_x, UTM_num_y, trUTMLL, trLLUTM, dx, dy, dy0, dy1, fSize, fontType, scale, geo_bb_or):
        if grid_spacing > 0:
            # Bottom
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler(ruletest, extentsUTM[0], extentsUTM[1], 0, extentsGeo[1], extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, 1, True, dx[0], dy[1], dy0[1], 0, 'UTMBotTest', fSize, fontType, grid_spacing, scale, range(1), geo_bb_or)
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == 'fail':
                rangeUD = range(2, UTM_num_x+1)
            else:
                rangeUD = range(1, UTM_num_x+1)

            for u in rangeUD:
                root_rule = self.utm_grid_labeler(root_rule, extentsUTM[0], extentsUTM[1], 0, extentsGeo[1], extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, u, True, dx[0], dy[1], dy0[1]+0.4*(scale)*fSize/1.5, 0, 'UTMBot'+str(u), fSize, fontType, grid_spacing, scale, rangeUD, geo_bb_or)

            # Upper
            rangeUD = range(1, UTM_num_x+1)
            for u in rangeUD:
                root_rule = self.utm_grid_labeler(root_rule, extentsUTM[0], extentsUTM[3], 0, extentsGeo[3], extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, u, True, dx[1], dy[0], dy0[0]-1.3*(scale)*fSize/1.5, 0, 'UTMUp'+str(u), fSize, fontType, grid_spacing, scale, rangeUD, geo_bb_or)

            # Left
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler(ruletest, extentsUTM[0], extentsUTM[1], extentsGeo[0], 0, extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, 1, False, dx[2], dy[3], dy0[3], dy1[1], 'UTMLeftTest', fSize, fontType, grid_spacing, scale, range(1), geo_bb_or)
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == 'fail':
                rangeLat = range(2, UTM_num_y+1)
            else:
                rangeLat = range(1, UTM_num_y+1)
            for u in rangeLat:
                if u==min(rangeLat): 
                    extra_dist = -3.2*scale*fSize/1.5
                else:
                    extra_dist = 0
                root_rule = self.utm_grid_labeler(root_rule, extentsUTM[0], extentsUTM[1], extentsGeo[0], 0, extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, u, False, dx[2]+extra_dist, dy[3], dy0[3], dy1[1], 'UTMLeft'+str(u), fSize, fontType, grid_spacing, scale, rangeLat, geo_bb_or)
            
            # Right
            rangeLat = range(1, UTM_num_y+1)
            for u in rangeLat:
                root_rule = self.utm_grid_labeler(root_rule, extentsUTM[2], extentsUTM[1], extentsGeo[2], 0, extentsGeo[0], extentsGeo[1], px, py, trUTMLL, trLLUTM, u, False, dx[3], dy[3], dy0[3], dy1[1], 'UTMRight'+str(1), fSize, fontType, grid_spacing, scale, rangeLat, geo_bb_or)
            
        return root_rule

    def styleCreator(self, layer, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor):
        """Getting Input Data For Grid Generation"""
        grid_spacing = spacing
        geo_number_x = crossX
        geo_number_y = crossY
        fSize = fontSize
        fontType = font
        LLfontType = fontLL

        #Loading feature
        layer_bound = layer
        query = '"'+str(id_attr)+'"='+str(id_value)
        layer_bound.selectByExpression(query, QgsVectorLayer.SelectBehavior(0))
        feature_bound = layer_bound.selectedFeatures()[0]
        layer_bound.removeSelection()
        projCRS = layer_bound.crs().authid()

        #Defining CRSs Transformations
        trLLUTM = QgsCoordinateTransform(QgsCoordinateReferenceSystem('EPSG:4326'), QgsCoordinateReferenceSystem(projCRS), QgsProject.instance())
        trUTMLL = QgsCoordinateTransform(QgsCoordinateReferenceSystem(projCRS), QgsCoordinateReferenceSystem('EPSG:4326'), QgsProject.instance())
        
        # Transforming to Geographic and defining bounding boxes
        feature_geometry = feature_bound.geometry()
        feature_bbox = feature_geometry.boundingBox()
        bound_UTM_bb = str(feature_bbox).replace(',','').replace('>','')
        feature_geometry.transform(trUTMLL)
        feature_geo_bbox = feature_geometry.boundingBox()
        feature_bbox_or = feature_geometry.orientedMinimumBoundingBox()
        geo_bound_bb = str(feature_geo_bbox).replace(',','').replace('>','')
        oriented_geo_bb = str(feature_bbox_or).replace(',','').replace('>','').replace('((','').replace('))','')

        #Defining UTM Grid Symbology Type
        renderer = layer.renderer()
        properties = {'color': 'black'}
        grid_symb = QgsFillSymbol.createSimple(properties)
        symb_out = QgsSimpleFillSymbolLayer()
        symb_out.setStrokeColor(QColor('black'))
        symb_out.setFillColor(QColor('white'))
        symb_out.setStrokeWidth(0.05)

        """ Creating UTM Grid """
        extentsUTM = (float(bound_UTM_bb.split()[1]), float(bound_UTM_bb.split()[2]), float(bound_UTM_bb.split()[3]), float(bound_UTM_bb.split()[4]))
        extentsGeo = (float(geo_bound_bb.split()[1]), float(geo_bound_bb.split()[2]), float(geo_bound_bb.split()[3]), float(geo_bound_bb.split()[4]))
        if grid_spacing > 0:
            UTM_num_x = floor(extentsUTM[2]/grid_spacing) - floor(extentsUTM[0]/grid_spacing)
            UTM_num_y = floor(extentsUTM[3]/grid_spacing) - floor(extentsUTM[1]/grid_spacing)

            #Generating Vertical Lines
            for x in range(1, UTM_num_x+1):
                grid_symb= self.utm_Symb_Generator (layer_bound, grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, UTM_num_x, UTM_num_y, x, 0, extentsGeo, extentsUTM)

            #Generating Horizontal Lines
            for y in range(1, UTM_num_y+1):
                grid_symb = self.utm_Symb_Generator (layer_bound, grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, UTM_num_x, UTM_num_y, 0, y, extentsGeo, extentsUTM)

        """ Creating Geo Grid """
        px = (round(extentsGeo[2],6) - round(extentsGeo[0],6))/(geo_number_x+1)
        py = (round(extentsGeo[3],6) - round(extentsGeo[1],6))/(geo_number_y+1)
        grid_symb = self.geoGridcreator(layer_bound, grid_symb, extentsGeo, px, py, geo_number_x, geo_number_y, scale, trLLUTM)

        """ Rendering UTM and Geographic Grid """
        #Changing UTM Grid Color
        grid_symb.setColor(color)
        grid_symb.changeSymbolLayer(0, symb_out)

        #Creating Rule Based Renderer (Rule For The Other Features)
        properties = {'color': 'white'}
        ext_grid_symb = QgsFillSymbol.createSimple(properties)
        symb_ot = QgsRuleBasedRenderer.Rule(ext_grid_symb)
        symb_ot.setFilterExpression('\"'+str(id_attr)+'\" <> '+str(id_value))
        symb_ot.setLabel('other')

        #Creating Rule Based Renderer (Rule For The Selected Feature, Root Rule)
        symb_new = QgsRuleBasedRenderer.Rule(grid_symb)
        symb_new.setFilterExpression('\"'+str(id_attr)+'\" = '+str(id_value))
        symb_new.setLabel('layer')
        symb_new.appendChild(symb_ot)

        #Applying New Renderer
        render_base = QgsRuleBasedRenderer(symb_new)
        new_renderer = QgsInvertedPolygonRenderer.convertFromRenderer(render_base)
        layer_bound.setRenderer(new_renderer)

        """ Labeling Geo Grid """
        dx = [2.0, -11.0, -8.0, -3.6]
        dx = [i*scale*fSize/1.5 for i in dx]
        dy = [1.7, -3.8, -0.8, -0.8]
        dy = [i*scale*fSize/1.5 for i in dy]

        root_rule = self.geoGridlabelPlacer(extentsGeo, px, py, geo_number_x, geo_number_y, dx, dy, fSize, LLfontType, trLLUTM, llcolor, scale)

        """ Labeling UTM Grid"""
        dx = [-2.9, -2.9, -8.9, 2.0]
        dx = [i*scale*fSize/1.5 for i in dx]
        dy = [1.4, -4.6, -0.5, -1.5]
        dy = [i*scale*fSize/1.5 for i in dy]
        dy0 = [5.0, -7.2, -3.2, -4.2]
        dy0 = [i*scale*fSize/1.5 for i in dy0]
        dy1 = [2.15, 1.2]
        dy1 = [i*scale*fSize/1.5 for i in dy1]

        root_rule = self.utmGridlabelPlacer(root_rule, grid_spacing, extentsGeo, extentsUTM, px, py, UTM_num_x, UTM_num_y, trUTMLL, trLLUTM, dx, dy, dy0, dy1, fSize, fontType, scale, oriented_geo_bb)

        """ Activating Labels """
        rules = QgsRuleBasedLabeling(root_rule)
        layer.setLabeling(rules)
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()
        return
