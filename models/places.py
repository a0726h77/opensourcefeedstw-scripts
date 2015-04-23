#!/usr/bin/env python
# encoding: utf-8

import db
from db.orm.places import Places


class PlacesModel(object):
    def find(self, **kwargs):
        query = Places.query

        for attr, value in kwargs.iteritems():
            query = query.filter(getattr(Places, attr) == value)

        return query.first()

    def add(self, name, address=None, lat=None, lng=None):
        data = {
            'name': name,
            'address': address,
            'lat': lat,
            'lng': lng
        }

        place = Places(**data)
        db.session.add(place)
        db.session.commit()

        return place.id
