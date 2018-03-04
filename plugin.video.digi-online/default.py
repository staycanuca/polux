import HTMLParser
import cookielib
import json
import os
import re
import sys
import urllib
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import time
import socket, ssl
import m3u8
#import requests


## Settings
settings = xbmcaddon.Addon(id='plugin.video.digi-online')
login_User = settings.getSetting('login_User')
login_Password = settings.getSetting('login_Password')
login_Enabled = settings.getSetting('login_Enabled')
debug_Enabled = settings.getSetting('debug_Enabled')
http_log_Enable = settings.getSetting('http_log_Enable')
osdInfo_Enabled = settings.getSetting('popup_Enabled')
epgInfo_Enabled = settings.getSetting('popup_EPGinfo')

extra_streamSRV = settings.getSetting('extra_streamSRV')
hiddenProgrammes = ['discoverye', 'tv5mondee', 'tlce', 'travelmixchannele', 'eentertainmente', 'connectmedia']

digiMaster = 'balancer.digi24.ro'
keyMaster = 'http://balancer.digi24.ro/streamer/make_key.php'
digiwebSite = 'www.digi-online.ro'
digiURL = 'http://www.digi-online.ro'
loginURL = 'http://www.digi-online.ro/xhr-login.php'

userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
browser='chrome'
deviceModel = '61'
deviceOS='macintel'
device_id = 'chrome_61_macintel_333806a4cf23e251087b9da0892b177c_PCBROWSER'

myLogFile = os.path.join(settings.getAddonInfo('path'), 'resources', 'plugin_video_digi-online.log')
myCookieFile = os.path.join(settings.getAddonInfo('path'), 'resources', 'cookie.txt')
myPlayFile = os.path.join(settings.getAddonInfo('path'), 'resources', 'playlist.m3u8')
stream_Quality = settings.getSetting('stream_Quality')
if stream_Quality == '':
  stream_Quality = 'hq'

search_thumb = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', 'search.png')
movies_thumb = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', 'movies.png')
next_thumb = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', 'next.png')
addon_thumb = os.path.join(settings.getAddonInfo('path'), 'icon.png')
addon_fanart = os.path.join(settings.getAddonInfo('path'), 'fanart.jpg')

LF = open(myLogFile, 'w+')
LF.write('--- INIT -------------------' + '\n')
LF.close()


def removeSubstr(string, suffix):
    return string[:string.index(suffix) + len(suffix)]


def trimSubstrEnd(string, prefix):
    part = string.split(prefix)
    return str(part[1])


def trimSubstr(string, suffix):
    part = string.split(suffix)
    return str(part[0])


def setIcon(thumb_file):
  thumb_file_name = thumb_file.replace(' ', '')[:-4].upper()
  try:
    thumb_file_name = os.path.join(settings.getAddonInfo('path'), 'resources', 'media', thumb_file)
  except:
    thumb_file_name = movies_thumb

  return thumb_file_name


def log_MyVars():
  LF = open(myLogFile, 'a')
  LF.write('---- MyVars ----------------' + '\n')
  LF.write("login_User: '" + "********" + '\'\n')
  LF.write("login_Password: '" + "********"  + '\'\n')
  LF.write("Digi-Online login enabled: '" + str(login_Enabled) + '\'\n')
  LF.write("OSD Info Popup: '" + str(osdInfo_Enabled) + '\'\n')
  LF.write("OSD EPG Info: '" + str(epgInfo_Enabled) + '\'\n')
  LF.write("Preferred stream_Quality: '" + stream_Quality + '\'\n')
  LF.write("http_log_Enable: '" + str(http_log_Enable) + '\'\n')
  LF.write("userAgent: '" + userAgent + '\'\n')
  LF.write("device_id: '" + device_id + '\'\n')
  LF.write('----------------------------' + '\n')
  LF.close()


