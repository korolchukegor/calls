# coding: utf-8

import csv


def read_func(file):

    serv = 0
    sales = 0
    tradein = 0
    nfz = 0
    dop = 0
    zch = 0
    ins = 0

    unic_serv_nums = set()
    unic_sales_nums = set()
    unic_tradein_nums = set()
    unic_nfz_nums = set()
    unic_dop_nums = set()
    unic_zch_nums = set()
    unic_ins_nums = set()

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
    int_tradein_nums = 513
    int_nfz_nums = 514
    int_dop_nums = 545
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

    with open('{}'.format(file), newline='') as csvfile:
        callsreader = csv.reader(csvfile, delimiter=';', quotechar='|')

        for i in callsreader:

            if i[1] == 'RX' and int(i[3]) in int_serv_nums and int(i[4]) >= 25:
                serv += 1
                unic_serv_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) in int_sales_nums and int(i[4]) >= 45:
                sales += 1
                unic_sales_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) == int_tradein_nums and int(i[4]) >= 45:
                tradein += 1
                unic_tradein_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) == int_nfz_nums and int(i[4]) >= 45:
                nfz += 1
                unic_nfz_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) == int_dop_nums and int(i[4]) >= 45:
                dop += 1
                unic_dop_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) in int_zch_nums and int(i[4]) >= 45:
                zch += 1
                unic_zch_nums.add(i[2])

            elif i[1] == 'RX' and int(i[3]) in int_ins_nums and int(i[4]) >= 45:
                ins += 1
                unic_ins_nums.add(i[2])

    global html_text

    html_text = u"""<span>Общее количество звонков <b>по сервису</b>  - {0}<br>
              Уникальное количество звонков - {1}</span>
        <br><hr>
        <span>Общее количество звонков <b>по продажам</b>  - {2}<br>
              Уникальное количество звонков - {3}</span>
        <br><hr>
        <span>Общее количество звонков <b>по NFZ</b>  - {4}<br>
              Уникальное количество звонков - {5}</span>
        <br><hr>
        <span>Общее количество звонков <b>по Trade-in</b>  - {6}<br>
              Уникальное количество звонков - {7}</span>
        <br><hr>
        <span>Общее количество звонков <b>по доп.оборудованию</b>  - {8}<br>
              Уникальное количество звонков - {9}</span>
        <br><hr>
        <span>Общее количество звонков <b>по запчастям</b>  - {10}<br>
              Уникальное количество звонков - {11}</span>
        <br><hr>
        <span>Общее количество звонков <b>по страхованию</b>  - {12}<br>
              Уникальное количество звонков - {13}</span>""".format(serv, len(unic_serv_nums),
                                                                    sales, len(unic_sales_nums),
                                                                    nfz, len(unic_nfz_nums),
                                                                    tradein, len(unic_tradein_nums),
                                                                    dop, len(unic_dop_nums),
                                                                    zch, len(unic_zch_nums),
                                                                    ins, len(unic_ins_nums))
