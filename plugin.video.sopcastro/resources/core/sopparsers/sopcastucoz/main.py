# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of sopcastro addon

Sopcast.ucoz

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

base_url = 'http://sopcast.ucoz.com'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: sopcast_ucoz()
	elif parserfunction == 'play': sopcast_ucoz_play(name,url)
    
def sopcast_ucoz():
    conteudo=clean(get_page_source('http://sopcast.ucoz.com'))
    listagem=re.compile('<div class="eTitle" style="text-align:left;"><a href="(.+?)">(.+?)</a>').findall(conteudo)
    for urllist,titulo in listagem:
    	addDir(titulo,urllist,501,'',len(listagem),False,parser="sopcastucoz",parserfunction="play")

def sopcast_ucoz_play(name,url):
    conteudo=clean(get_page_source('http://sopcast.ucoz.com' + url))
    blogpost = re.findall('script.+?p>(.*?)<tr><td colspan', conteudo, re.DOTALL)
    if blogpost:
    	ender=[]
    	titulo=[]
    	match = re.compile('br.+?>(.+?)<br.+?(sop.+?)<').findall(blogpost[0])
    	for nume,address in match:
    		if "sop://" in address:
    			titulo.append('' + nume +' Sopcast')
    			ender.append(address)
    		elif "acestrem://" in address:
    			titulo.append('Acestream [' + address.replace(' (ace stream)','') +']')
    			ender.append(address.replace(' (ace stream)',''))
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
