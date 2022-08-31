# using yagmail for access to GMail
import os
import base64
import datetime
import sys

import yagmail

from configparser import ConfigParser
from lib.run_configs import RunConfigs
from xml_report_access import XMLReportAccess

class Emailer(object):
    
    REPORT_LOCATION = os.environ["CURRENT_REPORT_OUTPUT"];
    PROJECT_NAME = os.environ["PROJECT_NAME"];

    def __init__(self):
        return

    def from_email(self):
        return RunConfigs()._email_report_from_address;

    def today_date(self):
        date_s = str(datetime.datetime.now())
        return date_s

    def send_email(self):
        singular_status = XMLReportAccess().get_singular_status();
        print(singular_status)
        rp = XMLReportAccess().get_report_results_data_object();
        print(self.from_email())
        print(self.today_date())

        try:
            email_pw = os.environ.get('EMAILER_GMAIL_PASSWORD')
        except Exception as e:
            print(e.message)        

        yag = yagmail.SMTP('pyautonotification@gmail.com', email_pw)
        contents = ['Test results attached']
        subject = "TEST RESULT - [{}] - {} - {}".format(self.PROJECT_NAME, singular_status, self.today_date())
        yag.send('davidreynon@gmail.com', subject , contents)


    def main(self):
        print('in emailer.py main()')
        self.send_email()



if __name__=="__main__":
    Emailer().main()