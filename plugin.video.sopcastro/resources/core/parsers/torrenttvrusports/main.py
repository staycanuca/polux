# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of sopcastro addon

Torrent-TV.ru sports section

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *

base_url = 'http://91.92.66.82/trash/ttv-list/ttv.m3u'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: torrent_tv_sports()
    
def torrent_tv_sports():
	try:
		source = mechanize_browser(base_url)
	except: source = "";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match= re.compile("#EXTINF:-1,Sky Sports News \(.+?\)\n(.*)").findall(source)
		if match: addDir('Sky Sports News',match[0],1,os.path.join(current_dir,'icon.png'),len(match),False)
		match= re.compile("#EXTINF:-1,(.+?)\(Спорт\)\n(.*)").findall(source)
		for titulo,acestream in match:
			clean = re.compile("\((.+?)\)").findall(titulo)
			for categorie in clean:
				titulo = titulo.replace("(" + categorie +")","")
			addDir(titulo,acestream,1,os.path.join(current_dir,'icon.png'),len(match),False)
        #xbmc.executebuiltin("Container.SetViewMode(51)")
