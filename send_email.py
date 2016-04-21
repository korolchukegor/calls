# coding: utf-8

import os
import uuid
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_mail(html_text, day_before, week, template):
    """ Формирование письма для рассылки """

    fromaddr = 'Neva Calls <korolchukwork@gmail.com>'
    toaddr = ['Egor <egor.korolchuk@vwspb.ru>', 'Yana <marketing@vwspb.ru>', 'Oleg <oleg.semenov@vwspb.ru>']

    if template == 'template7':
        img = dict(title=u'Picture report…', path=u'spirit.png', cid=str(uuid.uuid4()))
        subject = u'Отчет по звонкам за {} неделю'.format(week)

    else:
        img = dict(title=u'Picture report…', path='', cid=str(uuid.uuid4()))
        subject = u'Отчет по звонкам за {}'.format('{:%d-%m-%y}'.format(day_before))

    msg = MIMEMultipart('related')
    msg['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    msg['From'] = Header(fromaddr.encode('utf-8'), 'UTF-8').encode()
    for taddr in toaddr:
        msg['To'] = Header(taddr.encode('utf-8'), 'UTF-8').encode()

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    htmlpart = MIMEText(html_text.encode('utf-8'), 'html', 'UTF-8')
    msg_alternative.attach(htmlpart)
    try:
        with open(img['path'], 'rb') as file:
            msg_image = MIMEImage(file.read(), name=os.path.basename(img['path']))
            msg.attach(msg_image)
        msg_image.add_header('Content-ID', '<{}>'.format(img['cid']))
    except FileNotFoundError:
        pass

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
    server.sendmail(fromaddr, toaddr, msg.as_string())
    print('Отчет отправлен')
    # Закрываем соединение с сервером
    server.quit()
