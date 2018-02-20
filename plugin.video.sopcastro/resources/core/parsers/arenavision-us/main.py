# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of sopcastro addon

Arenavision.us

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
from cleaner import *

base_url = "http://www.arenavision.us"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: arenavision_menu()
	elif parserfunction == "arenavision_streams": arenavision_streams(name,url)
	elif parserfunction == "arenavision_schedule": arenavision_schedule(url)
	elif parserfunction == "arenavision_chooser": arenavision_chooser(url)



def arenavision_menu():
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(base_url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('leaf"><a href="([^"]+?)"[^>]*>(.+?)</a').findall(source)
		for link, nome in match:
			if "events" in nome.lower():
				addDir("[B][COLOR red]Agenda/Schedule[/COLOR][/B]",base_url+link,401,os.path.join(current_dir,"icon.png"),1,True,parser="arenavision-us",parserfunction="arenavision_schedule")
			elif ("#" in nome.lower() or "av" in nome.lower() or "arenavision" in nome.lower()) and link != "/":
				addDir(nome,link,401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision-us",parserfunction="arenavision_streams")
			else: pass


def arenavision_streams(name,url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		match = re.compile('sop://(.+?)"').findall(source)
		if match: sop.sopstreams(name,os.path.join(current_dir,"icon.png"),"sop://" + match[0])
		else:
			match = re.compile('this.loadPlayer\("(.+?)"').findall(source)
			if match: ace.acestreams(name,os.path.join(current_dir,"icon.png"),match[0])
			else: xbmcgui.Dialog().ok(translate(40000),translate(40022))

def arenavision_schedule(url):
	headers = {
		"Cookie" : "beget=begetok; has_js=1;"
	}
	try:
		source = requests.get(url,headers=headers).text
	except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	if source:
		DATESTR = "<td[^>]+>(\d+)/(\d+)/(\d+)</td>"
		HOURSTR = "<td[^>]+>(\d+):(\d+)[^<]*</td>"
		TEXTSTR = "<td[^>]+>(.+?)</td>"
		EVENTSTR = "<tr>{DATE}[^<]+{HOUR}[^<]+{SPORT}[^<]+{COMPETITION}[^<]+{EVENT}[^<]+{CHANNELS}.*?</tr>".format(DATE = DATESTR, HOUR = HOURSTR, SPORT = TEXTSTR, COMPETITION = TEXTSTR, EVENT = TEXTSTR, CHANNELS = TEXTSTR)
		events = re.findall(EVENTSTR, source, re.DOTALL)
		for day, month, year, hour, minute, sport, competition, event, channelsStr in events:
			if channelsStr == "":
				pass

			timeStr = ""
			try:
				import datetime
				from utils import pytzimp
				d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
				timezona = settings.getSetting('timezone_new')
				my_location = pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
				convertido = d.astimezone(my_location)
				fmt = "%d-%m-%y %H:%M"
				timeStr=convertido.strftime(fmt)
			except:
				timeStr='N/A'

			channelsStr = removeNonAscii(channelsStr)
			channelsAndLanguages = re.findall(" *([Ss\d-]+) *\[([^\]]+)\]", channelsStr)

			streams = [(language, channels.split("-")) for channels, language in channelsAndLanguages]

			addDir('[B][COLOR red]{0}[/COLOR] [COLOR white]{1}[/COLOR][/B] {3} [COLOR yellow][{2}][/COLOR]'.format(timeStr, removeNonAscii(sport), removeNonAscii(competition), removeNonAscii(event)), str(streams),401,os.path.join(current_dir,"icon.png"),1,False,parser="arenavision-us",parserfunction="arenavision_chooser")
		return None


def arenavision_chooser(url):
	languagesAndChannels = eval(url)
	stringList = []
	channelList = []
	for language, channels in languagesAndChannels:
		stringList += [ "[COLOR white][{0}][/COLOR] [COLOR yellow]#{1}[/COLOR]".format(language, channel) for channel in channels ]
		channelList += channels

	index = xbmcgui.Dialog().select("On...", stringList)
	if index > -1:
		arenavision_streams("ArenaVision {0}".format(channelList[index]), "http://arenavision2018.ml" + "/" + str(channelList[index]).zfill(2))

def removeNonAscii(s):
	filtered = "".join(filter(lambda x: ord(x)<128, s))
	strings = re.findall("^\s*([^.]+?)(?:<br|$)", filtered, re.MULTILINE)
	return " ".join(strings)
