# coding: utf-8

import sqlite3
import logging
import files


def callsbyday(day_report, dept):
    """ Чтение данных за прошлый день из базы """

    day = files.DateFormat.calls_date(day_report)
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute("SELECT count(DISTINCT num) FROM calls WHERE datetime == (?) AND department == (?)", (day, dept))
    for i in c.fetchall():
        return i[0]

    conn.close()


def callsbyweek(dept, year, week):
    """ Чтение данных за прошлую неделю """

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT num) FROM calls WHERE department == (?) AND datetime LIKE '{}%' "
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
        "SELECT count(DISTINCT id) FROM calltouch WHERE dept == (?) AND type == (?) AND date == (?)",
        (dept, type, date))
    result = c.fetchone()[0]
    conn.close()
    return result


def calltouch_by_week(date_start, date_end, dept, type):
    """ Чтение данных о заявках за прошлую неделю день из базы """

    date_start = files.DateFormat.calls_date(date_start)
    date_end = files.DateFormat.calls_date(date_end)

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute(
        "SELECT count(DISTINCT id) FROM calltouch WHERE dept == (?) AND type == (?) AND date BETWEEN (?) AND (?)",
        (dept, type, date_start, date_end))
    result = c.fetchone()[0]

    conn.close()
    return result

def make_html(template, link,
              serv_calls_all, serv_leads, serv_calls,
              sales_calls_all, sales_leads, sales_calls,
              tradein_calls_all, tradein_leads, tradein_calls,
              nfz_calls_all, nfz_leads, nfz_calls,
              dop_calls_all, dop_leads, dop_calls,
              zch_calls_all, zch_leads, zch_calls,
              insurance_calls_all, insurance_leads, insurance_calls):
    # TODO Сделать красиво (args)
    """ Формирование html по шаблону """

    global html_text

    with open('{}.html'.format(template), 'r', encoding='utf-8') as tp:
        html_text = tp.read().format(link=link,
                                     serv_calls_all=serv_calls_all,
                                     serv_leads=serv_leads,
                                     serv_calls=serv_calls,
                                     sales_calls_all=sales_calls_all,
                                     sales_leads=sales_leads,
                                     sales_calls=sales_calls,
                                     tradein_calls_all=tradein_calls_all,
                                     tradein_leads=tradein_leads,
                                     tradein_calls=tradein_calls,
                                     nfz_calls_all=nfz_calls_all,
                                     nfz_leads=nfz_leads,
                                     nfz_calls=nfz_calls,
                                     dop_calls_all=dop_calls_all,
                                     dop_leads=dop_leads,
                                     dop_calls=dop_calls,
                                     zch_calls_all=zch_calls_all,
                                     zch_leads=zch_leads,
                                     zch_calls=zch_calls,
                                     insurance_calls_all=insurance_calls_all,
                                     insurance_leads=insurance_leads,
                                     insurance_calls=insurance_calls)
    logging.info('html OK')
