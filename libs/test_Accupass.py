# -*- coding: utf-8 -*-

import os

import Accupass

DRY_RUN = True if os.environ.get('DRY_RUN') == 'True' else False

ORG_ID = 965090279531912
EVENT_URL = ''


def test_get_recent_event():
    assert Accupass.get_recent_event(ORG_ID)


def test_get_past_event():
    assert Accupass.get_past_event(ORG_ID)


# def test_get_event():
#     assert Accupass.get_event(EVENT_URL)
