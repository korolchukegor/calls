# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
from pandas import DataFrame
import sqlite3

matplotlib.rc('font', family='Arial')


with shelve.open('data') as db:
    print(db['Сервис'])
    print(db['Продажи'])


x = {'Сервис':[10,10,10,10,10,10,10], 'Продажи':[20,20,20,20,20,20,20], 'NFZ':[30,30,30,30,30,30,30], 'Trade-in':[32,14,27,25,14,14,13], 'Доп.оборудование':[32,35,27,25,74,43,96], 'Запчасти':[32,43,27,5,74,75,96], 'Страхование':[0,45,12,25,74,75,0]}
y = []
z = [1, 2, 3]
# Значения по оси X
#with open('test.txt') as day:
 #   for d in day.readlines():
 #       x.append(int(d))

print(x)

#df2 = DataFrame(randn(10, 5))
# Набор значений по оси Y

y = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Суб', 'Воскр']

df2 = DataFrame(x, index=y, columns=['Сервис', 'Продажи', 'NFZ', 'Trade-in', 'Доп.оборудование', 'Запчасти', 'Страхование'])

print(df2)

line_10 = df2.plot(kind='bar', stacked=True)





# Строим диаграмму

# Задаем исходные данные для каждой линии диаграммы, внешний вид линий и маркеров.
# Функция plot() возвращает кортеж ссылок на объекты класса matplotlib.lines.Line2D

#line_10 = plt.plot(x, y, 'bD:')

# Задаем интервалы значений по осям X и Y

#plt.axis([0, 100, 0, 100])

# Задаем заголовок диаграммы

plt.title(u'Звонки за период:')

# Задаем подписи к осям X и Y

plt.xlabel(u'Дата')
plt.ylabel(u'Звонки')

# Задаем исходные данные для легенды и ее размещение

#plt.legend(line_10, [u'Сервис'], loc='best')

# Включаем сетку

plt.grid()

# Сохраняем построенную диаграмму в файл

# Задаем имя файла и его тип

plt.savefig('spirit.png', format = 'png')
