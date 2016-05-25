# coding: utf-8

import json
import configparser
import requests
import logging
import sqlite3
import re
import datetime
import time

config = configparser.ConfigParser()
config.read('config.ini')

url_direct = config['yandex_direct']['url']
token_direct = config['yandex_direct']['token']
login_direct = config['yandex_direct']['login']

service = {'service': config['yandex_direct']['service'].split(',')}
sales = {'sales': config['yandex_direct']['sales'].split(',')}
tradein = {'tradein': config['yandex_direct']['tradein'].split(',')}
nfz = {'nfz': config['yandex_direct']['nfz'].split(',')}
insurance = {'insurance': config['yandex_direct']['insurance'].split(',')}


def check_direct(dept, date, compaign_type):
    """ Получение данных из Яндекс.Директ и добавление в базу """

    compaign = {'type': compaign_type, 'shows': [], 'clicks': [], 'sum': []}

    data = {
        'method': 'GetSummaryStat',
        'token': token_direct,
        'locale': 'ru',
        "param": {

            'CampaignIDS': list(dept.values())[0],
            'StartDate': date,
            'EndDate': date,
            'Currency': 'RUB',
            'IncludeVAT': 'Yes'
        }
    }

    response = requests.post(url_direct, data=json.dumps(data, ensure_ascii=False).encode('utf8'))
    js = json.loads(response.text)
    try:
        for i in js['data']:
            if compaign_type == 'search':
                compaign['shows'].append(i["ShowsSearch"])
                compaign['clicks'].append(i["ClicksSearch"])
                compaign['sum'].append(i["SumSearch"])
            elif compaign_type == 'rsya':
                compaign['shows'].append(i["ShowsContext"])
                compaign['clicks'].append(i["ClicksContext"])
                compaign['sum'].append(i["SumContext"])

        logging.info('Direct request {} OK'.format(date))

    except KeyError:
        logging.warning('Direct request problem')


    try:
        conn = sqlite3.connect('dbtel.db')
        c = conn.cursor()
        id = re.sub(r'[- :]', '', date) + str(int(time.mktime(datetime.datetime.now().timetuple())))

        c.execute("INSERT OR IGNORE INTO direct VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (int(id), date, compaign['type'], list(dept.keys())[0],
                   sum(compaign['shows']),
                   sum(compaign['clicks']),
                   round(sum(compaign['sum']) * 30)))
        time.sleep(1)
        conn.commit()
        conn.close()
        logging.info('Direct data added OK')
    except sqlite3.Error as e:
        logging.warning('Error with adding to DB - {}'.format(e.args[0]))


def compaignid_bannerid(bannerid):
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