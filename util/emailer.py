# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import base64
import datetime
import sys
from configparser import ConfigParser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileName, FileContent, \
                FileType, Disposition, ContentId, Personalization, Email, \
                Subject, Content
from lib.run_configs import RunConfigs
from xml_report_access import XMLReportAccess

class Emailer(object):
    
    REPORT_LOCATION = os.environ["CURRENT_REPORT_OUTPUT"];
    PROJECT_NAME = os.environ["PROJECT_NAME"];

    def __init__(self):
        """Initialize and populate empty Personalization() object"""
        self.personalization = Personalization();
        self.populate_personalization();

    def populate_personalization(self):
        """Populate values for TO and BCC(admin email)"""
        self.to_email();
        self.cc_email();
        self.bcc_email();


    def to_email(self):
        """Adds to email to Personalization() object"""
        to = RunConfigs()._email_report_to_addresses;
        tos = to.split(",");
        for t in tos:
            self.personalization.add_to(Email(t));
        return;

    def bcc_email(self):
        """Adds bcc email to Personalization() object"""
        bcc = RunConfigs()._email_report_bcc_emails;
        if bcc:
            bccs = bcc.split(",");
            for b in bccs:
                self.personalization.add_bcc(Email(b));
            return;

    def cc_email(self):
        """Adds cc email to Personalization() object"""
        cc = RunConfigs()._email_report_cc_emails;
        if cc:
            ccs = cc.split(",");
            for c in ccs:
                self.personalization.add_cc(Email(c));
            return;

    def from_email(self):
        return RunConfigs()._email_report_from_address;

    def today_date(self):
        date_s = str(datetime.datetime.now())
        return date_s

    def get_attachment(self):
        attachment = Attachment();

        file_path = self.REPORT_LOCATION;
        with open(file_path, 'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()

        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('text/html')
        attachment.file_name = FileName('report.html');        
        attachment.disposition = Disposition('attachment')

        return attachment;

    def send_email(self):
        singular_status = XMLReportAccess().get_singular_status();
        rp = XMLReportAccess().get_report_results_data_object();
        subject = "[%s] - Automation Report for %s - %s" % (singular_status, self.PROJECT_NAME, self.today_date());
        html_content = "<H1><strong>Automation Report for %s - %s</strong></H1>" % (self.PROJECT_NAME, singular_status);
        html_content += "<H4><BR/>Run on: %s</H4>" % self.today_date();
        html_content += "<BR/></BR/><H2><B>TOTAL TESTS:%s</B><BR/><H3>Fails:%s<BR/>Errors:%s<BR/>Skipped:%s</H3>" % (rp['tests'], rp['failures'], rp['errors'], rp['skip']);
        html_content += "<BR/><H6>See attached report.html for details.</H6>";
        mail_packet = Mail();
        mail_packet.from_email = (Email(self.from_email()));
        mail_packet.add_personalization(self.personalization);        
        mail_packet.subject = subject;
        mail_packet.add_content(Content("text/html", html_content));
        mail_packet.add_attachment(self.get_attachment());
        
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(mail_packet);
        except Exception as e:
            print(e.message)

    def main(self):
        print('NOTE::: -> in emailer.py. To re-enable emailer... remove from emailer.py - main() -> return statement')
        return
        self.send_email();

if __name__=="__main__":
    Emailer().main()