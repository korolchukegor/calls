# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame
import sqlite3
import files

matplotlib.rc('font', family='Arial')

x = {}
y = files.weeks_to_graph

servdict = {u'service': []}
salesdict = {u'sales': []}
tradeindict = {u'tradein': []}
nfzdict = {u'nfz': []}
dopdict = {u'dop': []}
zchdict = {u'zch': []}
insdict = {u'insurance': []}


def read_base50(dept, weeks_years_list):
    """ Чтение данных из базы за 50 недель """

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    for lst in weeks_years_list:
        week = lst[1]
        year = lst[0]
        for key in dept:
            c.execute("SELECT count(DISTINCT num) FROM calls WHERE department == (?) AND datetime LIKE '{}%' "
                      "AND week == (?)".format(year), (key, week))
            for i in c.fetchall():
                dept[key].append(int(i[0]))

    x.update(dept)
    conn.close()


def graphics():
    """ Строим график """

    df2 = DataFrame(x, index=y, columns=[u'service', u'sales', u'tradein', u'nfz', u'dop', u'zch', u'insurance'])
    df2.plot(kind='bar', stacked=True, width=.8, figsize=(20, 20))
    plt.axis([-0.5, 50.5, 0, 1200])
    plt.title(u'Звонки по неделям:', {'fontname': 'Arial', 'fontsize': 20})  # Задаем заголовок диаграммы
    plt.xlabel(u'Недели', {'fontname': 'Arial', 'fontsize': 20})  # Задаем подписи к осям X и Y
    plt.ylabel(u'Звонки', {'fontname': 'Arial', 'fontsize': 20})
    plt.grid()  # Включаем сетку
    plt.savefig('spirit.png', format='png')  # Сохраняем построенную диаграмму в файл
