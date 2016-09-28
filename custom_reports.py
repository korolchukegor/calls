# coding: utf-8

import config
import db
import sector as cs

import logging
from sqlalchemy import func, distinct, and_, or_


class Reports:
    """
    This class generates cross reports from multiple tables
    """

    @staticmethod
    def report_cpc(date_start, date_end, dept_num, session):
        """
        Counts CPC by departments
        """
        #  This is CPC by source type!!!
        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]

        query = session.query(db.Ads.source, db.Ads.source_type, func.sum(db.Ads.money), func.sum(db.Ads.clicks))\
            .filter(func.DATE(db.Ads.datetime).between(date_start, date_end), db.Ads.department == dept_name)\
            .group_by(db.Ads.source, db.Ads.source_type)

        return {dept_name: {'{} {}'.format(i[0], i[1]): round(i[2] / i[3], 2) for i in query.all() if i[3]}}

    @staticmethod
    def report_cpl(date_start, date_end, dept_num, session):
        """
        Counts CPL by departments
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]
        terms = [db.Calltouch.source == 'yandex', db.Calltouch.source == 'google']

        query = session.query(db.Ads.source, func.sum(db.Ads.money)) \
            .filter(func.DATE(db.Ads.datetime).between(date_start, date_end), db.Ads.department == dept_name) \
            .group_by(db.Ads.source).all()

        query2 = session.query(db.Calltouch.source, func.count(distinct(db.Calltouch.telephone)))\
            .filter(db.Calltouch.medium == 'cpc', func.DATE(db.Calltouch.datetime).between(date_start, date_end),
                    db.Calltouch.department == dept_name, or_(*terms)).group_by(db.Calltouch.source).all()
        return 'ads', query, 'ct', query2
        ads_source, money = query
        ct_source, value = query2


        # return dept_name, ads_source, money, ct_source, value
        # return {dept_name: {i[0]: round(i[2], 2) for i in query.all() if i[3]}}


class CustomData(cs.Sector):
    """
    Class responsible for for all custom activities related to several tables.
    """

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        pass  # No need because all data is already gotten

    def report_data(self, date_start, date_end):
        pass

    def plot_data(self):
        pass