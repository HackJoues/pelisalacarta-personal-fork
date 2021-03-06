# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cine-adicto.com by Bandavi
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
import vk
import buscador

CHANNELNAME = "cineadicto"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[cineadicto.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[cineadicto.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos"       , category , "Ultimas Pel�culas A�adidas"    ,"http://www.cine-adicto.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListaCat"         , category , "Listado por Genero"    ,"http://www.cine-adicto.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListaAlfa"         , category , "Listado Alfanumerico"    ,"http://www.cine-adicto.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Estrenos","http://www.cine-adicto.com/category/categorias/estrenos","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Documentales","http://www.cine-adicto.com/category/categorias/documentales/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Peliculas en HD","http://www.cine-adicto.com/category/categorias/peliculas-hd-categorias","","")
	xbmctools.addnewfolder( CHANNELNAME , "search" , category , "Buscar","http://www.cine-adicto.com/","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	logger.info("[cineadicto.py] search")

	buscador.listar_busquedas(params,url,category)

def searchresults(params,url,category):
	logger.info("[cineadicto.py] searchresults")

	buscador.salvar_busquedas(params,url,category)

	#convert to HTML
	tecleado = url.replace(" ", "+")
	searchUrl = "http://www.cine-adicto.com/?s="+tecleado
	searchresults2(params,searchUrl,category)

def searchresults2(params,url,category):
	logger.info("[cineadicto.py] SearchResult")
	
	
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#print data
	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="poster">[^<]+<a href="([^"]+)"'                          # URL
	patronvideos += '><img src="([^"]+)" width=[^\/]+\/>'                                 # TUMBNAIL
	patronvideos += '</a>[^<]+<[^>]+>[^<]+<[^>]+>[^<]+<a href="[^"]+">([^<]+)</a>'        # TITULO 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedurl = match[0]
		
		scrapedtitle =match[2]
		scrapedtitle = scrapedtitle.replace("&#8211;","-")
		scrapedtitle = scrapedtitle.replace("&nbsp;"," ")
		scrapedthumbnail = match[1]
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
			

def ListaCat(params,url,category):
	logger.info("[cineadicto.py] ListaCat")
	
	
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Acci�n","http://www.cine-adicto.com/category/categorias/accion/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Animado","http://www.cine-adicto.com/category/categorias/animado/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Anime","http://www.cine-adicto.com/category/categorias/anime/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Asi�ticas","http://www.cine-adicto.com/category/categorias/asiaticas/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Aventuras","http://www.cine-adicto.com/category/categorias/aventura/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Ciencia-Ficci�n","http://www.cine-adicto.com/category/categorias/ciencia-ficcion/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Cl�sicos","http://www.cine-adicto.com/category/categorias/clasicos/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Comedia","http://www.cine-adicto.com/category/categorias/comedia/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Comedias Romanticas","http://www.cine-adicto.com/category/categorias/comedias-romanticas/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Destacado","http://www.cine-adicto.com/category/categorias/destacado/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Documentales","http://www.cine-adicto.com/category/categorias/documentales/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Drama","http://www.cine-adicto.com/category/categorias/drama/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Espa�ol Latino","http://www.cine-adicto.com/category/categorias/espanol-latino/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Estreno","http://www.cine-adicto.com/category/categorias/estreno/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Infantil","http://www.cine-adicto.com/category/categorias/infantil/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Intriga","http://www.cine-adicto.com/category/categorias/intriga/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Musicales","http://www.cine-adicto.com/category/categorias/musicales/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Peliculas HD","http://www.cine-adicto.com/category/categorias/peliculas-hd-categorias/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Romance","http://www.cine-adicto.com/category/categorias/romance/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideosMirror", category , "Suspenso","http://www.cine-adicto.com/category/categorias/suspenso/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Terror","http://www.cine-adicto.com/category/categorias/terror/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Thriller","http://www.cine-adicto.com/category/categorias/thriller/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"ListvideosMirror", category , "Western","http://www.cine-adicto.com/category/categorias/western/","","")
	
	# Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def ListaAlfa(params, url, category):

	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "0-9","http://www.cine-adicto.com/tag/9/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "A","http://www.cine-adicto.com/tag/a/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "B","http://www.cine-adicto.com/tag/b/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "C","http://www.cine-adicto.com/tag/c/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "D","http://www.cine-adicto.com/tag/d/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "E","http://www.cine-adicto.com/tag/e/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "F","http://www.cine-adicto.com/tag/f/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "G","http://www.cine-adicto.com/tag/g/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "H","http://www.cine-adicto.com/tag/h/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "I","http://www.cine-adicto.com/tag/i/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "J","http://www.cine-adicto.com/tag/j/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "K","http://www.cine-adicto.com/tag/k/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "L","http://www.cine-adicto.com/tag/l/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "M","http://www.cine-adicto.com/tag/m/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "N","http://www.cine-adicto.com/tag/n/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "O","http://www.cine-adicto.com/tag/o/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "P","http://www.cine-adicto.com/tag/p/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Q","http://www.cine-adicto.com/tag/q/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "R","http://www.cine-adicto.com/tag/r/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "S","http://www.cine-adicto.com/tag/s/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "T","http://www.cine-adicto.com/tag/t/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "U","http://www.cine-adicto.com/tag/u/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "V","http://www.cine-adicto.com/tag/v/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "W","http://www.cine-adicto.com/tag/w/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "X","http://www.cine-adicto.com/tag/x/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Y","http://www.cine-adicto.com/tag/y/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listvideos", category , "Z","http://www.cine-adicto.com/tag/z/","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )



        
def ListvideosMirror(params,url,category):
	logger.info("[cineadicto.py] ListvideosMirror")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)


	# Patron de las entradas
	patronvideos  = '<div class="poster">[^<]+<a href="([^"]+)"'                          # URL
	patronvideos += '><img src="([^"]+)" width=[^\/]+\/>'                                # TUMBNAIL
	patronvideos += '</a>[^<]+<[^>]+>[^<]+<[^>]+>[^<]+<a href="[^"]+">([^<]+)</a>'        # TITULO 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# A�ade las entradas encontradas
	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		scrapedurl = match[0]
		scrapedthumbnail = match[1]
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	#Extrae la marca de siguiente p�gina
	patronvideos  = '</span><a href="(http://www.cine-adicto.com/.*?page/[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = matches[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "ListvideosMirror" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        

