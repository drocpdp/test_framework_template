import os, signal, sys
import time
import subprocess
from lib.run_configs import RunConfigs

class RunProxy(object):

	"""
	When Proxy starts, pid is written to serializable file.
	When Proxy is killed, file is deleted.

	Command line arguments -- start | stop
	"""

	def __init__(self):
		self.pid_location = os.environ['CONFIGS_LOCATION'] + '/pid.txt';

	def _is_pid_file_present(self):
		return os.path.isfile(self.pid_location);

	def _get_pid_of_proxy_from_file(self):
		f = open(self.pid_location, "r");
		pid = f.read().strip();
		return pid;

	def _write_pid_of_proxy_into_file(self, pid: str):
		f = open(self.pid_location, "w+");
		f.write(str(pid));
		return;

	def _delete_pid_file(self):
		try:
			os.remove(self.pid_location);
		except OSError:
			pass;

	def start_proxy(self):
		sauce_connect_location = os.environ['SAUCE_CONNECT_LOCATION'];
		sauce_username = os.environ['SAUCE_USERNAME'];
		sauce_access_key = os.environ['SAUCE_ACCESS_KEY'];
		sc_proxy_identifier = os.environ['SC_PROXY_IDENTIFIER'];		
		self.proxy_instance = subprocess.Popen([sauce_connect_location, '-u', sauce_username, '-k',sauce_access_key, '-i', sc_proxy_identifier]);
		""" record pid """
		self._write_pid_of_proxy_into_file(self.proxy_instance.pid);
		time.sleep(60);
		return;
		
	def stop_proxy(self):
		if self._is_pid_file_present():
			pid = self._get_pid_of_proxy_from_file();
			if pid == '':
				self._delete_pid_file();
				return;
			pid = int(pid);
			subprocess.Popen(['kill','-2',str(pid)]);
			self._delete_pid_file();
			time.sleep(60);
		return;

	def main(self):
		if RunConfigs()._proxy == 'True':
			if sys.argv[1] == 'start':
				self.start_proxy();
			elif sys.argv[1] == 'stop':
				self.stop_proxy();
			return;

if __name__=="__main__":
	RunProxy().main()




