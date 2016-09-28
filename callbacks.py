# coding: utf-8

from sqlalchemy import func, or_

import db
import config
import sector as cs


class CheckCallBacks:
    """
    This class responsible for checking whether all leads are called back
    """
    # TODO Переделать все 2 запросами вместо join
    @staticmethod
    def check_status(date_report, session):
        """
        Finds lead in db and check its status
        """

        query = session.query(func.min(db.Calltouch.datetime), func.min(db.Telephony.datetime), db.Telephony.duration,
                              db.Calltouch.telephone, db.Calltouch.status, db.Calltouch.deadline) \
            .join(db.Telephony, db.Telephony.telephone_to == db.Calltouch.telephone) \
            .filter(func.DATE(db.Calltouch.deadline) == date_report, func.DATE(db.Telephony.datetime) == date_report,
                    db.Telephony.datetime > db.Calltouch.datetime).group_by(db.Calltouch.telephone)

        for i in query.all():
            lead_date, call_date, duration, telephone, status, deadline = i

            if duration <= 40 and call_date <= deadline:
                status = 'Short call'
            elif duration >= 40 and call_date > deadline:
                status = 'Late call'
            elif duration <= 40 and call_date > deadline:
                status = 'Short and Late call'
            elif duration >= 40 and call_date <= deadline:
                status = 'Good call'
            else:
                status = 'Bad call'
            session.query(db.Calltouch).filter(db.Calltouch.datetime == lead_date,
                                               db.Calltouch.telephone == telephone).update({'status': status},
                                                                                           synchronize_session=False)

    @staticmethod
    def not_called(date_start, date_end, session):
        """
        Return calls without callback
        """

        query = session.query(db.Calltouch.datetime, db.Calltouch.telephone, db.Calltouch.fio, db.Calltouch.department) \
            .filter(func.DATE(db.Calltouch.deadline).between(date_start, date_end), db.Calltouch.status == 'Not called',
                    ).group_by(db.Calltouch.telephone)

        return [(str(i[0]).split('.')[0], i[1], i[2], i[3]) for i in query.all()]

    @staticmethod
    def not_called_count(date_start, date_end, dept_num, session):
        """
        Return calls without callback
        """

        dept = config.DEPARTMENTS[dept_num]
        dept_name = list(dept.keys())[0]

        query = session.query(db.Calltouch.datetime, db.Calltouch.telephone, db.Calltouch.fio) \
            .filter(func.DATE(db.Calltouch.deadline).between(date_start, date_end), db.Calltouch.status == 'Not called',
                    db.Calltouch.department == dept_name).group_by(db.Calltouch.telephone).count()

        return query

    @staticmethod
    def late_called(date_start, date_end, session):
        """
        Return calls with late callback
        """

        terms = [db.Calltouch.status == 'Late call', db.Calltouch.status == 'Short and Late call']

        query = session.query(db.Calltouch.datetime, db.Telephony.datetime, db.Calltouch.department,
                              db.Calltouch.telephone, db.Calltouch.fio, db.Calltouch.deadline) \
            .join(db.Telephony, db.Telephony.telephone_to == db.Calltouch.telephone) \
            .filter(func.DATE(db.Calltouch.deadline).between(date_start, date_end), or_(*terms)) \
            .group_by(db.Calltouch.telephone).order_by(func.min(db.Telephony.datetime))

        return [(str(i[0]).split('.')[0], i[3], i[4], str(i[1] - i[5]).split('.')[0], i[2]) for i in query.all()]

    @staticmethod
    def lead_log(date_report, session):
        """
        Create a file with all leads to control
        """

        query = session.query(db.Calltouch.datetime, db.Calltouch.department, db.Calltouch.telephone, db.Calltouch.fio,
                              db.Calltouch.deadline, db.Calltouch.status) \
            .filter(func.DATE(db.Calltouch.deadline) == date_report)
        c = 1
        for i in query.all():
            with open('leads_log.txt', 'a') as file:
                datetime, dept, telephone, fio, deadline, status = i
                file.write('Lead #{} {} {} {} {} {} {}\n'.format(c, str(datetime), dept, telephone, fio, deadline, status))

                query_new = session.query(db.Telephony.datetime, db.Telephony.call_type,
                                          db.Telephony.telephone_from, db.Telephony.telephone_to, db.Telephony.duration) \
                    .filter(func.DATE(db.Telephony.datetime) == date_report, db.Telephony.telephone_to == telephone)
                for j in query_new.all():
                    datetime_new, call_type, telephone_from, telephone_to, duration = j

                    file.write('{} {} {} {} {}\n'.format(str(datetime_new), call_type, telephone_from,
                                                                telephone_to, duration))
                file.write('\n ------------------------- \n')
                c += 1


class CallBacks(cs.Sector):
    """
    Class responsible for callbacks of the leads.
    """

    def __init__(self):
        super().__init__()

    def get_data(self, date):
        with db.session_scope() as session:
            CheckCallBacks.check_status(date, session)

            # TODO удалить это
            CheckCallBacks.lead_log(date, session)

    def report_data(self, date_start, date_end):
        cb = CheckCallBacks()
        with db.session_scope() as session:
            not_called_count_list = [cb.not_called_count(date_start, date_end, dept_num, session) for dept_num in
                                     range(len(config.DEPARTMENTS))]
            not_called_list = cb.not_called(date_start, date_end, session)
            late_called_list = cb.late_called(date_start, date_end, session)
            return {'num_leads': not_called_count_list, 'lost_leads': not_called_list, 'late_leads': late_called_list}

    def check_data(self):
        pass  # TODO make a check func

    def plot_data(self):
        pass
