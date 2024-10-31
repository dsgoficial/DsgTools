# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-10-29
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jaime Guilherme - Cartographic Engineer @ Brazilian Army
        email                : jaime.breda@ime.eb.br
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




from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.core import (
    QgsProcessingMultiStepFeedback,
    QgsVectorLayer,
)
from qgis.PyQt.Qt import QObject


class GeneralizeUtils(QObject):
    def __init__(self):
        super(GeneralizeUtils, self).__init__()
        self.algRunner = AlgRunner()

    def runStrangle(
        self, layer:QgsVectorLayer, context, length_tol, area_tol, feedback=None
    ):
        """
        Gets the features from lyr acording to parameters.
        :param (QgsVectorLayer) lyr: layer;
        :param length_tol: number;
        :param area_tol: number;
        """
        steps = 12
        currentStep = 0
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(steps, feedback)
            multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying dissolve."))
        dissolve = self.algRunner.runDissolve(layer,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Applying negative buffer to remove thin parts."))
        buffer_neg = self.algRunner.runBuffer(dissolve,
            distance=-length_tol / 2.0,
            context=context,
            dissolve=True,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        multitosingle = self.algRunner.runMultipartToSingleParts(buffer_neg,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Removing null geometries."))
        removenull = self.algRunner.runRemoveNull(multitosingle,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Applying positive buffer."))
        buffer_pos = self.algRunner.runBuffer(removenull,
            distance=length_tol / 2.0,
            context=context,
            dissolve=True,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Applying negative buffer to remove thin parts."))

        # single part pois resultado do buffer dissolvido é sempre multipart (pior para spatialIndex)
        final_buffer_pos = self.algRunner.runMultipartToSingleParts(buffer_pos,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Obtaining empty spaces."))
        empty_space = self.algRunner.runDifference(
            inputLyr=layer,
            overlayLyr=final_buffer_pos,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        
        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        new_multitosingle = self.algRunner.runMultipartToSingleParts(empty_space,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        
        filtered_empty_space = self.algRunner.runFilterExpression(
            inputLyr=new_multitosingle,
            expression=f"""area($geometry) >= {area_tol} """,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        
        filtered_buffer = self.algRunner.runDifference(
            inputLyr=layer,
            overlayLyr=filtered_empty_space,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if feedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)

        multiStepFeedback.setProgressText(self.tr("Transforming multipart geometries into singlepart."))
        output = self.algRunner.runMultipartToSingleParts(filtered_buffer,
            context=context,
            feedback=multiStepFeedback
        )

        return output