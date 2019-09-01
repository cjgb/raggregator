#!/usr/bin/python3
# -*- coding: utf-8 -*-

from auxfuns import process_entries

urls =  ["https://rugbcn.wordpress.com/feed/",
         "http://madrid.r-es.org/feed/",
         "https://sevillarusers.wordpress.com/feed/",
         "https://almeriarusers.wordpress.com/feed/",
         "https://valenciarusers.wordpress.com/feed/",
         "https://ralamanca.wordpress.com/feed/",
         "https://www.r-users.gal/noticias.xml"]

r_tags = []

rss_metadata = {
    'title'       : "Noticias de los grupos locales de usuarios de R en España",
    'link'        : "http://r-es.org/grupos-locales/",
    'description' : "Noticias de los grupos locales de usuarios de R en España"
}

output_file = "/tmp/r_groups_spain.rss"

process_entries(urls, r_tags, rss_metadata, output_file)
