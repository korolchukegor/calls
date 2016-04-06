# coding: utf-8

import csv
import sqlite3


int_serv_nums = []
int_sales_nums = []
int_tradein_nums = []
int_nfz_nums = []
int_dop_nums = []
int_zch_nums = []
int_ins_nums = []


def read_config(int_dept_nums, colnum):
    """ Чтение файла  config """

    with open('config.csv', newline='') as csvfile:
        cells = csv.reader(csvfile, delimiter=';', quotechar='|')
        next(cells)

        for cell in cells:
            if cell[colnum] != '':
                int_dept_nums.append(int(cell[colnum]))


serv = {'Сервис': []}
sales = {'Продажи': []}
tradein = {'Tradein': []}
nfz = {'NFZ': []}
dop = {'Доп': []}
zch = {'Запчасти': []}
ins = {'Страхование': []}


def check_phone(file, int_dept_nums, dept, time):
    """ Фильтрация csv-файла со звонками """

    with open('{}'.format(file), newline='') as csvfile:
        callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for i in callsreader:
            if i[1] == 'RX' and int(i[3]) in int_dept_nums and int(i[4]) >= time:
                addnums = [dept[key].append(i[2]) for key in dept]


def results(dept, file_name):
    """ Запись данных в базу """

    conn = sqlite3.connect('db.db')
    c = conn.cursor()

    for key in dept:
        c.execute('''CREATE TABLE IF NOT EXISTS {}(date TEXT UNIQUE, department TEXT, nums TEXT)'''.format(key))
        c.execute("INSERT OR IGNORE INTO {} VALUES (?, ?, ?)".format(key), (file_name, key, len(dept[key])))

    conn.commit()
    conn.close()


def make_html(template):
    """ Формирование html по шаблону """

    global html_text
    with open('{}.html'.format(template), 'r', encoding='utf-8') as tp:
        html_text = tp.read().format(len(serv['Сервис']), len(set(serv['Сервис'])),
                                     len(sales['Продажи']), len(set(sales['Продажи'])),
                                     len(tradein['Tradein']), len(set(tradein['Tradein'])),
                                     len(nfz['NFZ']), len(set(nfz['NFZ'])),
                                     len(dop['Доп']), len(set(dop['Доп'])),
                                     len(zch['Запчасти']), len(set(zch['Запчасти'])),
                                     len(ins['Страхование']), len(set(ins['Страхование'])))
