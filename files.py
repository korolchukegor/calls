# coding: utf-8

import datetime
import shutil
import os
import logging

directory = r'{}\tarif\\'.format(os.getcwd())  # рабочая директория
day_before = datetime.datetime.today() - datetime.timedelta(days=1)  # определяем вчерашний день
date_day_before = '{:%Y-%m-%d}'.format(day_before)
seven_days_before = datetime.datetime.today() - datetime.timedelta(days=7)  # определяем дату неделю назад
weekday = datetime.datetime.today().weekday()  # определяем день недели
file_name = '{:%y_%m_%d}'.format(day_before)  # приобразовываем дату в название файла
server_dir = r'\\VS\tarif\\'
work_file = r'{}\{}.csv'.format(directory, file_name)
weeks_start = []
weeks_end = []
weeks_to_graph = []

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s %(filename)s:%(lineno)d', level=logging.DEBUG, filename=u'log.log')


def copyfile(serverfile, workfile):
    """ Копируем файл на локальную машину """

    shutil.copyfile(serverfile, workfile)
    logging.info('copying {}'.format(workfile))

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


def time_gen(start, end, delta):
    """ Генератор временного промежутка """

    curr = start
    while curr < end:
        yield curr
        curr += delta


week = filetoweek(file_name)
year_now = '{:%Y}'.format(datetime.datetime.today())

for res in time_gen((datetime.datetime.today() - datetime.timedelta(weeks=50)), datetime.datetime.today(), datetime.timedelta(weeks=1)):
    weeks_start.append('{:%Y-%m-%d}'.format(res))
    weeks_to_graph.append(res.isocalendar()[1])

for res in time_gen((day_before - datetime.timedelta(weeks=49)), datetime.datetime.today(), datetime.timedelta(weeks=1)):
    weeks_end.append('{:%Y-%m-%d}'.format(res))



