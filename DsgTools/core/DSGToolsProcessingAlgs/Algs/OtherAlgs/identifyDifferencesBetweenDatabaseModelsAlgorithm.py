# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Matheus Alves Silva - Cartographic Engineer @ Brazilian Army
        email                : matheus.silva@ime.eb.br
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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFileDestination,
)
from processing.gui.wrappers import WidgetWrapper
from qgis.PyQt.QtWidgets import QLineEdit
from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from collections import defaultdict
import json


class IdentifyDifferencesBetweenDatabaseModelsAlgorithm(QgsProcessingAlgorithm):
    MASTERFILE = "MASTERFILE"
    SERVERIP = "SERVERIP"
    PORT = "PORT"
    DBNAME = "DBNAME"
    USER = "USER"
    PASSWORD = "PASSWORD"
    OUTPUT = "OUTPUT"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFile(
                self.MASTERFILE, self.tr("Path of Masterfile"), extension="json"
            )
        )

        self.addParameter(QgsProcessingParameterString(self.SERVERIP, self.tr("IP")))

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PORT,
                self.tr("Port"),
                minValue=0,
                maxValue=9999,
                defaultValue=5432,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(self.DBNAME, self.tr("Database Name"))
        )

        self.addParameter(
            QgsProcessingParameterString(self.USER, self.tr("Database User"))
        )

        password = QgsProcessingParameterString(
            self.PASSWORD,
            self.tr("Database Password"),
        )
        password.setMetadata(
            {
                "widget_wrapper": "DsgTools.core.DSGToolsProcessingAlgs.Algs.OtherAlgs.identifyDifferencesBetweenDatabaseModelsAlgorithm.MyWidgetWrapper"
            }
        )

        self.addParameter(password)

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr("Path to save .txt File"),
                fileFilter=".txt",
                createByDefault=True,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        masterFile = self.parameterAsFile(parameters, self.MASTERFILE, context)
        serverIp = self.parameterAsString(parameters, self.SERVERIP, context)
        port = self.parameterAsInt(parameters, self.PORT, context)
        dbName = self.parameterAsString(parameters, self.DBNAME, context)
        user = self.parameterAsString(parameters, self.USER, context)
        password = self.parameterAsString(parameters, self.PASSWORD, context)
        fileTxt = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        abstractDb = self.getAbstractDb(
            host=serverIp,
            port=port,
            database=dbName,
            user=user,
            password=password,
        )
        masterDict = self.getMasterDict(masterFile)
        msg = ""
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        msg += self.validateDatabaseVersionAndImplementation(masterDict, abstractDb)
        if multiStepFeedback.isCanceled():
            self.pushOutputMessage(feedback, msg)
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        msg += self.validateDomainTables(masterDict, abstractDb)
        if multiStepFeedback.isCanceled():
            self.pushOutputMessage(feedback, msg)
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        outputMsg, nameTableMsgDict = self.validateEDGVTables(masterDict, abstractDb)
        msg += outputMsg
        if multiStepFeedback.isCanceled():
            self.pushOutputMessage(feedback, msg)
            return {}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nameTableMsgDictTwo = self.validateCheckConstraint(masterDict, abstractDb)
        if multiStepFeedback.isCanceled():
            self.pushOutputMessage(feedback, msg)
            return {}

        nameTableMsgDict.update(nameTableMsgDictTwo)

        for table in nameTableMsgDict:
            msg += self.tr("Error in table = {0}: \n").format(table)
            for typeMsg in nameTableMsgDict[table]:
                if nameTableMsgDict[table][typeMsg] == []:
                    continue
                msg += f"   {typeMsg}\n"
                msg += f"   "
                for element in nameTableMsgDict[table][typeMsg]:
                    msg += f"\t- {element}\n"
                msg = msg[: len(msg) - 2] + "\n"
            msg += "\n"

        self.pushOutputMessage(feedback, msg, fileTxt)

        return {self.OUTPUT: fileTxt}

    def pushOutputMessage(self, feedback, msg, fileTxt):
        if msg == "":
            feedback.pushInfo(
                self.tr("The input database structure matches the structure defined by the input masterfile.")
            )
            with open(f"{fileTxt}", "w") as file:
                file.write(
                    self.tr("The input database structure matches the structure defined by the input masterfile.")
                )
        else:
            feedback.pushInfo(
                self.tr("The input database structure does not match the structure defined by the input masterfile:")
            )
            feedback.pushInfo(msg)
            with open(f"{fileTxt}", "w") as file:
                file.write(
                    self.tr("The input database structure does not match the structure defined by the input masterfile:\n")
                )
                file.write(f"{msg}")
        file.close()

    def getAbstractDb(self, host, port, database, user, password):
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(host, port, database, user, password)
        return abstractDb

    def getMasterDict(self, masterFile):
        """
        Read the masterfile
        """
        masterFile = open(masterFile)
        masterDict = json.load(masterFile)
        return masterDict

    def validateDatabaseVersionAndImplementation(self, masterDict, abstractDb):
        msg = ""
        (
            edgvVersion,
            implementationVersion,
        ) = abstractDb.getDatabaseAndImplementationVersions()
        if (
            edgvVersion != masterDict["modelo"]
            or implementationVersion != masterDict["versao"]
        ):
            msg += self.tr("Version error:\n")
        if edgvVersion != masterDict["modelo"]:
            msg += self.tr("   Database version ({0}) does not match masterfile version ({1})\n").format(edgvVersion, masterDict['modelo'])
        if implementationVersion != masterDict["versao"]:
            msg += self.tr("   Database implementation version ({0}) does not match masterfile implementation version ({1})\n").format(implementationVersion, masterDict['versao'])
        return msg

    def validateDomainTables(self, masterDict, abstractDb):
        """
        1. Validar schema do domínio
        2. Pegar conjunto de nome de domínios do masterDict;
        3. Pegar conjunto de nome de domínios do banco;
        4. Identificar domínios que existem no masterDict, mas não existem no banco (tabelas que faltam no banco);
        5. Identificar domínios que existem no banco, mas não estão previstas no masterDict (tabelas excedentes no banco);
        """
        msg = ""
        if not abstractDb.checkIfSchemaExistsInDatabase(masterDict["schema_dominios"]):
            msg += self.tr("Domain schema error:\n")
            msg += self.tr("   The domain schema {0} is not implemented in the database.").format(masterDict['schema_dominios'])
            return msg
        masterDictDomainNameSet = set(i["nome"] for i in masterDict["dominios"])
        dbDomainNameSet = abstractDb.getTableListFromSchema(
            masterDict["schema_dominios"]
        )

        inMasterDictNotInDbSet = masterDictDomainNameSet.difference(dbDomainNameSet)
        inDbNotInMasterDictSet = dbDomainNameSet.difference(masterDictDomainNameSet)

        if len(inMasterDictNotInDbSet) > 0 or len(inDbNotInMasterDictSet) > 0:
            msg += self.tr("Error, there is a discrepancy between database tables and Masterfile in the domains schema:\n")

        if len(inMasterDictNotInDbSet) > 0:
            msg += self.tr("    Domains that exist in the masterDict but not in the database (missing tables in the database) are: ")
            for e in inMasterDictNotInDbSet:
                msg += f"{e}, "
            msg = msg[: len(msg) - 2] + "\n\n"

        if len(inDbNotInMasterDictSet) > 0:
            msg += self.tr("    Domains that exist in the database but are not defined in the masterDict (extra tables in the database) are: ")
            for e in inDbNotInMasterDictSet:
                msg += f"{e}, "
            msg = msg[: len(msg) - 2] + "\n\n"
        domainDict = {i["nome"]: i["valores"] for i in masterDict["dominios"]}
        nameIdxDict = {
            i["nome"]: masterDict["dominios"].index(i) for i in masterDict["dominios"]
        }
        attributeNameDict = {
            "code": "code",
            "value": "code_name",
            "valor_filtro": "filter",
        }
        tableColumnsSetDict = abstractDb.getColumnsDictFromSchema(
            masterDict["schema_dominios"]
        )
        tablePrimaryKeySetDict = abstractDb.getPrimaryKeyDictFromSchema(
            masterDict["schema_dominios"]
        )
        for domainName in masterDictDomainNameSet.intersection(dbDomainNameSet):
            # 1. verificar se existem as colunas code e value
            columnsMasterFileSet = set()
            for column in domainDict[domainName][0]:
                if column in attributeNameDict:
                    columnsMasterFileSet.add(attributeNameDict[column])
            if tableColumnsSetDict[domainName] != columnsMasterFileSet:
                inMasterDictNotInDbSet = columnsMasterFileSet.difference(
                    tableColumnsSetDict[domainName]
                )
                inDbNotInMasterDictSet = tableColumnsSetDict[domainName].difference(
                    columnsMasterFileSet
                )
                msg += self.tr("Error in domains schema columns 'code' and 'value':\n")
                msg += self.tr("   Table {0} ").format(domainName)
                if len(inMasterDictNotInDbSet) > 0:
                    msg += self.tr("has the following columns in the MasterFile but not in the database:\n")
                    msg += ", ".join(list(inMasterDictNotInDbSet)) + "\n\n"
                if len(inDbNotInMasterDictSet) > 0:
                    msg += self.tr("has the following columns in the database but not in the MasterFile:\n")
                    msg += ", ".join(list(inDbNotInMasterDictSet)) + "\n\n"
                continue

            # 2. verificar se a chave primária é a coluna code
            setPrimaryKey = tablePrimaryKeySetDict[domainName]
            if len(setPrimaryKey) > 1:
                msg += self.tr("Primary Key error:\n")
                msg += self.tr("    The 'code' column should be the primary key, but the following were passed as primary keys:\n")
                msg += ", ".join(list(setPrimaryKey)) + "\n\n"
            elif len(setPrimaryKey) == 1:
                for pk in setPrimaryKey:
                    break
                if pk != "code":
                    msg += self.tr("Primary Key error:\n")
                    msg += self.tr("   The 'code' column should be the primary key of table {0}, but the primary key passed was: {1}\n\n").format(domainName, pk)
            else:
                msg += self.tr("Primary Key error:\n")
                msg += self.tr("   Table {0} does not have a primary key.\n\n").format(domainName)
            # 3. comparar os valores do masterfile, incluindo o valor a ser preenchido, com os valores populados no banco
            # Início da parte 3
            # monta o conjunto de tuplas do masterfile
            if not masterDict["dominios"][nameIdxDict[domainName]].get("filtro", False):
                masterFileDomainTupleSet = {
                    (
                        masterDict["a_ser_preenchido"]["code"],
                        masterDict["a_ser_preenchido"]["value"]
                        + f' ({masterDict["a_ser_preenchido"]["code"]})',
                    )
                }
                masterFileDomainTupleSet |= set(
                    (i["code"], i["value"] + f' ({i["code"]})')
                    for i in domainDict[domainName]
                )
                columnNameList = ["code", "code_name"]
            else:
                masterFileDomainTupleSet = {
                    (
                        masterDict["a_ser_preenchido"]["code"],
                        masterDict["a_ser_preenchido"]["value"]
                        + f' ({masterDict["a_ser_preenchido"]["code"]})',
                        masterDict["a_ser_preenchido"]["value"]
                        + f' ({masterDict["a_ser_preenchido"]["code"]})',
                    )
                }
                masterFileDomainTupleSet |= set(
                    (i["code"], i["value"] + f' ({i["code"]})', i["valor_filtro"])
                    for i in domainDict[domainName]
                )
                columnNameList = ["code", "code_name", "filter"]
            # monta o conjunto de tuplas do banco

            dbDomainTupleSet = abstractDb.getTupleSetFromTable(
                schemaName=masterDict["schema_dominios"],
                tableName=domainName,
                columnNameList=columnNameList,
            )

            if masterFileDomainTupleSet == dbDomainTupleSet:
                continue
            else:
                inMasterFileDomainNotInDbDomainSet = (
                    masterFileDomainTupleSet.difference(dbDomainTupleSet)
                )
                inDbDomainNotInMasterFileDomainSet = dbDomainTupleSet.difference(
                    masterFileDomainTupleSet
                )
                msg += self.tr("Value errors in domains schema:\n")
                msg += self.tr("   Table {0} has the following errors:\n").format(domainName)
                if len(inMasterFileDomainNotInDbDomainSet) > 0:
                    if not masterDict["dominios"][nameIdxDict[domainName]].get(
                        "filtro", False
                    ):
                        msg += self.tr("- Values in MasterFile without correspondence in the database: ")
                        for valor in inMasterFileDomainNotInDbDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}"
                        msg += "\n"
                    else:
                        msg += self.tr("- Values in MasterFile without correspondence in the database: ")
                        for valor in inMasterFileDomainNotInDbDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}, 'filter': {valor[2]}"
                        msg += "\n"
                if len(inDbDomainNotInMasterFileDomainSet) > 0:
                    if not masterDict["dominios"][nameIdxDict[domainName]].get(
                        "filtro", False
                    ):
                        msg += self.tr("- Values in database without correspondence in the MasterFile: ")
                        for valor in inDbDomainNotInMasterFileDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}"
                        msg += "\n"
                    else:
                        msg += self.tr("- Values in database without correspondence in the MasterFile: ")
                        for valor in inDbDomainNotInMasterFileDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}, 'filter': {valor[2]}"
                        msg += "\n"
                msg += "\n"
        return msg

    def validateEDGVTables(self, masterDict, abstractDb):
        """
        1 - verificar se o schema edgv faz parte do database
        2 - validar schema edgv, verificando a presença de todas as tabelas que são necessárias
        3 - validar a chave primária da tabela como sendo o 'id'
        4 - validas as colunas de cada tabela do schema edgv juntamente com os seus valores
        """
        msg = ""
        if not abstractDb.checkIfSchemaExistsInDatabase(masterDict["schema_dados"]):
            msg += self.tr("Schema {0} error: \n").format(masterDict["schema_dados"])
            msg += self.tr("    The schema '{0}' is not present in the database.\n").format(masterDict["schema_dados"])
            return msg
        dbEDGVNameSet = abstractDb.getTableListFromSchema(masterDict["schema_dados"])
        masterDictEDGVSet = set(
            f'{i["categoria"]}_{i["nome"]}{masterDict["geom_suffix"][j]}'
            for i in masterDict["classes"]
            for j in i["primitivas"]
        )
        masterDictEDGVSet |= set(
            f'{i["categoria"]}_{i["nome"]}{masterDict["geom_suffix"][j]}'
            for i in masterDict["extension_classes"]
            for j in i["primitivas"]
        )
        inMasterDictNotInDbSet = masterDictEDGVSet.difference(dbEDGVNameSet)
        inDbNotInMasterDictSet = dbEDGVNameSet.difference(masterDictEDGVSet)
        if len(inMasterDictNotInDbSet) > 0 or len(inDbNotInMasterDictSet) > 0:
            msg += self.tr("Error, there is a table discrepancy between the database and Masterfile:\n")
        if len(inMasterDictNotInDbSet) > 0:
            msg += self.tr("    Tables from {0} that are in the MasterFile but not in the database are: ").format(masterDict["schema_dados"])
            for table in inMasterDictNotInDbSet:
                msg += f"{table}, "
            msg = msg[: len(msg) - 2] + "\n\n"
        if len(inDbNotInMasterDictSet) > 0:
            msg += self.tr("    Tables from {0} that are in the database but not in the MasterFile are: ").format(masterDict["schema_dados"])
            for table in inDbNotInMasterDictSet:
                msg += f"{table}, "
            msg = msg[: len(msg) - 2] + "\n\n"

        tableNamePrimaryKeyDict = abstractDb.getPrimaryKeyDictFromSchema(
            masterDict["schema_dados"]
        )
        nameTableMsgDict = defaultdict(dict)
        for tableName in tableNamePrimaryKeyDict:
            if tableNamePrimaryKeyDict[tableName] == {"id"}:
                continue
            if not nameTableMsgDict[tableName].get(
                "primary key differs from 'id', the primary key(s) of the table are: ",
                False,
            ):
                nameTableMsgDict[tableName][
                    "primary key differs from 'id', the primary key(s) of the table are: "
                ] = []
            for pk in tableNamePrimaryKeyDict[tableName]:
                nameTableMsgDict[tableName][
                    "primary key differs from 'id', the primary key(s) of the table are: "
                ].append(f"{pk}, ")

        edgvDict = {
            f'{i["categoria"]}_{i["nome"]}{masterDict["geom_suffix"][j]}': i[
                "atributos"
            ]
            for i in masterDict["classes"]
            for j in i["primitivas"]
        }
        edgvDictExtensionClasses = {
            f'{i["categoria"]}_{i["nome"]}{masterDict["geom_suffix"][j]}': i[
                "atributos"
            ]
            for i in masterDict["extension_classes"]
            for j in i["primitivas"]
        }
        edgvDict.update(edgvDictExtensionClasses)
        geomSuffixDict = {
            "MultiPoint": "_p",
            "MultiLinestring": "_l",
            "MultiPolygon": "_a",
        }
        nameTableColumnIsNullableOrNoForeignTypeTableDict = (
            abstractDb.getTypeColumnFromSchema(masterDict["schema_dados"])
        )
        nameTableColumnMaxVarcharDict = abstractDb.getMaxLengthVarcharFromSchema(
            masterDict["schema_dados"]
        )
        for edgvName in masterDictEDGVSet.intersection(dbEDGVNameSet):
            masterNameTypeCardinalityMapValueSet = set()
            masterNameTypeCardinalityMapValueSet |= {
                ("geom", "USER-DEFINED", "YES"),
                ("observacao", "varchar(255)", "YES"),
            }
            for attribute in edgvDict[edgvName]:
                if attribute.get("primitivas", False):
                    geomList = attribute["primitivas"]
                    geomSuffixSet = set(geomSuffixDict[i] for i in geomList)
                    if ("_" + edgvName[-1]) in geomSuffixSet:
                        if attribute["cardinalidade"] == "0..1":
                            masterNameTypeCardinalityMapValueSet |= {
                                (attribute["nome"], attribute["tipo"], "YES")
                            }
                        elif attribute["cardinalidade"] == "1..1":
                            if not attribute.get("mapa_valor", False):
                                masterNameTypeCardinalityMapValueSet |= {
                                    (attribute["nome"], attribute["tipo"], "NO")
                                }
                            else:
                                masterNameTypeCardinalityMapValueSet |= {
                                    (
                                        attribute["nome"],
                                        attribute["tipo"],
                                        "NO",
                                        attribute["mapa_valor"],
                                    )
                                }
                else:
                    if attribute["cardinalidade"] == "0..1":
                        masterNameTypeCardinalityMapValueSet |= {
                            (attribute["nome"], attribute["tipo"], "YES")
                        }
                    elif attribute["cardinalidade"] == "1..1":
                        if not attribute.get("mapa_valor", False):
                            masterNameTypeCardinalityMapValueSet |= {
                                (attribute["nome"], attribute["tipo"], "NO")
                            }
                        else:
                            masterNameTypeCardinalityMapValueSet |= {
                                (
                                    attribute["nome"],
                                    attribute["tipo"],
                                    "NO",
                                    attribute["mapa_valor"],
                                )
                            }
            dbNameTypeCardinalityMapValueSet = set()
            for column in nameTableColumnIsNullableOrNoForeignTypeTableDict[edgvName]:
                if column == "id":
                    continue
                typeColumn = nameTableColumnIsNullableOrNoForeignTypeTableDict[
                    edgvName
                ][column]["type"]
                if typeColumn == "character varying":
                    maxVarchar = nameTableColumnMaxVarcharDict[edgvName][column]
                    typeColumn = f"varchar({maxVarchar})"
                if (
                    nameTableColumnIsNullableOrNoForeignTypeTableDict[edgvName][column][
                        "nullable"
                    ]
                    == "YES"
                ):
                    dbNameTypeCardinalityMapValueSet |= {(column, typeColumn, "YES")}
                else:
                    if not nameTableColumnIsNullableOrNoForeignTypeTableDict[edgvName][
                        column
                    ].get("foreignTable", False):
                        dbNameTypeCardinalityMapValueSet |= {(column, typeColumn, "NO")}
                    else:
                        mapValue = nameTableColumnIsNullableOrNoForeignTypeTableDict[
                            edgvName
                        ][column]["foreignTable"]
                        dbNameTypeCardinalityMapValueSet |= {
                            (column, typeColumn, "NO", mapValue)
                        }
            if masterNameTypeCardinalityMapValueSet == dbNameTypeCardinalityMapValueSet:
                continue
            else:
                inMasterNotInDbSet = masterNameTypeCardinalityMapValueSet.difference(
                    dbNameTypeCardinalityMapValueSet
                )
                inDbNotInMasterSet = dbNameTypeCardinalityMapValueSet.difference(
                    masterNameTypeCardinalityMapValueSet
                )
                if len(inMasterNotInDbSet) > 0 or len(inDbNotInMasterSet) > 0:
                    if not nameTableMsgDict[edgvName].get(
                        "The following values are present in the database but not in the Masterfile: ",
                        False,
                    ):
                        nameTableMsgDict[edgvName][
                            "The following values are present in the database but not in the Masterfile: "
                        ] = []
                    if not nameTableMsgDict[edgvName].get(
                        "The following values are present in the Masterfile but not in the database: ",
                        False,
                    ):
                        nameTableMsgDict[edgvName][
                            "The following values are present in the Masterfile but not in the database: "
                        ] = []
                if len(inMasterNotInDbSet) > 0:
                    for valor in inMasterNotInDbSet:
                        if len(valor) == 3:
                            nameTableMsgDict[edgvName][
                                "The following values are present in the Masterfile but not in the database: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, "
                            )
                        else:
                            nameTableMsgDict[edgvName][
                                "The following values are present in the Masterfile but not in the database: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, mapa_valor = {valor[3]}, "
                            )
                if len(inDbNotInMasterSet) > 0:
                    for valor in inDbNotInMasterSet:
                        if len(valor) == 3:
                            nameTableMsgDict[edgvName][
                                "The following values are present in the database but not in the Masterfile: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, "
                            )
                        else:
                            nameTableMsgDict[edgvName][
                                "The following values are present in the database but not in the Masterfile: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, mapa_valor = {valor[3]}, "
                            )
        return msg, nameTableMsgDict

    def validateCheckConstraint(self, masterDict, abstractDb):
        """ """
        dbNameTableColumnCheckConstraintDict = abstractDb.getCheckConstraintDict()
        for table in dbNameTableColumnCheckConstraintDict:
            for column in dbNameTableColumnCheckConstraintDict[table]:
                dbNameTableColumnCheckConstraintDict[table][column] = set(
                    dbNameTableColumnCheckConstraintDict[table][column]
                )

        masterNameTableColumnCheckConstraintDict = defaultdict(dict)
        for table in masterDict["classes"]:
            self.nameTableColumnCheckConstraint(
                masterDict, table, masterNameTableColumnCheckConstraintDict
            )

        for table in masterDict["extension_classes"]:
            self.nameTableColumnCheckConstraint(
                masterDict, table, masterNameTableColumnCheckConstraintDict
            )

        correspNameTableMapValueColumnDict = defaultdict(dict)
        for table in masterDict["classes"]:
            self.nameTableMapValueColumn(
                masterDict, table, correspNameTableMapValueColumnDict
            )

        for table in masterDict["extension_classes"]:
            self.nameTableMapValueColumn(
                masterDict, table, correspNameTableMapValueColumnDict
            )

        nameColumnCodeDict = defaultdict(set)
        for dominio in masterDict["dominios"]:
            for value in dominio["valores"]:
                nameColumnCodeDict[dominio["nome"]].add(value["code"])

        nameTableColumnForeignSetDict = defaultdict(dict)
        for table in correspNameTableMapValueColumnDict:
            for mapValue in correspNameTableMapValueColumnDict[table]:
                if mapValue not in nameColumnCodeDict:
                    continue
                nameTableColumnForeignSetDict[table][
                    correspNameTableMapValueColumnDict[table][mapValue]
                ] = nameColumnCodeDict[mapValue]

        tableToRemoveSet = self.tableToRemove(
            masterNameTableColumnCheckConstraintDict, nameTableColumnForeignSetDict
        )

        for table in tableToRemoveSet:
            masterNameTableColumnCheckConstraintDict.pop(table)

        for table in masterNameTableColumnCheckConstraintDict:
            for column in masterNameTableColumnCheckConstraintDict[table]:
                masterNameTableColumnCheckConstraintDict[table][column].add(9999)

        for table in dbNameTableColumnCheckConstraintDict:
            for column in dbNameTableColumnCheckConstraintDict[table]:
                nameTableMsgDict = self.validateCheckConstraintSet(
                    dbNameTableColumnCheckConstraintDict,
                    table,
                    column,
                    masterNameTableColumnCheckConstraintDict,
                )

        for table in masterNameTableColumnCheckConstraintDict:
            for column in masterNameTableColumnCheckConstraintDict[table]:
                nameTableMsgDictTwo = self.validateCheckConstraintSet(
                    dbNameTableColumnCheckConstraintDict,
                    table,
                    column,
                    masterNameTableColumnCheckConstraintDict,
                )
        nameTableMsgDict.update(nameTableMsgDictTwo)
        return nameTableMsgDict

    def tableToRemove(
        self, masterNameTableColumnCheckConstraintDict, nameTableColumnForeignSetDict
    ):
        tableForRemove = set()
        for table in masterNameTableColumnCheckConstraintDict:
            for column in masterNameTableColumnCheckConstraintDict[table]:
                if not nameTableColumnForeignSetDict.get(table, False):
                    continue
                if not nameTableColumnForeignSetDict[table].get(column, False):
                    continue
                foreignSet = nameTableColumnForeignSetDict[table][column]
                checkSet = masterNameTableColumnCheckConstraintDict[table][column]
                if foreignSet != checkSet:
                    continue
                tableForRemove.add(table)
        return tableForRemove

    def nameTableMapValueColumn(
        self, masterDict, table, correspNameTableMapValueColumnDict
    ):
        for attribute in table["atributos"]:
            if not attribute.get("valores", False):
                continue
            nameWithoutGeomSuffix = f'{table["categoria"]}_{table["nome"]}'
            if type(attribute["valores"]) == list:
                if type(attribute["valores"][0]) == int:
                    nameWithGeomSuffixSet = set(
                        nameWithoutGeomSuffix + masterDict["geom_suffix"][i]
                        for i in table["primitivas"]
                    )
                    for name in nameWithGeomSuffixSet:
                        if correspNameTableMapValueColumnDict[name].get(
                            attribute["mapa_valor"], False
                        ):
                            continue
                        correspNameTableMapValueColumnDict[name][
                            attribute["mapa_valor"]
                        ] = attribute["nome"]
                else:
                    for value in attribute["valores"]:
                        if not value.get("primitivas", False):
                            nameWithGeomSuffixSet = set(
                                nameWithoutGeomSuffix + i for i in ["_p", "_l", "_a"]
                            )
                        else:
                            nameWithGeomSuffixSet = set(
                                nameWithoutGeomSuffix + masterDict["geom_suffix"][i]
                                for i in value["primitivas"]
                            )
                        for name in nameWithGeomSuffixSet:
                            if correspNameTableMapValueColumnDict[name].get(
                                attribute["mapa_valor"], False
                            ):
                                continue
                            correspNameTableMapValueColumnDict[name][
                                attribute["mapa_valor"]
                            ] = attribute["nome"]
            else:
                for value in attribute["valores"]:
                    nameWithSuffixGeom = (
                        nameWithoutGeomSuffix + masterDict["geom_suffix"][value]
                    )
                    if correspNameTableMapValueColumnDict[nameWithSuffixGeom].get(
                        attribute["mapa_valor"], False
                    ):
                        continue
                    correspNameTableMapValueColumnDict[nameWithSuffixGeom][
                        attribute["mapa_valor"]
                    ] = attribute["nome"]

    def validateCheckConstraintSet(
        self,
        dbNameTableColumnCheckConstraintDict,
        table,
        column,
        masterNameTableColumnCheckConstraintDict,
    ):
        dbCheckConstraintSet = dbNameTableColumnCheckConstraintDict[table][column]
        masterCheckConstraintSet = masterNameTableColumnCheckConstraintDict[table][
            column
        ]
        inDbNotInMasterSet = dbCheckConstraintSet.difference(masterCheckConstraintSet)
        inMasterNotInMasterSet = masterCheckConstraintSet.difference(
            dbCheckConstraintSet
        )
        nameTableMsgDict = defaultdict(dict)
        if len(inDbNotInMasterSet) > 0 or len(inMasterNotInMasterSet) > 0:
            if not nameTableMsgDict[table].get(
                "Check constraints present in the database but not in the MasterFile: ",
                False,
            ):
                nameTableMsgDict[table][
                    "Check constraints present in the database but not in the MasterFile: "
                ] = []
            if not nameTableMsgDict[table].get(
                "Check constraints present in the Masterfile but not in the database: ",
                False,
            ):
                nameTableMsgDict[table][
                    "Check constraints present in the Masterfile but not in the database: "
                ] = []
        if len(inDbNotInMasterSet) > 0:
            for check in inDbNotInMasterSet:
                nameTableMsgDict[table][
                    "Check constraints present in the database but not in the MasterFile: "
                ].append(f"{check}, ")
        if len(inMasterNotInMasterSet) > 0:
            for check in inMasterNotInMasterSet:
                nameTableMsgDict[table][
                    "Check constraints present in the Masterfile but not in the database: "
                ].append(f"{check}, ")
        return nameTableMsgDict

    def nameTableColumnCheckConstraint(
        self, masterDict, table, masterNameTableColumnCheckConstraintDict
    ):
        for attribute in table["atributos"]:
            if not attribute.get("valores", False):
                continue
            nameWithoutGeomSuffix = f'{table["categoria"]}_{table["nome"]}'
            if type(attribute["valores"]) == list:
                if type(attribute["valores"][0]) == int:
                    nameWithGeomSuffixSet = set(
                        nameWithoutGeomSuffix + masterDict["geom_suffix"][i]
                        for i in table["primitivas"]
                    )
                    for name in nameWithGeomSuffixSet:
                        masterNameTableColumnCheckConstraintDict[name][
                            attribute["nome"]
                        ] = set(attribute["valores"])
                else:
                    for value in attribute["valores"]:
                        if not value.get("primitivas", False):
                            nameWithGeomSuffixSet = set(
                                nameWithoutGeomSuffix + i for i in ["_p", "_l", "_a"]
                            )
                        else:
                            nameWithGeomSuffixSet = set(
                                nameWithoutGeomSuffix + masterDict["geom_suffix"][i]
                                for i in value["primitivas"]
                            )
                        for name in nameWithGeomSuffixSet:
                            if not masterNameTableColumnCheckConstraintDict[name].get(
                                attribute["nome"], False
                            ):
                                masterNameTableColumnCheckConstraintDict[name][
                                    attribute["nome"]
                                ] = {value["code"]}
                            else:
                                masterNameTableColumnCheckConstraintDict[name][
                                    attribute["nome"]
                                ].add(value["code"])
            else:
                for value in attribute["valores"]:
                    nameWithSuffixGeom = (
                        nameWithoutGeomSuffix + masterDict["geom_suffix"][value]
                    )
                    masterNameTableColumnCheckConstraintDict[nameWithSuffixGeom][
                        attribute["nome"]
                    ] = set(attribute["valores"][value])

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydifferencesbetweendatabasemodelsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Differences Between Database Models")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Utils")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Utils"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyDifferencesBetweenDatabaseModelsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyDifferencesBetweenDatabaseModelsAlgorithm()


class MyWidgetWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder = args[0]

    def createWidget(self):
        self._lineedit = QLineEdit()
        self._lineedit.setEchoMode(QLineEdit.Password)
        # if self.placeholder:
        #     self._lineedit.setPlaceholderText(self.placeholder)
        return self._lineedit

    def value(self):
        return self._lineedit.text()
