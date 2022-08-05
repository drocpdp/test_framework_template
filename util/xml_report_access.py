from bs4 import BeautifulSoup
import os

class XMLReportAccess(object):

	def __init__(self):
		raw_content = open(os.environ['CURRENT_REPORT_XML_OUTPUT'], 'r');
		content = raw_content.read();
		bs = BeautifulSoup(content, "lxml-xml");
		self.bs = bs

	def testing(self):
		print ("tests:", self._tests, " errors:", self._errors, " failures:", self._failures, " skip:", self._skip);
		print (self.get_singular_status());


	def get_testsuite_object(self):
		return self.bs.testsuite;

	@property
	def _tests(self):
		"""number of tests total"""
		return self.get_testsuite_object()['tests'];	


	@property
	def _errors(self):
		"""number of tests error"""
		return self.get_testsuite_object()['errors'];

	@property
	def _failures(self):
		"""number of tests failed"""
		return self.get_testsuite_object()['failures'];

	@property
	def _skip(self):
		"""number of tests skipped"""
		return self.get_testsuite_object()['skip'];		

	def get_report_results_data_object(self):
		"""helper method"""
		tests = self._tests;
		errors = self._errors;
		failures = self._failures;
		skip = self._skip;
		return {'tests':tests, 'errors':errors, 'failures':failures, 'skip':skip};

	def get_singular_status(self):
		"""helper method"""
		if int(self._tests) == 0:
			return 'NO TESTS RUN';
		if int(self._errors) > 0:
			return 'ERRORS';
		if int(self._failures) > 0:
			return 'FAILED';
		return 'PASSED';


if __name__=="__main__":
	XMLReportAccess().testing();