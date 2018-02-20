# -*- coding: utf-8 -*-

""" sopcastro  (c)  2014 enen92 fightnight

    This file contains the the code for favourites used in the addon

    Functions:

	addon_favourites() -> Main menu. It parses the userdata/Favourites folder for items and lists them
	manual_add_to_favourites() -> Add a favourite to list manually
	add_to_addon_favourites(name,url,iconimage) -> Add an item to the addon favourites. Receives the name of the channel, the url and the iconimage
	remove_addon_favourites(url) -> Remove from addon favourites


"""

import xbmc,xbmcgui,xbmcplugin,xbmcvfs,sys,os
from utils.pluginxbmc import *
from utils.iofile import *
from utils.directoryhandle import addDir
from random import randint

def addon_favourites():
	if os.path.exists(os.path.join(pastaperfil,"Favourites")):
		dirs, files = xbmcvfs.listdir(os.path.join(pastaperfil,"Favourites"))
		if files:
			for file in files:
				string = readfile(os.path.join(pastaperfil,"Favourites",file))
				match = string.split("|")
				try: iconimage = match[2]
				except:
					iconimage = addonpath + art + getUrlType(match[1]) + '_logo.png'
				addDir("[B][COLOR orange]" + match[0] + "[/B][/COLOR]", match[1], getUrlTypeID(match[1]), iconimage, 1 ,False)
	addDir('[B]' + translate(70022) + '[/B]', MainURL, 203, addonpath + art + 'plus-menu.png', 2, False)
    #xbmc.executebuiltin("Container.SetViewMode(51)")

def manual_add_to_favourites():
	keyb = xbmc.Keyboard("", translate(70023))
	keyb.doModal()
	if (keyb.isConfirmed()):
		favourite_url = keyb.getText()
		if favourite_url.startswith("sop://") or favourite_url.startswith("acestream://") or favourite_url.endswith(".torrent") or favourite_url.endswith(".acelive"):
			keyb = xbmc.Keyboard("", translate(70024))
			keyb.doModal()
			if (keyb.isConfirmed()):
				favourite_name = keyb.getText()
				if favourite_name: pass
				else: favourite_name = 'sopcastro ' + str(randint(1,100))
				add_to_addon_favourites(favourite_name,favourite_url,'')
		else:
			mensagemok(translate(40000),translate(40128))

def add_to_addon_favourites(name,url,iconimage):
	name = name.replace("[b]","").replace("[/b]","").replace("[color orange]","").replace("[/color]","").replace("[B]","").replace("[/B]","")
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode=(.+?)&").findall(url.replace(";",""))
		for url,mode in match:
			favourite_text = str(name) + " (" + str(url) + ")|" + str(mode) + "|" + str(url) + '|' + str(iconimage)
			favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
			if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
			save(favouritetxt, favourite_text)
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40148), 1,addonpath+"/icon.png"))
	else:
		if not iconimage:
			iconimage = os.path.join(addonpath,'resources','art', getUrlType(url) + '_logo.png')

		favourite_text = str(name).translate(None, "|") + " (" + str(url) + ")|" + str(url) + '|' + str(iconimage)

		favouritetxt = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
		if not xbmcvfs.exists(os.path.join(pastaperfil,"Favourites")): xbmcvfs.mkdir(os.path.join(pastaperfil,"Favourites"))
		save(favouritetxt, favourite_text)
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40148), 1,addonpath+"/icon.png"))
		xbmc.executebuiltin("Container.Refresh")

def remove_addon_favourites(url):
	if "runplugin" in url:
		match = re.compile("url=(.+?)&mode").findall(url.replace(";",""))
		if match: ficheiro = os.path.join(pastaperfil,"Favourites",match[0].replace("/","").replace(":","") + ".txt")
	else:
		ficheiro = os.path.join(pastaperfil,"Favourites",url.replace(":","").replace("/","") + ".txt")
	xbmcvfs.delete(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(40000), translate(40147), 1,addonpath+"/icon.png"))
	xbmc.executebuiltin("Container.Refresh")

def getUrlType(url):
	if url.startswith("sop://"):
		return "sopcast"
	elif url.startswith("acestream://") or url.endswith(".torrent") or url.endswith(".acelive"):
		return "acestream"
	else:
		if len(url) < 30:
			return "sopcast"
		else:
			return "acestream"

def getUrlTypeID(url):
	return 1 + int(getUrlType(url) != "acestream")

