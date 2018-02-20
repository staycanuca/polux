# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of sopcastro addon

lfootball.ws

"""
import sys,os,zlib,urllib2
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *

base_url  = "http://lfootball.ws"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: lfootballws_events()
	elif parserfunction == 'streams': lfootballws_streams(url)

def lfootballws_events():
	try:
		source = mechanize_browser(base_url)
	except: source = ""; xbmcgui.Dialog().ok(translate(40000),translate(40128)); return;

	items = re.findall('<li class="fl">[^<]*<[^>]+class="link"[^>]+href="([^"]+)".+?"(?:liveCon clear|date)"><span[^>]*>(.+?)</span>', source, re.DOTALL)
	number_of_items= len(items)
	liveStreams = []
	nextStreams = []

	for url, dateEnc in items:
		date = dateEnc.decode("windows-1251").encode('utf8')
		dateRE = re.search('(\d+) ([^\s]+) (\d+):(\d+)', date)
		teams = re.search("\d+-(.+).html", url).group(1)
		if dateRE:
			import datetime
			from utils import pytzimp
			parsedTime = datetime.datetime(2015, 7, day=int(dateRE.group(1)), hour=int(dateRE.group(3)), minute=int(dateRE.group(4)))
			d = pytzimp.timezone('Europe/Moscow').localize(parsedTime)
			myTimeZone=pytzimp.timezone(pytzimp.all_timezones[int(settings.getSetting('timezone_new'))])
			convertedTime=d.astimezone(myTimeZone)
			timeStr=myTimeZone.normalize(convertedTime).strftime("%d %H:%M")
			nextStreams.append((url, teams, timeStr))
		elif date == "Live":
			liveStreams.append((url, teams))

	for stream in liveStreams:
		addDir("[B][COLOR green](Live)[/COLOR][/B] {0}".format(stream[1]), stream[0],401,os.path.join(current_dir,'icon.png'),number_of_items,False,parser="lfootballws",parserfunction="streams")

	for stream in reversed(nextStreams):
		addDir("[B][COLOR orange]({0} {1})[/COLOR][/B] {2}".format(translate(600012), stream[2], stream[1]), stream[0],401,os.path.join(current_dir,'icon.png'),number_of_items,False,parser="lfootballws",parserfunction="streams")


def lfootballws_streams(url):
	try:
		source = mechanize_browser(url)
	except: source = ""; xbmcgui.Dialog().ok(translate(40000),translate(40128));sys.exit(0); return

	links = []
	names = []
	streams = re.findall('<tr>.*?<td>.+?<td>.+?class="live-table__sourse">(.+?)</a.+?<td>.+?<td>([^<]*).+?<td>([^<]*).+?<td>.+?<td>([^<]*).*?href="([^"]+)".*?</tr>', source, re.DOTALL)
	for type, rate, channel, format, url in streams:
		name = "[{0} {1}] {2} ({3})".format(type, rate, channel, format)
		names.append(name)
		links.append(url)

	if len(links) > 0:
		dialog = xbmcgui.Dialog()
		index = dialog.select(translate(40021), names)

		if index>-1:
			name=names[index]
			url=links[index]
			from utils.parsers import parser_resolver
			parser_resolver(name, url, os.path.join(current_dir,'icon.png'))
	else:
		xbmcgui.Dialog().ok(translate(40000),translate(40022))

