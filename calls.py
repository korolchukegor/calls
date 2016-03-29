# coding: utf-8

import csv


def read_func(file):

    serv = []
    sales = []
    tradein = []
    nfz = []
    dop = []
    zch = []
    ins = []
    int_serv_nums = []
    int_sales_nums = []
    int_tradein_nums = []
    int_nfz_nums = []
    int_dop_nums = []
    int_zch_nums = []
    int_ins_nums = []

    def read_config(int_dept_nums, colnum):
        with open('config.csv', newline='') as csvfile:
            cells = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(cells)

            for cell in cells:
                if cell[colnum] != '':
                    int_dept_nums.append(int(cell[colnum]))

    read_config(int_serv_nums, 0)
    read_config(int_sales_nums, 1)
    read_config(int_tradein_nums, 2)
    read_config(int_nfz_nums, 3)
    read_config(int_dop_nums, 4)
    read_config(int_zch_nums, 5)
    read_config(int_ins_nums, 6)

    def check_phone(int_dept_nums, dept, time):

        if i[1] == 'RX' and int(i[3]) in int_dept_nums and int(i[4]) >= time:
            dept.append(i[2])

    with open('{}'.format(file), newline='') as csvfile:
        callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for i in callsreader:
            check_phone(int_serv_nums, serv, 25)
            check_phone(int_sales_nums, sales, 45)
            check_phone(int_nfz_nums, nfz, 45)
            check_phone(int_tradein_nums, tradein, 45)
            check_phone(int_dop_nums, dop, 45)
            check_phone(int_zch_nums, zch, 45)
            check_phone(int_ins_nums, ins, 45)

    global html_text
    with open('template_1.html', 'r', encoding='utf-8') as h:
        html_text = h.read().format(len(serv), len(set(serv)),
                                    len(sales), len(set(sales)),
                                    len(nfz), len(set(nfz)),
                                    len(tradein), len(set(tradein)),
                                    len(dop), len(set(dop)),
                                    len(zch), len(set(zch)),
                                    len(ins), len(set(ins)))
