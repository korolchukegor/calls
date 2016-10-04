# coding: utf-8

import config
import db
from datetime_conversion import DateFormat
import sector as cs
import plot_ly

import logging
import requests
import os
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from sqlalchemy import func


class ShowsAndClicks:
    """
    Class responsible for data processing of ads.
    """

    @staticmethod
    def request_direct(date_report, dept_num):
        """
        Request for data from Yandex Direct
        """

        token = None

        if dept_num == 1:
            token = config.TOKEN_DIRECT_PKW
        elif dept_num != 1:
            token = config.TOKEN_DIRECT

        dept = config.DEPARTMENTS[dept_num]
        dept_compaigns = dept[list(dept.keys())[0]]['direct']
        dept_name = list(dept.keys())[0]
        date = DateFormat.date_str(date_report)

        data = {
            'method': 'GetSummaryStat',
            'token': token,
            'locale': 'ru',
            "param": {

                'CampaignIDS': dept_compaigns,
                'StartDate': date,
                'EndDate': date,
                'Currency': 'RUB',
                'IncludeVAT': 'Yes'
            }
        }

        try:
            request = requests.post(config.URL_DIRECT, json=data, timeout=10)

        except requests.exceptions.RequestException as e:
            logging.warning('Direct request ERROR - {}'.format(e.args[0]))
            request = requests.post(config.URL_DIRECT, json=data, timeout=10)

        return {dept_name: request.json()}

    def request_adwords(self, date_report, dept_num):
        """
        Request for data from Google Adwords
        """

        SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        DISCOVERY_URI = 'https://analyticsreporting.googleapis.com/$discovery/rest'
        KEY_FILE_LOCATION = os.path.join(config.basedir, config.KEY_FILE_LOCATION)
        SERVICE_ACCOUNT_EMAIL = config.SERVICE_ACCOUNT_EMAIL
        VIEW_ID = config.VIEW_ID

        dept = config.DEPARTMENTS[dept_num]
        dept_compaigns = dept[list(dept.keys())[0]]['analytics']
        dept_name = list(dept.keys())[0]

        try:
            date = DateFormat.date_str(date_report)
            credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION,
                                                                     scopes=SCOPES)
            http = credentials.authorize(httplib2.Http())
            analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

            response = analytics.reports().batchGet(
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

                list_by_dept = [i for i in report_data if i['ga:adwordsCampaignID'] in dept_compaigns]

                return {dept_name: list_by_dept}

        except Exception as e:
            logging.warning(e)

    @staticmethod
    def parse(request, date_report, session):
        """
        Parse json data and add to DB
        """

        g_dis_net = 'ga:adDistributionNetwork'

        for key, value in request.items():
            if key == 'drt':
                for dept_data in value:
                    dept = list(dept_data.keys())[0]
                    data = list(dept_data.values())[0]
                    if 'data' in data:
                        shows_s = sum(i["ShowsSearch"] for i in data['data'])
                        shows_c = sum(i["ShowsContext"] for i in data['data'])
                        clicks_s = sum(i["ClicksSearch"] for i in data['data'])
                        clicks_c = sum(i["ClicksContext"] for i in data['data'])
                        money_s = round(sum(i["SumSearch"] for i in data['data']) * 30, 2)  # include VAT
                        money_c = round(sum(i["SumContext"] for i in data['data']) * 30, 2)  # include VAT

                        search = db.Ads(date_report, 'yandex', 'search', dept, shows_s, clicks_s, money_s)
                        context = db.Ads(date_report, 'yandex', 'context', dept, shows_c, clicks_c, money_c)
                        session.add(search)
                        session.add(context)

            elif key == 'adw':
                for dept_data in value:
                    dept = list(dept_data.keys())[0]
                    data = list(dept_data.values())[0]
                    if data:
                        shows_s = sum(int(i['ga:impressions']) for i in data if i[g_dis_net] != 'Content')
                        shows_c = sum(int(i['ga:impressions']) for i in data if i[g_dis_net] == 'Content')
                        clicks_s = sum(int(i['ga:adClicks']) for i in data if i[g_dis_net] != 'Content')
                        clicks_c = sum(int(i['ga:adClicks']) for i in data if i[g_dis_net] == 'Content')
                        money_s = round(sum(float(i['ga:adCost']) for i in data if i[g_dis_net] != 'Content') * 1.18, 2)
                        money_c = round(sum(float(i['ga:adCost']) for i in data if i[g_dis_net] == 'Content') * 1.18, 2)

                        search = db.Ads(date_report, 'google', 'search', dept, shows_s, clicks_s, money_s)
                        context = db.Ads(date_report, 'google', 'context', dept, shows_c, clicks_c, money_c)
                        session.add(search)
                        session.add(context)

    @staticmethod
    def report_ctr(date_start, date_end, dept_num, session):
        """
        Counts CTR by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]

        query = session.query(func.sum(db.Ads.clicks), func.sum(db.Ads.shows)).filter(
            func.DATE(db.Ads.datetime).between(date_start, date_end),
            db.Ads.department == dept_name,
            db.Ads.source_type == 'search')
        try:
            return round(query.one()[0] / query.one()[1] * 100, 2)
        except TypeError:
            return 0

    @staticmethod
    def report_cpc(date_start, date_end, dept_num, session):
        """
        Counts CPC by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]

        query = session.query(func.sum(db.Ads.money), func.sum(db.Ads.clicks)).filter(
            func.DATE(db.Ads.datetime).between(date_start, date_end),
            db.Ads.department == dept_name)
        try:
            return round(query.one()[0] / query.one()[1], 2)
        except TypeError:
            return 0


