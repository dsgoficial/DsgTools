# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2025-07-17
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

import json
import numpy as np
import os
import shutil
import traceback
from osgeo import gdal, osr
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterFile,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterBoolean,
    QgsProcessingException,
    QgsRasterLayer,
    QgsMessageLog,
    Qgis
)

class RasterRemapAlgorithm(QgsProcessingAlgorithm):
    INPUT_RASTER = 'INPUT_RASTER'
    MAPPING_FILE = 'MAPPING_FILE'
    OUTPUT_RASTER = 'OUTPUT_RASTER'
    FORCE_CHUNKED = 'FORCE_CHUNKED'

    def createInstance(self):
        return RasterRemapAlgorithm()

    def tr(self, string):
        return QCoreApplication.translate("RasterRemapAlgorithm", string)

    def name(self):
        return "rasterremapalgorithm"

    def displayName(self):
        return self.tr("Remap raster values from json")

    def group(self):
        return self.tr("Raster Handling")

    def groupId(self):
        return "DSGTools - Raster Handling"

    def shortHelpString(self):
        return self.tr(
            "Remaps raster values using a JSON mapping file.\n"
            "OPTIMIZED WITH ADAPTIVE SPLITTING FOR LARGE RASTERS.\n"
            "\n"
            "Parameters:\n"
            "- Input Raster: The input raster\n"
            "- Mapping File: JSON file with value mapping\n"
            "- Output Raster: The remapped output raster\n"
            "- Force Chunked Processing: Force chunked processing (default: No)\n"
            "\n"
            "PROCESSING STRATEGY:\n"
            "\n"
            "The algorithm attempts to process the entire raster at once for maximum\n"
            "performance with NumPy. If a memory error occurs, it automatically splits:\n"
            "\n"
            "1st attempt: Process everything (1x1 = 1 block)\n"
            "2nd attempt: Split into 2x2 (4 blocks)\n"
            "3rd attempt: Split into 4x4 (16 blocks)\n"
            "4th attempt: Split into 8x8 (64 blocks)\n"
            "... and so on until successful\n"
            "\n"
            "This maximizes efficient NumPy usage and minimizes Python loops.\n"
            "\n"
            "JSON FILE FORMAT:\n"
            "\n"
            "{\n"
            '  "description": "Mapping description",\n'
            '  "nodata_value": -9999,\n'
            '  "mapping": {\n'
            '    "0": -9999,\n'
            '    "3": 601,\n'
            '    "15": 901\n'
            "  }\n"
            "}\n"
            "\n"
            "REQUIRED FIELDS:\n"
            "- mapping: Object with \"source_value\": target_value pairs\n"
            "- nodata_value: Value for nodata pixels"
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input Raster'),
                [QgsProcessing.TypeRaster]
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.MAPPING_FILE,
                self.tr('Mapping JSON File'),
                extension='json'
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output Raster')
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FORCE_CHUNKED,
                self.tr('Force Chunked Processing'),
                defaultValue=False,
                optional=True
            )
        )

    def loadMapping(self, mappingFile, feedback):
        """Loads and validates the JSON mapping file."""
        try:
            with open(mappingFile, 'r', encoding='utf-8') as f:
                mappingData = json.load(f)

            if 'mapping' not in mappingData:
                raise QgsProcessingException(
                    self.tr('JSON file must contain the "mapping" field.')
                )

            mapping = mappingData['mapping']
            nodataValue = mappingData.get('nodata_value', -9999)

            if not mapping:
                raise QgsProcessingException(
                    self.tr('The "mapping" field cannot be empty.')
                )

            # Convert to numeric types
            mappingNumeric = {}
            invalidMappings = []

            for key, value in mapping.items():
                try:
                    inputVal = int(key)
                    outputVal = int(value)
                    mappingNumeric[inputVal] = outputVal
                except ValueError:
                    invalidMappings.append('%s -> %s' % (key, value))

            if invalidMappings:
                feedback.pushWarning(
                    self.tr('Invalid values ignored: %s') % ', '.join(invalidMappings)
                )

            if not mappingNumeric:
                raise QgsProcessingException(
                    self.tr('No valid mapping found.')
                )

            feedback.pushInfo(
                self.tr('Mapping loaded: %s classes') % len(mappingNumeric)
            )
            feedback.pushInfo(
                self.tr('NoData value: %s') % nodataValue
            )

            return mappingNumeric, nodataValue

        except json.JSONDecodeError as e:
            raise QgsProcessingException(
                self.tr('Error decoding JSON: %s') % str(e)
            )
        except FileNotFoundError:
            raise QgsProcessingException(
                self.tr('File not found: %s') % mappingFile
            )
        except Exception as e:
            raise QgsProcessingException(
                self.tr('Error loading JSON: %s') % str(e)
            )

    def determineOutputDtype(self, mappingNumeric, nodataValue):
        """Determines the optimal data type for the output raster."""
        mappedValues = list(mappingNumeric.values())
        minVal = min(mappedValues + [nodataValue])
        maxVal = max(mappedValues + [nodataValue])

        if minVal >= -128 and maxVal <= 127:
            outputDtype = gdal.GDT_Byte if minVal >= 0 else gdal.GDT_Int16
            numpyDtype = np.uint8 if minVal >= 0 else np.int16
        elif minVal >= -32768 and maxVal <= 32767:
            outputDtype = gdal.GDT_Int16
            numpyDtype = np.int16
        elif minVal >= 0 and maxVal <= 65535:
            outputDtype = gdal.GDT_UInt16
            numpyDtype = np.uint16
        elif minVal >= -2147483648 and maxVal <= 2147483647:
            outputDtype = gdal.GDT_Int32
            numpyDtype = np.int32
        else:
            outputDtype = gdal.GDT_Float32
            numpyDtype = np.float32

        return outputDtype, numpyDtype

    def remapArray(self, inputArray, mappingNumeric, nodataValue, inputNodata, numpyDtype):
        """Applies remapping on a NumPy array."""
        outputArray = np.full(inputArray.shape, nodataValue, dtype=numpyDtype)

        # Apply mapping - NumPy vectorized operation
        for inputVal, outputVal in mappingNumeric.items():
            mask = inputArray == inputVal
            outputArray[mask] = outputVal

        # Handle input nodata values
        if inputNodata is not None:
            outputArray[inputArray == inputNodata] = nodataValue

        return outputArray

    def processBandWhole(self, inputBand, outputBand, mappingNumeric,
                         nodataValue, inputNodata, numpyDtype, feedback):
        """Attempts to process the entire band at once."""
        try:
            feedback.pushInfo(self.tr('Attempting to process entire band...'))

            # Read full array
            inputArray = inputBand.ReadAsArray()

            if inputArray is None:
                raise MemoryError(self.tr('Failed to read array'))

            # Apply remapping
            outputArray = self.remapArray(
                inputArray, mappingNumeric, nodataValue,
                inputNodata, numpyDtype
            )

            # Write result
            outputBand.WriteArray(outputArray)
            outputBand.SetNoDataValue(nodataValue)
            outputBand.FlushCache()

            feedback.pushInfo(self.tr('Band processed successfully (full mode)'))
            return True

        except (MemoryError, Exception) as e:
            feedback.pushInfo(
                self.tr('Could not process entire band: %s') % str(e)
            )
            return False

    def processBandChunked(self, inputBand, outputBand, cols, rows,
                           mappingNumeric, nodataValue, inputNodata,
                           numpyDtype, feedback):
        """Processes the band in chunks with adaptive splitting."""

        # Start with 2x2 split
        divisions = 2
        maxDivisions = 64  # Maximum limit to avoid very small chunks

        while divisions <= maxDivisions:
            try:
                feedback.pushInfo(
                    self.tr('Attempting to process in %sx%s chunks...') % (divisions, divisions)
                )

                # Calculate chunk size
                chunkRows = rows // divisions
                chunkCols = cols // divisions

                # Calculate estimated size in GB
                estimatedSizeGb = (chunkRows * chunkCols * np.dtype(numpyDtype).itemsize) / (1024**3)
                feedback.pushInfo(
                    self.tr('Estimated size per chunk: %.2f GB') % estimatedSizeGb
                )

                totalChunks = divisions * divisions
                currentChunk = 0

                # Process each chunk
                for i in range(divisions):
                    if feedback.isCanceled():
                        return False

                    # Calculate Y bounds
                    yStart = i * chunkRows
                    if i == divisions - 1:
                        yEnd = rows
                    else:
                        yEnd = (i + 1) * chunkRows
                    ySize = yEnd - yStart

                    for j in range(divisions):
                        if feedback.isCanceled():
                            return False

                        # Calculate X bounds
                        xStart = j * chunkCols
                        if j == divisions - 1:
                            xEnd = cols
                        else:
                            xEnd = (j + 1) * chunkCols
                        xSize = xEnd - xStart

                        # Read chunk
                        inputChunk = inputBand.ReadAsArray(xStart, yStart, xSize, ySize)

                        if inputChunk is None:
                            raise MemoryError(
                                self.tr('Failed to read chunk (%s,%s)') % (i, j)
                            )

                        # Apply remapping
                        outputChunk = self.remapArray(
                            inputChunk, mappingNumeric, nodataValue,
                            inputNodata, numpyDtype
                        )

                        # Write chunk
                        outputBand.WriteArray(outputChunk, xStart, yStart)

                        # Update progress
                        currentChunk += 1
                        progress = int((currentChunk / totalChunks) * 100)
                        feedback.setProgress(progress)

                        if currentChunk % max(1, totalChunks // 10) == 0:
                            feedback.pushInfo(
                                self.tr('Progress: %s/%s chunks (%s%%)') % (
                                    currentChunk, totalChunks, progress
                                )
                            )

                outputBand.SetNoDataValue(nodataValue)
                outputBand.FlushCache()

                feedback.pushInfo(
                    self.tr('Band processed successfully in %sx%s chunks '
                            '(total: %s chunks)') % (divisions, divisions, totalChunks)
                )
                return True

            except (MemoryError, Exception) as e:
                feedback.pushWarning(
                    self.tr('Failed with %sx%s chunks: %s') % (divisions, divisions, str(e))
                )
                # Double the number of divisions
                divisions *= 2
                continue

        raise QgsProcessingException(
            self.tr('Could not process even with %sx%s chunks. '
                    'Raster too large or insufficient memory.') % (maxDivisions, maxDivisions)
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Configure GDAL to report errors
        gdal.UseExceptions()

        try:
            # Get parameters
            inputRaster = self.parameterAsRasterLayer(parameters, self.INPUT_RASTER, context)
            mappingFile = self.parameterAsString(parameters, self.MAPPING_FILE, context)
            outputPath = self.parameterAsOutputLayer(parameters, self.OUTPUT_RASTER, context)
            forceChunked = self.parameterAsBool(parameters, self.FORCE_CHUNKED, context)

            # Validate output path
            if not outputPath:
                raise QgsProcessingException(
                    self.tr('Output path not specified')
                )

            # Warn if using network path
            if outputPath.startswith('\\\\') or outputPath.startswith('//'):
                feedback.pushWarning(
                    self.tr('WARNING: Network path detected for output file.\n'
                            'Processing may be slower. Consider using a local disk.')
                )

            if not inputRaster or not inputRaster.isValid():
                raise QgsProcessingException(
                    self.tr('Invalid input raster')
                )

            # Load mapping
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('LOADING MAPPING'))
            feedback.pushInfo('=' * 60)
            mappingNumeric, nodataValue = self.loadMapping(mappingFile, feedback)

            # Open raster
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('OPENING RASTER'))
            feedback.pushInfo('=' * 60)
            inputPath = inputRaster.source()
            feedback.pushInfo(self.tr('Path: %s') % inputPath)

            try:
                dataset = gdal.Open(inputPath, gdal.GA_ReadOnly)

                if dataset is None:
                    gdalError = gdal.GetLastErrorMsg()
                    raise QgsProcessingException(
                        self.tr('Could not open the input raster.\n'
                                'GDAL error: %s\n'
                                'Path: %s') % (gdalError, inputPath)
                    )

                feedback.pushInfo(self.tr('Raster opened successfully'))

            except Exception as e:
                raise QgsProcessingException(
                    self.tr('Error opening raster: %s\n'
                            'Path: %s') % (str(e), inputPath)
                )

            # Get raster information
            cols = dataset.RasterXSize
            rows = dataset.RasterYSize
            bands = dataset.RasterCount
            geotransform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()

            feedback.pushInfo(
                self.tr('Dimensions: %s x %s pixels') % ('{:,}'.format(cols), '{:,}'.format(rows))
            )
            feedback.pushInfo(self.tr('Bands: %s') % bands)

            # Calculate estimated size
            inputBand = dataset.GetRasterBand(1)
            inputNodata = inputBand.GetNoDataValue()
            inputDtype = gdal.GetDataTypeName(inputBand.DataType)

            sizeGb = (cols * rows * inputBand.DataType) / (1024**3)
            feedback.pushInfo(self.tr('Estimated size: %.2f GB') % sizeGb)
            feedback.pushInfo(self.tr('Input data type: %s') % inputDtype)

            # Determine output type
            outputDtype, numpyDtype = self.determineOutputDtype(
                mappingNumeric, nodataValue
            )
            feedback.pushInfo(
                self.tr('Output data type: %s') % gdal.GetDataTypeName(outputDtype)
            )

            # Create output raster
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('CREATING OUTPUT RASTER'))
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('Output path: %s') % outputPath)

            # Validate output directory
            outputDir = os.path.dirname(outputPath)
            if not outputDir:
                outputDir = '.'

            feedback.pushInfo(self.tr('Output directory: %s') % outputDir)

            if not os.path.exists(outputDir):
                try:
                    os.makedirs(outputDir, exist_ok=True)
                    feedback.pushInfo(self.tr('Directory created: %s') % outputDir)
                except Exception as e:
                    raise QgsProcessingException(
                        self.tr('Could not create output directory:\n'
                                '%s\n'
                                'Error: %s') % (outputDir, str(e))
                    )
            else:
                feedback.pushInfo(self.tr('Directory exists: %s') % outputDir)

            # Test write permission
            testFile = os.path.join(outputDir, '.test_write_permission')
            try:
                with open(testFile, 'w') as f:
                    f.write('test')
                os.remove(testFile)
                feedback.pushInfo(self.tr('Write permission verified'))
            except Exception as e:
                raise QgsProcessingException(
                    self.tr('No write permission in directory:\n'
                            '%s\n'
                            'Error: %s') % (outputDir, str(e))
                )

            # Check available disk space (Windows)
            try:
                import shutil
                total, used, free = shutil.disk_usage(outputDir)
                availableGb = free / (1024**3)
                requiredGb = sizeGb * 1.5  # Add 50% margin

                feedback.pushInfo(
                    self.tr('Available space: %.1f GB') % availableGb
                )
                feedback.pushInfo(
                    self.tr('Required space (estimated): %.1f GB') % requiredGb
                )

                if availableGb < requiredGb:
                    raise QgsProcessingException(
                        self.tr('INSUFFICIENT DISK SPACE!\n'
                                'Available: %.1f GB\n'
                                'Required: %.1f GB\n'
                                'Free up disk space or choose another location.') % (
                            availableGb, requiredGb
                        )
                    )
                else:
                    feedback.pushInfo(self.tr('Sufficient disk space'))

            except QgsProcessingException:
                raise
            except Exception as e:
                feedback.pushWarning(
                    self.tr('Could not check disk space: %s') % str(e)
                )

            # Check if file already exists
            if os.path.exists(outputPath):
                feedback.pushWarning(
                    self.tr('File already exists and will be overwritten: %s') % outputPath
                )
                try:
                    os.remove(outputPath)
                    feedback.pushInfo(self.tr('Previous file removed'))
                except Exception as e:
                    raise QgsProcessingException(
                        self.tr('Could not remove existing file:\n'
                                '%s\n'
                                'Error: %s\n'
                                'The file may be in use by another program.') % (
                            outputPath, str(e)
                        )
                    )

            try:
                feedback.pushInfo(self.tr('Getting GTiff driver...'))
                driver = gdal.GetDriverByName('GTiff')
                if driver is None:
                    raise QgsProcessingException(
                        self.tr('GTiff driver not available in GDAL')
                    )

                feedback.pushInfo(self.tr('GTiff driver obtained'))

                # Prepare creation options
                createOptions = ['COMPRESS=LZW', 'TILED=YES', 'BIGTIFF=YES']
                feedback.pushInfo(
                    self.tr('Creation options: %s') % ', '.join(createOptions)
                )

                # Log parameters
                feedback.pushInfo(self.tr('Creation parameters:'))
                feedback.pushInfo(self.tr('  - Columns: %s') % '{:,}'.format(cols))
                feedback.pushInfo(self.tr('  - Rows: %s') % '{:,}'.format(rows))
                feedback.pushInfo(self.tr('  - Bands: %s') % bands)
                feedback.pushInfo(
                    self.tr('  - Type: %s') % gdal.GetDataTypeName(outputDtype)
                )

                feedback.pushInfo(self.tr('Creating GDAL dataset...'))

                outputDataset = driver.Create(
                    outputPath,
                    cols,
                    rows,
                    bands,
                    outputDtype,
                    options=createOptions
                )

                feedback.pushInfo(self.tr('Create() call completed'))

                if outputDataset is None:
                    # Capture GDAL error
                    gdalError = gdal.GetLastErrorMsg()
                    gdalErrorNum = gdal.GetLastErrorNo()
                    gdalErrorType = gdal.GetLastErrorType()

                    errorDetails = self.tr(
                        'Could not create the output raster.\n'
                        'Path: %s\n'
                        'GDAL Error Number: %s\n'
                        'GDAL Error Type: %s\n'
                        'GDAL Error Message: %s\n\n'
                        'Possible causes:\n'
                        '- Invalid or too long path\n'
                        '- Special characters in file name\n'
                        '- Inaccessible network drive\n'
                        '- GTiff driver issue\n'
                        '- File/process blocked by antivirus'
                    ) % (outputPath, gdalErrorNum, gdalErrorType, gdalError)
                    raise QgsProcessingException(errorDetails)

                feedback.pushInfo(self.tr('Output file created'))

                outputDataset.SetGeoTransform(geotransform)
                outputDataset.SetProjection(projection)
                feedback.pushInfo(self.tr('Georeferencing configured'))

                # Validate that we can access the bands
                for b in range(1, bands + 1):
                    band = outputDataset.GetRasterBand(b)
                    if band is None:
                        raise QgsProcessingException(
                            self.tr('Could not create band %s in the output raster') % b
                        )
                feedback.pushInfo(
                    self.tr('%s band(s) created successfully') % bands
                )

                # Try initial flush to detect I/O errors
                try:
                    outputDataset.FlushCache()
                    feedback.pushInfo(self.tr('Disk write validation OK'))
                except Exception as flushError:
                    raise QgsProcessingException(
                        self.tr('Error writing to disk: %s\n'
                                'Possible causes:\n'
                                '- Insufficient disk space\n'
                                '- Write permissions\n'
                                '- Network path issues') % str(flushError)
                    )

            except Exception as e:
                # Try to clean up partial file
                try:
                    if outputDataset is not None:
                        outputDataset = None
                    if os.path.exists(outputPath):
                        os.remove(outputPath)
                        feedback.pushInfo(self.tr('Partial file removed'))
                except:
                    pass

                # Re-raise with more context
                errorType = type(e).__name__
                errorMsg = str(e)
                gdalError = gdal.GetLastErrorMsg()

                fullError = self.tr('Error creating output raster:\n'
                                    'Type: %s\n'
                                    'Message: %s\n') % (errorType, errorMsg)
                if gdalError:
                    fullError += 'GDAL: %s\n' % gdalError
                fullError += self.tr('Path: %s\n') % outputPath

                feedback.reportError(fullError)

                raise QgsProcessingException(fullError)

            # Process each band
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('PROCESSING BANDS'))
            feedback.pushInfo('=' * 60)

            for bandIdx in range(1, bands + 1):
                feedback.pushInfo(
                    self.tr('\nBand %s/%s') % (bandIdx, bands)
                )
                feedback.pushInfo('-' * 60)

                if feedback.isCanceled():
                    break

                inputBand = dataset.GetRasterBand(bandIdx)
                outputBand = outputDataset.GetRasterBand(bandIdx)

                # Decide processing strategy
                if forceChunked:
                    feedback.pushInfo(self.tr('Chunked mode forced by user'))
                    success = self.processBandChunked(
                        inputBand, outputBand, cols, rows,
                        mappingNumeric, nodataValue, inputNodata,
                        numpyDtype, feedback
                    )
                else:
                    # Try full mode first
                    success = self.processBandWhole(
                        inputBand, outputBand, mappingNumeric,
                        nodataValue, inputNodata, numpyDtype, feedback
                    )

                    # If it fails, use chunked mode
                    if not success:
                        feedback.pushInfo(self.tr('Switching to chunked mode...'))
                        success = self.processBandChunked(
                            inputBand, outputBand, cols, rows,
                            mappingNumeric, nodataValue, inputNodata,
                            numpyDtype, feedback
                        )

                if not success:
                    raise QgsProcessingException(
                        self.tr('Failed to process band %s') % bandIdx
                    )

            # Close datasets and ensure final flush
            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('FINALIZING'))
            feedback.pushInfo('=' * 60)

            try:
                # Force flush all bands
                for bandIdx in range(1, bands + 1):
                    band = outputDataset.GetRasterBand(bandIdx)
                    if band:
                        band.FlushCache()

                outputDataset.FlushCache()
                feedback.pushInfo(self.tr('Data written to disk'))

                # Close datasets
                dataset = None
                outputDataset = None
                feedback.pushInfo(self.tr('Files closed'))

                # Verify that file was created
                if not os.path.exists(outputPath):
                    raise QgsProcessingException(
                        self.tr('Output file was not created. Check permissions and disk space.')
                    )

                fileSizeGb = os.path.getsize(outputPath) / (1024**3)
                feedback.pushInfo(
                    self.tr('File created: %.2f GB') % fileSizeGb
                )

            except Exception as e:
                raise QgsProcessingException(
                    self.tr('Error finalizing file: %s') % str(e)
                )

            feedback.pushInfo('=' * 60)
            feedback.pushInfo(self.tr('COMPLETED SUCCESSFULLY!'))
            feedback.pushInfo(self.tr('File saved: %s') % outputPath)
            feedback.pushInfo('=' * 60)

            return {self.OUTPUT_RASTER: outputPath}

        except QgsProcessingException:
            # Re-raise QgsProcessingException without modifying
            raise
        except MemoryError as e:
            errorMsg = self.tr(
                'MEMORY ERROR: %s\n\n'
                'The raster is too large to process.\n'
                'Solutions:\n'
                '1. Check the "Force Chunked Processing" option\n'
                '2. Close other programs to free memory\n'
                '3. Process on a machine with more RAM'
            ) % str(e)
            feedback.reportError(errorMsg)
            raise QgsProcessingException(errorMsg)
        except Exception as e:
            errorType = type(e).__name__
            errorMsg = self.tr('UNEXPECTED ERROR [%s]: %s') % (errorType, str(e))
            feedback.reportError(errorMsg)
            feedback.reportError('=' * 60)

            # Try to get more GDAL information
            try:
                gdalError = gdal.GetLastErrorMsg()
                gdalErrorNum = gdal.GetLastErrorNo()
                if gdalError:
                    feedback.reportError(
                        self.tr('GDAL Error #%s: %s') % (gdalErrorNum, gdalError)
                    )
            except:
                pass

            # Add traceback for debug
            tb = traceback.format_exc()
            feedback.reportError(self.tr('Full traceback:'))
            feedback.reportError(tb)
            feedback.reportError('=' * 60)

            raise QgsProcessingException('%s: %s' % (errorType, str(e)))
