import smtplib
from email.mime.text import MIMEText

def sendEmail(subject="Anaplan Status Non Defined",status="Unspecified Error"):
    sender = 'admin@example.com'
    receivers = ['info@example.com']
    port = 1025
    msg = MIMEText(status)
    msg['Subject'] = subject
    msg['From'] = 'admin@example.com'
    msg['To'] = 'info@example.com'
    with smtplib.SMTP('localhost', port) as server:
        # server.login('username', 'password')
        server.sendmail(sender, receivers, msg.as_string())
 #       print("Successfully sent email")