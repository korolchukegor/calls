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

traf = {

        'Поиск Яндекс': {'source': 'yandex', 'source_type': 'organic', 'quantity': [], 'by_weeks': []},
        'Поиск Google': {'source': 'google', 'source_type': 'organic', 'quantity': [], 'by_weeks': []},
        'Поиск Mail': {'source': 'go.mail.ru', 'source_type': 'organic', 'quantity': [], 'by_weeks': []},
        'Реклама Яндекс': {'source': 'yandex', 'source_type': ['cpc', 'cpc (yclid)'], 'quantity': [], 'by_weeks': [], 'cpl': [], 'money': []},
        'Реклама Google': {'source': 'google', 'source_type': ['cpc', 'cpc (gclid)'], 'quantity': [], 'by_weeks': [], 'cpl': [], 'money': []},
        'Реклама VK': {'source': 'vk', 'source_type': 'cpc', 'quantity': [], 'by_weeks': []},
        'Прямые заходы': {'source': '(direct)', 'source_type': '(none)', 'quantity': [], 'by_weeks': []},
        'Email': {'source': 'email', 'source_type': None, 'quantity': [], 'by_weeks': []},
        'Переходы по ссылкам': {'source': None, 'source_type': 'referral', 'quantity': [], 'by_weeks': []},
        'Остальное': {'source': 'Остальные', 'source_type': None, 'quantity': [], 'by_weeks': []},
        'Auto.ru': {'source': 'AUTORU', 'source_type': None, 'quantity': [], 'by_weeks': []}

    }

weeks_list = files.weeks_to_graph(files.weeks_start_dates(int(config['plotly']['weeks_num'])))
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


def read_base_cpl(date_start, date_end, table):

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query(
            "SELECT sum(money) FROM {} WHERE date BETWEEN (?) AND (?)".format(table),
            (day_start, day_end))
        result = data_base.result()[0]

        if table == 'direct':
            key = 'Реклама Яндекс'
        elif table == 'adwords':
            key = 'Реклама Google'

        traf[key]['money'].append(result)
        money = traf[key]['money']
        leads = traf[key]['by_weeks']
    try:
        traf[key]['cpl'] = list(map(lambda a, b: round(a / b),  money, leads))
    except TypeError as te:
        logging.warning('money in {} for that weeks are None'.format(table), te)
    except ZeroDivisionError as zde:
        logging.warning('leads in {} for that weeks are 0'.format(key), zde)


def read_base_ads_cr_contacts(date_start, date_end, dept_dict, dept):
    """ Чтение данных по количеству контактов и кликов из таблиц Calltouch, Direct и Adwords за указанный период """

    source_type = 'cpc'
    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query("SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = ? AND source_type = ? AND date BETWEEN (?) AND (?)",
            (dept, source_type, day_start, day_end))
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


def rb_leads_by_source(date_start, date_end):
    """ Чтение данных о заявках и звонках с сайта по источникам """

    data_base = db.Database_manager()
    for day_start, day_end in zip(date_start, date_end):
        data_base.query("SELECT count(DISTINCT telephone), source, source_type FROM calltouch WHERE date BETWEEN (?) AND (?) GROUP BY source, source_type",
                  (day_start, day_end))
        result = data_base.result_all()

        for i in result:

            if i[1] == 'AUTORU' and i[2] is None:
                traf['Auto.ru']['quantity'].append(i[0])

            elif i[1] == 'Остальные' and i[2] == '':
                traf['Остальное']['quantity'].append(i[0])

            elif i[2] == 'referral':
                traf['Переходы по ссылкам']['quantity'].append(i[0])

            elif i[1] == 'email':
                traf['Email']['quantity'].append(i[0])

        for name, values in traf.items():
            for i in result:
                try:
                    if i[1] == values['source'] and i[2] in values['source_type']:
                        values['quantity'].append(i[0])

                except TypeError:
                    pass
            traf[name]['by_weeks'].append(sum(values['quantity']))
            traf[name]['quantity'].clear()


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
            make_trace_line(insurance_dict['adwords'][data_type], name='Страхование Adwords')]

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


def send_data_plot_lines_cr(filename):
    """ Сборка и отправка данных графика """

    data = [make_trace_line(service_dict['cr_contacts'], name='Сервис'),
            make_trace_line(sales_dict['cr_contacts'], name='Продажи'),
            make_trace_line(tradein_dict['cr_contacts'], name='Trade-in'),
            make_trace_line(nfz_dict['cr_contacts'], name='NFZ'),
            make_trace_line(insurance_dict['cr_contacts'], name='Страхование')]


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


def sd_plot_lines_cpl(filename, data_type):
    """ Сборка и отправка данных графика """

    data = [make_trace_line(traf['Реклама Яндекс'][data_type], name='Реклама Яндекс'),
            make_trace_line(traf['Реклама Google'][data_type], name='Реклама Google'),
            ]

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


def sdplot_leads_by_source(filename):
    """ Сборка и отправка данных графика лидов по источникам"""

    data = [make_trace_bar(traf['Поиск Яндекс']['by_weeks'], name='Поиск Яндекс'),
            make_trace_bar(traf['Поиск Google']['by_weeks'], name='Поиск Google'),
            make_trace_bar(traf['Поиск Mail']['by_weeks'], name='Поиск Mail'),
            make_trace_bar(traf['Реклама Яндекс']['by_weeks'], name='Реклама Яндекс'),
            make_trace_bar(traf['Реклама Google']['by_weeks'], name='Реклама Google'),
            make_trace_bar(traf['Реклама VK']['by_weeks'], name='Реклама VK'),
            make_trace_bar(traf['Прямые заходы']['by_weeks'], name='Прямые заходы'),
            make_trace_bar(traf['Email']['by_weeks'], name='Email'),
            make_trace_bar(traf['Переходы по ссылкам']['by_weeks'], name='Переходы по ссылкам'),
            make_trace_bar(traf['Остальное']['by_weeks'], name='Остальное'),
            make_trace_bar(traf['Auto.ru']['by_weeks'], name='Auto.ru')
            ]

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


def create_dashboard(plot_url1, plot_url2, plot_url3, plot_url4, plot_url5, plot_url6, plot_url7, plot_url8):
    """ Отправляет данные в Dashboard """

    dashboard_json = {
        "rows": [
            [
                {"plot_url": plot_url1},
                {"plot_url": plot_url2},
                {"plot_url": plot_url3}
            ],

            [
                {"plot_url": plot_url4},
                {"plot_url": plot_url5},
                {"plot_url": plot_url6}
            ],

            [
                {"plot_url": plot_url7},
                {"plot_url": plot_url8}
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
    logging.info('https://dashboards.ly{}'.format(dashboard_url))
    return 'https://dashboards.ly{}'.format(dashboard_url)

