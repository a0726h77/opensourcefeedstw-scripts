#!/usr/bin/env python
# encoding: utf-8

import requests
from BeautifulSoup import BeautifulSoup
from pyquery import PyQuery as pq
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
    r = requests.get(url, headers={"Accept-Language": "en-US,en;q=0.5"})
    doc = pq(r.content)

    event = {}
    try:
        event = {}
        event['name'] = doc('h1').text()
        event['url'] = url
        event['description'] = doc('div.description').html()
        event['people_count'] = doc('div.event-attendees').find('h2').find('em').text()
        event['start_datetime'] = datetime.datetime.strptime(doc('span.timezoneSuffix')[0].text, "%Y/%m/%d(%a) %H:%M(+0800)")
        # event['end_datetime'] = ''
        place = re.search("(.*) \/ (.*)", doc('span.info-desc')[1].texteventcontent())
        event['place_name'] = place[0]
        event['address'] = place[1]
    except:
        pass

    if event:
        return event


class KKTIX():
    def __init__(self, debug=False):
        pass
