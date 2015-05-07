#!/usr/bin/env python
# encoding: utf-8

import re


def parse_kktix_org_subdomain_url(url):
    m = re.search('(http://[\w\-]+.kktix.cc/)', url)

    if m:
        return m.groups()[0]


def generate_kktix_rss_url(url):
    domain = parse_kktix_org_subdomain_url(url)

    if domain:
        return '%sevents.atom' % domain
