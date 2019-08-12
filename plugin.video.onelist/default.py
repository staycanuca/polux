# -*- coding: utf-8 -*-
import re,os,urllib2,urllib
import xbmcplugin,xbmcgui,xbmcaddon


addon = xbmcaddon.Addon()
BASE=addon.getSetting('M3U')
header_string='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'

def settings():
    xbmcaddon.Addon().openSettings()

def INDEX_CHANNELS():
    url=BASE
    req=urllib2.Request(url)
    req.add_header('User-Agent',header_string)
    response=urllib2.urlopen(req)
    source=response.read()
    response.close()
    match=re.compile('#EXT.+?,(.+?)\n(.+?)\n').findall(source)
    addDir('[B][COLOR white]Change Playlist[/COLOR][/B]','url',1,'')
    for play_name,play_url in match:
        addLink(play_name,play_url,'https://imge.apk.tools/150/e/b/a/com.app.legomartintv.png')
		
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                 param[splitparams[0]]=splitparams[1]
    return param

def addLink(name,url,iconimage):
    if url.startswith('acestream://'):
        url = 'plugin://program.plexus/?mode=1&url={0}&name={1}&iconimage={2}'.format(url, name, iconimage)
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage)
        liz.setInfo(type="Video",infoLabels={"Title":name})
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    elif url.startswith('sop://'):
        url = 'plugin://program.plexus/?mode=2&url={0}&name={1}&iconimage={2}'.format(url, name, iconimage)
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage)
        liz.setInfo(type="Video",infoLabels={"Title":name})
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    elif '.ts' in url:
        url = 'plugin://plugin.video.f4mTester/?url={0}&streamtype=TSDOWNLOADER&name={1}'.format(url, name, iconimage)
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage)
        liz.setInfo(type="Video",infoLabels={"Title":name})
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    else:
        ok=True
        liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage)
        liz.setInfo(type="Video",infoLabels={"Title":name})
        liz.setProperty('IsPlayable','true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
		

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name })
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

xbmc.log("Mode: "+str(mode))
xbmc.log("URL: "+str(url))
xbmc.log("Name: "+str(name))

if mode==None or url==None or len(url)<1:
        INDEX_CHANNELS()

elif mode == 1:
    xbmcaddon.Addon().openSettings()
    exit()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