class Ads(cs.Sector):
    """
    Class responsible for data from Yandex Direct and Google Adwords.
    """

    sc = ShowsAndClicks()
    table = db.Ads

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        """
        This method gets all data from ads and adds it to DB
        """

        with db.session_scope() as session:
            adwords = {'adw': [self.sc.request_adwords(date, dept) for dept in range(len(config.DEPARTMENTS))]}
            direct = {'drt': [self.sc.request_direct(date, dept) for dept in range(len(config.DEPARTMENTS))]}
            self.sc.parse(adwords, date, session)
            self.sc.parse(direct, date, session)

    def report_data(self, date_start, date_end):
        """
        This method returns a list of data by departments
        """

        with db.session_scope() as session:
            ctr = [self.sc.report_ctr(date_start, date_end, dept, session) for dept in range(len(config.DEPARTMENTS))]
            cpc = [self.sc.report_cpc(date_start, date_end, dept, session) for dept in range(len(config.DEPARTMENTS))]

            return {'ctr': ctr, 'cpc': cpc}

    def plot_data(self):
        """
        This method create a plot with ctr and cpc by weeks
        """

        title_ctr = u'CTR, %'
        title_cpc = u'CPC, p.'
        barmode = ''
        pl = plot_ly.Plotly()
        ads = Ads()
        dt = DateFormat()

        plt_ctr = list(zip(*[ads.report_data(dt_start, dt_end).get('ctr') for dt_start, dt_end in
                             zip(dt.weeks_start_dates(config.WEEKS_NUM), dt.weeks_end_dates(config.WEEKS_NUM))]))

        plt_cpc = list(zip(*[ads.report_data(dt_start, dt_end).get('cpc') for dt_start, dt_end in
                             zip(dt.weeks_start_dates(config.WEEKS_NUM), dt.weeks_end_dates(config.WEEKS_NUM))]))

        data_ctr = [pl.make_trace_line(ctr, list(dept.values())[0]['name']) for dept, ctr in
                    zip(config.DEPARTMENTS, plt_ctr)]

        data_cpc = [pl.make_trace_line(cpc, list(dept.values())[0]['name']) for dept, cpc in
                    zip(config.DEPARTMENTS, plt_cpc)]

        return {'ctr': pl.send_data_plot(data_ctr, title_ctr, barmode),
                'cpc': pl.send_data_plot(data_cpc, title_cpc, barmode)}
