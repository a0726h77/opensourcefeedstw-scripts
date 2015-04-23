# -*- coding: utf-8 -*-

import db


class GroupFacebookID(db.Base):
    __tablename__ = 'group_facebook_id'

    group_urlname = db.Column(db.String(255), primary_key=True)
    facebook_id = db.Column(db.Integer)
