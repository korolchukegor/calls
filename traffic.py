# coding: utf-8

import os
import config
import db
from datetime_conversion import DateFormat
import sector as cs

import logging
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2


def request_analytics(date_report, session):
    """
    Request for data from Google Analytics
    """
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    DISCOVERY_URI = 'https://analyticsreporting.googleapis.com/$discovery/rest'
    KEY_FILE_LOCATION = os.path.join(config.basedir, config.KEY_FILE_LOCATION)
    SERVICE_ACCOUNT_EMAIL = config.SERVICE_ACCOUNT_EMAIL
    VIEW_ID = config.VIEW_ID
    date = DateFormat.date_str(date_report)
    credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION,
                                                             scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)
    try:
        response = analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': date, 'endDate': date}],
                        'dimensions': [{'name': 'ga:source'}, {'name': 'ga:medium'}]

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

            for dimensions_dict in report_data:
                traffic = db.Traffic(date_report, dimensions_dict['ga:source'], dimensions_dict['ga:medium'],
                                     dimensions_dict['ga:visits'])
                session.add(traffic)

    except Exception as e:
        logging.warning(e)


class Traffic(cs.Sector):
    """
    Class responsible for data from Google Analytics.
    """

    table = db.Traffic

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        """
        This method gets all data from Google Analytics and adds it to DB
        """
        with db.session_scope() as session:
            request_analytics(date, session)

    def report_data(self, date_start, date_end):
        pass

    def plot_data(self):
        pass