def listvideos(params,url,category):
	logger.info("[cineadicto.py] listvideos")

	if url=="":
		url = "http://www.cine-adicto.com/"
                
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	#<div class="feature-image">
	#<a href="http://www.cine-adicto.com/the-last-airbender.html" title="The Last Airbender"><img src="http://www.cine-adicto.com/wp-content/uploads/2010/07/airbenderposter.jpg" title="The Last Airbender" alt="The Last Airbender" width="12

	# Extrae las entradas (carpetas)
	patronvideos  =  '<div class="feature-image">[^<]+<a href="([^"]+)"'     # URL
	patronvideos +=  ' title="([^"]+)"'                       	             # TITULO
	patronvideos +=  '><img src="([^"]+)" '                                  # TUMBNAIL
	patronvideos += '.*?<p><p>(.+?)</p>'                                     # DESCRIPCION
	#patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  
	#patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		
		scrapedtitle = match[1]
		# URL
		scrapedurl = match[0]
		# Thumbnail
		scrapedthumbnail = match[2]
		# Argumento
		scrapedplot = match[3]
		

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		
			# A�ade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	#Extrae la marca de siguiente p�gina
	patronvideos  = "<span class='current'>[^<]+</span><a href='([^']+)'" #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])#matches[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category,cLose="true"):
	logger.info("[cineadicto.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	scrapedurl = ""
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
	patronvideos = 'name="Pelicula" src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		data = scrapertools.cachePage(matches[0])
    # Extrae el argumento
	patronarg = '</p><p>.*?<strong>([^<]+</strong> <strong>.*?)<p></p>'
	matches   = re.compile(patronarg,re.DOTALL).findall(data)
	if len(matches)>0:
		plot  = re.sub("<[^>]+>"," ",matches[0])
  
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos en los servidores habilitados
	# ------------------------------------------------------------------------------------

   
			
	## --------------------------------------------------------------------------------------##
	#               Busca enlaces a videos .flv o (.mp4 dentro de un xml)                     #
	## --------------------------------------------------------------------------------------##
	patronvideos = 'file=(http\:\/\/[^\&]+)\&'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	playWithSubt = "play"
	c = 0
	if len(matches)>0:
		for match in matches:
			subtitle = "[FLV-Directo]"
			c += 1
			if ("playlist" in match):
				data2 = scrapertools.cachePage(match)
				logger.info("data2="+data2)
				patronvideos  = '<track>.*?'
				patronvideos += '<title>([^<]+)</title>[^<]+'
				patronvideos += '<location>([^<]+)</location>(?:[^<]+'
				patronvideos += '<meta rel="type">video</meta>[^<]+|[^<]+'
				patronvideos += '<meta rel="captions">([^<]+)</meta>[^<]+)'
				patronvideos += '</track>'
				matches2 = re.compile(patronvideos,re.DOTALL).findall(data2)
				scrapertools.printMatches(matches)
				
				for match2 in matches2:
					sub = ""
					if match2[2].endswith(".xml"): # Subtitulos con formato xml son incompatibles con XBMC
						sub = "[Subtitulo incompatible con xbmc]"
						playWithSubt = "play"
					if ".mp4" in match2[1]:
						subtitle = "[MP4-Directo]"
					scrapedtitle = '%s (castellano) - %s  %s' %(title,match2[0],subtitle)
					
					scrapedurl = match2[1].strip()
					scrapedthumbnail = thumbnail
					scrapedplot = plot
					if ("cast.xml" or "mirror.xml") not in match:
						scrapedtitle = '%s (V.O.S) - %s  %s %s' %(title,match2[0],subtitle,sub)
						if not match2[2].endswith("cine-adicto2.srt") and (sub == ""): 
							scrapedurl = scrapedurl + "|" + match2[2]
							playWithSubt = "play2"
							
					if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
							
					# A�ade al listado de XBMC
					xbmctools.addnewvideo( CHANNELNAME , playWithSubt , category , "Directo" , scrapedtitle, scrapedurl , scrapedthumbnail, scrapedplot )
				
			else:
				c +=1
				scrapedurl = match
				if match.endswith(".srt") and not (((c / 2) * 2 - c) == 0) :
					scrapedurl = scrapedurl + "|" + match 
					xbmctools.addnewvideo( CHANNELNAME ,"play2"  , category , "Directo" , title + " (V.O.S) - "+subtitle, scrapedurl , thumbnail , plot )
				elif 	match.endswith(".xml") and not (((c / 2) * 2 - c) == 0):
					sub = "[Subtitulo incompatible con xbmc]"
					xbmctools.addnewvideo( CHANNELNAME ,"play"  , category , "Directo" , title + " (V.O) - %s %s" %(subtitle,sub), scrapedurl , thumbnail , plot )
				elif not match.endswith("srt" or "xml") :
					xbmctools.addnewvideo( CHANNELNAME ,"play"  , category , "Directo" , title + " - [Directo]" , scrapedurl , thumbnail , plot )
				
				print scrapedurl
	
	try:
		matches = url.split("/")
		url2 = "http://www.cine-adicto.com/tab/"+matches[3]
		data2 = scrapertools.cachePage(url2)
	
		
		listavideos = servertools.findvideos(data2)
		c = 0
		for video in listavideos:
			if "stagevu.com/embed" not in video[1]:
				videotitle = video[0]
				url = video[1]
				server = video[2]
				if "facebook" in url:
					c += 1
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - Parte %d %s" %(c,videotitle) , url , thumbnail , plot )
				else:
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	except:
		pass


	## --------------------------------------------------------------------------------------##
	#            Busca enlaces de videos para el servidor vk.com                             #
	## --------------------------------------------------------------------------------------##
	'''
	var video_host = '447.gt3.vkadre.ru';
	var video_uid = '0';
	var video_vtag = '2638f17ddd39-';
	var video_no_flv = 0;
	var video_max_hd = '0';
	var video_title = 'newCine.NET+-+neWG.Es+%7C+Chicken+Little';

	'''
	patronvideos = '<iframe src="(http://[^\/]+\/video_ext.php[^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		print " encontro VK.COM :%s" %matches[0]
 		videourl = 	vk.geturl(matches[0])
 		xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+"[VK]", videourl , thumbnail , plot )
 		
	'''
	patronvideos = 'name="Pelicula" src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if cLose == "false":return
	if len(matches)>0:
		for match in matches:
			detail(params,match,category,"false")
	'''
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )



