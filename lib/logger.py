
class Logger():

	def logs(self, log_entry, level='ALL'):
		if level=='ALL':
			print(str(log_entry));

	def log_fail(self, log_entry=None):
		log_entry = '[FAIL]:: %s' % (str(log_entry))
		self.logs(log_entry, level='ALL')

	def log_pass(self, log_entry=None):
		log_entry = '[PASS]:: %s' % (str(log_entry))
		self.logs(log_entry, level='ALL')