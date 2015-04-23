#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import os
from os.path import expanduser
import sys
import re
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../lib')

import KKTIX
import Accupass
from Meetup import Meetup
from Facebook import Facebook, Graph

from model.group_facebook_id import GroupFacebookIDModel
from model.events import EventsModel
from model.group_websites import GroupWebsitesModel
group_facebook_id_model = GroupFacebookIDModel()
events_model = EventsModel()
group_websites_model = GroupWebsitesModel()

config_file = expanduser("~") + '/.opensourcefeeds.cfg'
config = ConfigParser.SafeConfigParser()
config.read(config_file)

meetup = Meetup(config.get('MEETUP', 'key'))

facebook = Facebook()
facebook.login(config.get('FACEBOOK', 'username'), config.get('FACEBOOK', 'password'))
token = facebook.get_token()
facebook_graph = Graph(token)


def parse_meetup_group_urlname(url):
    m = re.search('http://www.meetup.com/([\w-]+)[/]?', url)
    if m:
        group_urlname = m.groups()[0]

        return group_urlname
    else:
        print '* error : group name search failed %s' % group_website.url


def parse_accupass_org_id(url):
    m = re.search('http://www.accupass.com/org/detail/r/(\d+)/1/0', url)
    if m:
        org_id = m.groups()[0]

        return org_id
    else:
        print '* error : org id search failed %s' % group_website.url


def get_facebook_id(url):
    m = re.search('http[s]?://www.facebook.com/groups/([\w\.]+)[/]?', url)

    if not m:
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


# def get_facebook_group_id(url):
#     m = re.search('https://www.facebook.com/groups/([\w\.]+)[/]?', url)
#
#     group_id = None
#     if m and re.search('([a-zA-Z\.]+)', m.groups()[0]):
#         group_urlname = m.groups()[0]
#
#         # 查詢資料庫是否已有 group id
#         group_id = db.session.query(GroupFacebookID).filter(GroupFacebookID.group_urlname == group_urlname).first()
#
#         if group_id:
#             group_id = group_id.facebook_id
#         else:
#             group_id = facebook.get_group_id(group_urlname)
#
#             if group_id:
#                 db.session.execute(GroupFacebookID.__table__.insert({'group_urlname': group_urlname, 'facebook_id': group_id}))
#                 db.session.commit()
#     elif m:
#         group_id = m.groups()[0]
#
#     return group_id

if __name__ == '__main__':
    group_websites = group_websites_model.find_all_by_names(['KKTIX', 'Meetup', 'Facebook', 'Accupass'])
    # group_websites = db.session.query(GroupWebsites).filter(db.or_(GroupWebsites.name == 'KKTIX', GroupWebsites.name == 'Meetup', GroupWebsites.name == 'Facebook', GroupWebsites.name == 'Accupass')).all()
    # group_websites = db.session.query(GroupWebsites).filter(GroupWebsites.group_id == 10).all()

    for group_website in group_websites:
        try:
            print group_website.url

            events = None
            if group_website.name == 'KKTIX':
                events = KKTIX.get_recent_event(group_website.url)
            elif group_website.name == 'Meetup':
                group_urlname = parse_meetup_group_urlname(group_website.url)

                events = meetup.get_recent_event(group_urlname)
            elif group_website.name == 'Accupass':
                org_id = parse_accupass_org_id(group_website.url)

                events = Accupass.get_recent_event(org_id)
            elif group_website.name == 'Facebook':
                # group_id = get_facebook_group_id(group_website.url)
                #
                # if group_id:
                #     events = facebook_graph.getGroupRecentEvents(group_id)

                facebook_id = get_facebook_id(group_website.url)

                if facebook_id:
                    events = facebook_graph.getRecentEvents(facebook_id)

            if events:
                for event in events:
                    print event

                    ## 資料庫沒有資料才新增 ##
                    ev = events_model.find_all(group_website.group_id, event['url'])

                    if not ev:
                        start_datetime = None
                        end_datetime = None
                        if 'start_datetime' in event:
                            start_datetime = event['start_datetime']
                        if 'end_datetime' in event:
                            end_datetime = event['end_datetime']

                        events_model.add(group_website.group_id, event['name'], event['url'], start_datetime, end_datetime)
                    ## 資料庫沒有資料才新增 ##

            time.sleep(1)
        except Exception, e:
            print e
