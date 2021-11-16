# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-11
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Eliton / Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : eliton.filho / @eb.mil.br
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

from qgis.PyQt.QtCore import (QCoreApplication, QVariant)
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsFeature,
                       QgsField,
                       QgsProcessingFeatureSourceDefinition,
                       QgsFeatureRequest
                       )
from qgis import processing

from .validationAlgorithm import ValidationAlgorithm


class VerifyCountourStackingAlgorihtm(ValidationAlgorithm):

    INPUT_CONTOUR_LINES = 'INPUT_CONTOUR_LINES'
    INPUT_LEVES_FIELD = 'INPUT_LEVES_FIELD'
    INPUT_IS_DEPRESSION_FIELD = 'INPUT_IS_DEPRESSION_FIELD'
    INPUT_LEVEL_GAP = 'INPUT_LEVEL_GAP'
    OUTPUT = 'OUTPUT'
    OUTPUT_NEW_LAYER = 'OUTPUT_NEW_LAYER'
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                'INPUT_COUNTOUR_LINES',
                self.tr('Select'),
                types=[QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                'INPUT_LEVES_FIELD',
                self.tr('Contour levels layer'), 
                type=QgsProcessingParameterField.Numeric, 
                parentLayerParameterName='INPUT_COUNTOUR_LINES', 
                allowMultiple=False, 
                defaultValue='cota')
            )
        self.addParameter(
            QgsProcessingParameterField(
                'INPUT_IS_DEPRESSION_FIELD',
                self.tr('Attribute information about "depression"'), 
                type=QgsProcessingParameterField.Numeric, 
                parentLayerParameterName='INPUT_COUNTOUR_LINES', 
                allowMultiple=False, 
                defaultValue='depressao')
            )
        self.addParameter(
            QgsProcessingParameterNumber(
                'INPUT_LEVEL_GAP',
                self.tr('Equidistance value'), 
                type=QgsProcessingParameterNumber.Double, 
                minValue=0)
            )
        
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Flags')
            )
        ) 

    def processAlgorithm(self, parameters, context, feedback):
        countourLayer = self.parameterAsVectorLayer( parameters,'INPUT_COUNTOUR_LINES', context )
        levelsField = self.parameterAsFields( parameters,'INPUT_LEVES_FIELD', context )[0]
        levelGap = self.parameterAsDouble (parameters,'INPUT_LEVEL_GAP', context)
        isDepressionField = self.parameterAsFields (parameters,'INPUT_IS_DEPRESSION_FIELD', context)[0]
        feedback.setProgressText('Verificando inconsistencias ')
        step =1
        progressStep = 100/4
        countourLayerPolyHoles = self.lineToPolygons(countourLayer,context, feedback)
        step +=1
        feedback.setProgress( step * progressStep )
        countourLayerPoly = self.fillHoles(countourLayerPolyHoles, context, feedback)
        step +=1
        feedback.setProgress( step * progressStep )
        outputPolygons = []
        self.fillField(countourLayer, countourLayerPoly)
        step +=1
        feedback.setProgress( step * progressStep )
        self.compareLevel(levelsField, levelGap, isDepressionField, countourLayerPoly, outputPolygons, feedback, step, progressStep)
        if outputPolygons:
            newLayer = self.outLayer(parameters, context, outputPolygons, countourLayer)
        else: 
            newLayer = self.tr('No flags')
        return {self.OUTPUT: newLayer}

    def lineToPolygons(self, layer,context, feedback):
        r = processing.run(
            'native:polygonize',
            {   'INPUT' : QgsProcessingFeatureSourceDefinition(
                    layer.source()
                ), 
                'KEEP_FIELDS' : True,
                'OUTPUT' : 'TEMPORARY_OUTPUT'
            },
            context = context,
            feedback = feedback
        )
        return r['OUTPUT']  
    def createFeaturesArray(self, originalLayer):
        arrayFeatures = []
        features = originalLayer.getFeatures()

        for feature in features:
            arrayFeatures.append(feature)

        return arrayFeatures
        
    def fillHoles(self, layer, context, feedback):
        r = processing.run(
            'native:deleteholes',
            {   'INPUT' : layer,
                'OUTPUT' : 'TEMPORARY_OUTPUT'
            },
            context = context,
            feedback = feedback
        )
        return r['OUTPUT']  
    def fillField(self, countourLayer, countourLayerPoly):
        countourLayerPoly.startEditing()
        pr = countourLayerPoly.dataProvider()
        updateMap = {}
        for feature1 in pr.getFeatures():
            AreaOfInterest = feature1.geometry().boundingBox()
            request = QgsFeatureRequest().setFilterRect(AreaOfInterest)
            for feature2 in countourLayer.getFeatures(request):
                if feature2.geometry().touches(feature1.geometry()):
                    fv = {}
                    for field in feature2.fields():
                        fieldIdx = pr.fields().indexFromName( field.name())
                        fv[fieldIdx] = feature2[field.name()]
                        
                        feature1[field.name()] =  feature2[field.name()]
                    updateMap[feature1.id()] = fv
        pr.changeAttributeValues( updateMap )
        countourLayerPoly.commitChanges()
        return False
    def compareLevel(self, levelsField, levelGap, isDepressionField, countourLayerPoly, outputPolygons, feedback, step, progressStep):
        isDep = 1
        isNotDep = 0  
        auxstep = 0
        AUXCOUNT = 0
        auxProgressStep = countourLayerPoly.featureCount()
        for feature1 in countourLayerPoly.getFeatures():
            AUXCOUNT += 1
            auxcount=0
            auxstep+=1
            feedback.setProgress( step*(1+(auxstep/auxProgressStep)) * progressStep )
            toCompare = []
            areaComp = []
            skip = True
            AreaOfInterest = feature1.geometry().boundingBox()
            request = QgsFeatureRequest().setFilterRect(AreaOfInterest)
            for feature2 in countourLayerPoly.getFeatures(request):
                auxcount+=1
                if str(feature1.geometry())==str(feature2.geometry()):
                    continue
                if feature1.geometry().within(feature2.geometry()):
                    toCompare.append(feature2)
                    areaComp.append(feature2.geometry().area())
                    skip = False
            if skip:
                continue
            fToCompare = toCompare[areaComp.index(min(areaComp))]                
            if fToCompare[isDepressionField] == isNotDep:
                if feature1[isDepressionField] == isNotDep:
                    if not((feature1[levelsField] - fToCompare[levelsField])==levelGap):
                        outputPolygons.append([feature1, 1])
                if feature1[isDepressionField] == isDep:
                    if not(feature1[levelsField] == fToCompare[levelsField]):
                        outputPolygons.append([feature1, 3])
            if fToCompare[isDepressionField] == isDep:
                if feature1[isDepressionField] == isDep:
                    if not((fToCompare[levelsField] - feature1[levelsField])==levelGap):
                        outputPolygons.append([feature1, 2])
                if feature1[isDepressionField] == isNotDep:
                    if not(feature1[levelsField] == fToCompare[levelsField]):
                        outputPolygons.append([feature1, 4])
        return False
    def outLayer(self, parameters, context, polygons, streamLayer):
        newFields = polygons[0][0].fields()
        newFields.append(QgsField('erro', QVariant.String))
        
        (sink, newLayer) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            newFields,
            3, #polygon
            streamLayer.sourceCrs()
        )
        dicterro = {
            1: self.tr('Extern and intern are normal, but elevation differences are not greater than one equidistance'),
            2: self.tr('Extern and intern are depressions, but elevation differences are not smaller than one equidistance'),
            3: self.tr('Extern is normal, intern is depression, but elevations are different'),
            4: self.tr('Extern is depression, intern is normal, but elevations are different')
        }
        for polygon in polygons:
            newFeat = QgsFeature()
            newFeat.setGeometry(polygon[0].geometry())
            newFeat.setFields(newFields)
            for field in  range(len(polygon[0].fields())):
                newFeat.setAttribute((field), polygon[0].attribute((field)))
            newFeat['erro'] = dicterro[polygon[1]]
            sink.addFeature(newFeat, QgsFeatureSink.FastInsert)
        
        return newLayer

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'verifycountourstacking'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Verifies the stacking of contour lines')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('VerifyCountourStackingAlgorihtm', string)

    def createInstance(self):
        return VerifyCountourStackingAlgorihtm()
