# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculas21 by Bandavi
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
import string

CHANNELNAME = "peliculas21"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[peliculas21.py] init")

DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )

def mainlist(params,url,category):
	xbmc.output("[peliculas21.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , "Pel�culas - Novedades"            ,"http://www.peliculas21.com","","")
	xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , "Pel�culas - Estrenos"             ,"http://www.peliculas21.com/estrenos/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , "Trailers - Pr�ximos Estrenos","http://www.peliculas21.com/trailers/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliscat"   , category , "Pel�culas - Lista por categor�as" ,"http://www.peliculas21.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "pelisalfa"  , category , "Peliculas - Lista alfab�tica"     ,"","","")
	xbmctools.addnewfolder( CHANNELNAME , "listaActoresMasBuscados" , category , "Actores - Lista Los M�s Buscados"     ,"http://www.peliculas21.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "buscaporletraActor" , category , "Actores - Busqueda Alfab�tica"  ,"http://www.peliculas21.com/?actdos=Smart","","")	
	xbmctools.addnewfolder( CHANNELNAME , "search"     , category , "Pel�culas - Buscar"                           ,"","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def pelisalfa(params, url, category):

	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "0-9","http://www.peliculas21.com/0-9/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "A","http://www.peliculas21.com/a/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "B","http://www.peliculas21.com/b/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "C","http://www.peliculas21.com/c/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "D","http://www.peliculas21.com/d/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "E","http://www.peliculas21.com/e/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "F","http://www.peliculas21.com/f/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "G","http://www.peliculas21.com/g/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "H","http://www.peliculas21.com/h/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "I","http://www.peliculas21.com/i/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "J","http://www.peliculas21.com/j/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "K","http://www.peliculas21.com/k/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "L","http://www.peliculas21.com/l/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "M","http://www.peliculas21.com/m/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "N","http://www.peliculas21.com/n/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "O","http://www.peliculas21.com/o/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "P","http://www.peliculas21.com/p/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "Q","http://www.peliculas21.com/q/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "R","http://www.peliculas21.com/r/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "S","http://www.peliculas21.com/s/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "T","http://www.peliculas21.com/t/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "U","http://www.peliculas21.com/u/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "V","http://www.peliculas21.com/v/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "W","http://www.peliculas21.com/w/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "X","http://www.peliculas21.com/x/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "Y","http://www.peliculas21.com/y/","","")
	xbmctools.addnewfolder( CHANNELNAME ,"listsimple", category , "Z","http://www.peliculas21.com/z/","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )



def search(params,url,category):
	xbmc.output("[peliculas21.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.peliculas21.com/?palabra="+tecleado
			listsimple(params,searchUrl,category)

def performsearch(texto):
	xbmc.output("[peliculas.py] performsearch")
	url = "http://www.peliculas21.com/?palabra="+texto
	url1 = "http://www.peliculas21.com"

	# Descarga la p�gina
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="fichafilm"><a href="([^"]+)"  target="_blank" ' # url
	patronvideos += 'class="titulo"><img src="([^"]+)"  '                        # Imagen
	patronvideos += 'width=[^>]+>([^<]+)</a>.*?<[^/]+/>.*?<div.*?>.*?'           # Titulo 
	patronvideos += '(<b>Doblaje:</b>[^<]+|<b>PROXIMAMENTE</b></span>-->)</div>' # Doblaje para Peliculas | Proximamente para trailers
	patronvideos += '(.*?)<b>(G&eacute;nero:</b>'                                # Duracion si hay
	patronvideos += '.*?)<div style=[^>]+>'                                      # Genero
	patronvideos += '<b>(Sinopsis:</b>.*?)<.*?'                                  # Sinopsis
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	resultados = []

	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		#scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
		#scrapedtitle = scrapedtitle.replace("</span>","")
		scrapedurl = urlparse.urljoin(url1,match[0])
		scrapedthumbnail = urlparse.urljoin(url1,match[1])
		scrapedthumbnail = scrapedthumbnail.replace(" ","")
		scrapedplot  = match[3].replace("\n"," ")+"\n"
		
		
		scrapedplot += match[4][4:].replace("\n","")+"\n"	
		
		scrapedplot += match[5].replace("\n"," ")+"\n"
		scrapedplot += match[6]
		scrapedplot  = re.sub("<[^>]+>","",scrapedplot)
		scrapedplot  = scrapedplot.replace("&eacute;","�")
		scrapedplot  = scrapedplot.replace("&oacute;","�")
		scrapedplot  = scrapedplot.replace("&ntilde;","�")

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		resultados.append( [CHANNELNAME , "listvideos" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
		
	return resultados

def peliscat(params,url,category):
	xbmc.output("[peliculas21.py] peliscat")
	
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	
	# Extrae los G�neros de las Peliculas
	patronvideos = '<div class="generos">(.*?)<br style="clear:both" />'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	patronvideos = '<a href="([^"]+)">([^<]+)</a>'
	matches1 = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	for match in matches1:
		url	= urlparse.urljoin(url,match[0])
		genero = match[1]
	
		xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , genero ,url,"","")

	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listsimple(params,url,category):
	xbmc.output("[peliculas21.py] listsimple")
	url1 = "http://www.peliculas21.com"
	# Descarga la p�gina
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="fichafilm"><a href="([^"]+)"  target="_blank" ' # url
	patronvideos += 'class="titulo"><img src="([^"]+)"  '                        # Imagen
	patronvideos += 'width=[^>]+>([^<]+)</a>.*?<[^/]+/>.*?<div.*?>.*?'           # Titulo 
	patronvideos += '(<b>Doblaje:</b>[^<]+|<b>PROXIMAMENTE</b></span>-->)</div>' # Doblaje para Peliculas | Proximamente para trailers
	patronvideos += '(.*?)<b>(G&eacute;nero:</b>'                                # Duracion si hay
	patronvideos += '.*?)<div style=[^>]+>'                                      # Genero
	patronvideos += '<b>(Sinopsis:</b>.*?)<.*?'                                  # Sinopsis
	#xbmc.output("[ listsimple  patronvideos")
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	#xbmc.output("[ listsimple  matches")
	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		#scrapedtitle = scrapedtitle.replace("<span class='style4'>","")
		#scrapedtitle = scrapedtitle.replace("</span>","")
		scrapedurl = urlparse.urljoin(url1,match[0])
		scrapedthumbnail = urlparse.urljoin(url1,match[1])
		scrapedthumbnail = scrapedthumbnail.replace(" ","")
		scrapedplot  = match[3].replace("\n"," ")+"\n"
		
		
		scrapedplot += match[4][4:].replace("\n","")+"\n"	
		
		scrapedplot += match[5].replace("\n"," ")+"\n"
		scrapedplot += match[6]
		scrapedplot  = re.sub("<[^>]+>","",scrapedplot)
		scrapedplot  = scrapedplot.replace("&eacute;","�")
		scrapedplot  = scrapedplot.replace("&oacute;","�")
		scrapedplot  = scrapedplot.replace("&ntilde;","�")
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
		#<div class="pagination" align="center" ><p><span  class='current'>1</span><a  href='/estrenos/2/'>2</a><a  href='/estrenos/2/'>Siguiente &raquo;</a><a  href='/estrenos/2/'></a>
	# Extrae la marca de siguiente p�gina
	if url == "http://www.peliculas21.com" or "http://www.peliculas21.com/nuevo" in url:
		patronvideos = '<div class="pagination" align="center" >.*?<div.*?<a href="([^"]+)">M�s peliculas</a></div>'
	else:
		patronvideos  = '<div class="pagination" align="center" >.*?<a  href=\'([^\']+)\'>Siguiente.*?<a  href=\'[^\']+\'>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = urlparse.urljoin(url1,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listvideos(params,url,category):
	xbmc.output("[peliculas21.py] listvideos")

	if url=="":
		url = "http://www.peliculas21.com"
	
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
	#title = urllib.unquote_plus(params.get("title"))
	#thumbnail = urllib.unquote_plus(params.get("thumbnail"))
	#plot = urllib.unquote_plus(params.get("plot"))
	
	# Busca el area donde estan los videos y la descripcion
	patronvideos = '<!--<br/>(.*?)<!-- FIN #content-->'
	matches      = re.compile(patronvideos,re.DOTALL).findall(data)
	
	# busca el titulo y el thumbnail
	patronvideos = '<img src="([^"]+)".*?>.*?<.*?>(.*?)</div>'
	matches2 =  re.compile(patronvideos,re.DOTALL).findall(matches[0])
	for match in matches2:
		title = match[1]
		thumbnail = urlparse.urljoin(url,match[0])
	plot = ""
	patronvideos = '<b>Duraci&oacute;n:</b>(.*?)<br />'
	duracion     = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	if len(duracion)>0:plot = "Duracion:"+duracion[0] + "\n"
		
	patronvideos = '<b>G&eacute;nero:</b>(.*?)<br />'
	genero       = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	if len(genero)>0:plot = plot + "Genero:  "+genero[0] +"\n"
	
	patronvideos = '<b>Sinopsis:</b>(.*?)</div>'
	sinopsis     = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	
	
	  
	# Busca los actores
	matchesactores = buscactores(matches[0]) 
	if len(matchesactores)>0:
		plot = plot + "Actores:   "
		c = 0
		actores = "ACTORES DE ESTA PELICULA :\n\n"
		for match in matchesactores:
			c =  c + 1
			actores = actores + "-"+match[1] + "\n"
			if   c == 3:
				plot = plot + match[1] + "\n"
			elif c == 4:
				plot = plot + "*              "  + match[1]+" "
			else:
				plot = plot + match[1]+ " , "
		
	plot = plot	+ "\nSinopsis: " + sinopsis[0]
	plot = re.sub("<[^>]+>"," ",plot)
	# Busca el trailer 
	patronvideos = '<param name="movie" value="([^"]+)"></param>'
	matchtrailer = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	if len(matchtrailer)>0:
		for match in matchtrailer:
		# A�ade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "youtubeplay" , category ,"Directo", "Ver El Trailer de : "+title , match , thumbnail, plot )
	else:
		import trailertools
		# A�ade al listado de XBMC
		xbmctools.addnewfolder( "trailertools" , "buscartrailer" , category , "Buscar trailer para : "+title , url , os.path.join(IMAGES_PATH, 'buscatrailers.png'), plot )
		
		
	matchesBK = matches[0]
	# Extrae las entradas (videos) para megavideo con tipo de audio
	patronvideos  = '<span  style="font-size:12px;"><strong>(.*?)</strong></span><br/>.*?'
	patronvideos += '<span.*?>.*?<a href="http\:\/\/www.megavideo.com\/[\?v=|v/]+([A-Z0-9]{8}).*?" target="_blank">1</a>.</span><br />'
	
	matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])
	scrapertools.printMatches(matches)
	encontrados = set()
	for match in matches:
		if match[1] not in encontrados:
			encontrados.add(match[1])
		
			# Titulo
			scrapedtitle = title + " -   [" +scrapertools.entityunescape(match[0])+ "]" + " (Megavideo)"
			# URL
			scrapedurl = match[1]
			# Thumbnail
			scrapedthumbnail = thumbnail
			# Argumento
			scrapedplot = plot

			# Depuracion
			if (DEBUG):
				xbmc.output("scrapedtitle="+scrapedtitle)
				xbmc.output("scrapedurl="+scrapedurl)
				xbmc.output("scrapedthumbnail="+scrapedthumbnail)

			# A�ade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "play" , category ,"Megavideo", scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae las entradas (videos) directos
	patronvideos = 'flashvars="file=([^\&]+)\&amp;controlbar=over'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	if len(matches)>0:
		
		data1 = scrapertools.cachePage(matches[0])
		#xbmc.output(data)
		patron = 'author">(.*?)</media:credit>.*?<media\:content url="([^"]+)"'
		matches = re.compile(patron,re.DOTALL).findall(data1)
		scrapertools.printMatches(matches)
		
		for match in matches:
			# A�ade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title +" -  ["+match[0]+"]"+ " (Directo)" , match[1] , thumbnail , plot )
			
	# Busca otras peliculas relacionadas con los actores
	if len(matchesactores)>0:
		titulo = "Busca otros Films de los actores de esta pelicula"
		xbmctools.addnewfolder( CHANNELNAME , "listaractores" , category , titulo , matchesBK , thumbnail, actores )
		
	# Lista peliculas relacionadas
	titulo = "Ver Peliculas Relacionadas" 
	matches = buscarelacionados(matchesBK)
	plot2 = "PELICULAS RELACIONADAS :\n\n"
	for match in matches:
		plot2 = plot2 + "-"+match[1]+"\n"
	xbmctools.addnewfolder( CHANNELNAME , "listarelacionados" , category , titulo , matchesBK , thumbnail, plot2 )
	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )




