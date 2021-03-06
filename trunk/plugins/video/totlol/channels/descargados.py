# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Lista de v�deos descargados
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

CHANNELNAME = "descargados"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[descargados.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[descargados.py] mainlist")

	downloadpath = xbmcplugin.getSetting("downloadpath")
	xbmc.output("[descargados.py] downloadpath="+downloadpath)
	
	# A�ade al listado de XBMC
	ficheros = os.listdir(downloadpath)
	for fichero in ficheros:
		url = os.path.join( downloadpath , fichero )
		listitem = xbmcgui.ListItem( fichero, iconImage="DefaultVideo.png" )
		xbmcplugin.addDirectoryItem( handle = pluginhandle, url = url, listitem=listitem, isFolder=False)
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
