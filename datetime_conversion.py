# coding: utf-8

import datetime
import config


class DateFormat:
    """
    Conversion of datetime to text and back
    """

    @staticmethod
    def calltouch_leads(date):
        """
        Conversion Calltouch leads text Date to YYYY/MM/DD str
        """

        return '{:%Y/%m/%d}'.format(date)

    @staticmethod
    def calltouch_calls(date):
        """
        Conversion Calltouch calls Date to DD/MM/YYYY str
        """

        return '{:%d/%m/%Y}'.format(date)

    @staticmethod
    def calltouch_str_date(str_date):
        """
        Conversion str to Date obj
        """

        return datetime.datetime.strptime(str_date, "%d/%m/%Y %H:%M:%S")

    @staticmethod
    def erp_str_date(str_date, str_time):
        """
        Conversion str to Date obj
        """

        return datetime.datetime.strptime(' '.join([str_date, str_time]), "%d.%m.%y %H:%M:%S")

    @staticmethod
    def str_datetime(str_date):
        """
        Conversion str to Datetime obj
        """

        return datetime.datetime.strptime(str_date, "%Y-%m-%d  %H:%M:%S")

    @staticmethod
    def tmstmp_datetime(tmstmp_datetime):
        """
        Conversion timestamp to Datetime obj
        """

        return datetime.datetime.fromtimestamp(tmstmp_datetime/1000.0)

    @staticmethod
    def str_date(str_date):
        """
        Conversion str to Date obj
        """

        return datetime.datetime.strptime(str_date, "%Y-%m-%d").date()

    @staticmethod
    def date_str(date):
        """
        Conversion Date obj to str
        """

        return datetime.datetime.strftime(date, '%Y-%m-%d')

    @staticmethod
    def str_week(str_date):
        """
        Conversion str to week
        """

        return datetime.datetime.strptime(str_date, "%Y-%m-%d").date().isocalendar()[1]

    @staticmethod
    def date_filename(date):
        """
        Conversion Date to full path filename \\y_m_d.csv
        """

        return r'{}.csv'.format('{:%y_%m_%d}'.format(date))

    @staticmethod
    def date_range(date_start, date_end, delta, inclusion=False):
        """
        Create a date range. Inclusion reflects to include date_start and date_end or not
        """

        if not inclusion:
            curr = date_start + delta
            while curr < date_end:
                yield curr
                curr += delta
        elif inclusion:
            curr = date_start
            while curr <= date_end:
                yield curr
                curr += delta

    def weeks_start_dates(self, weeks):
        """
        Create a list of the initial date for the specified week
        """

        weeks_start = [self.date_str(res) for res in
                       self.date_range((datetime.date.today() - datetime.timedelta(weeks=weeks)),
                                       datetime.date.today(), datetime.timedelta(weeks=1))]
        return weeks_start

    def weeks_end_dates(self, weeks):
        """
        Create a list of the final date for the specified week
        """

        day_before = datetime.date.today() - datetime.timedelta(days=1)
        weeks_end = [self.date_str(res) for res in
                     self.date_range((day_before - datetime.timedelta(weeks=int(weeks - 1))),
                                     datetime.date.today(), datetime.timedelta(weeks=1))]
        return weeks_end

    def weeks_to_graph(self, weeks_start):
        """
        Create a list of week numbers
        """

        weeks_list = [self.str_week(date) for date in weeks_start]
        return weeks_list

    @staticmethod
    def leads_deadline(dt_lead):
        """
        Forming deadline from lead datetime
        """

        if dt_lead < datetime.datetime.combine(dt_lead.date(), datetime.time(9, 0)):
            deadline = datetime.datetime.combine(dt_lead.date(), datetime.time(10, 0))
        elif dt_lead > datetime.datetime.combine(dt_lead.date(), datetime.time(20, 0)):
            deadline = datetime.datetime.combine(dt_lead.date(), datetime.time(10, 0)) + datetime.timedelta(days=1)
        else:
            deadline = dt_lead + datetime.timedelta(hours=int(config.DL_HOURS))
        return deadline
