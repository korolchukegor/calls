# coding: utf-8

import assembling
from assembling import *
import send_email
from graph import *
import calls_files

if __name__ == '__main__':

    template = 'template'
    read_config(int_serv_nums, 0)
    read_config(int_sales_nums, 1)
    read_config(int_tradein_nums, 2)
    read_config(int_nfz_nums, 3)
    read_config(int_dop_nums, 4)
    read_config(int_zch_nums, 5)
    read_config(int_ins_nums, 6)

    check_phone(calls_files.csv_work_file, int_serv_nums, serv, 25)
    check_phone(calls_files.csv_work_file, int_sales_nums, sales, 45)
    check_phone(calls_files.csv_work_file, int_tradein_nums, tradein, 45)
    check_phone(calls_files.csv_work_file, int_nfz_nums, nfz, 45)
    check_phone(calls_files.csv_work_file, int_dop_nums, dop, 45)
    check_phone(calls_files.csv_work_file, int_zch_nums, zch, 45)
    check_phone(calls_files.csv_work_file, int_ins_nums, ins, 45)

    results(serv, calls_files.file_name)
    results(sales, calls_files.file_name)
    results(nfz, calls_files.file_name)
    results(tradein, calls_files.file_name)
    results(dop, calls_files.file_name)
    results(zch, calls_files.file_name)
    results(ins, calls_files.file_name)

    make_html(template)

    send_email.send_mail(assembling.html_text,
                         calls_files.day_before,
                         calls_files.seven_days_before,
                         template)

    if calls_files.weekday == 0:

        template = 'template7'
        check_phone(calls_files.csv_work_file2, int_serv_nums, serv, 25)
        check_phone(calls_files.csv_work_file2, int_sales_nums, sales, 45)
        check_phone(calls_files.csv_work_file2, int_tradein_nums, tradein, 45)
        check_phone(calls_files.csv_work_file2, int_nfz_nums, nfz, 45)
        check_phone(calls_files.csv_work_file2, int_dop_nums, dop, 45)
        check_phone(calls_files.csv_work_file2, int_zch_nums, zch, 45)
        check_phone(calls_files.csv_work_file2, int_ins_nums, ins, 45)

        read_base(servdict, calls_files.days_of_last_week)
        read_base(salesdict, calls_files.days_of_last_week)
        read_base(tradeindict, calls_files.days_of_last_week)
        read_base(nfzdict, calls_files.days_of_last_week)
        read_base(dopdict, calls_files.days_of_last_week)
        read_base(zchdict, calls_files.days_of_last_week)
        read_base(insdict, calls_files.days_of_last_week)

        make_html(template)

        graphics()

        send_email.send_mail(assembling.html_text,
                             calls_files.day_before,
                             calls_files.seven_days_before,
                             template)
