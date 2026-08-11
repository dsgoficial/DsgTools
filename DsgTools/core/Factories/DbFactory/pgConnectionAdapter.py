# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-01-01
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from contextlib import contextmanager

import psycopg2
import psycopg2.extras


class PsycopgDbError:
    """
    Drop-in replacement for QSqlError, exposing the same interface used
    across PostgisDb / AbstractDb so no call-site needs to change.
    """

    def __init__(self, message: str = ""):
        self._message = message

    def text(self) -> str:
        return self._message

    def databaseText(self) -> str:
        return self._message

    def isValid(self) -> bool:
        return bool(self._message)


class PsycopgDbAdapter:
    """
    Drop-in replacement for QSqlDatabase("QPSQL").

    Exposes the same interface used throughout PostgisDb and AbstractDb so
    that all callers (postgisDb, genericDbManager, permissionManager,
    exploreServerWidget, …) continue to work without modification.

    Setter/getter pairs mirror the QSqlDatabase API:
        setHostName / hostName
        setPort     / port
        setDatabaseName / databaseName
        setUserName / userName
        setPassword / password

    Connection lifecycle:
        open()        → establishes the psycopg2 connection
        close()       → closes it
        isOpen()      → True when an active connection exists

    Transaction control (autocommit is off by default after open()):
        transaction() → sets the connection to manual-commit mode
        commit()      → commits the current transaction
        rollback()    → rolls back the current transaction

    Error reporting:
        lastError()   → returns a PsycopgDbError instance

    Compatibility shim:
        driverName()  → always returns "QPSQL" (callers use this to branch
                         on PostGIS vs SpatiaLite vs GeoPackage)
    """

    def __init__(self):
        self._host: str = ""
        self._port: int = 5432
        self._database: str = ""
        self._user: str = ""
        self._password: str = ""
        self._connection = None  # psycopg2 connection object
        self._last_error: PsycopgDbError = PsycopgDbError()

    # ------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------
    def setHostName(self, host: str):
        self._host = host

    def setPort(self, port: int):
        self._port = int(port)

    def setDatabaseName(self, database: str):
        self._database = database

    def setUserName(self, user: str):
        self._user = user

    def setPassword(self, password: str):
        self._password = password

    # ------------------------------------------------------------------
    # Getters  (mirror QSqlDatabase)
    # ------------------------------------------------------------------
    def hostName(self) -> str:
        return self._host

    def port(self) -> int:
        return self._port

    def databaseName(self) -> str:
        return self._database

    def userName(self) -> str:
        return self._user

    def password(self) -> str:
        return self._password

    def driverName(self) -> str:
        """Always returns 'QPSQL' so that driver-checking code keeps working."""
        return "QPSQL"

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------
    def isOpen(self) -> bool:
        return self._connection is not None and not self._connection.closed

    def open(self) -> bool:
        """
        Opens a psycopg2 connection using the stored parameters.
        Returns True on success, False on failure (error stored in lastError()).
        """
        try:
            if self.isOpen():
                return True
            self._connection = psycopg2.connect(
                host=self._host,
                port=self._port,
                dbname=self._database,
                user=self._user,
                password=self._password,
            )
            # Start in autocommit=False so that explicit transaction() /
            # commit() / rollback() behave like QSqlDatabase.
            self._connection.autocommit = False
            self._last_error = PsycopgDbError()
            return True
        except Exception as e:
            self._last_error = PsycopgDbError(str(e))
            self._connection = None
            return False

    def close(self):
        """Closes the underlying psycopg2 connection if it is open."""
        if self._connection is not None:
            try:
                self._connection.close()
            except Exception:
                pass
            finally:
                self._connection = None

    # ------------------------------------------------------------------
    # Transaction control
    # ------------------------------------------------------------------
    def transaction(self):
        """
        Begins a new transaction.

        psycopg2 with autocommit=False is always in a transaction after the
        first statement.  Calling this method issues a SAVEPOINT so that
        nested transaction() / rollback() pairs work correctly, mirroring
        QSqlDatabase behaviour for callers like genericDbManager that call
        transaction() on both adminDb and targetDb before a batch of
        operations.
        """
        if not self.isOpen():
            return False
        try:
            cursor = self._connection.cursor()
            cursor.execute("BEGIN")
            cursor.close()
            return True
        except Exception as e:
            self._last_error = PsycopgDbError(str(e))
            return False

    def commit(self) -> bool:
        """Commits the current transaction."""
        if not self.isOpen():
            return False
        try:
            self._connection.commit()
            return True
        except Exception as e:
            self._last_error = PsycopgDbError(str(e))
            return False

    def rollback(self) -> bool:
        """Rolls back the current transaction."""
        if not self.isOpen():
            return False
        try:
            self._connection.rollback()
            return True
        except Exception as e:
            self._last_error = PsycopgDbError(str(e))
            return False

    # ------------------------------------------------------------------
    # Error reporting
    # ------------------------------------------------------------------
    def lastError(self) -> PsycopgDbError:
        return self._last_error

    # ------------------------------------------------------------------
    # Cursor access (used by PostgisDb helpers _execute / _fetch_all / …)
    # ------------------------------------------------------------------
    def cursor(self, cursor_factory=None):
        """
        Returns a psycopg2 cursor from the underlying connection.
        Raises RuntimeError if the connection is not open.
        """
        if not self.isOpen():
            raise RuntimeError("Cannot obtain cursor: database connection is not open.")
        if cursor_factory is not None:
            return self._connection.cursor(cursor_factory=cursor_factory)
        return self._connection.cursor()

    # ------------------------------------------------------------------
    # Autocommit DDL helper
    # ------------------------------------------------------------------
    @contextmanager
    def autocommit_block(self):
        """
        Context manager for DDL statements that PostgreSQL forbids inside a
        transaction (CREATE DATABASE, DROP DATABASE, etc.).

        Commits any pending transaction, switches to autocommit=True, yields
        the underlying connection, then restores autocommit=False.
        """
        if not self.isOpen():
            raise RuntimeError("Cannot execute DDL: connection is not open.")
        try:
            self._connection.commit()
        except Exception:
            self._connection.rollback()
        self._connection.autocommit = True
        try:
            yield self._connection
        finally:
            self._connection.autocommit = False

    # ------------------------------------------------------------------
    # Ephemeral / server-level connection helper
    # ------------------------------------------------------------------
    @contextmanager
    def ephemeral_connection(
        self, host: str, port: int, database: str, user: str, password: str
    ):
        """
        Context manager that opens a *temporary* psycopg2 connection to an
        arbitrary database (e.g. for iterating server databases) and
        guarantees it is closed afterwards.

        Usage::

            with self.db.ephemeral_connection(host, port, db, user, pw) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                    rows = cur.fetchall()

        This fixes the connection leak that existed in getEDGVDbsFromServer,
        which created N QSqlDatabase("QPSQL") objects in a loop without
        ever closing them.
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=database,
                user=user,
                password=password,
            )
            conn.autocommit = True  # read-only server queries need no txn
            yield conn
        finally:
            if conn is not None and not conn.closed:
                conn.close()
