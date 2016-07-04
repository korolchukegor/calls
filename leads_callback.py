# coding: utf-8

import sqlite3
import files
import datetime
import logging


def leads_callback(date_report):
    """ Проверка обзвонов по заявкам """

    counter = 0
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    fileheader = 'Проверка {}\n'.format(date_report)
    date_calls = files.DateFormat.calls_date(date_report)
    status = 'Not called'
    dt_lead_txt = None
    deadline_txt = None
    status_txt = None

    with open('callback_report/callback - {}.txt'.format(date_calls), 'a') as txtfile:
        txtfile.write(fileheader + '\n')
    c.execute(
        "SELECT id, date, time, dept, telephone, fio, deadline FROM calltouch WHERE status = ? AND "
        "type = 'lead' AND deadline LIKE '{}%'".format(date_calls), (status,))

    for j in c.fetchall():
        counter += 1
        id, date, time, dept, telephone, fio, deadline = j
        dl_time = deadline.split(' ')[1]
        dl_date = deadline.split(' ')[0]
        deadline = datetime.datetime(year=int(dl_date.split('-')[0]), month=int(dl_date.split('-')[1]),
                                     day=int(dl_date.split('-')[2]), hour=int(dl_time.split(':')[0]),
                                     minute=int(dl_time.split(':')[1]), second=int(dl_time.split(':')[2]))
        dt_lead = datetime.datetime(year=int(date.split('-')[0]), month=int(date.split('-')[1]),
                                    day=int(date.split('-')[2]), hour=int(time.split(':')[0]),
                                    minute=int(time.split(':')[1]), second=int(time.split(':')[2]))
        leadheader = 'Заявка №{} - {} - {}'.format(counter, telephone, dept)
        if len(str(telephone)) == 11:

            dt_lead_txt = 'Заявка поступила - {}'.format(dt_lead)
            deadline_txt = 'Deadline - {}'.format(deadline)
            telephone = '8' + str(telephone)[1:]

            c.execute("SELECT num, duration, date, time FROM calls_out WHERE num == (?) AND date == (?)",
                      (telephone, date_calls))
            calls_list = [i for i in c.fetchall()]
            if calls_list:
                datetime_call = datetime.datetime(year=int(calls_list[0][2].split('-')[0]),
                                                  month=int(calls_list[0][2].split('-')[1]),
                                                  day=int(calls_list[0][2].split('-')[2]),
                                                  hour=int(calls_list[0][3].split(':')[0]),
                                                  minute=int(calls_list[0][3].split(':')[1]),
                                                  second=int(calls_list[0][3].split(':')[2]))

                if calls_list[-1][1] <= 40 and datetime_call <= deadline:
                    status = 'Short call'
                    status_txt = 'Звонок - {}\nКороткий звонок - {} с.\n'.format(datetime_call, calls_list[-1][1])

                elif calls_list[-1][1] > 40 and datetime_call > deadline:
                    status = 'Late call'
                    status_txt = 'Звонок - {}\nЗвонок с опозданием, задержка - {}\n'.format(datetime_call,
                                                                                            datetime_call - deadline)
                elif calls_list[-1][1] <= 40 and datetime_call > deadline:
                    status = 'Short and Late call'
                    status_txt = 'Звонок - {}\nКороткий звонок - {} с. Звонок с опозданием, задержка - {}\n'.format(
                        datetime_call, calls_list[-1][1], datetime_call - deadline)

                elif calls_list[-1][1] >= 40 and datetime_call <= deadline:
                    status = 'Good call'
                    status_txt = 'Успешный звонок\n'

            else:
                status_txt = 'Заявка без обзвона!!!\n'

        else:
            status = 'Bad phone'
            status_txt = 'Некорректный номер телефона\n'
        try:
            c.execute("UPDATE calltouch SET status = (?) WHERE id = (?)", (status, id))
            conn.commit()
        except Exception as e:
            logging.warning(e.args[0])

        with open('callback_report/callback - {}.txt'.format(date_calls), 'a') as txtfile:
            txtfile.write('{}\n{}\n{}\n{}\n'.format(leadheader, dt_lead_txt, deadline_txt, status_txt))

    conn.close()
