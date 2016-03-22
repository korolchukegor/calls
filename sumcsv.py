# coding: utf-8

import csv

file = r'C:\Users\korolchuk\Documents\python\service_calls\tarif\test\16_03_17.csv'
file2 = r'C:\Users\korolchuk\Documents\python\service_calls\tarif\test\16_03_18.csv'

f = open('{}'.format(file), newline=''):
    callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for i in callsreader: