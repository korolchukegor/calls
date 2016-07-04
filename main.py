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
import configparser
import analytics

# TODO Сделать debug_mode

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    servdict = {u'service': []}
    salesdict = {u'sales': []}
    tradeindict = {u'tradein': []}
    nfzdict = {u'nfz': []}
    dopdict = {u'dop': []}
    zchdict = {u'zch': []}
    insdict = {u'insurance': []}

    date_report = files.day_before

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s %(filename)s:%(lineno)d',
                        level=logging.DEBUG, filename=u'log.log')
    logging.info('------SCRIPT STARTS------')

    files.copyfile(files.server_dir + files.file_name + '.csv', files.work_file)

    index.check_phone(files.work_file, index.int_serv_nums, index.depts[0], files.week,
                      int(config['seconds']['service']))
    index.check_phone(files.work_file, index.int_sales_nums, index.depts[1], files.week,
                      int(config['seconds']['sales']))
    index.check_phone(files.work_file, index.int_tradein_nums, index.depts[2], files.week,
                      int(config['seconds']['tradein']))
    index.check_phone(files.work_file, index.int_nfz_nums, index.depts[3], files.week, int(config['seconds']['nfz']))
    index.check_phone(files.work_file, index.int_dop_nums, index.depts[4], files.week, int(config['seconds']['dop']))
    index.check_phone(files.work_file, index.int_zch_nums, index.depts[5], files.week, int(config['seconds']['zch']))
    index.check_phone(files.work_file, index.int_ins_nums, index.depts[6], files.week,
                      int(config['seconds']['insurance']))

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

    analytics.analytics_report(date_report)

    index.base_days_lost(table='calls')
    index.base_days_lost(table='calltouch')
    index.base_days_lost(table='direct')
    index.base_days_lost(table='adwords')
    index.base_days_lost(table='traffic')

    html.make_html(

        template='template',
        link=None,
        serv_calls_all=html.callsbyday(date_report, index.depts[0]),
        serv_leads=html.calltouch_by_day(date_report, index.depts[0], type='lead'),
        serv_calls=html.calltouch_by_day(date_report, index.depts[0], type='call'),
        serv_no_callback=None,
        sales_calls_all=html.callsbyday(date_report, index.depts[1]),
        sales_leads=html.calltouch_by_day(date_report, index.depts[1], type='lead'),
        sales_calls=html.calltouch_by_day(date_report, index.depts[1], type='call'),
        sales_no_callback=None,
        tradein_calls_all=html.callsbyday(date_report, index.depts[2]),
        tradein_leads=html.calltouch_by_day(date_report, index.depts[2], type='lead'),
        tradein_calls=html.calltouch_by_day(date_report, index.depts[2], type='call'),
        tradein_no_callback=None,
        nfz_calls_all=html.callsbyday(date_report, index.depts[3]),
        nfz_leads=html.calltouch_by_day(date_report, index.depts[3], type='lead'),
        nfz_calls=html.calltouch_by_day(date_report, index.depts[3], type='call'),
        nfz_no_callback=None,
        dop_calls_all=html.callsbyday(date_report, index.depts[4]),
        dop_leads=html.calltouch_by_day(date_report, index.depts[4], type='lead'),
        dop_calls=html.calltouch_by_day(date_report, index.depts[4], type='call'),
        dop_no_callback=None,
        zch_calls_all=html.callsbyday(date_report, index.depts[5]),
        zch_leads=html.calltouch_by_day(date_report, index.depts[5], type='lead'),
        zch_calls=html.calltouch_by_day(date_report, index.depts[5], type='call'),
        zch_no_callback=None,
        insurance_calls_all=html.callsbyday(date_report, index.depts[6]),
        insurance_leads=html.calltouch_by_day(date_report, index.depts[6], type='lead'),
        insurance_calls=html.calltouch_by_day(date_report, index.depts[6], type='call'),
        insurance_no_callback=None)

    leads_callback.leads_callback(date_report)
    send_email.send_mail(html.html_text, date_report, files.week, 'template')
    logging.info('------DAILY SCRIPT ENDS------')

    if files.weekday == 0:
        weeks_num = int(config['plotly']['weeks_num'])
        logging.info(
            'report from {} -- {}'.format(files.weeks_start_dates(weeks_num)[0], files.weeks_end_dates(weeks_num)[-1]))
        plot.read_base50(plot.servdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.salesdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.tradeindict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.nfzdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.dopdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.zchdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))
        plot.read_base50(plot.insdict, files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num))

        plot_url1 = plot.send_data_plot(filename=u'Звонки')

        plot.clear_lst(plot.servdict, plot.salesdict, plot.tradeindict, plot.nfzdict, plot.dopdict, plot.zchdict,
                       plot.insdict)

        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.servdict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.salesdict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.tradeindict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.nfzdict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.dopdict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.zchdict, type='lead')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.insdict, type='lead')

        plot_url2 = plot.send_data_plot(filename=u'Заявки с сайта')

        plot.clear_lst(plot.servdict, plot.salesdict, plot.tradeindict, plot.nfzdict, plot.dopdict, plot.zchdict,
                       plot.insdict)

        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.servdict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.salesdict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.tradeindict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.nfzdict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.dopdict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.zchdict, type='call')
        plot.read_base_calltouch(files.weeks_start_dates(weeks_num), files.weeks_end_dates(weeks_num), plot.insdict, type='call')

        plot_url3 = plot.send_data_plot(filename=u'Звонки с сайта')

        dashboard = plot.create_dashboard(plot_url1, plot_url2, plot_url3)

        html.make_html(

            template='template7',
            link=dashboard,
            serv_calls_all=html.callsbyweek(index.depts[0], files.year_now, files.week),
            serv_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[0], type='lead'),
            serv_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[0], type='call'),
            serv_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[0]),
            sales_calls_all=html.callsbyweek(index.depts[1], files.year_now, files.week),
            sales_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[1], type='lead'),
            sales_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[1], type='call'),
            sales_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[1]),
            tradein_calls_all=html.callsbyweek(index.depts[2], files.year_now, files.week),
            tradein_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[2], type='lead'),
            tradein_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[2], type='call'),
            tradein_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[2]),
            nfz_calls_all=html.callsbyweek(index.depts[3], files.year_now, files.week),
            nfz_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[3], type='lead'),
            nfz_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[3], type='call'),
            nfz_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[3]),
            dop_calls_all=html.callsbyweek(index.depts[4], files.year_now, files.week),
            dop_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[4], type='lead'),
            dop_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[4], type='call'),
            dop_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[4]),
            zch_calls_all=html.callsbyweek(index.depts[5], files.year_now, files.week),
            zch_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[5], type='lead'),
            zch_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[5], type='call'),
            zch_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[5]),
            insurance_calls_all=html.callsbyweek(index.depts[6], files.year_now, files.week),
            insurance_leads=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[6], type='lead'),
            insurance_calls=html.calltouch_by_week(files.seven_days_before, files.day_before, index.depts[6], type='call'),
            insurance_no_callback=html.check_callbacks(files.seven_days_before, files.day_before, index.depts[6]))
        send_email.send_mail(html.html_text, files.day_before, files.week, 'template7')
        logging.info('------WEEKLY SCRIPT ENDS------')
