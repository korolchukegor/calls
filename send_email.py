# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

subject = u'Тестирование оповещений на email'
fromaddr = 'Mr. Robot <korolchukwork@gmail.com>'
toaddr = 'Administrator <egorkorolchuk@gmail.com>'

multipart = MIMEMultipart('alternative')
multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
multipart['To'] = Header(toaddr.encode('utf-8'), 'UTF-8').encode()
multipart['From'] = Header(fromaddr.encode('utf-8'), 'UTF-8').encode()

html = u'<html><body>Привет, {}!</br>Это тестовая рассылка!</body></html>'.format(toaddr)
text = u'Привет!\nЭто тестовая рассылка!'

htmlpart = MIMEText(html.encode('utf-8'), 'html', 'UTF-8')
multipart.attach(htmlpart)
textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
multipart.attach(textpart)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

multipart.attach(part1)
multipart.attach(part2)

username = u'korolchukwork@gmail.com'
password = u'wgBZ1FgI8ykmWNF8vQgP'
#Инициализируем соединение с сервером gmail по протоколу smtp.
serv = u'smtp.gmail.com:587'
server = smtplib.SMTP(serv)
#Выводим на консоль лог работы с сервером (для отладки)
# server.set_debuglevel(1);
#Переводим соединение в защищенный режим (Transport Layer Security)
server.starttls()
#Проводим авторизацию:
server.login(username,password)
#Отправляем письмо:
server.sendmail(fromaddr, toaddr, multipart.as_string())
#Закрываем соединение с сервером
server.quit()

