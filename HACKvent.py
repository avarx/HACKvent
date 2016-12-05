#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
from PIL import Image
import datetime
import io
import json
import requests
import sys
import urllib2 as urllib
import zbarlight

HV_URL = 'http://hackvent.hacking-lab.com'
HV_TICKET = 'YOUR_TICKET'
HV_USER = 'YOUR_USERNAME'
HV_COOKIE = {'HACKvent_Ticket': HV_TICKET,'HACKvent_User':HV_USER}
HV_SERIVCEURL = 'http://hackvent.hacking-lab.com/load.php?service=';

def get_url(url):
    if HV_TICKET!='YOURTICKET':
        return HV_URL + url
    else:
        print('Change HV_TICKET!')
        sys.exit(0)

def get_challenge_content(day):
    url = get_url('/challenge.php?day='+str(day))
    r = requests.get(url,cookies=HV_COOKIE)
    c = r.content
    soup = BeautifulSoup(c, "lxml")
    desc = "Challenge Description: Day "+str(day)
    content = soup.find(text=desc).find_next("div")
    return content

def submit_flag(flag):
    data = {'code':flag}
    r = requests.post(HV_SERIVCEURL+'solution', data=data,cookies=HV_COOKIE)
    answer = json.loads(r.text)
    return(answer['txt'])

def get_flag(solution):
    data = {'code':solution, 'day':datetime.datetime.now().day, 'ticket':HV_TICKET}
    r = requests.post(HV_SERIVCEURL+'getBall', data=data)
    answer = json.loads(r.text)
    qr = answer['img']
    return scan_qr(qr)

def scan_qr(qr):
    fd = urllib.urlopen(HV_URL+'/img/'+qr)
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    code = zbarlight.scan_codes('qrcode', im)
    return code[0]