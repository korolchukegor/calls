# coding: utf-8

import config
import db
from datetime_conversion import DateFormat
import sector as cs
import plot_ly

import logging
import requests
import time
import re
from sqlalchemy import func, or_, distinct


class LeadsAndCalls:
    """
    Class responsible for data processing of incoming leads and call from web site.
    """

    req = None
    type = None

    def request(self, date, type):
        """
        Request for leads
        """

        self.type = type
        check_date = None
        url = None

        if self.type == 'lead':
            check_date = DateFormat.calltouch_leads(date)
            url = config.URL_CALLTOUCH
        elif self.type == 'call':
            check_date = DateFormat.calltouch_calls(date)
            url = config.URL_CALLS_CALLTOUCH

        data = {

            'clientApiId': config.TOKEN_CALLTOUCH,
            'dateFrom': check_date,
            'dateTo': check_date
        }

        try:
            req_calltouch = requests.get(url, data, timeout=10)

        except requests.exceptions.RequestException as e:
            logging.warning('Calltouch request ERROR - {}'.format(e.args[0]))
            time.sleep(30)
            req_calltouch = requests.get(url, data, timeout=10)
        self.req = req_calltouch.json()

    def parse(self, session):
        """
        Parse json data and add to DB
        """
        try:
            for i in self.req:
                if self.type == 'lead':
                    datetime = DateFormat.tmstmp_datetime(i['order']['dateCreated'])
                    source = i['order']['session']['source']
                    medium = i['order']['session']['medium']
                    utm_content = i['order']['session']['utmContent']
                    utm_compaign = i['order']['session']['utmCampaign']
                    fio = i['client']['fio']
                    subject = i['subject']
                    department = self.subject_dept(subject)
                    keyword = i['order']['session']['keywords']
                    deadline = DateFormat.leads_deadline(datetime)
                    requestid = i['requestNumber']

                    if i['client']['phones']:
                        phone = i['client']['phones'][0]['phoneNumber']
                        if len(phone) == 7:
                            phone = '7812' + phone
                        telephone = self.dadata(phone)
                        if telephone:
                            status = 'Not called'
                        else:
                            status = 'No telephone'

                    else:
                        telephone = None
                        status = 'No telephone'

                    if i['client']['contacts']:
                        email = self.email_check(i['client']['contacts'][0]['contactValue'])
                    else:
                        email = None

                elif self.type == 'call':
                    if i['callerNumber'] == 'Anonymous':
                        continue
                    datetime = DateFormat.calltouch_str_date(i['date'])
                    source = i['source']
                    medium = i['medium']
                    utm_content = i['utmContent']
                    utm_compaign = i['utmCampaign']
                    fio = None
                    subject = None
                    keyword = i['keyword']
                    deadline = None
                    status = None
                    requestid = i['callId']
                    email = None
                    telephone = i['callerNumber']
                    department = self.call_dept(telephone, datetime, session)

                lead_or_call = db.Calltouch(datetime, self.type, department, telephone, email, source, medium, subject,
                                            fio,
                                            status, deadline, utm_content, utm_compaign, requestid, keyword)
                session.add(lead_or_call)
        except KeyError as e:
            logging.warning('Calltouch request parse problem {}'.format(e.args[0]))

    @staticmethod
    def report_leads(date_start, date_end, dept_num, session):
        """
        Counts calls by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]
        terms = [db.Calltouch.telephone.isnot(None), db.Calltouch.email.isnot(None)]

        query = session.query(db.Calltouch.telephone, db.Calltouch.email) \
            .group_by(db.Calltouch.telephone, db.Calltouch.email).filter(
            func.DATE(db.Calltouch.datetime).between(date_start, date_end),
            db.Calltouch.type == 'lead',
            or_(*terms),
            db.Calltouch.department == dept_name).count()

        return query

    @staticmethod
    def report_calls(date_start, date_end, dept_num, session):
        """
        Counts calls by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]
        dept_dict = dept[list(dept.keys())[0]]
        query = session.query(distinct(db.Calltouch.telephone)).group_by(db.Calltouch.telephone) \
            .join(db.Telephony).filter(func.DATE(db.Calltouch.datetime).between(date_start, date_end),
                                       db.Calltouch.type == 'call',
                                       db.Calltouch.department == dept_name,
                                       db.Telephony.duration >= dept_dict['time']).count()

        return query

    @staticmethod
    def subject_dept(subject):
        """
        Lead subject to name of department
        """

        for dept in range(len(config.DEPARTMENTS)):
            if subject in config.DEPARTMENTS[dept][list(config.DEPARTMENTS[dept].keys())[0]]['subjects']:
                return list(config.DEPARTMENTS[dept].keys())[0]
        else:
            return 'Unknown'

    @staticmethod
    def call_dept(phone, datetime, session):
        """
        Telephone to name of department
        """
        try:
            query = session.query(db.Telephony.department) \
                .filter(db.Telephony.telephone_from == phone,
                        func.DATE(db.Telephony.datetime) == func.DATE(datetime)).order_by(db.Telephony.datetime.desc())
            return query.first()[0]
        except TypeError:
            return 'Unknown'

    @staticmethod
    def dadata(tel_number):
        """
        Convert phone numbers in normal format. Paid feature!
        """

        data = [tel_number]

        headers = {

            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authorization': config.DADATA_TOKEN,
            'X-Secret': config.DADATA_SECRET

        }

        try:
            request = requests.post(config.DADATA_URL, json=data, headers=headers, timeout=10)

        except requests.exceptions.RequestException as e:
            logging.warning('DaDaTa request ERROR - {}'.format(e.args[0]))
            time.sleep(30)
            request = requests.post(config.DADATA_URL, json=data, headers=headers, timeout=10)

        js = request.json()

        try:
            datatel = js[0]['country_code'] + js[0]['city_code'] + js[0]['number']

        except TypeError:
            datatel = None

        return datatel

    @staticmethod
    def email_check(email):
        """
        Checking email address by the mask
        """

        try:
            re_mail = re.search(r'\w+@\w+\.\w+', email)
            result = re_mail.group(0)
        except AttributeError:
            result = None
        except TypeError:
            result = None

        return result


