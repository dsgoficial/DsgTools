# -*- coding: utf-8 -*-
"""
Credenciais do DSGTools no QgsAuthManager (CDCiber 4.2).

Prova que o configurador e os demais pontos de escrita gravam a chave authcfg
e nunca password, que a senha volta pelo authcfg, que a migração das senhas
legadas só apaga o texto claro depois de testar a conexão, que sem senha
mestra nada cai para texto claro e que nenhum log carrega a senha.

Isolamento (obrigatório, antes do QGIS subir; o run_local.py sobe o QGIS):

    QGIS_CUSTOM_CONFIG_PATH  diretório descartável do perfil
    QGIS_AUTH_DB_DIR_PATH    diretório descartável do banco de autenticação
    QT_QPA_PLATFORM=offscreen

Sem as duas variáveis o QGIS avulso usa o perfil e o qgis-auth.db reais do
usuário, e por isso o módulo se recusa a rodar. O QSettings é redirecionado
para um diretório temporário aqui mesmo, e o auxiliar de senha (cofre do
sistema operacional) é desligado antes de qualquer operação de autenticação,
para que o teste nunca leia nem grave a senha mestra real.

PostGIS real (opcional, mas os casos de conexão bem-sucedida dependem dele):

    DSGTOOLS_TEST_PG_HOST, DSGTOOLS_TEST_PG_PORT, DSGTOOLS_TEST_PG_USER,
    DSGTOOLS_TEST_PG_PASSWORD

Um PostGIS descartável serve, por exemplo um contêiner postgis/postgis com
senha aleatória gerada na hora e destruído no fim.

Uso:
    tests/run_local.py tests.test_credentialStore
"""

import contextlib
import io
import os
import secrets
import socket
import tempfile
import unittest

from qgis.core import QgsApplication, QgsAuthMethodConfig, QgsProviderRegistry
from qgis.PyQt.QtCore import QSettings

_SETTINGS_DIR = tempfile.mkdtemp(prefix="dsgtools_cred_settings_")
QSettings.setDefaultFormat(QSettings.Format.IniFormat)
QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, _SETTINGS_DIR)

MASTER_PASSWORD = "dsgtools-test-master-" + secrets.token_hex(8)
ARTIFICIAL_PASSWORD = "dsgcred-" + secrets.token_hex(12)

PG_HOST = os.environ.get("DSGTOOLS_TEST_PG_HOST", "127.0.0.1")
PG_PORT = os.environ.get("DSGTOOLS_TEST_PG_PORT", "")
PG_USER = os.environ.get("DSGTOOLS_TEST_PG_USER", "postgres")
PG_PASSWORD = os.environ.get("DSGTOOLS_TEST_PG_PASSWORD", "")

SERVERS = "PostgreSQL/servers"
CONNECTIONS = "PostgreSQL/connections"


def _norm(path):
    return os.path.normcase(os.path.abspath(path))


def _isolationProblem():
    authDir = os.environ.get("QGIS_AUTH_DB_DIR_PATH")
    if not authDir or not os.environ.get("QGIS_CUSTOM_CONFIG_PATH"):
        return (
            "defina QGIS_CUSTOM_CONFIG_PATH e QGIS_AUTH_DB_DIR_PATH com diretorios "
            "descartaveis antes de subir o QGIS: sem elas o teste tocaria o perfil "
            "e o banco de autenticacao reais"
        )
    authManager = QgsApplication.authManager()
    if not _norm(authManager.authenticationDatabasePath()).startswith(_norm(authDir)):
        return "o banco de autenticacao nao esta no diretorio descartavel"
    if not _norm(QSettings().fileName()).startswith(_norm(_SETTINGS_DIR)):
        return "o QSettings nao esta no diretorio descartavel"
    return None


_ISOLATION = _isolationProblem()
if _ISOLATION is None:
    _authManager = QgsApplication.authManager()
    # o cofre do sistema e do usuario, nao do perfil: desligado antes de tudo
    _authManager.setPasswordHelperEnabled(False)
    if not _authManager.masterPasswordIsSet():
        _authManager.setMasterPassword(MASTER_PASSWORD, True)


def _credentialStore():
    from DsgTools.core.Utils import credentialStore

    return credentialStore


def _value(path):
    return QSettings().value(path)


def _closedPort():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return str(port)


