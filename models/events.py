#!/usr/bin/env python
# encoding: utf-8

import db
from db.orm.events import Events


class EventsModel(object):
    def find_all(self, group_id, url):
        return Events.query.filter(Events.group_id == group_id, Events.url == url).all()

    def find_all_match_url(self, url, **kwargs):
        query = Events.query.filter(Events.url.like('%%%s%%' % url))

        if kwargs:
            for attr, value in kwargs.iteritems():
                query = query.filter(getattr(Events, attr) == value)

        return query.all()

    def add(self, group_id, name, url, start_datetime=None, end_datetime=None):
        data = {
            'group_id': group_id,
            'name': name,
            'url': url,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime
        }

        event = Events(**data)
        db.session.add(event)
        db.session.commit()

        return event.id

    def update(self, id, values):
        rows = Events.query.filter(Events.id == id).update(values)

        db.session.commit()

        if rows:
            return id
