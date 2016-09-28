# coding: utf-8

import config
import db
import datetime_conversion
from datetime_conversion import DateFormat
import sector as cs
import plot_ly

import logging
import shutil
import csv
from sqlalchemy import func, distinct


class Calls:
    """
    Class responsible for data processing of incoming and outgoing calls in the company.
    """

    @staticmethod
    def copyfiles(date):
        """
        Copying files with calls from server to local directory
        """

        filename = DateFormat.date_filename(date)
        shutil.copyfile(config.SERVER_DIR + filename, config.DIRECTORY_CALLS + filename)

    def parse_calls(self, date, session):
        """
        Parsing csv files with calls
        """
        # TODO Сделать нормальный путь
        with open('{}\{}'.format(config.DIRECTORY_CALLS, DateFormat.date_filename(date)), newline='') as csvfile:

            callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for i in callsreader:
                if len(i[2]) == 11 and i[2][0:1] == '8':
                    tel_from = '7' + i[2][1:]
                elif len(i[2]) == 10:
                    tel_from = '7' + i[2]
                else:
                    tel_from = i[2]

                if len(i[3]) == 11 and i[3][0:1] == '8':
                    tel_to = '7' + i[3][1:]
                elif len(i[3]) == 7:
                    tel_to = '7812' + i[3]
                else:
                    tel_to = i[3]

                dept = self.phone_dept(int(tel_to))

                try:
                    if i[1] == 'RX':
                        call_type = 'IN'
                    elif i[1] == 'TX':
                        call_type = 'OUT'
                    else:
                        call_type = i[1]

                    call = db.Telephony(DateFormat.str_datetime(i[0]), call_type, dept, tel_from, tel_to, i[4])
                    session.add(call)
                except ValueError as e:
                    logging.warning(u'Parsing problem - {}, {}'.format(i[7], e.args[0]))

    @staticmethod
    def report_calls(date_start, date_end, dept_num, session):
        """
        Counts calls by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]
        dept_dict = dept[list(dept.keys())[0]]

        query = session.query(func.count(distinct(db.Telephony.telephone_from))).filter(
            func.DATE(db.Telephony.datetime).between(date_start, date_end),
            db.Telephony.call_type == 'IN',
            db.Telephony.department == dept_name,
            db.Telephony.duration >= dept_dict['time'],
        )
        return query.one()[0]

    @staticmethod
    def phone_dept(tel):
        """
        Check department by telephone to.
        """

        for dept in config.DEPARTMENTS:
            dept_name = list(dept.keys())[0]
            dept_dict = dept[dept_name]
            int_nums = dept_dict['int_nums']

            if tel in int_nums:
                return dept_name
            else:
                continue
        else:
            return "Unknown"


class Telephony(cs.Sector):
    """
    Class responsible for for all activities related to telephony.
    """

    table = db.Telephony

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        """
        This method gets all data from telephony and adds it to DB
        """

        calls = Calls()

        with db.session_scope() as session:
            Calls.copyfiles(date)
            calls.parse_calls(date, session)

    def report_data(self, date_start, date_end):
        """
        This method returns a list of calls by departments
        """

        with db.session_scope() as session:
            rprt = [Calls.report_calls(date_start, date_end, dept, session) for dept in range(len(config.DEPARTMENTS))]

            return rprt

    def plot_data(self):
        """
        This method create a plot with calls by weeks
        """

        title = u'Все входящие звонки'
        barmode = 'stack'
        pl = plot_ly.Plotly()
        dc = datetime_conversion.DateFormat()
        plt_data = list(zip(*[self.report_data(dt_start, dt_end) for dt_start, dt_end in
                              zip(dc.weeks_start_dates(config.WEEKS_NUM), dc.weeks_end_dates(config.WEEKS_NUM))]))

        data = [pl.make_trace_bar(calls, list(dept.values())[0]['name']) for dept, calls in
                zip(config.DEPARTMENTS, plt_data)]

        return pl.send_data_plot(data, title, barmode)

