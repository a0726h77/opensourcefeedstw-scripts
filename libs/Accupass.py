#!/usr/bin/env python
# encoding: utf-8

import requests
from BeautifulSoup import BeautifulSoup
import re


def get_events(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    results = []
    for event_box in soup.findAll('div', attrs={'class': 'APCSS_linkBox-event'}):
        _ = {}

        link = event_box.find('a', attrs={'class': 'tit'})
        _['url'] = 'http://www.accupass.com%s' % link['href']

        name = link.find('strong')
        _['name'] = name.text

        time = event_box.find('span', attrs={'class': 'time'})
        m = re.search('(\d{4}-\d{2}-\d{2})', time.text)
        if m:
            _['start_datetime'] = m.groups()[0]

        results.append(_)

    if results:
        return results


def get_recent_event(org_id):
    url = 'http://www.accupass.com/org/detailtab/r/%s/1/0' % org_id

    return get_events(url)


def get_past_event(org_id):
    url = 'http://www.accupass.com/org/detailtab/r/%s/2/0' % org_id

    return get_events(url)


class Accupass():
    def __init__(self, debug=False):
        pass
