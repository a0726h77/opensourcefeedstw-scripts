#!/usr/bin/env python
# encoding: utf-8

import db
from db.orm.group_websites import GroupWebsites


class GroupWebsitesModel(object):
    def find_all_by_names(self, names):
        return GroupWebsites.query.filter(GroupWebsites.name.in_(names)).all()

    def find_all_match_url(self, url):
        return GroupWebsites.query.filter(GroupWebsites.url.like('%%%s%%' % url)).all()

    def save_feed_url(self, id, feed_url):
        values = {
            'feed_url': feed_url
        }

        rows = GroupWebsites.query.filter(GroupWebsites.id == id).update(values)

        db.session.commit()

        if rows:
            return id
