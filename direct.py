# coding: utf-8

import json
import configparser
import requests
import logging
import sqlite3
import files


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


def check_direct(dept, date_report, compaign_type):
    """ Получение данных из Яндекс.Директ и добавление в базу """

    date = files.DateFormat.calls_date(date_report)

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

    try:
        response = requests.post(url_direct, data=json.dumps(data, ensure_ascii=False).encode('utf8'), timeout=0.001)
        js = json.loads(response.text)
    except Exception as e:
        logging.warning('Direct request ERROR - {}'.format(e.args[0]))

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


    except KeyError as e:
        logging.warning('Direct request problem {}'.format(e.args[0]))


    try:
        conn = sqlite3.connect('dbtel.db')
        c = conn.cursor()

        c.execute("INSERT OR IGNORE INTO direct VALUES (?, ?, ?, ?, ?, ?)",
                  (date, compaign['type'], list(dept.keys())[0],
                   sum(compaign['shows']),
                   sum(compaign['clicks']),
                   round(sum(compaign['sum']) * 30)))

        conn.commit()
        conn.close()

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

    try:
        resp = requests.post(url_direct, data=json.dumps(data), timeout=0.001)
    except Exception as e:
        logging.warning('Direct request ERROR - {}'.format(e.args[0]))

    js = json.loads(resp.text)
    try:
        for pos in js['data']:
            return pos['CampaignID']

    except KeyError:
        pass