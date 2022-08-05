import os
import sys
import datetime
from configparser import ConfigParser
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from lib.run_configs import RunConfigs

class Emailer(object):
    
    PROPERTIES_FILE = os.environ["EMAILER_PROPERTIES_FILE"];
    REPORT_LOCATION = os.environ["EMAILER_REPORT_LOCATION"];
    
    def _get_property(self, config, section='default', private=False):
        """Gets properties. Also allows for private config file. This is not added to repository."""
        c = ConfigParser()
        if private:
            c.read(self.PRIVATE_CONFIG_FILE)
        else:
            c.read(self.PROPERTIES_FILE)
        return c.get(section, config)
    
    def today_date(self):
        date_s = str(datetime.datetime.now())
        return date_s
    
    @property
    def email(self):
        """Gets email login, address, etc. info from config file"""
        email = {}
        email['from'] = self._get_property('from', 'email')
        email['to'] = self._get_property('to', 'email')
        email['password'] = self._get_property('password', 'email')        
        return email

    def send_email(self, msg=''):
        #Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = "Automation Report for davidreynon.com - " + (self.today_date())
        outer['To'] = self.email['to']
        outer['From'] = self.email['from']

        # List of attachments
        attachments = [self.REPORT_LOCATION]

        # Add attachments to message
        for file in attachments:
            if os.path.exists(file):
                with open(file,'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition','attachment', filename=os.path.basename(file))
                outer.attach(msg)

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.email['from'], self.email['password'])
                s.sendmail(self.email['from'], self.email['to'], composed)
                s.close()
        except:
            print("Unable to send the email. Error: ", sys.exec_info()[0])
            raise

    def _form_email(self):
        outer = MIMEMultipart()
        outer['Subject']
        content = 'test'
        return content
    
    def main(self):
        self.send_email(self._form_email())

if __name__=="__main__":
    Emailer().main()
