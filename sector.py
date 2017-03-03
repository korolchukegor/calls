# coding: utf-8

import db
import datetime_conversion as dc
import config

from sqlalchemy import func, distinct
import logging
import datetime as dt


class Sector:
    """
    Abstract class responsible for data processing in the company
    """

    table = None

    def __init__(self):
        pass

    def get_data(self, date):
        raise NotImplementedError()

    def check_data(self):
        """
        Checking whether the lost days
        """
        table = self.table

        with db.session_scope() as session:
            query = session.query(func.count(distinct(func.strftime("%Y-%m-%d", table.datetime))))
            result = query.one()[0]

            if result <= 1:  # if base is empty or there is only one date

                logging.warning('{} table is empty'.format(table.__tablename__))
                date_from = dt.datetime.today() - dt.timedelta(weeks=config.WEEKS_NUM)
                date_to = dt.datetime.today() - dt.timedelta(days=1)
                dates = [date for date in
                         dc.DateFormat.date_range(date_from, date_to, dt.timedelta(days=1), inclusion=True)]
		
                
                for lost_date in dates:
                    self.get_data(lost_date)
                #sys.exit('DB is empty, dates are lost - {}'.format(dates))

            else:  # if base is NOT empty but there are not all dates
                query = session.query(distinct(func.DATE(table.datetime))).order_by(table.datetime.asc())
                call_list = [dt.datetime.strptime(i[0], '%Y-%m-%d').date() for i in query.all()]
                date_critical = (dt.datetime.today() - dt.timedelta(weeks=config.WEEKS_NUM)).date()
                yesterday = (dt.datetime.today() - dt.timedelta(days=1)).date()

                if call_list[0] > date_critical:  # if base dates less than the critical need
                    logging.warning(
                        'dates between {} and {} are lost'.format(date_critical, call_list[0]))
                    list_lost = [lost_date for lost_date in
                                 dc.DateFormat.date_range(date_critical, call_list[0] - dt.timedelta(days=1),
                                                          dt.timedelta(days=1), inclusion=True)]

                    for lost_date in list_lost:
                        self.get_data(lost_date)
                    #sys.exit('Dates are lost - {}'.format(list_lost))

                elif call_list[-1] < yesterday:  # if for some reason there is no yesterday's date and dates before it
                    logging.warning(
                        'dates between {} and {} are lost'.format(call_list[-1], yesterday))
                    list_lost = [lost_date for lost_date in
                                 dc.DateFormat.date_range(call_list[-1] + dt.timedelta(days=1), yesterday,
                                                          dt.timedelta(days=1), inclusion=True)]
                    for lost_date in list_lost:
                        self.get_data(lost_date)
                    #sys.exit('Dates are lost - {}'.format(list_lost))

                for index, item in enumerate(call_list, start=0):
                    try:
                        if call_list[index + 1] - dt.timedelta(days=1) != call_list[index]:
                            logging.warning(
                                'dates between {} and {} are lost'.format(call_list[index], call_list[index + 1]))

                            list_lost = [lost_date for lost_date in
                                         dc.DateFormat.date_range(call_list[index], call_list[index + 1],
                                                                  dt.timedelta(days=1))]
                           
                            for lost_date in list_lost:
                                self.get_data(lost_date)
                            #sys.exit('Dates are lost - {}'.format(list_lost))

                    except IndexError:
                        pass

    def report_data(self, date_start, date_end):
        raise NotImplementedError()

    def plot_data(self):
        raise NotImplementedError()



