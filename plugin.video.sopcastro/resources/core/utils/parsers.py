# -*- coding: utf-8 -*-

""" sopcastro  (c)  2014 enen92 fightnight

    This file contains parser utilities

    Functions:

    parser_resolver(name,url,icon) -> Process an URL to reproduce Sopcast or AceStream content

"""

import requests
import acestream as ace
import sopcast as sop
from utils.pluginxbmc import *
from utils.webutils import *

def play_stream_url(name, icon, url):
    if "sop://" in url: sop.sopstreams(name,icon,url)
    else: ace.acestreams(name,icon,url)

def parser_resolver(name,url,icon,depth=0):
    if "sop://" not in url and "acestream://" not in url:
        if "http://" not in url:
            url = "http://" + url

        try:
            if 'arenavision' in url or 'elgoles.net' in url:
                headers = { "Cookie" : "beget=begetok; has_js=1;" }
                source = requests.get(url, headers = headers).text
            else:
                source = get_page_source(url)
        except:
            xbmcgui.Dialog().ok(translate(40000), translate(40128))
            return None

        patternList = ['(sop://[^ "\'<]+)',                   # Sopcast
                       '(?:acestream://|this.loadPlayer\(["\'])([^"\']+)["\']', # AceStream
                       '<i?frame[^>]+src=["\']([^>]+?)["\']' # iframes
                      ]

        allPatterns = "|".join(patternList)

        matchs = re.findall(allPatterns, source, re.IGNORECASE)
        iframes = []
        streams = []

        for match in matchs:
            if match[0]:
                if not match[0] in streams:
                    streams.append(match[0])
            elif match[1]:
                if not match[1] in streams:
                    streams.append(match[1])
            else:
                iframes.append(match[2])

        if len(streams) > 0:
            urlToPlay = None
            if len(streams) > 1:
                index = xbmcgui.Dialog().select(translate(40021), streams)
                if index > -1: urlToPlay = streams[index]
            else:
                urlToPlay = streams[0]

            if urlToPlay:
                play_stream_url(name, icon, urlToPlay)

            return urlToPlay


        for iframe in iframes:
            redirect_url = iframe if '/' in iframe else url + '/' + iframe
            if depth < 2:
                found = parser_resolver(name,redirect_url,icon,depth+1)
                if found: return found

        if depth == 0:
            xbmcgui.Dialog().ok(translate(40000),translate(40022))

        return None

    else: play_stream_url(name,icon,url)

    return url

# http://stackoverflow.com/a/14173535/1344260
def russianTransliterate(string):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

    tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )

    return string.decode("utf-8").translate(tr)
