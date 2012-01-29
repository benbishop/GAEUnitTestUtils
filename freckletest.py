__author__ = 'Ben'

import unittest
import unittestutils
from google.appengine.ext import testbed
from google.appengine.api import users
from google.appengine.ext import webapp

class BaseGAETestCase(unittest.TestCase):
    def _initTestBed(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()


    def setUp(self):
        self._initTestBed()