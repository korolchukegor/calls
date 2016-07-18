# coding: utf-8

import csv
import sqlite3
import datetime
import files
import logging
import configparser
import db
import direct
import calltouch
import re
import analytics


config = configparser.ConfigParser()
config.read('config.ini')

int_serv_nums = list(map(int, config['int_dept_nums']['service'].split(',')))
int_sales_nums = list(map(int, config['int_dept_nums']['sales'].split(',')))
int_tradein_nums = list(map(int, config['int_dept_nums']['tradein'].split(',')))
int_nfz_nums = list(map(int, config['int_dept_nums']['nfz'].split(',')))
int_dop_nums = list(map(int, config['int_dept_nums']['dop'].split(',')))
int_zch_nums = list(map(int, config['int_dept_nums']['zch'].split(',')))
int_ins_nums = list(map(int, config['int_dept_nums']['insurance'].split(',')))

depts = [

    u'service',
    u'sales',
    u'tradein',
    u'nfz',
    u'dop',
    u'zch',
    u'insurance'
]


def check_phone(file, int_dept_nums, dept, week, time):
    """ Фильтрация csv-файла со звонками """
    # TODO Переписать для одной общей таблицы

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calls(id TEXT UNIQUE,
                                                    date TEXT,
                                                    week INTEGER,
                                                    department TEXT,
                                                    num INTEGER)''')

    with open('{}'.format(file), newline='') as csvfile:

        callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for i in callsreader:
            if i[3] == u'НеваАвтоком':
                i[3] = u'2447788'
            elif i[2] == u'НеваСервис':
                i[2] = u'2447778'
            idnum = re.sub(r'[- :]', '', i[0]) + i[2] + i[3]

            try:
                if i[1] == u'RX' and int(i[3]) in int_dept_nums and int(i[4]) >= time:
                    c.execute("INSERT OR IGNORE INTO calls VALUES (?, ?, ?, ?, ?)", (idnum, i[0].split(' ')[0],
                                                                                     week, dept, i[2]))

            except ValueError as e:
                logging.warning(u'wrong number - {}, {}'.format(i[3], e.args[0]))

            if len(i[3]) == 7:
                i[3] = '8812' + i[3]
            try:
                if i[1] == u'TX':
                    c.execute("INSERT OR IGNORE INTO calls_out VALUES (?, ?, ?, ?, ?)", (idnum, i[0].split(' ')[0],
                                                                                         i[0].split(' ')[1], i[3],
                                                                                         i[4]))
            except ValueError:
                logging.warning(u'calls_back problem'.format(i[3]))

    conn.commit()
    conn.close()


def copy_and_add(date_start, date_end, table):
    """ Копирование и обработка файлов """

    lst = []
    if table == 'calls' or table == 'calls_out':
        while True:
            date_start = date_start + datetime.timedelta(days=1)
            if date_start == date_end:
                break
            lst.append('{:%y_%m_%d}.csv'.format(date_start))

        for file in lst:
            week = files.DateFormat.filetoweek(file)
            files.copyfile(files.server_dir + file, files.directory + file)
            check_phone(files.directory + file, int_serv_nums, depts[0], week, 25)
            check_phone(files.directory + file, int_sales_nums, depts[1], week, 60)
            check_phone(files.directory + file, int_tradein_nums, depts[2], week, 45)
            check_phone(files.directory + file, int_nfz_nums, depts[3], week, 45)
            check_phone(files.directory + file, int_dop_nums, depts[4], week, 45)
            check_phone(files.directory + file, int_zch_nums, depts[5], week, 45)
            check_phone(files.directory + file, int_ins_nums, depts[6], week, 45)

    elif table == 'direct':
        while True:
            date_start = date_start + datetime.timedelta(days=1)
            if date_start == date_end:
                break
            lst.append(date_start)

        for date in lst:
            direct.check_direct(direct.service, date, compaign_type='search')
            direct.check_direct(direct.sales, date, compaign_type='search')
            direct.check_direct(direct.tradein, date, compaign_type='search')
            direct.check_direct(direct.nfz, date, compaign_type='search')
            direct.check_direct(direct.insurance, date, compaign_type='search')
            direct.check_direct(direct.service, date, compaign_type='rsya')
            direct.check_direct(direct.sales, date, compaign_type='rsya')
            direct.check_direct(direct.tradein, date, compaign_type='rsya')
            direct.check_direct(direct.nfz, date, compaign_type='rsya')
            direct.check_direct(direct.insurance, date, compaign_type='rsya')

    elif table == 'adwords':
        while True:
            date_start = date_start + datetime.timedelta(days=1)
            if date_start == date_end:
                break
            lst.append(date_start)

        for date in lst:
            analytics.analytics_report(date)

    elif table == 'traffic':
        while True:
            date_start = date_start + datetime.timedelta(days=1)
            if date_start == date_end:
                break
            lst.append(date_start)

        for date in lst:
            analytics.analytics_report(date)

    elif table == 'calltouch':
        while True:
            date_start = date_start + datetime.timedelta(days=1)
            if date_start == date_end:
                break
            lst.append(date_start)

        for date in lst:
            calltouch.calltouch_leads_request(date)
            calltouch.calltouch_calls_request(date)


def base_days_lost(table):
    """ Первый запуск и проверка, не пропущены ли дни """

    data_base = db.Database_manager()
    data_base.query("SELECT count(DISTINCT date) FROM {}".format(table))
    result = data_base.result()

    if result[0] <= 1:

        logging.warning('{} table is empty'.format(table))
        date_last_year = datetime.datetime.today() - datetime.timedelta(days=100)
        date_of_file = datetime.datetime.today()
        copy_and_add(date_last_year, date_of_file, table)

    else:
        data_base.query("SELECT DISTINCT date FROM {} ORDER BY date ASC".format(table))

        call_list = [i[0] for i in data_base.result_all()]

        for index in range(len(call_list) - 1):
            date_index = files.DateFormat.db_date_normal(call_list[index])
            next_date_index = files.DateFormat.db_date_normal(call_list[index + 1])

            if next_date_index - datetime.timedelta(days=1) != date_index:
                logging.warning('dates between {} and {} are lost'.format(date_index, next_date_index))
                copy_and_add(date_index, next_date_index, table)

