#!/usr/bin/env python
# encoding: utf-8

import db
from db.orm.group_facebook_id import GroupFacebookID


class GroupFacebookIDModel(object):
    def find_group_id(self, urlname):
        return GroupFacebookID.query.filter(GroupFacebookID.group_urlname == urlname).first()

    def add(self, urlname, facebook_id):
        data = {
            'group_urlname': urlname,
            'facebook_id': facebook_id
        }

        group_facebook_id = GroupFacebookID(**data)
        db.session.add(group_facebook_id)
        db.session.commit()

        return group_facebook_id.facebook_id
