# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadByClass
                                 A QGIS plugin
 Load database classes.
                             -------------------
        begin                : 2014-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
        mod history          : 2014-12-17 by Leonardo Lourenço - Computing Engineer @ Brazilian Army
        mod history          : 2014-12-17 by Maurício de Paulo - Cartographic Engineer @ Brazilian Army
        mod history          : 2020-04-01 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from __future__ import print_function
from builtins import range
from qgis.core import QgsPointXY, QgsGeometry, QgsFeature
import string, os, math, itertools, csv
from qgis.PyQt.QtCore import QObject

class UtmGrid(QObject):
    def __init__(self):
        """Constructor."""
        super(UtmGrid,self).__init__()
        self.scales=[1000,500,250,100,50,25,10,5,2,1]
        nomen1000=['Nao Recorta']
        nomen500=[['V','X'],['Y','Z']]
        nomen250=[['A','B'],['C','D']]
        nomen100=[['I','II','III'],['IV','V','VI']]
        nomen50=[['1','2'],['3','4']]
        nomen25=[['NO','NE'],['SO','SE']]
        nomen10=[['A','B'],['C','D'],['E','F']]
        nomen5=[['I','II'],['III','IV']]
        nomen2=[['1', '2', '3'], ['4', '5', '6']]
        nomen1=[['A','B'],['C','D']]
        self.scaleText=[nomen1000,nomen500,nomen250,nomen100,nomen50,nomen25,nomen10,nomen5,nomen2,nomen1]
        self.matrizRecorte=[]
        self.spacingX=[]
        self.spacingY=[]
        self.stepsDone=0
        self.stepsTotal=0
        self.featureBuffer=[]
        self.MIdict=[]
        self.MIRdict=[]
        
    def __del__(self):
        """Destructor."""
        pass
    
    def findScaleText(self,scaleText,scaleId):
        """Get the scale matrix for the given scaleText and scaleId
        """
        j=-1
        for j,row in enumerate(self.scaleText[scaleId]):
            if (scaleText in row):
                i=row.index(scaleText)
                break
        return (i,len(self.scaleText[scaleId])-j-1) 
        
    def getScale(self, inomen):
        """Get scale for the given map index
        """
        return self.scales[ self.getScaleIdFromiNomen(inomen) ]
    
    def getScaleIdFromiNomen(self, inomen):
        """Get scale index in self.scales object for the given map index
        """
        id = len(inomen.split('-')) - 2
        return id
     
    def getScaleIdFromScale(self, scale):
        """Get scale if for the given scale (e.g. 1, 2, 25, 250)
        """
        return self.scales.index(scale)

    def getSpacingX(self,scale):
        """Get X spacing for the given scale
        """
        scaleId=self.scales.index(scale)
        if (scaleId<0): return 0
        if (len(self.spacingX)==0):
            dx=6
            self.spacingX=[dx]
            for i in range(1,len(self.scaleText)):
                subdivisions=len(self.scaleText[i][0])
                dx/=float(subdivisions)
                self.spacingX.append(dx)
        return self.spacingX[scaleId]
    
    def getSpacingY(self,scale): 
        """Get Y spacing for the given scale
        """
        scaleId=self.scales.index(scale)
        if (scaleId<0): return 0
        if (len(self.spacingY)==0):
            dy=4
            self.spacingY=[dy]
            for i in range(1,len(self.scaleText)):
                subdivisions=len(self.scaleText[i])
                dy/=float(subdivisions)
                self.spacingY.append(dy)
        return self.spacingY[scaleId]
    
    def makeQgsPolygon(self, xmin, ymin, xmax, ymax):
        """Creating a polygon for the given coordinates
        """
        dx = (xmax - xmin)/3
        dy = (ymax - ymin)/3
        
        polyline = []

        point = QgsPointXY(xmin, ymin)
        polyline.append(point)
        point = QgsPointXY(xmin+dx, ymin)
        polyline.append(point)
        point = QgsPointXY(xmax-dx, ymin) 
        polyline.append(point)
        point = QgsPointXY(xmax, ymin)
        polyline.append(point)
        point = QgsPointXY(xmax, ymin+dy)
        polyline.append(point)
        point = QgsPointXY(xmax, ymax-dy)
        polyline.append(point)
        point = QgsPointXY(xmax, ymax)
        polyline.append(point)
        point = QgsPointXY(xmax-dx, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin+dx, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin, ymax)
        polyline.append(point)
        point = QgsPointXY(xmin, ymax-dy)
        polyline.append(point)
        point = QgsPointXY(xmin, ymin+dy)
        polyline.append(point)
        point = QgsPointXY(xmin, ymin)
        polyline.append(point)

        qgsPolygon = QgsGeometry.fromMultiPolygonXY([[polyline]])
        return qgsPolygon
        
    def getHemisphereMultiplier(self,inomen):
        """Check the hemisphere
        """
        if (len(inomen) > 1):
            h = inomen[0].upper()
            if (h=='S'):
                return -1
            else:
                return 1

    def getLLCornerLatitude1kk(self,inomen):
        """Get lower left Latitude for 1:1.000.000 scale
        """
        try:
            l=inomen[1].upper()
            y = 0.0
            operator=self.getHemisphereMultiplier(inomen)
            verticalPosition=string.ascii_uppercase.index(l)
            y=(y+4*verticalPosition)*operator
            if (operator<0): y-=4
        except:
            raise Exception(self.tr('Invalid inomen parameter!'))
        return y

    def getLLCornerLongitude1kk(self,inomen):
        """Get lower left Longitude for 1:1.000.000 scale
        """
        try:
            fuso=int(inomen[3:5])
            x=0  
            if((fuso > 0) and (fuso <= 60)):
                x = (((fuso - 30)*6.0)-6.0)
            return x
        except:
            raise Exception(self.tr('Invalid inomen parameter!'))
    
    def getLLCorner(self,inomen):
        """Get lower left coordinates for scale determined by the given map index
        """
        try:
            x=self.getLLCornerLongitude1kk(inomen)
            y=self.getLLCornerLatitude1kk(inomen)
            inomenParts=inomen.upper().split('-')
            #Escala de 500.00
            for partId in range(2,len(inomenParts)):
                scaleId=partId-1
                dx=self.getSpacingX(self.scales[scaleId])
                dy=self.getSpacingY(self.scales[scaleId])
                scaleText=inomenParts[partId]
                i,j=self.findScaleText(scaleText, partId-1)
                x+=i*dx
                y+=j*dy
            return (x,y)
        except:
            raise Exception(self.tr('Invalid inomen parameter!'))
    
    def computeNumberOfSteps(self,startScaleId,stopScaleId):
        """Compute the number of steps to build a progress
        """
        steps=1
        for i in range(startScaleId+1,stopScaleId+1):
            steps*=len(self.scaleText[i])*len(self.scaleText[i][0])
        return steps
    
    def createFrame(self, map_index, layer):
        stopScale = self.getScale(map_index)
        
        # Enter in edit mode
        layer.startEditing()

        self.populateQgsLayer(map_index, stopScale, layer)

        # Commiting changes        
        layer.commitChanges()        
    
    def createFrame(self, map_index, layer, stopScale):
        # Enter in edit mode
        layer.startEditing()

        self.populateQgsLayer(map_index, stopScale, layer)

        # Commiting changes        
        layer.commitChanges()
        
    def getQgsPolygonFrame(self, map_index):
        """Particular case used to create frame polygon for the given
        map_index
        """
        scale = self.getScale(map_index)
        (x, y) = self.getLLCorner(map_index)
        dx = self.getSpacingX(scale)
        dy = self.getSpacingY(scale)
        poly = self.makeQgsPolygon(x, y, x + dx, y + dy)
        return poly
    
    def populateQgsLayer(self, iNomen, stopScale, layer):
        """Generic recursive method to create frame polygon for the given
        stopScale within the given map index (iNomen)
        """
        scale = self.getScale(iNomen)            
        #first run
        if (self.stepsTotal==0):
            self.stepsTotal=self.computeNumberOfSteps(self.getScaleIdFromScale(scale), self.getScaleIdFromScale(stopScale))
            # fix_print_with_import
            print("Total:",self.stepsTotal)
            self.stepsDone=0
        if scale == stopScale:
            (x, y) = self.getLLCorner(iNomen)
            dx = self.getSpacingX(stopScale)
            dy = self.getSpacingY(stopScale)
            poly = self.makeQgsPolygon(x, y, x + dx, y + dy)
            
            self.insertFrameIntoQgsLayer(layer, poly, iNomen)
            
            self.stepsDone+=1
            # fix_print_with_import
            print(self.stepsDone, '/', self.stepsTotal)
        else:
            scaleId = self.getScaleIdFromiNomen(iNomen)
            matrix = self.scaleText[ scaleId+1 ]
            
            for i in range(len(matrix)):
                line = matrix[i]
                for j in range(len(line)):
                    inomen2 = iNomen + '-' + line[j]
                    self.populateQgsLayer(inomen2, stopScale, layer)
                    
    def insertFrameIntoQgsLayer(self, layer, poly, map_index):
        """Inserts the poly into layer
        """
        provider = layer.dataProvider()

        #Creating the feature
        feature = QgsFeature()
        feature.initAttributes(1)
        feature.setAttribute(0, map_index)
        feature.setGeometry(poly)

        # Adding the feature into the file
        provider.addFeatures([feature])
    
    def getMIdict(self):
        if not self.MIdict:
            self.MIdict = self.getDict("MI100.csv")
        return self.MIdict
            
    def getMIRdict(self):
        if not self.MIRdict:
            self.MIRdict = self.getDict("MIR250.csv")
        return self.MIRdict    
    
    def getDict(self, file_name):    
        csvFile = open(os.path.join(os.path.dirname(__file__),file_name))
        data = csvFile.readlines()
        csvFile.close()
        l1 = [(x.strip()).split(';') for x in data]
        dicionario = dict((a[1],a[0]) for a in l1)
        return dicionario

    def getINomenFromMI(self,mi):
        mi = self.checkLeftPaddingMI(mi)
        inom = self.getINomen(self.getMIdict(), mi)
        if inom in self.getMIexceptions():
            return ''
        return inom

    def getINomenFromMIR(self,mir):
        inom = self.getINomen(self.getMIRdict(), mir)
        if inom in self.getMIexceptions():
            return ''
        return inom
        
    def getINomen(self, dict, index):
        key = index.split('-')[0]
        otherParts = index.split('-')[1:]
        if (key in dict):
            if len(otherParts)==0:
                return dict[key]
            else:
                return dict[key]+'-'+'-'.join(otherParts)
        else:
            return ''
    
    def getMIfromInom(self,inom):
        return self.getMI(self.getMIdict(),inom)
    
    def getMI(self, miDict, inom):
        parts = inom.split('-')
        hundredInom = '-'.join(parts[0:5])
        remains = parts[5::]
        for k,v in miDict.items():
            if v == hundredInom:
                return '-'.join([k]+remains)
    
    def getMIR(self, miDict, inom):
        parts = inom.split('-')
        hundredInom = '-'.join(parts[0:4])
        remains = parts[4::]
        for k,v in miDict.items():
            if v == hundredInom:
                return '-'.join([k]+remains)
    
    def get_MI_MIR_from_inom(self, inom):
        if inom in self.getMIexceptions():
            return ''
        if len(inom.split('-')) > 4:
            return self.getMIfromInom(inom)
        else:
            return self.getMIR(self.getMIRdict(), inom)

    def get_INOM_from_lat_lon(self, lon, lat):
        """
        Returns Inom with the nearest lower left lon lat.
        """
        INOM = 'N' if lat >= 0 else 'S'
        INOM += string.ascii_uppercase[math.floor(abs(lat/4.)) % 26] + '-'
        utm_zone = math.floor(31 + lon/6)
        return INOM+str(utm_zone)
    
    def get_INOM_range_from_BB(self, xmin, ymin, xmax, ymax):
        """
        Returns a set of INOM that intersect bbRect formed by 
        xmin, xmax, ymin, ymax
        """
        minInom = self.get_INOM_from_lat_lon(xmin, ymin)
        maxInom = self.get_INOM_from_lat_lon(xmax, ymax)
        if minInom == maxInom:
            return list([minInom])
        return self.get_INOM_range_from_min_max_inom(minInom, maxInom)
    
    def get_INOM_range_from_min_max_inom(self, minInom, maxInom):
        minFuse = int(minInom.split('-')[-1])
        maxFuse = int(maxInom.split('-')[-1])
        fuseRange = map(str, range(minFuse,maxFuse+2,1))
        letterRange = self.get_letter_range(minInom, maxInom)
        return list(
            '-'.join(i) for i in itertools.product(letterRange, fuseRange)
        )

    def get_letter_range(self, minInom, maxInom):
        if minInom[0] == 'S' and maxInom[0] == 'N':
            return self.get_letter_range('SA-XX', minInom) + self.get_letter_range('NA-XX', maxInom)
        else:
            startIndex = string.ascii_uppercase.index(minInom[1])
            endIndex = string.ascii_uppercase.index(maxInom[1])
            multiplier = 1 if minInom[0] == 'N' else -1
            return list(
                map(
                    lambda x: minInom[0]+x,
                    string.ascii_uppercase[min(startIndex, endIndex):max(startIndex, endIndex)+3:1]
                )
            )[::multiplier]
    
    @staticmethod
    def getMIexceptions():
        '''
        Returns a set of INOMs that don't have MI
        '''
        pathCsvExceptions25k = os.path.join(os.path.dirname(__file__),'exclusionList25k.csv')
        pathCsvExceptions50k = os.path.join(os.path.dirname(__file__),'exclusionList50k.csv')
        with open(pathCsvExceptions25k, 'r') as file:
            exceptions25k = [x[0] for x in csv.reader(file)]
        with open(pathCsvExceptions50k, 'r') as file:
            exceptions50k = [x[0] for x in csv.reader(file)]
        return set((*exceptions25k, *exceptions50k))

    @staticmethod
    def checkLeftPaddingMI(mi):
        leftPart = mi.split('-')[0]
        if len(leftPart) < 4:
            return f'{"".join("0" for _ in range(4-len(leftPart)))}{mi}'
        return mi

if __name__ == "__main__":
    x = UtmGrid()
    print(x.get_INOM_range_from_min_max_inom('SE-17','NC-22'))
    print(x.get_INOM_range_from_min_max_inom('SC-17','SA-22'))
    print(x.get_INOM_range_from_BB(-83, -19, -49, 9))
    print(x.get_INOM_range_from_min_max_inom('SE-17','NC-22') == x.get_INOM_range_from_BB(-83, -19, -49, 9) )
    print(x.get_MI_MIR_from_inom('NB-20-Z-D-I-1'))
