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
        sql = "SELECT complex_schema, complex, aggregated_schema, aggregated_class, column_name from complex_schema where complex = \'"+complex+'\''
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
        sql = "SELECT column_name from complex_schema where complex = \'"+complexClass+'\''+" and aggregated_class = "+'\''+aggregatedClass+'\''
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

    def loadLayerFromDatabaseUsingInh(self, layer_name):
        sql = "id in (SELECT id FROM "+layer_name+")"
        return sql

    def getCreateDatabase(self, name):
        sql = "CREATE DATABASE "+name
        return sql

    def insertFrameIntoTable(self, wkt):
        sql = "INSERT INTO aux_moldura_a(geom) VALUES(ST_GeomFromText("+wkt+"))"
        return sql

    def getElementCountFromLayer(self, schema, table):
        sql = "SELECT count(id) FROM ONLY {0}.{1} limit 1".format(schema,table)
        return sql

    def getElementCountFromLayerWithInh(self, layer):
        sql = "SELECT count(*) FROM "+layer
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
                        RETURN;
                        
                    END
                $BODY$ LANGUAGE plpgsql;#
            '''
        sql += 'SELECT droprole(\''+role+'\')#'
        sql += 'DROP ROLE IF EXISTS '+role
        return sql
    
    def grantRole(self, user, role):
        sql = 'GRANT '+role+' TO '+user
        return sql
    
    def revokeRole(self, user, role):
        sql = 'REVOKE '+role+' FROM '+user
        return sql
        
    def getRoles(self):
        sql = 'SELECT rolname FROM pg_roles WHERE rolname <> \'postgres\' AND rolcanlogin = \'f\' AND rolname in (select split_part(unnest(nspacl)::text, \'=\', 1) from pg_namespace where nspname = \'pg_catalog\')'
        return sql

    def getUserRelatedRoles(self, username):
        sql =   '''select rolname, usename from 
                    (select * from pg_roles as r where r.rolcanlogin = \'f\' and r.rolname<>\'postgres\') as listaRoles left join 
                    (select * from pg_auth_members as m join pg_user as u on m.member = u.usesysid and u.usename=\'%s\') 
                    as euTenho on euTenho.roleid=listaRoles.oid  where rolname in (select split_part(unnest(nspacl)::text, \'=\', 1) from pg_namespace where nspname = \'pg_catalog\')
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
                'SELECT ' || ccu.column_name || ' FROM dominios.' || ccu.table_name || ' ORDER BY ' || ccu.column_name || ' ASC'
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                            ON ccu.constraint_name = tc.constraint_name
                WHERE constraint_type = 'FOREIGN KEY' and tc.constraint_schema in (%s)''' % schemas
        return sql
    
    def getTableDomains(self,tableList):
        schemas = '\''+'\',\''.join(schemaList)+'\''
        sql = '''SELECT
                tc.table_schema,tc.table_name, kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                'SELECT ' || ccu.column_name || ' FROM dominios.' || ccu.table_name || ' ORDER BY ' || ccu.column_name || ' ASC'
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
        elif edgvVersion == 'FTer_2a_Ed':
            sql = 'SELECT table_schema, table_name, column_name FROM INFORMATION_SCHEMA.COLUMNS where table_schema in (\'ge\',\'pe\',\'complexos\',\'public\')'
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
    
    def getRolePrivileges(self, role, dbname):
        sql = 'SELECT * FROM information_schema.role_table_grants where grantee = \'%s\' and table_catalog = \'%s\' ORDER BY table_name' % (role, dbname)
        return sql
    
    def isSuperUser(self,user):
        sql = 'SELECT rolsuper FROM pg_roles WHERE rolname = \'%s\'' % user 
        return sql

    def getInvalidGeom(self, tableSchema, tableName):
        return "select  f.id as id,(reason(ST_IsValidDetail(f.geom,0))), (location(ST_IsValidDetail(f.geom,0))) as geom from (select id, geom from only %s.%s  where ST_IsValid(geom) = 'f') as f" % (tableSchema,tableName)
    
    def getNonSimpleGeom(self, tableSchema, tableName):
        return "select  f.id as id,(reason(ST_IsValidDetail(f.geom,0))), (location(ST_IsValidDetail(f.geom,0))) as geom from (select id, geom from only %s.%s  where ST_IsSimple(geom) = 'f') as f" % (tableSchema,tableName)
    
    def checkValidationStructure(self):
        return "select count(*) from information_schema.columns where table_name = 'aux_flags_validacao'"

    def createValidationStructure(self, srid):
        sql = """CREATE SCHEMA IF NOT EXISTS validation#
        CREATE TABLE validation.aux_flags_validacao (
            id serial NOT NULL,
            process_name varchar(200) NOT NULL,
            layer varchar(200) NOT NULL,
            feat_id smallint NOT NULL,
            reason varchar(200) NOT NULL,
            user_fixed boolean NOT NULL DEFAULT FALSE,
            dimension smallint NOT NULL,
            CONSTRAINT aux_flags_validacao_pk PRIMARY KEY (id)
             WITH (FILLFACTOR = 100)
        )#
        
        CREATE TABLE validation.aux_flags_validacao_p (
            geom geometry(MULTIPOINT, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_p_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#
        
        CREATE TABLE validation.aux_flags_validacao_l (
            geom geometry(MULTILINESTRING, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_l_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#
        
        CREATE TABLE validation.aux_flags_validacao_a (
            geom geometry(MULTIPOLYGON, %s) NOT NULL,
            CONSTRAINT aux_flags_validacao_a_pk PRIMARY KEY (id)
        )INHERITS(validation.aux_flags_validacao)#
        
        CREATE TABLE validation.status
        (
          id smallint NOT NULL,
          status character varying(200) NOT NULL,
          CONSTRAINT status_pk PRIMARY KEY (id)
        )#
        CREATE TABLE validation.process_history (
            id serial NOT NULL,
            process_name varchar(200) NOT NULL,
            log text NOT NULL,
            status int NOT NULL,
            finished timestamp NOT NULL default now(),
            CONSTRAINT process_history_pk PRIMARY KEY (id),
            CONSTRAINT process_history_status_fk FOREIGN KEY (status) REFERENCES validation.status (id) MATCH FULL ON UPDATE NO ACTION ON DELETE NO ACTION
        
        )#
        CREATE TABLE validation.settings(
            id serial NOT NULL,
            scale character varying(10),
            tolerance float,
            earthcoverage text,
            CONSTRAINT settings_pk PRIMARY KEY (id)
        )#
        INSERT INTO validation.settings(earthcoverage) VALUES (NULL)#
        INSERT INTO validation.status(id,status) VALUES (0,'Not yet ran'), (1,'Finished'), (2,'Failed'), (3,'Running'), (4,'Finished with flags')   
        """ % (srid, srid, srid)
        return sql
    
    def validationStatus(self, processName):
        sql = "SELECT status FROM validation.process_history where process_name = '%s' ORDER BY finished DESC LIMIT 1; " % processName
        return sql
    
    def validationStatusText(self, processName):
        sql = "SELECT sta.status FROM validation.process_history as hist left join validation.status as sta on sta.id = hist.status where hist.process_name = '%s' ORDER BY hist.finished DESC LIMIT 1 " % processName
        return sql
    
    def setValidationStatusQuery(self, processName,log,status):
        sql = "INSERT INTO validation.process_history (process_name, log, status) values ('%s','%s',%s)" % (processName,log,status)
        return sql
    
    def insertFlagIntoDb(self,layer,feat_id,reason,geom,srid,processName, dimension):
        sql = ''
        if dimension == 0:
            sql = "INSERT INTO validation.aux_flags_validacao_p (process_name, layer, feat_id, reason, geom, dimension) values ('%s','%s',%s,'%s',ST_SetSRID(ST_Multi('%s'),%s), %s);" % (processName, layer, str(feat_id), reason, geom, srid, dimension)
        elif dimension == 1:
            sql = "INSERT INTO validation.aux_flags_validacao_l (process_name, layer, feat_id, reason, geom, dimension) values ('%s','%s',%s,'%s',ST_SetSRID(ST_Multi('%s'),%s), %s);" % (processName, layer, str(feat_id), reason, geom, srid, dimension)
        elif dimension == 2:
            sql = "INSERT INTO validation.aux_flags_validacao_a (process_name, layer, feat_id, reason, geom, dimension) values ('%s','%s',%s,'%s',ST_SetSRID(ST_Multi('%s'),%s), %s);" % (processName, layer, str(feat_id), reason, geom, srid, dimension)
        return sql
    
    def getRunningProc(self):
        sql = "SELECT process_name, status FROM validation.process_history ORDER BY finished DESC LIMIT 1;"
        return sql
    
    def deleteFlags(self, processName):
        sql = """
        DELETE FROM validation.aux_flags_validacao_p 
        WHERE id in 
        (SELECT id FROM validation.aux_flags_validacao_p where process_name = '%s')#
        
        DELETE FROM validation.aux_flags_validacao_l 
        WHERE id in 
        (SELECT id FROM validation.aux_flags_validacao_l where process_name = '%s')#

        DELETE FROM validation.aux_flags_validacao_a 
        WHERE id in 
        (SELECT id FROM validation.aux_flags_validacao_a where process_name = '%s')
        """ % (processName, processName, processName)
        return sql
    
    def testSpatialRule(self, class_a, necessity, predicate_function, class_b, min_card, max_card):
        if predicate_function == 'ST_Disjoint':
            if class_a!=class_b:
                sameClassRestriction=''
            else:
                sameClassRestriction=' WHERE a.id <> b.id '
                    
            if necessity == '\'f\'':
                sql = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.id id, SUM(CASE WHEN %s(a.geom,b.geom) = 'f' THEN 1 ELSE 0 END) count, a.geom geom 
                    FROM %s as a,%s as b %s GROUP BY a.id) as foo
                WHERE foo.count > 0
                """% (predicate_function, class_a, class_b, sameClassRestriction)
                
            elif necessity == '\'t\'':
                sql = """SELECT DISTINCT foo.id, foo.geom FROM
                (SELECT a.id id, SUM(CASE WHEN %s(a.geom,b.geom) = 'f' THEN 1 ELSE 0 END) count, a.geom geom 
                    FROM %s as a,%s as b %s GROUP BY a.id) as foo
                WHERE foo.count = 0
                """% (predicate_function, class_a, class_b, sameClassRestriction)
        else:
            if necessity == '\'f\'':# must (be)
                if class_a!=class_b:
                    sameClassRestriction=''
                else:
                    sameClassRestriction=' WHERE a.id <> b.id '
                
                if max_card == '*':
                    sql = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.id id, SUM(CASE WHEN %s(a.geom,b.geom) THEN 1 ELSE 0 END) count, a.geom geom 
                        FROM %s as a,%s as b %s GROUP BY a.id) as foo
                    WHERE foo.count < %s
                    """ % (predicate_function, class_a, class_b, sameClassRestriction, min_card)
                else:
                    sql = """SELECT DISTINCT foo.id, foo.geom FROM
                    (SELECT a.id id, SUM(CASE WHEN %s(a.geom,b.geom) THEN 1 ELSE 0 END) count, a.geom geom 
                        FROM %s as a,%s as b %s GROUP BY a.id) as foo
                    WHERE foo.count < %s OR foo.count > %s
                    """ % (predicate_function, class_a, class_b, sameClassRestriction, min_card, max_card)
            elif necessity == '\'t\'':# must not (be)
                if class_a!=class_b:
                    sameClassRestriction=''
                else:
                    sameClassRestriction=' AND a.id <> b.id '
                
                sql = """SELECT DISTINCT a.id id, ST_Intersection(a.geom, b.geom) as geom
                FROM %s as a, %s as b 
                    WHERE %s(a.geom,b.geom) = %s %s
                """ % (class_a, class_b, predicate_function, necessity, sameClassRestriction)
        return sql
    
    def getDimension(self, geom):
        sql = "select ST_Dimension('%s')" % geom
        return sql
    
    def getMulti(self,cl):
        sql = "select id from only %s where ST_NumGeometries(geom) > 1" % cl
        return sql

    def getDuplicatedGeom(self,schema,cl):
        sql = """select * from (
        SELECT id,
        ROW_NUMBER() OVER(PARTITION BY geom ORDER BY id asc) AS Row,
        geom FROM ONLY %s.%s 
        ) dups
        where     
        dups.Row > 1""" % (schema,cl)
        return sql
    
    def getSmallAreas(self,schema,cl,areaTolerance):
        sql = """select  foo2.id, foo2.geom from (
        select id, geom, ST_Area(geom) as area from %s.%s 
        ) as foo2 where foo2.area < %s order by foo2.id""" % (schema,cl,areaTolerance)
        return sql
    
    def getSmallLines(self,schema,cl,areaTolerance):
        sql = """select  foo2.id, foo2.geom from (
        select id, geom, ST_Length(geom) as len from %s.%s 
        ) as foo2 where len < %s order by foo2.id""" % (schema,cl,areaTolerance)
        return sql
    
    def prepareVertexNearEdgesStruct(self, tableSchema, tableName):
        sql = """drop table if exists seg#
        create temp table seg as (
        SELECT segments.id as id, ST_MakeLine(sp,ep) as geom
        FROM
           (SELECT
              ST_PointN(geom, generate_series(1, ST_NPoints(geom)-1)) as sp,
              ST_PointN(geom, generate_series(2, ST_NPoints(geom)  )) as ep,
              linestrings.id as id
            FROM
              (SELECT id as id, (ST_Dump(ST_Boundary(geom))).geom
               FROM only {0}.{1} 
               ) AS linestrings
            ) AS segments)#
        drop table if exists pontos#
        create temp table pontos as select id as id, (ST_DumpPoints(geom)).geom as geom from only {0}.{1}#
        create index pontos_gist on pontos using gist (geom)#
        create index seg_gist on seg using gist (geom)""".format(tableSchema, tableName)
        return sql

    def getVertexNearEdgesStruct(self, epsg, tol):
        sql = """select pontos.id, ST_SetSRID(pontos.geom,{0}) as geom from pontos, seg where ST_DWithin(seg.geom, pontos.geom, {1}) and ST_Distance(seg.geom, pontos.geom) > 0""".format(epsg,tol)
        return sql
    
    def deleteFeatures(self,schema,table,idList):
        sql = """DELETE FROM %s.%s 
        WHERE id in (%s)""" %(schema,table,','.join(idList))
        return sql
    
    def deleteFeaturesNotIn(self,schema,table,idList):
        sql = """DELETE FROM %s.%s 
        WHERE id not in (%s)""" %(schema,table,','.join(map(str,idList)))
        return sql        
    
    def getNotSimple(self, tableSchema, tableName):
        sql = """select foo.id as id, ST_MULTI(st_startpoint(foo.geom)) as geom from (
        select id as id, (ST_Dump(ST_Node(ST_SetSRID(ST_MakeValid(geom),ST_SRID(geom))))).geom as geom from {0}.{1}  
        where ST_IsSimple(geom) = 'f') as foo where st_equals(st_startpoint(foo.geom),st_endpoint(foo.geom))""".format(tableSchema, tableName)
        return sql

    def getOutofBoundsAngles(self, tableSchema, tableName, angle):
        if tableName.split('_')[-1] == 'l':
            sql = """
            WITH result AS (SELECT points.id, points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN(geom, generate_series(1, ST_NPoints(geom)-2)) as pt1,
                              ST_PointN(geom, generate_series(2, ST_NPoints(geom)-1)) as anchor,
                              ST_PointN(geom, generate_series(3, ST_NPoints(geom))) as pt2,
                              linestrings.id as id
                            FROM
                              (SELECT id as id, (ST_Dump(geom)).geom as geom
                               FROM only {0}.{1}
                               ) AS linestrings WHERE ST_NPoints(linestrings.geom) > 2 ) as points)
            select distinct id, anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))""".format(tableSchema, tableName, angle)
        elif  tableName.split('_')[-1] == 'a':
            sql = """
            WITH result AS (SELECT points.id, points.anchor, (degrees
                                        (
                                            ST_Azimuth(points.anchor, points.pt1) - ST_Azimuth(points.anchor, points.pt2)
                                        )::decimal + 360) % 360 as angle
                        FROM
                        (SELECT
                              ST_PointN(geom, generate_series(1, ST_NPoints(geom)-1)) as pt1,
                              ST_PointN(geom, generate_series(1, ST_NPoints(geom)-1) %  (ST_NPoints(geom)-1)+1) as anchor,
                              ST_PointN(geom, generate_series(2, ST_NPoints(geom)) %  (ST_NPoints(geom)-1)+1) as pt2,
                              linestrings.id as id
                            FROM
                              (SELECT id as id, ST_Boundary((ST_Dump(ST_ForceRHR(geom))).geom) as geom
                               FROM only {0}.{1}
                               ) AS linestrings WHERE ST_NPoints(linestrings.geom) > 2 ) as points)
            select distinct id, anchor, angle from result where (result.angle % 360) < {2} or result.angle > (360.0 - ({2} % 360.0))""".format(tableSchema, tableName, angle)
        return sql
    
    def getFlagsByProcess(self, processName):
        sql = """select layer, feat_id from validation.aux_flags_validacao where process_name = '%s'""" % processName
        return sql
    
    def forceValidity(self, tableSchema, tableName, idList, srid):
        sql = """update {0}.{1} set geom = ST_Multi(result.geom) from (
        select distinct parts.id, ST_Union(parts.geom) as geom from {0}.{1} as source, 
                                        (select id as id, ST_Multi(((ST_Dump(ST_SetSRID(ST_MakeValid(geom), {3}))).geom)) as geom from 
                                        {0}.{1}  where id in ({2})) as parts where ST_GeometryType(parts.geom) = ST_GeometryType(source.geom) group by parts.id
        ) as result where  result.id = {0}.{1}.id""".format(tableSchema,tableName,','.join(idList),srid)
        return sql
    
    def getTableExtent(self, tableSchema, tableName):
        sql = """
        SELECT ST_XMin(ST_Extent(geom)), ST_XMax(ST_Extent(geom)), ST_YMin(ST_Extent(geom)), ST_YMax(ST_Extent(geom)) AS extent FROM {}.{}
        """.format(tableSchema, tableName)
        return sql
    
    def getOrphanGeomTablesWithElements(self,loading = False):
        if not loading:
            sql = """
            select pgcl2.sc || '.' || pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid) 
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ('ge','pe', 'cb') and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union 
            select distinct gc.f_table_schema || '.' || p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid 
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and 
                gc.f_table_schema in ('cb', 'pe', 'ge')
            
            order by tb
            """
        else:
            sql = """
            select pgcl2.sc || '.' || pgcl2.n as tb from pg_class as pgcl
                left join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                left join pg_namespace as pgnsp on pgcl.relnamespace = pgnsp.oid
                left join pg_inherits as pginh on pginh.inhparent = pgcl.oid
                join (select pgcl.oid, pgmsp.nspname as sc, pgcl.relname as n from pg_class as pgcl
                            join (select * from pg_attribute where attname = 'geom') as pgatt on pgatt.attrelid = pgcl.oid
                            left join pg_namespace pgmsp on pgcl.relnamespace = pgmsp.oid) 
                as pgcl2 on pgcl2.oid = pginh.inhrelid
                where pgnsp.nspname in ('ge','pe', 'cb', 'public') and pgatt.attname IS NULL and pgcl.relkind = 'r'
            union 
            select distinct gc.f_table_schema || '.' || p.relname as tb from pg_class as p
                left join pg_inherits as inh  on inh.inhrelid = p.oid 
                left join geometry_columns as gc on gc.f_table_name = p.relname
                where (inh.inhrelid IS NULL) and 
                gc.f_table_schema in ('cb', 'pe', 'ge', 'public')
            
            order by tb
            """
        return sql
    
    def updateOriginalTable(self, tableSchema, tableName, result, epsg):
        sqls = []
        for key in result.keys():
            geoms = []
            for wkb in result[key]:
                geoms.append("ST_SetSRID(ST_Multi('{0}'), {1})".format(wkb, epsg))
            array = ','.join(geoms)
            union = 'ST_Union(ARRAY[{}])'.format(array)

            sql = """
            UPDATE {0}.{1} SET geom = ST_Multi({2}) WHERE id = {3}
            """.format(tableSchema, tableName, union, key)
            sqls.append(sql)
        return sqls
    
    def getOrphanTableElementCount(self, orphan):
        sql = "select id from %s limit 1" % orphan
        return sql
    
    def checkCentroidAuxStruct(self):
        sql = "select distinct count(column_name) from information_schema.columns where column_name = 'centroid' group by column_name"
        return sql
    
    def dropCentroid(self, table):
        sql = "alter table %s drop column if exists centroid" % table
        return sql
    
    def createCentroidColumn(self, table_schema, table_name, srid):
        sql = """alter table {1}.{2} add column centroid geometry('POINT',{0})#
        alter table {1}.{2} alter column geom drop not null#
        CREATE INDEX {3} ON {1}.{2} USING gist(centroid)""".format(srid,table_schema, table_name,table_name[:-2]+'_c_gist')
        return sql
    
    def createCentroidGist(self, table_schema, table_name):
        gistName = table_name[:-2]+'_c_gist'
        sql = "CREATE INDEX {0} ON {1}.{2} USING gist(centroid)".format(gistName,table_schema,table_name)
        return sql
    
    def getEarthCoverageClasses(self):
        sql = "select distinct table_schema || '.' || table_name from information_schema.columns where column_name = 'centroid'"
        return sql

    def getEarthCoverageDict(self):
        sql = "select earthcoverage from validation.settings limit 1"
        return sql

    def setEarthCoverageDict(self,earthDict):
        if earthDict:
            sql = "update validation.settings set earthcoverage = '%s'" % earthDict
        else:
            sql = "update validation.settings set earthcoverage = NULL"
        return sql
    
    
    def makeRelationDict(self, table, codes):
        sql = 'select code, code_name from dominios.%s where code in %s' % (table, in_clause)
        return sql

    def getEarthCoverageCentroids(self):
        sql = "select distinct table_schema ||'.'|| table_name from information_schema.columns where column_name = 'centroid'"
        return sql
    
    def getWhoAmI(self, cl, id):
        sql = "select p.relname from {0} as c, pg_class as p where c.tableoid = p.oid and c.id = {1}".format(cl,id)
        return sql
    
    def snapLinesToFrame(self, cl, tol):
        schema, table = cl.split('.')
        sql = """
        update {0}.{1} as classe set geom = ST_Multi(agrupado.geom)
        from
            (
                select simplelines.id as id, ST_Union(simplelines.newline) as geom
                from
                (
                    select short.id, St_SetPoint((ST_Dump(short.geom)).geom, 0, 
                    ST_EndPoint(from_start)) as newline
                    from
                    (   select a.id as id, a.geom as geom,
                        ST_ShortestLine(st_startpoint((ST_Dump(a.geom)).geom), 
                        ST_Boundary(m.geom)) as from_start
                        from {0}.{1} a, public.aux_moldura_a m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines.id
            ) as agrupado
        where classe.id = agrupado.id#
        update {0}.{1} as classe set geom = ST_Multi(agrupado.geom)
        from
            (
                select simplelines.id as id, ST_Union(simplelines.newline) as geom
                from
                (
                    select short.id, St_SetPoint((ST_Dump(short.geom)).geom, 
                    short.index - 1, ST_EndPoint(from_start)) as newline
                    from
                    (   select a.id as id, a.geom as geom,
                        ST_ShortestLine(st_endpoint((ST_Dump(a.geom)).geom), 
                        ST_Boundary(m.geom)) as from_start,
                        ST_NPoints((ST_Dump(a.geom)).geom) as index
                        from {0}.{1} a, public.aux_moldura_a m
                    ) as short
                    where ST_Length(from_start) < {2}
                ) as simplelines group by simplelines.id
            ) as agrupado
        where classe.id = agrupado.id        
        """.format(schema, table, str(tol))
        return sql
    
    def densifyFrame(self, cl):
        schema, table = cl.split('.')
        sql = """
        update public.aux_moldura_a m set geom = st_multi(st_snap(m.geom, 
        foo.vertices, 0.0000000001))
        from
        (
            select st_union(st_boundary(a.geom)) as vertices from 
        {0}.{1} a
        ) as foo        
        """.format(schema, table)
        return sql

    def snapToGrid(self, cl, precision, srid):
        sql = 'select id, ST_AsBinary(ST_SetSRID(ST_SnapToGrid(geom,{1}),{2})) as geom from {0}'.format(cl, precision, srid)
        return sql
    
    def makeRecursiveSnapFunction(self):
        sql = """
        CREATE OR REPLACE FUNCTION dsgsnap(tabela text, snap float) RETURNS void AS 
        $BODY$
            DECLARE
            id int;
            BEGIN
                FOR id in execute('select id from '||tabela)
                LOOP
                    EXECUTE     
                'update '||tabela||' as classe set geom = st_multi(res.geom) 
                from 
                    (
                        select st_snap(a.geom, st_collect(b.geom), '||snap||') as geom, a.id as id 
                        from '||tabela||' a, '||tabela||' b 
                        where a.id != b.id and a.id = '||id||' 
                        group by a.id, a.geom
                    ) as res 
                where res.id = classe.id';
                END LOOP;
                RETURN;                        
            END
        $BODY$
        LANGUAGE plpgsql;
        """
        return sql
    
    def executeRecursiveSnap(self, cl, tol):
        sql = 'SELECT dsgsnap(\'{0}\', {1})'.format(cl, str(tol))
        return sql
    
    def createTempTable(self, tableName):
        sql = '''
        DROP TABLE IF EXISTS {0}_temp#
        CREATE TABLE {0}_temp as (select * from {1} where 1=2)
        '''.format(tableName,tableName)
        return sql
    
    def dropTempTable(self, tableName):
        sql = 'DROP TABLE IF EXISTS {0}_temp'.format(tableName)
        return sql
    
    def populateTempTable(self, tableName, attributes, values, geometry, srid):
        columnTupleString = ','.join(map(str,attributes))
        columnTupleString += ',geom'
        valueTupple = []
        for value in values:
            if isinstance(value, str):
                valueTupple.append("'{0}'".format(value))
            else:
                valueTupple.append(value)
        valueTupple.append("ST_SetSRID(ST_Multi('{0}'),{1})".format(geometry,str(srid)))
        valueTuppleString = ','.join(map(str,valueTupple))
        sql = """INSERT INTO {0}_temp({1}) VALUES ({2})""".format(tableName, columnTupleString, valueTuppleString)
        return sql
    
    def createSpatialIndex(self, tableName):
        sql = 'create index {0}_temp_gist on {1}_temp using gist (geom)'.format(tableName.split('.')[-1], tableName)
        return sql
    
    def getStyles(self):
        sql = 'select description, f_table_schema, f_table_name, stylename from public.layer_styles where f_table_catalog = current_database()'
        return sql

    def checkStyleTable(self):
        sql = "select relname from pg_class where relname = 'layer_styles' limit 1"
        return sql
    
    def createStyleTable(self):
        sql = """
        CREATE TABLE public.layer_styles
        (
          id serial NOT NULL,
          f_table_catalog character varying,
          f_table_schema character varying,
          f_table_name character varying,
          f_geometry_column character varying,
          stylename text,
          styleqml text,
          stylesld text,
          useasdefault boolean,
          description text,
          owner character varying(30),
          ui xml,
          update_time timestamp without time zone DEFAULT now(),
          CONSTRAINT layer_styles_pkey PRIMARY KEY (id)
        )
        """
        return sql
    
    def getStylesFromDb(self, dbVersion):
        if dbVersion == '2.1.3':
            sql = """select distinct description from public.layer_styles where f_table_catalog = current_database() and description like 'edgv_213%'"""
        elif dbVersion == 'FTer_2a_Ed':
            sql = """select distinct description from public.layer_styles where f_table_catalog = current_database() and description like 'edgv_FTer_2a_Ed%'"""
        return sql
    
    def getStyle(self, styleName, table_name):
        sql = """SELECT styleqml from public.layer_styles where f_table_name = '{0}' and description = '{1}' and f_table_catalog = current_database()""".format(table_name, styleName)
        return sql
    
    def updateStyle(self, styleName, table_name, parsedQml, tableSchema):
        sql = """UPDATE public.layer_styles SET styleqml = '{0}', update_time = now() where f_table_name = '{1}' and description = '{2}'""".format(parsedQml.replace("'","''"),table_name, styleName)
        return sql
    
    def importStyle(self, styleName, table_name, parsedQml, tableSchema, dbName):
        if table_name[-1] == 'c':
            geomColumn = 'centroid'
        else:
            geomColumn = 'geom'
        sql = """INSERT INTO  public.layer_styles (styleqml, f_table_name, description, f_geometry_column, stylename, f_table_schema, f_table_catalog, useasdefault) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',FALSE)""".format(parsedQml.replace("'","''"), table_name, styleName, geomColumn, styleName.split('/')[-1]+'/'+table_name, tableSchema, dbName)
        return sql
    
    def getTableSchemaFromDb(self, table):
        sql = """select distinct table_schema from information_schema.columns where table_name = '{0}'""".format(table)
        return sql
    
    def getAllStylesFromDb(self):
        sql = """SELECT DISTINCT f_table_catalog, description, f_table_name, update_time from public.layer_styles order by f_table_catalog, description, f_table_name asc """
        return sql
    
    def deleteStyle(self, styleName):
        sql = """delete from public.layer_styles where description = '{0}'""".format(styleName)
        return sql
    
    def getConstraints(self, schemaList):
        sql = """select sch.nspname, cl.relname, c.conname, c.consrc from 
            (
                select * from pg_constraint where contype = 'c'
            ) as c join (
                select oid, nspname from pg_namespace where nspname in ({0})
            ) as sch on sch.oid = c.connamespace
            left join pg_class as cl on c.conrelid = cl.oid
            """.format(','.schemaList)
        return sql
    
    def getGeometricSchemas(self):
        sql = 'select distinct f_table_schema from public.geometry_columns'
        return sql
    
    def getGeomTablesFromGeometryColumns(self):
        sql = 'select srid, f_geometry_column, type, f_table_schema, f_table_name from public.geometry_columns'
        return sql
    
    def getGeomTablesDomains(self, version):
        if version == '2.1.3':
            sql = """SELECT distinct conrelid::regclass as cl, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'f' and conrelid::regclass::text in 
            (select f_table_schema||'.'||f_table_name from public.geometry_columns where f_table_schema <> 'views')"""
        elif version == 'FTer_2a_Ed':
            sql = """SELECT distinct conrelid::regclass as cl, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'f' and conrelid::regclass::text in 
        (select f_table_name from public.geometry_columns f_table_schema <> 'views') """
        return sql
    
    def getGeomTableConstraints(self, version):
        if version == '2.1.3':
            sql = """SELECT distinct conrelid::regclass as cl, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'c' and conrelid::regclass::text in 
            (select f_table_schema||'.'||f_table_name from public.geometry_columns f_table_schema <> 'views')"""
        elif version == 'FTer_2a_Ed':
            sql = """SELECT distinct conrelid::regclass as cl, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'c' and conrelid::regclass::text in 
        (select f_table_name from public.geometry_columns f_table_schema <> 'views') """
        return sql
    
    def getMultiColumns(self, schemaList):
        sql = """select row_to_json(a) from (
                select t.table_name, array_agg(t.column_name::text) as attributes from 
                (select table_name, column_name from information_schema.columns  
                where data_type = 'ARRAY' and table_schema in ({0}) 
                ) as t group by t.table_name
            ) as a
        """.format(','.join(schemaList))
        return sql
    
    def getGeomByPrimitive(self):
        sql = """select row_to_json(a) from (select type as geomtype, array_agg(f_table_name) as classlist from public.geometry_columns group by type) as a"""
        return sql
    
    def getGeomColumnDict(self):
        sql = """select row_to_json(row(f_table_schema||'.'||f_table_name, f_geometry_column)) from public.geometry_columns"""
        return sql
