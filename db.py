# coding: utf-8

import sqlite3
import logging


# TODO делать шифрование SQLCipher

class Database_manager:
    """ Класс для управления добавлением и чтением записей в базе """

    def __init__(self):

        self.dbpath = 'dbtel.db'
        self.getconnection(self.dbpath)

    def getconnection(self, dbpath):

        try:
            self.conn = sqlite3.connect(dbpath)
            self.c = self.conn.cursor()
            logging.info('Connection to DB OK')

        except sqlite3.Error as e:
            logging.warning('DB problem {}'.format(e.args[0]))

    def query(self, sql_text):
        self.c.execute(sql_text)

    def result(self):
        return self.c.fetchone()

    def result_all(self):
        result_all = [i[0] for i in self.c.fetchall()]
        return result_all

    def __del__(self):
        self.conn.commit()
        self.conn.close()


