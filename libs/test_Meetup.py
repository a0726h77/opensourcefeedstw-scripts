# -*- coding: utf-8 -*-

import os
from os.path import expanduser
import ConfigParser

from Meetup import Meetup

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

config_file = expanduser("~") + '/.opensourcefeeds.cfg'
config = ConfigParser.SafeConfigParser()
config.read(config_file)

GROUP_NAME = 'h4-taiwan'
EVENT_URL = ''

meetup = Meetup(config.get('MEETUP', 'key'))


def test_get_recent_event():
    assert meetup.get_recent_event(GROUP_NAME)


def test_get_past_event():
    assert meetup.get_past_event(GROUP_NAME)


# def test_get_event():
#     assert meetup.get_event(EVENT_URL)