def play(params,url,category):
	xbmc.output("[peliculas21.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def youtubeplay(params,url,category):
        xbmc.output("[peliculas21.py] youtubeplay")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
        try:
	   plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
        except:
           plot = xbmc.getInfoLabel( "ListItem.Plot" )
        server = "Directo"
	youtubeurlcatch  = 'http://www.flashvideodownloader.org/download.php?u='+url
        data2 = scrapertools.cachePage(youtubeurlcatch)
        patronlinkdirecto = '<div class="mod_download"><a href="([^"]+)"'
        linkdirectoyoutube = re.compile(patronlinkdirecto,re.DOTALL).findall(data2)
        if len(linkdirectoyoutube)>0:
               xbmc.output(" link directos encontrados  "+str(len(linkdirectoyoutube)))
               if len(linkdirectoyoutube)>1:

                  # Abre el di�logo de selecci�n
                  opciones = []
	          opciones.append("FLV")
	          opciones.append("MP4")
               
	          dia = xbmcgui.Dialog()
	          seleccion = dia.select("tiene 2 formatos elige uno", opciones)
	          xbmc.output("seleccion=%d" % seleccion)        
                  if seleccion==-1:
	             return("")
	       
                  youtubeurl = linkdirectoyoutube[seleccion]
               else:
                  youtubeurl = linkdirectoyoutube[0]   
            
               xbmc.output("link directo de youtube : "+youtubeurl) 


               xbmctools.playvideo(CHANNELNAME,server,youtubeurl,category,title,thumbnail,plot)

def listaractores(params,data,category):
	xbmc.output("[peliculas21.py] listaractores")
	
	url1 = "http://www.peliculas21.com"
	actores = buscactores(data)
	opciones = []
	actorURL = []
	for i in actores:
		opciones.append(i[1])
		actorURL.append(urlparse.urljoin(url1,i[0]))           
	dia = xbmcgui.Dialog()
	seleccion = dia.select("Selecciona uno ", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1:return
	else:
		listsimple(params,actorURL[seleccion],category)
	return
	
def buscactores(data):
	patronvideos = ' <a href="([^"]+)">(.*?)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	return(matches)
	
def listarelacionados(params,data,category):
	xbmc.output("[peliculas21.py] listaractores")
	
	url1 = "http://www.peliculas21.com"
	#patronvideos = '<div><a href="([^"]+)">([^<]+)</a><br'
	matches = buscarelacionados(data) #re.compile(patronvideos,re.DOTALL).findall(data)
	
	opciones = []
	URL = []
	for i in matches:
		opciones.append(i[1])
		URL.append(urlparse.urljoin(url1,i[0]))           
	dia = xbmcgui.Dialog()
	seleccion = dia.select("Selecciona uno ", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1:return
	else:
		listvideos(params,URL[seleccion],category)
	return
	
def buscarelacionados(data):
	patronvideos = '<div><a href="([^"]+)">([^<]+)</a><br'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	return (matches)
	
def buscaporletraActor(params,url,category):
	xbmc.output("[peliculas21.py] buscaporletra")
	data = scrapertools.cachePage(url)
	patron  = '<div class="title">Listado de Actores</div><br/>(.*?)<div class="subtitulo">Abecedario</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	patron  = '<a href="(.*?)">(.*?)</a>'
	matches = re.compile(patron,re.DOTALL).findall(matches[0])
        
	letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
	opciones = []
	opciones.append("Buscar por palabras (Teclado)")
	#opciones.append("0-9")
	for letra in letras:
		opciones.append(letra)
	dia = xbmcgui.Dialog()
	seleccion = dia.select("busqueda rapida, elige uno : ", opciones)
	xbmc.output("seleccion=%d" % seleccion)
	if seleccion == -1 :return
	if seleccion == 0:
		keyboard = xbmc.Keyboard('')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			tecleado = keyboard.getText()
			if len(tecleado)>0:
				xbmc.output("Nuevo string tecleado   "+tecleado)
				for match in matches:
					if (string.lower(tecleado)) in (string.lower(match[1])):
						scrapedurl   = "http://www.peliculas21.com"+match[0]
						scrapedtitle = match[1]
						scrapedthumbnail = ""
						scrapedplot = " "
						if (DEBUG):
							xbmc.output("scrapedtitle="+scrapedtitle)
							xbmc.output("scrapedurl="+scrapedurl)
							xbmc.output("scrapedthumbnail="+scrapedthumbnail)
							#  A�ade al listado de XBMC
							xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
								
	else:
		for match in matches:
			if match[1][0:1] == letras[seleccion-1]:
				scrapedurl   = "http://www.peliculas21.com"+match[0]
				scrapedtitle = match[1]
				scrapedthumbnail = ""
				scrapedplot = " "
				if (DEBUG):
					xbmc.output("scrapedtitle="+scrapedtitle)
					xbmc.output("scrapedurl="+scrapedurl)
					xbmc.output("scrapedthumbnail="+scrapedthumbnail)
					#  A�ade al listado de XBMC
					xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )
				
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def listaActoresMasBuscados(params,url,category):
	xbmc.output("[peliculas21.py] listaActoresMasBuscados")
	
	url1 = "http://www.peliculas21.com"
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	patronvideos = 'Los m&aacute;s buscados:    <br />(.*?)<!--<div'
	matches1 = re.compile(patronvideos,re.DOTALL).findall(data)
	patronvideos = '<a href="([^"]+)">([^<]+)</a>'
	matches =  re.compile(patronvideos,re.DOTALL).findall(matches1[0])
	scrapertools.printMatches(matches)
	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		# URL
		scrapedurl = urlparse.urljoin(url1,match[0])
		# Thumbnail
		scrapedthumbnail = ""
        
		# Argumento
		scrapedplot = "Busca los Films existentes de este Actor � Actriz"

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listsimple" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
		
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
