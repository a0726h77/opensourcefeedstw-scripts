#!/usr/bin/env python
# encoding: utf-8

import requests
from BeautifulSoup import BeautifulSoup
import datetime
import re


def get_recent_event(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    results = []
    for content_div in soup.findAll('div', attrs={'class': 'content-block'}):
        for h2 in content_div.findAll('h2'):
            if h2.text.encode('utf-8') in ['近期公開活動', 'Recent Events']:
                for li in content_div.findAll('li', attrs={'class': 'clearfix'}):
                    _ = {}

                    link = li.find('h2').find('a')
                    _['name'] = link.text
                    _['url'] = link['href']

                    time = li.find('span', attrs={'class': 'timezoneSuffix'})
                    dt = datetime.datetime.strptime(time.text, "%Y/%m/%d %H:%M(+0800)")
                    _['start_datetime'] = dt

                    results.append(_)

    if results:
        return results


def get_past_event(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    results = []
    for content_div in soup.findAll('div', attrs={'class': 'content-block'}):
        for h2 in content_div.findAll('h2'):
            if h2.text.encode('utf-8') in ['曾舉辦的活動', 'Past Events']:
                for li in content_div.findAll('li'):
                    _ = {}

                    link = li.find('a')
                    _['name'] = link.text
                    _['url'] = link['href']

                    results.append(_)

    if results:
        return results

def get_event(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    event = {}
    try:
        i = 1
        for li in soup.find('div', attrs={'class': 'event-info'}).findAll('li'):
            if i == 1:  # datetime
                j = 1
                for time_span in li.findAll('span', attrs={'class': 'timezoneSuffix'}):
                    if j == 1:
                        event['start_datetime'] = datetime.datetime.strptime(time_span.text, "%Y/%m/%d %H:%M(+0800)")
                    elif j == 2:
                        event['end_datetime'] = datetime.datetime.strptime(time_span.text, "%Y/%m/%d %H:%M(+0800)")
                    j = j + 1
            elif i == 2 or i == 3:
                # people count
                m = re.search("(\d+) \/ (\d+)", li.text)
                if m:
                    event['people_count'] = m.groups()[1]
                else:
                    # address
                    m = re.search("(.*) \/ (.*)", li.text)
                    if m:
                        event['place_name'] = m.groups()[0]
                        event['address'] = m.groups()[1]
                    else:
                        m = re.search("(.*)", li.text)
                        if m and u'聯絡主辦單位' not in m.groups()[0]:
                            event['place_name'] = m.groups()[0]

            i = i + 1
    except:
        pass

    if event:
        return event


class KKTIX():
    def __init__(self, debug=False):
        pass
