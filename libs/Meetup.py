#!/usr/bin/env python
# encoding: utf-8

import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../vendor'))

import meetup_api_client


class Meetup():
    def __init__(self, key, debug=False):
        self.meetup = meetup_api_client.Meetup(key)

    def get_recent_event(self, group_urlname):
        events = self.meetup.get_events(group_urlname=group_urlname)

        results = []
        for event in events.results:
            _ = {}

            _['name'] = event.name
            _['url'] = event.event_url

            dt = datetime.datetime.strptime(event.time, "%a %b %d %H:%M:00 CST %Y")
            _['start_datetime'] = dt

            results.append(_)

        if results:
            return results