def ROOT():
  #addDir('*GHID TV', '', setIcon('tv.png'))
  #addDir('*DIGI PLAY', '', setIcon('movies.png'))
  addDir('Digi24', 'http://www.digi-online.ro/tv/digi24/', setIcon('Digi24.png'))
  addDir('digi24.ro', 'http://www.digi24.ro/live/digi24', setIcon('Digi24.png'))
  addDir('B1 TV', 'http://www.digi-online.ro/tv/b1+tv/', setIcon('B1TV.png'))
  addDir('Realitatea TV', 'http://www.digi-online.ro/tv/realitatea+tv/', setIcon('RealitateaTV.png'))
  addDir('Romania TV', 'http://www.digi-online.ro/tv/romania+tv/', setIcon('RomaniaTV.png'))
  addDir('France 24 [EN]', 'http://www.digi-online.ro/tv/france+24/', setIcon('France24.png'))
  if settings.getSetting('75') == 'true':
    addDir('TV5 Monde [FR]', 'http://' + str(extra_streamSRV) +'/digiedge2/tv5mondee' + str(stream_Quality) +'/index.m3u8?is=75&src=app&t=00000000000000000000000000000000', setIcon('tv5monde.png'))
  addDir('CNN [EN]', 'http://www.digi-online.ro/tv/cnn/', setIcon('CNN.png'))

  addDir('Travel Channel', 'http://www.digi-online.ro/tv/travel+channel/', setIcon('TravelChannel.png'))
  if settings.getSetting('74') == 'true':
    addDir('Travel Mix Channel', 'http://' + str(extra_streamSRV) +'/travelmixchannele' + str(stream_Quality) +'/index.m3u8?is=74&src=app&t=00000000000000000000000000000000', setIcon('tv.png'))
  addDir('Digi Life', 'http://www.digi-online.ro/tv/digi+life/', setIcon('DigiLife.png'))
  addDir('Digi World', 'http://www.digi-online.ro/tv/digi+world/', setIcon('DigiWorld.png'))
  addDir('Viasat Explorer', 'http://www.digi-online.ro/tv/viasat+explorer/', setIcon('ViasatExplore.png'))
  if settings.getSetting('71') == 'true':
    addDir('Discovery Channel', 'http://' + str(extra_streamSRV) +'/digiedge2/discoverye' + str(stream_Quality) +'/index.m3u8?is=71&src=app&t=00000000000000000000000000000000', setIcon('DiscoveryChannel.png'))
  addDir('National Geographic', 'http://www.digi-online.ro/tv/national+geographic/', setIcon('NatGeographic.png'))
  addDir('History Channel', 'http://www.digi-online.ro/tv/history+channel/', setIcon('HistoryChannel.png'))
  addDir('Viasat History', 'http://www.digi-online.ro/tv/viasat+history/', setIcon('ViasatHistory.png'))
  addDir('National Geographic Wild', 'http://www.digi-online.ro/tv/national+geographic+wild/', setIcon('NatGeoWild.png'))
  addDir('BBC Earth', 'http://www.digi-online.ro/tv/bbc+earth/', setIcon('BBC_Earth.png'))
  addDir('Digi Animal World', 'http://www.digi-online.ro/tv/digi+animal+world/', setIcon('DigiAnimalWorld.png'))
  addDir('Viasat Nature', 'http://www.digi-online.ro/tv/viasat+nature/', setIcon('ViasatNature.png'))
  addDir('Fishing & Hunting', 'http://www.digi-online.ro/tv/fishing+and+hunting/', setIcon('PVTV.png'))
  addDir('CBS Reality', 'http://www.digi-online.ro/tv/cbs+reality/', setIcon('CBSReality.png'))
  if settings.getSetting('72') == 'true':
    addDir('TLC Entertainment', 'http://' + str(extra_streamSRV) +'/digiedge2/tlce' + str(stream_Quality) +'/index.m3u8?is=72&src=app&t=00000000000000000000000000000000', setIcon('TLC.png'))
  if settings.getSetting('73') == 'true':
    addDir('Epop Entertainment', 'http://' + str(extra_streamSRV) +'/digiedge2/eentertainmente' + str(stream_Quality) +'/index.m3u8?is=73&src=app&t=00000000000000000000000000000000', setIcon('tv.png'))

  addDir('AXN', 'http://www.digi-online.ro/tv/axn/', setIcon('AXN.png'))
  addDir('AXN Spin', 'http://www.digi-online.ro/tv/axn+spin/', setIcon('AXN_Spin.png'))
  addDir('AXN White', 'http://www.digi-online.ro/tv/axn+white/', setIcon('AXN_White.png'))
  addDir('AXN Black', 'http://www.digi-online.ro/tv/axn+black/', setIcon('AXN_Black.png'))
  addDir('Film Cafe', 'http://www.digi-online.ro/tv/film+cafe/', setIcon('FilmCafe.png'))
  addDir('TNT', 'http://www.digi-online.ro/tv/tnt/', setIcon('TNT2.png'))
  addDir('TV1000', 'http://www.digi-online.ro/tv/tv+1000/', setIcon('TV1000.png'))
  if login_Enabled == "true":
    addDir('Digi Film', 'http://www.digi-online.ro/tv/digi+film/', setIcon('DigiFilm.png'))

  addDir('UTV', 'http://www.digi-online.ro/tv/utv/', setIcon('UTV.png'))
  addDir('Music Channel', 'http://www.digi-online.ro/tv/music+channel/', setIcon('MusicChannel.png'))
  addDir('Kiss TV', 'http://www.digi-online.ro/tv/kiss+tv/', setIcon('KissTV.png'))
  addDir('HitMusic Channel','http://www.digi-online.ro/tv/hit+music+channel/', setIcon('HitMusicChannel.png'))
  addDir('Slager TV [HU]','http://www.digi-online.ro/tv/slager+tv/', setIcon('SlagerTV.png'))

  addDir('Disney Channel', 'http://www.digi-online.ro/tv/disney+channel/', setIcon('DisneyChannel.png'))
  addDir('Megamax', 'http://www.digi-online.ro/tv/megamax/', setIcon('Megamax.png'))
  addDir('Nickelodeon', 'http://www.digi-online.ro/tv/nickelodeon/', setIcon('Nickelodeon.png'))
  addDir('Minimax', 'http://www.digi-online.ro/tv/minimax/', setIcon('Minimax.png'))
  addDir('Disney Junior', 'http://www.digi-online.ro/tv/disney+junior/', setIcon('DisneyJunior.png'))
  addDir('Cartoon Network', 'http://www.digi-online.ro/tv/cartoon+network/', setIcon('CartoonNetw.png'))
  addDir('Boomerang', 'http://www.digi-online.ro/tv/boomerang/', setIcon('Boomerang.png'))
  addDir('Davinci Learning', 'http://www.digi-online.ro/tv/davinci+learning/', setIcon('DaVinciLearning.png'))

  addDir('DigiSport 1', 'http://www.digi-online.ro/tv/digisport+1/', setIcon('DigiSport1.png'))
  addDir('DigiSport 2', 'http://www.digi-online.ro/tv/digisport+2/', setIcon('DigiSport2.png'))
  addDir('DigiSport 3', 'http://www.digi-online.ro/tv/digisport+3/', setIcon('DigiSport3.png'))
  addDir('DigiSport 4', 'http://www.digi-online.ro/tv/digisport+4/', setIcon('DigiSport4.png'))
  addDir('EuroSport 1', 'http://www.digi-online.ro/tv/eurosport/', setIcon('EuroSport1.png'))
  addDir('EuroSport 2', 'http://www.digi-online.ro/tv/eurosport+2/', setIcon('EuroSport2.png'))

  addDir('TVR 1', 'http://www.digi-online.ro/tv/tvr+1/', setIcon('TVR1.png'))
  addDir('TVR 2', 'http://www.digi-online.ro/tv/tvr+2/', setIcon('TVR2.png'))
  addDir('Digi24 Oradea', 'http://www.digi-online.ro/tv/digi24+oradea/', setIcon('Digi24.png'))
  addDir('Digi24 Brasov', 'http://www.digi-online.ro/tv/digi24+brasov/', setIcon('Digi24.png'))
  addDir('Digi24 Cluj', 'http://www.digi24.ro/live/digi24-cluj-napoca', setIcon('Digi24.png'))
  #addDir('M1', 'https://c402-node62-cdn.connectmedia.hu/1100/746f4587970e6a9d1d77231922604086/5a19fb6f/05.m3u8', setIcon('tv.png'))


