# coding: utf-8

import index
import html
import plot
import send_email
import files
import logging
import direct

if __name__ == '__main__':

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s %(filename)s:%(lineno)d',
                        level=logging.DEBUG,
                        filename=u'log.log')
    logging.info('SCRIPT STARTS')

    files.copyfile(files.server_dir + files.file_name + '.csv', files.work_file)

    index.counter_days(files.directory)

    index.check_phone(files.work_file, index.int_serv_nums, index.depts[0], files.week, 25)
    index.check_phone(files.work_file, index.int_sales_nums, index.depts[1], files.week, 60)
    index.check_phone(files.work_file, index.int_tradein_nums, index.depts[2], files.week, 45)
    index.check_phone(files.work_file, index.int_nfz_nums, index.depts[3], files.week, 45)
    index.check_phone(files.work_file, index.int_dop_nums, index.depts[4], files.week, 45)
    index.check_phone(files.work_file, index.int_zch_nums, index.depts[5], files.week, 45)
    index.check_phone(files.work_file, index.int_ins_nums, index.depts[6], files.week, 45)

    direct.check_direct(direct.service, files.date_day_before, compaign_type='search')
    direct.check_direct(direct.sales, files.date_day_before, compaign_type='search')
    direct.check_direct(direct.tradein, files.date_day_before, compaign_type='search')
    direct.check_direct(direct.nfz, files.date_day_before, compaign_type='search')
    direct.check_direct(direct.insurance, files.date_day_before, compaign_type='search')
    direct.check_direct(direct.service, files.date_day_before, compaign_type='rsya')
    direct.check_direct(direct.sales, files.date_day_before, compaign_type='rsya')
    direct.check_direct(direct.tradein, files.date_day_before, compaign_type='rsya')
    direct.check_direct(direct.nfz, files.date_day_before, compaign_type='rsya')
    direct.check_direct(direct.insurance, files.date_day_before, compaign_type='rsya')

    html.make_html('template', plot.plot_url, html.callsbyday(files.date_day_before, index.depts[0]),
                   html.callsbyday(files.date_day_before, index.depts[1]),
                   html.callsbyday(files.date_day_before, index.depts[2]),
                   html.callsbyday(files.date_day_before, index.depts[3]),
                   html.callsbyday(files.date_day_before, index.depts[4]),
                   html.callsbyday(files.date_day_before, index.depts[5]),
                   html.callsbyday(files.date_day_before, index.depts[6]))

    send_email.send_mail(html.html_text, files.day_before, files.week, 'template')
    logging.info('DAILY SCRIPT ENDS')

    if files.weekday == 0:

        logging.info('report from {} -- {}'.format(files.weeks_start[0], files.weeks_start[-1]))
        plot.read_base50(plot.servdict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.salesdict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.tradeindict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.nfzdict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.dopdict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.zchdict, files.weeks_start, files.weeks_end)
        plot.read_base50(plot.insdict, files.weeks_start, files.weeks_end)

        plot.make_trace(plot.servdict)
        plot.make_trace(plot.salesdict)
        plot.make_trace(plot.tradeindict)
        plot.make_trace(plot.nfzdict)
        plot.make_trace(plot.dopdict)
        plot.make_trace(plot.zchdict)
        plot.make_trace(plot.insdict)

        plot.send_data_plot()
        plot.create_dashboard(plot.plot_url)

        html.make_html('template7', plot.plot_url, html.callsbyweek(index.depts[0], files.year_now, files.week),
                       html.callsbyweek(index.depts[1], files.year_now, files.week),
                       html.callsbyweek(index.depts[2], files.year_now, files.week),
                       html.callsbyweek(index.depts[3], files.year_now, files.week),
                       html.callsbyweek(index.depts[4], files.year_now, files.week),
                       html.callsbyweek(index.depts[5], files.year_now, files.week),
                       html.callsbyweek(index.depts[6], files.year_now, files.week))

        send_email.send_mail(html.html_text, files.day_before, files.week, 'template7')
        logging.info('WEEKLY SCRIPT ENDS')
