# coding: utf-8

import calltouch
import config
import email_report
import telephony
import ads
import traffic
import plot_ly
import callbacks

import datetime
import time
import logging
import progressbar


class Main:
    """
    Main class of the program
    """

    def __init__(self, date_report):
        super().__init__()
        self.bar = progressbar.ProgressBar()
        self.date_report = date_report
        self.tp = telephony.Telephony()
        self.ct = calltouch.Calltouch()
        self.ads = ads.Ads()
        self.tr = traffic.Traffic()
        self.er = email_report.EmailReport()
        self.pl = plot_ly.Plotly()
        self.cb = callbacks.CallBacks()

        self.bar.update(5)

    def everyday(self):
        """
        Method creates everyday report
        """

        # Telephony data
        self.tp.get_data(self.date_report)
        tp_data = self.tp.report_data(self.date_report, self.date_report)

        self.bar.update(15)

        # Calltouch data
        self.ct.get_data(self.date_report)
        ct_report = self.ct.report_data(self.date_report, self.date_report)
        ct_calls = ct_report.get('calls')
        ct_leads = ct_report.get('leads')

        self.bar.update(25)

        # Ads data
        self.ads.get_data(self.date_report)

        # Traffic data
        self.tr.get_data(self.date_report)

        self.bar.update(35)

        # Callbacks
        self.cb.get_data(self.date_report)
        callbacks = self.cb.report_data(self.date_report, self.date_report)
        num_lost_leads = callbacks.get('num_leads')
        lost_leads = callbacks.get('lost_leads')
        late_leads = callbacks.get('late_leads')

        self.bar.update(55)

        # Creating HTML data for email report
        html_data = self.er.html(tp_data, ct_calls, ct_leads, num_lost_leads, lost_leads, late_leads, link=None)
        subject = "Отчет за {}".format(self.date_report)

        self.bar.update(75)

        # Creating and sending email
        msg = self.er.create_mail(config.FROM_ADDR, config.TO_ADDR_DEBUG2, subject, html_data)
        self.er.send_email(config.FROM_ADDR, config.TO_ADDR_DEBUG2, msg)

        self.bar.update(100)

    def everyweek(self):
        """
        Method creates week report with plots
        """

        self.ads.check_data()
        self.tr.check_data()

        # Telephony data
        self.tp.check_data()
        tp_data = self.tp.report_data(config.WEEK_REPORT_DATE, self.date_report)

        self.bar.update(120)

        # Calltouch data
        self.ct.check_data()
        ct_report = self.ct.report_data(config.WEEK_REPORT_DATE, self.date_report)
        ct_calls = ct_report.get('calls')
        ct_leads = ct_report.get('leads')

        self.bar.update(140)

        # Callbacks
        self.cb.get_data(self.date_report)
        callbacks = self.cb.report_data(config.WEEK_REPORT_DATE, self.date_report)
        num_lost_leads = callbacks.get('num_leads')
        lost_leads = callbacks.get('lost_leads')
        late_leads = callbacks.get('late_leads')

        self.bar.update(160)

        # Creating plots
        tp_plot = self.tp.plot_data()
        ct_plots = self.ct.plot_data()
        calls_plot = ct_plots.get('calls')
        leads_plot = ct_plots.get('leads')
        # ads_plots = self.ads.plot_data()
        # ctr_plot = ads_plots.get('ctr')
        # cpc_plot = ads_plots.get('cpc')

        self.bar.update(180)

        # Creating dashboard
        link = self.pl.create_dashboard(tp_plot, calls_plot, leads_plot) #, ctr_plot, cpc_plot)

        self.bar.update(190)

        # Creating HTML data for email report
        html_data = self.er.html(tp_data, ct_calls, ct_leads, num_lost_leads, lost_leads, late_leads, link)
        subject = "Отчет за период {} - {}".format(config.WEEK_REPORT_DATE, self.date_report)

        self.bar.update(195)

        # Creating and sending email
        msg = self.er.create_mail(config.FROM_ADDR, config.TO_ADDR_DEBUG2, subject, html_data)
        self.er.send_email(config.FROM_ADDR, config.TO_ADDR_DEBUG2, msg)

        self.bar.finish()

class Profiler:
    """ Check the speed of the script """

    _startTime = None

    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        logging.warning("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))

if __name__ == '__main__':

    main = Main(config.DATE_REPORT)
    with Profiler() as p:
        main.everyday()
        if datetime.date.today().weekday() == 0:  # If today is a monday
            main.everyweek()
