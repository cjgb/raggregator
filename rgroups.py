#!/usr/bin/python3
# -*- coding: utf-8 -*-

from feedparser import parse
from datetime import datetime
import PyRSS2Gen
import sys
import re
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen

def download(url):
    try:
        feed = parse(urlopen(url))
    except:
        sys.stderr.write('Error reading url ' + url + '\n')
        feed = None
    return feed


def process_description( text ):
    text_parts = BeautifulSoup(text, "lxml").findAll(text=True)
    p = ''.join(text_parts)
    if(len(p) < 500):
        return(p)
    return p[0:300] + '[...]'


def is_too_old(post_parsed_date):
    post_date = datetime(*post_parsed_date[:6])
    return (right_now - post_date).days > 60


def when_post(post_parsed_date):
    post_date = datetime(*post_parsed_date[:6])
    days = (right_now - post_date).days
    if days == 0:
        return "Hoy"
    if days == 1:
        return "Ayer"
    return "Hace " + str(days) + u" días"


def get_date(entry):
    if entry.has_key("date"):
        return(entry["date"])
    elif entry.has_key("published"):
        return(entry["published"])
    else:
        return("unknown")


right_now = datetime(*time.localtime()[:6])

urls =  ["https://rugbcn.wordpress.com/feed/", 
         "http://madrid.r-es.org/feed/",
         "https://sevillarusers.wordpress.com/feed/",
         "https://almeriarusers.wordpress.com/feed/",
         "https://valenciarusers.wordpress.com/feed/",
         "https://ralamanca.wordpress.com/feed/",
         "https://www.r-users.gal/noticias.xml"]

feeds = [download(url) for url in urls]
feeds = [x for x in feeds if x is not None]

entries = []
for feed in feeds:
    for entry in feed["items"]:
        if entry.has_key("date_parsed"):
            post_parsed_date = entry["date_parsed"]
        elif entry.has_key("updated_parsed"):
            post_parsed_date = entry["updated_parsed"]
        elif entry.has_key("published_parsed"):
            post_parsed_date = entry["published_parsed"]
        else:
            sys.stderr.write('Warning: entry without timestamp' + '\n')
            continue
        if not is_too_old(post_parsed_date):
            entries.append((post_parsed_date, entry)) 

entries.sort(reverse = True)
entries = [entry for (date,entry) in entries]

entries_out = []
for entry in entries:
    entries_out.append(PyRSS2Gen.RSSItem( 
                    title       = entry['title'], 
                    link        = entry['link'], 
                    guid        = entry['link'], 
                    description = process_description( entry['description'] ), 
                    pubDate     = get_date(entry)))

rss = PyRSS2Gen.RSS2(
    title = "Noticias de los grupos locales de usuarios de R en España",
    link = "http://r-es.org/grupos-locales/",
    description = "Noticias de los grupos locales de usuarios de R en España",
    lastBuildDate = datetime.now(),
    items = entries_out
 )

rss.write_xml(open("/tmp/r_groups_spain.rss", "w"), encoding = "utf-8")