def addDir(name, url, iconimage):
    iconimage = urllib.unquote(urllib.unquote(iconimage))
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&name=" + urllib.quote_plus(name) + "&thumb=" + urllib.quote_plus(iconimage)
    listedItem = xbmcgui.ListItem(name, iconImage=movies_thumb, thumbnailImage=iconimage)
    itemInfo = {
      'type': 'Video',
      'genre': 'Live Stream',
      'title': name,
      'playcount': '0'
    }
    listedItem.setInfo('video', itemInfo)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=listedItem)

    if debug_Enabled == 'true':
      LF = open(myLogFile, 'a')
      LF.write("addDir: '" + name + "', '" + url + "', '" + iconimage + '\'\n')
      LF.close()

    return ok


def getParams():
  param = []
  paramstring = sys.argv[2]
  if len(paramstring) >= 2:
      params = sys.argv[2]
      cleanedparams = params.replace('?', '')
      if (params[len(params) - 1] == '/'):
	  params = params[0:len(params) - 2]
      pairsofparams = cleanedparams.split('&')
      param = {}
      for i in range(len(pairsofparams)):
	  splitparams = {}
	  splitparams = pairsofparams[i].split('=')
	  if (len(splitparams)) == 2:
	      param[splitparams[0]] = splitparams[1]
