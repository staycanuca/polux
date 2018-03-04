# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains the common variables used by the addon.
    
    Functions:
    translate(text) -> Translate a string based on the Kodi used language.
   	notifi(title,message) -> Displays a notification.
    _log(message) -> Write to xbmc log file.
    
"""

import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import urllib
import urllib2
import re
import time
import socket
import os
import sys
import urllib

linkwiki="https://wiki.p2ptv.ml"
addon_id = 'plugin.video.p2ptv'
art = os.path.join('resources','art')
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
addonver = settings.getAddonInfo('version')
addonprofile = xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
messageok = xbmcgui.Dialog().ok
messagepg = xbmcgui.DialogProgress()
MainURL = 'https://www.p2ptv.ml'
addon_icon    = settings.getAddonInfo('icon')
mystrm_folder = os.path.join(addonprofile,'streams')
addontest = xbmcaddon.Addon()
      
def translate(text):
    return settings.getLocalizedString(text).encode('utf-8')

def notifi(title,message):
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (title, message, 1,addonpath+"/icon.png"))

def _log(message):
    xbmc.log("pluginxbmc." + message)

#Multicolor icons implementation
if settings.getSetting('menu_items_color') == '0':
    mystreamsPNG = 'blue\mystreams.png'
    historyPNG = 'blue\history.png'
    channelslists_menu_itemPNG = 'blue\channelslists-menu-item.png'
    play_menu_itemPNG =  'blue\play-menu-item.png'
    acestream_menu_itemPNG = 'blue\acestream-menu-item.png'
    sopcast_menu_itemPNG = 'blue\sopcast-menu-item.png'
    plus_menuPNG = 'blue\plus-menu.png'

elif settings.getSetting('menu_items_color') == '1':
    mystreamsPNG = 'red\mystreams.png'
    historyPNG = 'red\history.png'
    channelslists_menu_itemPNG = 'red\channelslists-menu-item.png'
    play_menu_itemPNG =  'red\play-menu-item.png'
    acestream_menu_itemPNG = 'red\acestream-menu-item.png'     
    sopcast_menu_itemPNG = 'red\sopcast-menu-item.png' 
    plus_menuPNG = 'red\plus-menu.png'

elif settings.getSetting('menu_items_color') == '2':
    mystreamsPNG = 'orange\mystreams.png'
    historyPNG = 'orange\history.png'
    channelslists_menu_itemPNG = 'orange\channelslists-menu-item.png'
    play_menu_itemPNG =  'orange\play-menu-item.png'
    acestream_menu_itemPNG = 'orange\acestream-menu-item.png'
    sopcast_menu_itemPNG = 'orange\sopcast-menu-item.png'
    plus_menuPNG = 'orange\plus-menu.png'

elif settings.getSetting('menu_items_color') == '3':
    mystreamsPNG = 'green\mystreams.png'
    historyPNG = 'green\history.png'
    channelslists_menu_itemPNG = 'green\channelslists-menu-item.png'
    play_menu_itemPNG =  'green\play-menu-item.png'
    acestream_menu_itemPNG = 'green\acestream-menu-item.png'
    sopcast_menu_itemPNG = 'green\sopcast-menu-item.png'
    plus_menuPNG = 'green\plus-menu.png'
