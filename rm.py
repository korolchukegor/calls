# coding: utf-8
import html
import index
import send_email
import os
import csv
import files

directory = r'{}\tarif'.format(os.getcwd())
days_of_week = ['16_01_18', '16_01_19', '16_01_20', '16_01_21', '16_01_22', '16_01_23', '16_01_24']
for day in days_of_week:
    day_of_week = open(directory + '\{}.csv'.format(day), 'r', newline='')
    callsreader = csv.reader(day_of_week, delimiter=';', quotechar='|')
    with open(directory + '\{}-{}.csv'.format(days_of_week[0],
                                              days_of_week[6]), 'a', newline='') as week_calls:
        callswriter = csv.writer(week_calls, delimiter=';', quotechar='|')
        for i in callsreader:
            callswriter.writerow(i)

html.make_html('template7', html.callsbyweek(index.depts[0], 2016, 3),
               html.callsbyweek(index.depts[1], 2016, 3),
               html.callsbyweek(index.depts[2], 2016, 3),
               html.callsbyweek(index.depts[3], 2016, 3),
               html.callsbyweek(index.depts[4], 2016, 3),
               html.callsbyweek(index.depts[5], 2016, 3),
               html.callsbyweek(index.depts[6], 2016, 3))

send_email.send_mail(html.html_text, files.day_before, 3, 'template7')