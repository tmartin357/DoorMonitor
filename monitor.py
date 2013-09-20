#!/usr/bin/env python2

#--------------------------------------------------------------------------
# LICENCE
#--------------------------------------------------------------------------
#This monitor.py is part of SPSUAUVDoorMonitor.
#
#SPSUAUVDoorMonitor is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#SPSUAUVDoorMonitor is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with SPSUAUVDoorMonitor. If not, see http://www.gnu.org/licenses/.
#--------------------------------------------------------------------------

#Edit the credentials at or near line 83
 
import serial
import datetime
import smtplib
import cv
import os, re
import sys
import time

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

nmorning = 10;#Time to stop monitoring
nevening = 22;#Time to start monitoring

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
 
sender = 'spsu.auv.team+security@gmail.com'
recipient = 'taylormartin357@gmail.com, tmartin3@spsu.edu'
#subject = 'AUV After Hours Access'
 
ser = serial.Serial('/dev/ttyACM0',9600)

def savepic():
    cap = cv.CreateCameraCapture(0)
    if not cap:
        print("!!! Failed CreateCameraCapture: invalid parameter!")
    img = cv.QueryFrame(cap)
    cv.SaveImage('suspect.jpg',img)
    del cap
    pass

def opened():
    now = datetime.datetime.now()
    time.sleep(1)
    savepic()
    
    msg = MIMEMultipart()
    msg['Subject'] = "AUV After Hours Access %s" %now.strftime("%A, %d. %B %Y %I:%M%p")
    msg['To'] = recipient
    msg['From'] = sender
        
    message = 'The AUV Lab door was opened at ' + now.strftime("%A, %d. %B %Y %I:%M%p") +'\r\n\r\nhttp://10.36.1.160:8080/ie.htm\r\n\r\n\r\nAUV Security'
    message = "" + message + ""
     
    img = MIMEImage(open('suspect.jpg', 'rb').read(), _subtype="jpg")
    img.add_header('Content-Disposition', 'attachment', filename='suspect.jpg')
    msg.attach(img)
    
    part = MIMEText('text', "plain")
    part.set_payload(message)
    msg.attach(part)
    
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login('spsuauvteam', 'SPSU.Zodiac.0540')
 
    session.sendmail(sender, recipient, msg.as_string())
    session.quit()
    
    print 'Opened'
    print now
    print ''
    
def closed():
    print 'Closed'
    print datetime.datetime.now()
    print ''

while True:
    morning = datetime.datetime.now().replace(hour=nmorning, minute=0, second=0, microsecond=0)
    evening = datetime.datetime.now().replace(hour=nevening, minute=0, second=0, microsecond=0)
    hour = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    if hour < morning or hour > evening:
        red = ser.read()
        if red == '1':
            closed()
        elif red == '0':
            opened()
    pass

ser.close()