def _writeLegacy(group, name, host, port, user, password, database=None):
    settings = QSettings()
    settings.beginGroup("{0}/{1}".format(group, name))
    settings.remove("")
    if database is not None:
        settings.setValue("database", database)
    settings.setValue("host", host)
    settings.setValue("port", port)
    settings.setValue("username", user)
    settings.setValue("password", password)
    if group == SERVERS:
        settings.setValue("isDefault", False)
    settings.endGroup()
    settings.sync()


def _loadAuthcfg(authcfg):
    """
    Reads an authcfg straight from QgsAuthManager (not through the module
    under test).
    """
    config = QgsAuthMethodConfig()
    result = QgsApplication.authManager().loadAuthenticationConfig(
        authcfg, config, True
    )
    ok = result[0] if isinstance(result, tuple) else result
    if isinstance(result, tuple) and result[1] is not None:
        config = result[1]
    if not ok:
        return (None, None)
    return (config.config("username"), config.config("password"))


def _iniText():
    settings = QSettings()
    settings.sync()
    with open(settings.fileName(), "rb") as handle:
        return handle.read().decode("utf-8", errors="replace")


class LogCapture:
    """
    Captures QgsMessageLog, stdout and stderr while active.
    """

    def __init__(self):
        self.messages = []
        self._stdout = io.StringIO()
        self._stderr = io.StringIO()

    def _receive(self, message, tag, *args):
        self.messages.append("{0}|{1}".format(tag, message))

    def _signals(self):
        # QGIS 4.2.1 delivers QgsMessageLog.logMessage through
        # messageReceivedWithFormat; messageReceived alone hears nothing
        log = QgsApplication.messageLog()
        signals = [log.messageReceived]
        if hasattr(log, "messageReceivedWithFormat"):
            signals.append(log.messageReceivedWithFormat)
        return signals

    def __enter__(self):
        for signal in self._signals():
            signal.connect(self._receive)
        self._redirectOut = contextlib.redirect_stdout(self._stdout)
        self._redirectErr = contextlib.redirect_stderr(self._stderr)
        self._redirectOut.__enter__()
        self._redirectErr.__enter__()
        return self

    def __exit__(self, *args):
        self._redirectErr.__exit__(*args)
        self._redirectOut.__exit__(*args)
        QgsApplication.processEvents()
        for signal in self._signals():
            signal.disconnect(self._receive)
        return False

    def text(self):
        return "\n".join(
            self.messages + [self._stdout.getvalue(), self._stderr.getvalue()]
        )


class CredentialStoreTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if _ISOLATION is not None:
            raise RuntimeError("recusado: " + _ISOLATION)

    def setUp(self):
        settings = QSettings()
        settings.remove("PostgreSQL")
        settings.sync()
        authManager = QgsApplication.authManager()
        if not authManager.masterPasswordIsSet():
            authManager.setMasterPassword(MASTER_PASSWORD, True)
        for authcfg in authManager.configIds():
            authManager.removeAuthenticationConfig(authcfg)
        try:
            _credentialStore().resetSessionState()
        except ImportError:
            pass

    def requirePostgis(self):
        if not (PG_PORT and PG_PASSWORD):
            self.skipTest("PostGIS de teste nao configurado (DSGTOOLS_TEST_PG_*)")

    def configurator(self):
        from DsgTools.gui.ServerTools.serverConfigurator import ServerConfigurator

        return ServerConfigurator(None)

    def saveServer(self, name, host, port, user, password):
        dlg = self.configurator()
        self.assertTrue(dlg.storeServerConfiguration(name, host, port, user, password))
        return dlg

    # (a) -----------------------------------------------------------------
    def test_a_configurator_saves_authcfg_and_never_password(self):
        self.saveServer("srvA", "127.0.0.1", "5432", "operador", ARTIFICIAL_PASSWORD)
        path = SERVERS + "/srvA"
        self.assertFalse(QSettings().contains(path + "/password"))
        authcfg = _value(path + "/authcfg")
        self.assertTrue(authcfg)
        self.assertIn(authcfg, QgsApplication.authManager().configIds())
        self.assertEqual(_loadAuthcfg(authcfg), ("operador", ARTIFICIAL_PASSWORD))
        self.assertNotIn(ARTIFICIAL_PASSWORD, _iniText())
        self.assertEqual(_value(path + "/username"), "operador")
        self.assertEqual(_value(path + "/host"), "127.0.0.1")

        # the password comes back through the authcfg on the public readers
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        self.assertEqual(
            PostgisDb().getServerConfiguration("srvA"),
            ("127.0.0.1", "5432", "operador", ARTIFICIAL_PASSWORD),
        )
        from DsgTools.gui.ServerTools.viewServers import ViewServers

        viewServers = ViewServers()
        self.assertEqual(
            viewServers.getServerConfiguration("srvA")[3], ARTIFICIAL_PASSWORD
        )

        # editing keeps the same authcfg (connections referencing it survive)
        dlg = self.configurator()
        dlg.setServerConfiguration("srvA")
        self.assertEqual(dlg.passwordEdit.text(), ARTIFICIAL_PASSWORD)
        newPassword = ARTIFICIAL_PASSWORD + "-novo"
        dlg.storeServerConfiguration(
            "srvA", "127.0.0.1", "5432", "operador", newPassword
        )
        self.assertEqual(_value(path + "/authcfg"), authcfg)
        self.assertEqual(_loadAuthcfg(authcfg), ("operador", newPassword))
        self.assertFalse(QSettings().contains(path + "/password"))
        self.assertNotIn(newPassword, _iniText())

    # (b) -----------------------------------------------------------------
    def test_b_migration_with_successful_test_removes_password(self):
        self.requirePostgis()
        store = _credentialStore()
        _writeLegacy(SERVERS, "legado", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        _writeLegacy(
            CONNECTIONS,
            "legado_postgres",
            PG_HOST,
            PG_PORT,
            PG_USER,
            PG_PASSWORD,
            "postgres",
        )
        # same host, port and user, other password: not DSGTools's credential
        _writeLegacy(
            CONNECTIONS,
            "alheia",
            PG_HOST,
            PG_PORT,
            PG_USER,
            ARTIFICIAL_PASSWORD,
            "postgres",
        )

        report = store.migrateAll(force=True)  # real psycopg2 test

        self.assertEqual(report[SERVERS + "/legado"], store.MIGRATED)
        self.assertEqual(report[CONNECTIONS + "/legado_postgres"], store.MIGRATED)
        self.assertEqual(report[CONNECTIONS + "/alheia"], store.NOT_DSGTOOLS)
        serverAuthcfg = _value(SERVERS + "/legado/authcfg")
        self.assertTrue(serverAuthcfg)
        self.assertFalse(QSettings().contains(SERVERS + "/legado/password"))
        self.assertFalse(
            QSettings().contains(CONNECTIONS + "/legado_postgres/password")
        )
        self.assertEqual(
            _value(CONNECTIONS + "/legado_postgres/authcfg"), serverAuthcfg
        )
        self.assertEqual(_loadAuthcfg(serverAuthcfg), (PG_USER, PG_PASSWORD))
        self.assertEqual(_value(CONNECTIONS + "/alheia/password"), ARTIFICIAL_PASSWORD)
        self.assertFalse(QSettings().contains(CONNECTIONS + "/alheia/authcfg"))
        self.assertNotIn(PG_PASSWORD, _iniText())

        # QGIS itself opens the migrated connection through the authcfg
        metadata = QgsProviderRegistry.instance().providerMetadata("postgres")
        connection = metadata.findConnection("legado_postgres", False)
        self.assertIn("authcfg=" + serverAuthcfg, connection.uri())
        self.assertNotIn("password", connection.uri())
        self.assertEqual(connection.executeSql("SELECT 1"), [[1]])

        # idempotent
        before = sorted(QgsApplication.authManager().configIds())
        again = store.migrateAll(force=True)
        self.assertEqual(again[SERVERS + "/legado"], store.NOTHING_TO_DO)
        self.assertEqual(again[CONNECTIONS + "/legado_postgres"], store.NOTHING_TO_DO)
        self.assertEqual(sorted(QgsApplication.authManager().configIds()), before)

    def test_b2_reading_a_legacy_password_migrates_the_entry(self):
        self.requirePostgis()
        _writeLegacy(SERVERS, "lido", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        self.assertEqual(
            PostgisDb().getServerConfiguration("lido"),
            (PG_HOST, PG_PORT, PG_USER, PG_PASSWORD),
        )
        self.assertFalse(QSettings().contains(SERVERS + "/lido/password"))
        authcfg = _value(SERVERS + "/lido/authcfg")
        self.assertTrue(authcfg)
        self.assertEqual(_loadAuthcfg(authcfg), (PG_USER, PG_PASSWORD))

    # (c) -----------------------------------------------------------------
    def test_c_migration_with_failed_test_keeps_password(self):
        store = _credentialStore()
        port = _closedPort()
        _writeLegacy(
            SERVERS, "fora", "127.0.0.1", port, "operador", ARTIFICIAL_PASSWORD
        )
        before = sorted(QgsApplication.authManager().configIds())

        status = store.migrateServer("fora", force=True)  # real psycopg2, refused

        self.assertEqual(status, store.UNREACHABLE)
        self.assertEqual(_value(SERVERS + "/fora/password"), ARTIFICIAL_PASSWORD)
        self.assertFalse(QSettings().contains(SERVERS + "/fora/authcfg"))
        self.assertEqual(sorted(QgsApplication.authManager().configIds()), before)

        # the plugin keeps working with the legacy password
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        self.assertEqual(
            PostgisDb().getServerConfiguration("fora")[3], ARTIFICIAL_PASSWORD
        )
        self.assertEqual(_value(SERVERS + "/fora/password"), ARTIFICIAL_PASSWORD)

        # injected failure, then the server answers: tried again, migrated
        self.assertEqual(
            store.migrateServer(
                "fora", testFunction=lambda *a: (False, "x"), force=True
            ),
            store.UNREACHABLE,
        )
        self.assertEqual(_value(SERVERS + "/fora/password"), ARTIFICIAL_PASSWORD)
        self.assertEqual(
            store.migrateServer("fora", testFunction=lambda *a: (True, ""), force=True),
            store.MIGRATED,
        )
        self.assertFalse(QSettings().contains(SERVERS + "/fora/password"))
        self.assertEqual(
            _loadAuthcfg(_value(SERVERS + "/fora/authcfg")),
            ("operador", ARTIFICIAL_PASSWORD),
        )

    # (d) -----------------------------------------------------------------
    def test_d_no_log_contains_the_password(self):
        store = _credentialStore()
        canary = "canario-" + secrets.token_hex(6)
        with LogCapture() as probe:
            from qgis.core import QgsMessageLog

            QgsMessageLog.logMessage(canary, "DSGTools Plugin")
            print(canary)
        # the instrument must catch what is logged, or a clean result proves nothing
        self.assertTrue(any(canary in m for m in probe.messages), "QgsMessageLog")
        self.assertIn(canary, probe._stdout.getvalue(), "stdout")

        errors = []
        with LogCapture() as capture:
            self.saveServer(
                "srvD", "127.0.0.1", _closedPort(), "operador", ARTIFICIAL_PASSWORD
            )
            _writeLegacy(
                SERVERS,
                "foraD",
                "127.0.0.1",
                _closedPort(),
                "operador",
                ARTIFICIAL_PASSWORD,
            )
            store.migrateAll(force=True)
            store.migrateServer(
                "foraD", testFunction=lambda *a: (False, ""), force=True
            )
            ok, message = store.testConnection(
                "127.0.0.1", _closedPort(), "postgres", "operador", ARTIFICIAL_PASSWORD
            )
            errors.append(message)
            if PG_PORT and PG_PASSWORD:
                # wrong password against a live server: a real auth error
                from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

                db = PostgisDb()
                db.testCredentials(
                    PG_HOST, PG_PORT, "postgres", PG_USER, ARTIFICIAL_PASSWORD
                )
                errors.append(db.db.lastError().text())
                try:
                    db.checkAndOpenDb()
                except Exception as e:
                    errors.append(":".join(str(a) for a in e.args))
                _writeLegacy(
                    SERVERS, "authD", PG_HOST, PG_PORT, PG_USER, ARTIFICIAL_PASSWORD
                )
                store.migrateServer("authD", force=True)
        self.assertTrue(capture.messages, "nenhuma mensagem capturada nos fluxos")
        self.assertTrue(any("foraD" in m for m in capture.messages))
        self.assertTrue(
            errors[0], "o teste de conexao recusado devolveu mensagem vazia"
        )
        self.assertNotIn(ARTIFICIAL_PASSWORD, capture.text())
        for error in errors:
            self.assertNotIn(ARTIFICIAL_PASSWORD, error)
        self.assertEqual(
            store.redact("a " + ARTIFICIAL_PASSWORD + " b", ARTIFICIAL_PASSWORD),
            "a *** b",
        )

    # (e) -----------------------------------------------------------------
    def test_e_without_master_password_nothing_falls_back_to_clear_text(self):
        authManager = QgsApplication.authManager()
        authManager.clearMasterPassword()
        self.assertFalse(authManager.masterPasswordIsSet())
        try:
            with LogCapture() as capture:
                dlg = self.saveServer(
                    "srvE", "127.0.0.1", "5432", "operador", ARTIFICIAL_PASSWORD
                )
            self.assertFalse(QSettings().contains(SERVERS + "/srvE/password"))
            self.assertFalse(QSettings().contains(SERVERS + "/srvE/authcfg"))
            self.assertEqual(_value(SERVERS + "/srvE/username"), "operador")
            self.assertFalse(getattr(dlg, "passwordStored", True))
            self.assertNotIn(ARTIFICIAL_PASSWORD, _iniText())
            self.assertNotIn(ARTIFICIAL_PASSWORD, capture.text())
        finally:
            authManager.setMasterPassword(MASTER_PASSWORD, True)
        self.assertEqual(authManager.configIds(), [])

    # (f) -----------------------------------------------------------------
    def test_f_connection_created_from_server_uses_authcfg(self):
        self.saveServer("srvF", "127.0.0.1", "5432", "operador", ARTIFICIAL_PASSWORD)
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        db = PostgisDb()
        db.db.setDatabaseName("bdteste")
        self.assertTrue(db.storeConnection("srvF"))
        path = CONNECTIONS + "/srvF_bdteste"
        self.assertFalse(QSettings().contains(path + "/password"))
        self.assertEqual(_value(path + "/authcfg"), _value(SERVERS + "/srvF/authcfg"))
        self.assertEqual(_value(path + "/database"), "bdteste")
        self.assertNotIn(ARTIFICIAL_PASSWORD, _iniText())
        metadata = QgsProviderRegistry.instance().providerMetadata("postgres")
        uri = metadata.findConnection("srvF_bdteste", False).uri()
        self.assertIn("authcfg=" + _value(SERVERS + "/srvF/authcfg"), uri)
        self.assertNotIn(ARTIFICIAL_PASSWORD, uri)
        self.assertEqual(
            db.getConnectionFromQSettings("srvF_bdteste"),
            ("127.0.0.1", "5432", "bdteste", "operador", ARTIFICIAL_PASSWORD),
        )

    # (g) -----------------------------------------------------------------
    def test_g_removing_a_server_removes_its_authcfg(self):
        self.saveServer("srvG", "127.0.0.1", "5432", "operador", ARTIFICIAL_PASSWORD)
        self.saveServer("srvH", "127.0.0.1", "5433", "operador", ARTIFICIAL_PASSWORD)
        authcfgG = _value(SERVERS + "/srvG/authcfg")
        authcfgH = _value(SERVERS + "/srvH/authcfg")
        self.assertTrue(authcfgG and authcfgH)
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        db = PostgisDb()
        db.db.setDatabaseName("bdh")
        db.storeConnection("srvH")
        from DsgTools.gui.ServerTools.viewServers import ViewServers

        viewServers = ViewServers()
        viewServers.removeServerConfiguration("srvG")
        viewServers.removeServerConfiguration("srvH")
        configIds = QgsApplication.authManager().configIds()
        self.assertFalse(QSettings().contains(SERVERS + "/srvG/host"))
        self.assertNotIn(authcfgG, configIds)
        # still referenced by a connection: kept, the connection keeps working
        self.assertIn(authcfgH, configIds)
        self.assertEqual(_value(CONNECTIONS + "/srvH_bdh/authcfg"), authcfgH)

    # (h) -----------------------------------------------------------------
    def test_h_server_manager_migrates_once_and_readers_keep_working(self):
        self.requirePostgis()
        _writeLegacy(SERVERS, "padrao", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        QSettings().setValue(SERVERS + "/padrao/isDefault", True)
        from DsgTools.gui.ServerTools.viewServers import ViewServers, ViewServersStatic

        viewServers = ViewServers()
        # built at plugin start: nothing migrated (nor decrypted) yet
        self.assertEqual(_value(SERVERS + "/padrao/password"), PG_PASSWORD)
        viewServers.show()  # first show of the session: migration runs
        QgsApplication.processEvents()
        viewServers.hide()
        self.assertFalse(QSettings().contains(SERVERS + "/padrao/password"))
        authcfg = _value(SERVERS + "/padrao/authcfg")
        self.assertEqual(_loadAuthcfg(authcfg), (PG_USER, PG_PASSWORD))

        self.assertEqual(viewServers.connectionParameters()["password"], PG_PASSWORD)
        self.assertEqual(
            viewServers.getDefaultConnectionParameters(),
            ("padrao", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD),
        )
        static = ViewServersStatic()
        self.assertEqual(static.connectionParameters()["password"], PG_PASSWORD)
        self.assertEqual(static.getDefaultConnectionParameters()[4], PG_PASSWORD)
        from DsgTools.core.DbTools.dbConverter import DbConverter

        self.assertEqual(
            DbConverter.userPasswordFromHost(None, PG_HOST, PG_USER), PG_PASSWORD
        )
        self.assertIsNone(DbConverter.userPasswordFromHost(None, PG_HOST, "outro"))

    # (i) and (j): layer URIs and the saved project ------------------------
    def createTestTables(self, temporaryUser=None, temporaryPassword=None):
        import psycopg2

        conn = psycopg2.connect(
            host=PG_HOST,
            port=int(PG_PORT),
            dbname="postgres",
            user=PG_USER,
            password=PG_PASSWORD,
            connect_timeout=5,
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            cur.execute("DROP SCHEMA IF EXISTS cred_teste CASCADE")
            cur.execute("DROP SCHEMA IF EXISTS dominios CASCADE")
            cur.execute("CREATE SCHEMA cred_teste")
            cur.execute(
                "CREATE TABLE cred_teste.ponto (id serial PRIMARY KEY, nome text, "
                "geom geometry(Point, 4326))"
            )
            cur.execute(
                "INSERT INTO cred_teste.ponto (nome, geom) VALUES "
                "('a', ST_SetSRID(ST_MakePoint(-43, -22), 4326))"
            )
            cur.execute("CREATE SCHEMA dominios")
            cur.execute(
                "CREATE TABLE dominios.situacao (code integer PRIMARY KEY, code_name text)"
            )
            cur.execute("INSERT INTO dominios.situacao VALUES (1, 'x')")
            if temporaryUser:
                cur.execute("DROP ROLE IF EXISTS " + temporaryUser)
                cur.execute(
                    "CREATE ROLE " + temporaryUser + " LOGIN PASSWORD %s",
                    (temporaryPassword,),
                )
                for schema in ("cred_teste", "dominios"):
                    cur.execute(
                        "GRANT USAGE ON SCHEMA {0} TO {1}".format(schema, temporaryUser)
                    )
                    cur.execute(
                        "GRANT SELECT ON ALL TABLES IN SCHEMA {0} TO {1}".format(
                            schema, temporaryUser
                        )
                    )
        conn.close()

    def loadTestLayers(self, db):
        from qgis.core import QgsLayerTreeGroup
        from DsgTools.core.Factories.LayerLoaderFactory.postgisLayerLoader import (
            PostGISLayerLoader,
        )

        class _Canvas:
            def layers(self):
                return []

        class _Iface:
            # the loader only asks the canvas which layers are already there
            def mapCanvas(self):
                return _Canvas()

        loader = PostGISLayerLoader(_Iface(), db, False)
        layers = [
            # self.uri path (buildUri)
            loader.loadQgsVectorLayer(("cred_teste", "ponto")),
            # hand built URIs
            loader.loadQgsVectorLayer(("cred_teste", "ponto"), nonSpatial=True),
            loader.loadDomain("situacao", QgsLayerTreeGroup("dominios")),
        ]
        for layer in layers:
            self.assertIsNotNone(layer)
            self.assertTrue(layer.isValid(), layer.name())
            self.assertEqual(layer.featureCount(), 1)
        # loadDomain only puts the layer in a tree group; registered here so
        # that its URI is also written to the .qgs
        from qgis.core import QgsProject

        QgsProject.instance().addMapLayer(layers[2], False)
        self.assertEqual(len(QgsProject.instance().mapLayers()), 3)
        return layers

    def writeProject(self):
        from qgis.core import QgsProject

        path = os.path.join(tempfile.mkdtemp(prefix="dsgtools_cred_qgs_"), "p.qgs")
        self.assertTrue(QgsProject.instance().write(path))
        with open(path, "rb") as handle:
            return path, handle.read().decode("utf-8", errors="replace")

    def test_i_layers_from_authcfg_server_keep_password_out_of_the_qgs(self):
        self.requirePostgis()
        from qgis.core import QgsProject

        QgsProject.instance().clear()
        self.createTestTables()
        self.saveServer("srvI", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        authcfg = _value(SERVERS + "/srvI/authcfg")
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        host, port, user, password = PostgisDb().getServerConfiguration("srvI")
        db = PostgisDb()
        db.connectDatabaseWithParameters(host, port, "postgres", user, password)
        before = sorted(QgsApplication.authManager().configIds())

        layers = self.loadTestLayers(db)

        # the messages never echo a source: it may hold the password
        for layer in layers:
            self.assertTrue(
                "authcfg=" + str(authcfg) in layer.source(), "sem authcfg na fonte"
            )
            self.assertTrue(PG_PASSWORD not in layer.source(), "senha na fonte")
        path, text = self.writeProject()
        self.assertTrue("authcfg=" + str(authcfg) in text, "sem authcfg no .qgs")
        self.assertTrue(PG_PASSWORD not in text, "senha no .qgs")
        self.assertEqual(sorted(QgsApplication.authManager().configIds()), before)

        # the saved project opens again with valid layers, through the authcfg
        QgsProject.instance().clear()
        self.assertTrue(QgsProject.instance().read(path))
        reopened = list(QgsProject.instance().mapLayers().values())
        self.assertEqual(len(reopened), 3)
        for layer in reopened:
            self.assertTrue(layer.isValid(), layer.name())
            self.assertEqual(layer.featureCount(), 1)
        QgsProject.instance().clear()

    def test_i2_getURIV2_from_authcfg_server_keeps_password_out(self):
        """
        getURIV2 (usado pelo getLayerDict) monta a URI pelo authcfg da conexão,
        e a camada abre válida por ele; a senha não aparece na fonte.
        """
        self.requirePostgis()
        from qgis.core import QgsVectorLayer

        self.createTestTables()
        self.saveServer("srvI2", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        authcfg = _value(SERVERS + "/srvI2/authcfg")
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        host, port, user, password = PostgisDb().getServerConfiguration("srvI2")
        db = PostgisDb()
        db.connectDatabaseWithParameters(host, port, "postgres", user, password)
        uri = db.getURIV2("cred_teste", "ponto", "geom")
        source = uri.uri(False)
        self.assertTrue("authcfg=" + str(authcfg) in source, "sem authcfg na URI")
        self.assertTrue(PG_PASSWORD not in source, "senha na URI")
        layer = QgsVectorLayer(source, "ponto", "postgres")
        self.assertTrue(layer.isValid(), "camada pelo authcfg não abriu")
        self.assertEqual(layer.featureCount(), 1)

    def test_j_temporary_credential_without_authcfg_stays_in_the_uri(self):
        """
        Residual risk, kept on purpose: a credential passed straight to
        connect (the temporary SAP user) has no authcfg, and none is created,
        so the URI and the .qgs keep its password, as before. It also proves
        that the .qgs check of (i) does catch a password when there is one.
        """
        self.requirePostgis()
        from qgis.core import QgsProject

        QgsProject.instance().clear()
        temporaryUser = "sap_temp_" + secrets.token_hex(3)
        temporaryPassword = "sap-" + secrets.token_hex(10)
        self.createTestTables(temporaryUser, temporaryPassword)
        # a DSGTools server on the same host, other user: must not be used
        self.saveServer("srvJ", PG_HOST, PG_PORT, PG_USER, PG_PASSWORD)
        before = sorted(QgsApplication.authManager().configIds())
        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        db = PostgisDb()
        db.connectDatabaseWithParameters(
            PG_HOST, PG_PORT, "postgres", temporaryUser, temporaryPassword
        )

        layers = self.loadTestLayers(db)

        # the messages never echo a source: it may hold the password
        for layer in layers:
            self.assertTrue("authcfg=" not in layer.source(), "authcfg inesperado")
        path, text = self.writeProject()
        self.assertTrue(temporaryPassword in text, "a regua do .qgs nao achou a senha")
        self.assertTrue(PG_PASSWORD not in text, "senha do servidor no .qgs")
        self.assertEqual(sorted(QgsApplication.authManager().configIds()), before)
        QgsProject.instance().clear()

    # (k) -----------------------------------------------------------------
    def test_k_server_without_password_reads_as_empty_string(self):
        """
        A server saved without password (trust, .pgpass, PGPASSWORD) reads as
        an empty password. None used to reach the layer source as the text
        password='None' and to break the edit dialog.
        """
        store = _credentialStore()
        self.saveServer("srvK", "127.0.0.1", "5432", "operador", "")
        self.assertEqual(
            store.readServer("srvK"), ("127.0.0.1", "5432", "operador", "")
        )
        # legacy entry with an empty password key, as the old code wrote it
        _writeLegacy(SERVERS, "srvKlegado", "127.0.0.1", "5432", "operador", "")
        self.assertEqual(store.readServer("srvKlegado")[3], "")

        from qgis.core import QgsDataSourceUri

        from DsgTools.core.Factories.DbFactory.postgisDb import PostgisDb

        db = PostgisDb()
        host, port, user, password = db.getServerConfiguration("srvK")
        db.db.setHostName(host)
        db.db.setPort(int(port))
        db.db.setDatabaseName("banco")
        db.db.setUserName(user)
        db.db.setPassword(password)
        uri = QgsDataSourceUri()
        db._setUriConnection(uri, host, port, "banco", user, db.db.password())
        self.assertNotIn("None", uri.uri(False))
        self.assertNotIn("password", uri.uri(False))
        self.assertNotIn("None", db.makeOgrConn())
        # the adapter never keeps None, whoever sets it
        db.db.setPassword(None)
        self.assertEqual(db.db.password(), "")

        dlg = self.configurator()
        dlg.setServerConfiguration("srvK")
        self.assertEqual(dlg.passwordEdit.text(), "")
        self.assertFalse(dlg.passwordLoadFailed)

    # (l) -----------------------------------------------------------------
    def test_l_editing_a_legacy_server_without_master_password_keeps_it(self):
        """
        Editing a server that still has the clear text password while the
        authentication database refuses to store it must not lose the
        password: the entry stays as it was and migrates later.
        """
        port = _closedPort()
        _writeLegacy(SERVERS, "srvL", "127.0.0.1", port, "operador", ARTIFICIAL_PASSWORD)
        authManager = QgsApplication.authManager()
        authManager.clearMasterPassword()
        self.assertFalse(authManager.masterPasswordIsSet())
        try:
            dlg = self.configurator()
            dlg.isEdit = 1
            dlg.oldName = "srvL"
            self.assertTrue(
                dlg.storeServerConfiguration(
                    "srvL", "127.0.0.1", port, "operador2", ARTIFICIAL_PASSWORD
                )
            )
            self.assertEqual(_value(SERVERS + "/srvL/password"), ARTIFICIAL_PASSWORD)
            self.assertEqual(_value(SERVERS + "/srvL/username"), "operador2")
            self.assertFalse(QSettings().contains(SERVERS + "/srvL/authcfg"))
            self.assertTrue(dlg.passwordStored)
            # a password that was never in clear text still does not go there
            dlg = self.configurator()
            dlg.isEdit = 1
            dlg.oldName = "srvL"
            newPassword = ARTIFICIAL_PASSWORD + "-novo"
            dlg.storeServerConfiguration(
                "srvL", "127.0.0.1", port, "operador2", newPassword
            )
            self.assertFalse(QSettings().contains(SERVERS + "/srvL/password"))
            self.assertFalse(dlg.passwordStored)
            self.assertNotIn(newPassword, _iniText())
        finally:
            authManager.setMasterPassword(MASTER_PASSWORD, True)

    # (m) -----------------------------------------------------------------
    def test_m_sweep_tests_unreachable_legacy_servers_in_parallel(self):
        """
        The sweep of the server manager waits for the slowest server, not for
        the sum of the timeouts of the unreachable ones.
        """
        import threading
        import time

        store = _credentialStore()
        for i in range(4):
            _writeLegacy(
                SERVERS,
                "srvM{0}".format(i),
                "127.0.0.1",
                str(40000 + i),
                "operador",
                ARTIFICIAL_PASSWORD,
            )
        calls = []
        lock = threading.Lock()

        def slowTest(host, port, database, user, password, timeout=3):
            with lock:
                calls.append(str(port))
            time.sleep(1.0)
            return (False, "OperationalError: sem resposta")

        original = store.testConnection
        store.testConnection = slowTest
        try:
            start = time.time()
            report = store.migrateAll()
            elapsed = time.time() - start
        finally:
            store.testConnection = original
        self.assertEqual(sorted(calls), ["40000", "40001", "40002", "40003"])
        self.assertLess(elapsed, 2.5, "os testes de conexao rodaram em sequencia")
        for i in range(4):
            path = SERVERS + "/srvM{0}".format(i)
            self.assertEqual(report[path], store.UNREACHABLE)
            self.assertEqual(_value(path + "/password"), ARTIFICIAL_PASSWORD)
            self.assertFalse(QSettings().contains(path + "/authcfg"))
        self.assertEqual(QgsApplication.authManager().configIds(), [])


if __name__ == "__main__":
    unittest.main()
