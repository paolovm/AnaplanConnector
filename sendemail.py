import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def sendEmail(subject="Anaplan Status Non Defined",status="Unspecified Error"):
    receivers="paolovm@gmail.com,marcia_borges@fornodeminas.com.br"

    sender = 'fdmplanning@gmail.com'
    password = 'Fdmpla2021'

    port=1025
    port = 465
    context = ssl.create_default_context()

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    msg.attach(MIMEText(status))

#    with smtplib.SMTP('localhost', port) as server:
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        pass
        #server.login("paolovm@gmail.com", password)
        #server.sendmail(sender, receivers, msg.as_string())

    print(status)
    print("Successfully sent email")

if __name__ == '__main__':
    sendEmail()

