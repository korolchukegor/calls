# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame
import sqlite3

matplotlib.rc('font', family='Arial')

x = {}
servdict = {'Сервис': []}
salesdict = {'Продажи': []}
tradeindict = {'Tradein': []}
nfzdict = {'NFZ': []}
dopdict = {'Доп': []}
zchdict = {'Запчасти': []}
insdict = {'Страхование': []}

def read_base(dept, days_of_last_week):
    """ Чтение данных из базы """

    conn = sqlite3.connect('db.db')
    c = conn.cursor()

    for key in dept:
        c.execute("SELECT nums FROM {} WHERE date IN ({})".format(key, ','.join(['?'] * len(days_of_last_week))),
                  days_of_last_week)

        for num in c.fetchall():
            dept[key].append(int(','.join(num)))

        x.update(dept)
    conn.close()
    return x


def graphics():
    """ Строим график """

    y = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суб', 'Воскр']
    df2 = DataFrame(x, index=y, columns=['Сервис', 'Продажи', 'Tradein', 'NFZ', 'Доп', 'Запчасти', 'Страхование'])
    df2.plot(kind='bar', stacked=True, figsize=(15, 15))
    plt.axis([-1, 7, 0, 300])
    plt.title(u'Звонки за прошлую неделю:', {'fontname': 'Arial', 'fontsize': 20})  # Задаем заголовок диаграммы
    plt.xlabel(u'Дата', {'fontname': 'Arial', 'fontsize': 20})                      # Задаем подписи к осям X и Y
    plt.ylabel(u'Звонки', {'fontname': 'Arial', 'fontsize': 20})
    plt.grid()                                                                      # Включаем сетку
    plt.savefig('spirit.png', format='png')                                         # Сохраняем построенную диаграмму в файл
