import smtplib, ssl
from email.mime.text import MIMEText

def sendEmail(subject="Anaplan Status Non Defined",status="Unspecified Error"):
    sender = 'paolovm@gmail.com'
#    receivers = ['jvictor@ctiglobal.com;paolo.malafaia@flexthink.com.au']
    receivers='paolovm@gmail.com'
    port=1025
#    port = 465

    context = ssl.create_default_context()
    password = ''
    msg = MIMEText(status)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
 #   with smtplib.SMTP('localhost', port) as server:
#    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#        server.login("paolovm@gmail.com", password)
  #      server.sendmail(sender, receivers, msg.as_string())
    print(MIMEText(status))
    print("Successfully sent email")

if __name__ == '__main__':
    sendEmail()

