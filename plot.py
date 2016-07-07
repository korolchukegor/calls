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

service_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
sales_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
tradein_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
nfz_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
dop_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
zch_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}
insurance_dict = {u'calls': [], 'adwords': {u'ctr': [], u'cpc': []}, 'direct': {u'ctr': [], u'cpc': []}, 'cr_contacts': []}


weeks_list = files.weeks_to_graph(files.weeks_start_dates(10))
dashboard_link = None


def clear_lst(*args):
    """ Очистка списков в словарях департаментов """

    for arg in args:
        arg.clear()


def read_base50(weeks_start, weeks_end, dict, dept):
    """ Чтение данных из базы за указанный период """

    data_base = db.Database_manager()
    for day_start, day_end in zip(weeks_start, weeks_end):
        data_base.query("SELECT count(DISTINCT num) FROM calls WHERE department = (?) AND date BETWEEN (?) AND (?)",
                        (dept, day_start, day_end))
        result = data_base.result()
        dict['calls'].append(int(result[0]))


def read_base_calltouch(date_start, date_end, dict, dept, type):
    """ Чтение данных из базы Calltouch за указанный период """

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query(
            "SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = ? AND type = ? AND date BETWEEN (?) AND (?)",
            (dept, type, day_start, day_end))
        result = data_base.result()
        dict['calls'].append(int(result[0]))


def read_base_ads_cpc(date_start, date_end, dept_dict, dept, table):
    """ Чтение данных по количеству кликов и потраченным деньгам из таблиц Direct и Adwords за указанный период """

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query(
            "SELECT sum(clicks), sum(money) FROM {} WHERE department = ? AND date BETWEEN (?) AND (?)".format(table),
            (dept, day_start, day_end))
        result_all = data_base.result_all()

        try:
            dept_dict[table]['cpc'].append(round(result_all[0][1]/result_all[0][0], 2))
        except ArithmeticError:
            dept_dict[table]['cpc'].append(0)
        except TypeError:
            dept_dict[table]['cpc'].append(0)


def read_base_ads_ctr(date_start, date_end, dept_dict, dept, table):
    """ Чтение данных по количеству показов и кликов из таблиц Direct и Adwords за указанный период """

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query(
            "SELECT sum(shows), sum(clicks) FROM {} WHERE type = 'search' AND department = ? AND date BETWEEN (?) AND (?)".format(table),
            (dept, day_start, day_end))
        result_all = data_base.result_all()

        try:
            dept_dict[table]['ctr'].append(round(result_all[0][1]/result_all[0][0] * 100, 2))
        except ArithmeticError:
            dept_dict[table]['ctr'].append(0)
        except TypeError:
            dept_dict[table]['ctr'].append(0)


def read_base_ads_cr_contacts(date_start, date_end, dept_dict, dept):
    """ Чтение данных по количеству контактов и кликов из таблиц Calltouch, Direct и Adwords за указанный период """

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query("SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = ? AND date BETWEEN (?) AND (?)",
            (dept, day_start, day_end))
        result_calltouch = data_base.result()[0]
        data_base.query("SELECT sum(clicks) FROM adwords WHERE department = ? AND date BETWEEN (?) AND (?)",
            (dept, day_start, day_end))
        result_adwords = data_base.result()[0]
        data_base.query("SELECT sum(clicks) FROM direct WHERE department = ? AND date BETWEEN (?) AND (?)",
            (dept, day_start, day_end))
        result_direct = data_base.result()[0]
        if not result_adwords:
            result_adwords = 0
        if not result_direct:
            result_direct = 0

        try:
            dept_dict['cr_contacts'].append(round((result_calltouch / (result_adwords + result_direct)) * 100, 2))
        except ArithmeticError:
            dept_dict['cr_contacts'].append(0)


def make_trace_bar(y, name):
    """ Создание блоков графика """

    trace = go.Bar(
        x=weeks_list, y=y, name='{}'.format(name)
    )
    return trace


def make_trace_line(y, name):
    """ Создание линий графика """

    trace = go.Scatter(
        x=weeks_list, y=y, name='{}'.format(name), connectgaps=True
    )
    return trace


def send_data_plot(filename):
    """ Сборка и отправка данных графика """

    data = [make_trace_bar(service_dict[u'calls'], name='Сервис'), make_trace_bar(sales_dict[u'calls'], name='Продажи'), make_trace_bar(tradein_dict[u'calls'], name='Trade-in'), make_trace_bar(nfz_dict[u'calls'], name='NFZ'),
            make_trace_bar(dop_dict[u'calls'], name='Доп. Оборудование'), make_trace_bar(zch_dict[u'calls'], name='Запчасти'), make_trace_bar(insurance_dict[u'calls'], name='Страхование')]

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


def send_data_plot_lines(filename, data_type):
    """ Сборка и отправка данных графика """

    data = [make_trace_line(service_dict['direct'][data_type], name='Сервис Direct'),
            make_trace_line(service_dict['adwords'][data_type], name='Сервис Adwords'),
            make_trace_line(sales_dict['direct'][data_type], name='Продажи Direct'),
            make_trace_line(sales_dict['adwords'][data_type], name='Продажи Adwords'),
            make_trace_line(tradein_dict['direct'][data_type], name='Trade-in Direct'),
            make_trace_line(tradein_dict['adwords'][data_type], name='Trade-in Adwords'),
            make_trace_line(nfz_dict['direct'][data_type], name='NFZ Direct'),
            make_trace_line(nfz_dict['adwords'][data_type], name='NFZ Adwords'),
            make_trace_line(insurance_dict['direct'][data_type], name='Страхование Direct'),
            make_trace_line(insurance_dict['adwords'][data_type], name='Страхование Adwords'),]

def send_data_plot_lines_cr(filename):
    """ Сборка и отправка данных графика """

    data = [make_trace_line(service_dict['cr_contacts'], name='Сервис'),
            make_trace_line(sales_dict['cr_contacts'], name='Продажи'),
            make_trace_line(tradein_dict['cr_contacts'], name='Trade-in'),
            make_trace_line(nfz_dict['cr_contacts'], name='NFZ'),
            make_trace_line(insurance_dict['cr_contacts'], name='Страхование'),]


    layout = go.Layout(title=filename, xaxis=dict(
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


def create_dashboard(plot_url1, plot_url2, plot_url3, plot_url4, plot_url5, plot_url6):
    """ Отправляет данные в Dashboard """

    dashboard_json = {
        "rows": [
            [{"plot_url": plot_url1},
             {"plot_url": plot_url2},
             {"plot_url": plot_url3},
             {"plot_url": plot_url4},
             {"plot_url": plot_url5},
             {"plot_url": plot_url6}
             ]

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
    return 'https://dashboards.ly{}'.format(dashboard_url)

