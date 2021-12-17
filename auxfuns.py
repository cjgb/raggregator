import feedparser
import sys
#import urllib2
import urllib.request, urllib.error, urllib.parse
import datetime
import PyRSS2Gen
import time
from bs4 import BeautifulSoup

def download(url):
    #opener = urllib2.build_opener()
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')]
    try:
        feed = feedparser.parse(opener.open(url, timeout = 10))
    except:
        sys.stderr.write( 'Error reading url ' + url + '\n' )
        #sys.exit( 127 )
        feed = None
    return feed

def process_description( text ):
    soup = BeautifulSoup(text, features="html.parser")
    text_parts = soup.findAll(text=True)
    p = ''.join(text_parts)
    if( len( p ) < 500 ):
        return( p )
    return p[0:300] + '[...]'

def is_too_old(post_parsed_date, right_now):
    post_date = datetime.datetime( *post_parsed_date[:6] )
    return (right_now - post_date).days > 60

def get_date(entry):
    if "date" in entry:
        return(entry["date"])
    elif "published" in entry:
        return(entry["published"])
    else:
        return("unknown")

def process_entries(urls, r_tags, rss_metadata, output_file):

    right_now = datetime.datetime( *time.localtime()[:6] )

    feeds = [download(url) for url in urls]
    feeds = [x for x in feeds if not x is None]

    entries = []
    for feed in feeds:
        for entry in feed[ "items" ]:
            if "date_parsed" in entry:
                post_parsed_date = entry["date_parsed"]
            elif "updated_parsed" in entry:
                post_parsed_date = entry["updated_parsed"]
            elif "published_parsed" in entry:
                post_parsed_date = entry["published_parsed"]
            else:
                continue

            if len(r_tags) > 0 and \
                entry.has_key('tags') and \
                not any([tag['term'] in r_tags for tag in entry['tags']]):
                continue

            if not is_too_old(post_parsed_date, right_now):
                entries.append((post_parsed_date, entry))

    entries.sort(reverse = True, key=lambda x: x[0])
    entries = [ entry for (date,entry) in entries ]


    entries_out = []
    for entry in entries:
        entries_out.append(PyRSS2Gen.RSSItem(
                        title       = entry['title'],
                        link        = entry['link'],
                        guid        = entry['link'],
                        description = process_description( entry['description'] ),
                        pubDate     = get_date(entry)))

    rss = PyRSS2Gen.RSS2(
        title = rss_metadata['title'],
        link = rss_metadata['link'],
        description = rss_metadata['description'],
        lastBuildDate = datetime.datetime.now(),
        items = entries_out
     )

    rss.write_xml(open(output_file, "w"), encoding = "utf-8")
