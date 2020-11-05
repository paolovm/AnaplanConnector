import smtplib
from email.mime.text import MIMEText

def sendEmail():
    sender = 'admin@example.com'
    receivers = ['info@example.com']
    port = 1025
    msg = MIMEText('This is test mail')
    msg['Subject'] = 'Test mail'
    msg['From'] = 'admin@example.com'
    msg['To'] = 'info@example.com'
    with smtplib.SMTP('localhost', port) as server:
        # server.login('username', 'password')
        server.sendmail(sender, receivers, msg.as_string())
        print("Successfully sent email")