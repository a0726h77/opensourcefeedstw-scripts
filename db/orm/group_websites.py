# -*- coding: utf-8 -*-

import db


class GroupWebsites(db.Base):
    __tablename__ = 'group_websites'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    feed_url = db.Column(db.String(255))
    feed_cache_date = db.Column(db.DateTime)
    feed_cache_attempt_date = db.Column(db.DateTime)

    # def get_all(self):
    #     # return GroupWebsites.query.all()
    #     # return self.query.all()
    #     # return super(GroupWebsites, self).query.all()
    #     return super(self.__class__, self).query.all()
