# coding: utf-8

import json
import configparser
import requests
import sqlite3
import logging
import files

config = configparser.ConfigParser()
config.read('config.ini')

url_calltouch = config['calltouch']['url']
url_calltouch_calls = config['calltouch']['urlcalls']
token_calltouch = config['calltouch']['token']

url_direct = config['yandex_direct']['url']
token_direct = config['yandex_direct']['token']
login_direct = config['yandex_direct']['login']

url_dadata = config['dadata']['url']
token_dadata = config['dadata']['token']
secret_dadata = config['dadata']['secret']


def calltouch_leads_request(date_report):
    """ Запрос данных по заявкам в Calltouch """

    check_date = files.DateFormat.calltouch_leads(date_report)

    data = {

        'clientApiId': token_calltouch,
        'dateFrom': check_date,
        'dateTo': check_date

    }

    req_calltouch = requests.get(url_calltouch, data)

    jdata = json.loads(req_calltouch.text)
    for i in jdata:
        # TODO Все операции с базой в отдельный модуль
        try:
            conn = sqlite3.connect('dbtel.db')
            c = conn.cursor()
            type = 'lead'
            lead_id = int(i['requestNumber'])
            date = i['dateStr']
            subject = i['subject']
            source = i['order']['session']['source']
            medium = i['order']['session']['medium']
            utm_content = bannerid_compaignid(i['order']['session']['utmContent'])
            keyword = i['order']['session']['keywords']
            fio = i['client']['fio']
            dept = subject_dept(i['subject'])

            try:
                email = 'None'
                oldphone = i['client']['phones'][0]['phoneNumber']
                if len(oldphone) == 7:
                    oldphone = '812' + oldphone

                phone = tel_datatel(oldphone)
                if phone is not None:
                    c.execute("INSERT OR IGNORE INTO calltouch VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                              (lead_id, date, subject, type, phone, email, source, medium, utm_content, keyword, fio,
                               dept))
            except TypeError:
                phone = 'None'
                email = i['client']['contacts'][0]['contactValue']
                c.execute("INSERT OR IGNORE INTO calltouch VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (lead_id, date, subject, type, phone, email, source, medium, utm_content, keyword, fio, dept))

            conn.commit()
            conn.close()
            logging.info('Direct data added OK')
        except sqlite3.Error as e:
            logging.warning('Error with adding to DB - {}'.format(e.args[0]))


def calltouch_calls_request(date_report):
    """ Запрос данных по звонкам в Calltouch """

    check_date = files.DateFormat.calltouch_calls(date_report)
    date_calls = files.DateFormat.calls_date(date_report)

    data = {

        'clientApiId': token_calltouch,
        'dateFrom': check_date,
        'dateTo': check_date

    }

    req_calltouch = requests.get(url_calltouch_calls, data)
    jdata = json.loads(req_calltouch.text)

    for i in jdata:

        try:
            conn = sqlite3.connect('dbtel.db')
            c = conn.cursor()

            type = 'call'
            email = 'None'
            subject = 'None'
            fio = 'None'
            call_id = int(i['callId'])
            date = i['date']
            phone = i['callerNumber']
            source = i['source']
            medium = i['medium']
            utm_content = bannerid_compaignid(i['utmContent'])
            keyword = i['keyword']
            dept = call_dept(phone, date_calls)

            c.execute("INSERT OR IGNORE INTO calltouch VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (call_id, date, subject, type, phone, email, source, medium, utm_content, keyword, fio, dept))

            conn.commit()
            conn.close()
            logging.info('Direct data added OK')

        except sqlite3.Error as e:
            logging.warning('Error with adding to DB - {}'.format(e.args[0]))


def bannerid_compaignid(bannerid):
    """ Преобразование номера объявления в номер кампании """

    data = {

        'method': 'GetBanners',
        'token': token_direct,
        "param": {

            'BannerIDS': [bannerid]
        }
    }
    resp = requests.post(url_direct, data=json.dumps(data))
    js = json.loads(resp.text)
    try:
        for pos in js['data']:
            return pos['CampaignID']

    except KeyError:
        pass


def tel_datatel(tel_number):
    """ Преобразование омер телефона в нормальный формат """

    data = [tel_number]

    headers = {

        'Accept': 'application/json',
        'Content-type': 'application/json',
        'Authorization': token_dadata,
        'X-Secret': secret_dadata

    }
    request = requests.post(url_dadata, data=json.dumps(data), headers=headers)
    js = json.loads(request.text)
    logging.info('DaDaTa status - {}'.format(request.status_code))
    try:
        datatel = js[0]['country_code'] + js[0]['city_code'] + js[0]['number']

    except TypeError:
        datatel = None

    return datatel


def subject_dept(subject):
    """ Преобразование темы заявки в название департамента """

    if subject in config['lead_subjects']['service'].split(','):
        return 'service'

    elif subject in config['lead_subjects']['sales'].split(','):
        return 'sales'

    elif subject in config['lead_subjects']['tradein'].split(','):
        return 'tradein'

    elif subject in config['lead_subjects']['nfz'].split(','):
        return 'nfz'

    elif subject in config['lead_subjects']['insurance'].split(','):
        return 'insurance'

    else:
        return 'other'


def call_dept(phone, date):
    """ Определение департамента по номеру телефона входящего зонка """

    phone = '8' + str(phone)[1:]
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    try:
        c.execute("SELECT department FROM calls WHERE num == (?) AND datetime == (?)", (phone, date))
        dept = c.fetchone()[0]
    except TypeError:
        dept = 'other'

    conn.close()
    return dept
