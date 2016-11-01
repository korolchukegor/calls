# coding: utf-8

import os
import smtplib
import logging
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

import config


class EmailReport:
    """
    Class responsible for creating and sending email reports
    """

    @staticmethod
    def html(telephony, calltouch_calls, calltouch_leads, num_lost_leads, lost_leads, late_leads, link):
        """
        Method creates html data for the letter
        """

        # Add another sector_report to zip
        items = [{list(dept.values())[0]['name']: [tel, call, lead, lost]} for dept, tel, call, lead, lost in
                 zip(config.DEPARTMENTS, telephony, calltouch_calls, calltouch_leads, num_lost_leads)]
        
        env = Environment(loader=FileSystemLoader(config.basedir))
        template = env.get_template(config.TEMPLATE)

        return template.render(link=link, items=items, lost_leads=lost_leads, late_leads=late_leads)

    @staticmethod
    def create_mail(from_addr, to_addr, subject, data):
        """
        Method generates a letter
        data - html text
        """

        msg = MIMEMultipart('related')
        msg['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
        msg['From'] = Header(from_addr.encode('utf-8'), 'UTF-8').encode()
        for t_a in to_addr:
            msg['To'] = Header(t_a.encode('utf-8'), 'UTF-8').encode()

        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)

        htmlpart = MIMEText(data.encode('utf-8'), 'html', 'UTF-8')
        msg_alternative.attach(htmlpart)

        return msg.as_string()

    @staticmethod
    def send_email(from_addr, to_addr, msg_as_string):
        """
        Method send a letter
        """

        server = smtplib.SMTP(config.SMTP)
        server.set_debuglevel(0)
        server.starttls()
        server.login(config.USERNAME, config.PASSWORD)
        server.sendmail(from_addr, to_addr, msg_as_string)
        server.quit()