class Calltouch(cs.Sector):
    """
    Class responsible for for all activities related to telephony.
    """

    table = db.Calltouch

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        """
        This method gets all data from calltouch and adds it to DB
        """

        c_and_l = LeadsAndCalls()
        with db.session_scope() as session:
            c_and_l.request(date, type='lead')
            c_and_l.parse(session)
            c_and_l.request(date, type='call')
            c_and_l.parse(session)

    def report_data(self, date_start, date_end):
        """
        This method returns a list numbers of of calls and leads by departments
        """

        with db.session_scope() as session:
            calls = [LeadsAndCalls.report_calls(date_start, date_end, dept, session) for dept in
                     range(len(config.DEPARTMENTS))]
            leads = [LeadsAndCalls.report_leads(date_start, date_end, dept, session) for dept in
                     range(len(config.DEPARTMENTS))]

            return {'calls': calls, 'leads': leads}

    def plot_data(self):
        """
        This method create a plot with calls from site by weeks
        """

        title_calls = u'Входящие звонки с сайта'
        title_leads = u'Заявки с сайта'
        barmode = 'stack'
        pl = plot_ly.Plotly()
        dt = DateFormat()
        ct = Calltouch()

        plt_calls_data = list(zip(*[ct.report_data(dt_start, dt_end).get('calls') for dt_start, dt_end in
                                    zip(dt.weeks_start_dates(config.WEEKS_NUM), dt.weeks_end_dates(config.WEEKS_NUM))]))

        plt_leads_data = list(zip(*[ct.report_data(dt_start, dt_end).get('leads') for dt_start, dt_end in
                                    zip(dt.weeks_start_dates(config.WEEKS_NUM), dt.weeks_end_dates(config.WEEKS_NUM))]))

        data_calls = [pl.make_trace_bar(calls, list(dept.values())[0]['name']) for dept, calls in
                      zip(config.DEPARTMENTS, plt_calls_data)]

        data_leads = [pl.make_trace_bar(leads, list(dept.values())[0]['name']) for dept, leads in
                      zip(config.DEPARTMENTS, plt_leads_data)]

        return {'calls': pl.send_data_plot(data_calls, title_calls, barmode),
                'leads': pl.send_data_plot(data_leads, title_leads, barmode)}
