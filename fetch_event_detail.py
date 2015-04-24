#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
from os.path import expanduser
import re
import time
from pygeocoder import Geocoder

from libs import KKTIX
from h4_scripts.Facebook import Facebook, Graph

from models.group_websites import GroupWebsitesModel
from models.group_facebook_id import GroupFacebookIDModel
from models.events import EventsModel
from models.places import PlacesModel
group_websites_model = GroupWebsitesModel()
group_facebook_id_model = GroupFacebookIDModel()
events_model = EventsModel()
places_model = PlacesModel()

config_file = expanduser("~") + '/.opensourcefeeds.cfg'
config = ConfigParser.SafeConfigParser()
config.read(config_file)

# meetup = Meetup(config.get('MEETUP', 'key'))

facebook = Facebook()
facebook.login(config.get('FACEBOOK', 'username'), config.get('FACEBOOK', 'password'))
token = facebook.get_token()
facebook_graph = Graph(token)


# def parse_meetup_group_urlname(url):
#     m = re.search('http://www.meetup.com/([\w-]+)[/]?', url)
#     if m:
#         group_urlname = m.groups()[0]
#
#         return group_urlname
#     else:
#         print '* error : group name search failed %s' % group_website.url
#
#
# def parse_accupass_org_id(url):
#     m = re.search('http://www.accupass.com/org/detail/r/(\d+)/1/0', url)
#     if m:
#         org_id = m.groups()[0]
#
#         return org_id
#     else:
#         print '* error : org id search failed %s' % group_website.url
#
#
# def get_facebook_id(url):
#     m = re.search('http[s]?://www.facebook.com/groups/([\w\.]+)[/]?', url)
#
#     if not m:
#         m = re.search('http[s]?://www.facebook.com/([\w\.]+)[/]?', url)
#
#     facebook_id = None
#     if m and re.search('([a-zA-Z\.]+)', m.groups()[0]):
#         urlname = m.groups()[0]
#
#         # 查詢資料庫是否已有 group id
#         facebook_id = db.session.query(GroupFacebookID).filter(GroupFacebookID.group_urlname == urlname).first()
#
#         if facebook_id:
#             facebook_id = facebook_id.facebook_id
#         else:
#             facebook_id = facebook.get_facebook_id(urlname)
#
#             if facebook_id:
#                 db.session.execute(GroupFacebookID.__table__.insert({'group_urlname': urlname, 'facebook_id': facebook_id}))
#                 db.session.commit()
#     elif m:
#         facebook_id = m.groups()[0]
#
#     return facebook_id


def parse_facebook_event_id(url):
    m = re.search('https://www.facebook.com/events/(\d+)', url)
    if m:
        event_id = m.groups()[0]

        return event_id


def address_to_coordinates(address):
    try:
        results = Geocoder.geocode(address)

        return results[0].coordinates
    except:
        print 'address not found : %s' % address
        return None


def search_and_create_place(name, address=None, lat=None, lng=None):
    # if address and lat and lng:
    #     place = db.session.query(Places).filter(Places.name == name, Places.address == address, Places.lat == lat, Places.lng == lng).first()
    #
    #     if not place:
    #         return create_place(name, address, lat, lng)
    if lat and lng:
        place = places_model.find(**{'name': name, 'lat': lat, 'lng': lng})

        if not place:
            return places_model.add(name, lat=lat, lng=lng)
    # elif address:
    #     place = db.session.query(Places).filter(Places.name == name, Places.address == address).first()
    #
    #     if not place:
    #         # 只有地址，嘗試搜尋坐標
    #         coordinates = address_to_coordinates(address)
    #
    #         if coordinates:
    #             return create_place(name, address, coordinates[0], coordinates[1])
    #         else:
    #             return create_place(name, address)
    elif address:
        coordinates = address_to_coordinates(address)

        if coordinates:
            lat = coordinates[0]
            lng = coordinates[1]

            place = places_model.find(**{'name': name, 'lat': lat, 'lng': lng})

            if not place:
                return places_model.add(name, address, lat, lng)
        else:
            place = places_model.find(**{'name': name, 'address': address})

            if not place:
                return places_model.add(name, address)
    else:
        coordinates = address_to_coordinates(name)

        if coordinates:
            lat = coordinates[0]
            lng = coordinates[1]

            place = places_model.find(**{'name': name, 'lat': lat, 'lng': lng})

            if not place:
                return places_model.add(name, lat=lat, lng=lng)
        else:
            place = places_model.find(**{'name': name})

            if not place:
                return places_model.add(name)

    return place.id


if __name__ == '__main__':
    events = events_model.find_all_match_url('kktix', **{'place': None, 'people_count': None})
    evnets = events + events_model.find_all_match_url('meetup', **{'place': None, 'people_count': None})
    evnets = events + events_model.find_all_match_url('facebook', **{'place': None, 'people_count': None})
    evnets = events + events_model.find_all_match_url('accupass', **{'place': None, 'people_count': None})
    # events = db.session.query(Events).filter(Events.url.like('%facebook%'), db.or_(Events.place == None, Events.people_count == None)).all()
    # events = db.session.query(Events).filter(Events.id == 824, db.or_(Events.place == None, Events.people_count == None)).all()

    for event in events:
        try:
            print event.url

            event_detail = None
            if 'kktix' in event.url:
                event_detail = KKTIX.get_event(event.url)
            # elif group_website.name == 'Meetup':
            #     group_urlname = parse_meetup_group_urlname(group_website.url)
            #
            #     events = meetup.get_recent_event(group_urlname, status='past')
            # elif group_website.name == 'Accupass':
            #     org_id = parse_accupass_org_id(group_website.url)
            #
            #     events = Accupass.get_past_event(org_id)
            elif 'facebook' in event.url:
                facebook_event_id = parse_facebook_event_id(event.url)
                print facebook_event_id

                if facebook_event_id:
                    event_detail = facebook_graph.getEvent(facebook_event_id)

            if event_detail:
                if not event.place:
                    place = None

                    if 'place_name' in event_detail and 'address' in event_detail and 'lat' in event_detail and 'lng' in event_detail:
                        place = search_and_create_place(event_detail['place_name'], event_detail['address'], event_detail['lat'], event_detail['lng'])
                    elif 'place_name' in event_detail and 'lat' in event_detail and 'lng' in event_detail:
                        place = search_and_create_place(event_detail['place_name'], lat=event_detail['lat'], lng=event_detail['lng'])
                    elif 'place_name' in event_detail and 'address' in event_detail:
                        place = search_and_create_place(event_detail['place_name'], event_detail['address'])
                    elif 'place_name' in event_detail:
                        place = search_and_create_place(event_detail['place_name'])

                    if place:
                        events = events_model.update(event.id, {'place': place})
                    else:
                        print 'place not found'

                if not event.people_count and 'people_count' in event_detail:
                    events = events_model.update(event.id, {'people_count': event_detail['people_count']})

            time.sleep(1)
        except Exception, e:
            print e
