from configparser import ConfigParser
from lib.run_configs import RunConfigs
from lib.logger import Logger
import datetime
import os
import time

class BaseClass(Logger):

	@property
	def root_location(self):
		# hardcoded for now
		root_location = os.environ['PYTHONPATH'].replace(":","") + "/";
		self.logs(root_location);
		return root_location

	@property
	def config_location(self):
		config_location = 'config/pages/'
		return config_location

	def properties_file(self):
		properties_file = '%s%s%s' % (self.root_location, self.config_location, self.PROPERTIES_FILE)
		return properties_file

	def get_property(self, config, section='default'):
		return self.get_full_property_value(config, section)

	def get_full_property_value(self, config, section='default'):
		c = ConfigParser()
		c.read(self.properties_file())
		section = RunConfigs()._properties_section;
		if section is not None:
			return c.get(section, config);
		return c.get('default', config)

	def today_date(self):
		date_s = str(datetime.datetime.now());
		return date_s;		