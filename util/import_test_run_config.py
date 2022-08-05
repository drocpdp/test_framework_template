import os
import sys
import shutil

class ImportTestRunConfig(object):

	def __init__(self):
		print("in ImportTestRunConfig()");
		print (sys.argv);
		return;

	@property	
	def configs_test_run_dir(self):
		return os.environ['CONFIGS_TEST_RUNS'];

	@property
	def configs_run_config_file(self):
		return os.environ['RUN_CONFIG_XML'];
	

	@property
	def sys_args(self):
		return sys.argv;
	
	@property
	def test_run_file_name(self):
		return self.sys_args[1];
	
	def get_configs_test_run_file_name(self):
		return ("%s/%s" % (self.configs_test_run_dir,self.test_run_file_name));


	def main(self):
		test_run_file_name = self.get_configs_test_run_file_name();
		configs_run_config_file = self.configs_run_config_file;
		print (test_run_file_name);
		print (configs_run_config_file);
		shutil.copyfile(test_run_file_name, configs_run_config_file);
		return;



if __name__=="__main__":
	ImportTestRunConfig().main();
