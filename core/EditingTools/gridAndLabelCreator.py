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
                      QgsCoordinateReferenceSystem, QgsFillSymbol, \
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
    
    def geo_test(self, layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font):
        if layer.crs().isGeographic() == False:
            self.styleCreator(layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, True)
        else:
            self.styleCreator(layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, False)
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
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(1)
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

    def utm_symb_generator(self, grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, t, u, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM, utmcheck):
    
        test_line = [None]*2
        symb = QgsGeometryGeneratorSymbolLayer.create(properties)
        symb.setSymbolType(1)

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

    def grid_labeler(self, coord_base_x, coord_base_y, px, py, u, t, dx, dy, vAlign, hAlign, desc, fSize, fontType, expression_str, trLLUTM, utmcheck):
        pgrid = QgsPoint(coord_base_x + px*u + dx, coord_base_y + py*t + dy)
        self.utmLLtransform(utmcheck, pgrid, trLLUTM)
        #Label Format Settings
        settings = QgsPalLayerSettings()
        settings.Placement = QgsPalLayerSettings.Free
        settings.isExpression = True
        textprop = QgsTextFormat()
        textprop.setColor(QColor(0,0,0,255))
        textprop.setSize(fSize)
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

        #Creating and Activating Labeling Rule
        settings.setDataDefinedProperties(datadefined)
        rule = QgsRuleBasedLabeling.Rule(settings)
        rule.setDescription(desc)
        rule.setActive(True)
        
        return rule

    def utm_grid_labeler(self, x_UTM, y_UTM, x_geo, y_geo, x_min, y_min, px, py, trUTMLL, trLLUTM, u, isVertical, dx, dy, dyO, dy1, label_index, vAlign, hAlign, desc, fSize, fontType, grid_spacing, map_scale, utmcheck):

        # Check if is labeling grid's vertical lines
        if isVertical:
            x = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            x.transform(trUTMLL)
            x = x.x()+dx

            # Displacing UTM Label it overlaps with Geo Label
            y = y_geo
            test = QgsPoint(((floor(x_UTM/grid_spacing)+u)*grid_spacing),y_UTM)
            test.transform(trUTMLL)
            testif = abs(floor(abs(round(test.x(), 4) - (x_min % (px)) - (0.001 *map_scale/10000))/px) - floor(abs(round(test.x(), 4) - (x_min % (px)) + (0.001 *map_scale/10000))/px))
            if testif >= 1:
                y = y+dyO
            else:
                y = y+dy

            full_label = str((floor(x_UTM/grid_spacing)+u)*grid_spacing)

        # Labeling grid's horizontal lines
        else:
            x = x_geo+dx
            # Displacing UTM Label it overlaps with Geo Label
            y = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            y.transform(trUTMLL)
            y = y.y()
            test = QgsPoint(x_UTM,(floor(y_UTM/grid_spacing)+u)*grid_spacing)
            test.transform(trUTMLL)
            testif = abs(floor(abs(round(test.y(), 4) - (y_min % (py)) - (0.0004 *map_scale/10000))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)))/py))
            if testif >= 1:
                y = y+dy1
            else:
                testif2 = abs(floor(abs(round(test.y(), 4) - (y_min % (py)))/py) - floor(abs(round(test.y(), 4) - (y_min % (py)) + (0.0004 *map_scale/10000))/py))
                if testif2 >= 1:
                    y = y+dyO
                else:
                    y = y+dy
            full_label = str((floor(y_UTM/grid_spacing)+u)*grid_spacing)

        if label_index == 1:
            expression_str = full_label[ : len( full_label )-5]
        elif label_index == 2:
            expression_str = str('\'')+full_label[len( full_label )-5 : -3]+str('\'')
            fSize = 7.08*fSize/4.25
        elif label_index == 3:
            expression_str = str('\'')+full_label[-3 : ]+str('\'')

        ruleUTM = self.grid_labeler(x, y, 0, 0, 0, 0, 0, 0, vAlign, hAlign, desc, fSize, fontType, expression_str, trLLUTM, utmcheck)

        return ruleUTM

    def conv_dec_gms(self, base_coord, coord_spacing, u, neg_character, pos_character):
        
        x = base_coord + coord_spacing*u
        conv_exp_str = 'concat(floor(round(abs('+str(x)+'),4)),'+str('\'º\'')+','+str('\' \'')+', if(round((round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60-floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x) \
            +'),4)),4)*60))*60) = 60, concat(floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60)+1,'+str('\' 0\'\'\'')+'), concat(floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60),'+str('\'"\'') \
            +','+str('\' \'')+',round((round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60-floor(round((-floor(round(abs('+str(x)+'),4))+round(abs('+str(x)+'),4)),4)*60))*60),'+str('\'\'\'\'')+')),if('+str(x) \
            +'<0, '+str('\' ')+neg_character+str('\'')+','+str('\' ')+pos_character+str('\'')+'))'

        return conv_exp_str

    def styleCreator(self, layer, index, id_attr, id_value, spacing, crossX, crossY, scale, color, fontSize, font, utmcheck):
        """Getting Input Data For Grid Generation"""
        grid_spacing = spacing
        geo_number_x = crossX
        geo_number_y = crossY
        map_scale = scale*1000
        grid_color = color
        fSize = fontSize
        fontType = font

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
        else:
            bound_sourcecrs = layer_bound.crs().authid()
            feature_bbox = feature_bound.geometry().boundingBox()
        geo_bound_bb = str(feature_bbox).replace(',','').replace('>','')

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
        symb_out.setStrokeColor(QColor('white'))
        symb_out.setFillColor(QColor('white'))


        """ Creating UTM Grid """
        if not utmcheck:
            geo_UTM = feature_bound.geometry()
            geo_UTM.transform(trLLUTM)
            bound_UTM_bb = str(geo_UTM.boundingBox()).replace(',','').replace('>','')
        xmin_source = float(geo_bound_bb.split()[1])
        ymin_source = float(geo_bound_bb.split()[2])
        xmax_source = float(geo_bound_bb.split()[3])
        ymax_source = float(geo_bound_bb.split()[4])
        xmin_UTM = float(bound_UTM_bb.split()[1])
        ymin_UTM = float(bound_UTM_bb.split()[2])
        xmax_UTM = float(bound_UTM_bb.split()[3])
        ymax_UTM = float(bound_UTM_bb.split()[4])

        if grid_spacing > 0:
            UTM_num_x = floor(xmax_UTM/grid_spacing) - floor(xmin_UTM/grid_spacing)
            UTM_num_y = floor(ymax_UTM/grid_spacing) - floor(ymin_UTM/grid_spacing)
            #Generating Vertical Lines
            for x in range(1, UTM_num_x+1):
                grid_symb= self.utm_symb_generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, x, 0, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM, utmcheck)
            #Generating Horizontal Lines
            for y in range(1, UTM_num_y+1):
                grid_symb = self.utm_symb_generator (grid_spacing, trUTMLL, trLLUTM, grid_symb, properties, geo_number_x, geo_number_y, UTM_num_x, UTM_num_y, 0, y, xmin_source, xmax_source, ymin_source, ymax_source, xmin_UTM, xmax_UTM, ymin_UTM, ymax_UTM, utmcheck)

        """ Creating Geo Grid """
        px = (xmax_source-xmin_source)/(geo_number_x+1)
        py = (ymax_source-ymin_source)/(geo_number_y+1)
        map_scaleX = scale/10
        #Generating Crosses
        for u in range(1, (geo_number_x+2)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, -0.0003215*map_scaleX, 0, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(1, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0, -0.0003215*map_scaleX, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+1)):
            for t in range(0, (geo_number_y+2)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0.0003215*map_scaleX, 0, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)
        for u in range(0, (geo_number_x+2)):
            for t in range(0, (geo_number_y+1)):
                symb_cross = self.crossLinegenerator(xmin_source, ymin_source, px, py, u, t, 0, 0.0003215*map_scaleX, utmcheck, trLLUTM)
                grid_symb.appendSymbolLayer(symb_cross)

        """ Rendering UTM and Geographic Grid """
        #Changing UTM Grid Color
        grid_symb.setColor(grid_color)
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
        root_rule = QgsRuleBasedLabeling.Rule(QgsPalLayerSettings())
        #Upper
        for u in range(0, geo_number_x+2):
            ruletemp = self.grid_labeler (xmin_source, ymax_source, px, py, u, 0, 0, (0.00015*map_scaleX), '', 'Center', 'Up '+str(u+1), fSize, fontType, self.conv_dec_gms(xmin_source, px, u, 'W', 'E'), trLLUTM, utmcheck)
            root_rule.appendChild(ruletemp)
        #Bottom
        for b in range(0, geo_number_x+2):
            ruletemp = self.grid_labeler (xmin_source, ymin_source, px, py, b, 0, 0, (-0.00040*map_scaleX), '', 'Center', 'Bot '+str(b+1), fSize, fontType, self.conv_dec_gms(xmin_source, px, b, 'W', 'E'), trLLUTM, utmcheck)
            root_rule.appendChild(ruletemp)
        #Right
        for r in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler (xmax_source, ymin_source, px, py, 0, r, (0.00018*map_scaleX), 0, 'Half', '', 'Right '+str(r+1), fSize, fontType, self.conv_dec_gms(ymin_source, py, r, 'S', 'N'), trLLUTM, utmcheck)
            root_rule.appendChild(ruletemp)
        #Left
        for l in range(0, geo_number_y+2):
            ruletemp = self.grid_labeler (xmin_source, ymin_source, px, py, 0, l, (-0.00120*map_scaleX), 0, 'Half', '', 'Left '+str(l+1), fSize, fontType, self.conv_dec_gms(ymin_source, py, l, 'S', 'N'), trLLUTM, utmcheck)
            root_rule.appendChild(ruletemp)

        """ Labeling UTM Grid"""
        if grid_spacing > 0:
            for u in range(1, UTM_num_x+1):
                # Upper
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (-0.00030*map_scaleX), (0.00024*map_scaleX), (0.00052*map_scaleX), 0, 1, '', '', 'UTMUp'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, 0, (0.00012*map_scaleX), (0.00040*map_scaleX), 0, 2, '', 'Center', 'UTMUp'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymax_UTM, 0, ymax_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (0.00018*map_scaleX), (0.00024*map_scaleX), (0.00052*map_scaleX), 0, 3, '', '', 'UTMUp'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                # Bottom
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True,(-0.00030*map_scaleX), (-0.00028*map_scaleX), (-0.00075*map_scaleX), 0, 1, '', '', 'UTMBot'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, 0, (-0.00039*map_scaleX), (-0.00087*map_scaleX), 0, 2, '', 'Center', 'UTMBot'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, 0, ymin_source, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, True, (0.00018*map_scaleX), (-0.00028*map_scaleX), (-0.00075*map_scaleX), 0, 3, '', '', 'UTMBot'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)

            for u in range(1, UTM_num_y+1):
                # Left
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00110*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 1, '', '', 'UTMLeft'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00070*map_scaleX), (-0.00015*map_scaleX), (0.00052*map_scaleX), (0.00020*map_scaleX), 2, '', 'Center', 'UTMLeft'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmin_UTM, ymin_UTM, xmin_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (-0.00050*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 3, '', '', 'UTMLeft'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                # Right
                ruletemp = self.utm_grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00010*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 1, '', '', 'UTMRight'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00050*map_scaleX), (-0.00015*map_scaleX), (0.00052*map_scaleX), (0.00020*map_scaleX), 2, '', 'Center', 'UTMRight'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)
                ruletemp = self.utm_grid_labeler (xmax_UTM, ymin_UTM, xmax_source, 0, xmin_source, ymin_source, px, py, trUTMLL, trLLUTM, u, False, (0.00070*map_scaleX), (-0.00003*map_scaleX), (0.00064*map_scaleX), (0.00032*map_scaleX), 3, '', '', 'UTMRight'+str(u), fSize, fontType, grid_spacing, map_scale, utmcheck)
                root_rule.appendChild(ruletemp)

        """ Activating Labels """
        rules = QgsRuleBasedLabeling(root_rule)
        layer.setLabeling(rules)
        layer.setLabelsEnabled(True)
        layer.triggerRepaint()
        return
