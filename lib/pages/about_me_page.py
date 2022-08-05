import selenium
from selenium.webdriver.firefox.webdriver import WebDriver
from lib.base_page import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import time

class AboutMePage(BasePage):

	PROPERTIES_FILE = "about_me_page.properties"

	def get_entry_content_text_content(self, driver):
		return self.get_element(driver, "entry_content").text;

	def get_entry_content_content_clean(self, driver):
		''' remove line breaks and white space '''
		content = self.get_entry_content_text_content(driver)
		return content.rstrip().lstrip().strip().replace('\r', ' ').replace('\n', ' ');

	def get_expected_entry_content_content_clean(self):
		return self.get_full_property_value('expected_about_me_page_content');
