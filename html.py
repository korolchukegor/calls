# coding: utf-8

import sqlite3
import logging
import files


def callsbyday(day_report, dept):
    """ Чтение данных за прошлый день из базы """

    day = files.DateFormat.calls_date(day_report)
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute("SELECT count(DISTINCT num) FROM calls WHERE date = (?) AND department = (?)", (day, dept))
    for i in c.fetchall():
        return i[0]

    conn.close()


def callsbyweek(dept, year, week):
    """ Чтение данных за прошлую неделю """

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT num) FROM calls WHERE department = (?) AND date LIKE '{}%' "
        "AND week == (?)".format(year), (dept, week))
    for i in c.fetchall():
        return i[0]

    conn.close()


def calltouch_by_day(date_report, dept, type):
    """ Чтение данных о заявках за прошлый день из базы """

    date = files.DateFormat.calls_date(date_report)
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT telephone) + count(DISTINCT email) FROM calltouch WHERE dept = (?) AND type = (?) AND date = (?)",
        (dept, type, date))
    result = c.fetchone()[0]
    conn.close()
    return result


def visits_by_day(date_report):
    """ Чтение данных о визитах сайта за прошлый день из базы """

    date = files.DateFormat.calls_date(date_report)
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute("SELECT medium, value FROM traffic WHERE date = ? GROUP BY medium", (date,))
    result = c.fetchall()
    conn.close()

    traf = {

        'Поиск': 'organic',
        'Реклама': 'cpc',
        'Прямые заходы': '(none)',
        'Email': 'email',
        'Переходы по ссылкам': 'referral',
        'Не определеено': '(not set)',

    }

    yesterday_traffic = [{name: i[1] for name, source in traf.items() if source == i[0]} for i in result]

    return yesterday_traffic


def calltouch_by_week(date_start, date_end, dept, type):
    """ Чтение данных о заявках за указанный период. На выходе str """

    date_start = files.DateFormat.calls_date(date_start)
    date_end = files.DateFormat.calls_date(date_end)

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = (?) AND type = (?) AND date BETWEEN (?) AND (?)",
        (dept, type, date_start, date_end))
    result = c.fetchone()[0]

    conn.close()
    return result


def check_callbacks(date_start, date_end, dept):
    """ Чтение данных об обзвонах заявок за указанный период """

    date_start = files.DateFormat.calls_date(date_start)
    date_end = files.DateFormat.calls_date(date_end)
    status = 'Not called'

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT telephone) FROM calltouch WHERE dept = (?) AND status = (?) AND date BETWEEN (?) AND (?)",
        (dept, status, date_start, date_end))
    result = c.fetchone()[0]

    conn.close()
    return result


def make_html(template, link,
              serv_calls_all, serv_leads, serv_calls, serv_no_callback,
              sales_calls_all, sales_leads, sales_calls, sales_no_callback,
              tradein_calls_all, tradein_leads, tradein_calls, tradein_no_callback,
              nfz_calls_all, nfz_leads, nfz_calls, nfz_no_callback,
              dop_calls_all, dop_leads, dop_calls, dop_no_callback,
              zch_calls_all, zch_leads, zch_calls, zch_no_callback,
              insurance_calls_all, insurance_leads, insurance_calls, insurance_no_callback):

    # TODO Сделать красиво (args)
    """ Формирование html по шаблону """

    global html_text

    with open('{}.html'.format(template), 'r', encoding='utf-8') as tp:
        html_text = tp.read().format(link=link,
                                     serv_calls_all=serv_calls_all,
                                     serv_leads=serv_leads,
                                     serv_calls=serv_calls,
                                     serv_no_callback=serv_no_callback,
                                     sales_calls_all=sales_calls_all,
                                     sales_leads=sales_leads,
                                     sales_calls=sales_calls,
                                     sales_no_callback=sales_no_callback,
                                     tradein_calls_all=tradein_calls_all,
                                     tradein_leads=tradein_leads,
                                     tradein_calls=tradein_calls,
                                     tradein_no_callback=tradein_no_callback,
                                     nfz_calls_all=nfz_calls_all,
                                     nfz_leads=nfz_leads,
                                     nfz_calls=nfz_calls,
                                     nfz_no_callback=nfz_no_callback,
                                     dop_calls_all=dop_calls_all,
                                     dop_leads=dop_leads,
                                     dop_calls=dop_calls,
                                     dop_no_callback=dop_no_callback,
                                     zch_calls_all=zch_calls_all,
                                     zch_leads=zch_leads,
                                     zch_calls=zch_calls,
                                     zch_no_callback=zch_no_callback,
                                     insurance_calls_all=insurance_calls_all,
                                     insurance_leads=insurance_leads,
                                     insurance_calls=insurance_calls,
                                     insurance_no_callback=insurance_no_callback)
    logging.info('html OK')
