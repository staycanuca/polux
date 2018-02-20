# -*- coding: utf-8 -*-

""" 
This plugin is 3rd party and not part of p2p-streams addon

Livefootballol.me

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

base_url = "http://www.livefootballol.me"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: lfol_menu()
	elif parserfunction == "lfol_schedule": lfol_schedule()
	elif parserfunction == "lfol_streams": lfol_streams(name,url)
	elif parserfunction == "lfol_play_stream": lfol_play_stream(name,url,iconimage)
	elif parserfunction == "lfol_channels": lfol_channels()
	elif parserfunction == "lfol_channels_sop": lfol_channels_sop()
	elif parserfunction == "lfol_channels_ace": lfol_channels_ace()

def lfol_menu():
	addDir('Schedule','',401,os.path.join(current_dir,"icon.png"),1,True,parser="livefootballol",parserfunction="lfol_schedule")
	addDir('Channels','',401,os.path.join(current_dir,"icon.png"),1,True,parser="livefootballol",parserfunction="lfol_channels")
	
def lfol_channels():
	addDir('Acestream channels','',401,os.path.join(current_dir,"icon.png"),1,True,parser="livefootballol",parserfunction="lfol_channels_ace")
	addDir('Sopcast channels','',401,os.path.join(current_dir,"icon.png"),1,True,parser="livefootballol",parserfunction="lfol_channels_sop")

def lfol_channels_ace():
	try:
		source = requests.get(base_url+'/acestream-channel-list.html').text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('">\s*(?:<strong>)*\s*(.+?)</s.+?(?:</strong>)*</a></td>\n<td>(.+?)</td>\n<td>(.+?)</td>\n<td>(.+?)</td>').findall(source)
		for name,link,language,rate in match:
			addDir(clean(name)+' ('+language+'; '+rate+')',link,1,os.path.join(current_dir,"icon.png"),1,False,parser=None,parserfunction=None)

def lfol_channels_sop():
	try:
		source = requests.get(base_url+'/sopcast-channel-list.html').text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('">\s*(?:<strong>)*\s*(.+?)</s.+?(?:</strong>)*</a></td>\n<td>(.+?)</td>\n<td>(.+?)</td>\n<td>(.+?)</td>').findall(source)
		for name,link,rate,language in match:
			addDir(clean(name)+' ('+language+'; '+rate+')',link,2,os.path.join(current_dir,"icon.png"),1,False,parser=None,parserfunction=None)
	
def lfol_schedule():
	try:
		source = requests.get(base_url+'/live-football-streaming.html').text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('<div>\s*<h3>.+?(\d+)/(\d+)/(\d+).+<\/h3>\s*<\/div>\s*(<list (?:\s*|.)+?<\/list>)').findall(source)
		yday=0
		date_format = xbmc.getRegion('datelong')
		meridiem = xbmc.getRegion('meridiem')
		time_format = '%H:%M'
		if meridiem != '/':
			time_format = '%I:%M%p'
		for day,month,year, list in match:
			match = re.compile('(\d+)\:(\d+) (\[.+?\])\s*(?:<span class="even">)*\s*<a.+?href="(.+?)".*?>(.+?)<\/a>').findall(list)
			for hour, minute, competition, link, name in match:
				if "/streaming/" in link.lower():
					try:
						import datetime
						from utils import pytzimp
						d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
						timezona= settings.getSetting('timezone_new')
						my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
						convertido=d.astimezone(my_location)
						time=convertido.strftime(time_format)
						time='[B][COLOR orange]'+time+'[/B][/COLOR]'
						if yday != convertido.day:
							yday = convertido.day
							date=convertido.strftime(date_format) 
							addLink("[B][COLOR orange]"+date+"[/B][/COLOR]",'',os.path.join(current_dir,'icon.png'))
					except:
						time='[B][COLOR orange]'+hour+':'+minute+'[/B][/COLOR]'
						if yday != day:
							yday = day
							addLink('[B][COLOR orange]'+day+'/'+month+'/'+year+' GMT+1 [/B][/COLOR]','',os.path.join(current_dir,"icon.png"))
					addDir(time+' '+competition+' '+name,base_url+link,401,os.path.join(current_dir,"icon.png"),1,True,parser="livefootballol",parserfunction="lfol_streams")
				else: pass

def lfol_streams(name,url):
	try:
		source = requests.get(url).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('(?:.*\[(.+)\].*\n.*)?href="(.+?-(?:acestream|sopcast).*.html)">\s*(?:<strong>)*\s*(.+?)\s*(?:<\/strong>)*\s*<\/a>', re.IGNORECASE).findall(source)
		lang=''
		if match:
			for newlang, link, name in match:
				if(newlang):
					lang=newlang
				if(lang):
					name=name+'[B][COLOR orange] ['+lang+'][/B][/COLOR]'
				addDir(name,link,401,os.path.join(current_dir,"icon.png"),1,False,parser="livefootballol",parserfunction="lfol_play_stream")
		else:
			xbmcgui.Dialog().ok(translate(40000),translate(40022))

def lfol_play_stream(name,url,iconimage):
	try:
		source = requests.get(url).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('href="(acestream\:.+?)">').findall(source)
		match2 = re.compile('href="(sop\:.+?)">').findall(source)
		if match:
			ace.acestreams(name, iconimage, match[0])
		elif match2:
			sop.sopstreams(name, iconimage, match2[0])
		else:
			xbmcgui.Dialog().ok(translate(40000),translate(40022))
			
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def clean(text):
	text = text.replace(u'\xda','U').replace(u'\xc9','E').replace(u'\xd3','O').replace(u'\xd1','N').replace(u'\xcd','I').replace(u'\xc1','A').replace(u'\xfa','u')
	return text
		
