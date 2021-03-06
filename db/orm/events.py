# -*- coding: utf-8 -*-

import db


class Events(db.Base):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String)
    url = db.Column(db.String(255), nullable=False)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    place = db.Column(db.Integer)
    people_count = db.Column(db.Integer)
    updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
