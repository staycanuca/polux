# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains the main menu and the addon directory tree.
    
"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time,subprocess,xbmcvfs,socket
from utils.pluginxbmc import *
from protocols import acestream as ace
from protocols import sopcast as sop
from utils.autoconf import *
from utils.directoryhandle import addLink,addDir
from protocols.acecore import stop_aceengine
from pages.history import *
from pages.mystreams import *
from pages.lists_manager import *
from protocols.resolver import *

def main_menu():
    addDir('[B]'+translate(30001)+'[/B]',MainURL,10,os.path.join(addonpath,art,mystreamsPNG),2,True)
    if settings.getSetting('addon_history') == "true":
        addDir('[B]'+translate(30002)+'[/B]',MainURL,8,os.path.join(addonpath,art,historyPNG),2,True)
    addDir('[B]'+translate(30169)+'[/B]',MainURL,100,os.path.join(addonpath,art,channelslists_menu_itemPNG),2,True)
    addDir('[B]'+translate(30166)+'[/B]',MainURL,14,os.path.join(addonpath,art,play_menu_itemPNG),2,False)
    addDir('[B]' + translate(30006)+'[/B]',MainURL,6,os.path.join(addonpath,art,acestream_menu_itemPNG),1,False)

    #break_sopcast is a function used in Windows to intentionally break the Sopcast.exe file by renaming one of its codec files. 
    #It's ran here to rename the file again in case it failed when played before.
    sop.break_sopcast()

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

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: regexs=params["regexs"]
except:pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: parser=urllib.unquote_plus(params["parser"])
except: pass
try:parserfunction=params["parserfunction"]
except: pass

print("Mode: "+str(mode))
print("URL: "+str(url))
print("Name: "+str(name))
print("Iconimage: "+str(iconimage))

if mode==None:
    print("Installed version: v" + addonver)
    if settings.getSetting('autoconfig') == "true": first_conf()
    else:
        if settings.getSetting('last_version_check') != addonver:
            try:check_for_updates()
            except: pass
    main_menu()

#from 1-15 functions related to AceStream, SopCast, playback history and 'My Streams' folder.
elif mode==1: ace.acestreams(name,iconimage,url)
elif mode==2: sop.sopstreams(name,iconimage,url)
elif mode==6: ace.load_local_torrent()
elif mode==7: stop_aceengine()
elif mode==8: list_history()
elif mode==9: remove_history()
elif mode==10: my_streams_menu()
elif mode==11: add_stream()
elif mode==12: add_stream(name,url,iconimage)
elif mode==13: remove_stream(name,url)
elif mode==14: test_channel()
elif mode==15: playstream(name,iconimage,url)
#from 100-199 functions related to remote/local channels lists.
elif mode == 100: lists_menu()
elif mode == 101: list_type(url)
elif mode == 102: parse_tvlist(url)
elif mode == 103: addlist()
elif mode == 104: xbmc.executebuiltin(url.replace(';',''))
elif mode == 105: remove_list(name)
elif mode == 106: selection_dialog(name,url)
elif mode == 107: SopXML_get_channels(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
