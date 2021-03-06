# -*- coding: utf-8 -*-

from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

import re,urlparse

from core.item import Item
cerealizer.register(Item)

#----------------------------------------------------------------------------------------------------------------
VIDEO_PREFIX = "/video/pelisalacarta"
NAME = L('Title')
ART           = 'art-default.jpg'
ICON          = 'icon-default.png'
#----------------------------------------------------------------------------------------------------------------

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, mainlist, L('VideoTitle'), ICON, ART)    
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("MediaPreview", viewMode="MediaPreview", mediaType="items")
    Plugin.AddViewGroup("Showcase", viewMode="Showcase", mediaType="items")
    #Plugin.AddViewGroup("CoverFlow", viewMode="CoverFlow", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
    Plugin.AddViewGroup("WallStream", viewMode="WallStream", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def mainlist():
    Log("[__init__.py] channelselector")

    from core import config
    
    dir = MediaContainer(viewGroup="InfoList")

    import channelselector
    canales = channelselector.getmainlist()

    Log(canales)

    for canal in canales:
        if canal.channel=="configuracion":
            dir.Append(PrefsItem(title="Configuración", thumb='http://pelisalacarta.mimediacenter.info/posters/'+canal.channel+'.png'))
        elif canal.channel=="buscador":
            dir.Append( Function( InputDirectoryItem( do_search, canal.title, "subtitle", "txt", thumb = 'http://pelisalacarta.mimediacenter.info/posters/'+canal.channel+'.png', art=R(ART) ) , itemtext = canal.serialize() ) )
        else:
            if canal.channel!="trailertools" and canal.channel!="descargas" and canal.channel!="favoritos":
                dir.Append( Function( DirectoryItem( runchannel, title = canal.title, subtitle = "", thumb = 'http://pelisalacarta.mimediacenter.info/posters/'+canal.channel+'.png', art=R(ART) ) , channel=canal.channel , action = canal.action ))

    return dir

def runchannel(sender,channel,action="mainlist",category=""):
    Log("[__init__.py] runchannel")
    '''
    from PMS import Prefs
    valor = Prefs.Get("megavideouser")
    Log("login="+valor)
    from core import config
    valor = config.get_setting("megavideouser")
    Log("login="+valor)
    Log("get_data_path="+config.get_data_path())
    '''
    Log("channel="+channel)
    Log("action="+action)

    dir = MediaContainer(viewGroup="InfoList")
    
    # Importa el canal y obtiene los items
    try:
        exec "from pelisalacarta.channels import "+channel
    except:
        try:
            exec "from core import "+channel
        except:
            exec "import "+channel
        
    if channel!="channelselector":
        exec "itemlist = "+channel+"."+action+"(None)"
    elif action=="channeltypes":
        itemlist = channelselector.getchanneltypes()
    elif action=="listchannels":
        itemlist = channelselector.filterchannels(category)

    Log("itemlist %d items" % len(itemlist))

    for item in itemlist:    
        Log("item="+item.tostring()+" channel=["+item.channel+"]")

        category=""
        if "F" in item.category:
            category = category + "Películas, "
        if "S" in item.category:
            category = category + "Series, "
        if "D" in item.category:
            category = category + "Documentales, "
        if "A" in item.category:
            category = category + "Anime, "
        if "M" in item.category:
            category = category + "Música, "
        if "G" in item.category:
            category = category + "Servidores, "
        if "NEW" in item.category:
            category = "Los nuevos, "
        
        if category!="":
            category = category[:-2]
        
        if not item.thumbnail.startswith("http://"):
            item.thumbnail = 'http://pelisalacarta.mimediacenter.info/posters/'+item.channel+'.png'
        #Log("category=%s" % category)

        #thumbnail = 'images/posters/'+item.channel+'.png'
        #Log("thumbnail=%s" % thumbnail)

        # Opciones de menú
        if item.channel=="channelselector":
            dir.Append( Function( DirectoryItem( runchannel, title = item.title, subtitle = "", thumb = item.thumbnail, art=R(ART) ) , channel=item.channel , action = item.action , category = item.category ))
        # Los canales
        else:
            if item.type=="generic":
                dir.Append( Function( DirectoryItem( actionexecute, title = item.title, subtitle = category, thumb = item.thumbnail ) , itemtext = item.serialize() ) )

    return dir

def actionexecute(sender,itemtext):
    Log("[__init__.py] actionexecute")
    item = Item()
    item.deserialize(itemtext)

    Log("[__init__.py] "+item.tostring())
    dir = MediaContainer(viewGroup="InfoList")
    
    if item.action=="":
        item.action="mainlist"
    Log("[__init__.py] action="+item.action)
    
    exec "from pelisalacarta.channels import "+item.channel

    if item.action=="findvideos":
        try:
            exec "itemlist = "+item.channel+"."+item.action+"(item)"
        except:
            itemlist = findvideos(item)
    else:
        exec "itemlist = "+item.channel+"."+item.action+"(item)"

    for item in itemlist:
        item.title = encodingsafe(item.title)
        item.plot = encodingsafe(item.plot)
        Log("item="+item.tostring())

        if item.folder:
            if item.action=="search":
                dir.Append( Function( InputDirectoryItem( do_search, item.title, "subtitle", "txt", thumb = item.thumbnail ) , itemtext = item.serialize() ) )
            else:
                dir.Append( Function( DirectoryItem( actionexecute, title = item.title, subtitle = "subtitle", thumb = item.thumbnail ) , itemtext = item.serialize() ) )
        else:
            dir.Append( Function( DirectoryItem( playvideo , title=item.title, subtitle="", summary=item.plot, thumb = item.thumbnail), itemtext = item.serialize() ) )

    Log("[__init__.py] 5")

    return dir

def do_search(sender,query="",itemtext=""):
    item = Item()
    item.deserialize(itemtext)
    item.title = encodingsafe(item.title)
    item.plot = encodingsafe(item.plot)

    Log("[__init__.py] do_search "+item.tostring())
    dir = MediaContainer(viewGroup="InfoList")

    if item.channel=="buscador":
        exec "from pelisalacarta import buscador"
        exec "itemlist = buscador.do_search_results(query)"
    else:
        exec "from pelisalacarta.channels import "+item.channel
        exec "itemlist = "+item.channel+".search(item,texto=query)"

    for item in itemlist:
        item.title = encodingsafe(item.title)
        item.plot = encodingsafe(item.plot)
        Log("item="+item.title)

        if item.folder:
            dir.Append( Function( DirectoryItem( actionexecute, title = item.title, subtitle = "subtitle", thumb = item.thumbnail ) , itemtext = item.serialize() ) )
        else:
            dir.Append( Function( DirectoryItem( playvideo , title=item.title, subtitle="", summary=item.plot, thumb = item.thumbnail), itemtext = item.serialize() ) )

    return dir

def findvideos(item):
    from core.item import Item

    Log("[__init__.py] findvideos")

    url = item.url
    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot

    # Descarga la pagina
    from core import scrapertools
    data = scrapertools.cachePage(url)
    
    from servers import servertools
    listavideos = servertools.findvideos(data)
    
    itemlist = []
    for video in listavideos:
        scrapedtitle = video[0]
        scrapedurl = video[1]
        server = video[2]

        itemlist.append( Item(channel=item.channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))

    return itemlist

def playvideo(sender,itemtext):
    Log("[__init__.py] playvideo")
    item = Item()
    item.deserialize(itemtext)

    dir = MediaContainer(viewGroup="InfoList")

    if item.action=="play":
        try:
            Log("[__init__.py] playvideo ejecutando metodo play del canal #"+item.channel+"#")
            exec "from pelisalacarta.channels import "+item.channel
            exec "itemlist = "+item.channel+"."+item.action+"(item)"
            item = itemlist[0]
            item.title = encodingsafe(item.title)
            item.plot = encodingsafe(item.plot)
        except:
            Log("[__init__.py] playvideo error al ejecutar metodo play del canal")
            import sys
            for line in sys.exc_info():
                Log( "%s" % line )

    from core import config

    Log("[__init__.py] playvideo url="+item.url+", server="+item.server)

    video_urls = []
    video_password=""
    url = item.url
    server = item.server
    

    # Extrae las URL de los vídeos, y si no puedes verlo te dice el motivo
    from servers import servertools
    video_urls,puedes,motivo = servertools.resolve_video_urls_for_playing(server,url,video_password,False)

    # Si puedes ver el vídeo, presenta las opciones
    if puedes:
        for video_url in video_urls:
            if len(video_url)>2:
                wait_time=video_url[2]
                dir.Append(Function( VideoItem(playvideonormal, title="Ver el vídeo "+video_url[0]+" (Espera %d segundos)" % wait_time, subtitle="", summary="", thumb = ""), mediaurl=video_url[1] ))
            else:
                wait_time=0
                dir.Append(Function( VideoItem(playvideonormal, title="Ver el vídeo "+video_url[0], subtitle="", summary="", thumb = ""), mediaurl=video_url[1] ))

    # Si no puedes ver el vídeo te informa
    else:
        if server!="":
            if "<br/>" in motivo:
                dir.Append(Function( VideoItem(playvideonormal, title="No puedes ver este vídeo", subtitle="", summary="No puedes ver ese vídeo porque...\n"+motivo.split("<br/>")[0]+"\n"+motivo.split("<br/>")[1]+"\n"+url, thumb = ""), mediaurl="" ))
            else:
                dir.Append(Function( VideoItem(playvideonormal, title="No puedes ver este vídeo", subtitle="", summary="No puedes ver ese vídeo porque...\n"+motivo , thumb = ""), mediaurl="" ))
        else:
            dir.Append(Function( VideoItem(playvideonormal, title="No puedes ver este vídeo", subtitle="", summary="No puedes ver ese vídeo porque...\n"+"El servidor donde está alojado no está"+"\nsoportado en pelisalacarta todavía" , thumb = ""), mediaurl="" ))
    
    '''
    try:
        Log("megavideo="+config.get_setting("megavideopremium"))
        # Extrae todos los enlaces posibles
        exec "from servers import "+server+" as server_connector"
        if server=="megavideo" or server=="megaupload":
            video_urls = server_connector.get_video_url( page_url=url , premium=(config.get_setting("megavideopremium")=="true") , user=config.get_setting("megavideouser") , password=config.get_setting("megavideopassword"), video_password=video_password )
        elif server=="fileserve":
            video_urls = server_connector.get_video_url( page_url=url , premium=(config.get_setting("fileservepremium")=="true") , user=config.get_setting("fileserveuser") , password=config.get_setting("fileservepassword"), video_password=video_password )
        else:
            video_urls = server_connector.get_video_url( page_url=url , video_password=video_password )
    except:
        import sys
        for line in sys.exc_info():
            Log( "%s" % line )

    if config.get_setting("fileniumpremium")=="true" and item.server not in ["downupload","vk","fourshared","directo","adnstream","facebook","megalive","tutv","stagevu"]:
        exec "from servers import filenium as gen_conector"
        video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("fileniumpremium")=="true") , user=config.get_setting("fileniumuser") , password=config.get_setting("fileniumpassword"), video_password=video_password )
        Log("[xbmctools.py] filenium url="+video_gen)
        video_urls.append( [ "[filenium]", video_gen ] )
    '''
    
    return dir

def playvideonormal(sender,mediaurl,wait_time=0):
    Log("[__init__.py] playvideonormal url="+mediaurl)
    return Redirect(mediaurl)

def encodingsafe(text):
    from core import logger
    text = unicode( text , "utf-8",errors="replace" ).encode("utf-8")
    return text