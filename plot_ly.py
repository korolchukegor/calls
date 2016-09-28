# coding: utf-8

import json
import logging

import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import requests

import config
import datetime_conversion


class Plotly:

    weeks_list = None

    def __init__(self):
        tls.set_credentials_file(username=config.USERNAME_PLOTLY, api_key=config.API_KEY_PLOTLY)
        dc = datetime_conversion.DateFormat()
        dates = dc.weeks_start_dates(config.WEEKS_NUM)
        self.weeks_list = dc.weeks_to_graph(dates)

    def make_trace_bar(self, y, name):
        """
        Method makes and returns a trace for Bar plot
        """
        trace = go.Bar(
            x=self.weeks_list, y=y, name=name
        )
        return trace

    def make_trace_line(self, y, name):
        """
        Method makes and returns a trace for Scatter plot
        """

        trace = go.Scatter(
            x=self.weeks_list, y=y, name=name, connectgaps=True
        )
        return trace

    @staticmethod
    def send_data_plot(data, title, barmode):
        """
        Method accumulates and send data to create a plot, returns a link to plot
        """

        layout = go.Layout(barmode=barmode, title=title, xaxis=dict(
            title=u'Недели',
            autorange=True,
            showgrid=False,
            zeroline=False,
            showline=False,
            autotick=True,
            ticks='',
            type='category',
            showticklabels=True))

        fig = go.Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename=title, sharing='public')
        logging.debug('Plot OK - {}'.format(plot_url))
        return plot_url

    @staticmethod
    def create_dashboard(*urls):
        """
        Method send plot urls to Dashboard and return a link to that Dashboard
        """

        # Consistently puts on two urls in a row
        rows = []
        for index in range(0, len(urls), 2):
            try:
                lst = [{"plot_url": urls[index]}, {"plot_url": urls[index + 1]}]
            except IndexError:
                lst = [{"plot_url": urls[index]}]
            rows.append(lst)

        dashboard_json = {
            "rows": rows,
            "banner": {
                "visible": True,
                "backgroundcolor": "#3d4a57",
                "textcolor": "white",
                "title": "Neva report",
                "links": []
            },
            "requireauth": False,
            "auth": {
                "username": "",
                "passphrase": ""
            }
        }

        try:
            response = requests.post('https://dashboards.ly/publish',
                                     data={'dashboard': json.dumps(dashboard_json)},
                                     headers={'content-type': 'application/x-www-form-urlencoded'}, timeout=10)
        except requests.exceptions.RequestException as e:
            logging.warning('Dashboard request ERROR - {}'.format(e.args[0]))
            response = requests.post('https://dashboards.ly/publish',
                                     data={'dashboard': json.dumps(dashboard_json)},
                                     headers={'content-type': 'application/x-www-form-urlencoded'}, timeout=10)

        response.raise_for_status()
        dashboard_url = response.json()['url']
        logging.debug('https://dashboards.ly{}'.format(dashboard_url))

        return 'https://dashboards.ly{}'.format(dashboard_url)
