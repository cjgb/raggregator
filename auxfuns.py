import feedparser
import sys
import urllib2
import datetime
import PyRSS2Gen
import time
from BeautifulSoup import BeautifulSoup

def download(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')]
    try:
        feed = feedparser.parse(opener.open(url, timeout = 10))
    except:
        sys.stderr.write( 'Error reading url ' + url + '\n' )
        #sys.exit( 127 )
        feed = None
    return feed

def process_description( text ):
    soup = BeautifulSoup(text)
    text_parts = soup.findAll(text=True)
    p = ''.join(text_parts)
    if( len( p ) < 500 ):
        return( p )
    return p[0:300] + '[...]'

def is_too_old(post_parsed_date, right_now):
    post_date = datetime.datetime( *post_parsed_date[:6] )
    return (right_now - post_date).days > 60

def get_date(entry):
    if entry.has_key("date"):
        return(entry["date"])
    elif entry.has_key("published"):
        return(entry["published"])
    else:
        return("unknown")

def process_entries(urls, r_tags, rss_metadata, output_file):

    right_now = datetime.datetime( *time.localtime()[:6] )

    feeds = [download(url) for url in urls]
    feeds = filter(lambda x: not x is None, feeds)

    entries = []
    for feed in feeds:
        for entry in feed[ "items" ]:
            if entry.has_key("date_parsed"):
                post_parsed_date = entry["date_parsed"]
            elif entry.has_key("updated_parsed"):
                post_parsed_date = entry["updated_parsed"]
            elif entry.has_key("published_parsed"):
                post_parsed_date = entry["published_parsed"]
            else:
                continue

            if len(r_tags) > 0 and \
                entry.has_key('tags') and \
                not any([tag['term'] in r_tags for tag in entry['tags']]):
                continue

            if not is_too_old(post_parsed_date, right_now):
                entries.append((post_parsed_date, entry))

    entries.sort( reverse = True )
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

