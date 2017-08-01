#!/usr/bin/env python
# encoding: utf-8

'''
2018-08-01
from meetup/python-api-client change to meetup-api
'''

import time

import meetup.api


class Meetup():
    def __init__(self, key, debug=False):
        self.meetup = meetup.api.Client(key)

    def get_recent_event(self, group_urlname):
        return self.get_events(group_urlname, 'upcoming')

    def get_past_event(self, group_urlname):
        return self.get_events(group_urlname, 'past')

    def get_events(self, group_urlname, status):
        events = self.meetup.GetEvents(group_urlname=group_urlname, status=status, fields='description')

        results = []
        for event in events.results:
            print(dir(event))
            print(event.keys())
            _ = {}

            _['name'] = event['name']
            _['url'] = event['event_url']
            _['description'] = event['description']
            _['people_count'] = event['yes_rsvp_count']
            _['start_datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event['time'] / 1000))

            results.append(_)

        if results:
            return results
