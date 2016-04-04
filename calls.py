# coding: utf-8

import assembling
from assembling import *
import send_email

if __name__ == '__main__':

    read_config(int_serv_nums, 0)
    read_config(int_sales_nums, 1)
    read_config(int_tradein_nums, 2)
    read_config(int_nfz_nums, 3)
    read_config(int_dop_nums, 4)
    read_config(int_zch_nums, 5)
    read_config(int_ins_nums, 6)

    check_phone(int_serv_nums, serv, 25)
    check_phone(int_sales_nums, sales, 45)
    check_phone(int_tradein_nums, tradein, 45)
    check_phone(int_nfz_nums, nfz, 45)
    check_phone(int_dop_nums, dop, 45)
    check_phone(int_zch_nums, zch, 45)
    check_phone(int_ins_nums, ins, 45)

    results(serv)
    results(sales)
    results(nfz)
    results(tradein)
    results(dop)
    results(zch)
    results(ins)

    make_html()

    send_email.send_mail(assembling.html_text)
