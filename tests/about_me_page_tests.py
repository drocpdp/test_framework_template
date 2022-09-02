from lib.base_test_class import BaseTestClass
from lib.pages.about_me_page import AboutMePage
import time

class AboutMePageTests(BaseTestClass):

	def test_about_me_page_is_on_current_page(self):
		about_me = AboutMePage();
		about_me.go_to_page(self.driver);
		self.assertTrue(about_me.is_on_current_page(self.driver));
	
	"""
	def test_about_me_text_is_current_and_correct(self):
		about_me = AboutMePage();
		about_me.go_to_page(self.driver);
		actual_content = (about_me.get_entry_content_content_clean(self.driver));
		expected_content = (about_me.get_expected_entry_content_content_clean());
		self.assertEqual(actual_content,expected_content);
	"""