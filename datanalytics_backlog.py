#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import datetime
import random
import urllib

from bs4 import BeautifulSoup
import requests as req
import PyRSS2Gen

# get all blog entries (older than...)

resp = req.get('https://datanalytics.com/sitemap.xml')
soup = BeautifulSoup(resp.text, features='xml')

r = re.compile('https://www.datanalytics.com/[0-9]{4}/[0-9]{2}/[0-9]{2}/*')

all_links = soup.find_all('url')
all_links = [x.loc.text for x in all_links]
all_links = list(filter(r.match, all_links))

date = datetime.datetime.now().date() - datetime.timedelta(days = 400)
current_year = date.strftime("%Y")

all_links = [x for x in all_links if re.search('https://www.datanalytics.com/([0-9]{4})/*', x).group(1) < current_year]

my_new_entry = random.choice(all_links)


# get entry elements

req = urllib.request.Request(my_new_entry)
soup = BeautifulSoup(urllib.request.urlopen(req).read().decode("utf-8"), 'html.parser')

title       = soup.findAll(attrs={"property": "og:title"})[0]['content']
description = soup.findAll(attrs={"property": "og:description"})[0]['content']
#pubDate     = soup.findAll(attrs={"property": "article:published_time"})[0]['content']


# build a feed

entries_out = [
    PyRSS2Gen.RSSItem(
        title       = title,
        link        = my_new_entry,
        #guid        = my_new_entry,
        description = description,
        pubDate     = datetime.datetime.now()
    )
]

rss = PyRSS2Gen.RSS2(
    title = 'Datanalytics - Random old posts',
    link = 'https://www.datanalytics.com',
    description = 'A random old post from datanalytics.com a couple times a day',
    lastBuildDate = datetime.datetime.now(),
    items = entries_out
)

rss.write_xml(open('/tmp/random_old_post.rss', "w"), encoding = "utf-8")
