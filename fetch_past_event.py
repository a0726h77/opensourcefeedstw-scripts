#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
from os.path import expanduser
import re
import time

from libs import KKTIX
from libs import Accupass
from libs.Meetup import Meetup
from h4_scripts.Facebook import Facebook, Graph

from models.group_facebook_id import GroupFacebookIDModel
from models.events import EventsModel
from models.group_websites import GroupWebsitesModel
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

if __name__ == '__main__':
    group_websites = group_websites_model.find_all_by_names(['KKTIX', 'Meetup', 'Facebook', 'Accupass'])

    for group_website in group_websites:
        try:
            print group_website.url

            events = None
            if group_website.name == 'KKTIX':
                events = KKTIX.get_past_event(group_website.url)
            # elif group_website.name == 'Meetup':
            #     group_urlname = parse_meetup_group_urlname(group_website.url)
            #
            #     events = meetup.get_recent_event(group_urlname, status='past')
            elif group_website.name == 'Accupass':
                org_id = parse_accupass_org_id(group_website.url)

                events = Accupass.get_past_event(org_id)
            elif group_website.name == 'Facebook':
                facebook_id = get_facebook_id(group_website.url)
                print facebook_id

                if facebook_id:
                    events = facebook_graph.getPastEvents(facebook_id)

            if events:
                for event in events:
                    # print event

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
