# coding: utf-8

import os
import datetime
import configparser
import logging


# main
basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read_file('config2.ini')

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s %(filename)s:%(lineno)d',
                    level=logging.WARNING, filename=os.path.join(basedir, u'log2.log'))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'neva.db')
DATE_REPORT = datetime.date.today() - datetime.timedelta(days=1)
WEEK_REPORT_DATE = datetime.date.today() - datetime.timedelta(days=7)
WEEKDAY = datetime.date.today().weekday()

DEPARTMENTS = [

    {'service': {

        'int_nums': list(map(int, config['int_dept_nums']['service'].split(','))),
        'time': int(config['seconds']['service']),
        'direct': config['yandex_direct']['service'].split(','),
        'analytics': config['analytics']['service'].split(','),
        'name': u'Сервис',
        'subjects': config['lead_subjects']['service'].split(',')

    }},
    {'sales': {

        'int_nums': list(map(int, config['int_dept_nums']['sales'].split(','))),
        'time': int(config['seconds']['sales']),
        'direct': config['yandex_direct']['sales'].split(','),
        'analytics': config['analytics']['sales'].split(','),
        'name': u'Продажи',
        'subjects': config['lead_subjects']['sales'].split(',')

    }},
    {'tradein': {

        'int_nums': list(map(int, config['int_dept_nums']['tradein'].split(','))),
        'time': int(config['seconds']['tradein']),
        'direct': config['yandex_direct']['tradein'].split(','),
        'analytics': config['analytics']['tradein'].split(','),
        'name': u'Trade-in',
        'subjects': config['lead_subjects']['tradein'].split(',')

    }},
    {'nfz': {

        'int_nums': list(map(int, config['int_dept_nums']['nfz'].split(','))),
        'time': int(config['seconds']['nfz']),
        'direct': config['yandex_direct']['nfz'].split(','),
        'analytics': config['analytics']['nfz'].split(','),
        'name': u'NFZ',
        'subjects': config['lead_subjects']['nfz'].split(',')

    }},
    {'dop': {

        'int_nums': list(map(int, config['int_dept_nums']['dop'].split(','))),
        'time': int(config['seconds']['dop']),
        'direct': config['yandex_direct']['dop'].split(','),
        'analytics': config['analytics']['dop'].split(','),
        'name': u'Доп. оборудование',
        'subjects': config['lead_subjects']['dop'].split(',')

    }},
    {'zch': {

        'int_nums': list(map(int, config['int_dept_nums']['zch'].split(','))),
        'time': int(config['seconds']['zch']),
        'direct': config['yandex_direct']['zch'].split(','),
        'analytics': config['analytics']['zch'].split(','),
        'name': u'Запчасти',
        'subjects': config['lead_subjects']['zch'].split(',')

    }},
    {'insurance': {

        'int_nums': list(map(int, config['int_dept_nums']['insurance'].split(','))),
        'time': int(config['seconds']['insurance']),
        'direct': config['yandex_direct']['insurance'].split(','),
        'analytics': config['analytics']['insurance'].split(','),
        'name': u'Страхование/кредит',
        'subjects': config['lead_subjects']['insurance'].split(',')

    }},
]

# telephony
DIRECTORY_CALLS = r'{}\\tarif\\'.format(basedir)  # Directory with csv files (calls)
# SERVER_DIR = config['calls_server']['directory']
FTP_HOST = config['ftp']['host']
FTP_LOGIN = config['ftp']['login']
FTP_PASSWORD = config['ftp']['password']

# callbacks
DIR_CALLBACKS = config['callbacks']['directory']
FILENAME_CALLBACKS = config['callbacks']['filename']
DL_HOURS = int(config['deadline']['hours'])

# direct
URL_DIRECT = config['yandex_direct']['url']
TOKEN_DIRECT = config['yandex_direct']['token']
TOKEN_DIRECT_PKW = config['yandex_direct']['token_pkw']
LOGIN_DIRECT = config['yandex_direct']['login']

# analytics
KEY_FILE_LOCATION = config['analytics']['KEY_FILE_LOCATION']
SERVICE_ACCOUNT_EMAIL = config['analytics']['SERVICE_ACCOUNT_EMAIL']
VIEW_ID = config['analytics']['VIEW_ID']

# plotly
WEEKS_NUM = int(config['plotly']['weeks_num'])
USERNAME_PLOTLY = config['plotly']['username']
API_KEY_PLOTLY = config['plotly']['api_key']

# email_report
# TEMPLATE = config['email_report']['template']
TEMPLATE = 'template2.html'
SMTP = config['email_report']['SMTP']
FROM_ADDR = config['email_report']['FROM_ADDR']
TO_ADDR = config['email_report']['TO_ADDR'].split(',')
TO_ADDR_DEBUG = config['email_report']['TO_ADDR_DEBUG'].split(',')
TO_ADDR_DEBUG2 = config['email_report']['TO_ADDR_DEBUG2'].split(',')
USERNAME = config['mail_login']['username']
PASSWORD = config['mail_login']['password']

# calltouch
URL_CALLTOUCH = config['calltouch']['url']
TOKEN_CALLTOUCH = config['calltouch']['token']
URL_CALLS_CALLTOUCH = config['calltouch']['urlcalls']

# dadata
DADATA_URL = url_dadata = config['dadata']['url']
DADATA_TOKEN = config['dadata']['token']
DADATA_SECRET = config['dadata']['secret']
