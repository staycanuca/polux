# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of sopcastro addon

1torrent.tv

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

base_url = 'http://1torrent.tv'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: onetorrent_main()
	elif parserfunction == 'list_category': list_category(url)
	elif parserfunction == 'play_torrent':  onetorrent_resolver(name,url)

def onetorrent_main():
	html_source = clean(get_page_source(base_url+"/channels.php"))
	categorias=re.findall('<div class="tab_caption.+?" id="tcap_(.+?)".+?>(.+?)</div>', html_source)
	catMap = dict([(catid, catname) for catid,catname in categorias])

	catResult = {}
	canais=re.findall('<div class=".+?" id="tcon_([0-9]+)"(.+?)</div></div></div></div>', html_source)
	for catid, lista in canais:
		individual=re.findall('<img src="(.+?)">.+?<a href="(.+?)=(.+?)">(.+?)</a', lista)
		catResult[catMap[catid]] = [(name, link, img, url) for img,url,link,name in individual]

	for name, streams in catResult.iteritems():
		addDir('[B][COLOR orange]{0}[/B][/COLOR]'.format(name),str(streams),401,os.path.join(current_dir,"icon.png"),len(catResult),True,parser="onetorrenttv",parserfunction="list_category")

def list_category(categoryData):
	category = eval(categoryData)
	for stream in category:
		addDir(stream[0],'http://1torrent.tv/sc_current_stream.php?cid='+stream[1],401,base_url + stream[2],2,False,parser="onetorrenttv",parserfunction='play_torrent')

def onetorrent_resolver(name,url):
	try:
		conteudo=get_page_source(url)
	except: conteudo = ''
	if conteudo:
		try:torrent=re.findall('\"stream_url\":\"(.+?)\"', conteudo)[0]
		except:torrent=re.findall('\"stream_url\":\"(.+?)\"', conteudo)[0]
		logo=re.findall('\"logo\":\"(.+?)\"', conteudo)[0]
		ace.acestreams(name,base_url + logo,torrent)
