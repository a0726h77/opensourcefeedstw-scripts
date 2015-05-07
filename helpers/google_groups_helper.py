#!/usr/bin/env python
# encoding: utf-8

import re


def parse_google_groups_url_name(url):
    m = None

    if re.search('https://groups.google.com/forum/#!forum/([\w\-]+)', url):
        m = re.search('https://groups.google.com/forum/#!forum/([\w\-]+)', url)
    elif re.search('https://groups.google.com/forum/\?fromgroups#!forum/([\w\-]+)', url):
        m = re.search('https://groups.google.com/forum/\?fromgroups#!forum/([\w\-]+)', url)

    if m:
        return m.groups()[0]


def generate_google_groups_rss_url(url):
    name = parse_google_groups_url_name(url)

    if name:
        return 'https://groups.google.com/group/%s/feed/rss_v2_0_msgs.xml' % name
