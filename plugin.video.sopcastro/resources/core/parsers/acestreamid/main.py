# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of sopcastro addon

ACESearch

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *

base_url = 'https://acestreamid.com/'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: acesearch()
    
def acesearch():
	try:
		source = mechanize_browser(base_url)
	except: source = "";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match= re.compile("(?s)<div class=\"font-small.+?\">(.+?)</div></div.+?class=\"content wrap\">(.+?)</div></div>").findall(source)
		for titulo,acestream in match:
			addDir(titulo,acestream,1,os.path.join(current_dir,'icon.png'),len(match),False)
        #xbmc.executebuiltin("Container.SetViewMode(51)")
