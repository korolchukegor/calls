# coding: utf-8

import datetime




today = datetime.datetime.today()           # определяем дату сегодня
day = today                                 # присваиваем значение по умолчанию
weekday = datetime.datetime.today().weekday()
days_of_last_week = []                      # тут будут дни прошлой недели
day_before = today - datetime.timedelta(days=1)
seven_days_before = today - datetime.timedelta(days=7)
file_name = '{:%y_%m_%d}'.format(day_before)

directory = r'C:\Users\Egor\PycharmProjects\calls\tarif'

file = open(directory + '\{}.txt'.format(file_name), 'r')
# тут будет вызов программы обработки файла
print('Звонков вчера -', file.read())
# -------------------------------------------


# Нужно запускать, только если понедельник
# if weekday = 0:
while day != seven_days_before:             # заполняем список днями прошлой недели
    day = day - datetime.timedelta(days=1)
    days_of_last_week.append('{:%y_%m_%d}'.format(day))

for day in days_of_last_week:
    week = open(directory + '\{}.txt'.format(day), 'r')
    print(week.read())
print('Всего звонков за неделю -', 28)

# try:

# except:


# Программа запускается ежедневно
# Проверяет дату и открывает вчерашний файл
# Выполняется и отправляет отчет на почту
# Если день = 0 (Понедельник), то отправляет отчет за всю прошлую неделю (открывает последние 7 файлов и сводит в один)