#-----------------------------------------------------------------------------------------------------------
#'url': 'http%3A%2F%2Fwww.digi-online.ro%2Ftv%2Frealitatea%2Btv%2F', 'name': 'Realitatea+TV'
#-----------------------------------------------------------------------------------------------------------
  if debug_Enabled == 'true':
    LF = open(myLogFile, 'a')
    LF.write("getParams: '" + str(param) + '\'\n')
    LF.close()
  return param


def makeCookie(name, value, domain):
    return cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )


def processLink(url):
    global myCookieJar
    global uloggedIN
    global sessionID
    f = HTMLParser.HTMLParser()
    url = f.unescape(url)

    if debug_Enabled == 'true':
      LF = open(myLogFile, 'a')
      LF.write("processLink parse URL: '" + url + '\'\n')

    if "www.digi-online.ro/tv/" in url:
      #myCookieJar.set_cookie(makeCookie("cookie_desclimer", "true", digiwebSite))
      #myCookieJar.set_cookie(makeCookie("_ga", "GA1.2.2001247683.1507822507", ".digi.online.ro"))
      #myCookieJar.set_cookie(makeCookie("_gid", "GA1.2.1402381958.1507822507", ".digi.online.ro"))
      #myCookieJar.set_cookie(makeCookie("_gat", "1", ".digi.online.ro"))
      myCookieJar.set_cookie(makeCookie("device_id", device_id, digiwebSite))
      urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(myCookieJar))
    else:
      urlopener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    ## LOGIN
    if login_Enabled == 'true' and "www.digi-online.ro/tv/" in url:
      urlopener.addheaders = [
	  ('Host', digiwebSite),
	  ('Accept', '*/*'),
	  ('Origin', digiURL),
	  ('X-Requested-With', 'XMLHttpRequest'),
	  ('User-Agent', userAgent),
	  ('Content-type', 'application/x-www-form-urlencoded'),
	  ('Referer', digiURL),
	  ('Accept-Encoding', 'identity'),
	  ('Accept-Language', 'en-ie'),
	  ('Connection', 'close')
	]

      logindata = urllib.urlencode({
	'user': login_User,
	'password': login_Password,
	'browser': browser,
	'model': deviceModel,
	'os': deviceOS
	  })

      try:
	httpPost = urlopener.open(loginURL, logindata)
	response = httpPost.read()

	if debug_Enabled == 'true':
	  LF.write("processLink HTTP POST: '" + loginURL + '\'\n')
	  LF.write("processLink HTTP/1.1 200 OK: '" + response + '\'\n')

	if str(response) == 'true':
	  uloggedIN = True
	  for cookie in myCookieJar:
	    #print cookie.name, cookie.value, cookie.domain #etc etc
	    if str(cookie.name) == 'sid':
	      sessionID = str(cookie.value)
	else:
	    xbmcgui.Dialog().ok('Login Error', response)

      except:
	  xbmcgui.Dialog().ok('HTTP POST Error', 'Could not access ' + str(loginURL))
	  errMsg1="processLink HTTP POST error '" + loginURL + '\'\n'
	  pass

      if debug_Enabled == 'true':
	LF.write(errMsg1)
	LF.write("processLink uloggedIN: '" + str(uloggedIN) + '\'\n')
	LF.write("processLink sessionID: '" + str(sessionID) + '\'\n')
    ## END LOGIN

    ## Load URL
    urlopener.addheaders = [
	  ('Host', digiwebSite),
	  ('Upgrade-Insecure-Requests', '1'),
	  ('User-Agent', userAgent),
	  ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
	  ('Referer', 'http://www.digi-online.ro/tv/'),
	  ('Accept-Encoding', 'identity'),
	  ('Accept-Language', 'en-ie'),
	  ('Connection', 'keep-alive')
        ]

    ## Load Page
    try:
	httpGet = urlopener.open(url)
        link = httpGet.read()

	## List cookies
	if debug_Enabled == 'true':
	  LF.write("processLink HTTP GET '" + url + '\'\n')
	  for cookie in (myCookieJar):
	    LF.write("processLink cookie: " + str(cookie) + '\n')
	  if http_log_Enable == 'true':
	    LF.write("processLink HTTP/1.1 200 OK: --- LINK --- ---" + '\n')
	    LF.write(link + '\n')
	    LF.write("processLink: --------- END LINK -----" + '\n')

        return link
    except:
        return False

    if debug_Enabled == 'true':
      LF.write('----------------------------' + '\n')
      LF.close()


