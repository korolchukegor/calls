# coding: utf-8

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import calls
import calls_files

subject = u'Отчет по звонкам за {}'.format(calls_files.file_name)
fromaddr = 'Mr. Robot <korolchukwork@gmail.com>'
toaddr = ['Administrator <egor.korolchuk@vwspb.ru>', 'Yana <marketing@vwspb.ru>', 'Oleg <oleg.semenov@vwspb.ru>]

multipart = MIMEMultipart('alternative')
multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
for taddr in toaddr:
    multipart['To'] = Header(taddr.encode('utf-8'), 'UTF-8').encode()
multipart['From'] = Header(fromaddr.encode('utf-8'), 'UTF-8').encode()


text = u'Привет!\nЭто тестовая рассылка!'

htmlpart = MIMEText(calls.html_text.encode('utf-8'), 'html', 'UTF-8')
multipart.attach(htmlpart)
textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
multipart.attach(textpart)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(calls.html_text, 'html')

multipart.attach(part1)
multipart.attach(part2)

username = u'korolchukwork@gmail.com'
password = u'wgBZ1FgI8ykmWNF8vQgP'
# Инициализируем соединение с сервером gmail по протоколу smtp.
serv = u'smtp.gmail.com:587'
server = smtplib.SMTP(serv)
# Выводим на консоль лог работы с сервером (для отладки)
# server.set_debuglevel(1);
# Переводим соединение в защищенный режим (Transport Layer Security)
server.starttls()
# Проводим авторизацию:
server.login(username, password)
# Отправляем письмо:
server.sendmail(fromaddr, toaddr, multipart.as_string())
# Закрываем соединение с сервером
server.quit()
