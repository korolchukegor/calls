# coding: utf-8

import datetime
import shutil
import os

directory = r'{}\tarif\\'.format(os.getcwd())  # рабочая директория
day_before = datetime.datetime.today() - datetime.timedelta(days=1)  # определяем вчерашний день
date_day_before = '{:%Y-%m-%d}'.format(day_before)
seven_days_before = datetime.datetime.today() - datetime.timedelta(days=7)  # определяем дату неделю назад
weekday = datetime.datetime.today().weekday()  # определяем день недели
file_name = '{:%y_%m_%d}'.format(day_before)  # приобразовываем дату в название файла
server_dir = r'\\VS\tarif\\'
work_file = r'{}\{}.csv'.format(directory, file_name)
weeks_years_list = []
weeks_to_graph = []


def copyfile(serverfile, workfile):
    """ Копируем файл на локальную машину """

    shutil.copyfile(serverfile, workfile)


def filetodate(filename):
    """ Получаем дату по названию файл """

    year = int('20' + filename[0:2])
    month = int(filename[3:5])
    day = int(filename[6:8])

    return datetime.date(year, month, day)


def filetoweek(filename):
    """ Получаем номер недели по названию файла """

    year = int('20' + filename[0:2])
    month = int(filename[3:5])
    day = int(filename[6:8])

    return datetime.date(year, month, day).isocalendar()[1]


def weeks_years(start, end, delta):
    """ Генератор временного промежутка """

    curr = start
    while curr < end:
        yield curr
        curr += delta
week = filetoweek(file_name)
year_now = '{:%Y}'.format(datetime.datetime.today())

for res in weeks_years((day_before - datetime.timedelta(weeks=50)), datetime.datetime.today(), datetime.timedelta(weeks=1)):
    weeks_years_list.append([int('{:%Y}'.format(res)), res.isocalendar()[1]])
    weeks_to_graph.append(res.isocalendar()[1])