def play(params,url,category):
	logger.info("[cineadicto.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def play2(params,url,category):
	logger.info("[cineadicto.py] play2")
	url1 = url
	if "|" in url:
		urlsplited = url.split("|")
		url1 = urlsplited[0]
		urlsubtit = urlsplited[1]
		subt_ok = "0"
		while subt_ok == "0":
			subt_ok = downloadstr(urlsubtit)
			print "subtitulo subt_ok = %s" % str(subt_ok)
			if subt_ok is None: # si es None la descarga del subtitulo esta ok
				config.setSetting("subtitulo", "true")
				break
	play(params,url1,category)


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
        
        
def downloadstr(urlsub):
	
	import downloadtools
	
	fullpath = os.path.join( config.DATA_PATH, 'subtitulo.srt' )
	if os.path.exists(fullpath):
		try:
			subtitfile = open(fullpath,"w")
			subtitfile.close()
		except IOError:
			logger.info("Error al limpiar el archivo subtitulo.srt "+fullpath)
			raise
	try:		
		ok = downloadtools.downloadfile(urlsub,fullpath)
	except IOError:
		logger.info("Error al descargar el subtitulo "+urlsub)
		return -1
	return ok

def getpost(url,values): # Descarga la pagina con envio de un Form
	
	#url=url
	try:
		data = urllib.urlencode(values)          
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		the_page = response.read() 
		return the_page 
	except Exception: 
		return "Err " 	
