# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of sopcastro addon

MyWebTV
"""
import sys,os,requests
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
	elif parserfunction == 'post': tron_post(url)
	elif parserfunction == 'play': tron_play(name,url)
    
def tron():
    conteudo=clean(get_page_source('http://www.mywebtv.info'))
    blogpost = re.findall('<div id="channel">(.+?)<div id="body">', conteudo, re.DOTALL)
    if blogpost:
        listagem=re.compile('href="(.+?)".+?<h1 class="title" style=".+?">(.+?)</h1>').findall(blogpost[0])
        for link,titulo in listagem:
		    urllist = 'http://www.mywebtv.info' + link
	            addDir(titulo,urllist,501,os.path.join(current_dir,"icon.png"),1,True,parser="mywebtv",parserfunction="post")

def tron_post(url):
    conteudo=clean(get_page_source(url))
    blogpost = re.findall('<div class="sources">(.+?)<div class="epg-header">', conteudo, re.DOTALL)
    if blogpost:
        listagem=re.compile('href="(/.+?/sursa-\d)".+?<h2>(Sursa \d)</h2>.+?<h3>(Ace Player|sopcast)</h3>.+?<h3>(.+?)</h3>').findall(blogpost[0])
        for link,sursa,player,titlu in listagem:
		    titulo = titlu + ' ' + player + ' ' + sursa
		    urllist = 'http://www.mywebtv.info' + link
	            addDir(titulo,urllist,501,os.path.join(current_dir,"icon.png"),1,False,parser="mywebtv",parserfunction="play")

def tron_play(name,url):
    conteudo=clean(get_page_source(url))
    blogpost = re.findall('<div class="player player-ch">(.+?)<div class="play-info">', conteudo, re.DOTALL)
    if blogpost:
    	ender=[]
    	titulo=[]
    	match = re.compile('href="(acestream://|sop://.+?)"').findall(blogpost[0])
    	for address in match:
    		if "sop://" in address:
    			titulo.append('sopcast link')
    			ender.append(address)
    		elif "acestream://" in address:
    			titulo.append('acestream link')
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
