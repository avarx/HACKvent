#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from bs4 import BeautifulSoup
import json
import requests
import sys

HV_URL = 'http://hackvent.hacking-lab.com'
HV_TICKET = 'YOURTICKET'
HV_USER = 'YOURNICK'
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