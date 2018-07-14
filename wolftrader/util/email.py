from wolftrader.application import gmail_account, gmail_password, gmail_port, gmail_stmp, \
    report_buy, report_sell, report_report, \
    wolf_logo, indicators_graph, rsi_graph, report_table
from wolftrader.util.logger import *
import smtplib

class EmailUtil:
    class_name = __file__

    def __init__(self):
        try:
            self.__email_account = gmail_account
            self.__email_password = gmail_password
            self.__port = gmail_port
            self.__smtp = gmail_stmp
            self.__server = smtplib.SMTP_SSL(self.__smtp, self.__port)
            self.__server.ehlo()
            self.__server.login(self.__email_account, self.__email_password)
            log_info('{} Successfully authenticated user {} '.format(EmailUtil.class_name, self.__email_account))
            log_debug('{} has been instantiated '.format(EmailUtil.class_name))
        except Exception as error:
            log_critical('{} error instantiating'.format(EmailUtil.class_name))

    def create_email(self, subject, receiver, body, template):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.image import MIMEImage
        from email.headerregistry import Address
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.__email_account
            msg['To'] = ','.join(receiver)
            msg.preamble = '''Your mail does not support the email format'''
            if template:
                with open(wolf_logo, 'rb') as wl:
                    logo = MIMEImage(wl.read(), 'png')
                    logo.add_header('Content-ID', '<wolfie>')
                    msg.attach(logo)
                if template == 'buy':
                    with open(report_buy, 'r') as rb:
                        body = MIMEText(rb.read(), 'html')
                        msg.attach(body)

                elif template == 'sell':
                    with open(report_sell, 'r') as rs:
                        body = MIMEText(rs.read(), 'html')
                        msg.attach(body)

                elif template == 'report':
                    with open(report_report, 'r') as r, \
                         open(indicators_graph, 'rb') as ig, \
                         open(rsi_graph, 'rb') as rg, \
                         open(report_table) as table:
                        indicators = MIMEImage(ig.read(), 'png')
                        rsi = MIMEImage(rg.read(), 'png')
                        indicators.add_header('Content-ID', '<indicators>')
                        rsi.add_header('Content-ID', '<rsi>')
                        body = MIMEText(r.read().replace('$table$', table.read()), 'html')
                        msg.attach(body)
                        msg.attach(indicators)
                        msg.attach(rsi)
                else:
                    log_error('No template specified')

            log_debug('{} email has been created successfully: \n {}'.format(EmailUtil.class_name, msg.as_string()))
            return msg
        except Exception as error:
            log_critical('{} creating email has failed, Error: {}'.format(EmailUtil.class_name, error))

    def send_email(self, subject, receiver, body, template):
        try:
            email = self.create_email(subject, receiver, body, template)
            self.__server.send_message(email, self.__email_account, receiver)
            log_info('{}, mail has been sent successfully to the following address(es): {}'.format(EmailUtil.class_name, receiver))
        except Exception as error:
            log_critical('{} error sending email'.format(EmailUtil.class_name))

    def __str__(self):
        return 'EmailUtil ---> {} {} {}'.format(self.__email_account, self.__port, self.__smtp)

    def __repr__(self):
        return 'EmailUtil() variables are read from a properties file'

