import os
import selenium
import datetime
from lib.run_configs import RunConfigs
from appium import webdriver as AppiumDriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver

from lib.base_class import BaseClass

class Driver(BaseClass):

	def get_driver(self):
		""" Here we get configs to determind if test is to be run
		locally or remotely. To keep it clean, we modify any post-instantiation
		needs via another method. Capabilities are handled via the 
		_get_desired_capabilities() method. 
		Then, finally return the complete driver object.

		Attributes:
		-------------
		None

		Returns:
		-------------
		WebDriver instance.
		"""
		driver = None;
		self.logs("In Driver().__init__()");
		if (RunConfigs()._remote_or_local == "local"):
			driver = self._get_local_driver();
		else:
			driver = self._get_remote_driver();
		# post instantiation modifiers
		driver = self._modify_driver(driver);
		return driver;

	def _get_local_driver(self):
		""" which local driver """
		if (RunConfigs()._browser_name == "chrome"):
			return self.get_chrome_driver_local();
		if (RunConfigs()._browser_name == "firefox"):
			return self.get_firefox_driver_local();

	def _get_remote_driver(self):
		command_exec = self._get_command_executor();
		if (RunConfigs()._is_appium == "True"):
			desired_cap = self._get_appium_desired_capabilities();
			return AppiumDriver.Remote(command_executor=command_exec, desired_capabilities=desired_cap);
		else:
			desired_cap = self._get_desktop_desired_capabilities();
			return RemoteDriver(command_executor=command_exec, desired_capabilities=desired_cap);

	def _get_command_executor(self):
		url = RunConfigs()._run_location_url;
		return url;

	def _get_appium_desired_capabilities(self):
		capabilities = {};
		capabilities['appium_version'] = RunConfigs()._appium_appium_version;
		capabilities['deviceName'] = RunConfigs()._appium_device_name;
		capabilities['deviceOrientation'] = RunConfigs()._appium_device_orientation;
		capabilities['platformVersion'] = RunConfigs()._appium_platform_version;
		capabilities['platformName'] = RunConfigs()._appium_platform_name;
		capabilities['browserName'] = RunConfigs()._appium_browser_name;
		"""sauce labs"""
		capabilities = self._get_sauce_labs_options(capabilities);
		return capabilities;		

	def _get_desktop_desired_capabilities(self):
		capabilities = {};
		capabilities['browserName'] = RunConfigs()._browser_name;
		capabilities['version'] = RunConfigs()._browser_version;
		capabilities['platformName'] = RunConfigs()._platform_type;
		capabilities['acceptsSslCerts'] = True;
		capabilities['tunnelIdentifier'] = os.environ["SC_PROXY_IDENTIFIER"];
		"""sauce labs"""
		capabilities = self._get_sauce_labs_options(capabilities);
		return capabilities;

	def _get_sauce_labs_options(self, capabilities: dict):
		""" If run_location_name is saucelabs, add these """
		if RunConfigs()._run_location_name.startswith('saucelabs'):
			sauce_options = {};
			sauce_options['username'] = os.environ["SAUCE_USERNAME"];
			sauce_options['accessKey'] = os.environ["SAUCE_ACCESS_KEY"];
			sauce_options['build'] = RunConfigs()._build_name;
			sauce_options['name'] = RunConfigs()._run_name + self.today_date();
			sauce_options['maxDuration'] = 1800;
			sauce_options['commandTimeout'] = 300;
			sauce_options['idleTimeout'] = 1000;
			capabilities["sauce:options"] = sauce_options;					
		return capabilities;

	def get_chrome_driver_local(self):
		base_directory = os.environ['BASE_DIRECTORY'];
		return ChromeDriver(executable_path=base_directory + "/chromedriver");

	def get_firefox_driver_local(self):
		base_directory = os.environ['BASE_DIRECTORY'];
		return FirefoxDriver(executable_path=base_directory + "/geckodriver");

	def _modify_driver(self, driver):
		driver = self._set_driver_window_size(driver);
		return driver;

	def _set_driver_window_size(self, driver):
		""" returns driver instance"""
		window_size_x = RunConfigs()._window_size_x;
		window_size_y = RunConfigs()._window_size_y;
		if (window_size_x is not None or window_size_y is not None):
			driver.set_window_size(int(window_size_x), int(window_size_y));
		return driver;