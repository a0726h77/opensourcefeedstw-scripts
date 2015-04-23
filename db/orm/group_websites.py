# -*- coding: utf-8 -*-

import db


class GroupWebsites(db.Base):
    __tablename__ = 'group_websites'

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), primary_key=True)

    # def get_all(self):
    #     # return GroupWebsites.query.all()
    #     # return self.query.all()
    #     # return super(GroupWebsites, self).query.all()
    #     return super(self.__class__, self).query.all()
