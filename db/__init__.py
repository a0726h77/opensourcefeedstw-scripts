#!/usr/bin/env python
# encoding: utf-8

from os.path import expanduser
import ConfigParser
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.sql import func

config_file = expanduser("~") + '/.opensourcefeeds.cfg'
Config = ConfigParser.ConfigParser()
Config.read(config_file)

engine = create_engine('mysql://%s:%s@%s/%s?charset=utf8&use_unicode=0' % (Config.get('DATABASE', 'username'), Config.get('DATABASE', 'password'), Config.get('DATABASE', 'host'), Config.get('DATABASE', 'database')))

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()
