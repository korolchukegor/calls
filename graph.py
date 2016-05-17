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


def read_base50(dept, weeks_start, weeks_end):
    """ Чтение данных из базы за указанный период """

    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    for key in dept:
        for day_start, day_end in zip(weeks_start, weeks_end):
            c.execute("SELECT count(DISTINCT num) FROM calls WHERE department == (?) AND datetime BETWEEN (?) AND (?)",
                      (key, day_start, day_end))
            for j in c.fetchall():
                dept[key].append(int(j[0]))

    x.update(dept)
    conn.close()


def graphics():
    """ Строим график """

    # TODO Сделать дополнительный график линиями
    df2 = DataFrame(x, index=y, columns=[u'service', u'sales', u'tradein', u'nfz', u'dop', u'zch', u'insurance'])
    df2.plot(kind='bar', stacked=True, width=.8, figsize=(20, 20))
    plt.axis([-0.5, 49.5, 0, 1200])
    plt.title(u'Звонки по неделям:', {'fontname': 'Arial', 'fontsize': 20})  # Задаем заголовок диаграммы
    plt.xlabel(u'Недели', {'fontname': 'Arial', 'fontsize': 20})  # Задаем подписи к осям X и Y
    plt.ylabel(u'Звонки', {'fontname': 'Arial', 'fontsize': 20})
    plt.grid()  # Включаем сетку
    plt.savefig('spirit.png', format='png')  # Сохраняем построенную диаграмму в файл
