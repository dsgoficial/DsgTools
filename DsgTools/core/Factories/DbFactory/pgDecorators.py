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

import functools
import inspect


def ensure_connected(method):
    """
    Decorator that replaces the repetitive ``self.checkAndOpenDb()`` pattern.

    Before calling the decorated method it checks whether ``self.db`` is open
    and opens it if not.  If the connection cannot be opened it raises a
    RuntimeError with the adapter's last error message, exactly as
    ``checkAndOpenDb`` did.

    Usage::

        @ensure_connected
        def getDatabaseVersion(self):
            ...  # self.db is guaranteed to be open here
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.db.isOpen():
            if not self.db.open():
                raise RuntimeError(
                    self.tr("Error opening database: ") + self.db.lastError().text()
                )
        return method(self, *args, **kwargs)

    return wrapper


def transactional(use_param="useTransaction"):
    """
    Decorator factory that wraps a method in a database transaction when the
    caller passes ``useTransaction=True`` (the default for most callers).

    When ``useTransaction=False`` the method body runs as-is, leaving
    transaction control to the caller (e.g. genericDbManager opens a
    transaction on multiple databases before calling individual methods with
    ``useTransaction=False``).

    Parameters
    ----------
    use_param : str
        Name of the boolean keyword argument that controls whether the
        decorator should manage the transaction.  Defaults to
        ``"useTransaction"`` to match the existing API.

    Usage::

        @ensure_connected
        @transactional()
        def createDb(self, host, port, database, user, password, useTransaction=True):
            ...

        # External caller coordinating across multiple databases:
        abstractDb.db.transaction()
        try:
            abstractDb.createDb(..., useTransaction=False)
            abstractDb.db.commit()
        except Exception:
            abstractDb.db.rollback()
    """

    def decorator(method):
        # Capture the actual default value from the method's signature so that
        # callers who rely on the default (rather than passing the kwarg
        # explicitly) get correct behaviour.  For example, some methods default
        # to ``useTransaction=False`` for coordination with genericDbManager.
        sig = inspect.signature(method)
        param = sig.parameters.get(use_param)
        if param is not None and param.default is not inspect.Parameter.empty:
            param_default = param.default
        else:
            param_default = True  # safe default when parameter is absent

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            use_txn = kwargs.get(use_param, param_default)

            if not use_txn:
                return method(self, *args, **kwargs)

            self.db.transaction()
            try:
                result = method(self, *args, **kwargs)
                self.db.commit()
                return result
            except Exception:
                self.db.rollback()
                raise

        return wrapper

    return decorator
