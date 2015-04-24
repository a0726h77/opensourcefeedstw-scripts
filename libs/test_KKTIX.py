# -*- coding: utf-8 -*-

import os

import KKTIX

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

URL = 'http://a0726h77-a19bb8.kktix.cc/'
EVENT_URL = 'http://a0726h77-a19bb8.kktix.cc/events/c15ea1-d8112f'


def test_get_recent_event():
    assert KKTIX.get_recent_event(URL)


def test_get_past_event():
    assert KKTIX.get_past_event(URL)


def test_get_event():
    assert KKTIX.get_event(EVENT_URL)
