# coding: utf-8

import datetime
import shutil
import os
import logging
import configparser

# TODO Сделать файл красиво
config = configparser.ConfigParser()
config.read('config.ini')

directory = r'{}\tarif\\'.format(os.getcwd())
day_before = datetime.datetime.today() - datetime.timedelta(days=1)
seven_days_before = datetime.datetime.today() - datetime.timedelta(days=7)
weekday = datetime.datetime.today().weekday()  # определяем день недели
file_name = '{:%y_%m_%d}'.format(day_before)  # приобразовываем дату в название файла
server_dir = config['calls_server']['directory']
work_file = r'{}\{}.csv'.format(directory, file_name)
weeks_start = []
weeks_end = []
weeks_to_graph = []


class DateFormat:
    """ Преобразование даты в необходимый вид """

    @staticmethod
    def calltouch_leads(date):
        """ Calltouch запрос лидов """

        new_date = '{:%Y/%m/%d}'.format(date)
        return new_date

    @staticmethod
    def calltouch_calls(date):
        """ Calltouch запрос лидов """

        new_date = '{:%d/%m/%Y}'.format(date)
        return new_date

    @staticmethod
    def calls_date(date):
        """ Индексирование csv-файла со звонками """

        new_date = '{:%Y-%m-%d}'.format(date)
        return new_date

    @staticmethod
    def filetodate(filename):
        """ Получаем дату по названию файл """

        year = int('20' + filename[0:2])
        month = int(filename[3:5])
        day = int(filename[6:8])

        return datetime.date(year, month, day)

    @staticmethod
    def filetoweek(filename):
        """ Получаем номер недели по названию файла """

        year = int('20' + filename[0:2])
        month = int(filename[3:5])
        day = int(filename[6:8])

        return datetime.date(year, month, day).isocalendar()[1]


def copyfile(serverfile, workfile):
    """ Копируем файл на локальную машину """

    shutil.copyfile(serverfile, workfile)
    logging.info('copying {}'.format(workfile))


def time_gen(start, end, delta):
    """ Генератор временного промежутка """

    curr = start
    while curr < end:
        yield curr
        curr += delta


week = DateFormat.filetoweek(file_name)
year_now = '{:%Y}'.format(datetime.datetime.today())

for res in time_gen((datetime.datetime.today() - datetime.timedelta(weeks=50)), datetime.datetime.today(),
                    datetime.timedelta(weeks=1)):
    weeks_start.append('{:%Y-%m-%d}'.format(res))
    weeks_to_graph.append(str(res.isocalendar()[1]))

for res in time_gen((day_before - datetime.timedelta(weeks=49)), datetime.datetime.today(),
                    datetime.timedelta(weeks=1)):
    weeks_end.append('{:%Y-%m-%d}'.format(res))
