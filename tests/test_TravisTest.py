# -*- coding: utf-8 -*-
import sys
from qgis.testing import unittest


class TestTest(unittest.TestCase):
    def test_passes(self):
        self.assertTrue(True)


def run_all():
    """Default function that is called by the runner if nothing else is specified"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestTest, "test"))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
