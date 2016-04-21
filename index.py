# coding: utf-8

import os
import csv
import sqlite3
import datetime
import re
import files

int_serv_nums = []
int_sales_nums = []
int_tradein_nums = []
int_nfz_nums = []
int_dop_nums = []
int_zch_nums = []
int_ins_nums = []

depts = [

    u'service',
    u'sales',
    u'tradein',
    u'nfz',
    u'dop',
    u'zch',
    u'insurance'
]


def read_config(int_dept_nums, colnum):
    """ Чтение файла  config """

    with open('config.csv', newline='') as csvfile:
        cells = csv.reader(csvfile, delimiter=';', quotechar='|')
        next(cells)

        for cell in cells:
            if cell[colnum] != '':
                int_dept_nums.append(int(cell[colnum]))


def check_phone(file, int_dept_nums, dept, week, time):
    """ Фильтрация csv-файла со звонками """

    print('Обрабатываю звонки и заношу в базу', dept)
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calls(id TEXT UNIQUE,
                                                    datetime TEXT,
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
                    c.execute("INSERT OR IGNORE INTO calls VALUES (?, ?, ?, ?, ?)", (idnum, i[0][0:10],
                                                                                     week, dept, i[2]))
            except ValueError:
                print(u'Неправильное значение номера - ', i[3])

    conn.commit()
    conn.close()


def read_base():
    """ Вывод всех данных из базы """

    conn = sqlite3.connect(u'dbtel.db')
    c = conn.cursor()

    c.execute("SELECT * FROM calls")
    for j in c.fetchall():
        print(j)

    conn.close()


def copy_and_add(lst, date_start, date_end):
    """ Копирование и обработка файлов """

    print('Копирую файлы')
    while True:
        date_start = date_start + datetime.timedelta(days=1)
        if date_start == date_end:
            break
        lst.append('{:%y_%m_%d}.csv'.format(date_start))

    for file in lst:
        week = files.filetoweek(file)
        files.copyfile(files.server_dir + file, files.directory + file)
        check_phone(files.directory + file, int_serv_nums, depts[0], week, 25)
        check_phone(files.directory + file, int_sales_nums, depts[1], week, 60)
        check_phone(files.directory + file, int_tradein_nums, depts[2], week, 45)
        check_phone(files.directory + file, int_nfz_nums, depts[3], week, 45)
        check_phone(files.directory + file, int_dop_nums, depts[4], week, 45)
        check_phone(files.directory + file, int_zch_nums, depts[5], week, 45)
        check_phone(files.directory + file, int_ins_nums, depts[6], week, 45)


def counter_days(directory):
    """ Первый запуск и проверка, не пропущены ли дни """

    files_list = []
    files_list_lost = []
    files_list_lastyear = []

    if len(os.listdir(directory)) <= 1:
        print('Папка пустая')
        date_last_year = datetime.datetime.today() - datetime.timedelta(days=365)
        date_of_file = datetime.datetime.today()
        copy_and_add(files_list_lastyear, date_last_year, date_of_file)

    else:
        print('Проверяю, все ли данные есть')
        for file in os.listdir(directory):
            if len(file) == 12:
                date_file = files.filetodate(file)
                files_list.append(date_file)

        for indx in range(len(files_list) - 1):
            if files_list[indx + 1] - datetime.timedelta(days=1) != files_list[indx]:
                date = files_list[indx]
                copy_and_add(files_list_lost, date, files_list[indx + 1])
