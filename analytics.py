from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import configparser
import logging
import db
import files

config = configparser.ConfigParser()
config.read('config.ini')

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = 'https://analyticsreporting.googleapis.com/$discovery/rest'
KEY_FILE_LOCATION = config['analytics']['KEY_FILE_LOCATION']
SERVICE_ACCOUNT_EMAIL = config['analytics']['SERVICE_ACCOUNT_EMAIL']
VIEW_ID = config['analytics']['VIEW_ID']

depts = [

    {'service': config['analytics']['service'].split(',')},
    {'sales': config['analytics']['sales'].split(',')},
    {'tradein': config['analytics']['tradein'].split(',')},
    {'nfz': config['analytics']['nfz'].split(',')}
]


def initialize_analyticsreporting():
    """ Авторизация в аналитиксе """

    try:

        credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http())
        analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
        return analytics

    except Exception as e:
        logging.warning(e)


def get_report(analytics, date):
    """ Отправка запроса """

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': date, 'endDate': date}],
                    'metrics': [{'expression': 'ga:impressions'}, {'expression': 'ga:adClicks'},
                                {'expression': 'ga:adCost'}],
                    'dimensions': [{'name': 'ga:adwordsCustomerID'}, {'name': 'ga:adwordsCampaignID'},
                                   {'name': 'ga:adDistributionNetwork'}]

                }]
        }
    ).execute()


def get_report_traffic(analytics, date_start, date_end):
    """ Отправка запроса """

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': date_start, 'endDate': date_end}],
                    'dimensions': [{'name': 'ga:source'}, {'name': 'ga:medium'}]

                }]
        }
    ).execute()


def report_response(response):
    """ Чтение ответа """

    for report in response.get('reports', []):

        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        rows = report.get('data', {}).get('rows', [])
        report_data = []
        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])
            headers = [headers['name'] for headers in metricHeaders]
            dimensions_dict = {header: dimension for header, dimension in zip(dimensionHeaders, dimensions)}
            for values in dateRangeValues:
                dimensions_dict.update({header: value for header, value in zip(headers, values['values'])})
                report_data.append(dimensions_dict)

        return report_data


def adwords_to_db(report_data, date):
    """ Добавление данных из отчёта по adwords в базу данных """

    data_base = db.Database_manager()

    service_kms = {'shows': [], 'clicks': [], 'sum': []}
    service_search = {'shows': [], 'clicks': [], 'sum': []}
    sales_kms = {'shows': [], 'clicks': [], 'sum': []}
    sales_search = {'shows': [], 'clicks': [], 'sum': []}
    tradein_kms = {'shows': [], 'clicks': [], 'sum': []}
    tradein_search = {'shows': [], 'clicks': [], 'sum': []}
    nfz_kms = {'shows': [], 'clicks': [], 'sum': []}
    nfz_search = {'shows': [], 'clicks': [], 'sum': []}

    for dimensions_dict in report_data:

        type = dimensions_dict['ga:adDistributionNetwork']
        department = compaignid_to_dept(dimensions_dict['ga:adwordsCampaignID'])
        shows = int(dimensions_dict['ga:impressions'])
        clicks = int(dimensions_dict['ga:adClicks'])
        money = float(dimensions_dict['ga:adCost']) * 1.18

        if department == 'service' and type == 'Content':
            service_kms['shows'].append(shows)
            service_kms['clicks'].append(clicks)
            service_kms['sum'].append(money)

        elif department == 'service' and type != 'Content':
            service_search['shows'].append(shows)
            service_search['clicks'].append(clicks)
            service_search['sum'].append(money)

        elif department == 'sales' and type == 'Content':
            sales_kms['shows'].append(shows)
            sales_kms['clicks'].append(clicks)
            sales_kms['sum'].append(money)

        elif department == 'sales' and type != 'Content':
            sales_search['shows'].append(shows)
            sales_search['clicks'].append(clicks)
            sales_search['sum'].append(money)

        elif department == 'tradein' and type == 'Content':
            tradein_kms['shows'].append(shows)
            tradein_kms['clicks'].append(clicks)
            tradein_kms['sum'].append(money)

        elif department == 'tradein' and type != 'Content':
            tradein_search['shows'].append(shows)
            tradein_search['clicks'].append(clicks)
            tradein_search['sum'].append(money)

        elif department == 'nfz' and type == 'Content':
            nfz_kms['shows'].append(shows)
            nfz_kms['clicks'].append(clicks)
            nfz_kms['sum'].append(money)

        elif department == 'nfz' and type != 'Content':
            nfz_search['shows'].append(shows)
            nfz_search['clicks'].append(clicks)
            nfz_search['sum'].append(money)

    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'kms', 'service', sum(service_kms['shows']), sum(service_kms['clicks']),
                 round(sum(service_kms['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'search', 'service', sum(service_search['shows']), sum(service_search['clicks']),
                 round(sum(service_search['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'kms', 'sales', sum(sales_kms['shows']), sum(sales_kms['clicks']),
                 round(sum(sales_kms['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'search', 'sales', sum(sales_search['shows']), sum(sales_search['clicks']),
                 round(sum(sales_search['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'kms', 'tradein', sum(tradein_kms['shows']), sum(tradein_kms['clicks']),
                 round(sum(tradein_kms['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'search', 'tradein', sum(tradein_search['shows']), sum(tradein_search['clicks']),
                 round(sum(tradein_search['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'kms', 'nfz', sum(nfz_kms['shows']), sum(nfz_kms['clicks']),
                 round(sum(nfz_kms['sum']))))
    data_base.query("INSERT OR IGNORE INTO adwords VALUES (?, ?, ?, ?, ?, ?)",
                (date, 'search', 'nfz', sum(nfz_search['shows']), sum(nfz_search['clicks']),
                 round(sum(nfz_search['sum']))))


def traffic_to_db(report_data, date):
    """ Добавление данных из отчёта по трафику в базу данных """

    data_base = db.Database_manager()

    for dimensions_dict in report_data:

        data_base.query("INSERT OR IGNORE INTO traffic VALUES (?, ?, ?, ?)",
                        (date, dimensions_dict['ga:source'], dimensions_dict['ga:medium'],
                         dimensions_dict['ga:visits']))


def compaignid_to_dept(compaignid):
    """ Определение департамента по номеру кампании """

    for dept in depts:
        if compaignid in list(dept.values())[0]:
            return list(dept.keys())[0]


def analytics_report(date_report):
    """ Запуск скрипта """

    date = files.DateFormat.calls_date(date_report)
    analytics = initialize_analyticsreporting()

    try:
        adwords_to_db(report_response(get_report(analytics, date)), date)
        traffic_to_db(report_response(get_report_traffic(analytics, date, date)), date)

    except Exception as e:
        logging.warning(e)
