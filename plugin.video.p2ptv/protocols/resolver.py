# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains a simple resolver script that detects the protocol of the URI address and then plays the stream.
    
    Functions:
    playstream(name,iconimage,url) -> Detects the protocol and then plays the stream with the correct library.
    test_channel() -> Displays an input dialog, detects the protocol of the URI address and then plays the stream with the correct library.
    
"""

import xbmc
import xbmcgui
import xbmcplugin
import acestream as ace
import sopcast as sop
from utils.pluginxbmc import *
from pages.history import add_to_history

def playstream(name,iconimage,url):
    if url.startswith("sop://"):
        sop.sopstreams(name,iconimage,url)
    elif url.startswith("acestream://"):
        ace.acestreams(name,iconimage,url)
    elif (url.startswith("http://")) or (url.startswith("https://")) or(url.startswith("rtmp://")) or (url.startswith("rtsp://")) or (url.startswith("mmsh://")):
        if settings.getSetting('addon_history') == "true":
	        try: add_to_history(name, str(url),15, iconimage)
	        except: pass
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        listitem.setLabel(name)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        listitem.setPath(url)
        playlist.add(url, listitem)
        xbmc.Player().play(playlist)    
    else:
        messageok(translate(30000), translate(30182))

def test_channel():
    keyb = xbmc.Keyboard('', translate(30166))
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        if search=='': sys.exit(0)
        else:
            if search.startswith("acestream://"):
                url_addr = search
                ace.acestreams(translate(30020) + ' ( ' + str(url_addr) + ')','',str(url_addr))
            elif search.startswith("sop://"):
                url_addr = search
                sop.sopstreams(translate(30021) + ' ( ' + str(url_addr) + ')','',str(url_addr))
            elif (search.startswith("http://")) or (search.startswith("https://")) or (search.startswith("rtmp://")) or (search.startswith("rtsp://")) or (search.startswith("mmsh://")):
                url_addr = search
                playstream(translate(30021) + ' ( ' + str(url_addr) + ')','',str(url_addr))
            elif search.startswith("sopid:"):
                url_addr = str(search).replace("sopid:", "")
                sop.sopstreams(translate(30020) + ' ( ' + str(url_addr) + ')','',str(url_addr))
            else:
                messageok(translate(30000),translate(30011))
