#!/usr/bin/env python
# encoding: utf-8

import db
from db.orm.events import Events


class EventsModel(object):
    def find_all(self, url):
        # return Events.query.filter(Events.group_id == group_id, Events.url == url).all()
        return Events.query.filter(Events.group_id == group_id, Events.url.like("%" + url + "%")).all()

    def find_all_match_url(self, url, **kwargs):
        query = Events.query.filter(Events.url.like('%%%s%%' % url))

        if kwargs:
            for attr, value in kwargs.iteritems():
                query = query.filter(getattr(Events, attr) == value)

        return query.all()

    def add(self, group_id=None, name=None, description=None, url=None, start_datetime=None, end_datetime=None, people_count=None):
        data = {
            'group_id': group_id,
            'name': name,
            'description': description,
            'url': url,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'people_count': people_count
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
