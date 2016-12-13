#!/usr/bin/python2
# -*- coding: utf-8 -*-

from auxfuns import process_entries

urls =  [
            'http://rchibchombia.blogspot.com/feeds/posts/default',                     # r chibchombia
            'http://emilopezcano.blogspot.com/feeds/posts/default',                     # emilio lopez cano
            'https://www.blogger.com/feeds/1685427845194108708/posts/default',          # ibarra chile
            'http://i314.com.ar/?feed=atom',                                            # i314 argentina
            'http://statisticalecology.blogspot.com/feeds/posts/default',               # ecolog'ia estad'istica
            'http://www.datanalytics.com/feed',                                         # m'io
            'http://analisisydecision.es/feed/',                                        # rvaquerizo
            'http://acercad.wordpress.com/feed/',                                       # Jaume Tormo
            'http://feeds.feedburner.com/Geomarketing',                                 # GMK
            'http://rprojectsp.blogspot.com/feeds/posts/default',                       # Bebilda
            #'http://predictive.wordpress.com/feed/',                                    # Apuntes de estad'istica
            'http://erre-que-erre-paco.blogspot.com/feeds/posts/default?alt=rss',       # erreros
            'http://feeds.feedburner.com/analisis-comunicacion-datos-cuantitativos',    # gibaja
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

rss_metadata = {
    'title'       : "Noticias de R en español",
    'link'        :  "http://www.datanalytics.com/2010/06/03/agregador-de-noticias-sobre-r-en-espanol/",
    'description' : "Agregación de noticias sobre R en español"
}

output_file = "/tmp/r_blogs_mashup.rss"

process_entries(urls, r_tags, rss_metadata, output_file)


