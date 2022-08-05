#!/bin/bash
export BASE_DIRECTORY=/opt/testing
#PROJECT_NAME is now bash_profile environment variable
export CONFIGS_LOCATION=$BASE_DIRECTORY/configs
export CONFIGS_TEST_RUNS=$CONFIGS_LOCATION/run_configs/test_runs
export RUN_CONFIG_XML=$CONFIGS_LOCATION/run_configs/$PROJECT_NAME.xml
export PROJECT_DIRECTORY=$BASE_DIRECTORY/$PROJECT_NAME
export CURRENT_REPORT_OUTPUT=$BASE_DIRECTORY/reports/$PROJECT_NAME.html
export CURRENT_REPORT_XML_OUTPUT=$BASE_DIRECTORY/reports/$PROJECT_NAME.xml
export ARCHIVE_REPORT_OUTPUT_DIRECTORY=$BASE_DIRECTORY/reports/old_reports
source $BASE_DIRECTORY/virtualenvs/$PROJECT_NAME/bin/activate
export PATH=$BASE_DIRECTORY/virtualenvs/$PROJECT_NAME/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PYTHONPATH=$PROJECT_DIRECTORY

# Set this depending on environment
export SAUCE_CONNECT_LOCATION=$PROJECT_DIRECTORY/util/sauce_connect/bin/linux/sc

export SC_PROXY_IDENTIFIER=sc-proxy-tunnel

# contains logic so that it will not run proxy if config has proxy set to False
python3 $PROJECT_DIRECTORY/lib/run_proxy.py stop
python3 $PROJECT_DIRECTORY/lib/run_proxy.py start

# import current/new test run config
python3 $PROJECT_DIRECTORY/util/import_test_run_config.py $1

# Test runs
nosetests -a "!mobile" --exe --with-html --html-file=$CURRENT_REPORT_OUTPUT $PROJECT_DIRECTORY --with-xunit --xunit-file=$CURRENT_REPORT_XML_OUTPUT

# contains logic so that it will not run proxy if config has proxy set to False
python3 $PROJECT_DIRECTORY/lib/run_proxy.py stop

# email out report
python3 $PROJECT_DIRECTORY/util/emailer_send_grid.py

# cleanup
file_name=$PROJECT_NAME.html
file_name_xml=$PROJECT_NAME.xml
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
new_fileName=$file_name.$current_time
new_fileName_xml=$file_name_xml.$current_time
mv $CURRENT_REPORT_OUTPUT $ARCHIVE_REPORT_OUTPUT_DIRECTORY/$new_fileName
mv $CURRENT_REPORT_XML_OUTPUT $ARCHIVE_REPORT_OUTPUT_DIRECTORY/$new_fileName_xml