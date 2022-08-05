import unittest
import time
from lib.driver import Driver
from lib.run_configs import RunConfigs
from nose.plugins.attrib import attr

class BaseTestClass(unittest.TestCase):

	def setUp(self):
		self.driver = Driver().get_driver();

	def tearDown(self):
		self.driver.quit();