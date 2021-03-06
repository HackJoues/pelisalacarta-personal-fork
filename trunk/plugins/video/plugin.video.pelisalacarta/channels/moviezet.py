# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para moviezet
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "moviezet"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[moviezet.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Películas"  , action="peliculas", url="http://www.moviezet.com/movies/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series"     , action="series",    url="http://www.moviezet.com/shows/?page_id=2853"))
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"   , action="search", url="http://www.moviezet.com/?s="))
    
    return itemlist

def peliculas(item):
    logger.info("[moviezet.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades"  , action="novedades", url="http://www.moviezet.com/movies/?cat=1&orderby=date&order=desc"))
    itemlist.append( Item(channel=CHANNELNAME, title="Mas Populares"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=CHANNELNAME, title="Mejores Peliculas"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value_num&order=desc&meta_key=views"))
    itemlist.append( Item(channel=CHANNELNAME, title="Generos"  , action="generos", url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=CHANNELNAME, title="Por A�o"  , action="novedades", url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_year"))
    itemlist.append( Item(channel=CHANNELNAME, title="Lista Completa"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=title&order=desc"))

    return itemlist

def generos(item):
    logger.info("[moviezet.py] generos")
    itemlist = []
     
    itemlist.append( Item(channel=CHANNELNAME, title="Accion"  , action="novedades", url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Acci%C3%B3n"))
    itemlist.append( Item(channel=CHANNELNAME, title="Animacion"  , action="novedades", url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value_num&order=asc&meta_key=views"))
    itemlist.append( Item(channel=CHANNELNAME, title="Aventura"  , action="novedades", url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Aventura"))
    itemlist.append( Item(channel=CHANNELNAME, title="Belica"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=B%C3%A9lica"))
    itemlist.append( Item(channel=CHANNELNAME, title="Ciencia Ficcion"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Ciencia%20Ficci%C3%B3n"))
    itemlist.append( Item(channel=CHANNELNAME, title="Comedia"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Comedia"))
    itemlist.append( Item(channel=CHANNELNAME, title="Comedia Romantica"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Comedia%20Rom%C3%A1ntica"))
    itemlist.append( Item(channel=CHANNELNAME, title="Crimen"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Crimen"))
    itemlist.append( Item(channel=CHANNELNAME, title="Documental"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Documental"))
    itemlist.append( Item(channel=CHANNELNAME, title="Drama"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Drama"))
    itemlist.append( Item(channel=CHANNELNAME, title="Fantasia"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Fantas%C3%ADa"))
    itemlist.append( Item(channel=CHANNELNAME, title="Musical"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Musical"))
    itemlist.append( Item(channel=CHANNELNAME, title="Romance"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Romance"))
    itemlist.append( Item(channel=CHANNELNAME, title="Suspense"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Suspenso"))
    itemlist.append( Item(channel=CHANNELNAME, title="Terror"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=asc&meta_key=movie_genre&meta_value=Terror"))
    itemlist.append( Item(channel=CHANNELNAME, title="Western"     , action="novedades",    url="http://www.moviezet.com/movies/?cat=1&orderby=meta_value&order=desc&meta_key=movie_genre&meta_value=Western"))
    
    return itemlist

def novedades(item):
    if (DEBUG): logger.info("[moviezet.py] novedades login")
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)
    # Extrae las entradas
    '''
    <td valign="top">

    <a href="http://www.moviezet.com/movies/attack-the-block/" title="Ver Attack The Block Online"><img src="http://www.moviezet.com/wp-content/uploads/attackblock.jpg" alt="Ver Attack The Block Online" /></a>
    '''
    patronvideos  = '<td valign="top">[^<]+<a href="(.*?)" title="(.*?)"[^<]<img src="(.*?)".*?</a>'    
    #patronvideos += "<td valign='top'><a href='([^']+)'>"
    #patronvideos += "<td valign='top'><div class='tit'><a[^>]+>([^<]+)</a></div>[^<]+"
    #patronvideos += "<div class='font11'>([^<]+)<"

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("Ver ","").replace("Online","")
        scrapedplot = match[0]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    #<div class="pagination"><a href="http://www.moviezet.com/movies/page/2/?cat=1&orderby=date&order=desc" class="next">
    patronvideos  = '<div class="pagination"><a href="(.*?)" class="next">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="PÃ¡gina siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def series(item):
    logger.info("[moviezet.py] series")
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    #<li><a href="#" title="$#*! My Dad Says">$#*! My Dad Says</a></li>

    patron  = '<li><a href="#" title="[^>]+>(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match
        scrapedplot = ""
        code = match[0]
        scrapedurl = "http://www.moviezet.com/shows/?page_id=2853&show="+match
        #scrapedurl = urllib.quote(scrapedurl)
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle , folder=True, extra=scrapedtitle) )

    return itemlist

def temporadas(item):
    logger.info("[moviezet.py] temporadas")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las entradas
    #li><a href="#" title="1">Temporada 1</a></li>

    patron  = '<li><a href="#" title="[^>]+>(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match
        temporada = scrapedtitle.replace("Temporada ","")
        scrapedtitle = match
        scrapedplot = ""
        scrapedurl = "http://www.moviezet.com/shows/?page_id=2853&show="+item.title+"&season="+temporada
        scrapedthumbnail = item.thumbnail
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], temporada=["+temporada+"] show="+item.show)

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=item.show , folder=True, extra=item.extra + "|" + temporada) )

    return itemlist

def episodios(item):
    logger.info("[moviezet.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las temporadas

    temporadas_itemlist = temporadas(item)
    
    for temporada_item in temporadas_itemlist:
        data = scrapertools.cache_page(temporada_item.url)

        # Extrae las entradas
        #<li><a href="#7685" title="1"><b>1.</b> Pilot</a></li>
        patron  = '<li><a href="(.*?)" title="(.*?)"><b>.*?</b>(.*?)</a></li>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for match in matches:
            code = match[0]
            episodio = match[1]
            if len(episodio)==1:
                episodio = "0" + episodio
            scrapedtitle = temporada_item.title + "x" + episodio + " "+match[2].strip()
            scrapedplot = ""
            scrapedurl = "http://www.moviezet.com/shows/?page_id=2853&show=dexter+&season=1&episode="+match[1]
            scrapedthumbnail = item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+item.show)
    
            itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.show , folder=True) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[moviezet.py] findvideos")

    # True es Serie, False es Pelicula
    serieOpelicula = True
    code =""
    if (item.url.startswith("http://www.moviezet.com/shows/")):
        data = scrapertools.cachePage(item.url)
        #<a class="watch-show" href="http://www.moviezet.com/shows/dexter-pilot/">
        patron = '<a class="watch-show" href="(.*?)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        url = matches[0]
        serieOpelicula = True
    else:
        # http://www.cuevana.tv/peliculas/2553/la-cienaga/
        logger.info("url1="+item.url)
        url = item.url
        serieOpelicula = False
    
    logger.info("url2="+url)
    data = scrapertools.cachePage(url)
    logger.info("data="+data)

    # <p id="videoi" style="display: none; text-align: center;">?megaus=http://www.megaupload.com/?d=H0LTL5XI&wup=&bit=&mubs=7686_ES.srt&langids=ES&videoid=7686&fulldir=http://www.moviezet.com/shows/dexter-crocodile/</p>

    patron = "&mubs=(.*?)&"
    matches = re.compile(patron,re.DOTALL).findall(data)
    code = matches[0]
    logger.info("code="+code)
    

    # Subtitulos
    if serieOpelicula:
        suburl = "http://www.moviezet.com/files/s/sub/"+code
    else:
        suburl = "http://www.moviezet.com/files/sub/"+code
    logger.info("suburl="+suburl)
    
    # Elimina el archivo subtitulo.srt de alguna reproduccion anterior
    ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
    if os.path.exists(ficherosubtitulo):
        try:
          os.remove(ficherosubtitulo)
        except IOError:
          logger.info("Error al eliminar el archivo subtitulo.srt "+ficherosubtitulo)
          raise

    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, subtitle=suburl, folder=False))

    return itemlist
  

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto):
    logger.info("[moviezet.py] search")
    
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.moviezet.com/?s=Search.."
    
        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url + texto
        
        

        # Devuelve los resultados
        return listar(item)
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def listar(item):
    logger.info("[moviezet.py] listar")
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    #<a href="http://www.moviezet.com/movies/terminator-salvation/" title="Ver Terminator: La Salvaci�n Online"><img src="http://moviezet.com/wp-content/uploads/30.jpg" alt="Ver Terminator: La Salvaci�n Online" /></a>
    patronvideos  = '<div class="movie-thumb">.*?<a href="(.*?)" title="(.*?)"[^<]<img src="(.*?)".*?</a>'


    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1].replace("Ver","").replace("Online","")
        scrapedplot = match[2]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="listar", title="Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def strm_detail(item):
    logger.info("[moviezet.py] strm_detail")
    from core import xbmctools
    import xbmc
    
    code =""
    if (item.url.startswith("http://www.cuevana.tv/list_search_info.php")):
        data = scrapertools.cachePage(item.url)
        patron = "window.location\='/series/([0-9]+)/"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        url = "http://www.cuevana.tv/player/source?id=%s&subs=,ES&onstart=yes&tipo=s&sub_pre=ES" % matches[0]
        serieOpelicula = True
    else:
        logger.info("url1="+item.url)
        patron = "http://www.cuevana.tv/peliculas/([0-9]+)/"
        matches = re.compile(patron,re.DOTALL).findall(item.url)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        url = "http://www.cuevana.tv/player/source?id=%s&subs=,ES&onstart=yes&sub_pre=ES#" % code
        serieOpelicula = False
    
    logger.info("url2="+url)
    data = scrapertools.cachePage(url)

    # goSource('ee5533f50eab1ef355661eef3b9b90ec','megaupload')
    patron = "goSource\('([^']+)','megaupload'\)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = scrapertools.cachePagePost("http://www.cuevana.tv/player/source_get","key=%s&host=megaupload&vars=&id=2933&subs=,ES&tipo=&amp;sub_pre=ES" % matches[0])
    logger.info("data="+data)

    # Subtitulos
    if serieOpelicula:
        suburl = "http://www.cuevana.tv/files/s/sub/"+code+"_ES.srt"
    else:
        suburl = "http://www.cuevana.tv/files/sub/"+code+"_ES.srt"
    logger.info("suburl="+suburl)
    
    # Elimina el archivo subtitulo.srt de alguna reproduccion anterior
    ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
    if os.path.exists(ficherosubtitulo):
        try:
          os.remove(ficherosubtitulo)
        except IOError:
          logger.info("Error al eliminar el archivo subtitulo.srt "+ficherosubtitulo)
          raise

    from core import downloadtools
    downloadtools.downloadfile(suburl, ficherosubtitulo )
    config.set_setting("subtitulo","true")

    listavideos = servertools.findvideos(data)
    
    for video in listavideos:
        server = video[2]
        if server == "Megaupload":
            scrapedtitle = item.title + " [" + server + "]"
            scrapedurl = video[1]
            thumbnail = urllib.unquote_plus( item.thumbnail )
            plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
            xbmctools.playvideo(CHANNELNAME,server,scrapedurl,"Series",scrapedtitle,item.thumbnail,item.plot,strmfile=True,subtitle=suburl)
            exit
    logger.info("[moviezet.py] strm_detail fin")
    return

def addlist2Library(item):
    logger.info("[moviezet.py] addlist2Library")

    from core import library
    import xbmcgui
    itemlist = []
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    extra = item.extra.split("|")

    # Extrae las entradas (carpetas)
    patronvideos  = '<li onclick=\'listSeries\(3,"([^"]+)"\)\'><span class=\'nume\'>([^<]+)</span>([^<]+)</li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('pelisalacarta', 'Añadiendo episodios...')
    pDialog.update(0, 'Añadiendo episodio...')
    totalepisodes = len(matches)
    logger.info ("[cuevana.py - addlist2Library] Total Episodios:"+str(totalepisodes))
    i = 0
    errores = 0
    nuevos = 0
    for match in matches:
        scrapedtitle = "S"+extra[1]+"E"+match[1]+" "+match[2].strip()
        Serie = extra[0]
        server = "Megaupload"
        i = i + 1
        pDialog.update(i*100/totalepisodes, 'Añadiendo episodio...',scrapedtitle)
        if (pDialog.iscanceled()):
            return
        url = "http://www.cuevana.tv/list_search_info.php?episodio="+match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
            logger.info("url="+url) #OPCION 2.
            logger.info("scrapedthumbnail="+scrapedthumbnail)
            logger.info("Episodio "+str(i)+" de "+str(totalepisodes)+"("+str(i*100/totalepisodes)+"%)")
        try:
            nuevos = nuevos + library.savelibrary(scrapedtitle,url,scrapedthumbnail,server,scrapedplot,canal=CHANNELNAME,category="Series",Serie=Serie,verbose=False,accion="strm_detail",pedirnombre=False)
        except IOError:
            logger.info("Error al grabar el archivo "+scrapedtitle)
            errores = errores + 1
    if errores > 0:
        logger.info ("[cuevana.py - addlist2Library] No se pudo añadir "+str(errores)+" episodios")

    library.update(totalepisodes,errores,nuevos)
