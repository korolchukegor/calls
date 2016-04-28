# coding: utf-8

import sqlite3
import logging


def callsbyday(day, dept):
    """ Чтение данных за прошлый день из базы """

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


def make_html(template, serv, sales, tradein, nfz, dop, zch, ins):
    """ Формирование html по шаблону """

    global html_text
    with open('{}.html'.format(template), 'r', encoding='utf-8') as tp:
        html_text = tp.read().format(serv, sales, tradein, nfz, dop, zch, ins)
    logging.info('html OK')
