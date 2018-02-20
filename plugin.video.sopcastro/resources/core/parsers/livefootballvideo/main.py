# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of sopcastro addon

Livefootballvideo.com

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
from utils.timeutils import translate_months
from BeautifulSoup import BeautifulSoup as bs

base_url = 'http://livefootballvideo.com/streaming'


#<div class="team column"><img width="32" alt="Gimnasia La Plata" src="/images/teams/small/gimnasia-la-plata.png"><span>Gimnasia La Plata</span></div>
#<div class="versus column">vs.</div>
#<div class="team away column"><span>Nueva Chicago</span><img width="32" alt="Nueva Chicago" src="/images/teams/small/nueva-chicago.png"></div>
#<div class="live_btn column">
#<a class="online" href="http://livefootballvideo.com/streaming/argentina/primera-division/gimnasia-la-plata-vs-nueva-chicago">
#Online </a>


def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: livefootballvideo_events()
	elif parserfunction == 'sources': livefootballvideo_sources(url)

def livefootballvideo_events():
	try:
		html = get_page_source(base_url)
	except: html ="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
	soup=bs(html)
	table=soup.find('div',{'class':'listmatch'})
	lis=table.findAll('li')
	for item in lis:
		league=item.find('div',{'class':'leaguelogo column'}).find('img')['alt']
		time=item.find('span',{'class':'starttime time'})['rel']
		import datetime
		ts = datetime.datetime.fromtimestamp(float(time))
		year,month,day,hour,minute=ts.strftime('%Y'),ts.strftime('%m'),ts.strftime('%d'),ts.strftime('%H'),ts.strftime('%M')
		from utils import pytzimp
		d = pytzimp.timezone(str(pytzimp.timezone('Europe/Madrid'))).localize(datetime.datetime(2000 + int(year), int(month), int(day), hour=int(hour), minute=int(minute)))
		timezona= settings.getSetting('timezone_new')
		my_location=pytzimp.timezone(pytzimp.all_timezones[int(timezona)])
		convertido=d.astimezone(my_location)
		fmt = "%d-%m-%y [COLOR white]%H:%M[/COLOR]"
		time=convertido.strftime(fmt)
		try:
			team1=item.find('div',{'class':'team column'}).find('img')['alt']
			team2=item.find('div',{'class':'team away column'}).find('img')['alt']
		except:
			team1=item.find('div',{'class':'program column'}).getText()
			team2=''

		url=item.find('div',{'class':'live_btn column'}).find('a')['href']
		name='%s - %s'%(team1,team2)
		if team2=='':
			name=team1
		name=clean(cleanex(name))
		title='([COLOR blue][B]%s[/B][/COLOR]) [B][COLOR %s]%s[/COLOR][/B] [%s]'%(time,"green" if item.find('a',{'class':'online'}) else "orange",name,league)
		addDir(title,url,401,os.path.join(addonpath,'resources','art','football.png'),len(lis),False,parser='livefootballvideo',parserfunction='sources')

def livefootballvideo_sources(url):
	try:
		html = get_page_source(url)
	except: source = ""; xbmcgui.Dialog().ok(translate(40000),translate(40128))
	names,links=[],[]
	soup=bs(html)
	try:
		table=soup.find('div',{'id':'sopcastlist'}).find('tbody').findAll('tr')
		for i in range(1,len(table)):
			tds=table[i].findAll('td')
			channel_name=tds[1].getText()
			lang=tds[2].getText().replace('-','N/A')
			bitrate=tds[3].getText().replace('-','N/A')

			title='%s [%s] (%s)'%(channel_name,lang,bitrate)
			sop=table[i].findAll('a')[1]['href']

			names+=["[Sopcast] " + title]
			links+=[sop]
	except:
		names=[]
		links=[]
	try:
		table=soup.find('div',{'id':'livelist'}).find('tbody').findAll('tr')
		for i in range(3,len(table)):
			if table[i].find('a')['title']=='acestream':
				tds=table[i].findAll('td')
				channel_name=tds[1].getText()
				lang=tds[2].getText().replace('-','N/A')
				bitrate=tds[3].getText().replace('-','N/A')
				title='%s [%s] (%s)'%(channel_name,lang,bitrate)
				sop=table[i].findAll('a')[1]['href']
				names+=["[Acestream] " + title]
				links+=[sop]
	except:
		names=[]
		links=[]

	if links!=[]:
		dialog = xbmcgui.Dialog()
		index = dialog.select(translate(40021), names)

		if index>-1:
			name=names[index]
			url=links[index]
			from utils.parsers import parser_resolver
			parser_resolver(name, url, os.path.join(current_dir,'icon.png'))
	else:
		xbmcgui.Dialog().ok(translate(40000),translate(40022))
