from lib.base_class import BaseClass
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class BasePage(BaseClass):
	
	def get_elements(self, driver, prop_lookup_key, exp_conds=None, timeout=15):
		""" later on, 
		def get_invisible_elements (...)
			exp_conds = EC.invisibility_of_elements;
			self.get_elements(driver, prop_lookup_key, exp_conds)
			
		 ... etc
		
		Attributes:
		------------
		driver: type WebDriver
		prop_lookup_key: str
		 	Key to lookup in .properties file.
		exp_conds: expected_conditions
		 	Override this later if needed
	 	timeout: int
	 		This gets passed from is_element_exist mostly. This is useful if 
	 		there are negative tests. We EXPECT it not to appear, so to wait for 
	 		something that we know will not appear is an inefficient use of time.
		"""
		if exp_conds is None:
			exp_conds = EC.visibility_of_any_elements_located;
		by_obj = self.getByObject(prop_lookup_key)
		property_string = self.get_property_lookup_value(prop_lookup_key)

		return WebDriverWait(driver, timeout).until(
			exp_conds((
				by_obj, property_string)));


	def get_element(self, driver, prop):
		elements = self.get_elements(driver, prop)
		element = elements[0]
		return element

	def is_element_exist(self, driver, prop):
		""" We are handling the TimeoutException here for usage in negative test cases
			We do not really expect a lengthy check nor an Exception message. We allow
			this because we need to wrap the get_elements() with expected_conditions.
			Maybe in the future we branch out and wrap this around a separate function.
			
			Attributes
			----------
			driver: type WebDriver
			prop: str
				string to pass to get_elements()
		"""
		try:
			is_exists = self.get_elements(driver, prop, timeout=5);
			return True;
		except TimeoutException:
			self.logs("TimeoutException thrown, Element NOT located.")
			return False;

	def getByObject(self, key) -> By:
		full_prop_string = self.get_full_property_value(key)
		string_parts = full_prop_string.split("=",1)		
		locator_map = {
			'css': By.CSS_SELECTOR,
			'id': By.ID,
			'link': By.LINK_TEXT,
			'class': By.CLASS_NAME,
			'name': By.NAME,
			'partiallink': By.PARTIAL_LINK_TEXT,
			'tagname': By.TAG_NAME,
			'xpath': By.XPATH
		}
		return locator_map[string_parts[0]];

	def go_to_page(self, driver):
		""" Child class inherits this, calling for its own url property
		"""
		driver.get(self.get_property('url'));

	def get_property_lookup_value(self, key):
		full_prop_string = self.get_full_property_value(key)
		string_parts = full_prop_string.split("=",1)
		return string_parts[1]		

	def is_on_current_page(self, driver):
		"""Some classes can override this method"""
		if self.is_element_exist(driver, 'is_on_current_page_indicator_element'):
			expected = self.get_full_property_value('is_on_current_page_indicator_element_value');
			val = self.get_element(driver,'is_on_current_page_indicator_element').text
			self.logs(expected);
			self.logs(val);
			if val == expected:
				return True;
		return False;

	def wait_for_exists(self, driver, prop, timeout=10, poll_frequency=0.25):
		interval = int(timeout / poll_frequency)
		for x in range(0,interval):
			if self.is_element_exist(driver, prop):
				print ('showed');
				return 
			print ('did not show');
			time.sleep(poll_frequency);
		raise NoSuchElementException('Element Not Found');

