# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools
import config
import logger

CHANNELNAME = "peliculasid"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[peliculasid.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[peliculasid.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ultimas Pel�culas Subidas"    ,"http://www.peliculasid.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Estrenos","http://www.peliculasid.net/index.php?module=estrenos","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Series","http://www.peliculasid.net/index.php?module=series","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategorias" , category , "Categorias"        ,"http://www.peliculasid.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Buscar","http://www.peliculasid.net/index.php?module=documentales","","")

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listcategorias(params,url,category):
        logger.info("[peliculas.py] listcategorias")

        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Acci�n"    ,"http://www.peliculasid.com/accion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Animaci�n"    ,"http://www.peliculasid.com/animacion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Aventura"    ,"http://www.peliculasid.com/aventura-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ciencia Ficci�n"    ,"http://www.peliculasid.com/ciencia_ficcion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Cine Indio"    ,"http://www.peliculasid.com/cine_indio-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Comedia"    ,"http://www.peliculasid.com/comedia-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Crimen"    ,"http://www.peliculasid.com/crimen-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Documentales y mas"    ,"http://www.peliculasid.com/documentales-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Drama"    ,"http://www.peliculasid.com/drama-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Fantasia"    ,"http://www.peliculasid.com/fantasia-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Horror"    ,"http://www.peliculasid.com/horror-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Misterio"    ,"http://www.peliculasid.com/misterio-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Romance"    ,"http://www.peliculasid.com/romance-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Thriller"    ,"http://www.peliculasid.com/thriller-1.html","","")
        
        # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
        

def listvideos(params,url,category):
	logger.info("[peliculasid.py] listvideos")

	if url=="":
		url = "http://www.peliculasid.com/"
                
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="item">[^<]+<h1>([^<]+)</h1>[^<]+'
	patronvideos += '<a href="([^"]+)"><img src="([^"]+)"'
	#patronvideos += '<div class="cover boxcaption">.*?<h6>([^<]+)</h6>'

	#patronvideos += "<img src='(.*?)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[0]
		# URL
		scrapedurl = match[1]
		# Thumbnail
		scrapedthumbnail = match[2]
		scrapedthumbnail = scrapedthumbnail.replace(" ","")
		# Argumento
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente p�gina
	
	patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	logger.info("[peliculasid.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
        patrondescrip = '<strong>Sinopsis:</strong><br />(.*?)</p>'
        matches = re.compile(patrondescrip,re.DOTALL).findall(data)
        if DEBUG:
          if len(matches)>0:
		descripcion = matches[0]
                descripcion = descripcion.replace('&#8220;','"')
                descripcion = descripcion.replace('&#8221;','"')

                descripcion = descripcion.replace('&#8230;','...')
                descripcion = descripcion.replace('&#8217;',"'")
                descripcion = descripcion.replace("&nbsp;","")
		descripcion = descripcion.replace("<br/>","")
		descripcion = descripcion.replace("\r","")
		descripcion = descripcion.replace("\n"," ")
                descripcion = descripcion.replace("\t"," ")
		descripcion = re.sub("<[^>]+>"," ",descripcion)
#                logger.info("descripcion="+descripcion)
                descripcion = acentos(descripcion)
#                logger.info("descripcion="+descripcion)
                try :
                    plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
                except:
                    plot = descripcion

        #--- Busca los videos Directos
        patronvideos = 'flashvars" value="file=([^\&]+)\&amp'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        if len(matches)>0:
          if ("xml" in matches[0]):  
            #data = scrapertools.cachePage(matches[0])
            req = urllib2.Request(matches[0])
            try:
		response = urllib2.urlopen(req)
	    except:
                xbmctools.alertnodisponible()
                return
            data=response.read()
	    response.close()
            #logger.info("archivo xml :"+data)
            newpatron = '<title>([^<]+)</title>[^<]+<location>([^<]+)</location>'
            newmatches = re.compile(newpatron,re.DOTALL).findall(data)
            
            for match in newmatches:
              logger.info(" videos = "+match[1])
              if match[1].startswith("vid"):
				subtitle = match[0] + " (rtmpe) no funciona en xbmc"
              else:
				subtitle = match[0]
				
              xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, match[1] , thumbnail , plot )
                 
          else:
                logger.info(" matches = "+matches[0])
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title, matches[0] , thumbnail , plot )


	# Ahora usa servertools
	listavideos = servertools.findvideos(data)

	j=1
	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , (title.strip() + " (%d) " + videotitle) % j , url , thumbnail , plot )
		j=j+1

	# Carga los iframes
	#<a href="http://peliculasid.com/iframeplayer.php?url=aHR0cDovL3ZpZGVvLmFrLmZhY2Vib29rLmNvbS9jZnMtYWstc25jNC80MjIxNi82MS8xMjgxMTI4ODgxOTUwXzM5NTAwLm1wNA==" target="repro">Parte 1</a>
        patronvideos = '<a href="(http...peliculasid.com.iframeplayer[^"]+)"[^>]+>([^<]+)</a>'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = thumbnail
		scrapedplot = plot

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "iframes" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def iframes(params,url,category):
	logger.info("[peliculasid.py] iframes")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
	listavideos = servertools.findvideos(data)
	j=1
	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , (title.strip() + " (%d) " + videotitle) % j , url , thumbnail , plot )
		j=j+1

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[peliculasid.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def acentos(title):

        title = title.replace("Â�", "")
        title = title.replace("Ã©","�")
        title = title.replace("Ã¡","�")
        title = title.replace("Ã³","�")
        title = title.replace("Ãº","�")
        title = title.replace("Ã­","�")
        title = title.replace("Ã±","�")
        title = title.replace("â€", "")
        title = title.replace("â€œÂ�", "")
        title = title.replace("â€œ","")
        title = title.replace("é","�")
        title = title.replace("á","�")
        title = title.replace("ó","�")
        title = title.replace("ú","�")
        title = title.replace("í","�")
        title = title.replace("ñ","�")
        title = title.replace("Ã“","�")
        return(title)
