# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2026-11-05
        copyright            : (C) 2026 by 1st CGEO - Brazilian Army
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

Single place where DSGTools stores and reads database credentials.

The password never goes to QSettings. It is stored as a "Basic"
QgsAuthMethodConfig in the QGIS authentication database (encrypted with the
master password) and QSettings only keeps the reference, under the key
``authcfg``:

    PostgreSQL/servers/<name>/{host, port, username, isDefault, authcfg}
    PostgreSQL/connections/<name>/{database, host, port, username, authcfg}

``authcfg`` is also the key the QGIS PostgreSQL provider reads for its own
connection list, so a connection created by DSGTools opens in the QGIS
browser without a clear text password.

Legacy entries (``password`` key in clear text) are still read, so nothing
breaks, and are migrated: the credential is copied to the authentication
database, read back, tested against the server and only then the clear text
key is removed. If the server does not answer, the clear text key stays and
the migration is tried again later.

Nothing in this module logs, raises or returns a message containing a
password.
"""

import time
from concurrent.futures import ThreadPoolExecutor

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsAuthMethodConfig,
    QgsMessageLog,
)
from qgis.PyQt.QtCore import QSettings

SERVERS_GROUP = "PostgreSQL/servers"
CONNECTIONS_GROUP = "PostgreSQL/connections"
AUTHCFG_KEY = "authcfg"
LEGACY_PASSWORD_KEY = "password"  # nosec B105 (settings key name, not a secret)
AUTH_METHOD = "Basic"
AUTH_NAME_PREFIX = "DSGTools - "
SERVER_TEST_DATABASE = "postgres"
TEST_TIMEOUT_SECONDS = 3
MAX_PARALLEL_TESTS = 8
RETRY_INTERVAL_SECONDS = 300
LOG_TAG = "DSGTools Plugin"

# migration status
MIGRATED = "migrated"
NOTHING_TO_DO = "nothing-to-do"
NOT_DSGTOOLS = "not-created-by-dsgtools"
UNREACHABLE = "connection-test-failed"
STORE_FAILED = "auth-database-unavailable"
PENDING_SERVER = "server-not-migrated-yet"
POSTPONED = "postponed"

# session state (never persisted): entries whose last migration attempt
# failed, and whether the user declined the master password in this session
_lastFailure = {}
_storeDeclined = False
_sweepDone = False


def resetSessionState():
    """
    Forgets the failures and the master password refusal of this session.
    """
    global _storeDeclined, _sweepDone
    _lastFailure.clear()
    _storeDeclined = False
    _sweepDone = False


def _log(message, level=Qgis.MessageLevel.Info):
    QgsMessageLog.logMessage(message, LOG_TAG, level)


def redact(text, *secrets):
    """
    Replaces every secret found in text by ***.
    """
    text = "" if text is None else str(text)
    for secret in secrets:
        if secret:
            text = text.replace(str(secret), "***")
    return text


def _str(value):
    if value is None:
        return ""
    return str(value)


# ---------------------------------------------------------------------------
# QgsAuthManager
# ---------------------------------------------------------------------------
def _authManager():
    authManager = QgsApplication.authManager()
    if authManager is None or authManager.isDisabled():
        return None
    return authManager


def storeCredentials(user, password, name, authcfg=None):
    """
    Stores user and password as a Basic auth config in the QGIS authentication
    database. When authcfg is given and exists, it is updated in place (the
    references to it keep working).
    If the master password is not set, QGIS asks the user to create or enter
    it; if it is cancelled nothing is stored and None is returned: there is
    no clear text fallback.
    :return: (str) authcfg id or None.
    """
    authManager = _authManager()
    if authManager is None:
        return None
    config = QgsAuthMethodConfig(AUTH_METHOD)
    config.setName(AUTH_NAME_PREFIX + _str(name))
    config.setConfig("username", _str(user))
    config.setConfig("password", _str(password))
    if authcfg and authcfg in authManager.configIds():
        config.setId(authcfg)
        ok = authManager.updateAuthenticationConfig(config)
        return authcfg if ok else None
    result = authManager.storeAuthenticationConfig(config)
    ok = result[0] if isinstance(result, tuple) else bool(result)
    if isinstance(result, tuple) and len(result) > 1 and result[1] is not None:
        config = result[1]
    if not ok or not config.id():
        return None
    return config.id()


def loadCredentials(authcfg):
    """
    Reads user and password from a Basic authcfg. Other methods (PKI, OAuth2)
    and a refused master password return (None, None).
    :return: (tuple) (user, password)
    """
    authManager = _authManager()
    if not authcfg or authManager is None:
        return (None, None)
    if authcfg not in authManager.configIds():
        return (None, None)
    if authManager.configAuthMethodKey(authcfg) != AUTH_METHOD:
        return (None, None)
    config = QgsAuthMethodConfig()
    result = authManager.loadAuthenticationConfig(authcfg, config, True)
    ok = result[0] if isinstance(result, tuple) else bool(result)
    if isinstance(result, tuple) and len(result) > 1 and result[1] is not None:
        config = result[1]
    if not ok or not config.isValid(True):
        return (None, None)
    return (config.config("username"), config.config("password"))


def removeCredentials(authcfg):
    """
    Removes an authcfg from the authentication database.
    """
    authManager = _authManager()
    if not authcfg or authManager is None:
        return False
    if authcfg not in authManager.configIds():
        return False
    return bool(authManager.removeAuthenticationConfig(authcfg))


def authcfgReferences(authcfg, ignore=None):
    """
    Lists the QSettings groups (servers and connections) that use authcfg.
    """
    ignore = ignore or []
    references = []
    settings = QSettings()
    for group in (SERVERS_GROUP, CONNECTIONS_GROUP):
        settings.beginGroup(group)
        names = settings.childGroups()
        settings.endGroup()
        for name in names:
            path = "{0}/{1}".format(group, name)
            if path in ignore:
                continue
            if _str(settings.value(path + "/" + AUTHCFG_KEY)) == authcfg:
                references.append(path)
    return references


def authcfgForCredentials(host, port, user, password):
    """
    Finds the authcfg of a DSGTools server or of a QGIS connection that holds
    exactly this credential (same host and port in settings, same user and
    password in the authentication database). It never creates an authcfg
    and never asks for the master password: when the authentication
    database is locked it returns "" and the caller keeps today's behaviour.
    :return: (str) authcfg id or "".
    """
    authManager = _authManager()
    if not password or authManager is None or not authManager.masterPasswordIsSet():
        return ""
    candidates = []
    settings = QSettings()
    for group in (SERVERS_GROUP, CONNECTIONS_GROUP):
        settings.beginGroup(group)
        names = settings.childGroups()
        settings.endGroup()
        for name in names:
            path = "{0}/{1}".format(group, name)
            authcfg = _str(settings.value(path + "/" + AUTHCFG_KEY))
            settingsUser = _str(settings.value(path + "/username"))
            if (
                authcfg
                and authcfg not in candidates
                and _str(settings.value(path + "/host")) == _str(host)
                and _str(settings.value(path + "/port")) == _str(port)
                and settingsUser in ("", _str(user))
            ):
                candidates.append(authcfg)
    for authcfg in candidates:
        storedUser, storedPassword = loadCredentials(authcfg)
        if storedPassword == password and _str(storedUser) == _str(user):
            return authcfg
    return ""


def uriCredentials(uri):
    """
    User and password of a QgsDataSourceUri, resolving authcfg=<id> through
    the authentication database (a layer or connection URI that uses authcfg
    has no password of its own).
    :return: (tuple) (user, password)
    """
    authcfg = uri.authConfigId()
    if authcfg:
        user, password = loadCredentials(authcfg)
        if password is not None:
            return (user or uri.username(), password)
    return (uri.username(), uri.password())


# ---------------------------------------------------------------------------
# connection test
# ---------------------------------------------------------------------------
def testConnection(host, port, database, user, password, timeout=TEST_TIMEOUT_SECONDS):
    """
    Opens and closes a psycopg2 connection with a short timeout.
    :return: (tuple) (bool, str) success and a message without the password.
    """
    import psycopg2

    try:
        conn = psycopg2.connect(
            host=_str(host),
            port=int(port),
            dbname=_str(database),
            user=_str(user),
            password=_str(password),
            connect_timeout=int(timeout),
        )
        conn.close()
        return (True, "")
    except Exception as e:
        firstLine = redact(str(e), password).strip().splitlines()
        return (
            False,
            "{0}: {1}".format(type(e).__name__, firstLine[0] if firstLine else ""),
        )


# ---------------------------------------------------------------------------
# servers
# ---------------------------------------------------------------------------
def serverNames():
    settings = QSettings()
    settings.beginGroup(SERVERS_GROUP)
    names = settings.childGroups()
    settings.endGroup()
    return names


def connectionNames():
    settings = QSettings()
    settings.beginGroup(CONNECTIONS_GROUP)
    names = settings.childGroups()
    settings.endGroup()
    return names


def _readGroup(path, keys):
    settings = QSettings()
    settings.beginGroup(path)
    values = {key: settings.value(key) for key in keys}
    settings.endGroup()
    return values


def hasStoredPassword(path):
    """
    Tells if a settings group has a password (authcfg or legacy) without
    decrypting anything, so listing servers never asks for the master password.
    """
    values = _readGroup(path, [AUTHCFG_KEY, LEGACY_PASSWORD_KEY])
    return bool(_str(values[AUTHCFG_KEY]) or _str(values[LEGACY_PASSWORD_KEY]))


def _resolve(path, settingsUser, withPassword, migrate, migrateFunction):
    values = _readGroup(path, [AUTHCFG_KEY, LEGACY_PASSWORD_KEY])
    authcfg = _str(values[AUTHCFG_KEY])
    legacy = _str(values[LEGACY_PASSWORD_KEY])
    if not withPassword:
        return (settingsUser, None)
    if authcfg:
        user, password = loadCredentials(authcfg)
        if password:
            return (settingsUser or user, password)
    if legacy:
        if migrate:
            try:
                migrateFunction()
            except Exception as e:
                _log(
                    "Credential migration of {0} failed: {1}".format(
                        path, redact(e, legacy)
                    ),
                    Qgis.MessageLevel.Warning,
                )
        return (settingsUser, legacy)
    # no password stored (trust, .pgpass, PGPASSWORD): an empty string, as
    # before the authcfg change. None would reach the layer URI as the text
    # "None" and break the widgets that receive it
    return (settingsUser, "")


def readServer(name, withPassword=True, migrate=True):
    """
    Reads a DSGTools server. Password comes from authcfg first; a legacy
    clear text password is still returned and triggers the migration of the
    entry.
    :return: (tuple) (host, port, user, password)
    """
    path = "{0}/{1}".format(SERVERS_GROUP, name)
    values = _readGroup(path, ["host", "port", "username"])
    user, password = _resolve(
        path,
        values["username"],
        withPassword,
        migrate,
        lambda: migrateServer(name),
    )
    return (values["host"], values["port"], user, password)


def isDefaultServer(name):
    value = QSettings().value("{0}/{1}/isDefault".format(SERVERS_GROUP, name))
    return value is True or _str(value).lower() == "true"


def saveServer(
    name,
    host,
    port,
    user,
    password,
    isDefault=False,
    previousName=None,
    keepCredentialWhenEmpty=False,
):
    """
    Saves a DSGTools server. The password goes to the authentication
    database; QSettings receives only authcfg.
    :param previousName: (str) name of the server being edited (it is
        replaced, and its authcfg is reused).
    :param keepCredentialWhenEmpty: (bool) keep the existing credential when
        password is empty (used when the stored password could not be read).
    :return: (tuple) (saved, passwordStored)
    """
    settings = QSettings()
    oldAuthcfg = ""
    if previousName:
        oldPath = "{0}/{1}".format(SERVERS_GROUP, previousName)
        oldAuthcfg = _str(settings.value(oldPath + "/" + AUTHCFG_KEY))
        if not oldAuthcfg:
            # an edited server may also have the old authcfg under the new name
            oldAuthcfg = _str(
                settings.value("{0}/{1}/{2}".format(SERVERS_GROUP, name, AUTHCFG_KEY))
            )
    # clear text password of the entry being replaced (not migrated yet)
    legacy = _str(
        settings.value(
            "{0}/{1}/{2}".format(SERVERS_GROUP, previousName or name, LEGACY_PASSWORD_KEY)
        )
    )
    authcfg = ""
    passwordStored = False
    if password:
        authcfg = storeCredentials(user, password, name, authcfg=oldAuthcfg or None)
        passwordStored = bool(authcfg)
        authcfg = authcfg or ""
        if not passwordStored:
            _log(
                "Password of server {0} was not saved: the QGIS authentication "
                "database is not available (master password not set).".format(name),
                Qgis.MessageLevel.Warning,
            )
    elif oldAuthcfg and keepCredentialWhenEmpty:
        authcfg = oldAuthcfg
        passwordStored = True

    if previousName:
        settings.beginGroup("{0}/{1}".format(SERVERS_GROUP, previousName))
        settings.remove("")
        settings.endGroup()
    legacyKept = bool(password) and not passwordStored and legacy == password
    settings.beginGroup("{0}/{1}".format(SERVERS_GROUP, name))
    if legacyKept:
        # the authentication database refused the credential and the entry
        # still had this same password in clear text: it stays as it was
        # (nothing new is written in clear text) and the migration tries
        # again later. Dropping it here would lose the password
        settings.setValue(LEGACY_PASSWORD_KEY, legacy)
    else:
        settings.remove(LEGACY_PASSWORD_KEY)
    settings.setValue("host", host)
    settings.setValue("port", port)
    settings.setValue("username", user)
    if authcfg:
        settings.setValue(AUTHCFG_KEY, authcfg)
    else:
        settings.remove(AUTHCFG_KEY)
    settings.setValue("isDefault", bool(isDefault))
    settings.endGroup()
    settings.sync()

    if oldAuthcfg and oldAuthcfg != authcfg:
        _removeIfUnreferenced(oldAuthcfg)
    return (True, passwordStored or legacyKept)


def setDefaultServer(name):
    """
    Marks name as the default server (and the others as not default) without
    touching credentials.
    """
    settings = QSettings()
    for server in serverNames():
        settings.setValue(
            "{0}/{1}/isDefault".format(SERVERS_GROUP, server), server == name
        )
    settings.sync()


def _removeIfUnreferenced(authcfg, ignore=None):
    references = authcfgReferences(authcfg, ignore=ignore)
    if references:
        _log(
            "Credential {0} kept: still used by {1}.".format(
                authcfg, ", ".join(references)
            )
        )
        return False
    return removeCredentials(authcfg)


def removeServer(name):
    """
    Removes a DSGTools server and its credential (unless a connection still
    references it).
    """
    path = "{0}/{1}".format(SERVERS_GROUP, name)
    settings = QSettings()
    authcfg = _str(settings.value(path + "/" + AUTHCFG_KEY))
    settings.beginGroup(path)
    settings.remove("")
    settings.endGroup()
    settings.sync()
    if authcfg:
        _removeIfUnreferenced(authcfg)


# ---------------------------------------------------------------------------
# connections (QGIS PostgreSQL connection list)
# ---------------------------------------------------------------------------
def readConnection(name, withPassword=True, migrate=True):
    """
    Reads a connection of the QGIS PostgreSQL connection list.
    :return: (tuple) (host, port, database, user, password)
    """
    path = "{0}/{1}".format(CONNECTIONS_GROUP, name)
    values = _readGroup(path, ["host", "port", "database", "username"])
    user, password = _resolve(
        path,
        _str(values["username"]) or None,
        withPassword,
        migrate,
        lambda: migrateConnection(name),
    )
    return (values["host"], values["port"], values["database"], user, password)


def saveConnectionFromServer(connectionName, serverName, database, overwrite=False):
    """
    Creates a QGIS PostgreSQL connection that points to the credential of a
    DSGTools server through authcfg. Never writes a password.
    :return: (bool) True when the connection was written.
    """
    path = "{0}/{1}".format(CONNECTIONS_GROUP, connectionName)
    settings = QSettings()
    if not overwrite and settings.contains(path + "/database"):
        return False
    serverPath = "{0}/{1}".format(SERVERS_GROUP, serverName)
    if _str(settings.value(serverPath + "/" + LEGACY_PASSWORD_KEY)) and not _str(
        settings.value(serverPath + "/" + AUTHCFG_KEY)
    ):
        migrateServer(serverName)
    host, port, user, _ = readServer(serverName, withPassword=False)
    authcfg = _str(settings.value(serverPath + "/" + AUTHCFG_KEY))
    settings.beginGroup(path)
    settings.setValue("database", database)
    settings.setValue("host", host)
    settings.setValue("port", port)
    settings.setValue("username", user)
    settings.remove(LEGACY_PASSWORD_KEY)
    if authcfg:
        settings.setValue(AUTHCFG_KEY, authcfg)
    else:
        settings.remove(AUTHCFG_KEY)
    settings.endGroup()
    settings.sync()
    return True


# ---------------------------------------------------------------------------
# migration
# ---------------------------------------------------------------------------
def _canTry(path, force):
    if force:
        return True
    if _storeDeclined:
        return False
    last = _lastFailure.get(path)
    return last is None or time.time() - last > RETRY_INTERVAL_SECONDS


def _failed(path, status, detail=""):
    _lastFailure[path] = time.time()
    _log(
        "Credential migration of {0}: {1}{2}. The clear text password was kept "
        "and the migration will be tried again later.".format(
            path, status, " ({0})".format(detail) if detail else ""
        ),
        Qgis.MessageLevel.Warning,
    )
    return status


def _migrate(
    path,
    user,
    legacy,
    host,
    port,
    database,
    targetAuthcfg,
    name,
    testFunction,
    ownsAuthcfg,
):
    """
    Common steps: store (or reuse) the authcfg, read it back, test the
    connection with the credential read back, and only then drop the legacy
    key.
    """
    global _storeDeclined
    createdAuthcfg = None
    replacedAuthcfg = None
    authcfg = targetAuthcfg
    if authcfg:
        storedUser, storedPassword = loadCredentials(authcfg)
        if storedPassword != legacy or (storedUser or "") != (user or ""):
            if not ownsAuthcfg:
                return _failed(path, PENDING_SERVER)
            replacedAuthcfg = authcfg
            authcfg = None
    if not authcfg:
        authcfg = storeCredentials(user, legacy, name)
        if not authcfg:
            _storeDeclined = True
            return _failed(path, STORE_FAILED)
        createdAuthcfg = authcfg
    storedUser, storedPassword = loadCredentials(authcfg)
    if storedPassword != legacy:
        if createdAuthcfg:
            removeCredentials(createdAuthcfg)
        return _failed(path, STORE_FAILED, "read back mismatch")
    ok, message = testFunction(host, port, database, storedUser or user, storedPassword)
    if not ok:
        if createdAuthcfg:
            removeCredentials(createdAuthcfg)
        return _failed(path, UNREACHABLE, redact(message, legacy))
    settings = QSettings()
    settings.setValue(path + "/" + AUTHCFG_KEY, authcfg)
    settings.remove(path + "/" + LEGACY_PASSWORD_KEY)
    settings.sync()
    if (
        settings.contains(path + "/" + LEGACY_PASSWORD_KEY)
        or _str(settings.value(path + "/" + AUTHCFG_KEY)) != authcfg
    ):
        return _failed(path, STORE_FAILED, "settings not updated")
    _lastFailure.pop(path, None)
    if replacedAuthcfg:
        _removeIfUnreferenced(replacedAuthcfg)
    _log(
        "Credential migration of {0}: password moved to authcfg {1}.".format(
            path, authcfg
        )
    )
    return MIGRATED


def migrateServer(name, testFunction=None, force=False):
    """
    Migrates the legacy password of PostgreSQL/servers/<name>.
    """
    path = "{0}/{1}".format(SERVERS_GROUP, name)
    values = _readGroup(
        path, ["host", "port", "username", AUTHCFG_KEY, LEGACY_PASSWORD_KEY]
    )
    legacy = _str(values[LEGACY_PASSWORD_KEY])
    if not legacy:
        return NOTHING_TO_DO
    if not _canTry(path, force):
        return POSTPONED
    return _migrate(
        path,
        _str(values["username"]),
        legacy,
        values["host"],
        values["port"],
        SERVER_TEST_DATABASE,
        _str(values[AUTHCFG_KEY]) or None,
        name,
        testFunction or testConnection,
        ownsAuthcfg=True,
    )


def dsgtoolsServerForConnection(name):
    """
    Recognizes a connection created by DSGTools: same host, port, user and
    password as a DSGTools server. Only then the connection holds the very
    same credential as the server, and pointing it to the server's authcfg
    changes nothing but where the secret is kept. Connections that QGIS or
    the user created with other credentials are never touched.
    :return: (str) server name or None.
    """
    path = "{0}/{1}".format(CONNECTIONS_GROUP, name)
    values = _readGroup(path, ["host", "port", "username", LEGACY_PASSWORD_KEY])
    legacy = _str(values[LEGACY_PASSWORD_KEY])
    if not legacy:
        return None
    for server in sorted(serverNames()):
        host, port, user, _ = readServer(server, withPassword=False)
        if (
            _str(host) != _str(values["host"])
            or _str(port) != _str(values["port"])
            or _str(user) != _str(values["username"])
        ):
            continue
        serverPath = "{0}/{1}".format(SERVERS_GROUP, server)
        serverValues = _readGroup(serverPath, [AUTHCFG_KEY, LEGACY_PASSWORD_KEY])
        serverPassword = _str(serverValues[LEGACY_PASSWORD_KEY])
        if not serverPassword and _str(serverValues[AUTHCFG_KEY]):
            serverPassword = _str(loadCredentials(_str(serverValues[AUTHCFG_KEY]))[1])
        if serverPassword and serverPassword == legacy:
            return server
    return None


def migrateConnection(name, testFunction=None, force=False):
    """
    Migrates the legacy password of PostgreSQL/connections/<name> when the
    connection was created by DSGTools (see dsgtoolsServerForConnection).
    """
    path = "{0}/{1}".format(CONNECTIONS_GROUP, name)
    values = _readGroup(
        path, ["host", "port", "database", "username", AUTHCFG_KEY, LEGACY_PASSWORD_KEY]
    )
    legacy = _str(values[LEGACY_PASSWORD_KEY])
    if not legacy:
        return NOTHING_TO_DO
    ownAuthcfg = _str(values[AUTHCFG_KEY])
    if not _canTry(path, force):
        return POSTPONED
    server = dsgtoolsServerForConnection(name)
    if server is None:
        return NOT_DSGTOOLS
    serverAuthcfg = _str(
        QSettings().value("{0}/{1}/{2}".format(SERVERS_GROUP, server, AUTHCFG_KEY))
    )
    if not serverAuthcfg:
        status = migrateServer(server, testFunction=testFunction, force=force)
        if status != MIGRATED:
            return _failed(path, PENDING_SERVER)
        serverAuthcfg = _str(
            QSettings().value("{0}/{1}/{2}".format(SERVERS_GROUP, server, AUTHCFG_KEY))
        )
    if ownAuthcfg and ownAuthcfg != serverAuthcfg:
        # an authcfg chosen by the user is never replaced
        return NOT_DSGTOOLS
    return _migrate(
        path,
        _str(values["username"]),
        legacy,
        values["host"],
        values["port"],
        values["database"],
        serverAuthcfg,
        name,
        testFunction or testConnection,
        ownsAuthcfg=False,
    )


def _pretestedServers(force):
    """
    Tests in parallel the connection of every server that still has a
    clear text password, so a sweep waits for the slowest server and not
    for the sum of the timeouts of the unreachable ones. Only DSGTools
    servers are tested here; connections keep their own (sequential) test.
    :return: test function with the signature of testConnection.
    """
    targets = set()
    for server in serverNames():
        path = "{0}/{1}".format(SERVERS_GROUP, server)
        values = _readGroup(path, ["host", "port", "username", LEGACY_PASSWORD_KEY])
        legacy = _str(values[LEGACY_PASSWORD_KEY])
        if legacy and _canTry(path, force):
            targets.add(
                (
                    _str(values["host"]),
                    _str(values["port"]),
                    SERVER_TEST_DATABASE,
                    _str(values["username"]),
                    legacy,
                )
            )
    if len(targets) < 2:
        return testConnection
    results = {}
    with ThreadPoolExecutor(max_workers=min(MAX_PARALLEL_TESTS, len(targets))) as pool:
        futures = {target: pool.submit(testConnection, *target) for target in targets}
        for target, future in futures.items():
            results[target] = future.result()

    def tester(host, port, database, user, password):
        key = (_str(host), _str(port), _str(database), _str(user), _str(password))
        if key in results:
            return results[key]
        return testConnection(host, port, database, user, password)

    return tester


def migrateAll(testFunction=None, force=False):
    """
    Migrates every legacy password of DSGTools servers and of the connections
    DSGTools created. Idempotent: entries already migrated are skipped.
    :return: (dict) {settings path: status}
    """
    report = {}
    if testFunction is None:
        testFunction = _pretestedServers(force)
    for server in serverNames():
        report["{0}/{1}".format(SERVERS_GROUP, server)] = migrateServer(
            server, testFunction=testFunction, force=force
        )
    for connection in connectionNames():
        report["{0}/{1}".format(CONNECTIONS_GROUP, connection)] = migrateConnection(
            connection, testFunction=testFunction, force=force
        )
    pending = [
        path
        for path, status in report.items()
        if status not in (MIGRATED, NOTHING_TO_DO, NOT_DSGTOOLS)
    ]
    migrated = [path for path, status in report.items() if status == MIGRATED]
    if migrated or pending:
        _log(
            "Credential migration: {0} migrated, {1} pending.".format(
                len(migrated), len(pending)
            )
        )
    return report


def migrateOncePerSession(testFunction=None):
    """
    Runs migrateAll the first time the server tools are used in a session.
    """
    global _sweepDone
    if _sweepDone:
        return {}
    _sweepDone = True
    try:
        return migrateAll(testFunction=testFunction)
    except Exception as e:
        _log(
            "Credential migration failed: {0}".format(type(e).__name__),
            Qgis.MessageLevel.Warning,
        )
        return {}
