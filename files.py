# coding: utf-8

import datetime
import shutil
import os
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

directory = r'{}\tarif\\'.format(os.getcwd())
day_before = datetime.date.today() - datetime.timedelta(days=1)
seven_days_before = datetime.date.today() - datetime.timedelta(days=7)
weekday = datetime.date.today().weekday()  # определяем день недели
file_name = '{:%y_%m_%d}'.format(day_before)  # приобразовываем дату в название файла
server_dir = config['calls_server']['directory']
work_file = r'{}\{}.csv'.format(directory, file_name)


class DateFormat:
    """ Преобразование даты в необходимый вид и обратно """

    @staticmethod
    def calltouch_leads(date):
        """ Получаем дату в формате Calltouch для заявок - ГГГГ/ММ/ДД - str"""

        new_date = '{:%Y/%m/%d}'.format(date)
        return new_date

    @staticmethod
    def calltouch_calls(date):
        """ Получаем дату в формате Calltouch для звонков - ДД/ММ/ГГГГ - str"""

        new_date = '{:%d/%m/%Y}'.format(date)
        return new_date

    @staticmethod
    def calls_date(date):
        """ Получаем дату в формате ГГГГ-ММ-ДД - str"""

        new_date = '{:%Y-%m-%d}'.format(date)

        return new_date

    @staticmethod
    def filetodate(filename):
        """ Получаем дату по названию файла ГГ_ММ_ДД.csv - date"""

        year = int('20' + filename[0:2])
        month = int(filename[3:5])
        day = int(filename[6:8])

        return datetime.date(year, month, day)

    @staticmethod
    def filetoweek(filename):
        """ Получаем номер недели по названию файла ГГ_ММ_ДД.csv  """

        year = int('20' + filename[0:2])
        month = int(filename[3:5])
        day = int(filename[6:8])

        return datetime.date(year, month, day).isocalendar()[1]

    @staticmethod
    def strdate_to_week(str_date):
        """ Получаем номер недели по дате з строки """

        year = int(str_date.split('-')[0])
        month = int(str_date.split('-')[1])
        day = int(str_date.split('-')[2])

        return datetime.date(year, month, day).isocalendar()[1]

    @staticmethod
    def normal_date_calltouch(date):
        """ Приведение даты в формате Calltouch ДД/ММ/ГГГГ  к нормальному виду """

        year = int(date.split('/')[2])
        month = int(date.split('/')[1])
        day = int(date.split('/')[0])

        return datetime.date(year, month, day)

    @staticmethod
    def db_date_normal(db_date):
        """ Приведение даты из базы (str) в формате ГГГГ-ММ-ДД  к нормальному виду """

        year = int(db_date.split('-')[0])
        month = int(db_date.split('-')[1])
        day = int(db_date.split('-')[2])

        return datetime.date(year, month, day)

    @staticmethod
    def leads_deadline(date_time):
        """ Формирование дедлайна по времени заявке """

        date = date_time.split(' ')[0]
        time = date_time.split(' ')[1]

        dt_lead = datetime.datetime(year=int(date.split('/')[2]), month=int(date.split('/')[1]),
                                    day=int(date.split('/')[0]), hour=int(time.split(':')[0]),
                                    minute=int(time.split(':')[1]), second=int(time.split(':')[2]))

        if dt_lead < datetime.datetime(year=int(date.split('/')[2]), month=int(date.split('/')[1]),
                                       day=int(date.split('/')[0]), hour=9, minute=0, second=0):
            deadline = datetime.datetime(year=int(date.split('/')[2]), month=int(date.split('/')[1]),
                                         day=int(date.split('/')[0]), hour=10, minute=0, second=0)
        elif dt_lead > datetime.datetime(year=int(date.split('/')[2]), month=int(date.split('/')[1]),
                                         day=int(date.split('/')[0]), hour=20, minute=0, second=0):
            deadline = datetime.datetime(year=int(date.split('/')[2]), month=int(date.split('/')[1]),
                                         day=int(date.split('/')[0]), hour=10, minute=0, second=0) + datetime.timedelta(
                days=1)
        else:
            deadline = dt_lead + datetime.timedelta(hours=int(config['deadline']['hours']))
        return deadline


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


def weeks_start_dates(weeks):
    """ Создаем списки начальных дат по указанным неделям для последующего запроса из базы """

    weeks_start = [DateFormat.calls_date(res) for res in
                   time_gen((datetime.date.today() - datetime.timedelta(weeks=weeks)),
                            datetime.date.today(), datetime.timedelta(weeks=1))]
    return weeks_start


def weeks_end_dates(weeks):
    """ Создаем списки конечных дат по указанным неделям для последующего запроса из базы """

    weeks_end = [DateFormat.calls_date(res) for res in time_gen((day_before - datetime.timedelta(weeks=int(weeks - 1))),
                                                                datetime.date.today(), datetime.timedelta(weeks=1))]
    return weeks_end


def weeks_to_graph(weeks_start):

    weeks_list = [DateFormat.strdate_to_week(date) for date in weeks_start]
    return weeks_list

