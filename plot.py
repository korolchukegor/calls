# coding: utf-8

import json
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.tools as tls
import requests
import configparser
import files
import logging
import db

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

weeks_list = files.weeks_to_graph(files.weeks_start_dates(10))
dashboard_link = None

def clear_lst(*args):
    """ Очистка списков в словарях департаментов """

    for arg in args:
        for key in arg:
            arg[key].clear()


def read_base50(dept, weeks_start, weeks_end):
    """ Чтение данных из базы за указанный период """

    data_base = db.Database_manager()
    for key in dept:
        for day_start, day_end in zip(weeks_start, weeks_end):
            data_base.query("SELECT count(DISTINCT num) FROM calls WHERE department = (?) AND date BETWEEN (?) AND (?)",
                            (key, day_start, day_end))
            result = data_base.result()
            dept[key].append(int(result[0]))


def read_base_calltouch(date_start, date_end, dept, type):
    """ Чтение данных из базы Calltouch за указанный период """

    data_base = db.Database_manager()
    for key in dept:
        for day_start, day_end in zip(date_start, date_end):
            data_base.query(
                "SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = ? AND type = ? AND date BETWEEN (?) AND (?)",
                (key, type, day_start, day_end))
            result = data_base.result()
            dept[key].append(int(result[0]))


def make_trace(dept):
    """ Создание блоков графика """

    for key in dept:
        trace = go.Bar(
            x=weeks_list, y=dept[key], name='{}'.format(key)
        )

        return trace


def send_data_plot(filename):
    """ Сборка и отправка данных графика """

    data = [make_trace(servdict), make_trace(salesdict), make_trace(tradeindict), make_trace(nfzdict),
            make_trace(dopdict), make_trace(zchdict), make_trace(insdict)]

    layout = go.Layout(barmode='stack', title=filename, xaxis=dict(
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
    plot_url = py.plot(fig, filename=filename, sharing='public')
    logging.info('Plot OK - {}'.format(plot_url))
    return plot_url


def create_dashboard(plot_url1, plot_url2, plot_url3):
    """ Отправляет данные в Dashboard """

    dashboard_json = {
        "rows": [
            [{"plot_url": plot_url1},
             {"plot_url": plot_url2},
             {"plot_url": plot_url3}]

        ],
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

    response = requests.post('https://dashboards.ly/publish',
                             data={'dashboard': json.dumps(dashboard_json)},
                             headers={'content-type': 'application/x-www-form-urlencoded'})

    response.raise_for_status()
    dashboard_url = response.json()['url']
    logging.info('https://dashboards.ly{}'.format(dashboard_url))
    return ('https://dashboards.ly{}'.format(dashboard_url))
