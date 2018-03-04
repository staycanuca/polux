# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains the functions for xbmc addon directory handle.
    
    Functions:
    addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")) -> Addlink function used in the 'whole' addon.
    addDir(name,url,mode,iconimage,total,dirFolder,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path"),parser=None,parserfunction=None) -> AddDir function used in the whole addon.
    addDir_livestreams_common(name,url,mode,iconimage,folder,fanart) -> AddDir function used only for lists_manager folder.
    
"""

import xbmc
import xbmcgui
import xbmcvfs
import xbmcplugin
import os
import urllib
import sys
import hashlib
from pluginxbmc import *

def addLink(name,url,iconimage,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fan_art)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,dirFolder,fan_art="%s/fanart.jpg"%settings.getAddonInfo("path")):
    if "plugin://" in sys.argv[0]: u = sys.argv[0]; sysargv = sys.argv[0]
    else: u = 'plugin://plugin.video.p2ptv/'; sysargv = 'plugin://plugin.video.p2ptv/'
    u += "?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    contextmen = []
    liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty('fanart_image', fan_art)
    if mode == 1 or mode == 2 or mode == 15:
        fic = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
        if os.path.exists(os.path.join(mystrm_folder,fic)):
            contextmen.append((translate(30025), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),name,iconimage)))
        else:
            contextmen.append((translate(30026), 'XBMC.RunPlugin(%s?mode=12&url=%s&name=%s&iconimage=%s)' % (sysargv,urllib.quote_plus(url),name,iconimage)))
    elif mode == 101:
        try:
            fileloc = os.path.join(addonprofile,"Lists",name.replace("[B][COLOR orange]","").replace("[/B][/COLOR]","") + ".txt")
            if xbmcvfs.exists(fileloc):  
                contextmen.append((translate(30185), 'XBMC.RunPlugin(%s?mode=106&url=%s&name=%s&iconimage=%s)' % (sysargv, urllib.quote_plus(url),fileloc,iconimage)))
        except: pass
    liz.addContextMenuItems(contextmen,replaceItems=False)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=dirFolder,totalItems=total)
    
def addDir_livestreams_common(name,url,mode,iconimage,folder,fanart=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
    ok=True
    contextmen = []
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    if fanart:
        liz.setProperty('fanart_image', fanart)
    else:
        liz.setProperty('fanart_image', "%s/fanart.jpg"%settings.getAddonInfo("path"))
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
