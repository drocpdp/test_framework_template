from bs4 import BeautifulSoup
import os

class RunConfigs(object):

	def __init__(self):
		raw_content = open(os.environ['RUN_CONFIG_XML'], 'r');
		content = raw_content.read();
		bs = BeautifulSoup(content, "lxml-xml");
		self.bs = bs

	""" top level """
	def get_test_run_obj(self):
		return self.bs.testrun

	""" child of test_run """
	def get_current_run_obj(self):
		return self.get_test_run_obj().current_run;

	""" children of current_run_obj """
	def get_report_obj(self):
		return self.get_current_run_obj().report;

	def get_run_location_obj(self):
		return self.get_current_run_obj().run_location;

	def get_platform_obj(self):
		return self.get_current_run_obj().platform;

	def get_browser_obj(self):
		return self.get_current_run_obj().browser;

	""" children of get_platform_obj """
	def get_appium_obj(self):
		return self.get_platform_obj().appium;		


	""" property children """
	@property
	def _project_name(self):
		return self.get_current_run_obj().project_name.string;

	@property
	def _run_name(self):
		return self.get_current_run_obj().run_name.string;

	@property
	def _build_name(self):
		return self.get_current_run_obj().build_name.string;

	@property
	def _properties_section(self):
		""" properties file section other than default 
		for mobile testing """
		val = self.get_current_run_obj().properties_section;
		if val is not None:
			return val.string;
		return None;


	@property
	def _email_report_from_address(self):
		return self.get_report_obj().from_email.string;

	@property
	def _email_report_to_addresses(self):
		return self.get_report_obj().to_emails.string;

	@property
	def _email_report_cc_emails(self):
		val = self.get_report_obj().cc_emails;
		if val:
			return val.string;
		return None;

	@property
	def _email_report_bcc_emails(self):
		val = self.get_report_obj().bcc_emails;
		if val:
			return val.string;
		return None;		

	@property
	def _remote_or_local(self):
		return self.get_run_location_obj().remote_or_local.string;

	@property
	def _proxy(self):
		return self.get_run_location_obj().proxy.string;
	
	@property
	def _run_location_name(self):
		return self.get_run_location_obj().run_location_name.string;

	@property
	def _run_location_url(self):
		return self.get_run_location_obj().url.string;

	@property
	def _is_appium(self):
		val = self.get_platform_obj().is_appium;
		if val is not None:
			return val.string;
		return None;
	
	@property
	def _appium_appium_version(self):
		return self.get_appium_obj().appium_version.string;

	@property
	def _appium_device_name(self):
		return self.get_appium_obj().device_name.string;

	@property
	def _appium_device_orientation(self):
		return self.get_appium_obj().device_orientation.string;

	@property
	def _appium_platform_version(self):
		return self.get_appium_obj().platform_version.string;		

	@property
	def _appium_platform_name(self):
		return self.get_appium_obj().platform_name.string;					

	@property
	def _appium_browser_name(self):
		return self.get_appium_obj().browser_name.string;			

	@property
	def _platform_type(self):
		return self.get_platform_obj().type.string;

	@property
	def _platform_version(self):
		return self.get_platform_obj().version.string;

	@property
	def _browser_name(self):
		return self.get_browser_obj().browser_name.string;

	@property
	def _browser_version(self):
		return self.get_browser_obj().version.string;

	@property
	def _window_size_x(self):
		val = self.get_browser_obj().window_size_x;
		if val is not None:
			return val.string;
		return None;
	
	@property
	def _window_size_y(self):
		val = self.get_browser_obj().window_size_y;
		if val is not None:
			return val.string;
		return None;