# Import smtplib for the actual sending function
import smtplib
import requests
from django.conf import settings

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# RestFramework
from rest_framework.response import Response
from rest_framework import status

# Mock test for mailotp
def mailotp(otp):

# Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Our family reunion'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = me
    msg['To'] = ', '.join(family)
    msg.preamble = f'your login code is:{otp.password}'

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, family, msg.as_string())
    s.quit()


def send_otp(otp):
    url = settings.SMSSERVER
    data = {'recipient':otp.receiver, 'otp':otp.password }
    # requests.post(url, data=data)
    print("otp password")   
    print(otp.password)
    print(otp.receiver)
    return Response(data, status=status.HTTP_200_OK)
    
def send_password(data):
    message = f'کاربر گرامی پروفایل شما در سامانه پترونپ با موفقیت ذخیره شد. رمز عبور شما:{data["password"]}'


    url = settings.PASSWORD_SMSSERVER
    data = {'recipient':data['recipient'], 'message':message}
    print(data)
    # requests.post(url, data=data)
    return Response(data, status=status.HTTP_200_OK)
    

