# -*- coding: utf-8 -*-
"""@package docstring
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-10-21
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.core import Qgis
from qgis.PyQt.QtCore import QSettings
from qgis.core import (
    Qgis,
    QgsMessageLog,
    QgsCredentials,
    QgsVectorLayer,
    QgsDataSourceUri,
)

from .abstractDb import AbstractDb
from .pgConnectionAdapter import PsycopgDbAdapter
from .pgDataTypes import (
    ColumnDomainInfo,
    DatabaseLayerInfo,
    GeomDictResult,
    GeomTableEntry,
    TableDomainInfo,
)
from .pgDecorators import ensure_connected, transactional
from ..SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.dsgEnums import DsgEnums

from osgeo import ogr
from uuid import uuid4
from collections import defaultdict
import codecs, os, json, binascii, re
import psycopg2
import time


class PostgisDb(AbstractDb):
    def __init__(self):
        """
        Constructor
        """
        super(PostgisDb, self).__init__()
        # setting database type to postgresql
        self.db = PsycopgDbAdapter()
        # setting up a sql generator
        self.gen = SqlGeneratorFactory().createSqlGenerator(
            driver=DsgEnums.DriverPostGIS
        )
        self.databaseEncoding = "utf-8"

    def closeDatabase(self):
        if self.db is not None and self.db.isOpen():
            # self.dropAllConections(self.getDatabaseName())
            self.db.close()

    # ------------------------------------------------------------------
    # Low-level psycopg2 helpers
    # These replace the QSqlQuery(sql, self.db) / query.isActive() pattern.
    # All callers must ensure the connection is open (@ensure_connected).
    # ------------------------------------------------------------------

    def _execute(self, sql, params=None):
        """
        Execute *sql* (with optional *params* for parameterised queries) and
        return the cursor so the caller can fetch rows or check rowcount.
        Raises Exception on failure.
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, params)
        except Exception as e:
            raise Exception(str(e))
        return cursor

    def _execute_autocommit(self, sql, params=None):
        """
        Execute *sql* outside any transaction (autocommit mode).
        Required for PostgreSQL DDL that cannot run inside a transaction:
        CREATE DATABASE, DROP DATABASE, etc.
        """
        with self.db.autocommit_block() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, params)
            except Exception as e:
                raise Exception(str(e))
            finally:
                cursor.close()

    def _fetch_all(self, sql, params=None):
        """
        Execute *sql* and return all rows as a list of tuples.
        """
        cursor = self._execute(sql, params)
        return cursor.fetchall()

    def _fetch_one(self, sql, params=None):
        """
        Execute *sql* and return the first row, or None if empty.
        """
        cursor = self._execute(sql, params)
        return cursor.fetchone()

    @staticmethod
    def _as_json(value):
        """
        psycopg2 deserialises JSON/JSONB columns to dict/list automatically.
        This helper accepts both pre-parsed objects and raw strings so that
        callers don't need to branch on the type.
        """
        if isinstance(value, (dict, list)):
            return value
        return json.loads(value)

    def getDatabaseParameters(self):
        """
        Gets (host, port, user, password)
        """
        return (
            self.db.hostName(),
            self.db.port(),
            self.db.userName(),
            self.db.password(),
        )

    def getDatabaseName(self):
        """
        Gets the database name
        """
        return self.db.databaseName()

    def getHostName(self):
        return str(self.db.hostName())

    def connectDatabase(self, conn=None):
        """
        Connects to database
        conn: connection parameters. It can be a OGR connection or a QSettings connection
        """
        if conn.split(":")[0] == "PG":
            connSplit = conn.split(" ")
            parDict = dict()
            for i in connSplit[1::]:
                par = i.split("=")
                parDict[par[0]] = par[1]
            self.connectDatabaseWithParameters(
                parDict["host"],
                parDict["port"],
                parDict["dbname"],
                parDict["user"],
                parDict["password"],
            )
        else:
            self.connectDatabaseWithQSettings(conn)

    def connectDatabaseWithParameters(self, host, port, database, user, password):
        """
        Connects to database with parameters
        host: host IP
        port: host port
        database: database name
        user: user name
        password: user password
        """
        if not self.testCredentials(host, port, database, user, password):
            self.getCredentials(host, port, user, database)

    def getCredentials(self, host, port, user, database, timeout=100):
        conInfo = "host={0} port={1} dbname={2}".format(host, port, database)
        check = False
        startTime = time.time()
        while not check:
            (success, user, password) = QgsCredentials.instance().get(
                conInfo, user, None
            )
            if not success:
                return
            if self.testCredentials(host, port, database, user, password):
                check = True
                QgsCredentials.instance().put(conInfo, user, password)
            if time.time() - startTime > timeout:
                return

    def testCredentials(self, host, port, database, user, password):
        try:
            # Close any existing connection before changing parameters so
            # that PsycopgDbAdapter.open() always creates a fresh connection.
            if self.db.isOpen():
                self.db.close()
            self.db.setHostName(host)
            if not isinstance(port, int):
                port = int(port)
            self.db.setPort(port)
            self.db.setDatabaseName(database)
            self.db.setUserName(user)
            self.db.setPassword(password)
            self.checkAndOpenDb()
            return True
        except:
            return False

    def connectDatabaseWithQSettings(self, name):
        """
        Connects to database with parameters
        name: QSettings connection name
        """
        # getting connection parameters from qsettings
        (host, port, database, user, password) = self.getConnectionFromQSettings(name)
        self.db.setHostName(host)
        if type(port) != "int":
            self.db.setPort(int(port))
        else:
            self.db.setPort(port)
        self.db.setDatabaseName(database)
        self.db.setUserName(user)
        if not password or password == "":
            conInfo = "host=" + host + " port=" + port + " dbname=" + database
            check = False
            while not check:
                try:
                    (success, user, password) = QgsCredentials.instance().get(
                        conInfo, user, None
                    )
                    if not success:
                        return
                    self.db.setPassword(password)
                    check = True
                    self.checkAndOpenDb()
                    QgsCredentials.instance().put(conInfo, user, password)
                except:
                    pass
        else:
            self.db.setPassword(password)

    @ensure_connected
    def getDatabaseVersion(self):
        """
        Gets the database version
        """
        try:
            rows = self._fetch_all(self.gen.getEDGVVersion())
        except Exception:
            self.db.rollback()
            return "Non_EDGV"
        version = "-1"
        for row in rows:
            version = row[0]
        return version

    @ensure_connected
    def listGeomClassesFromDatabase(
        self,
        primitiveFilter=[],
        withElements=False,
        excludeViews=True,
        getGeometryColumn=False,
    ):
        """
        Gets a list with geometry classes from database
        returns dict if getGeometryColumn = True
        return list if getGeometryColumn = False
        """
        classList = []
        schemaList = [
            i for i in self.getGeomSchemaList() if i not in ["validation", "views"]
        ]
        # primitiveFilter building
        dbPrimitiveList = []
        if len(primitiveFilter) > 0:
            for primitive in primitiveFilter:
                if primitive == "p":
                    dbPrimitiveList.append("POINT")
                    dbPrimitiveList.append("MULTIPOINT")
                if primitive == "l":
                    dbPrimitiveList.append("LINESTRING")
                    dbPrimitiveList.append("MULTILINESTRING")
                if primitive == "a":
                    dbPrimitiveList.append("POLYGON")
                    dbPrimitiveList.append("MULTIPOLYGON")
        sql = self.gen.getGeomTables(
            schemaList,
            dbPrimitiveList=dbPrimitiveList,
            excludeViews=excludeViews,
            geomColumn=getGeometryColumn,
        )
        rows = self._fetch_all(sql)
        localList = []
        for row in rows:
            tableSchema = row[0]
            tableName = row[1]
            layerName = tableSchema + "." + tableName
            geometryColumn = ""
            if getGeometryColumn:
                geometryColumn = row[2]
            localList.append(
                {
                    "schema": tableSchema,
                    "tableName": tableName,
                    "layerName": layerName,
                    "geometryColumn": geometryColumn,
                }
            )
        # remove possible duplicates to filter layers with elements
        layerNameList = []
        for i in localList:
            if i["layerName"] not in layerNameList:
                layerNameList.append(i["layerName"])
        if withElements:
            listWithElements = self.getLayersWithElementsV2(layerNameList)
            partialTagList = [
                i for i in localList if i["tableName"] in listWithElements
            ]
        else:
            partialTagList = localList
        if not getGeometryColumn:
            classList = [i["layerName"] for i in partialTagList]
        else:
            classList = partialTagList
        return classList

    @ensure_connected
    def listComplexClassesFromDatabase(self):
        """
        Gets a list with complex classes from database
        """
        classList = []
        rows = self._fetch_all(self.gen.getTablesFromDatabase())
        for row in rows:
            tableSchema = row[0]
            tableName = row[1]
            layerName = tableSchema + "." + tableName
            if tableSchema == "complexos":
                classList.append(layerName)
        classList.sort()
        return classList

    def storeConnection(self, server):
        """
        Stores a connection into QSettings
        """
        (host, port, user, password) = self.getServerConfiguration(server)
        database = self.db.databaseName()
        connection = server + "_" + database
        settings = QSettings()
        if not settings.contains("PostgreSQL/connections/" + connection + "/database"):
            settings.beginGroup("PostgreSQL/connections/" + connection)
            settings.setValue("database", database)
            settings.setValue("host", host)
            settings.setValue("port", port)
            settings.setValue("username", user)
            settings.setValue("password", password)
            settings.endGroup()
            return True
        return False

    def getConnectionFromQSettings(self, conName):
        """
        Gets a connection from QSettings
        conName: connection name stored
        """
        settings = QSettings()
        settings.beginGroup("PostgreSQL/connections/" + conName)
        host = settings.value("host")
        port = settings.value("port")
        database = settings.value("database")
        user = settings.value("username")
        password = settings.value("password")
        settings.endGroup()
        return (host, port, database, user, password)

    def getServerConfiguration(self, name):
        """
        Gets a server configuration from QSettings
        name: server name
        """
        settings = QSettings()
        settings.beginGroup("PostgreSQL/servers/" + name)
        host = settings.value("host")
        port = settings.value("port")
        user = settings.value("username")
        password = settings.value("password")
        settings.endGroup()
        return (host, port, user, password)

    @ensure_connected
    def getStructureDict(self):
        """
        Gets database structure according to the edgv version
        """
        classDict = dict()
        rows = self._fetch_all(self.gen.getStructure(self.getDatabaseVersion()))
        for row in rows:
            className = str(row[0]) + "." + str(row[1])
            fieldName = str(row[2])
            if str(row[0]) == "complexos" or className.split("_")[-1] in [
                "p",
                "l",
                "a",
            ]:
                if className not in list(classDict.keys()):
                    classDict[className] = dict()
                classDict[className][fieldName] = fieldName
                if "geom" in list(classDict[className].keys()):
                    classDict[className]["geom"] = "GEOMETRY"
                if str(row[0]) != "complexos" and "id" in list(
                    classDict[className].keys()
                ):
                    classDict[className]["id"] = "OGC_FID"
        return classDict

    def makeOgrConn(self):
        """
        Makes a OGR connection string
        """
        dbName = self.db.databaseName()
        dbUser = self.db.userName()
        dbHost = self.db.hostName()
        dbPass = self.db.password()
        dbPort = str(self.db.port())
        constring = (
            "PG: dbname='"
            + dbName
            + "' user='"
            + dbUser
            + "' host='"
            + dbHost
            + "' password='"
            + dbPass
            + "' port="
            + dbPort
        )
        return constring

    @ensure_connected
    def getNotNullDict(self):
        """
        Gets a dictionary with all not null fields for the edgv database used
        """
        if self.getDatabaseVersion() == "2.1.3":
            schemaList = ["cb", "complexos"]
        elif self.getDatabaseVersion() in ("3.0", "2.1.3 Pro", "3.0 Pro"):
            schemaList = ["edgv", "complexos"]
        elif self.getDatabaseVersion() == "FTer_2a_Ed":
            schemaList = ["pe", "ge", "complexos"]
        else:
            QgsMessageLog.logMessage(
                self.tr("Operation not defined for this database version!"),
                "DSGTools Plugin",
                Qgis.MessageLevel.Critical,
            )
            return None

        rows = self._fetch_all(self.gen.getNotNullFields(schemaList))
        notNullDict = dict()
        for row in rows:
            schemaName = str(row[0])
            className = str(row[1])
            attName = str(row[2])
            cl = schemaName + "." + className
            if cl not in list(notNullDict.keys()):
                notNullDict[cl] = []
            notNullDict[cl].append(attName)
        return notNullDict

    @ensure_connected
    def getDomainDict(self):
        """
        SHOULD BE DEPRECATED OR IN FOR A MAJOR REFACTORY!!!!!
        Gets the domain dictionary for the edgv database used
        """
        if self.getDatabaseVersion() == "2.1.3":
            schemaList = ["cb", "complexos", "dominios"]
        elif self.getDatabaseVersion() in ("3.0", "2.1.3 Pro", "3.0 Pro"):
            schemaList = ["edgv", "complexos", "dominios"]
        elif self.getDatabaseVersion() == "FTer_2a_Ed":
            schemaList = ["pe", "ge", "complexos"]
        else:
            QgsMessageLog.logMessage(
                self.tr("Operation not defined for this database version!"),
                "DSGTools Plugin",
                Qgis.MessageLevel.Critical,
            )
            return

        rows = self._fetch_all(self.gen.validateWithDomain(schemaList))
        classDict = dict()
        for row in rows:
            schemaName = str(row[0])
            className = str(row[1])
            attName = str(row[2])
            domainQuery = str(row[5])
            cl = schemaName + "." + className
            for drow in self._fetch_all(domainQuery):
                value = int(drow[0])
                classDict = self.utils.buildNestedDict(
                    classDict, [str(cl), str(attName)], [value]
                )
        return classDict

    def translateAbstractDbLayerNameToOutputFormat(self, lyr, outputAbstractDb):
        """
        Translates abstractdb layer name to output format
        lyr: layer name that will be translated
        outputAbstractDb: output database
        """
        if outputAbstractDb.db.driverName() == "QSQLITE":
            return str(lyr.split(".")[0] + "_" + "_".join(lyr.split(".")[1::]))
        if outputAbstractDb.db.driverName() == "QPSQL":
            return lyr

    def translateOGRLayerNameToOutputFormat(self, lyr, ogrOutput):
        """
        Translates ogr layer name to output format
        lyr: layer name that will be translated
        ogrOutput: ogr output
        """
        if ogrOutput.GetDriver().name == "SQLite":
            return str(lyr.split(".")[0] + "_" + "_".join(lyr.split(".")[1::]))
        if ogrOutput.GetDriver().name == "PostgreSQL":
            return lyr

    def getTableSchema(self, lyr):
        """
        DEPRECATED
        Gets the table schema
        lyr: layer name
        """
        schema = lyr.split(".")[0]
        className = "_".join(lyr.split(".")[1::])
        return (schema, className)

    @ensure_connected
    def obtainLinkColumn(self, complexClass, aggregatedClass):
        """
        Obtains the link column between complex and aggregated class
        complexClass: complex class name
        aggregatedClass: aggregated class name
        """
        complexClass = complexClass.replace("complexos.", "")
        rows = self._fetch_all(self.gen.getLinkColumn(complexClass, aggregatedClass))
        column_name = ""
        for row in rows:
            column_name = row[0]
        return column_name

    @ensure_connected
    def loadAssociatedFeatures(self, complex):
        """
        Loads all the features associated to the complex
        complex: complex class name
        """
        associatedDict = dict()
        complex = complex.replace("complexos.", "")
        for row in self._fetch_all(self.gen.getComplexLinks(complex)):
            complex_schema = row[0]
            complex = row[1]
            aggregated_schema = row[2]
            aggregated_class = row[3]
            column_name = row[4]

            for crow in self._fetch_all(
                self.gen.getComplexData(complex_schema, complex)
            ):
                complex_uuid = crow[0]
                name = crow[1]

                if not (complex_uuid and name):
                    continue

                associatedDict = self.utils.buildNestedDict(
                    associatedDict, [name, complex_uuid, aggregated_class], []
                )

                for arow in self._fetch_all(
                    self.gen.getAssociatedFeaturesData(
                        aggregated_schema, aggregated_class, column_name, complex_uuid
                    )
                ):
                    ogc_fid = arow[0]
                    associatedDict = self.utils.buildNestedDict(
                        associatedDict,
                        [name, complex_uuid, aggregated_class],
                        [ogc_fid],
                    )
        return associatedDict

    @ensure_connected
    def isComplexClass(self, className):
        """
        Checks if a class is a complex class
        className: class name to be checked
        """
        for row in self._fetch_all(self.gen.getComplexTablesFromDatabase()):
            if row[0] == className:
                return True
        return False

    def disassociateComplexFromComplex(self, aggregated_class, link_column, id):
        """
        Disassociates a complex from another complex
        aggregated_class: aggregated class that will be disassociated
        link_column: link column between complex and its aggregated class
        id: complex id (uid) to be disassociated
        """
        self._execute(
            self.gen.disassociateComplexFromComplex(aggregated_class, link_column, id)
        )

    @ensure_connected
    def getUsers(self):
        """
        Gets 'this' database users
        """
        ret = [row[0] for row in self._fetch_all(self.gen.getUsers())]
        ret.sort()
        return ret

    @ensure_connected
    def getUserRelatedRoles(self, username):
        """
        Gets user roles assigned to 'username'
        username: user name
        """
        installed = []
        assigned = []
        for row in self._fetch_all(self.gen.getUserRelatedRoles(username)):
            rolname = row[0]
            usename = row[1]
            if not usename:
                installed.append(rolname)
            else:
                assigned.append(rolname)
        installed.sort()
        assigned.sort()
        return installed, assigned

    @ensure_connected
    def getRoles(self):
        """
        Gets roles installed in 'this' database
        """
        ret = [row[0] for row in self._fetch_all(self.gen.getRoles())]
        ret.sort()
        return ret

    @ensure_connected
    def createRole(self, role, roleDict, permissionManager=False):
        """
        Creates a role into this database
        role: role name
        dict: role definitions
        """
        # making this so the instaciated permissions stay with different names
        uuid = str(uuid4()).replace("-", "_")
        role += "_" + uuid

        sql = self.gen.createRole(role, roleDict)
        split = sql.split(";")

        if permissionManager:
            self._execute(sql)
            return role

        # try to revoke the permissions
        try:
            self.dropRole(role)
        except:
            pass

        for inner in split:
            try:
                self._execute(inner)
            except Exception as e:
                if "42710" in str(e) or (hasattr(e, "pgcode") and e.pgcode == "42710"):
                    # Role is already created (duplicate object error). Proceed with grants.
                    continue
                else:
                    raise Exception(
                        self.tr("Problem assigning profile: ") + role + "\n" + str(e)
                    )

    @ensure_connected
    def dropRole(self, role):
        """
        Deletes a role from 'this' database
        role: role name
        """
        sql = self.gen.dropRole(role)
        split = sql.split("#")

        for inner in split:
            try:
                self._execute(inner)
            except Exception as e:
                if "2BP01" in str(e) or (hasattr(e, "pgcode") and e.pgcode == "2BP01"):
                    # Role is still used by other databases; skip drop.
                    continue
                else:
                    raise Exception(
                        self.tr("Problem removing profile: ") + role + "\n" + str(e)
                    )

    @ensure_connected
    def alterUserPass(self, user, newpassword):
        """
        Alters the user password
        user: user name
        newpassword: new password
        """
        self._execute(self.gen.alterUserPass(user, newpassword))

    @ensure_connected
    def createUser(self, user, password, isSuperUser):
        """
        Creates a new user
        user: user name
        password: user password
        isSuperUser: bool to define is the newly created user is a super user (i.e a user like 'postgres')
        """
        self._execute(self.gen.createUser(user, password, isSuperUser))

    @ensure_connected
    def removeUser(self, user):
        """
        Removes a user
        user: user name
        """
        self._execute(self.gen.removeUser(user))

    @ensure_connected
    def grantRole(self, user, role):
        """
        Grants a role to a user
        user: user name
        role: role name
        """
        self._execute(self.gen.grantRole(user, role))

    @ensure_connected
    def revokeRole(self, user, role):
        """
        Revokes a role from the user
        user: user name
        role: role name
        """
        self._execute(self.gen.revokeRole(user, role))

    @ensure_connected
    def getTablesFromDatabase(self):
        """
        Gets all tables from database
        """
        return [
            "{0}.{1}".format(row[0], row[1])
            for row in self._fetch_all(self.gen.getTablesFromDatabase())
        ]

    @ensure_connected
    def getRolePrivileges(self, role, dbname):
        """
        Gets role settings (e.g. what is possible to do with the role)
        role: role name
        dbname: database name
        """
        privilegesDict = dict()

        for row in self._fetch_all(self.gen.getRolePrivileges(role, dbname)):
            schema = row[3]
            table = row[4]
            privilege = row[5]

            if schema in ["cb", "public", "complexos", "dominios", "pe", "ge"]:
                privilegesDict = self.utils.buildNestedDict(
                    privilegesDict, [schema, table], [privilege]
                )

        permissionsDict = dict()
        for schema in list(privilegesDict.keys()):
            for table in list(privilegesDict[schema].keys()):
                split = table.split("_")
                category = split[0]
                layerName = schema + "." + table

                if schema not in list(permissionsDict.keys()):
                    permissionsDict[schema] = dict()

                if category not in list(permissionsDict[schema].keys()):
                    permissionsDict[schema][category] = dict()

                privileges = privilegesDict[schema][table]
                write = [
                    "DELETE",
                    "INSERT",
                    "SELECT",
                    "UPDATE",
                    "TRUNCATE",
                    "REFERENCES",
                    "TRIGGER",
                ]
                if all((permission in privileges for permission in write)):
                    if layerName not in permissionsDict[schema][category]:
                        permissionsDict[schema][category][layerName] = dict()
                        permissionsDict[schema][category][layerName][
                            "read"
                        ] = "2"  # read yes
                        permissionsDict[schema][category][layerName][
                            "write"
                        ] = "2"  # write yes
                else:
                    if layerName not in permissionsDict[schema][category]:
                        permissionsDict[schema][category][layerName] = dict()
                        permissionsDict[schema][category][layerName][
                            "read"
                        ] = "2"  # read yes
                        permissionsDict[schema][category][layerName][
                            "write"
                        ] = "0"  # write no

        return permissionsDict

    def getFrameLayerName(self):
        """
        Gets the frame layer name
        """
        return "public.aux_moldura_a"

    @ensure_connected
    def getEDGVDbsFromServer(self, parentWidget=None, getDatabaseVersions=True):
        """
        Gets edgv databases from 'this' server.

        Previously this method created a new QSqlDatabase("QPSQL") per
        database in a loop and never closed them, leaking N connections.
        Now it uses ephemeral_connection() which guarantees the temporary
        connection is closed after each iteration.
        """
        try:
            rows = self._fetch_all(self.gen.getDatabasesFromServer())
        except Exception as e:
            raise Exception(self.tr("Problem getting EDGV databases: ") + str(e))

        dbList = [row[0] for row in rows]

        edvgDbList = []
        if parentWidget:
            progress = ProgressWidget(
                1,
                len(dbList),
                self.tr("Reading selected databases... "),
                parent=parentWidget,
            )
            progress.initBar()

        if getDatabaseVersions:
            host = self.db.hostName()
            port = self.db.port()
            user = self.db.userName()
            password = self.db.password()
            for database in dbList:
                try:
                    with self.db.ephemeral_connection(
                        host, port, database, user, password
                    ) as conn:
                        with conn.cursor() as cur:
                            cur.execute(self.gen.getGeometryTablesCount())
                            row = cur.fetchone()
                            if row and row[0] > 0:
                                try:
                                    cur.execute(
                                        self.gen.getEDGVVersionAndImplementationVersion()
                                    )
                                    for vrow in cur.fetchall():
                                        version = vrow[0]
                                        implVersion = vrow[1]
                                        if version:
                                            edvgDbList.append(
                                                (database, version, implVersion)
                                            )
                                        else:
                                            edvgDbList.append(
                                                (database, "Non_EDGV", -1)
                                            )
                                except Exception as ve:
                                    err = str(ve)
                                    if "42501" in err:
                                        # user may have some privileges on database,
                                        # but may not be granted on all schemas
                                        QgsMessageLog.logMessage(
                                            self.tr(
                                                "Unable to load '{0}'. User '{1}'"
                                                " has insufficient privileges."
                                            ).format(database, user),
                                            "DSGTools Plugin",
                                            Qgis.MessageLevel.Warning,
                                        )
                                    else:
                                        edvgDbList.append((database, "Non_EDGV", -1))
                except Exception as e:
                    QgsMessageLog.logMessage(
                        self.tr("Unable to load {0}. Error message: '{1}'").format(
                            database, str(e)
                        ),
                        "DSGTools Plugin",
                        Qgis.MessageLevel.Warning,
                    )
                if parentWidget:
                    progress.step()
        else:
            for database in dbList:
                if database not in [
                    "postgres",
                    "template_edgv_213",
                    "template_edgv_3",
                    "template_edgv_fter_2a_ed",
                    "template0",
                    "template1",
                ]:
                    edvgDbList.append(database)
                if parentWidget:
                    progress.step()
        return edvgDbList

    @ensure_connected
    def getDbsFromServer(self):
        """
        Gets databases from 'this' server
        """
        # Can only be used in postgres database.
        return [row[0] for row in self._fetch_all(self.gen.getDatabasesFromServer())]

    @ensure_connected
    def checkSuperUser(self):
        """
        Checks if the user used to connect to this database is a super user
        """
        row = self._fetch_one(self.gen.isSuperUser(self.db.userName()))
        return row[0] if row else False

    def checkTemplateImplementationVersion(self, edgvVersion=None):
        """
        Returns True if templateSql version is larger than installed template
        Works when abstractDb is connected to the template
        """
        if not edgvVersion:
            edgvVersion = self.getDatabaseVersion()
        templateName = self.getTemplateName(edgvVersion)
        fileImplementationVersion = self.getImplementationVersionFromFile(edgvVersion)
        templateImplementationVersion = self.getImplementationVersion()
        return templateImplementationVersion < fileImplementationVersion

    @ensure_connected
    def dropDatabase(self, candidateName, dropTemplate=False):
        """
        Drops a database from server
        candidataName: database name
        """
        if self.checkSuperUser():
            if dropTemplate:
                self.setDbAsTemplate(dbName=candidateName, setTemplate=False)
            self.dropAllConections(candidateName)
            self._execute_autocommit(self.gen.dropDatabase(candidateName))
        else:
            raise Exception(
                self.tr(
                    "Problem dropping database: user must have permission for that."
                )
            )

    @ensure_connected
    @transactional()
    def createResolvedDomainViews(
        self, createViewClause, fromClause, useTransaction=True
    ):
        """
        Creates a view with all domain values resolved
        createViewClause: sql query to create the view
        fromClause: from sql clause
        """
        if self.checkSuperUser():
            filename = self.getSqlViewFile()
            if filename != None:
                file = codecs.open(filename, encoding="utf-8", mode="r")
                sql = file.read()
                sql = sql.replace("[VIEW]", createViewClause).replace(
                    "[FROM]", fromClause
                )
                file.close()
                commands = [i for i in sql.split("#") if i != ""]
                try:
                    for command in commands:
                        self._execute(command)
                except Exception:
                    raise

    @ensure_connected
    def getSqlViewFile(self):
        """
        Gets the sql view file
        """
        currentPath = os.path.dirname(__file__)
        dbVersion = self.getDatabaseVersion()
        file = None
        if dbVersion == "2.1.3":
            file = os.path.join(
                currentPath,
                "..",
                "..",
                "DbTools",
                "PostGISTool",
                "sqls",
                "213",
                "views_213.sql",
            )
        if dbVersion == "FTer_2a_Ed":
            file = os.path.join(
                currentPath,
                "..",
                "..",
                "DbTools",
                "PostGISTool",
                "sqls",
                "FTer_2a_Ed",
                "views_edgvFter_2a_Ed.sql",
            )
        return file

    @ensure_connected
    def getInvalidGeomRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets invalid geometry data from database
        """
        tableSchema, tableName = self.getTableSchema(cl)
        rows = self._fetch_all(
            self.gen.getInvalidGeom(tableSchema, tableName, geometryColumn, keyColumn)
        )
        return [(row[0], row[1], row[2]) for row in rows]

    @ensure_connected
    @transactional()
    def insertFlags(self, flagTupleList, processName, useTransaction=True):
        """
        Inserts flags into database
        flagTupleList: flag tuple list
        processName: process name
        """
        if len(flagTupleList) > 0:
            try:
                for record in flagTupleList:
                    dimension = self.getDimension(record[3])
                    flagSRID = self.findEPSG(
                        parameters={
                            "tableSchema": "validation",
                            "tableName": "aux_flags_validacao_p",
                            "geometryColumn": "geom",
                        }
                    )
                    try:
                        tableSchema, tableName = record[0].split(".")
                        parameters = {
                            "tableSchema": tableSchema,
                            "tableName": tableName,
                            "geometryColumn": record[4],
                        }
                        srid = self.findEPSG(parameters=parameters)
                    except:
                        srid = flagSRID
                    sql = self.gen.insertFlagIntoDb(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        srid,
                        processName,
                        dimension,
                        record[4],
                        flagSRID,
                    )
                    self._execute(sql)
            except Exception:
                raise
            return len(flagTupleList)
        else:
            return 0

    @ensure_connected
    @transactional()
    def deleteProcessFlags(
        self, processName=None, className=None, flagId=None, useTransaction=True
    ):
        """
        Deletes flags from database
        processName: process name that will have all flags removed
        className: class name that will have all flags removed
        """
        sql = self.gen.deleteFlags(
            processName=processName, className=className, flagId=flagId
        )
        sqlList = sql.split("#")
        for inner in sqlList:
            self._execute(inner)

    @ensure_connected
    @transactional()
    def checkAndCreateValidationStructure(self, useTransaction=True):
        """
        Checks if the validation structure is already created, if not it should be created now
        """
        rows = self._fetch_all(self.gen.checkValidationStructure())
        created = all(row[0] != 0 for row in rows)
        if not created:
            sqltext = self.gen.createValidationStructure(self.findEPSG())
            sqlList = sqltext.split("#")
            try:
                for sql2 in sqlList:
                    self._execute(sql2)
            except Exception:
                raise

    @ensure_connected
    def setValidationProcessStatus(self, processName, log, status):
        """
        Sets the validation status for a specific process
        processName: process name
        """
        self._execute(self.gen.setValidationStatusQuery(processName, log, status))

    @ensure_connected
    def getRunningProc(self):
        """
        Gets the active running process into database
        """
        for row in self._fetch_all(self.gen.getRunningProc()):
            if row[1] == 3:
                return row[0]
        return None

    def isLyrInDb(self, lyr):
        """
        Checks if a layer is in the database
        """
        candidateUri = QgsDataSourceUri(lyr.dataProvider().dataSourceUri())
        candidateHost = candidateUri.host()
        candidatePort = int(candidateUri.port())
        candidateDb = candidateUri.database()
        if (
            self.db.hostName() == candidateHost
            and self.db.port() == candidatePort
            and self.db.databaseName() == candidateDb
        ):
            return True
        else:
            return False

    @ensure_connected
    def testSpatialRule(
        self,
        class_a,
        necessity,
        predicate_function,
        class_b,
        min_card,
        max_card,
        rule,
        aKeyColumn,
        bKeyColumn,
        aGeomColumn,
        bGeomColumn,
    ):
        """
        Tests spatial predicates to check whether a rule is broken
        """
        sql = self.gen.testSpatialRule(
            class_a,
            necessity,
            predicate_function,
            class_b,
            min_card,
            max_card,
            aKeyColumn,
            bKeyColumn,
            aGeomColumn,
            bGeomColumn,
        )
        ret = []
        flagClass = class_a.replace("_temp", "")
        for row in self._fetch_all(sql):
            feat_id = row[0]
            reason = self.tr("Feature id {} from {} violates rule {} {}").format(
                feat_id, class_a, rule.decode("utf-8"), class_b
            )
            geom = row[1]
            ret.append((flagClass, feat_id, reason, geom, aGeomColumn))
        return ret

    @ensure_connected
    def getDimension(self, geom):
        """
        Gets geometry's dimension
        geom: geometry tested
        """
        row = self._fetch_one(self.gen.getDimension(geom))
        return row[0] if row else 0

    @ensure_connected
    def getExplodeCandidates(self, cl):
        """
        Gets multi geometries (i.e number of parts > 1) that will be deaggregated later
        """
        return [row[0] for row in self._fetch_all(self.gen.getMulti(cl))]

    def getURI(self, table, useOnly=True, geomColumn="geom"):
        """
        Gets tabel URI
        table: table name
        useOnly: bool to determine if 'from only' should be used
        geomColumn: geometry column
        """
        schema, layer_name = self.getTableSchema(table)

        host = self.db.hostName()
        port = self.db.port()
        database = self.db.databaseName()
        user = self.db.userName()
        password = self.db.password()

        if useOnly:
            sql = self.gen.loadLayerFromDatabase(table)
        else:
            sql = self.gen.loadLayerFromDatabaseUsingInh(table)

        uri = QgsDataSourceUri()
        uri.setConnection(str(host), str(port), str(database), str(user), str(password))
        id = self.getPrimaryKeyColumn(table)
        uri.setDataSource(schema, layer_name, geomColumn, sql, id)
        uri.disableSelectAtId(True)

        return uri

    def getURIV2(self, tableSchema, tableName, geometryColumnm, sql=""):
        """
        New inplementation giving parameters.
        """
        host = self.db.hostName()
        port = self.db.port()
        database = self.db.databaseName()
        user = self.db.userName()
        password = self.db.password()

        uri = QgsDataSourceUri()
        uri.setConnection(str(host), str(port), str(database), str(user), str(password))
        id = self.getPrimaryKeyColumn("{0}.{1}".format(tableSchema, tableName))
        uri.setDataSource(tableSchema, tableName, geometryColumnm, sql, id)

        return uri

    @ensure_connected
    def getDuplicatedGeomRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets duplicated records
        cl: class to be checked
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        tableSchema, tableName = self.getTableSchema(cl)
        rows = self._fetch_all(
            self.gen.getDuplicatedGeom(
                tableSchema, tableName, geometryColumn, keyColumn
            )
        )
        return [(row[0], row[2]) for row in rows]

    @ensure_connected
    def getSmallAreasRecords(self, cl, tol, geometryColumn, keyColumn):
        """
        Gets duplicated records
        cl: class to be checked
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        tableSchema, tableName = self.getTableSchema(cl)
        rows = self._fetch_all(
            self.gen.getSmallAreas(
                tableSchema, tableName, tol, geometryColumn, keyColumn
            )
        )
        return [(row[0], row[1]) for row in rows]

    @ensure_connected
    def getSmallLinesRecords(self, classesWithGeom, tol, geometryColumn, keyColumn):
        """
        Gets small lines records
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        smallLinesDict = dict()
        for cl in classesWithGeom:
            tableSchema, tableName = self.getTableSchema(cl)
            sql = self.gen.getSmallLines(
                tableSchema, tableName, tol, geometryColumn, keyColumn
            )
            for row in self._fetch_all(sql):
                smallLinesDict = self.utils.buildNestedDict(
                    smallLinesDict, [cl, row[0]], row[1]
                )
        return smallLinesDict

    @ensure_connected
    @transactional()
    def getVertexNearEdgesRecords(
        self,
        tableSchema,
        tableName,
        tol,
        geometryColumn,
        keyColumn,
        geomType,
        useTransaction=True,
    ):
        """
        Gets vertexes near edges. These vertexes are problematic and should be treated
        tableSchema: table schema
        tableName: table name
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        result = []
        sql = self.gen.prepareVertexNearEdgesStruct(
            tableSchema, tableName, geometryColumn, keyColumn, geomType
        )
        sqlList = sql.split("#")
        try:
            for sql2 in sqlList:
                self._execute(sql2)
            parameters = {
                "tableSchema": tableSchema,
                "tableName": tableName,
                "geometryColumn": geometryColumn,
            }
            epsg = self.findEPSG(parameters=parameters)
            sql = self.gen.getVertexNearEdgesStruct(
                epsg, tol, geometryColumn, keyColumn
            )
            for row in self._fetch_all(sql):
                result.append((row[0], row[1]))
        except Exception:
            raise
        return result

    @ensure_connected
    @transactional()
    def removeFeatures(self, cl, processList, keyColumn, useTransaction=True):
        """
        Removes features from class
        cl: class name
        processList: list of dictionaries (id and geometry column)
        keyColumn: pk column
        """
        tableSchema, tableName = self.getTableSchema(cl)
        idList = [i["id"] for i in processList]
        sql = self.gen.deleteFeatures(tableSchema, tableName, idList, keyColumn)
        try:
            self._execute(sql)
        except Exception:
            raise
        return len(idList)

    @ensure_connected
    def getNotSimpleRecords(self, cl, geometryColumn, keyColumn):
        """
        Gets not simple geometries records
        classesWithGeom: class list
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        tableSchema, tableName = self.getTableSchema(cl)
        rows = self._fetch_all(
            self.gen.getNotSimple(tableSchema, tableName, geometryColumn, keyColumn)
        )
        return [(row[0], row[1]) for row in rows]

    @ensure_connected
    def getOutOfBoundsAnglesRecords(
        self, tableSchema, tableName, tol, geometryColumn, geomType, keyColumn
    ):
        """
        Gets records with anchor points (points between segments) that are out of bounds (i.e outside a limit tolerance)
        tableSchema: table schema
        tableName: table name
        tol: tolerance
        geometryColumn: geometryColumn
        keyColumn: pk column
        """
        rows = self._fetch_all(
            self.gen.getOutofBoundsAngles(
                tableSchema, tableName, tol, geometryColumn, geomType, keyColumn
            )
        )
        return [(row[0], row[1]) for row in rows]

    @ensure_connected
    @transactional()
    def forceValidity(self, cl, processList, keyColumn, useTransaction=True):
        """
        Forces geometry validity (i.e uses ST_MakeValid)
        cl: class
        processList: list of dictionaries (id and geometry column)
        keyColumn: pk column
        """
        tableSchema, tableName = self.getTableSchema(cl)
        idList = [i["id"] for i in processList]
        geometryColumn = processList[0]["geometry_column"]
        parameters = {
            "tableSchema": tableSchema,
            "tableName": tableName,
            "geometryColumn": geometryColumn,
        }
        srid = self.findEPSG(parameters=parameters)
        sql = self.gen.forceValidity(
            tableSchema, tableName, idList, srid, keyColumn, geometryColumn
        )
        try:
            self._execute(sql)
        except Exception:
            raise
        return len(idList)

    @ensure_connected
    def getTableExtent(self, tableSchema, tableName):
        """
        Forces geometry validity (i.e uses ST_MakeValid)
        cl: class
        idList: feature ids to be processed
        """
        row = self._fetch_one(self.gen.getTableExtent(tableSchema, tableName))
        if row:
            return (row[0], row[1], row[2], row[3])
        return None

    @ensure_connected
    def getOrphanGeomTables(self, loading=False):
        """
        Gets parent classes
        """
        return [
            row[0]
            for row in self._fetch_all(
                self.gen.getOrphanGeomTablesWithElements(loading)
            )
        ]

    @ensure_connected
    def getOrphanGeomTablesWithElements(self, loading=False):
        """
        Gets populated parent classes
        """
        result = []
        for row in self._fetch_all(self.gen.getOrphanGeomTablesWithElements(loading)):
            orphanCandidate = row[0]
            for row2 in self._fetch_all(
                self.gen.getOrphanTableElementCount(orphanCandidate)
            ):
                if row2[0]:
                    result.append(row[0])
        return result

    @ensure_connected
    @transactional()
    def updateGeometries(
        self, tableSchema, tableName, tuplas, epsg, useTransaction=True
    ):
        """
        Updates geometries on database
        tableSchema: table schema
        tableName: table name
        tuplas: tuples used during the update
        epsg: geometry srid
        """
        sqls = self.gen.updateOriginalTable(tableSchema, tableName, tuplas, epsg)
        sqlDel = self.gen.deleteFeaturesNotIn(
            tableSchema, tableName, list(tuplas.keys())
        )
        try:
            for sql in sqls:
                self._execute(sql)
            self._execute(sqlDel)
        except Exception:
            raise

    @ensure_connected
    def getWhoAmI(self, cl, id):
        """
        Gets relation name (relname) from pg_class
        cl: class with schema
        id: table oid
        """
        row = self._fetch_one(self.gen.getWhoAmI(cl, id))
        return row[0] if row else None

    @ensure_connected
    def getDbOID(self):
        row = self._fetch_one(self.gen.getDbOID(self.db.databaseName()))
        return row[0] if row else None

    @ensure_connected
    @transactional()
    def snapToGrid(self, classList, tol, srid, geometryColumn, useTransaction=True):
        """
        Snaps tables to grid (i.e executes ST_SnapToGrid)
        classList: classes to be altered
        tol: tolerance
        geometryColumn: geometryColumn
        """
        try:
            for cl in classList:
                self._execute(self.gen.snapToGrid(cl, tol, srid, geometryColumn))
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def snapLinesToFrame(
        self,
        classList,
        frameTable,
        tol,
        geometryColumn,
        keyColumn,
        frameGeometryColumn,
        useTransaction=True,
    ):
        """
        Snaps lines to frame. This means the lines are prolonged to the frame according to the specified tolerance
        classList: classes to be altered
        tol: tolerance
        geometryColumn: line geometry column
        keyColumn: line ok column
        frameGeometryColumn: frame geometry column
        """
        for cl in classList:
            sqls = self.gen.snapLinesToFrame(
                cl, frameTable, tol, geometryColumn, keyColumn, frameGeometryColumn
            )
            for sql in sqls.split("#"):
                self._execute(sql)

    @ensure_connected
    @transactional()
    def densifyFrame(
        self,
        classList,
        frameTable,
        snapTolerance,
        geometryColumn,
        frameGeometryColumn,
        useTransaction=True,
    ):
        """
        Densifies the frame creating new vertexes where the lines were snapped
        classList: classes to be altered
        """
        try:
            for cl in classList:
                self._execute(
                    self.gen.densifyFrame(
                        cl,
                        frameTable,
                        snapTolerance,
                        geometryColumn,
                        frameGeometryColumn,
                    )
                )
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def recursiveSnap(
        self, classList, tol, geometryColumn, keyColumn, useTransaction=True
    ):
        """
        Executes a recursive snap within the class
        classList: classes to be snapped
        tol: tolerance
        """
        try:
            self._execute(self.gen.makeRecursiveSnapFunction(geometryColumn, keyColumn))
            for cl in classList:
                self._execute(self.gen.executeRecursiveSnap(cl, tol))
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def runQuery(self, sql, errorMsg, params, useTransaction=True):
        try:
            rows = self._fetch_all(sql)
            result = dict()
            key = ",".join(params)
            result[key] = [list(row[: len(params)]) for row in rows]
            return result
        except Exception as e:
            raise Exception(errorMsg + str(e))

    @ensure_connected
    @transactional()
    def createTempTable(self, tableName, geomColumnName, useTransaction=True):
        try:
            for s in self.gen.createTempTable(tableName).split("#"):
                self._execute(s)
            self._execute(self.gen.createSpatialIndex(tableName, geomColumnName))
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def dropTempTable(self, tableName, useTransaction=True):
        try:
            self._execute(self.gen.dropTempTable(tableName))
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def createStyleTable(self, useTransaction=True):
        try:
            self._execute(self.gen.createStyleTable())
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def checkAndCreateStyleTable(self, useTransaction=True):
        row = self._fetch_one(self.gen.checkStyleTable())
        created = row[0] if row else False
        if not created:
            try:
                self._execute(self.gen.createStyleTable())
            except Exception:
                raise
        return created

    @ensure_connected
    def getStylesFromDb(self, dbVersion):
        sql = self.gen.getStylesFromDb(dbVersion)
        if not sql:
            return []
        return [row[0] for row in self._fetch_all(sql)]

    @ensure_connected
    def getStyle(self, styleName, table_name, parsing=True):
        row = self._fetch_one(self.gen.getStyle(styleName, table_name))
        qml = row[0] if row else None
        if parsing and qml:
            qml = self.utils.parseStyle(qml)
        if qml:
            tempPath = os.path.join(os.path.dirname(__file__), "temp.qml")
            with open(tempPath, "w") as f:
                f.writelines(qml)
            return tempPath
        return None

    @ensure_connected
    @transactional()
    def updateStyle(self, styleName, table_name, qml, tableSchema, useTransaction=True):
        try:
            parsedQml = self.utils.parseStyle(qml)
            self._execute(
                self.gen.updateStyle(styleName, table_name, parsedQml, tableSchema)
            )
        except Exception:
            raise

    @ensure_connected
    @transactional()
    def deleteStyle(self, styleName, useTransaction=True):
        try:
            self._execute(self.gen.deleteStyle(styleName))
        except Exception:
            raise

    @ensure_connected
    def getTableSchemaFromDb(self, table):
        row = self._fetch_one(self.gen.getTableSchemaFromDb(table))
        return row[0] if row else None

    @ensure_connected
    def getLayersWithElementsV2(self, layerList, useInheritance=False):
        lyrWithElemList = []
        for layer in layerList:
            if isinstance(layer, dict):
                schema = layer["tableSchema"]
                lyr = layer["tableName"]
            else:
                if "." in layer:
                    schema, lyr = layer.replace('"', "").split(".")
                else:
                    lyr = layer
                    schema = self.getTableSchemaFromDb(lyr)
            sql = self.gen.getElementCountFromLayerV2(schema, lyr, useInheritance)
            try:
                row = self._fetch_one(sql)
            except Exception:
                QgsMessageLog.logMessage(
                    self.tr("Unable to read table {schema}.{table}").format(
                        schema=schema, table=lyr
                    ),
                    "DSGTools Plugin",
                    Qgis.MessageLevel.Warning,
                )
                continue
            if row is not None and row[0] > 0:
                lyrWithElemList.append(lyr)
        return lyrWithElemList

    @ensure_connected
    def countElements(self, layers):
        listaQuantidades = []
        for layer in layers:
            (schema, className) = self.getTableSchema(layer)
            if layer.split("_")[-1].lower() in ["p", "l", "a"] or schema == "complexos":
                sql = self.gen.getElementCountFromLayer(layer)
                row = self._fetch_one(sql)
                if row is None:
                    raise Exception(
                        self.tr("Problem counting elements: ") + layer
                    )
                listaQuantidades.append([layer, row[0]])
        return listaQuantidades

    @ensure_connected
    def findEPSG(self, parameters=None):
        parameters = dict() if parameters is None else parameters
        sql = self.gen.getSrid(parameters=parameters)
        row = self._fetch_one(sql)
        return row[0] if row else -1

    @ensure_connected
    def getImplementationVersion(self):
        sql = self.gen.getImplementationVersion()
        row = self._fetch_one(sql)
        if row is None:
            raise Exception(
                self.tr("Problem getting implementation version.")
            )
        return row[0]

    @ensure_connected
    def implementationVersion(self):
        sql = self.gen.implementationVersion()
        try:
            row = self._fetch_one(sql)
        except Exception:
            return ""
        if row is None or row[0] is None:
            return ""
        return row[0]

    @ensure_connected
    def insertFrame(self, scale, mi, inom, frame, paramDict=dict()):
        from qgis.core import QgsCoordinateReferenceSystem

        srid = self.findEPSG()
        geoSrid = (
            QgsCoordinateReferenceSystem(int(srid)).geographicCrsAuthId().split(":")[-1]
        )
        sql = self.gen.insertFrame(
            scale, mi, inom, frame, srid, geoSrid, paramDict=paramDict
        )
        self._execute(sql)
        self.db.commit()

    @ensure_connected
    def getQmlRecordDict(self, inputLayer):
        if isinstance(inputLayer, list):
            sql = self.gen.getQmlRecords(inputLayer)
        else:
            sql = self.gen.getQmlRecords([inputLayer])
        rows = self._fetch_all(sql)
        if not rows:
            raise Exception(
                self.tr("Problem getting qmlRecordDict.")
            )
        qmlDict = dict()
        for row in rows:
            if isinstance(inputLayer, list):
                qmlDict[row[0]] = row[1]
            else:
                return row[1]
        return qmlDict

    @ensure_connected
    def getAllStylesDict(self, perspective="style"):
        """
        Returns a dict of styles in a form acording to perspective:
            if perspective = 'style'    : [styleName][dbName][tableName] = timestamp
            if perspective = 'database' : [dbName][styleName][tableName] = timestamp
        """
        styleDict = dict()
        for row in self._fetch_all(self.gen.getAllStylesFromDb()):
            dbName = row[0]
            styleName = row[1]
            tableName = row[2]
            timestamp = row[3]
            if perspective == "style":
                styleDict = self.utils.buildNestedDict(
                    styleDict, [styleName, dbName, tableName], timestamp
                )
            elif perspective == "database":
                styleDict = self.utils.buildNestedDict(
                    styleDict, [dbName, styleName, tableName], timestamp
                )
        return styleDict

    @ensure_connected
    @transactional()
    def runSqlFromFile(self, sqlFilePath, useTransaction=True, encoding="utf-8"):
        with codecs.open(sqlFilePath, encoding=encoding, mode="r") as f:
            sql = f.read()
        try:
            self._execute(sql)
        except Exception:
            raise

    @ensure_connected
    def getGeomSchemaList(self):
        return [row[0] for row in self._fetch_all(self.gen.getGeometricSchemas())]

    @ensure_connected
    def getGeomDict(self, geomTypeDict, insertCategory=False) -> GeomDictResult:
        """
        Returns geometry metadata for all tables in the database.

        Returns a :class:`GeomDictResult` with two perspectives:

        * ``primitivePerspective`` — the ``geomTypeDict`` passed by the caller
          (primitive type → list of layer names).
        * ``tablePerspective`` — ``{layerName: GeomTableEntry}`` mapping with
          schema, srid (native int), geometry column/type and EDGV category.
        """
        edgvVersion = self.getDatabaseVersion()
        result = GeomDictResult(primitivePerspective=geomTypeDict)
        for row in self._fetch_all(self.gen.getGeomTablesFromGeometryColumns()):
            srid = row[0]
            geometryColumn = row[1]
            geometryType = row[2]
            tableSchema = row[3]
            tableName = row[4]
            layerName = tableName
            if geometryColumn == "centroid":
                parts = layerName.split("_")
                parts[-1] = "c"
                layerName = "_".join(parts)
            if layerName in result.tablePerspective:
                continue
            category = ""
            if insertCategory and edgvVersion != "Non_EDGV":
                category = layerName.split("_")[0]
            result.tablePerspective[layerName] = GeomTableEntry(
                schema=tableSchema,
                srid=srid,
                geometryColumn=geometryColumn,
                geometryType=geometryType,
                tableName=tableName,
                category=category,
            )
        return result

    @ensure_connected
    def getDbDomainDict(
        self, auxGeomDict: GeomDictResult, buildOtherInfo=False
    ) -> dict:
        """
        Returns domain / constraint metadata for all geometry tables.

        Return type is ``Dict[str, TableDomainInfo]``: a mapping from table
        name to a :class:`TableDomainInfo` whose ``columns`` attribute maps
        each FK column name to a :class:`ColumnDomainInfo`.

        Example structure::

            {
                'adm_posto_fiscal_a': TableDomainInfo(columns={
                    'operacional': ColumnDomainInfo(
                        references='"dominios"."operacional"',
                        refPk='code', otherKey='code_name',
                        values={1: 'Sim', 2: 'Não'},
                        constraintList=[1, 2],
                        isMulti=False, nullable=False,
                    ),
                    ...
                }),
                ...
            }
        """
        checkConstraintDict = self.getCheckConstraintDict()
        notNullDict = self.getNotNullDictV2()
        multiDict = self.getMultiColumnsDict()
        result: dict = {}

        for row in self._fetch_all(self.gen.getGeomTablesDomains()):
            (
                tableName,
                fkAttribute,
                domainTable,
                domainReferencedAttribute,
            ) = self.parseFkQuery(row[0], row[1])
            if tableName not in result:
                result[tableName] = TableDomainInfo()
            if fkAttribute in result[tableName].columns:
                continue
            values, otherKey = self.getLayerColumnDict(
                domainReferencedAttribute, domainTable
            )
            constraintList = checkConstraintDict.get(tableName, {}).get(fkAttribute, [])
            nullable = not (
                tableName in notNullDict
                and fkAttribute in notNullDict[tableName]["attributes"]
            )
            isMulti = tableName in multiDict and fkAttribute in multiDict[tableName]
            result[tableName].columns[fkAttribute] = ColumnDomainInfo(
                references=domainTable,
                refPk=domainReferencedAttribute,
                otherKey=otherKey,
                values=values,
                constraintList=constraintList,
                isMulti=isMulti,
                nullable=nullable,
            )

        for tableName, attrs in multiDict.items():
            if tableName not in auxGeomDict.tablePerspective:
                continue
            if tableName not in result:
                result[tableName] = TableDomainInfo()
            for fkAttribute in attrs:
                if fkAttribute in result[tableName].columns:
                    continue
                constraintList = checkConstraintDict.get(tableName, {}).get(
                    fkAttribute, []
                )
                nullable = not (
                    tableName in notNullDict
                    and fkAttribute in notNullDict[tableName]["attributes"]
                )
                result[tableName].columns[fkAttribute] = ColumnDomainInfo(
                    references=None,
                    refPk="code",
                    otherKey="code_name",
                    values={},
                    constraintList=constraintList,
                    isMulti=True,
                    nullable=nullable,
                )

        return result

    @ensure_connected
    def getCheckConstraintDict(self, layerFilter=None):
        """
        returns a dict like this:
        {'asb_dep_abast_agua_a': {
                'finalidade': [2,3,4]
                'construcao': [1,2]
                'situacaofisica': [0,1,2,3,5]
            }
        }
        """
        geomDict = dict()
        for row in self._fetch_all(
            self.gen.getGeomTableConstraints(layerFilter=layerFilter)
        ):
            tableName, attribute, checkList = self.parseCheckConstraintQuery(
                row[0], row[1]
            )
            if tableName not in list(geomDict.keys()):
                geomDict[tableName] = dict()
            geomDict[tableName][attribute] = checkList
        return geomDict

    def parseFkQuery(self, queryValue0, queryValue1):
        if "." in queryValue0:
            splitList = queryValue0.split(".")
            tableName = splitList[1]
        else:
            tableName = queryValue0
        fkText = queryValue1
        fkAttribute = fkText.split(")")[0].replace("FOREIGN KEY (", "")
        subtextList = (
            fkText.split(" REFERENCES ")[-1].replace(" MATCH FULL", "").split("(")
        )
        domainTable = subtextList[0]
        if "." not in domainTable:
            auxDomain = domainTable.replace('"', "")
            domainTable = '''"{0}"."{1}"'''.format(
                self.getTableSchemaFromDb(auxDomain), auxDomain
            )
        domainReferencedAttribute = subtextList[1].replace(")", "")
        return (
            tableName.replace('"', ""),
            fkAttribute.replace('"', ""),
            domainTable,
            domainReferencedAttribute,
        )

    def parseCheckConstraintQuery(self, queryValue0, queryValue1):
        try:
            if "ANY" in queryValue1 or "@" in queryValue1:
                return self.parseCheckConstraintWithAny(queryValue0, queryValue1)
            else:
                return self.parseCheckConstraintWithOr(queryValue0, queryValue1)
        except Exception as e:
            raise Exception(
                self.tr("Error parsing check constraint!\n" + ":".join(e.args))
            )

    def parseCheckConstraintWithOr(self, queryValue0, queryValue1):
        if "." in queryValue0:
            query0Split = queryValue0.split(".")
            tableSchema = query0Split[0]
            tableName = query0Split[1]
        else:
            tableName = queryValue0
        query1Split = (
            queryValue1.replace("CHECK ", "")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
            .replace('"', "")
            .split("OR")
        )
        checkList = []
        for i in query1Split:
            attrSplit = i.split("=")
            attribute = attrSplit[0]
            try:
                checkList.append(int(attrSplit[1]))
            except:
                pass  # ignore checks that are not from dsgtools
        return tableName, attribute, checkList

    def parseCheckConstraintWithAny(self, queryValue0, queryValue1):
        # Handle table name parsing
        tableName = queryValue0.split(".")[-1] if "." in queryValue0 else queryValue0

        # Define SQL type castings to remove
        sql_type_castings = [
            "::smallint",
            "::bigint",
            "::integer",
            "::character varying",
            "::varchar",
            "::text",
            "::numeric",
            "::boolean",
            "::timestamp",
            "::date",
            "::time",
            "::interval",
        ]

        # Define SQL keywords and symbols to remove
        sql_tokens = [
            "ANY",
            "ARRAY",
            "CHECK",
            "(",
            ")",
            "[",
            "]",
            '"',
        ]

        # Clean the query string
        cleaned_query = queryValue1

        # Remove SQL type castings
        for casting in sql_type_castings:
            cleaned_query = cleaned_query.replace(casting, "")

        # Remove other SQL tokens
        for token in sql_tokens:
            cleaned_query = cleaned_query.replace(token, "")

        # Determine the split token
        split_tokens = ["=", "<@", "@>", "<>", "!=", "~", "~*", "!~", "!~*"]
        split_token = next(
            (token for token in split_tokens if token in cleaned_query), "="
        )

        # Split the query into attribute and values
        attribute, values = [part.strip() for part in cleaned_query.split(split_token)]

        # Process the check list
        checkList = [val.strip().strip("'") for val in values.split(",")]

        # Try to convert values to integers if possible
        try:
            checkList = list(map(int, checkList))
        except ValueError:
            pass

        return tableName, attribute, checkList

    @ensure_connected
    def getMultiColumnsDict(self, layerFilter=None):
        """
        { 'table_name':[-list of columns-] }
        """
        if layerFilter:
            sql = self.gen.getMultiColumnsFromTableList(layerFilter)
        else:
            sql = self.gen.getMultiColumns(schemaList=self.getGeomSchemaList())
        geomDict = dict()
        for row in self._fetch_all(sql):
            aux = self._as_json(row[0])
            geomDict[aux["table_name"]] = aux["attributes"]
        return geomDict

    @ensure_connected
    def getTablesJsonList(self):
        return [
            self._as_json(row[0])
            for row in self._fetch_all(self.gen.getTablesJsonList())
        ]

    @ensure_connected
    def getGeomTypeDict(self, loadCentroids=False):
        geomDict = dict()
        for row in self._fetch_all(self.gen.getGeomByPrimitive()):
            aux = self._as_json(row[0])
            geomDict[aux["geomtype"]] = aux["classlist"]
        return geomDict

    @ensure_connected
    def getGeomColumnDict(self):
        """
        Dict in the form 'geomName':[-list of table names-]
        """
        geomDict = dict()
        for row in self._fetch_all(self.gen.getGeomColumnDict()):
            aux = self._as_json(row[0])
            if aux["f2"] not in list(geomDict.keys()):
                geomDict[aux["f2"]] = []
            geomDict[aux["f2"]].append(aux["f1"])
        return geomDict

    @ensure_connected
    def getGeomColumnTupleList(
        self,
        showViews=False,
        primitiveFilter=None,
        withElements=False,
        layerFilter=None,
    ):
        """
        list in the format [(table_schema, table_name, geometryColumn, geometryType, tableType)]
        """
        primitiveFilter = [] if primitiveFilter is None else primitiveFilter
        layerFilter = [] if layerFilter is None else layerFilter

        rows = self._fetch_all(self.gen.getGeomColumnTupleList(showViews=showViews))
        localList = [(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        if not withElements and primitiveFilter == []:
            return localList
        if withElements:
            listWithElements = self.getLayersWithElementsV2(
                [{"tableSchema": i[0], "tableName": i[1]} for i in localList]
            )
            geomList = [i for i in localList if i[1] in listWithElements]
        else:
            geomList = localList
        if primitiveFilter != []:
            geomTypeFilter = []
            if "p" in primitiveFilter:
                geomTypeFilter.append("POINT")
                geomTypeFilter.append("MULTIPOINT")
            if "l" in primitiveFilter:
                geomTypeFilter.append("LINESTRING")
                geomTypeFilter.append("MULTILINESTRING")
            if "a" in primitiveFilter:
                geomTypeFilter.append("POLYGON")
                geomTypeFilter.append("MULTIPOLYGON")
            geomList = [i for i in geomList if i[3] in geomTypeFilter]
        return geomList

    def getGeomColumnDictV2(
        self,
        showViews=False,
        primitiveFilter=[],
        withElements=False,
        excludeValidation=False,
    ):
        geomList = self.getGeomColumnTupleList(
            showViews=showViews,
            primitiveFilter=primitiveFilter,
            withElements=withElements,
        )
        edgvVersion = self.getDatabaseVersion()
        lyrDict = dict()
        for tableSchema, tableName, geom, geomType, tableType in geomList:
            if excludeValidation:
                if tableSchema == "validation":
                    continue
            if edgvVersion == "Non_EDGV":
                lyrName = tableName
                cat = tableSchema
            else:
                lyrName = "_".join(tableName.split("_")[1::])
                cat = tableName.split("_")[0]
            key = ",".join([cat, lyrName, geom, geomType, tableType])
            lyrDict[key] = {
                "tableSchema": tableSchema,
                "tableName": tableName,
                "geom": geom,
                "geomType": geomType,
                "tableType": tableType,
                "lyrName": lyrName,
                "cat": cat,
            }
        return lyrDict

    def getAuxInfoDict(self, layerFilter=None):
        """
        Dict with values of check constraint, null values and multi attributes
        """
        return {
            "attributeDomainDict": self.getAttributeDomainDict(layerFilter=layerFilter),
            "checkConstraintDict": self.getCheckConstraintDict(layerFilter=layerFilter),
        }

    @ensure_connected
    def getAttributeDomainDict(self, layerFilter=None):
        attributeDomainDict = defaultdict(lambda: defaultdict(dict))
        for row in self._fetch_all(
            self.gen.getGeomTablesDomains(layerFilter=layerFilter)
        ):
            (
                tableName,
                fkAttribute,
                domainTable,
                domainReferencedAttribute,
            ) = self.parseFkQuery(row[0], row[1])
            newAttrDict = attributeDomainDict[tableName][fkAttribute]
            domainPk = self.getPrimaryKeyColumn(domainTable)
            newAttrDict["references"] = domainTable
            newAttrDict["refPk"] = domainPk
            values, otherKey = self.getLayerColumnDict(domainPk, domainTable)
            newAttrDict["otherKey"] = otherKey
            newAttrDict["values"] = values
            newAttrDict["filterAttr"] = self.getFilter(domainTable, domainPk, otherKey)

        return attributeDomainDict

    def getFilter(self, domainTable, domainPk, otherKey):
        tableSchema, tableName = domainTable.split(".")
        knownColumns = [domainPk, otherKey]
        for row in self._fetch_all(
            self.gen.getAttributesFromTable(tableSchema, tableName)
        ):
            if row[0] not in knownColumns:
                return row[0]
        return None

    def getTableMetadataDict(self, layerFilter=None, showViews=False):
        """
        New method to handle information from database. Must be migrated to new postgisDb
        returns a dict of 'table_name' : {
            'table_name' : --name of the table--,
            'table_schema' : --schema of the table--,
            'primary_key' : --primary key--,
            'geometry_column' : --geometry column--,
            'geometry_type' : --geometry type--,
            'columns' : {
                --name of the column-- : {
                    'name' : --name of the column--,
                    'references' : --fk-- (optional),
                    'refPk' : --reference pk-- (optional),
                    'otherKey' : --domain value-- (optional),
                    'filterAttr' : --if attribute has filter (new feature, optional)--
                    'values' : [--list of values--] (optional),
                    'constraintList' : [--list of constraints--] (optional),
                    'isMulti' : --true or false--,
                    'nullable': --true or false--,
                    'column_type' : --type of the column--
                },
            'sqlFilter' : --
            }
        }
        """
        layerFilter = [] if layerFilter is None else layerFilter
        auxInfoDict = self.getAuxInfoDict(layerFilter)
        metadataDict = defaultdict(lambda: {"columns": defaultdict(dict)})
        for row in self._fetch_all(
            self.gen.getTableMetadataDict(layerFilter=layerFilter)
        ):
            auxDict = self._as_json(row[0])
            newDict = metadataDict[auxDict["table_name"]]
            self.setNewDictTableInfo(newDict, auxDict)
            attrDict = newDict["columns"][auxDict["attr_name"]]
            self.setNewAttrInfo(attrDict, auxDict, auxInfoDict)

        return metadataDict

    def setNewDictTableInfo(self, newDict, auxDict):
        newDict["table_name"] = auxDict["table_name"]
        newDict["table_schema"] = auxDict["table_schema"]
        newDict["primary_key"] = self.getPrimaryKeyColumn(
            ".".join([auxDict["table_schema"], auxDict["table_name"]])
        )
        newDict["geometry_column"] = auxDict["geometry_column"]
        newDict["geometry_type"] = auxDict["geometry_type"]

    def setNewAttrInfo(self, attrDict, auxDict, auxInfoDict):
        attrDict["name"] = auxDict["attr_name"]
        attrDict["nullable"] = auxDict["nullable"]
        attrDict["column_type"] = auxDict["column_type"]
        attrDict["isMulti"] = True if "ARRAY" in auxDict["column_type"] else False
        self.setReferenceInfo(attrDict, auxDict, auxInfoDict["attributeDomainDict"])
        self.setConstraintInfo(attrDict, auxDict, auxInfoDict["checkConstraintDict"])

    def setReferenceInfo(self, attrDict, auxDict, attributeDomainDict):
        if (
            auxDict["table_name"] in attributeDomainDict
            and auxDict["attr_name"] in attributeDomainDict[auxDict["table_name"]]
        ):
            attr_name_dict = attributeDomainDict[auxDict["table_name"]][
                auxDict["attr_name"]
            ]
            attrDict.update(attr_name_dict)

    @ensure_connected
    def getDomainDictFromDomainTable(self, refPk, domainTable, otherKey):
        domainDict = dict()
        for row in self._fetch_all(
            self.gen.getDomainCodeDictWithColumns(domainTable, refPk, otherKey)
        ):
            aux = self._as_json(row[0])
            domainDict.update({aux[refPk]: aux[otherKey]})
        return domainDict

    def setConstraintInfo(self, attrDict, auxDict, checkConstraintDict):
        if (
            auxDict["table_name"] in checkConstraintDict
            and auxDict["attr_name"] in checkConstraintDict[auxDict["table_name"]]
        ):
            attrDict["constraintList"] = checkConstraintDict[auxDict["table_name"]][
                auxDict["attr_name"]
            ]

    def getLayersFilterByInheritance(self, layerList):
        filter = [i.split(".")[-1] for i in self.getOrphanGeomTables(loading=True)]
        filtered = []
        for lyr in layerList:
            clause = lyr["tableName"] if isinstance(lyr, dict) else lyr
            if clause in filter:
                filtered.append(lyr)
        return filtered

    @ensure_connected
    def getNotNullDictV2(self, layerFilter=None):
        """
        Dict in the form 'tableName': { 'schema':-name of the schema'
                                        'attributes':[-list of table names-]}
        """
        notNullDict = dict()
        for row in self._fetch_all(self.gen.getNotNullDict(layerFilter=layerFilter)):
            aux = self._as_json(row[0])
            if aux["f1"] not in list(notNullDict.keys()):
                notNullDict[aux["f1"]] = dict()
            notNullDict[aux["f1"]]["schema"] = aux["f2"]
            if "attributes" not in list(notNullDict[aux["f1"]].keys()):
                notNullDict[aux["f1"]]["attributes"] = []
            notNullDict[aux["f1"]]["attributes"] = aux["f3"]
        return notNullDict

    @ensure_connected
    def getDomainDictV2(self, domainTable):
        domainDict = dict()
        for row in self._fetch_all(self.gen.getDomainDict(domainTable)):
            aux = self._as_json(row[0])
            domainDict[aux["f2"]] = aux["f1"]
        return domainDict

    @ensure_connected
    def getLayerColumnDict(self, refPk, domainTable):
        domainDict = dict()
        otherKey = None
        for row in self._fetch_all(self.gen.getDomainCodeDict(domainTable)):
            aux = self._as_json(row[0])
            if not otherKey:
                if "code_name" in list(aux.keys()):
                    otherKey = "code_name"
                else:
                    otherKey = [key for key in list(aux.keys()) if key != refPk][0]
            domainDict[aux[refPk]] = aux[otherKey]
        return domainDict, otherKey

    @ensure_connected
    def getGeomStructDict(self):
        """
        Returns dict in the following format:
        {'tableName': { 'attrName1':isNullable, 'attrName2':isNullable} }
        """
        yesNoDict = {"YES": True, "NO": False}
        geomStructDict = dict()
        for row in self._fetch_all(self.gen.getGeomStructDict()):
            aux = self._as_json(row[0])
            tableName = aux["table_name"]
            if tableName not in list(geomStructDict.keys()):
                geomStructDict[tableName] = dict()
            for d in aux["array_agg"]:
                geomStructDict[tableName][d["f1"]] = yesNoDict[d["f2"]]
        return geomStructDict

    @ensure_connected
    def createDbFromTemplate(self, dbName, templateName, parentWidget=None):
        # check if created, if created prompt if drop is needed
        if parentWidget:
            progress = ProgressWidget(
                1,
                2,
                self.tr("Creating database {0} from template {1}... ").format(
                    dbName, templateName
                ),
                parent=parentWidget,
            )
            progress.initBar()
        self.dropAllConections(templateName)
        if parentWidget:
            progress.step()
        self._execute_autocommit(self.gen.createFromTemplate(dbName, templateName))
        self.checkAndCreateStyleTable()
        # this close is to allow creation from template
        self.db.close()
        if parentWidget:
            progress.step()

    @ensure_connected
    def getViewDefinition(self, viewName):
        row = self._fetch_one(self.gen.getViewDefinition(viewName))
        return row[0] if row else None

    @ensure_connected
    @transactional()
    def updateDbSRID(
        self,
        srid,
        useTransaction=True,
        closeAfterUse=True,
        parentWidget=None,
        threading=False,
    ):
        tableDictList = self.getParentGeomTables(getDictList=True, showViews=False)
        viewList = [
            '''"{0}"."{1}"'''.format(i["tableSchema"], i["tableName"])
            for i in list(self.getGeomColumnDictV2(showViews=True).values())
            if i["tableType"] == "VIEW"
        ]
        viewDefinitionDict = {i: self.getViewDefinition(i) for i in viewList}

        if parentWidget:
            progress = ProgressWidget(
                1,
                2 * len(viewList) + len(tableDictList),
                self.tr("Updating SRIDs from {0}... ").format(self.db.databaseName()),
                parent=parentWidget,
            )
            progress.initBar()
        try:
            for view in viewList:
                viewSql = self.gen.dropView(view)
                self._execute(viewSql)
                if parentWidget:
                    progress.step()
            for tableDict in tableDictList:
                self._execute(self.gen.updateDbSRID(tableDict, srid))
                if parentWidget:
                    progress.step()
            for viewName in viewList:
                createViewSql = self.gen.createViewStatement(
                    viewName, viewDefinitionDict[viewName]
                )
                self._execute(createViewSql)
                if parentWidget:
                    progress.step()
        except Exception:
            raise
        # this close is to allow creation from template
        if closeAfterUse:
            self.db.close()

    @ensure_connected
    def checkTemplate(self, version=None):
        if not version:
            version = self.getDatabaseVersion()
        dbName = self.getTemplateName(version)
        for row in self._fetch_all(self.gen.checkTemplate()):
            if row[0] == dbName:
                return True
        return False

    @ensure_connected
    def createTemplateDatabase(self, version):
        """
        version: edgv version
        creates an empty database with the name of a template
        """
        dbName = self.getTemplateName(version)
        try:
            self.dropDatabase(dbName)
        except:
            pass
        self.createDatabase(dbName)

    @ensure_connected
    def createDatabase(self, dbName):
        """
        Creates a database with a given name
        """
        self._execute_autocommit(self.gen.getCreateDatabase(dbName))

    def getTemplateName(self, version):
        if version == "2.1.3":
            return "template_edgv_213"
        elif version == "2.1.3 Pro" or version == "EDGV 2.1.3 Pro":
            return "template_edgv_213_pro"
        elif version == "FTer_2a_Ed":
            return "template_edgv_fter_2a_ed"
        elif version in ("3.0", "EDGV 3.0"):
            return "template_edgv_3"
        elif version in ("EDGV 3.0 Pro", "3.0 Pro"):
            return "template_edgv_3_pro"
        elif version in ("EDGV 3.0 Topo", "3.0 Topo"):
            return "template_edgv_3_topo"
        elif version in ("EDGV 3.0 Orto", "3.0 Orto"):
            return "template_edgv_3_orto"

    @ensure_connected
    @transactional()
    def setDbAsTemplate(
        self, version=None, dbName=None, setTemplate=True, useTransaction=True
    ):
        if not dbName:
            dbName = self.getTemplateName(version)
        sql = self.gen.setDbAsTemplate(dbName, setTemplate)
        try:
            self._execute(sql)
        except Exception as e:
            raise Exception(self.tr("Problem setting database as template: ") + str(e))

    @ensure_connected
    def checkIfTemplate(self, dbName):
        sql = self.gen.checkIfTemplate(dbName)
        row = self._fetch_one(sql)
        if row:
            return row[0]

    def getCreationSqlPath(self, version):
        currentPath = os.path.dirname(__file__)
        edgvPath = ""
        if version == "2.1.3":
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "213",
                "edgv213.sql",
            )
        elif version == "2.1.3 Pro" or version == "EDGV 2.1.3 Pro":
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "213_Pro",
                "edgv213_pro.sql",
            )
        elif version == "FTer_2a_Ed":
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "FTer_2a_Ed",
                "edgvFter_2a_Ed.sql",
            )
        elif version in ("3.0", "EDGV 3.0"):
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "3",
                "edgv3.sql",
            )
        elif version in ("3.0 Pro", "EDGV 3.0 Pro"):
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "3_Pro",
                "edgv3_pro.sql",
            )
        elif version in ("3.0 Topo", "EDGV 3.0 Topo"):
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "3_Topo",
                "edgv3_topo.sql",
            )
        elif version in ("3.0 Orto", "EDGV 3.0 Orto"):
            edgvPath = os.path.join(
                currentPath,
                "..",
                "..",
                "..",
                "core",
                "DbModels",
                "PostGIS",
                "3_Orto",
                "edgv3_orto.sql",
            )
        return edgvPath

    def getCommandsFromFile(self, edgvPath, epsg=None):
        """
        Gets all sql commands from file
        """
        file = codecs.open(edgvPath, encoding="utf-8", mode="r")
        sql = file.read()
        if epsg:
            sql = sql.replace("[epsg]", str(epsg))
        file.close()
        commands = sql.split("#")
        return commands

    def getImplementationVersionFromFile(self, edgvVersion):
        edgvPath = self.getCreationSqlPath(edgvVersion)
        commands = self.getCommandsFromFile(edgvPath)
        searchString = (
            "INSERT INTO public.db_metadata (edgvversion, dbimplversion) VALUES ("
        )
        for command in commands:
            if searchString in command:
                return (
                    command.split(searchString)[-1]
                    .split(",")[1]
                    .replace(")", "")
                    .replace("'", "")
                )

    @ensure_connected
    @transactional()
    def setStructureFromSql(
        self, version, epsg, useTransaction=True, closeAfterUsage=True
    ):
        edgvPath = self.getCreationSqlPath(version)
        commands = [i for i in self.getCommandsFromFile(edgvPath, epsg=epsg) if i != ""]
        try:
            for command in commands:
                command = command.strip()
                if command:
                    self._execute(command)
        except Exception as e:
            raise Exception(
                self.tr("Error on database creation! ")
                + str(e)
                + self.tr(" Db will be dropped.")
            )
        self.alterSearchPath(version, useTransaction=useTransaction)
        self.setDbAsTemplate(version=version, useTransaction=useTransaction)
        self.createStyleTable(useTransaction=useTransaction)
        # this close is to allow creation from template
        if closeAfterUsage:
            self.db.close()

    @ensure_connected
    @transactional()
    def alterSearchPath(self, version, useTransaction=True):
        dbName = self.db.databaseName()
        sql = self.gen.alterSearchPath(dbName, version)
        self._execute(sql)

    def createFrame(self, type, scale, param, paramDict=dict()):
        mi, inom, frame = self.prepareCreateFrame(type, scale, param)
        self.insertFrame(scale, mi, inom, frame.asWkb(), paramDict=paramDict)
        return frame

    @ensure_connected
    def getUsersFromServer(self):
        sql = self.gen.getUsersFromServer()
        rows = self._fetch_all(sql)
        return [(row[0], row[1]) for row in rows]

    @ensure_connected
    def reassignAndDropUser(self, user):
        sql = self.gen.reasignAndDropUser(user)
        try:
            self._execute(sql)
        except Exception as e:
            raise Exception(self.tr("Problem removing user: ") + user + "\n" + str(e))

    @ensure_connected
    @transactional()
    def removeFeatureFlags(self, layer, featureId, processName, useTransaction=True):
        """
        Removes flags for a specific layer, feature id and process name
        layer: layer name
        featureId: feature id
        processName: process name
        """
        sql = self.gen.deleteFeatureFlagsFromDb(layer, str(featureId), processName)
        try:
            self._execute(sql)
        except Exception as e:
            raise Exception(self.tr("Problem deleting flag: ") + str(e))

    @ensure_connected
    @transactional()
    def removeEmptyGeometries(self, layer, geometryColumn, useTransaction=True):
        """
        Removes empty geometries from layer
        layer: layer name
        geometryColumn: geometryColumn
        """
        sql = self.gen.removeEmptyGeomtriesFromDb(layer, geometryColumn)
        try:
            self._execute(sql)
        except Exception as e:
            raise Exception(self.tr("Problem removing empty geometries: ") + str(e))

    @ensure_connected
    def getParamsFromConectedDb(self):
        host = self.db.hostName()
        port = self.db.port()
        user = self.db.userName()
        password = self.db.password()
        return (host, port, user, password)

    @ensure_connected
    def getRolesDict(self):
        """
        Gets a dict with the format: 'dbname':{[-list of roles-]}
        """
        sql = self.gen.getRolesDict()
        rows = self._fetch_all(sql)
        rolesDict = dict()
        for row in rows:
            aux = self._as_json(row[0])
            if aux["dbname"] not in list(rolesDict.keys()):
                rolesDict[aux["dbname"]] = []
            rolesDict[aux["dbname"]].append(aux["rolename"])
        return rolesDict

    @ensure_connected
    def getDomainTables(self):
        """
        Lists all domain tables available.
        """
        sql = self.gen.getDomainTables()
        rows = self._fetch_all(sql)
        return [row[0] for row in rows]

    @ensure_connected
    def getGeometricSchemaList(self):
        """
        Lists all schemas with geometries.
        """
        sql = self.gen.getGeometricSchemaList()
        rows = self._fetch_all(sql)
        return [row[0] for row in rows]

    @ensure_connected
    def getGeometricTableListFromSchema(self, schema):
        """
        Lists all tables with geometries from schema
        """
        sql = self.gen.getGeometricTableListFromSchema(schema)
        rows = self._fetch_all(sql)
        return [row[1] for row in rows]

    @ensure_connected
    def getParentGeomTables(
        self,
        getTuple=False,
        getFullName=False,
        primitiveFilter=[],
        showViews=False,
        getDictList=False,
    ):
        """
        Lists all tables with geometries from schema that are parents.
        """
        layerDictList = self.getGeomColumnDictV2(showViews=showViews)
        geomTables = [i["tableName"] for i in list(layerDictList.values())]
        inhDict = self.getInheritanceDict()

        # final parent list
        parentGeomTables = []
        childList = []
        parentList = []
        for parent in list(inhDict.keys()):
            # parents list
            if parent not in parentList:
                parentList.append(parent)
            # children list
            for child in inhDict[parent]:
                if child not in childList:
                    childList.append(child)

        # we must check tables orphan tables (no parent and no child)
        # if a table like this is a geometry table it should be stored
        for geomTable in geomTables:
            if (
                geomTable not in childList
                and geomTable not in parentList
                and geomTable not in parentGeomTables
            ):
                parentGeomTables.append(geomTable)

        # analyzing only the inheritance information
        for parent in list(inhDict.keys()):
            if parent in geomTables:
                # if a parent is a geometry table but is also a child it should not be stored
                if parent not in childList and parent not in parentGeomTables:
                    parentGeomTables.append(parent)
            else:
                # if the parent is not a geometry table all its children should be stored
                for child in inhDict[parent]:
                    if child not in parentGeomTables:
                        parentGeomTables.append(child)

        # filters in case of filter
        if primitiveFilter != []:
            filterList = [
                i["tableName"]
                for i in list(
                    self.getGeomColumnDictV2(
                        showViews=showViews,
                        primitiveFilter=primitiveFilter,
                    ).values()
                )
            ]
            aux = [i for i in parentGeomTables if i in filterList]
            parentGeomTables = aux
        parentGeomTables.sort()
        if getDictList:
            filteredDictList = [
                i
                for i in list(layerDictList.values())
                if i["tableName"] in parentGeomTables
            ]
            return filteredDictList
        # output types
        if getFullName:
            parentFullList = []
            for parent in parentGeomTables:
                schema = self.getTableSchemaFromDb(parent)
                if schema not in ["views", "validation"] and schema:
                    parentFullList.append(schema + "." + parent)
            return parentFullList
        if not getTuple:
            return [
                i
                for i in parentGeomTables
                if self.getTableSchemaFromDb(i) not in ["views", "validation"]
            ]
        else:
            parentTupleList = []
            for parent in parentGeomTables:
                schema = self.getTableSchemaFromDb(parent)
                if schema not in ["views", "validation"]:
                    parentTupleList.append((schema, parent))
            return parentTupleList

    @ensure_connected
    def getInheritanceDict(self):
        sql = self.gen.getInheritanceDict()
        rows = self._fetch_all(sql)
        inhDict = dict()
        for row in rows:
            aux = self._as_json(row[0])
            inhDict[aux["parentname"]] = aux["childname"]
        return inhDict

    def getInheritanceBloodLine(self, parent, inhDict=None):
        """
        Lists all tables that have parent as an ancestor.
        """
        if not inhDict:
            inhDict = self.getInheritanceDict()
        bloodLine = []
        self.utils.getRecursiveInheritance(parent, bloodLine, inhDict)
        return bloodLine

    @ensure_connected
    def getAttributeListFromTable(self, schema, tableName):
        """
        Lists all attributes from table.
        """
        sql = self.gen.getAttributeListFromTable(schema, tableName)
        rows = self._fetch_all(sql)
        return [row[0] for row in rows]

    @ensure_connected
    def getAttributeJsonFromDb(self):
        sql = self.gen.getAttributeDictFromDb()
        rows = self._fetch_all(sql)
        return [self._as_json(row[0]) for row in rows]

    @ensure_connected
    def getAllDomainValues(self, domainTableList=[]):
        if domainTableList == []:
            domainTableList = self.getDomainTables()
        valueList = []
        for domainTable in domainTableList:
            sql = self.gen.getAllDomainValues(domainTable)
            rows = self._fetch_all(sql)
            for row in rows:
                if row[0] not in valueList:
                    valueList.append(row[0])
        valueList.sort()
        return valueList

    @ensure_connected
    def getInheritanceTreeDict(self):
        inhDict = self.getInheritanceDict()
        layerList = self.listGeomClassesFromDatabase()
        geomTables = [i.split(".")[-1] for i in layerList]
        inhTreeDict = dict()
        for parent in list(inhDict.keys()):
            self.utils.getRecursiveInheritanceTreeDict(parent, inhTreeDict, inhDict)
        blackList = []
        for parent in list(inhTreeDict.keys()):
            otherKeys = [i for i in list(inhTreeDict.keys()) if i != parent]
            for otherKey in otherKeys:
                if inhTreeDict[parent] in list(inhTreeDict[otherKey].values()):
                    if parent not in blackList:
                        blackList.append(parent)
                        break
        for item in blackList:
            inhTreeDict.pop(item)
        childBlackList = []
        self.utils.getAllItemsInDict(inhTreeDict, childBlackList)
        for geomTable in geomTables:
            if geomTable not in childBlackList:
                schema = self.getTableSchemaFromDb(geomTable)
                if schema not in ["views", "validation"]:
                    inhTreeDict[geomTable] = dict()
        r = {"root": inhTreeDict}
        return r

    # def getInheritanceConstraintDict(self):
    #     """
    #     Returns a dict in the form:
    #         {'tableName':{'attributeName': {'tableName','constraintName', 'filter'}
    #             }
    #         }
    #     """
    #     self.checkAndOpenDb()
    #     schemaList = [i for i in self.getGeometricSchemaList() if i not in ['views', 'validation']]
    #     sql = self.gen.getConstraintDict(schemaList)
    #     query = QSqlQuery(sql, self.db)
    #     if not query.isActive():
    #         raise Exception(self.tr("Problem constraint dict from db: ")+query.lastError().text())
    #     inhConstrDict = dict()
    #     while query.next():
    #         queryResult = json.loads(query.value(0))
    #         tableName = queryResult['tablename']
    #         if tableName not in list(inhConstrDict.keys()):
    #             inhConstrDict[tableName] = dict()
    #         defList = queryResult['array_agg']
    #         for value in defList:
    #             constraintName = value['f1']
    #             constraintDef = value['f2']
    #             attrName = constraintName.split('_')[-2]
    #             currTableName = constraintName.split('_'+attrName)[0]
    #             if attrName not in list(inhConstrDict[tableName].keys()):
    #                 inhConstrDict[tableName][attrName] = []
    #             filterDef = self.parseCheckConstraintQuery(constraintName,constraintDef)[-1]
    #             schema = self.getTableSchemaFromDb(currTableName)
    #             currTag = {'schema':schema, 'tableName':currTableName, 'constraintName':constraintName, 'filter':filterDef}
    #             if currTag not in inhConstrDict[tableName][attrName]:
    #                 inhConstrDict[tableName][attrName].append(currTag)
    #     return inhConstrDict

    @ensure_connected
    def getDefaultFromDb(self, schema, tableName, attrName):
        """
        Gets default value from table
        """
        sql = self.gen.getDefaultFromDb(schema, tableName, attrName)
        row = self._fetch_one(sql)
        if row:
            return row[0]

    @ensure_connected
    @transactional()
    def upgradePostgis(self, useTransaction=True):
        updateDict = self.getPostgisVersion()
        if updateDict != dict():
            sql = self.gen.upgradePostgis(updateDict)
            try:
                self._execute(sql)
            except Exception as e:
                raise Exception(self.tr("Problem upgrading postgis: ") + str(e))

    @ensure_connected
    def getPostgisVersion(self):
        sql = self.gen.getPostgisVersion()
        rows = self._fetch_all(sql)
        updateDict = dict()
        for row in rows:
            defaultVersion = row[1]
            installedVersion = row[2]
            if defaultVersion != installedVersion and installedVersion not in [
                "",
                None,
            ]:
                updateDict[row[0]] = {
                    "defaultVersion": defaultVersion,
                    "installedVersion": installedVersion,
                }
        return updateDict

    @ensure_connected
    def checkIfTableExists(self, schema, tableName):
        sql = self.gen.checkIfTableExists(schema, tableName)
        rows = self._fetch_all(sql)
        for row in rows:
            if row[0]:
                return True
        return False

    @ensure_connected
    def getPrimaryKeyColumn(self, tableName):
        sql = self.gen.getPrimaryKeyColumn(tableName)
        row = self._fetch_one(sql)
        if row:
            return row[0]

    @ensure_connected
    def dropAllConections(self, dbName):
        """
        Terminates all database conections
        """
        if self.checkSuperUser():
            sql = self.gen.dropAllConections(dbName)
            try:
                self._execute(sql)
            except Exception as e:
                raise Exception(
                    self.tr("Problem dropping database conections: ") + str(e)
                )

    @ensure_connected
    def getAttributesFromTable(
        self, tableSchema, tableName, typeFilter=[], returnType="list"
    ):
        """
        Gets attributes from "tableSchema"."tableName" according to typeFilter
        """
        sql = self.gen.getAttributesFromTable(
            tableSchema, tableName, typeFilter=typeFilter
        )
        rows = self._fetch_all(sql)
        returnStruct = []
        for row in rows:
            if returnType == "list":
                returnStruct.append(row[0])
            else:
                returnStruct.append({"attrName": row[0], "attrType": row[1]})
        return returnStruct

    @ensure_connected
    def checkAndCreatePostGISAddonsFunctions(self, useTransaction=True):
        """
        Checks if PostGIS Add-ons functions are installed in the PostgreSQL choosed server.
        If not, it creates the functions based on our git submodule (ext_dep folder)
        """
        sql = self.gen.checkPostGISAddonsInstallation()
        rows = self._fetch_all(sql)
        created = all(row[0] != 0 for row in rows)
        if not created:
            current_dir = os.path.dirname(__file__)
            sql_file_path = os.path.join(
                current_dir, "..", "..", "ext_dep", "postgisaddon", "postgis_addons.sql"
            )
            self.runSqlFromFile(sql_file_path, useTransaction)

    @ensure_connected
    @transactional()
    def createAndPopulateCoverageTempTable(self, coverageLayer, useTransaction=True):
        """
        Creates and populates a postgis table with features that compose the coverage layer
        """
        # getting srid from something like 'EPSG:31983'
        srid = coverageLayer.crs().authid().split(":")[-1]
        # complete table name
        tableName = "validation.coverage"
        sql = self.gen.createCoverageTempTable(srid)
        try:
            self._execute(sql)
        except Exception as e:
            raise Exception(self.tr("Problem creating coverage temp table: ") + str(e))
        cursor = self.db.cursor()
        try:
            for feat in coverageLayer.getFeatures():
                featid = feat["featid"]
                classname = feat["classname"]
                if not feat.geometry():
                    continue
                geometry = binascii.hexlify(feat.geometry().asWkb()).decode()
                # psycopg2 parameterised INSERT — %s placeholders, params as tuple
                insertSql = (
                    "INSERT INTO {table} (featid, classname, geom) "
                    "VALUES (%s, %s, ST_SetSRID(ST_Multi(ST_GeomFromWKB(%s::bytea)),{srid}))"
                ).format(table=tableName, srid=srid)
                cursor.execute(
                    insertSql,
                    (featid, classname, psycopg2.Binary(bytes.fromhex(geometry))),
                )
        except Exception as e:
            raise Exception(
                self.tr("Problem populating coverage temp table: ") + str(e)
            )
        indexSql = self.gen.createSpatialIndex(tableName, "geom")
        try:
            cursor.execute(indexSql)
        except Exception as e:
            raise Exception(
                self.tr("Problem creating spatial index on coverage temp table: ")
                + str(e)
            )

    @ensure_connected
    def getGapsAndOverlapsRecords(self, frameTable, geomColumn, useTransaction=True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        # checking for gaps with frame
        invalidCoverageRecordsList = []
        sql = self.gen.checkCoverageForGapsWithFrame(frameTable, geomColumn)
        rows = self._fetch_all(sql)
        reason = self.tr("Gap between the frame layer and coverage layer")
        for row in rows:
            invalidCoverageRecordsList.append((0, reason, row[0]))
        # checking for overlaps in coverage
        invalidCoverageRecordsList += self.getOverlapsRecords(
            "validation.coverage_temp", "geom", "id"
        )
        # checking for inner gaps in coverage
        invalidCoverageRecordsList += self.getGapsRecords(
            "validation.coverage_temp", "geom", "id"
        )
        return invalidCoverageRecordsList

    @ensure_connected
    def getOverlapsRecords(self, table, geomColumn, keyColumn, useTransaction=True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        sql = self.gen.checkCoverageForOverlaps(table, geomColumn, keyColumn)
        rows = self._fetch_all(sql)
        reason = self.tr("Overlap between the features of the layer")
        return [(0, reason, row[0]) for row in rows]

    @ensure_connected
    def fillComboBoxProcessOrClasses(self, filterType=None):
        """
        Returns a list of possible classes or processes
        based on existing flags.
        """
        sql = self.gen.getProcessOrClassFlags(filterType)
        rows = self._fetch_all(sql)
        return [""] + [str(row[0]) for row in rows]

    @ensure_connected
    def createFilteredFlagsViewTable(self, filterType=None, filteredElement=None):
        """
        Cretas a View Table if it doesn't exist and populates it
        with data considering the users selection of filtering
        """
        sql = self.gen.createFilteredFlagsViewTableQuery(filterType, filteredElement)
        self._execute(sql)

    @ensure_connected
    def getGapsRecords(self, table, geomColumn, keyColumn, useTransaction=True):
        """
        Identify gaps and overlaps in the coverage layer
        """
        sql = self.gen.checkCoverageForGaps(table, geomColumn, keyColumn)
        rows = self._fetch_all(sql)
        reason = self.tr("Gap between the features of the layer")
        return [(0, reason, row[0]) for row in rows]

    def getLayerDict(self):
        """
        Returns a dict:
        {'table_schema.table_name (geometryColumn):QgsVectorLayer'}
        """
        lyrDict = dict()
        inputDict = self.getGeomColumnDictV2(excludeValidation=True)
        for key in list(inputDict.keys()):
            uri = self.getURIV2(
                inputDict[key]["tableSchema"],
                inputDict[key]["tableName"],
                inputDict[key]["geom"],
                "",
            )
            lyr = QgsVectorLayer(
                uri.uri(), inputDict[key]["lyrName"], "postgres", False
            )
            outputKey = "{0}.{1} ({2})".format(
                inputDict[key]["tableSchema"],
                inputDict[key]["tableName"],
                inputDict[key]["geom"],
            )
            lyrDict[outputKey] = lyr
        return lyrDict

    @ensure_connected
    def getAttrListWithFilter(self):
        sql = self.gen.getAttrListWithFilter()
        rows = self._fetch_all(sql)
        return [row[0] for row in rows]

    @ensure_connected
    def getAttrFilterDomainJsonList(self, domainNameList):
        jsonDict = dict()
        for domainName in domainNameList:
            sql = self.gen.getFilterJsonList(domainName)
            rows = self._fetch_all(sql)
            jsonDict[domainName] = [self._as_json(row[0]) for row in rows]
        return jsonDict

    @ensure_connected
    def getFilterDict(self):
        """
        returns a dict:
            {
                "tableName": [list of domain tuples]
            }
        """
        sql = self.gen.getGeomTablesDomains()
        rows = self._fetch_all(sql)
        filterDict = dict()
        attrList = self.getAttrListWithFilter()
        jsonDict = self.getAttrFilterDomainJsonList(attrList)
        for row in rows:
            # parse done in parseFkQuery to make code cleaner.
            (
                tableName,
                fkAttribute,
                domainTable,
                domainReferencedAttribute,
            ) = self.parseFkQuery(row[0], row[1])
            if domainTable.split(".")[-1] in attrList:
                filterDict[tableName] = jsonDict[domainTable.split(".")[-1]]
        return filterDict

    @ensure_connected
    def databaseInfo(self):
        """
        Gives information about all tables present in the database. Output is composed by
        schema, layer, geometry column, geometry type and srid, in that order.
        :return: (list of DatabaseLayerInfo) database information.
        """
        sql = self.gen.databaseInfo()
        return [
            DatabaseLayerInfo(
                schema=row[0],
                layer=row[1],
                geomCol=row[2],
                geomType=row[3],
                srid=row[4],
            )
            for row in self._fetch_all(sql)
        ]
