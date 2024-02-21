import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

fromaddr = "testovich.77@list.ru" # от кого
to_address = "gnarus@inbox.ru" # кому
# mypass = 'qwertyu12345!'
mypass = "kCJtpCZwCvtdy5zhXFZM" # пароль для отправки отчета
report_name = "project.log" # имя файла с отчетом

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = to_address
msg['Subject'] = "Привет от питона"

# Формирования отчета-файла
with open(report_name, "rb") as f:
    part = MIMEApplication(f.read(), Name=basename(report_name))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(report_name)
    msg.attach(part)

body = f"Отчет о автотестах"
msg.attach(MIMEText(body, 'plain'))

# Передача отчета-файла (у mail.ru используется SSL шифрование)
server = smtplib.SMTP('smtp.mail.ru', 465)
server.starttls()
server.login(fromaddr, mypass) # передача логина и пароля почты с которой будет отправка происходить
text = msg.as_string()

server.sendmail(fromaddr, to_address, text) # команда отправки отчета
print("send mail")
server.quit()