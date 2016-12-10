#!/usr/bin/python2
# -*- coding: utf-8 -*-

import feedparser
import datetime
import PyRSS2Gen
import sys
import re
import time
from BeautifulSoup import BeautifulSoup

from urllib import urlopen

def download(url):
    try:
        feed = feedparser.parse( urlopen( url ) )
    except:
        sys.stderr.write( 'Error reading url ' + url + '\n' )
        #sys.exit( 127 )
        feed = None
    return feed


def process_description( text ):
    #p = html2text.html2text( text )
    soup = BeautifulSoup(text)
    text_parts = soup.findAll(text=True)
    p = ''.join(text_parts)
    if( len( p ) < 500 ):
        return( p )
    return p[0:300] + '[...]'


def is_too_old(post_parsed_date):
    post_date = datetime.datetime( *post_parsed_date[:6] )
    return (right_now - post_date).days > 60


def when_post( post_parsed_date ):
    post_date = datetime.datetime( *post_parsed_date[:6] )
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

def create_html( entries ):
    f_html = open( '/tmp/r_blogs_mashup.php', 'w' )
    f_html.write( " <?php require('./daphplib/common01.php'); ?> " )
    f_html.write( " <title>Datanalytics.com: Noticias sobre R en español</title> " )
    f_html.write( " <meta name='description' content='Noticias sobre R en español'/> " )
    f_html.write( " <meta name='keywords' content='r, blog, mashup'/> " )
    f_html.write( " <style type='text/css'> .raggregate_date {font-style = italic ; font-size = 8px; text-align: right} </style> ")
    f_html.write( " <?php require('./daphplib/common02.php'); ?> " )
    f_html.write( " <?php require('./daphplib/common03.php'); ?> " )
    f_html.write( " <h1>Noticias sobre R de la blogosfera en español</h1> " )
    #f_html.write( " <ul>" )
    for entry in entries:
        #html_string  = "<li>"
        html_string  = '<a href="' + entry['link'] + '">' + entry['title'] + '</a>' 
        html_string += '  (' + when_post( entry['date_parsed'] ) + ')'
        html_string += "<br/>"
        #html_string += "<div class='raggregate_date'> " + when_post( entry['date_parsed'] ) + "</div>"
        html_string += process_description( entry['description'] )
        html_string += "<p></p>"
        #html_string += "</li>"
        f_html.write( html_string.encode('utf-8') )
    #f_html.write( " </ul>" )
    f_html.write( "<div class = 'raggregate_date'><a href='/r_blogs_mashup.rss'>RSS</a></div>" )
    f_html.write( " <?php require('./daphplib/common04.php'); ?> " )
    f_html.close()
    
right_now = datetime.datetime( *time.localtime()[:6] )

urls =  [ 
            'http://rchibchombia.blogspot.com/feeds/posts/default',                     # r chibchombia
            'http://emilopezcano.blogspot.com/feeds/posts/default',                     # emilio lopez cano
            'https://www.blogger.com/feeds/1685427845194108708/posts/default',          # ibarra chile
            'http://i314.com.ar/?feed=atom',                                            # i314 argentina
            'http://statisticalecology.blogspot.com/feeds/posts/default',               # ecolog'ia estad'istica
            'http://www.datanalytics.com/blog/feed',                                    # m'io
            'http://analisisydecision.es/feed/',                                        # rvaquerizo
            'http://acercad.wordpress.com/feed/',                                       # Jaume Tormo
            'http://feeds.feedburner.com/Geomarketing',                                 # GMK
            'http://rprojectsp.blogspot.com/feeds/posts/default',                       # Bebilda
            #'http://predictive.wordpress.com/feed/',                                    # Apuntes de estad'istica
            'http://erre-que-erre-paco.blogspot.com/feeds/posts/default?alt=rss',       # erreros
            'http://feeds.feedburner.com/analisis-comunicacion-datos-cuantitativos',    # gibaja
            #'http://www.grserrano.es/wp/feed/',                                         # serrano
            'http://procomun.wordpress.com/feed/',                                      # oscar perpignan
            'http://atejada.blogspot.com/feeds/posts/default?alt=rss',                  # alvaro tejada
            'http://negociness.blogspot.com/feeds/posts/default',                       # otto wagner
            'http://ecologicaconciencia.wordpress.com/feed/',                       	# lola ferrer castán
            'http://www.dataprix.com/taxonomy/term/2598/all/feed',                      # juan vidal gil
            'http://computandocienciapolitica.blogspot.com/feeds/posts/default',        # fede .c
            'http://sevillarusers.wordpress.com/feed/',                                 # grupo de usuarios de R de Sevilla   
            'http://estadisticadeaaz.blogspot.com/feeds/posts/default?alt=rss',         # Gigi Voinea
            'http://xrazonesparay.wordpress.com/feed/',                                 # inés garmendia
            'https://pedroconcejero.wordpress.com/feed/',                               # pedro concejero
            'https://medium.com/feed/kschool-data-scientists',                          # Kschool ciencia de datos (1a edicion)
            'http://bipostit.com/feed/', 		                                # 
            'http://luiscayuela.blogspot.com/feeds/posts/default'                       # luis cayuela
        ]

r_tags = [ 'r', u'r', 'R', u'C\xf3digo en R', u'R-castellano', 'R Tips', u'R' ]

feeds = [ download( url ) for url in urls ]
feeds = filter( lambda x: not x is None, feeds )

entries = []
for feed in feeds:
    for entry in feed[ "items" ]:
        if entry.has_key( 'tags' ) and any( [ tag['term'] in r_tags for tag in entry['tags'] ] ):
            if entry.has_key("date_parsed"):
                post_parsed_date = entry["date_parsed"]
            elif entry.has_key("updated_parsed"):
                post_parsed_date = entry["updated_parsed"]
            elif entry.has_key("published_parsed"):
                post_parsed_date = entry["published_parsed"]
            else:
                continue
            if not is_too_old(post_parsed_date):
                entries.append((post_parsed_date, entry)) 

entries.sort( reverse = True )
entries = [ entry for (date,entry) in entries ]

#create_html( entries )                                  # Creo el fichero de html

entries_out = []
for entry in entries:
    entries_out.append( PyRSS2Gen.RSSItem( 
                    title       = entry['title'], 
                    link        = entry['link'], 
                    guid        = entry['link'], 
                    description = process_description( entry['description'] ), 
                    pubDate     = get_date(entry)))

rss = PyRSS2Gen.RSS2(
    title = "Noticias de R en español",
    link = "http://www.datanalytics.com/2010/06/03/agregador-de-noticias-sobre-r-en-espanol/",
    description = "Agregación de noticias sobre R en español",
    lastBuildDate = datetime.datetime.now(),
    items = entries_out
 )

rss.write_xml( open( "/tmp/r_blogs_mashup.rss", "w" ), encoding = "utf-8" )

