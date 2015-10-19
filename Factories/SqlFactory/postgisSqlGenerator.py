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
        sql = "SELECT datname FROM pg_database where datname <> \'postgres\' and datname <> \'template\' and datname <> \'template0\' and datname <> \'template_postgis\'"
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
        
        sql += 'GRANT SELECT ON db_metadata TO '+roleName+';\n'
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
        sql = '''CREATE OR REPLACE FUNCTION droprole(name text) RETURNS void AS $BODY$
                    DECLARE
                        s text;
                    BEGIN
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL TABLES IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL FUNCTIONS IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON ALL SEQUENCES IN SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        FOR s in SELECT DISTINCT 'REVOKE ALL ON SCHEMA ' || table_schema || ' FROM ' || name from information_schema.columns
                        LOOP
                            EXECUTE s;
                        END LOOP;
                        EXECUTE 'REVOKE ALL ON db_metadata FROM '|| name;
                        EXECUTE 'DROP ROLE IF EXISTS '||name;
                        RETURN;
                        
                    END
                $BODY$ LANGUAGE plpgsql;#
            '''
        sql += 'SELECT droprole(\''+role+'\')'
        return sql
    
    def grantRole(self, user, role):
        sql = 'GRANT '+role+' TO '+user
        return sql
    
    def revokeRole(self, user, role):
        sql = 'REVOKE '+role+' FROM '+user
        return sql
        
    def getRoles(self):
        sql = 'SELECT rolname FROM pg_roles WHERE rolname <> \'postgres\' AND rolcanlogin = \'f\''
        return sql
    
    def getUserRelatedRoles(self, username):
        sql =   '''select rolname, usename from 
                    (select * from pg_roles as r where r.rolcanlogin = \'f\' and r.rolname<>\'postgres\') as listaRoles left join 
                    (select * from pg_auth_members as m join pg_user as u on m.member = u.usesysid and u.usename=\'%s\') 
                    as euTenho on euTenho.roleid=listaRoles.oid
                ''' % username
        return sql
    
    def getUsers(self):
        sql = 'SELECT usename FROM pg_user WHERE usename <> \'postgres\''
        return sql
    
    def createUser(self,user,password,isSuperuser):
        if isSuperuser:
            sql = 'CREATE ROLE '+user+' WITH SUPERUSER CREATEDB CREATEROLE REPLICATION LOGIN PASSWORD \''+password+'\';'
        else:
            sql = 'CREATE ROLE '+user+' WITH LOGIN PASSWORD \''+password+'\';'
        return sql   
    
    def removeUser(self,user):
        sql = 'DROP ROLE '+user
        return sql 
    
    def alterUserPass(self,user,newPass):
        sql = 'ALTER ROLE '+user+' WITH PASSWORD \''+newPass+'\''
        return sql 
    
    def validateWithDomain(self,schemaList):
        schemas = '\''+'\',\''.join(schemaList)+'\''
        sql = '''SELECT
                tc.table_schema,tc.table_name, kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || ccu.column_name || ' FROM dominios.' || ccu.table_name
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in (%s)''' % schemas
        return sql

    def getNotNullFields(self,schemaList):
        schemas = '\''+'\',\''.join(schemaList)+'\''
        sql = 'select table_schema, table_name, column_name from information_schema.columns where is_nullable = \'NO\' and column_name not in (\'id\',\'geom\') and table_schema in (%s)' % schemas
        return sql 
    
    def getFeaturesWithSQL(self,layer,attrList):
        ls = ','.join(attrList)
        sql = 'SELECT %s FROM ONLY %s' % (ls,layer)
        return sql    
    
    def getStructure(self,edgvVersion):
        sql = ''
        if edgvVersion == '2.1.3':
            sql = 'SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_schema in (\'cb\',\'complexos\',\'public\')'
        return sql
    
    def getAggregationColumn(self):
        sql = 'SELECT DISTINCT column_name FROM public.complex_schema'
        return sql
    
    def getAggregatorFromId(self, className, id):
       sql = 'SELECT id from %s where id =\'%s\'' % (className,id)
       return sql
   
    def getAggregatorFromComplexSchema(self,aggregated,aggregationColumn):
        sql = 'SELECT complex from public.complex_schema where aggregated_class = \'%s\' and aggregationColumn = \'%s\'' % (aggregated,aggregationColumn)
        return sql
    
    def createCustomSort(self):
        sql = '''CREATE OR REPLACE FUNCTION
                      array_sort_dsg(
                        array_vals_to_sort anyarray
                      )
                      RETURNS TABLE (
                        sorted_array anyarray
                      )
                      AS $BODY$
                        BEGIN
                          RETURN QUERY SELECT
                            ARRAY_AGG(val) AS sorted_array
                          FROM
                            (
                              SELECT
                                UNNEST(array_vals_to_sort) AS val
                              ORDER BY
                                val DESC NULLS FIRST
                            ) AS sorted_vals
                          ;
                        END;
                      $BODY$
                    LANGUAGE plpgsql;
                    '''
        return sql