def parseInput(url):
    global myCookieJar
    global httpURLopener
    result = None
    item = None
    infos = None
    match = None
    errMsg1 = ''

    ## if parsed URL is one of the hidden DIGI-Online/RDS programmes
    for prog in (hiddenProgrammes):
      if prog in url:
	result = url
	httpURLopener = urllib2.build_opener()
	match = [prog]

    if debug_Enabled == 'true':
	LF = open(myLogFile, 'a')
	LF.write("parseInput URL: '" + url + '\'\n')
	LF.write("parseInput hiddenProgrammes: '" + prog + '\'\n')

    if result is None:
      link = processLink(url)
      if epgInfo_Enabled == 'true':
	  getEPGdata(link)

      ## Case 1: "scope":"digi24" (www.digi24.ro)
      if "www.digi24.ro/live" in url:
	match = re.compile('"scope":"(.+?)"').findall(link)

      ## Case 2: data-balancer-scope-name="utv" (www.digi-online.ro)
      elif "www.digi-online.ro/tv/" in url:
	match = re.compile('data-balancer-scope-name="(.+?)"').findall(link)

      if len(match) > 0:
	  print match
      else:
	match = ['digi24']
	print match
	xbmcgui.Dialog().ok('Error', 'Could not access ' + url)
	errMsg1='\n' + "parseInput Error: Could not access '" + url + '\'\n'

    if "http://www.digi-online.ro/tv/digi+film/" in url:
      	xbmcgui.Dialog().ok('Error', 'DIGI FILM not yet implemented')

	ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
	httpURLopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(myCookieJar), urllib2.HTTPSHandler(context=ctx))
	httpURLopener.addheaders = [
	    ('Host', digiwebSite),
	    ('Accept', '*/*'),
	    ('Origin', digiURL),
	    ('User-Agent', userAgent),
	    ('Referer', url),
	    ('Accept-Encoding', 'identity'),
	    ('Accept-Language', 'en-GB,en;q=0.5'),
	    ('X-Requested-With', 'XMLHttpRequest'),
	    ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
	    ('Connection', 'close')
	  ]

	link = 'http://www.digi-online.ro/xhr-gen-stream.php'
	formdata = urllib.urlencode({'scope': 'digifilm'})
	httpGet = httpURLopener.open(link, formdata)
	response = httpGet.read()

	if debug_Enabled == 'true':
	  LF.write(errMsg1)
	  for cookie in (myCookieJar):
	    LF.write("parseInput cookie: " + str(cookie) + '\n')
	  LF.write("parseInput HTTP POST: '" + link + ' ' + formdata + '\'\n')
	  LF.write("parseInput HTTP/1.1 200 OK: '" + response + '\'\n')

	httpURLopener.addheaders = [
	    ('Host', 'digiapis.rcs-rds.ro'),
	    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
	    ('Origin', digiURL),
	    ('User-Agent', userAgent),
	    ('Referer', 'http://www.digi-online.ro/digifilm-player'),
	    ('Accept-Encoding', 'identity'),
	    ('Accept-Language', 'en-GB,en;q=0.5'),
	    ('Connection', 'close')
	  ]

	sslurl = 'https://digiapis.rcs-rds.ro/digionline/api/v11/streams_l.php?action=getStream&id_stream=7&quality=' + stream_Quality + '&id_device=' + device_id + '&platform=Browser&version_platform='+ deviceOS + '_' + browser + '_' + deviceModel + '&version_app=1.0.0&cd=0'

	#ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
	#response = urllib2.urlopen(sslurl, context=ctx)
	httpGet = httpURLopener.open(sslurl)
	mydata = httpGet.read()

	mydata = mydata.replace('\\', '')
	split = mydata.split(',')
	result = str(split[0])
	result = result.replace('"', '')
	result = result.replace('{stream_url:', '')

	if "http://" not in result:
	  result = "".join(("http:", result))

	if debug_Enabled == 'true':
	  LF.write(errMsg1)
	  LF.write("parseInput HTTPS GET: '" + sslurl + '\'\n')
	  LF.write("parseInput HTTPS OK (list): '" + mydata + '\'\n')
	  LF.write("parseInput result: '" + result + '\'\n')
	  LF.write("----------------------------"+'\n')

    elif result is None and match is not None:
      httpURLopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(myCookieJar))
      httpURLopener.addheaders = [
	  ('Host', digiMaster),
	  ('Accept', '*/*'),
	  ('Origin', digiURL),
	  ('User-Agent', userAgent),
	  ('Referer', url),
	  ('Accept-Encoding', 'identity'),
	  ('Accept-Language', 'en-GB,en;q=0.5'),
	  ('Connection', 'close')
	]

      httpGet = httpURLopener.open(keyMaster)
      myKey = httpGet.read()
      ## http://balancer.digi24.ro/streamer.php?&scope=digi24brasov&key=980cd632c5f0000df058486ff2df7e35&outputFormat=json&type=hls&quality=hq
      link = 'http://balancer.digi24.ro/streamer.php?&scope=' + match[0] + '&key=' + myKey + '&outputFormat=json&type=hls&quality=' + str(stream_Quality)

      if debug_Enabled == 'true':
	LF.write(errMsg1)
	LF.write("parseInput scope: '" + str(match) + '\'\n')
	LF.write("parseInput HTTP GET: '" + keyMaster + '\'\n')
	LF.write("parseInput HTTP/1.1 200 OK (key): '" + myKey + '\'\n')
	for cookie in (myCookieJar):
	  LF.write("processLink cookie: " + str(cookie) + '\n')

      if login_Enabled == 'true':
	slink = 'http://www.digi-online.ro/xhr-gen-stream.php'
	formdata = urllib.urlencode({'scope': match[0]})
	httpURLopener.addheaders = [
	    ('X-Requested-With', 'XMLHttpRequest')
	  ]
	httpGet = httpURLopener.open(slink, formdata)
	response = httpGet.read()

	if debug_Enabled == 'true':
	  LF.write("parseInput HTTP POST: '" + slink + ' ' + formdata +'\'\n')
	  LF.write("parseInput HTTP/1.1 200 OK: '" + response + '\'\n')

      try:
	file = httpURLopener.open(link).read()
	infos = json.loads(file)
	result = infos['file']

	if "http://" not in result:
	  result = "".join(("http:", result))

      except:
	xbmcgui.Dialog().ok('Error', 'Could not access ' + url)
	errMsg1="parseInput: Could not access '" + url + '\'\n'

      if debug_Enabled == 'true':
	LF.write(errMsg1)
	LF.write("parseInput HTTP GET: '" + link + '\'\n')
	LF.write("parseInput HTTP/1.1 200 OK (json): '" + str(infos) + '\'\n')
	LF.write("parseInput result: '" + result + '\'\n')
	LF.write("----------------------------"+'\n')

    ## Build ListItem
    if result is not None:
      try:
	item = xbmcgui.ListItem(path=result, iconImage=addon_thumb, thumbnailImage=nowPlayingThumb)
	itemInfo = {
	  'type': 'Video',
	  'genre': 'Live Stream',
	  'title': nowPlayingTitle,
	  'playcount': '0'
	}
	item.setInfo('video', itemInfo)
      except:
	xbmcgui.Dialog().ok('Error', 'Could not access media')
	errMsg1="parseInput: Could not access '" + result + '\'\n'

    ## Play stream
    if item is not None and result is not None:
      if debug_Enabled == 'true':
	LF.write(errMsg1)
	LF.write("xbmc.Player().play(" + result + "," + str(item) + ")" + '\n')

      xbmcplugin.setContent(int(sys.argv[1]), 'movies')
      #xbmc.Player().play(result)
      xbmc.Player().play(result, item)

      if epgInfo_Enabled == 'true':
	if infoEPGnowP == '':
	  xbmc.executebuiltin("Notification(Digi-Online, " + nowPlayingTitle + ")")
	else:
	  xbmc.executebuiltin("Notification(" + infoEPGnowP + ", " + '\n\n' + infoEPGnext + ")")
      elif osdInfo_Enabled == 'true':
	xbmc.executebuiltin("Notification(Digi-Online, " + nowPlayingTitle + ")")

    if debug_Enabled == 'true':
      LF.write(errMsg1)
      savePlayList(result)
      LF.close()


