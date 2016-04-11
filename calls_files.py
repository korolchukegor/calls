# coding: utf-8

import datetime
import shutil
import os
import csv

directory = r'{}\tarif'.format(os.getcwd())                     # рабочая директория
today = datetime.datetime.today()                               # определяем дату сегодня
day = today                                                     # присваиваем значение по умолчанию
weekday = datetime.datetime.today().weekday()                   # определяем день недели
print('Сегодня: {} - {}'.format(today, weekday))
days_of_last_week = []                                          # тут будут дни прошлой недели
day_before = today - datetime.timedelta(days=1)                 # определяем вчерашний день
seven_days_before = today - datetime.timedelta(days=7)          # определяем дату неделю назад


file_name = '{:%y_%m_%d}'.format(day_before)                    # приобразовываем дату в название файла

shutil.copyfile(r'\\VS\tarif\{}.csv'.format(file_name),         # копируем файл на локальную машину
                r'{}\{}.csv'.format(directory, file_name))
csv_work_file = r'{}\{}.csv'.format(directory, file_name)

if weekday == 0:
    while day != seven_days_before:                             # заполняем список днями прошлой недели
        day = day - datetime.timedelta(days=1)
        days_of_last_week.append('{:%y_%m_%d}'.format(day))

    for day in days_of_last_week:
        day_of_week = open(directory + '\{}.csv'.format(day), 'r', newline='')
        callsreader = csv.reader(day_of_week, delimiter=';', quotechar='|')
        with open(directory + '\{}-{}.csv'.format('{:%y_%m_%d}'.format(seven_days_before),
                                                  '{:%y_%m_%d}'.format(day_before)), 'a', newline='') as week_calls:
            callswriter = csv.writer(week_calls, delimiter=';', quotechar='|')
            for i in callsreader:
                callswriter.writerow(i)

    csv_work_file2 = directory + '\{}-{}.csv'.format('{:%y_%m_%d}'.format(seven_days_before),
                                                 '{:%y_%m_%d}'.format(day_before))
