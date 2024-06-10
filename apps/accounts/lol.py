import ssl
import smtplib
from email.mime.text import MIMEText

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.example.com', 465, context=context) as server:
    server.login('beksturgunbaevl@gmail.com', '')
    msg = MIMEText('This is the body of the email')
    msg['Subject'] = 'Subject of the email'
    msg['From'] = 'beksturgunbaevl@gmail.com'
    msg['To'] = 'beksturgunbaevl@gmail.com'
    server.sendmail('beksturgunbaevl@gmail.com', 'beksturgunbaevl@gmail.com', msg.as_string())