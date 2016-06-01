# coding: utf-8

import sqlite3
import logging

# TODO делать шифрование SQLCipher

class Database_manager:
    """ Класс для управления записями в базу """

    def __init__(self):

        self.dbpath = 'dbtel2.db'
        self.getconnection(self.dbpath)

    def getconnection(self, dbpath):

        try:

            self.conn = sqlite3.connect(dbpath)
            self.c = self.conn.cursor()
            logging.info('Connection to DB OK')

        except sqlite3.Error as e:
            logging.warning('DB problem {}'.format(e.args[0]))

    def addperiod(self, table, datestart, dateend):
        pass

db_manager = Database_manager()