def savePlayList(url):
      global httpURLopener
      PF = open(myPlayFile, 'w+')

      if "http://" not in url:
	url = "".join(("http:", url))

      if debug_Enabled == 'true':
	LF = open(myLogFile, 'a')
	LF.write("savePlayList URL: '" + url + '\'\n')

      if "index.m3u8" in url:
	url = removeSubstr(url, 'index.m3u8')
	response = httpURLopener.open(url)
	mydata = response.read()
	if debug_Enabled == 'true':
	  LF.write("savePlayList HTTP GET: '" + url + '\'\n')
	  LF.write("savePlayList HTTP/1.1 200 OK: \n" + mydata + '\n')
	PF.write(re.sub('([_A-Za-z0-9.]+).m3u8', '', mydata) + '\n')

	if ".m3u8" in mydata:
	  variant = str((re.compile('(.+?.m3u8)').findall(mydata))[0])
	  origin = url.replace('index.m3u8', '')
	  playlist = origin + variant
	  response = httpURLopener.open(playlist)
	  mydata = response.read()

	  if debug_Enabled == 'true':
	    LF.write("savePlayList HTTP GET: '" + playlist + '\'\n')
	    LF.write("savePlayList HTTP/1.1 200 OK: \n" + mydata + '\n')

	  mydata = mydata.replace('#EXTM3U', '')
	  mydata = mydata.replace('#EXT-X-VERSION:3', '')
	  for line in mydata.split('\n'):
	    if ".ts" in line:
	      nline = origin + line
	      mydata = mydata.replace(line, nline)

	  PF.write(mydata + '\n')
	PF.close

      if debug_Enabled == 'true':
	LF.write('----------------------------' + '\n')
	LF.close()


