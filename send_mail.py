import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yaml

with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)

fromaddr = testdata['mail_user'] # от кого
to_address = testdata['mail_for_report'] # кому
mypass = testdata['mail_pass'] # пароль для отправки отчета
report_name = "project.log" # имя файла с отчетом

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = to_address
msg['Subject'] = "Отчет по автотестам"

# Формирования отчета-файла
with open(report_name, "rb") as f:
    part = MIMEApplication(f.read(), Name=basename(report_name))
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(report_name)
    msg.attach(part)

body = f"Отчет по автотестам"
msg.attach(MIMEText(body, 'plain'))

# Передача отчета-файла (у mail.ru используется SSL шифрование)
server = smtplib.SMTP('smtp.mail.ru', 465)
server.starttls()
server.login(fromaddr, mypass) # передача логина и пароля почты с которой будет отправка происходить
text = msg.as_string()

server.sendmail(fromaddr, to_address, text) # команда отправки отчета
print("send mail")
server.quit()
