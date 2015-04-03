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
from qgis.core import QgsPoint, QgsGeometry, QgsFeature
import string, os

class UtmGrid:
    def __init__(self):
        """Constructor."""
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
        """Get X spacing fot the given scale
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
        """Get Y spacing fot the given scale
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

        point = QgsPoint(xmin, ymin)
        polyline.append(point)
        point = QgsPoint(xmin+dx, ymin)
        polyline.append(point)
        point = QgsPoint(xmax-dx, ymin) 
        polyline.append(point)
        point = QgsPoint(xmax, ymin)
        polyline.append(point)
        point = QgsPoint(xmax, ymin+dy)
        polyline.append(point)
        point = QgsPoint(xmax, ymax-dy)
        polyline.append(point)
        point = QgsPoint(xmax, ymax)
        polyline.append(point)
        point = QgsPoint(xmax-dx, ymax)
        polyline.append(point)
        point = QgsPoint(xmin+dx, ymax)
        polyline.append(point)
        point = QgsPoint(xmin, ymax)
        polyline.append(point)
        point = QgsPoint(xmin, ymax-dy)
        polyline.append(point)
        point = QgsPoint(xmin, ymin+dy)
        polyline.append(point)
        point = QgsPoint(xmin, ymin)
        polyline.append(point)

        qgsPolygon = QgsGeometry.fromMultiPolygon([[polyline]])
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
        l=inomen[1].upper()
        y = 0.0;
        operator=self.getHemisphereMultiplier(inomen)
        verticalPosition=string.uppercase.index(l)
        y=(y+4*verticalPosition)*operator
        if (operator<0): y-=4
        return y

    def getLLCornerLongitude1kk(self,inomen):
        """Get lower left Longitude for 1:1.000.000 scale
        """
        fuso=int(inomen[3:5])
        x=0  
        if((fuso > 0) and (fuso <= 60)):
            x = (((fuso - 30)*6.0)-6.0)
        return x
    
    def getLLCorner(self,inomen):
        """Get lower left coordinates for scale determined by the given map index
        """
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
            print "Total:",self.stepsTotal
            self.stepsDone=0
        if scale == stopScale:
            (x, y) = self.getLLCorner(iNomen)
            dx = self.getSpacingX(stopScale)
            dy = self.getSpacingY(stopScale)
            poly = self.makeQgsPolygon(x, y, x + dx, y + dy)
            
            self.insertFrameIntoQgsLayer(layer, poly, iNomen)
            
            self.stepsDone+=1
            print self.stepsDone, '/', self.stepsTotal
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
        l1 = map(lambda x: (x.strip()).split(';'),data)
        dicionario = dict((a[1].lstrip('0'),a[0]) for a in l1)
        return dicionario

    def getINomenFromMI(self,mi):
        return self.getINomen(self.getMIdict(), mi)

    def getINomenFromMIR(self,mir):
        return self.getINomen(self.getMIRdict(), mir)
        
    def getINomen(self, dict, index):
        key = index.split('-')[0]
        otherParts = index.split('-')[1:]
        if (dict.has_key(key)):
            return dict[key]+'-'+string.join(otherParts,'-')
        else:
            return ''
        
if (__name__=="__main__"):
    test=UtmGrid()
    mi="2895-1"
    inomen=test.getINomenFromMI(mi)
    print 'Working test:',inomen,'.'
    mi='teste'
    inomen=test.getINomenFromMI(mi)
    print 'Not working test:',inomen,'.'
    #print test.getQgsPolygonFrame(inomen).exportToWkt()
    
