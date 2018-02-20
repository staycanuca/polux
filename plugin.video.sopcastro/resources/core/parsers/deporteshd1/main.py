# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of sopcastro addon

DHD1

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

parserName = "deporteshd1"
base_url = "http://deporteshd1.blogspot.com"

def module_tree(name,url,iconimage,mode,parser,parserfunction):
    if not parserfunction: deporteshd1_menu()
    elif parserfunction == "resolve_and_play": deporteshd1_streams(name,url)


def deporteshd1_menu():
    try:
        source = get_page_source(base_url)
    except:
        xbmcgui.Dialog().ok(translate(40000),translate(40128))
        return

    category = re.findall("<li data-role='dropdown'><a href='#'>(AV.+?)</a><ul>(.+?)</ul>", source, re.MULTILINE | re.DOTALL)
    for categoryName, categoryLinks in category:

        linksMatch = re.findall("<li><a href='(http://deporteshd1.blogspot.com/p/.+?)'>(.+?)</a></li>", categoryLinks.replace('&#9312;', '1').replace('&#9313;', '2').replace('&#9314;', '3').replace('&#9315;', '4').replace('&#9316;', '5').replace('&#9317;', '6').replace('&#9318;', '7').replace('&#9319;', '8').replace('&#9320;', '9').replace('&#9321;', '10').replace('&#9322;', '11').replace('&#9323;', '12').replace('&#9324;', '13').replace('&#9325;', '14').replace('&#9326;', '15').replace('&#9327;', '16').replace('&#9328;', '17').replace('&#9329;', '18').replace('&#9330;', '19').replace('&#9331;', '20'))
        if linksMatch:
            addLink("[B][COLOR orange]{0}[/COLOR][/B]".format(categoryName), '', os.path.join(current_dir,'icon.png'))
            for linkUrl, linkName in linksMatch:
                addDir("[B]{0}[/B]".format(linkName), linkUrl, 401, os.path.join(current_dir,"icon.png"), 1, False, parser=parserName, parserfunction="resolve_and_play")


def deporteshd1_streams(name, url):
    try:
        source = get_page_source(url)
    except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))

    if source:
        aceHash = re.search('<a href="acestream://(.+?)"', source.replace('\n', ''))
        if aceHash:
            ace.acestreams(name, os.path.join(current_dir,'icon.png'), aceHash.group(1))
