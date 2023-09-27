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

from PyQt5.QtCore import QCoreApplication, QVariant
from datetime import datetime
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFile,
    QgsProcessingParameterString,
    QgsProcessingAlgorithm,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingException,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterField,
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
        msg, nameTableMsgDict = self.validateEDGVTables(masterDict, abstractDb)
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
            msg += f"Erro na tabela = {table}: \n"
            for typeMsg in nameTableMsgDict[table]:
                msg += f"   {typeMsg}\n"
                if nameTableMsgDict[table][typeMsg] == []:
                    continue
                msg += f"   "
                for element in nameTableMsgDict[table][typeMsg]:
                    msg += f"{element}"
                msg = msg[: len(msg) - 2] + "\n"
            msg += "\n"

        self.pushOutputMessage(feedback, msg, fileTxt)

        return {self.OUTPUT: fileTxt}

    def pushOutputMessage(self, feedback, msg, fileTxt):
        if msg == "":
            feedback.pushInfo(
                "A estrutura do banco de entrada corresponde à estrutura definida pelo masterfile de entrada."
            )
            with open(f"{fileTxt}", "w") as file:
                file.write(
                    "A estrutura do banco de entrada corresponde à estrutura definida pelo masterfile de entrada."
                )
        else:
            feedback.pushInfo(
                "A estrutura do banco de entrada não corresponde à estrutura definida pelo masterfile de entrada:"
            )
            feedback.pushInfo(msg)
            with open(f"{fileTxt}", "w") as file:
                file.write(
                    "A estrutura do banco de entrada não corresponde à estrutura definida pelo masterfile de entrada:\n"
                )
                file.write(f"{msg}")
        file.close()

    def getAbstractDb(self, host, port, database, user, password):
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(host, port, database, user, password)
        return abstractDb

    def getMasterDict(self, masterFile):
        """
        Leitura do masterfile
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
            msg += "Erro de versão:\n"
        if edgvVersion != masterDict["modelo"]:
            msg += f"   A versão do banco ({edgvVersion}) não corresponde à versão do masterfile ({masterDict['modelo']})\n"
        if implementationVersion != masterDict["versao"]:
            msg += f"   A versão de implementação do banco ({implementationVersion}) não corresponde à versão de implementação do masterfile ({masterDict['versao']})\n"
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
            msg += "Erro no Schema de domínios:\n"
            msg += f"   A o esquema de domínios {masterDict['schema_dominios']} não está implementado no banco."
            return msg
        masterDictDomainNameSet = set(i["nome"] for i in masterDict["dominios"])
        dbDomainNameSet = abstractDb.getTableListFromSchema(
            masterDict["schema_dominios"]
        )

        inMasterDictNotInDbSet = masterDictDomainNameSet.difference(dbDomainNameSet)
        inDbNotInMasterDictSet = dbDomainNameSet.difference(masterDictDomainNameSet)

        if len(inMasterDictNotInDbSet) > 0 or len(inDbNotInMasterDictSet) > 0:
            msg += "Erro, há disparidade entre as tabelas do Database e do Masterfile no Schema dominios:\n"

        if len(inMasterDictNotInDbSet) > 0:
            msg += "    Os domínios que existem no masterDict, mas não exitem no banco (tabelas que faltam no banco) são: "
            for e in inMasterDictNotInDbSet:
                msg += f"{e}, "
            msg = msg[: len(msg) - 2] + "\n\n"

        if len(inDbNotInMasterDictSet) > 0:
            msg += "    Os domínios que existem no banco, mas não estão previstas no masterDict (tabelas excedentes no banco) são: "
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
                msg += "Erro no Schema dominios colunas 'code' e 'value':\n"
                msg += f"   A tabela {domainName} "
                if len(inMasterDictNotInDbSet) > 0:
                    msg += "possui as seguintes colunas no MasterFile, mas não no database: "
                    for column in inMasterDictNotInDbSet:
                        msg += f"{column}, "
                    msg = msg[: len(msg) - 2] + "\n\n"
                if len(inDbNotInMasterDictSet) > 0:
                    msg += "possui as seguintes colunas no database, mas não no MasterFile: "
                    for column in inDbNotInMasterDictSet:
                        msg += f"{column}, "
                    msg = msg[: len(msg) - 2] + "\n\n"
                # TODO: adicionar mensagem com a diferença entre as colunas do masterfile e do banco
                # TODO: avisar que a verificação de domínio parou aqui por não ter as mesmas colunas
                return msg

            # 2. verificar se a chave primária é a coluna code
            setPrimaryKey = tablePrimaryKeySetDict[domainName]
            if len(setPrimaryKey) > 1:
                msg += "Erro Primary Key:\n"
                msg += "    A coluna 'code' deve ser a chave primária, mas foram passadas como chaves primárias: "
                for pk in setPrimaryKey:
                    msg += f"{pk}, "
                msg = msg[: len(msg) - 2] + "\n\n"
            elif len(setPrimaryKey) == 1:
                for pk in setPrimaryKey:
                    break
                if pk != "code":
                    msg += "Erro Primary Key:\n"
                    msg += f"   A coluna 'code' deve ser a chave primária da tabela {domainName}, mas a chava primária passada foi: {pk}\n\n"
            else:
                msg += "Erro Primary Key:\n"
                msg += f"   A tabela {domainName} não possui chave primária.\n\n"
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
                msg += "Erro valores no Schema dominios:\n"
                msg += f"   A tabela {domainName} "
                if len(inMasterFileDomainNotInDbDomainSet) > 0:
                    if not masterDict["dominios"][nameIdxDict[domainName]].get(
                        "filtro", False
                    ):
                        msg += f"possui os seguintes valores no MasterFile sem correspondência no database: "
                        for valor in inMasterFileDomainNotInDbDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}"
                        msg += "\n\n"
                    else:
                        msg += f"possui os seguintes valores no MasterFile sem correspondência no database: "
                        for valor in inMasterFileDomainNotInDbDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}, 'filter': {valor[2]}"
                        msg += "\n\n"
                if len(inDbDomainNotInMasterFileDomainSet) > 0:
                    if not masterDict["dominios"][nameIdxDict[domainName]].get(
                        "filtro", False
                    ):
                        msg += f"possui os seguintes valores no database sem correspondência no MasterFile: "
                        for valor in inDbDomainNotInMasterFileDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}"
                        msg += "\n\n"
                    else:
                        msg += f"possui os seguintes valores no database sem correspondência no MasterFile: "
                        for valor in inDbDomainNotInMasterFileDomainSet:
                            msg += f"'code': {valor[0]}, 'code_name': {valor[1]}, 'filter': {valor[2]}"
                        msg += "\n\n"

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
            msg += "Erro Schema edgv: \n"
            msg += "    O schema 'edgv' não está presente no database.\n"
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
            msg += "Erro, há divergência de tabelas no Database e Masterfile:\n"
        if len(inMasterDictNotInDbSet) > 0:
            msg += "    As tabelas do edgv que estão no MasterFile, mas não estão do database são: "
            for table in inMasterDictNotInDbSet:
                msg += f"{table}, "
            msg = msg[: len(msg) - 2] + "\n\n"
        if len(inDbNotInMasterDictSet) > 0:
            msg += "    As tabelas do edgv que estão no database, mas não estão no MasterFile são: "
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
                "chave primária diferente do 'id' a chava primária é/são da tabela: ",
                False,
            ):
                nameTableMsgDict[tableName][
                    "chave primária diferente do 'id' a chava primária é/são da tabela: "
                ] = []
            for pk in tableNamePrimaryKeyDict[tableName]:
                nameTableMsgDict[tableName][
                    "chave primária diferente do 'id' a chava primária é/são da tabela: "
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
                        "Os seguintes valores estão presentes no database, mas não estão no Masterfile: ",
                        False,
                    ):
                        nameTableMsgDict[edgvName][
                            "Os seguintes valores estão presentes no database, mas não estão no Masterfile: "
                        ] = []
                    if not nameTableMsgDict[edgvName].get(
                        "Os seguintes valores estão presentes no Masterfile, mas não estão no database: ",
                        False,
                    ):
                        nameTableMsgDict[edgvName][
                            "Os seguintes valores estão presentes no Masterfile, mas não estão no database: "
                        ] = []
                if len(inMasterNotInDbSet) > 0:
                    for valor in inMasterNotInDbSet:
                        if len(valor) == 3:
                            nameTableMsgDict[edgvName][
                                "Os seguintes valores estão presentes no Masterfile, mas não estão no database: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, "
                            )
                        else:
                            nameTableMsgDict[edgvName][
                                "Os seguintes valores estão presentes no Masterfile, mas não estão no database: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, mapa_valor = {valor[3]}, "
                            )
                if len(inDbNotInMasterSet) > 0:
                    for valor in inDbNotInMasterSet:
                        if len(valor) == 3:
                            nameTableMsgDict[edgvName][
                                "Os seguintes valores estão presentes no database, mas não estão no Masterfile: "
                            ].append(
                                f"coluna: {valor[0]}, tipo: {valor[1]}, opcional: {valor[2]}, "
                            )
                        else:
                            nameTableMsgDict[edgvName][
                                "Os seguintes valores estão presentes no database, mas não estão no Masterfile: "
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
                "As chaves check que estão presentes no database, mas não estão no MasterFile: ",
                False,
            ):
                nameTableMsgDict[table][
                    "As chaves check que estão presentes no database, mas não estão no MasterFile: "
                ] = []
            if not nameTableMsgDict[table].get(
                "As chaves check que estão presentes no Materfile, mas não estão no database: ",
                False,
            ):
                nameTableMsgDict[table][
                    "As chaves check que estão presentes no Materfile, mas não estão no database: "
                ] = []
        if len(inDbNotInMasterSet) > 0:
            for check in inDbNotInMasterSet:
                nameTableMsgDict[table][
                    "As chaves check que estão presentes no database, mas não estão no MasterFile: "
                ].append(f"{check}, ")
        if len(inMasterNotInMasterSet) > 0:
            for check in inMasterNotInMasterSet:
                nameTableMsgDict[table][
                    "As chaves check que estão presentes no Materfile, mas não estão no database: "
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
        return self.tr("Other Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Other Algorithms"

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
