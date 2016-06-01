# coding: utf-8

import sqlite3
import json
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import requests
import configparser
import files
import logging

config = configparser.ConfigParser()
config.read('config.ini')

tls.set_credentials_file(username=config['plotly']['username'], api_key=config['plotly']['api_key'])

servdict = {u'service': []}
salesdict = {u'sales': []}
tradeindict = {u'tradein': []}
nfzdict = {u'nfz': []}
dopdict = {u'dop': []}
zchdict = {u'zch': []}
insdict = {u'insurance': []}

plot_url = None


def read_base50(dept, weeks_start, weeks_end):
    """ Чтение данных из базы за указанный период """

    conn = sqlite3.connect(r'dbtel.db')
    c = conn.cursor()
    for key in dept:
        for day_start, day_end in zip(weeks_start, weeks_end):
            c.execute("SELECT count(DISTINCT num) FROM calls WHERE department == (?) AND datetime BETWEEN (?) AND (?)",
                      (key, day_start, day_end))
            for j in c.fetchall():
                dept[key].append(int(j[0]))
# TODO fetchone
    conn.close()


def make_trace(dept):
    """ Создание блоков графика """

    for key in dept:
        trace = go.Bar(
            x=files.weeks_to_graph, y=dept[key], name='{}'.format(key)
        )

        return trace


def send_data_plot():
    """ Сборка и отправка данных графика """

    global plot_url
    data = [make_trace(servdict), make_trace(salesdict), make_trace(tradeindict), make_trace(nfzdict),
            make_trace(dopdict), make_trace(zchdict), make_trace(insdict)]
    layout = go.Layout(barmode='stack', xaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        type='category',
        showticklabels=True))
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='stacked-bar', sharing='secret')
    logging.info('Plot OK - {}'.format(plot_url))


# TODO вынести в отдельный модуль, т.к. будет отправлять все данные
def create_dashboard(plot_url):
    """ Отправляет данные в Dashboard """

    dashboard_json = {
        "rows": [
            [{"plot_url": plot_url}],

        ],
        "banner": {
            "visible": True,
            "backgroundcolor": "#3d4a57",
            "textcolor": "white",
            "title": "Quarterly Outlook",
            "links": []
        },
        "requireauth": False,
        "auth": {
            "username": "Acme Corp",
            "passphrase": ""
        }
    }

    response = requests.post('https://dashboards.ly/publish',
                             data={'dashboard': json.dumps(dashboard_json)},
                             headers={'content-type': 'application/x-www-form-urlencoded'})

    response.raise_for_status()
    dashboard_url = response.json()['url']
    logging.info('https://dashboards.ly{}'.format(dashboard_url))