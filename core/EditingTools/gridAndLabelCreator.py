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
                      QgsGeometry, QgsGeometryGeneratorSymbolLayer
from qgis.core import QgsRuleBasedLabeling, QgsPalLayerSettings, QgsTextFormat, \
                      QgsPropertyCollection
from qgis.utils import iface
from qgis.gui import QgsMessageBar
from PyQt5.QtGui import QColor, QFont


class GridAndLabelCreator(object):
    def __init__(self, parent=None):
        super(GridAndLabelCreator, self).__init__()
    
    def geo_test(self, layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor):
        if layer.crs().isGeographic() == False:
            self.styleCreator(layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor, True)
        else:
            self.styleCreator(layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor, False)
        pass

    def utmLLtransform(self, utmcheck, p1, trLLUTM):
        if utmcheck:
            p1.transform(trLLUTM)
            return p1
        pass

    def crossLinegenerator(self, xmin_source, ymin_source, px, py, u, t, dx, dy, utmcheck, trLLUTM):
        p1 = QgsPoint(xmin_source+px*u, ymin_source+py*t)
        p2 = QgsPoint(xmin_source+px*u+dx, ymin_source+py*t+dy)
        self.utmLLtransform(utmcheck, p1, trLLUTM)
        self.utmLLtransform(utmcheck, p2, trLLUTM)
        properties = {'color': 'black'}
        line_temp = QgsLineSymbol.createSimple(properties)
        line_temp.setWidth(0.05)
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(1)
        symb.setSubSymbol(line_temp)
        symb.setGeometryExpression('make_line(make_point('+str(p1.x())+',('+str(p1.y())+')),make_point('+str(p2.x())+',('+str(p2.y())+')))')
        return symb

    def gridLinesymbolMaker(self, x1, y1, x2, y2, xmax_source, xmin_source, ymax_source, ymin_source, trUTMLL, trLLUTM, utmcheck, isVertical):
        a1 = QgsPoint(x1, y1)
        a2 = QgsPoint(x2, y2)
        a1.transform(trUTMLL)
        a2.transform(trUTMLL)
        if isVertical:
            p1 = QgsPoint(a1.x(), ymin_source)
            p2 = QgsPoint(a2.x(), ymax_source)
            self.utmLLtransform(utmcheck, p1, trLLUTM)
            self.utmLLtransform(utmcheck, p2, trLLUTM)
        else:
            p1 = QgsPoint(xmin_source, a1.y())
            p2 = QgsPoint(xmax_source, a2.y())
            self.utmLLtransform(utmcheck, p1, trLLUTM)
            self.utmLLtransform(utmcheck, p2, trLLUTM)
        return [a1,a2,p1,p2]

    def utm_symb_generator(self, grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, t, u, geo_bound_bb, bound_UTM_bb, utmcheck):
        xmin_source = float(geo_bound_bb.split()[1])
        ymin_source = float(geo_bound_bb.split()[2])
        xmax_source = float(geo_bound_bb.split()[3])
        ymax_source = float(geo_bound_bb.split()[4])
        xmin_UTM = float(bound_UTM_bb.split()[1])
        ymin_UTM = float(bound_UTM_bb.split()[2])
        xmax_UTM = float(bound_UTM_bb.split()[3])
        ymax_UTM = float(bound_UTM_bb.split()[4])
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
            auxPointlist = self.gridLinesymbolMaker(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing), ymin_UTM, ((floor(xmin_UTM/grid_spacing)+t)*grid_spacing), ymax_UTM, xmax_source, xmin_source, ymax_source, ymin_source, trUTMLL, trLLUTM, utmcheck, True)
            #0: left bound; 1: right bound
            test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymin_source)+','+str(xmin_source)+' '+str(ymax_source)+')')
            test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(xmax_source)+' '+str(ymin_source)+','+str(xmax_source)+' '+str(ymax_source)+')')
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0],auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                self.utmLLtransform(utmcheck, mid_point, trLLUTM)
                if auxPointlist[0].x() > auxPointlist[1].x():
                    symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
                else:
                    symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                self.utmLLtransform(utmcheck, mid_point, trLLUTM)
                if auxPointlist[0].x() < auxPointlist[1].x():
                    symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
                else:
                    symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')
            else:
                symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')

        #Horizontal
        elif (u == 1 and t == 0) or (u == UTM_num_y and t == 0):
            #Symbol vertices
            auxPointlist = self.gridLinesymbolMaker(xmin_UTM, ((floor(ymin_UTM/grid_spacing)+u)*grid_spacing), xmax_UTM, ((floor(ymin_UTM/grid_spacing)+u)*grid_spacing), xmax_source, xmin_source, ymax_source, ymin_source, trUTMLL, trLLUTM, utmcheck, False)
            #0: bottom bound; 1: upper bound
            test_line[0] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymin_source)+','+str(xmax_source)+' '+str(ymin_source)+')')
            test_line[1] = QgsGeometry.fromWkt('LINESTRING ('+str(xmin_source)+' '+str(ymax_source)+','+str(xmax_source)+' '+str(ymax_source)+')')
            test_grid = QgsGeometry.fromPolyline([auxPointlist[0],auxPointlist[1]])
            if test_line[0].intersects(test_grid):
                mid_point = test_line[0].intersection(test_grid).vertexAt(0)
                self.utmLLtransform(utmcheck, mid_point, trLLUTM)
                if auxPointlist[0].y() > auxPointlist[1].y():
                    symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
                else:
                    symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')
            elif test_line[1].intersects(test_grid):
                mid_point = test_line[1].intersection(test_grid).vertexAt(0)
                self.utmLLtransform(utmcheck, mid_point, trLLUTM)
                if auxPointlist[0].y() < auxPointlist[1].y():
                    symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(mid_point.x())+','+str(mid_point.y())+'))')
                else:
                    symb.setGeometryExpression('make_line(make_point('+str(mid_point.x())+','+str(mid_point.y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')
            else:
                symb.setGeometryExpression("make_line(make_point("+str(auxPointlist[2].x())+","+str(auxPointlist[2].y())+"), make_point("+str(auxPointlist[3].x())+","+str(auxPointlist[3].y())+"))")

        #Inner Grid Lines
        #Vertical
        elif (not(t == 1)) and (not(t == UTM_num_x)) and u == 0:
            auxPointlist = self.gridLinesymbolMaker(((floor(xmin_UTM/grid_spacing)+t)*grid_spacing), ymin_UTM, ((floor(xmin_UTM/grid_spacing)+t)*grid_spacing), ymax_UTM, xmax_source, xmin_source, ymax_source, ymin_source, trUTMLL, trLLUTM, utmcheck, True)
            symb.setGeometryExpression('make_line(make_point('+str(auxPointlist[2].x())+','+str(auxPointlist[2].y())+'), make_point('+str(auxPointlist[3].x())+','+str(auxPointlist[3].y())+'))')
        #Horizontal
        elif (not(u == 1)) and (not(u == UTM_num_y)) and t == 0:
            auxPointlist = self.gridLinesymbolMaker(xmin_UTM, ((floor(ymin_UTM/grid_spacing)+u)*grid_spacing), xmax_UTM, ((floor(ymin_UTM/grid_spacing)+u)*grid_spacing), xmax_source, xmin_source, ymax_source, ymin_source, trUTMLL, trLLUTM, utmcheck, False)
            symb.setGeometryExpression("make_line(make_point("+str(auxPointlist[2].x())+","+str(auxPointlist[2].y())+"), make_point("+str(auxPointlist[3].x())+","+str(auxPointlist[3].y())+"))")

        grid_symb.appendSymbolLayer(symb)
        return grid_symb

    def grid_labeler(self, coord_base_x, coord_base_y, px, py, u, t, dx, dy, vAlign, hAlign, desc, fSize, fontType, expression_str, trLLUTM, trUTMLL, llcolor, utmcheck, scale):
        if utmcheck:
            pgrid = QgsPoint(coord_base_x + px*u, coord_base_y + py*t)
            pgrid.transform(trLLUTM)
            pgrid = QgsPoint(pgrid.x()+ dx, pgrid.y()+ dy)
        else:
            pgrid = QgsPoint(coord_base_x + px*u + dx, coord_base_y + py*t + dy)

        #Label Format Settings
        settings = QgsPalLayerSettings()
        settings.Placement = QgsPalLayerSettings.Free
        settings.isExpression = True
        textprop = QgsTextFormat()
        textprop.setColor(llcolor)
        textprop.setSizeUnit(1)
        textprop.setSize(fSize*scale*1.324)
        textprop.setFont(QFont(fontType))
        textprop.setLineHeight(1)
        settings.setFormat(textprop)
        settings.fieldName = expression_str

        #Label Name and Position
        datadefined = QgsPropertyCollection()
        datadefined.setProperty(9, pgrid.x())
        datadefined.setProperty(10, pgrid.y())
        if not(hAlign == ''):
            datadefined.setProperty(11, hAlign)
        if not(vAlign == ''):
            datadefined.setProperty(12, vAlign)
        datadefined.setProperty(20, 1)
        
        #Creating and Activating Labeling Rule
        settings.setDataDefinedProperties(datadefined)
        rule = QgsRuleBasedLabeling.Rule(settings)
        rule.setDescription(desc)
        rule.setActive(True)
        
        return rule

    def utm_grid_labeler(self, root_rule, x_UTM, y_UTM, x_geo, y_geo, px, py, trUTMLL, trLLUTM, u, isVertical, dx, dy, dyO, dy1, vAlign, hAlign, desc, fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, rangetest, geo_bb_or):


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
        x_min = float(geo_bound_bb.split()[1])
        y_min = float(geo_bound_bb.split()[2])
        x_max = float(geo_bound_bb.split()[3])
        y_max = float(geo_bound_bb.split()[4])
        
        # Check if is labeling grid's vertical lines
        if isVertical:
            # Displacing UTM Label that overlaps Geo Label
            if utmcheck:
                dx0 = 0
            else:
                dx0 = dx
                dx = 0
            test_plac = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            test_plac.transform(trUTMLL)
            ancX = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing)+dx,y_UTM)
            ancX.transform(trUTMLL)
            ancY = QgsPoint(ancX.x(),y_geo)
            if utmcheck:
                ancY.transform(trLLUTM)
            test = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            test.transform(trUTMLL)
            if u == 1 and 'Up' in desc:
                deltaDneg = 0.0022
                deltaDpos = 0.0011
            elif u == 1 and 'Bot' in desc:
                deltaDneg = 0.00125
                deltaDpos = 0.0011
            else:
                deltaDneg = 0.00095
                deltaDpos = 0.0011
            testif = abs(floor(abs(round(test.x(), 4) - (x_min % (px)) - (deltaDneg*(fSize/1.5) * scale/10))/px) - floor(abs(round(test.x(), 4) - (x_min % (px)) + (deltaDpos*(fSize/1.5) * scale/10))/px))
            if testif >= 1:
                ancY = QgsPoint(ancY.x(),ancY.y()+dyO)
            else:
                ancY = QgsPoint(ancY.x(),ancY.y()+dy)
            x = ancX.x() + dx0
            if utmcheck:
                ancY.transform(trUTMLL)
            y =ancY.y()
            full_label = str((floor(x_UTM/grid_spacing)+u)*grid_spacing)
            if test_plac.x() < (x_min_test + (0.0005 * scale/10)) or test_plac.x() > (x_max_test - (0.0005 * scale/10)):
                rule_fake = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, vAlign, hAlign, desc, fSize, fontType, 'fail', trLLUTM, trUTMLL, QColor('black'), utmcheck, scale)
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
            if utmcheck:
                ancY.transform(trLLUTM)
            # Displacing UTM Label it overlaps with Geo Label
            test = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            test.transform(trUTMLL)
            testif = abs(floor(abs(round(test.y(), 4) - (y_min % (py)) - (0.0004*(fSize/1.5) * scale/10))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)))/py))
            if testif >= 1:
                ancY = QgsPoint(ancY.x(),ancY.y()+dy1)
            else:
                testif2 = abs(floor(abs(round(test.y(), 4) - (y_min % (py)))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)) + (0.0004*(fSize/1.5) * scale/10))/py))
                if testif2 >= 1:
                    ancY = QgsPoint(ancY.x(),ancY.y()+dyO)
                else:
                    ancY = QgsPoint(ancY.x(),ancY.y()+dy)
            if utmcheck:
                dx0 = 0
                ancX.transform(trLLUTM)
                ancX = QgsPoint(ancX.x()+dx, ancX.y())
                ancX.transform(trUTMLL)
                ancY.transform(trUTMLL)
            else:
                dx0 = dx
            x = ancX.x() + dx0
            y = ancY.y()
            full_label = str((floor(y_UTM/grid_spacing)+u)*grid_spacing)
            if test_plac.y() < (y_min_test + (0.0002 * scale/10)) or test_plac.y() > (y_max_test- (0.0002 * scale/10)):
                rule_fake = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, vAlign, hAlign, desc, fSize, fontType, 'fail', trLLUTM, trUTMLL, QColor('black'), utmcheck, scale)
                root_rule.appendChild(rule_fake)
                return root_rule

        ctrl_uni = {0:u'\u2070',1:u'\u00B9',2:u'\u00B2',3:u'\u00B3',4:u'\u2074',5:u'\u2075',6:u'\u2076',7:u'\u2077',8:u'\u2078',9:u'\u2079','m':u'\u1D50'}
        full_label = [char for char in full_label]
        for j in range(0,len(full_label)):
            if not (j == len(full_label)-5 or j == len(full_label)-4):
                full_label[j] = ctrl_uni[int(full_label[j])]
        full_label = ''.join(full_label)
        expression_str = str('\'') + full_label + str('\'')
        fontType.setWeight(50)
        fSizeAlt = fSize * 5/3
        if u == min(rangetest) and any(spec_lbl in desc for spec_lbl in ('Bot','Left')):
            extra_label = '  ' + 'N'
            dyT = 0.5*scale*fSize/1.5
            if len(expression_str) == 9:
                dxT = 3.5*scale*fSize/1.5
            elif len(expression_str) == 6:
                dxT = 1.5*scale*fSize/1.5
            elif len(expression_str) == 7:
                dxT = 2.5*scale*fSize/1.5
            if isVertical:
                extra_label = '  ' + 'E'
                dyT = 0.5*scale*fSize/1.5
                dxT = 3.0*scale*fSize/1.5
            expression_str =str('\'') + full_label + extra_label + str('\'')
            plac_m = QgsPoint(x,y)
            plac_m.transform(trLLUTM)
            plac_new = QgsPoint(plac_m.x()+dxT,plac_m.y()+dyT)
            plac_new.transform(trUTMLL)
            ruleUTM2 = self.grid_labeler(plac_new.x(), plac_new.y(), 0, 0, 0, 0, 0, 0, vAlign, 'Center', desc+'m', fSizeAlt, fontType, str('\'')+ctrl_uni['m']+str('\''), trLLUTM, trUTMLL, QColor('black'), utmcheck, scale)
            root_rule.appendChild(ruleUTM2)

        ruleUTM = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, vAlign, hAlign, desc, fSizeAlt, fontType, expression_str, trLLUTM, trUTMLL, QColor('black'), utmcheck, scale)
        root_rule.appendChild(ruleUTM)
        return root_rule

    def conv_dec_gms(self, base_coord, coord_spacing, u, neg_character, pos_character):
        
        xbase = base_coord + coord_spacing*u
        x = abs(xbase)
        xdeg = floor(round(x,4))
        xmin = floor(round(((x - xdeg)*60),4))
        xseg = floor(round(((x - xdeg - xmin/60)*3600),4))
        if xbase < 0:
            xhem = neg_character
        else:
            xhem = pos_character
        conv_exp_str = '\'' + str(xdeg).rjust(2,'0') + 'º ' + str(xmin).rjust(2,'0') + str('\\') + str('\' ') + str(xseg).rjust(2,'0') + '"\'' + '+\' ' + str(xhem) + '\''

        return conv_exp_str

    def geoGridcreator(self, grid_symb, geo_bound_bb, geo_number_x, geo_number_y, scale, utmcheck, trLLUTM):
        xmin_source = float(geo_bound_bb.split()[1])
        ymin_source = float(geo_bound_bb.split()[2])
        xmax_source = float(geo_bound_bb.split()[3])
        ymax_source = float(geo_bound_bb.split()[4])
        
        px = (xmax_source-xmin_source)/(geo_number_x+1)
        py = (ymax_source-ymin_source)/(geo_number_y+1)
        
        for u in range(1, (geo_number_x+2)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, -0.00002145*scale, 0, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(1, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0, -0.00002145*scale, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+1)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0.00002145*scale, 0, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(0, (geo_number_y+1)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0, 0.00002145*scale, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        
        return grid_symb

    def geoGridlabelPlacer(self, geo_bound_bb, geo_number_x, geo_number_y, dx, dy, fSize, LLfontType, trLLUTM, trUTMLL, llcolor, utmcheck, scale):
        xmin_source = float(geo_bound_bb.split()[1])
        ymin_source = float(geo_bound_bb.split()[2])
        xmax_source = float(geo_bound_bb.split()[3])
        ymax_source = float(geo_bound_bb.split()[4])

        px = (xmax_source-xmin_source)/(geo_number_x+1)
        py = (ymax_source-ymin_source)/(geo_number_y+1)

        root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())

        #Upper
        for u in range(0, geo_number_x+2):
            if u ==0:
                ruletemp = self.grid_labeler (xmin_source, ymax_source, px, py, u, 0, dx[2], dy[0], '', 'Center', 'Up '+str(u+1), fSize, LLfontType, str(self.conv_dec_gms(xmin_source, px, u, 'W', 'E'))+'+\'. GREENWICH\'', trLLUTM, trUTMLL, llcolor, utmcheck, scale)
                root_rule.appendChild(ruletemp)
            else:
                ruletemp = self.grid_labeler (xmin_source, ymax_source, px, py, u, 0, 0, dy[0], '', 'Center', 'Up '+str(u+1), fSize, LLfontType, self.conv_dec_gms(xmin_source, px, u, 'W', 'E'), trLLUTM, trUTMLL, llcolor, utmcheck, scale)
                root_rule.appendChild(ruletemp)
        #Bottom
        for b in range(0, geo_number_x+2):
            ruletemp = self.grid_labeler (xmin_source, ymin_source, px, py, b, 0, 0, dy[1], '', 'Center', 'Bot '+str(b+1), fSize, LLfontType, self.conv_dec_gms(xmin_source, px, b, 'W', 'E'), trLLUTM, trUTMLL, llcolor,  utmcheck, scale)
            root_rule.appendChild(ruletemp)
        #Right
        for r in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler (xmax_source, ymin_source, px, py, 0, r, dx[0], 0, 'Half', '', 'Right '+str(r+1), fSize, LLfontType, self.conv_dec_gms(ymin_source, py, r, 'S', 'N'), trLLUTM, trUTMLL, llcolor, utmcheck, scale)
            root_rule.appendChild(ruletemp)
        #Left
        for l in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler (xmin_source, ymin_source, px, py, 0, l, dx[1], 0, 'Half', '', 'Left '+str(l+1), fSize, LLfontType, self.conv_dec_gms(ymin_source, py, l, 'S', 'N'), trLLUTM, trUTMLL, llcolor, utmcheck, scale)
            root_rule.appendChild(ruletemp)

        return root_rule

    def utmGridlabelPlacer(self, root_rule, grid_spacing, geo_bound_bb, bound_UTM_bb, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, trUTMLL, trLLUTM, dx, dy, dy0, dy1, fSize, fontType, scale, utmcheck, geo_bb_or):
        xmin_source = float(geo_bound_bb.split()[1])
        ymin_source = float(geo_bound_bb.split()[2])
        xmax_source = float(geo_bound_bb.split()[3])
        ymax_source = float(geo_bound_bb.split()[4])
        xmin_UTM = float(bound_UTM_bb.split()[1])
        ymin_UTM = float(bound_UTM_bb.split()[2])
        xmax_UTM = float(bound_UTM_bb.split()[3])
        ymax_UTM = float(bound_UTM_bb.split()[4])
        px = (xmax_source-xmin_source)/(geo_number_x+1)
        py = (ymax_source-ymin_source)/(geo_number_y+1)

        if grid_spacing > 0:
            # Bottom
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler (ruletest, xmin_UTM, ymin_UTM, 0, ymin_source, px, py, trUTMLL, trLLUTM, 1, True, 0, dy[1]+0.4*(scale)*fSize/1.5, dy0[1]+0.4*(scale)*fSize/1.5, 0, 'Top', 'Center', 'UTMBotTest', fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, range(1), geo_bb_or)
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == 'fail':
                rangeUD = range(2, UTM_num_x+1)
            else:
                rangeUD = range(1, UTM_num_x+1)

            for u in rangeUD:
                root_rule = self.utm_grid_labeler (root_rule, xmin_UTM, ymin_UTM, 0, ymin_source, px, py, trUTMLL, trLLUTM, u, True, 0, dy[1]+0.4*(scale)*fSize/1.5, dy0[1]+0.4*(scale)*fSize/1.5, 0, 'Top', 'Center', 'UTMBot'+str(u), fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, rangeUD, geo_bb_or)

            # Upper
            rangeUD = range(1, UTM_num_x+1)
            for u in rangeUD:
                root_rule = self.utm_grid_labeler (root_rule, xmin_UTM, ymax_UTM, 0, ymax_source, px, py, trUTMLL, trLLUTM, u, True, 0, dy[0]-1.3*(scale)*fSize/1.5, dy0[0]-1.3*(scale)*fSize/1.5, 0, 'Bottom', 'Center', 'UTMUp'+str(u), fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, rangeUD, geo_bb_or)

            # Left
            ruletest = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
            ruletest = self.utm_grid_labeler (ruletest, xmin_UTM, ymin_UTM, xmin_source, 0, px, py, trUTMLL, trLLUTM, 1, False, dx[2]-3.1*scale*fSize/1.5, dy[3], dy0[3], dy1[1], 'Bottom', 'Center', 'UTMLeftTest', fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, range(1), geo_bb_or)
            rulechild = ruletest.children()[0]
            if rulechild.settings().fieldName == 'fail':
                rangeLat = range(2, UTM_num_y+1)
            else:
                rangeLat = range(1, UTM_num_y+1)
            for u in rangeLat:
                if u==min(rangeLat): 
                    extra_dist = -2.0*scale*fSize/1.5
                else:
                    extra_dist = 0
                root_rule = self.utm_grid_labeler (root_rule, xmin_UTM, ymin_UTM, xmin_source, 0, px, py, trUTMLL, trLLUTM, u, False, dx[2]+extra_dist, dy[3], dy0[3], dy1[1], 'Bottom', 'Center', 'UTMLeft'+str(u), fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, rangeLat, geo_bb_or)

            # Right
            rangeLat = range(1, UTM_num_y+1)
            for u in rangeLat:
                root_rule = self.utm_grid_labeler (root_rule, xmax_UTM, ymin_UTM, xmax_source, 0, px, py, trUTMLL, trLLUTM, u, False, dx[3], dy[3], dy0[3], dy1[1], '', 'Center', 'UTMRight'+str(1), fSize, fontType, grid_spacing, scale, utmcheck, geo_bound_bb, rangeLat, geo_bb_or)

        return root_rule

    def styleCreator(self, layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, fontLL, llcolor, utmcheck):
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

        #Getting Feature Source CRS and Geometry
        if utmcheck:
            feature_geometry = feature_bound.geometry()
            bound_UTM = layer_bound.crs().authid()
            feature_bbox = feature_geometry.boundingBox()
            bound_UTM_bb = str(feature_bbox).replace(',','').replace('>','')
            # Transforming to Geographic
            transform_feature = QgsCoordinateTransform(QgsCoordinateReferenceSystem(bound_UTM), QgsCoordinateReferenceSystem('EPSG:4674'), QgsProject.instance())
            feature_geometry.transform(transform_feature)
            bound_sourcecrs = 'EPSG:4674'
            feature_bbox = feature_geometry.boundingBox()
            feature_bbox_or = feature_geometry.orientedMinimumBoundingBox()
        else:
            feature_geometry = feature_bound.geometry()
            bound_sourcecrs = layer_bound.crs().authid()
            feature_bbox = feature_geometry.boundingBox()
            feature_bbox_or = feature_geometry.orientedMinimumBoundingBox()
        geo_bound_bb = str(feature_bbox).replace(',','').replace('>','')
        oriented_geo_bb = str(feature_bbox_or).replace(',','').replace('>','').replace('((','').replace('))','')

        #Defining CRSs Transformations
        inom = feature_bound[index]
        if inom[0]=='N': 
            bound_UTM = 'EPSG:319' + str(72 + int(inom[3:5])-18)
        elif inom[0]=='S': 
            bound_UTM = 'EPSG:319' + str(78 + int(inom[3:5])-18) 
        else:
            iface.messageBar().pushMessage("Error", "Invalid index attribute", level=Qgis.Critical)
            return
        trLLUTM = QgsCoordinateTransform(QgsCoordinateReferenceSystem(bound_sourcecrs), QgsCoordinateReferenceSystem(bound_UTM), QgsProject.instance())
        trUTMLL = QgsCoordinateTransform(QgsCoordinateReferenceSystem(bound_UTM), QgsCoordinateReferenceSystem(bound_sourcecrs), QgsProject.instance())

        #Defining UTM Grid Symbology Type
        renderer = layer.renderer()
        properties = {'color': 'black'}
        grid_symb = QgsFillSymbol.createSimple(properties)
        symb_out = QgsSimpleFillSymbolLayer()
        symb_out.setStrokeColor(QColor('black'))
        symb_out.setFillColor(QColor('white'))
        symb_out.setStrokeWidth(0.05)


        """ Creating UTM Grid """
        if not utmcheck:
            geo_UTM = feature_bound.geometry()
            geo_UTM.transform(trLLUTM)
            bound_UTM_bb = str(geo_UTM.boundingBox()).replace(',','').replace('>','')
        xmin_UTM = float(bound_UTM_bb.split()[1])
        ymin_UTM = float(bound_UTM_bb.split()[2])
        xmax_UTM = float(bound_UTM_bb.split()[3])
        ymax_UTM = float(bound_UTM_bb.split()[4])

        if grid_spacing > 0:
            UTM_num_x = floor(xmax_UTM/grid_spacing) - floor(xmin_UTM/grid_spacing)
            UTM_num_y = floor(ymax_UTM/grid_spacing) - floor(ymin_UTM/grid_spacing)
            #Generating Vertical Lines
            for x in range(1, UTM_num_x+1):
                grid_symb= self.utm_symb_generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, x, 0, geo_bound_bb, bound_UTM_bb, utmcheck)
            #Generating Horizontal Lines
            for y in range(1, UTM_num_y+1):
                grid_symb = self.utm_symb_generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, 0, y, geo_bound_bb, bound_UTM_bb, utmcheck)

        """ Creating Geo Grid """
        grid_symb = self.geoGridcreator(grid_symb, geo_bound_bb, geo_number_x, geo_number_y, scale, utmcheck, trLLUTM)

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
        if utmcheck:
            dx = [2*scale*fSize/1.5, -13.6*scale*fSize/1.5, 6*scale*fSize/1.5]
            dy = [1.7*scale*fSize/1.5, -3.8*scale*fSize/1.5]
        else:
            dx = [0.000018*scale, -0.000120*scale, 0.00005*scale]
            dy = [0.000015*scale, -0.000040*scale]

        root_rule = self.geoGridlabelPlacer(geo_bound_bb, geo_number_x, geo_number_y, dx, dy, fSize, LLfontType, trLLUTM, trUTMLL, llcolor, utmcheck, scale)

        """ Labeling UTM Grid"""
        if utmcheck:
            dx = [-2.7, -9.7, -6.2, 5.4]
            dx = [i*scale*fSize/1.5 for i in dx]
            dy = [2.5, -1.7, -0.5, -1.5]
            dy = [i*scale*fSize/1.5 for i in dy]
            dy0 = [5.45, -4.8, -3.2, -4.2]
            dy0 = [i*scale*fSize/1.5 for i in dy0]
            dy1 = [2.15, 1.2]
            dy1 = [i*scale*fSize/1.5 for i in dy1]
        else:
            dx = [-0.00003, -0.000107, -0.000070, 0.000060]
            dx = [i*scale*fSize/1.5 for i in dx]
            dy = [0.000027, 0.000016, -0.000041, -0.000052]
            dy = [i*scale*fSize/1.5 for i in dy]
            dy0 = [0.0000644, 0.000053, -0.000076, -0.000087]
            dy0 = [i*scale*fSize/1.5 for i in dy0]
            dy1 = [0.000032, 0.000020]
            dy1 = [i*scale*fSize/1.5 for i in dy1]

        root_rule = self.utmGridlabelPlacer(root_rule, grid_spacing, geo_bound_bb, bound_UTM_bb, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, trUTMLL, trLLUTM, dx, dy, dy0, dy1, fSize, fontType, scale, utmcheck, oriented_geo_bb)


        """ Activating Labels """
        rules = QgsRuleBasedLabeling(root_rule)
        layer.setLabeling(rules)
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()
        return
