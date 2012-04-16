# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tubutakadecine
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tubutakadecine"
__category__ = "F"
__type__ = "generic"
__title__ = "Tu butaka de cine"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tubutakadecine.py] mainlist")

    item.url = "http://www.tubutakadecine.com/"
    return novedades(item)

def novedades(item):
    logger.info("[peliculasflv.py] listado")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae los posts individuales
    patron = "(<div class='post-body.*?)<div class='post-footer'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    # Para cada post, saca los metadatos y añade el item
    for post in matches:
        #<span class="Apple-style-span" style="font-size: large;">CONAN EL BARBARO (2011)</span></b><br />
        try:
            #<span class="Apple-style-span" style="font-size: x-large;"><b>IRA DE TITANES</b></span><br />
            scrapedtitle = scrapertools.get_match(post,'<span class="Apple-style-span" style="font-size: x-large;">(.*?)</span>')
            scrapedtitle = scrapertools.htmlclean(scrapedtitle).strip()
            scrapedthumbnail = scrapertools.get_match(post,'<img border="0" height="[^"]+" src="([^"]+)"')
            scrapedplot = scrapertools.htmlclean(post).strip()
            scrapedplot = re.compile("\s*Ver trailer\s*",re.DOTALL).sub(" ",scrapedplot)

            scrapedurl = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = post , folder=True) )
        except:
            scrapedtitle = "(no identificado)"
            scrapedthumbnail = ""
            scrapedplot = ""
            scrapedurl = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra = post , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a class='blog-pager-older-link' href='([^']+)' id='Blog1_blog-pager-older-link' title='Entradas antiguas'>Entradas antiguas</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="novedades", title="Página siguiente >>" , url=scrapedurl , folder=True) )

    return itemlist

def findvideos(item):
    itemlist = servertools.find_video_items(data=item.extra)
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
    
    return itemlist