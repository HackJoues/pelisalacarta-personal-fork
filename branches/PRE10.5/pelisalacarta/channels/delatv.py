# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para delatv
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

CHANNELNAME = "delatv"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[delatv.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cinegratis.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , "Novedades" ,"http://delatv.com/","","")

	if xbmctools.getPluginSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

	
def novedades(params,url,category):
	xbmc.output("[delatv.py] novedades")

	# ------------------------------------------------------
	# Descarga la p�gina
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las pel�culas
	# ------------------------------------------------------
	#patron  = '<div class="thumb">[^<]+<a href="([^"]+)"><img src="([^"]+)".*?alt="([^"]+)"/></a>'
	patron  = '<div class="galleryitem">[^<]+'
	patron += '<h1>([^<]+)</h1>[^<]+'
	patron += '<a href="([^"]+)"><img src="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[0]
		scrapedurl = match[1]
		scrapedthumbnail = match[2].replace(" ","%20")
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la p�gina siguiente
	# ------------------------------------------------------
	#patron = '<a href="([^"]+)" >\&raquo\;</a>'
	patron  = 'class="current">[^<]+</span><a href="([^"]+)"'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "!Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapeddescription = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "novedades" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listmirrors(params,url,category):
	xbmc.output("[delatv.py] listmirrors")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la p�gina de detalle
	# http://delatv.com/sorority-row/
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	
	# Extrae el argumento
	patron = '<div class="sinopsis">.*?<li>(.*?)</li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0]

	# Extrae los enlaces a los v�deos (Megav�deo)
	#patronvideos  = '<tr>[^<]+'
	#patronvideos += '<td[^>]+><h2>([^<]+)</h2></td>[^<]+'
	#patronvideos += '<td[^>]+><a href="([^"]+)"><span class="flash"></span>'
	patron = '<a href="(http://delatv.com/flash/[^"]+)">(.*?)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)		

	for match in matches:
		etiquetaservidor = match[1].replace('<font color="white">','')
		etiquetaservidor = etiquetaservidor.replace('</font>','')
		etiquetaservidor = etiquetaservidor.replace('&Ntilde;','�')
		# A�ade al listado de XBMC
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Megavideo" , title + " (" + etiquetaservidor + ")" , match[0] , thumbnail , plot )

	# Extrae los enlaces a los v�deos (Directo)
	patron = '<a href="http://delatv.com/playlist/([^\/]+)/'
	#patron = '<a href="(http://delatv.com/playlist[^"]+)"><font color="white">([^<]+)</font></a>'
	#patronvideos  = '<tr>[^<]+'
	#patronvideos += '<td[^>]+><h2>([^<]+)</h2></td>[^<]+'
	#patronvideos += '<td[^>]+><a href="([^"]+)"><span class="flashflv"></span>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)>0:
		url = "http://www.delatv.com/xml/"+matches[0]+".xml"
		data = scrapertools.cachePage(url)
		#xbmc.output(data)
		#patron = '<media\:content url="([^"]+)"'
		patron  = '<track>[^<]+<creator>([^<]+)</creator>[^<]+<location>([^<]+)</location>'
		patron += '[^<]+(<meta rel="streamer">.*?</meta>.*?|)</track>'
		matches = re.compile(patron,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		
		for match in matches:
			titulo = title + " - " + match[0]
			if match[2] == "":
				url = match[1]
			else:
				url   = re.sub("<[^>]+>","",match[2])
				url   = url+"/"+match[1]
				url   = url.replace("\n","").replace(" ","")
				titulo = titulo + " [RTMPE]"
			print ' esta es la url: %s' %url
			# A�ade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , titulo + " [Directo]" , url , thumbnail , plot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[delatv.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]

	# Abre dialogo
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create( 'Accediendo al video...', title , plot )

	# Descarga la p�gina del reproductor
	xbmc.output("server="+server)
	if server=="Megavideo":
		# http://delatv.com/flash/UPY6KEB4/cleaner.html
		url = url.replace(" ","%20")
		xbmc.output("url="+url)
		data = scrapertools.cachePage(url)
		patron = '<iframe src="([^"]+)"'
		matches = re.compile(patron,re.DOTALL).findall(data)
		if len(matches)>0:
			url = matches[0]

		# Descarga el iframe con el embed
		# http://174.132.114.52/megaembed/UPY6KEB4/cleaner.html
		url = url.replace(" ","%20")
		xbmc.output("url="+url)
		data = scrapertools.cachePage(url)
		xbmc.output("data="+data)
		patron = '<embed src="http\:\/\/wwwstatic.megavideo.com/mv_player.swf\?v\=([^\&]+)&'
		matches = re.compile(patron,re.DOTALL).findall(data)
		if len(matches)>0:
			url = matches[0]

	xbmc.output("url="+url)

	# Cierra dialogo
	dialogWait.close()
	del dialogWait

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
