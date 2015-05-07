#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
from os.path import expanduser
import re

from h4_scripts.Facebook import Facebook, Graph

from models.group_facebook_id import GroupFacebookIDModel
group_facebook_id_model = GroupFacebookIDModel()

config_file = expanduser("~") + '/.opensourcefeeds.cfg'
config = ConfigParser.SafeConfigParser()
config.read(config_file)

facebook = Facebook()
facebook.login(config.get('FACEBOOK', 'username'), config.get('FACEBOOK', 'password'))


def get_facebook_id(url):
    if re.search('http[s]?://www.facebook.com/pages/([\w\.\-]+)/[\d]+', url):
        m = re.search('http[s]?://www.facebook.com/pages/([\w\.\-]+)/[\d]+', url)
    elif re.search('http[s]?://www.facebook.com/groups/([\w\.]+)[/]?', url):
        m = re.search('http[s]?://www.facebook.com/groups/([\w\.]+)[/]?', url)
    elif re.search('http[s]?://www.facebook.com/([\w\.]+)[/]?', url):
        m = re.search('http[s]?://www.facebook.com/([\w\.]+)[/]?', url)

    facebook_id = None
    if m and re.search('([a-zA-Z\.]+)', m.groups()[0]):
        urlname = m.groups()[0]

        # 查詢資料庫是否已有 group id
        facebook_id = group_facebook_id_model.find_group_id(urlname)

        if facebook_id:
            facebook_id = facebook_id.facebook_id
        else:
            facebook_id = facebook.get_facebook_id(urlname)

            if facebook_id:
                group_facebook_id_model.add(urlname, facebook_id)
    elif m:
        facebook_id = m.groups()[0]

    return facebook_id


def generate_facebook_rss_url(url):
    id = get_facebook_id(url)

    if id:
        return 'https://www.wallflux.com/feed/%s' % id
