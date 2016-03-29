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

    int_serv_nums = [int(nums) for nums in [

        519,
        530,
        534,
        535,
        536,
        538,
        2447778
    ]]
    int_sales_nums = [int(nums2) for nums2 in [

        520,
        521,
        522,
        523,
        525,
        526
    ]]
    int_tradein_nums = [int(nums3) for nums3 in [

        513
    ]]
    int_nfz_nums = [int(nums3) for nums3 in [

        514
    ]]
    int_dop_nums = [int(nums3) for nums3 in [

        545
    ]]
    int_zch_nums = [int(nums3) for nums3 in [

        551,
        553,
        554,
        555
    ]]
    int_ins_nums = [int(nums4) for nums4 in [

        562,
        563,
        564,
        567,
        568
    ]]


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
