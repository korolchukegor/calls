# coding: utf-8

import sqlite3
import files
import datetime


def leads_callback(date_report):
    """ Проверка обзвонов по заявкам """

    counter = 0
    conn = sqlite3.connect('dbtel.db')
    c = conn.cursor()
    fileheader = 'Проверка {}\n'.format(date_report)
    date_calls = files.DateFormat.calls_date(date_report)
    with open('callback_report/callback - {}.txt'.format(date_calls), 'a') as txtfile:
        txtfile.write(fileheader + '\n')
    type = 'lead'
    c.execute(
        "SELECT date, time, dept, telephone, fio, deadline FROM calltouch WHERE type = '{}' AND deadline LIKE '{}%'".format(
            type, date_calls))

    for j in c.fetchall():
        counter += 1
        date, time, dept, telephone, fio, deadline = j
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
                    status = 'Звонок - {}\nКороткий звонок - {} с.'.format(datetime_call, calls_list[-1][1])

                elif calls_list[-1][1] > 40 and datetime_call > deadline:
                    status = 'Звонок - {}\nЗвонок с опозданием, задержка - {}'.format(datetime_call,
                                                                                         datetime_call - deadline)
                elif calls_list[-1][1] <= 40 and datetime_call > deadline:
                    status = 'Звонок - {}\nКороткий звонок - {} с. Звонок с опозданием, задержка - {}'.format(
                        datetime_call, calls_list[-1][1], datetime_call - deadline)

                elif calls_list[-1][1] >= 40 and datetime_call <= deadline:
                    status = 'Успешный звонок'

            else:
                status = 'Заявка без обзвона!!!'

                # TODO Убрать в класс DateFormat

        else:
            status = 'Некорректный номер телефона'

        status_txt = status + '\n'
        with open('callback_report/callback - {}.txt'.format(date_calls), 'a') as txtfile:
            txtfile.write('{}\n{}\n{}\n{}\n'.format(leadheader, dt_lead_txt, deadline_txt, status_txt))

    conn.close()
