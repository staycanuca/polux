# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of sopcastro addon

MyWebTV
"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
import acestream as ace
import sopcast as sop

base_url = 'http://www.mywebtv.info'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: tron()
	elif parserfunction == 'play': tron_play(name,url)
    
def tron():
    conteudo=clean(get_page_source('http://www.mywebtv.info'))
    blogpost = re.findall('<ul class="scroll-pane2 style1">(.+?)</ul>', conteudo, re.DOTALL)
    if blogpost:
        listagem=re.compile('<div  class="strm2"><div onClick=".+?, \'(.+?)\'.+?>Stream (\d) \(sop\)</div>').findall(blogpost[0])
        for titulo,link in listagem:
		    urllist = titulo + '/sursa-' + link
	            addDir(titulo,urllist,501,'',len(listagem),False,parser="mywebtv",parserfunction="play")

def tron_play(name,url):
    conteudo=clean(get_page_source('http://www.mywebtv.info/' + url))
    blogpost = re.findall('<div id="player">(.+?)</div>', conteudo, re.DOTALL)
    if blogpost:
    	ender=[]
    	titulo=[]
    	match = re.compile('value="(sop://.+?)".+?value="(.+?)"').findall(blogpost[0])
    	for address,nume in match:
    		if "sop://" in address:
    			titulo.append('' + nume + ' - ' + name +' sopcast link')
    			ender.append(address)
    		elif "acestream://" in address:
    			titulo.append('' + nume + ' - ' + name +' acestream link')
    			ender.append(address)
    		else: pass
    	if ender and titulo:
    		index = xbmcgui.Dialog().select(translate(40023), titulo)
    		if index > -1:
    			nomeescolha=titulo[index]
    			linkescolha=ender[index]
    			if re.search('acestream',nomeescolha,re.IGNORECASE) or re.search('TorrentStream',nomeescolha,re.IGNORECASE): ace.acestreams(nomeescolha,'',linkescolha)
    			elif re.search('sopcast',nomeescolha,re.IGNORECASE): sop.sopstreams(nomeescolha,'',linkescolha)
		        else: xbmcgui.Dialog().ok(translate(40000),translate(40024))  
    else:
    	xbmcgui.Dialog().ok(translate(40000),translate(40008))
