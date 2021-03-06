﻿# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tal"
__category__ = "F"
__type__ = "generic"
__title__ = "tal"
__language__ = "ES"
__creationdate__ = "20130319"
__vfanart__ = "http://tal.tv/wp-content/themes/tal.tv/images/bg-body1.png"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tal.py] mainlist")    
    itemlist = []

    item.url="http://tal.tv/es"
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    '''
    <li id="menu-item-1956" class="comportamento menu-item menu-item-type-taxonomy menu-item-object-tema menu-item-1956"><a href="http://tal.tv/es/tema/comportamento">Comportamiento</a></li>
    '''
    '''patron  = '<div class="ProgDiv"[^<]+'
    patron += '<div class="ImageDiv"[^<]+'
    patron += '<img class="Image" alt="[^"]+" src="([^"]+)"/[^<]+'
    patron += '</div[^<]+'
    patron += '<div class="HSpacer"></div[^<]+'
    patron += '<div class="TextDiv"[^<]+'
    patron += '<div class="TextTitle"><a href="([^"]+)">([^<]+)</a></div[^<]+'
    patron += '<div class="TextBody">([^<]+)<'''
    patron = '<nav id="menu-temas"(.*?)</nav>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        data= matches[0]
    patron = '<li id="menu-item-[^"]+" class="[^"]+"><a[^<]+href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = scrapedurl
        itemlist.append( Item(channel=__channel__, action="videos", title=title, url=url, thumbnail="",  folder=True))

    return itemlist

def videos(item):
    logger.info("[tal.py] videos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    data = " ".join(data.split())
    #logger.info(data)
    '''
    <li class="culinaria" >
    <a href="http://tal.tv/es/video/paella-valenciana-mousse-de-parchita" >
    <img width="134" height="77" src="http://tal.tv/wp-content/uploads/2011/10/P000929-134x77.jpg" class="attachment-video-thumb wp-post-image" alt="P000929" />            </a>
    <h3><a href="http://tal.tv/es/video/paella-valenciana-mousse-de-parchita" >Probá la mousse de parchita que es sencilla. Después atrévase con la paella.</a></h3>
    <div class="dados">
    <div class="wrap-dados">
    <div class="dados-content">
    <h4>PAELLA VALENCIANA / MOUSSE…</h4>
    <span class="duracao">00:21:40</span>
    <span class="pais venezuela">Venezuela</span>
    </div>
    </div>
    </div>
    </li>
    '''
    patron  = '<li class="[^"]+"[^<]+<a href="([^"]+)"[^<]+<img width="\d+" height="\d+" src="([^"]+)".*?<h4>(.*?)</h4>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for scrapedurl, scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = scrapedthumbnail
        url = scrapedurl
        itemlist.append( Item(channel=__channel__, action="play", title=title, url=url, thumbnail=thumbnail,  folder=False))
    patron = '<li><a href="([^"]+)" class="next">&gt;</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        itemlist.append( Item(channel=__channel__, action="videos", title="Página Siguiente", url=matches[0], thumbnail="",  folder=True))     
    return itemlist

def play(item):
    logger.info("[tal.py] play")    
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    tcurl = "rtmpe://streaming.vzaar.com:1935/"

    itemlist = []
    
    #<param value="http://view.vzaar.com/605002.flashplayer" name="movie">
    patron = '<param value="([^"]+)" name="movie">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    if matches:
        swfurl = scrapertools.get_header_from_response(matches[0], "location")
        #logger.info("[tal.py] swfurl: " + swfurl)

    patron = '.*?guid=(.*?)\&.*?format=(.*?)\&'
    matches = re.compile(patron,re.DOTALL).findall(swfurl)
    if DEBUG: scrapertools.printMatches(matches)
    for guid, format in matches:
        if (format == 'mp4'):
            playpath = format + ":vzaar/" + guid[:3] + "/" + guid[3:6] + "/target/" + guid + "." + format
        else:
            playpath = "vzaar/" + guid[:3] + "/" + guid[3:6] + "/target/" + guid    
    #logger.info(playpath)
    scrapedurl = tcurl + " swfUrl=" + swfurl + " pageUrl=" + item.url + " playpath=" +  playpath + " swfVfy=true"      
    itemlist.append( Item(channel=__channel__, action="play",  server="directo",  title=item.title, url=scrapedurl, folder=False))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    # Todas las opciones tienen que tener algo
    categorias_items = mainlist(Item())

    # Lista de series
    if len(categorias_items)==0:
        print "No hay categorias"
        return False

    videos_items = videos(categorias_items[0])
    if len(videos_items)==0:
        print "La categoria "+categorias_items[0].title+" no tiene videos"
        return False

    mediaurl_items = play(videos_items[0])
    if len(mediaurl_items)==0:
        print "Error al averiguar la URL del primer episodio de "+series_items[0].title
        return False

    return True
