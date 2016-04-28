# coding: utf-8

import index
import html
import graph
import send_email
import files
import logging

if __name__ == '__main__':
    logging.info('SCRIPT STARTS')
    index.read_config(index.int_serv_nums, 0)
    index.read_config(index.int_sales_nums, 1)
    index.read_config(index.int_tradein_nums, 2)
    index.read_config(index.int_nfz_nums, 3)
    index.read_config(index.int_dop_nums, 4)
    index.read_config(index.int_zch_nums, 5)
    index.read_config(index.int_ins_nums, 6)

    index.counter_days(files.directory)

    files.copyfile(files.server_dir + files.file_name + '.csv', files.work_file)

    index.check_phone(files.work_file, index.int_serv_nums, index.depts[0], files.week, 25)
    index.check_phone(files.work_file, index.int_sales_nums, index.depts[1], files.week, 60)
    index.check_phone(files.work_file, index.int_tradein_nums, index.depts[2], files.week, 45)
    index.check_phone(files.work_file, index.int_nfz_nums, index.depts[3], files.week, 45)
    index.check_phone(files.work_file, index.int_dop_nums, index.depts[4], files.week, 45)
    index.check_phone(files.work_file, index.int_zch_nums, index.depts[5], files.week, 45)
    index.check_phone(files.work_file, index.int_ins_nums, index.depts[6], files.week, 45)

    html.make_html('template', html.callsbyday(files.date_day_before, index.depts[0]),
                   html.callsbyday(files.date_day_before, index.depts[1]),
                   html.callsbyday(files.date_day_before, index.depts[2]),
                   html.callsbyday(files.date_day_before, index.depts[3]),
                   html.callsbyday(files.date_day_before, index.depts[4]),
                   html.callsbyday(files.date_day_before, index.depts[5]),
                   html.callsbyday(files.date_day_before, index.depts[6]))

    send_email.send_mail(html.html_text, files.day_before, files.week, 'template')
    logging.info('DAILY SCRIPT ENDS')
    # index.read_base() # Для отладки

    if files.weekday == 0:

        html.make_html('template7', html.callsbyweek(index.depts[0], files.year_now, files.week),
                       html.callsbyweek(index.depts[1], files.year_now, files.week),
                       html.callsbyweek(index.depts[2], files.year_now, files.week),
                       html.callsbyweek(index.depts[3], files.year_now, files.week),
                       html.callsbyweek(index.depts[4], files.year_now, files.week),
                       html.callsbyweek(index.depts[5], files.year_now, files.week),
                       html.callsbyweek(index.depts[6], files.year_now, files.week))
        logging.info('report from {} -- {}'.format(files.weeks_start[0], files.weeks_start[-1]))
        graph.read_base50(graph.servdict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.salesdict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.tradeindict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.nfzdict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.dopdict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.zchdict, files.weeks_start, files.weeks_end)
        graph.read_base50(graph.insdict, files.weeks_start, files.weeks_end)

        graph.graphics()

        send_email.send_mail(html.html_text, files.day_before, files.week, 'template7')
        logging.info('WEEKLY SCRIPT ENDS')