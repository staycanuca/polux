# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains all functions for "My streams" folder.
    
    Functions:
    my_streams_menu() -> Display 'My streams' folder.
    add_stream(name='',url='',iconimage='') -> Add a channel to the local list.
    remove_stream(name,url) -> Remove a channel from the local list.
    
"""

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import hashlib
import sys
from utils.pluginxbmc import *
from utils.directoryhandle import *
from utils.iofile import *

def my_streams_menu():
    if settings.getSetting("menu_items_color") == "0":
        mystreamsPNG = './blue/mystreams.png'
        historyPNG = "./blue/history.png"
        romania_menu_itemPNG = "./blue/romania-menu-item.png"
        channelslists_menu_itemPNG = "./blue/channelslists-menu-item.png"
        play_menu_itemPNG =  "./blue/play-menu-item.png"
        acestream_menu_itemPNG = "./blue/acestream-menu-item.png"
        plus_menuPNG = "./blue/plus-menu.png"

    elif settings.getSetting("menu_items_color") == "1":
        mystreamsPNG = './red/mystreams.png'
        historyPNG = "./red/history.png"
        romania_menu_itemPNG = "./red/romania-menu-item.png"
        channelslists_menu_itemPNG = "./red/channelslists-menu-item.png"
        play_menu_itemPNG =  "./red/play-menu-item.png"
        acestream_menu_itemPNG = "./red/acestream-menu-item.png"
        plus_menuPNG = "./red/plus-menu.png"

    elif settings.getSetting("menu_items_color") == "2":
        mystreamsPNG = './orange/mystreams.png'
        historyPNG = "./orange/history.png"
        romania_menu_itemPNG = "./orange/romania-menu-item.png"
        channelslists_menu_itemPNG = "./orange/channelslists-menu-item.png"
        play_menu_itemPNG =  "./orange/play-menu-item.png"
        acestream_menu_itemPNG = "./orange/acestream-menu-item.png"
        plus_menuPNG = "./orange/plus-menu.png"

    elif settings.getSetting("menu_items_color") == "3":
        mystreamsPNG = './green/mystreams.png'
        historyPNG = "./green/history.png"
        romania_menu_itemPNG = "./green/romania-menu-item.png"
        channelslists_menu_itemPNG = "./green/channelslists-menu-item.png"
        play_menu_itemPNG =  "./green/play-menu-item.png"
        acestream_menu_itemPNG = "./green/acestream-menu-item.png"
        plus_menuPNG = "./green/plus-menu.png"

    if not os.path.exists(mystrm_folder): xbmcvfs.mkdir(mystrm_folder)
    files = os.listdir(mystrm_folder)
    if files:
        for fic in files:
            content = readfile(os.path.join(mystrm_folder,fic)).split('|')
            if content:
                if 'acestream://' in content[1] or '.acelive' in content[1] or '.torrent' in content[1]:
                    addDir(content[0],content[1],1,content[2],1,False)
                elif 'sop://' in content[1]:
                    addDir(content[0],content[1],2,content[2],1,False)
                elif 'http://' in content[1] or 'https://' in content[1] or 'mmsh://' in content[1] or 'rtmp://' in content[1] or 'rtsp://' in content[1]:
                    addDir(content[0],content[1],15,content[2],1,False)
                else:
                    pass
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
    addDir('[B][COLOR green]'+translate(30009)+'[/COLOR][/B]',MainURL,11,os.path.join(addonpath,art,plus_menuPNG),1,False)

def add_stream(name='',url='',iconimage=''):
    if not name or not url:
        keyb = xbmc.Keyboard('', translate(30010))
        keyb.doModal()
        if (keyb.isConfirmed()):
            stream = keyb.getText()
            if stream == '' : sys.exit(0)
            else:
                if ('acestream://' not in stream and '.acelive' not in stream and 'sop://' not in stream and 'http://' not in stream 
                and 'https://' not in stream and 'rtmp://' not in stream and 'mmsh://' not in stream):
                    messageok(translate(40000),translate(30011))
                    sys.exit(0)
                else:
                    #icon
                    yes = xbmcgui.Dialog().yesno(translate(30000), translate(30012))
                    if yes:
                        iconimage = xbmcgui.Dialog().browse(1, translate(30013),'video','.png|.jpg|.jpeg|.gif',True)
                    else:
                        if 'acestream://' in stream or '.acelive' in stream or '.torrent' in stream:
                            iconimage = os.path.join(addonpath,'resources','art','acestream-menu-item.png')
                        elif 'sop://' in stream:
                            iconimage = os.path.join(addonpath,'resources','art','sopcast-menu-item.png')
                        elif 'http://' in stream or 'https://' in stream or 'rtmp://' in stream or 'rtsp://' in stream or 'mmsh://' in stream:
                            iconimage = ''
                        else:
                            iconimage = ''
                    #name
                    keyb = xbmc.Keyboard('', translate(30014))
                    keyb.doModal()
                    if (keyb.isConfirmed()):
                        name = keyb.getText()
                        if name == '' : sys.exit(0)
                        else:
                        #save
                            content = name + '|' + stream + '|' + iconimage
                            filename = hashlib.md5(name + '|' + stream).hexdigest() + '.txt'
                            save(os.path.join(mystrm_folder,filename),content)
                            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30015), 1,os.path.join(addonpath,"icon.png")))
                            xbmc.executebuiltin("Container.Refresh")
    else:
        content = name + '|' + url + '|' + iconimage
        filename = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
        save(os.path.join(mystrm_folder,filename),content)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30015), 1,os.path.join(addonpath,"icon.png")))
        xbmc.executebuiltin("Container.Refresh")

def remove_stream(name,url):
    filename = hashlib.md5(name + '|' + url).hexdigest() + '.txt'
    fileloc = os.path.join(mystrm_folder,filename)
    try:
        os.remove(fileloc)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30016), 1,os.path.join(addonpath,"icon.png")))
        xbmc.executebuiltin("Container.Refresh")
    except: pass
