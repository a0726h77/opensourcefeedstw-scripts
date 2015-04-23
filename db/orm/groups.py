# -*- coding: utf-8 -*-

import db


class Groups(db.Base):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    alias_name = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    type = db.Column(db.Integer, nullable=False)
