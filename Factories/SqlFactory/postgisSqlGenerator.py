# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from DsgTools.Factories.SqlFactory.sqlGenerator import SqlGenerator

class PostGISSqlGenerator(SqlGenerator):
    def getComplexLinks(self, complex):
        sql = "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = "+complex
        return sql

    def getComplexTablesFromDatabase(self):
        sql = "select distinct table_name from information_schema.columns where table_schema = 'complexos'  ORDER BY table_name"
        return sql

    def getComplexData(self, complex_schema, complex):
        sql = "SELECT id, nome from "+complex_schema+"."+complex
        return sql

    def getAssociatedFeaturesData(self, aggregated_schema, aggregated_class, column_name, complex_uuid):
        sql = "SELECT id from only "+aggregated_schema+"."+aggregated_class+" where "+column_name+"="+'\''+complex_uuid+'\''
        return sql

    def getLinkColumn(self, complexClass, aggregatedClass):
        sql = "SELECT column_name from complex_schema where complex = "+complexClass+" and aggregated_class = "+'\''+aggregatedClass+'\''
        return sql

    def getSrid(self):
        sql = "SELECT srid from geometry_columns WHERE f_table_schema <> \'tiger\' and f_table_schema <> \'topology\'"
        return sql

    def getTablesFromDatabase(self):
        sql = "select distinct table_schema, table_name from information_schema.columns where (table_schema <> \'dominios\' and table_schema <> \'topology\')"
        return sql

    def disassociateComplexFromComplex(self, aggregated_class, link_column, uuid):
        sql = "UPDATE complexos."+aggregated_class+" SET "+link_column+"=NULL WHERE id = "+'\''+uuid+'\''
        return sql

    def getTemplates(self):
        sql = "SELECT datname FROM pg_database WHERE datistemplate = true;"
        return sql

    def allowConnections(self, name):
        sql = "ALTER DATABASE "+name+" SET search_path = public, topology, cb, cc, complexos, ct;"
        return sql

    def loadLayerFromDatabase(self, layer_name):
        sql = "id in (SELECT id FROM ONLY "+layer_name+")"
        return sql

    def getCreateDatabase(self, name):
        sql = "CREATE DATABASE "+name
        return sql

    def insertFrameIntoTable(self, wkt):
        sql = "INSERT INTO aux_moldura_a(geom) VALUES(ST_GeomFromText("+wkt+"))"
        return sql

    def getElementCountFromLayer(self, layer):
        sql = "SELECT count(*) FROM ONLY "+layer
        return sql
    
    def getDatabasesFromServer(self):
        sql = "SELECT datname FROM pg_database"
        return sql
    
    def dropDatabase(self, name):
        sql = "DROP DATABASE "+name
        return sql
    
    def createRole(self, roleName, mydict):
        sql = "CREATE ROLE "+roleName+" with NOLOGIN REPLICATION;\n"
        for db in mydict.keys():
            for schema in mydict[db].keys():
                for cat in mydict[db][schema].keys():
                    for table in mydict[db][schema][cat].keys():
                        read = mydict[db][schema][cat][table]["read"]
                        write = mydict[db][schema][cat][table]["write"]
                        if write == '2':
                            sql+='GRANT ALL ON '+table+' TO '+roleName+';\n'
                        elif read == '2':
                            sql+='GRANT SELECT ON '+table+' TO '+roleName+';\n'
                sql += 'GRANT ALL ON SCHEMA '+schema+' TO '+roleName+';\n'
                sql += 'REVOKE CREATE ON SCHEMA '+schema+' FROM '+roleName+';\n'
                sql += 'GRANT USAGE ON SCHEMA '+schema+' TO '+roleName+';\n'
                sql += 'GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA '+schema+' TO '+roleName+';\n'
                sql += 'GRANT USAGE ON ALL SEQUENCES IN SCHEMA '+schema+' TO '+roleName+';\n'
        
        sql += 'GRANT ALL ON ALL TABLES IN SCHEMA information_schema TO '+roleName+';\n'
        sql += 'GRANT ALL ON ALL TABLES IN SCHEMA pg_catalog TO '+roleName+';\n'
        sql += 'GRANT ALL ON SCHEMA information_schema TO '+roleName+';\n'
        sql += 'GRANT ALL ON SCHEMA pg_catalog TO '+roleName+';\n'
        sql += 'REVOKE CREATE ON SCHEMA information_schema FROM '+roleName+';\n'
        sql += 'REVOKE CREATE ON SCHEMA pg_catalog FROM '+roleName+';\n'
        sql += 'GRANT USAGE ON SCHEMA information_schema TO '+roleName+';\n'
        sql += 'GRANT USAGE ON SCHEMA pg_catalog TO '+roleName+';\n'
        sql += 'GRANT USAGE ON ALL SEQUENCES IN SCHEMA information_schema TO '+roleName+';\n'
        sql += 'GRANT USAGE ON ALL SEQUENCES IN SCHEMA pg_catalog TO '+roleName
        return sql

    def dropRole(self, role):
        sql = 'DROP ROLE IF EXISTS '+role
        return sql
    
    def grantRole(self, user, role):
        sql = 'GRANT '+role+' TO '+user
        return sql    