def getEPGdata(link):
  global infoEPGnowP
  global infoEPGnext

  if '<div class="info" epg-data=' in link:
    cruft = ["[", "]", "'", "{", "}", "start:", "stop:", "title:"]
    myEPGInfo = str(re.compile('<div class="info" epg-data="(.+?)"').findall(link)).replace("&quot;", "")
    for i in range(len(cruft)):
	myEPGInfo = myEPGInfo.replace(str(cruft[i]), "")
    if len(myEPGInfo) > 0:
      try:
	epgscrape = myEPGInfo.split(',')
	infoEPGnowP = str(epgscrape[0]) + '\n' + time.strftime("%H:%M", time.localtime(int(epgscrape[1]))) + " - " + time.strftime("%H:%M", time.localtime(int(epgscrape[2])))
	infoEPGnext = str(epgscrape[3]) + '\n' + time.strftime("%H:%M", time.localtime(int(epgscrape[4]))) + " - " + time.strftime("%H:%M", time.localtime(int(epgscrape[5])))
      except:
	pass

      if debug_Enabled == 'true':
	  LF = open(myLogFile, 'a')
	  LF.write('----------------------------' + '\n')
	  LF.write("getEPGdata infoEPGnowP: '" + infoEPGnowP.replace("\n", " ") + '\'\n')
	  LF.write("getEPGdata infoEPGnext: '" + infoEPGnext.replace("\n", " ") + '\'\n')
	  LF.write('----------------------------' + '\n')
	  LF.close()


#### RUN Addon ###
params = getParams()
url = None
nowPlayingThumb = None
nowPlayingTitle = None
httpURLopener = None
myCookieJar = cookielib.CookieJar()
uloggedIN = False;
sessionID = ''
infoEPGnowP = ''
infoEPGnext = ''

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass

try:
  nowPlayingTitle = urllib.unquote_plus(params["name"])
except:
  nowPlayingTitle = str(url)

try:
  nowPlayingThumb = urllib.unquote_plus(params["thumb"])
except:
  nowPlayingThumb = movies_thumb

if debug_Enabled == 'true':
    log_MyVars()

if url is None or len(url) < 1:
  ROOT()
else:
  parseInput(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

####################################################################################################

