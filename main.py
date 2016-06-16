# coding: utf-8

import index
import html
import plot
import send_email
import files
import logging
import direct
import calltouch
import leads_callback

# TODO Сделать debug_mode

if __name__ == '__main__':
    date_report = files.day_before

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s %(filename)s:%(lineno)d',
                        level=logging.DEBUG, filename=u'log.log')
    logging.info('SCRIPT STARTS')

    files.copyfile(files.server_dir + files.file_name + '.csv', files.work_file)

    index.base_days_lost(table='calls')
    index.base_days_lost(table='calltouch')
    index.base_days_lost(table='direct')
    index.check_phone(files.work_file, index.int_serv_nums, index.depts[0], files.week, 25)
    index.check_phone(files.work_file, index.int_sales_nums, index.depts[1], files.week, 60)
    index.check_phone(files.work_file, index.int_tradein_nums, index.depts[2], files.week, 45)
    index.check_phone(files.work_file, index.int_nfz_nums, index.depts[3], files.week, 45)
    index.check_phone(files.work_file, index.int_dop_nums, index.depts[4], files.week, 45)
    index.check_phone(files.work_file, index.int_zch_nums, index.depts[5], files.week, 45)
    index.check_phone(files.work_file, index.int_ins_nums, index.depts[6], files.week, 45)

    calltouch.calltouch_leads_request(date_report)
    calltouch.calltouch_calls_request(date_report)

    direct.check_direct(direct.service, date_report, compaign_type='search')
    direct.check_direct(direct.sales, date_report, compaign_type='search')
    direct.check_direct(direct.tradein, date_report, compaign_type='search')
    direct.check_direct(direct.nfz, date_report, compaign_type='search')
    direct.check_direct(direct.insurance, date_report, compaign_type='search')
    direct.check_direct(direct.service, date_report, compaign_type='rsya')
    direct.check_direct(direct.sales, date_report, compaign_type='rsya')
    direct.check_direct(direct.tradein, date_report, compaign_type='rsya')
    direct.check_direct(direct.nfz, date_report, compaign_type='rsya')
    direct.check_direct(direct.insurance, date_report, compaign_type='rsya')

    html.make_html(

        template='template',
        link=plot.plot_url,
        serv_calls_all=html.callsbyday(date_report, index.depts[0]),
        serv_leads=html.calltouch_by_day(date_report, index.depts[0], type='lead'),
        serv_calls=html.calltouch_by_day(date_report, index.depts[0], type='call'),
        sales_calls_all=html.callsbyday(date_report, index.depts[1]),
        sales_leads=html.calltouch_by_day(date_report, index.depts[1], type='lead'),
        sales_calls=html.calltouch_by_day(date_report, index.depts[1], type='call'),
        tradein_calls_all=html.callsbyday(date_report, index.depts[2]),
        tradein_leads=html.calltouch_by_day(date_report, index.depts[2], type='lead'),
        tradein_calls=html.calltouch_by_day(date_report, index.depts[2], type='call'),
        nfz_calls_all=html.callsbyday(date_report, index.depts[3]),
        nfz_leads=html.calltouch_by_day(date_report, index.depts[3], type='lead'),
        nfz_calls=html.calltouch_by_day(date_report, index.depts[3], type='call'),
        dop_calls_all=html.callsbyday(date_report, index.depts[4]),
        dop_leads=html.calltouch_by_day(date_report, index.depts[4], type='lead'),
        dop_calls=html.calltouch_by_day(date_report, index.depts[4], type='call'),
        zch_calls_all=html.callsbyday(date_report, index.depts[5]),
        zch_leads=html.calltouch_by_day(date_report, index.depts[5], type='lead'),
        zch_calls=html.calltouch_by_day(date_report, index.depts[5], type='call'),
        insurance_calls_all=html.callsbyday(date_report, index.depts[6]),
        insurance_leads=html.calltouch_by_day(date_report, index.depts[6], type='lead'),
        insurance_calls=html.calltouch_by_day(date_report, index.depts[6], type='call'),)

    send_email.send_mail(html.html_text, files.day_before, files.week, 'template')
    leads_callback.leads_callback(date_report)
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

        html.make_html(

            template='template7',
            link=plot.plot_url,
            serv_calls_all=html.callsbyweek(index.depts[0], files.year_now, files.week),
            serv_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[0], type='lead'),
            serv_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[0], type='call'),
            sales_calls_all=html.callsbyweek(index.depts[1], files.year_now, files.week),
            sales_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[1], type='lead'),
            sales_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[1], type='call'),
            tradein_calls_all=html.callsbyweek(index.depts[2], files.year_now, files.week),
            tradein_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[2], type='lead'),
            tradein_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[2], type='call'),
            nfz_calls_all=html.callsbyweek(index.depts[3], files.year_now, files.week),
            nfz_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[3], type='lead'),
            nfz_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[3], type='call'),
            dop_calls_all=html.callsbyweek(index.depts[4], files.year_now, files.week),
            dop_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[4], type='lead'),
            dop_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[4], type='call'),
            zch_calls_all=html.callsbyweek(index.depts[5], files.year_now, files.week),
            zch_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[5], type='lead'),
            zch_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[5], type='call'),
            insurance_calls_all=html.callsbyweek(index.depts[6], files.year_now, files.week),
            insurance_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[6], type='lead'),
            insurance_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[6], type='call'), )

        send_email.send_mail(html.html_text, files.day_before, files.week, 'template7')
        logging.info('WEEKLY SCRIPT ENDS')
