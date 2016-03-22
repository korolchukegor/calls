# coding: utf-8

import main



def lounch(a):

    if a == 1:
        main.mod_tel()
    elif a == 2:
        main.writefile()
    print('Вы выбрали', a)


a = int(input('Введите номер действия:\n 1 - обрезать номера\n 2 - сравнить с файлом звонков\n'))

lounch(a)