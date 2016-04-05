# coding: utf-8

import unittest
from calls_files import file_name, directory, csv_work_file
from assembling import *


class TestCalls_Files(unittest.TestCase):
    """ Тестирование модуля Calls_Files """

    def test_filename(self):
        """ Проверка правильности формирования имени файла """

        self.assertEqual(file_name, '16_04_04')

    def test_directory(self):
        """ Проверка правильности директории """

        self.assertEqual(directory, r'C:\Users\korolchuk\Documents\python\service_calls\tarif')

    def test_csv_work_file(self):
        """ Проверка правильности названия и полного пути csv-файла """

        self.assertEqual(csv_work_file, r'C:\Users\korolchuk\Documents\python\service_calls\tarif\16_04_04.csv')


class TestAssembling(unittest.TestCase):
    """ Тестирование модуля Assembling """

    def test_read_config(self):
        """ Проверка правильности чтения config """

        read_config(int_serv_nums, 0)
        read_config(int_sales_nums, 1)
        read_config(int_tradein_nums, 2)
        read_config(int_nfz_nums, 3)
        read_config(int_dop_nums, 4)
        read_config(int_zch_nums, 5)
        read_config(int_ins_nums, 6)

        self.assertEqual(int_serv_nums, [519, 530, 534, 535, 536, 538, 2447778])
        self.assertEqual(int_sales_nums, [520, 521, 522, 523, 525, 526])
        self.assertEqual(int_tradein_nums, [513])
        self.assertEqual(int_nfz_nums, [514])
        self.assertEqual(int_dop_nums, [545])
        self.assertEqual(int_zch_nums, [551, 553, 554, 555])
        self.assertEqual(int_ins_nums, [562, 563, 564, 567, 568])


if __name__ == '__main__':
    unittest.main()
