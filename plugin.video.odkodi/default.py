# -*- coding: utf-8 -*-

'''
    Template Add-on
    Copyright (C) 2016 Demo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, xbmcaddon
try:
    import json
except:
    import simplejson as json
ADDON_PATH = xbmc.translatePath('special://home/addons/plugin.video.odkodi/')
source_movies = ADDON_PATH + 'movies.txt'
source_series = ADDON_PATH + 'series.txt'
source_music = ADDON_PATH + 'music.txt'
source_ro = ADDON_PATH + 'ro.txt'
ICON = ADDON_PATH + 'icon.png'
FANART = ADDON_PATH + 'fanart.jpg'
PATH = 'Open Directories'
VERSION = '0.0.3'
Dialog = xbmcgui.Dialog()
addon_id = 'plugin.video.odkodi'
ADDON = xbmcaddon.Addon(id=addon_id)
movie_favourites = ADDON_PATH + 'movie_favourites.txt'
tv_favourites = ADDON_PATH + 'tv_favourites.txt'
music_favourites = ADDON_PATH + 'music_favourites.txt'
ro_favourites = ADDON_PATH + 'ro_favourites.txt'
movie_favourites_read = open(movie_favourites).read()
music_favourites_read = open(music_favourites).read()
tv_favourites_read = open(tv_favourites).read()
ro_favourites_read = open(ro_favourites).read()
imdb = 'http://www.imdb.com'
List = []
import os, shutil, xbmcgui
Dialog = xbmcgui.Dialog()
addons = xbmc.translatePath('special://home/addons/')
ADDON = xbmcaddon.Addon(id=addon_id)


def Main_Menu():
    Menu('Favourites','',5,ICON,FANART,'','','')
    Menu('Movies','',7,ICON,FANART,'','','')
    Menu('Tv Series','',8,ICON,FANART,'','','')
    Menu('Music','',9,ICON,FANART,'','','')
    Menu('Romanesti','',13,ICON,FANART,'','','')
    Menu('WebCrunch','',15,ICON,FANART,'','','')
#    Menu('Search','',6,ICON,FANART,'','','')


##################LIST OF INDEX'S########################

def Movies():
    OPEN = open(source_movies).read()
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url,name in Regex:
        Menu(name,url,1,ICON,FANART,'','','')
    else:
        Menu('[COLORred]Press here to add a source url[/COLOR]','',2,'',ICON,FANART,'','')

def Tv_Series():
    OPEN = open(source_series).read()
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url,name in Regex:
        Menu(name,url,1,ICON,FANART,'','','')
    else:
        Menu('[COLORred]Press here to add a source url[/COLOR]','',11,'',ICON,FANART,'','')			

def Music():
    OPEN = open(source_music).read()
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url,name in Regex:
        Menu(name,url,1,ICON,FANART,'','','')
    else:
        Menu('[COLORred]Press here to add a source url[/COLOR]','',12,'',ICON,FANART,'','')
		
def Ro():
    OPEN = open(source_ro).read()
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url,name in Regex:
        Menu(name,url,1,ICON,FANART,'','','')
    else:
        Menu('[COLORred]Press here to add a source url[/COLOR]','',14,'',ICON,FANART,'','')
		
def Online():
    url = 'https://raw.githubusercontent.com/HerbL27/FileMasta/master/API/open-directories.txt'
    HTML = Open_Url(url)
    match = re.compile('(http.+?)\n').findall(HTML)
    for url in match:
        name = url
        if 'book' in url:
            pass
        elif 'apk' in url:
            pass
        else:
            Menu(name,url,1,ICON,FANART,'','','')
		
#######################SEARCH########################
'''
def Search():
    Search_Name = Dialog.input('Search', type=xbmcgui.INPUT_ALPHANUM)
    OPEN = open(source_file).read()
    Regex = re.compile('url="(.+?)">name="(.+?)"').findall(OPEN)
    for url in Regex:
        Search_Loop('http://sv.dl-pars.in/')
    if Search_Name in name:
        Menu(name,url_search,1,ICON,FANART,'','')
    

def Search_Loop(url):
    HTML = Open_Url(url)
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(HTML)
    for url2,name in match:
        url3 = url + url2
        if '..' in url3:
            pass
        elif 'rar' in url3:
            pass
        elif 'srt' in url3:
            pass
        elif 'C=' in url2:
            pass
        elif '/' in url2:
            name = name
            url_search = url3
            Search_Loop(url)
        else:
            name = name
            url_search = url3
'''
#################################FAVOURITES#################################

def Write_Favourite(name,url,choice,mode):
    if choice == 1:
        favourite_file = movie_favourites
    elif choice == 2:
        favourite_file = tv_favourites
    elif choice == 3:
        favourite_file = music_favourites
    elif choice == 4:
        favourite_file = ro_favourites
    print_text_file = open(favourite_file,"a")
    print_text_file.write('url="'+str(url)+'">name="'+str(name)+'"'+'>mode="'+str(mode)+'"<END>\n')
    print_text_file.close

def Read_Favourite(name,url,choice,mode):
    if choice == 1:
        favourite_file = movie_favourites
    elif choice == 2:
        favourite_file = tv_favourites
    elif choice == 3:
        favourite_file = music_favourites
    elif choice == 4:
        favourite_file = ro_favourites
    Fav = open(favourite_file).read()
    Fav_Regex = re.compile('url="(.+?)">name="(.+?)">mode="(.+?)"<END>').findall(Fav)
    for url,name,mode in Fav_Regex:
        if mode == '1':
            Menu(name,url,mode,ICON,FANART,'','','')
        elif mode == '10':
            Play(name,url,mode,ICON,FANART,'','','')
    else:
        Menu('[COLORred]If empty you need to add Favourites![/COLOR]','','','','','','','')
        Menu('By bringing up context menu then adding to favourites','','','','','','','')
        Menu('[COLORblue]Press C/Menu/Right click to bring up context menu[/COLOR]','','','','','','','')
            
	
def Favourites_menu():
    Menu('Favourite Movies','',4,ICON,FANART,'','',1)
    Menu('Favourite Tv Shows','',4,ICON,FANART,'','',2)
    Menu('Favourite Music','',4,ICON,FANART,'','',3)
    Menu('Favourite Romanesti','',4,ICON,FANART,'','',4)
	

    		

#####################################MAIN REGEX LOOP ###############################
		
def Main_Loop(url):
    HTML = Open_Url(url)
    match = re.compile('<a href="(.+?)">(.+?)</a>').findall(HTML)
    for url2,name in match:
        url3 = url + url2
        search_name = name
        if '..' in url3:
            pass
        elif 'rar' in url3:
            pass
        elif 'ini' in url3:
            pass
        elif 'css' in url3:
            pass
        elif 'zip' in url3:
            pass
        elif 'doc' in url3:
            pass
        elif 'pdf' in url3:
            pass
        elif 'png' in url3:
            pass
        elif 'Parent Directory' in name:
            pass
        elif 'img src' in name:
            pass
        elif 'srt' in url3:
            pass
        elif 'txt' in url3:
            pass
        elif 'jpg' in url3:
            pass
        elif 'metathumb' in url3:
            pass
        elif 'xml' in url3:
            pass
        elif 'nfo' in url3:
            pass
        elif 'exe' in url3:
            pass
        elif 'C=' in url2:
            pass
        elif '/' in url2:
            Menu((name).replace('/',''),url3,1,ICON,FANART,'','','')
        elif ADDON.getSetting('Data')=='true':
            Imdb_Scrape(url3,name,search_name)
        else:
            Play(name,url3,10,ICON,FANART,'','','')

#######################IMDB GRAB#####################

def Imdb_Scrape(url3,name,search_name):
    url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q=' + (search_name).replace(' ','+') + '&s=all'
    HTML = Open_Url(url)
    match = re.compile('<table class="findList">.+?<tr class="findResult odd">.+?<a href="(.+?)" >',re.DOTALL).findall(HTML)
    for url in match:
        if 'title' in url:
            Pass_It = 'Pass' + name
            if not Pass_It in List:
                IMAGE = ''
                BACKGROUND=''
                DESCRIPTION=''
                final_url = imdb + url
                Final_Page = Open_Url(final_url)
                Image = re.compile('<div class="poster">.+?src="(.+?)"',re.DOTALL).findall(Final_Page)
                for image in Image:
                    IMAGE = image
                Description = re.compile('<div class="summary_text" itemprop="description">(.+?)</div>',re.DOTALL).findall(Final_Page)
                for desc in Description:
                    DESCRIPTION = (desc).replace('\n','').replace('  ','')
                Background = re.compile('<div class="mediastrip">.+?loadlate="(.+?)"',re.DOTALL).findall(Final_Page)
                for background in Background:
                    BACKGROUND = (background).replace('UY105_CR20,0,105,105','SY1000_CR0,0,1563,1000')
                Play(name,url3,10,IMAGE,BACKGROUND,DESCRIPTION,'','')
                List.append(Pass_It)
                setView('movies', 'INFO')
            else:
                pass
				
#    else:
 #       Play(clean_name,url3,10,ICON,FANART,'','','')
						
#######################################SOURCE FILE EDITOR################################################

def Source_Movie():
    Dialog.ok('Add Source',"Enter site url next","Then a name on second window","Close and reopen addon after to see changes")
    url = Dialog.input('ENTER SITE URL', type=xbmcgui.INPUT_ALPHANUM)
    name = Dialog.input('ENTER A MEMORABLE NAME FOR SITE', type=xbmcgui.INPUT_ALPHANUM)
    print_text_file = open(source_movies,"a")
    print_text_file.write('url="'+url+'">name="'+name+'"'+'\n')
    Dialog.ok('Added',"Press OK then go back","For changes to take effect")
	
def Source_Series():
    Dialog.ok('Add Source',"Enter site url next","Then a name on second window","Close and reopen addon after to see changes")
    url = Dialog.input('ENTER SITE URL', type=xbmcgui.INPUT_ALPHANUM)
    name = Dialog.input('ENTER A MEMORABLE NAME FOR SITE', type=xbmcgui.INPUT_ALPHANUM)
    print_text_file = open(source_series,"a")
    print_text_file.write('url="'+url+'">name="'+name+'"'+'\n')
    Dialog.ok('Added',"Press OK then go back","For changes to take effect")
	
def Source_Music():
    Dialog.ok('Add Source',"Enter site url next","Then a name on second window","Close and reopen addon after to see changes")
    url = Dialog.input('ENTER SITE URL', type=xbmcgui.INPUT_ALPHANUM)
    name = Dialog.input('ENTER A MEMORABLE NAME FOR SITE', type=xbmcgui.INPUT_ALPHANUM)
    print_text_file = open(source_music,"a")
    print_text_file.write('url="'+url+'">name="'+name+'"'+'\n')
    Dialog.ok('Added',"Press OK then go back","For changes to take effect")

def Source_Ro():
    Dialog.ok('Add Source',"Enter site url next","Then a name on second window","Close and reopen addon after to see changes")
    url = Dialog.input('ENTER SITE URL', type=xbmcgui.INPUT_ALPHANUM)
    name = Dialog.input('ENTER A MEMORABLE NAME FOR SITE', type=xbmcgui.INPUT_ALPHANUM)
    print_text_file = open(source_ro,"a")
    print_text_file.write('url="'+url+'">name="'+name+'"'+'\n')
    Dialog.ok('Added',"Press OK then go back","For changes to take effect")

			
####################################################################PROCESSES###################################################
def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try: 
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def setView(content, viewType):
	if content:
	    xbmcplugin.setContent(int(sys.argv[1]), content)
		
		
def Menu(name,url,mode,iconimage,fanart,description,trailer,choice,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&trailer="+urllib.quote_plus(trailer)+"&choice="+str(choice)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty("IsPlayable","true")
        if showcontext:
            contextMenu = []
            if not name in movie_favourites_read:
                contextMenu.append(('Add to Index Movie_Favourites','XBMC.RunPlugin(%s?choice=1&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            if not name in tv_favourites_read:
                contextMenu.append(('Add to Index TV_Favorites','XBMC.RunPlugin(%s?choice=2&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            if not name in music_favourites_read:
                contextMenu.append(('Add to Index Music_Favorites','XBMC.RunPlugin(%s?choice=3&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))	
            if not name in ro_favourites_read:
                contextMenu.append(('Add to Index Ro_Favorites','XBMC.RunPlugin(%s?choice=4&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))						 
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

		
def Play(name,url,mode,iconimage,fanart,description,trailer,choice,showcontext=True,allinfo={}):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&trailer="+urllib.quote_plus(trailer)+"&choice="+str(choice)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty("IsPlayable","true")
        if showcontext:
            contextMenu = []
            if not name in movie_favourites_read:
                contextMenu.append(('Add to Index Movie_Favourites','XBMC.RunPlugin(%s?choice=1&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            if not name in tv_favourites_read:
                contextMenu.append(('Add to Index TV_Favorites','XBMC.RunPlugin(%s?choice=2&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))
            if not name in music_favourites_read:
                contextMenu.append(('Add to Index Music_Favorites','XBMC.RunPlugin(%s?choice=3&mode=3&name=%s&url=%s&iconimage=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), mode)))				
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
		
def GetPlayerCore(): 
    try: 
        PlayerMethod=getSet("core-player") 
        if   (PlayerMethod=='DVDPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_DVDPLAYER 
        elif (PlayerMethod=='MPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_MPLAYER 
        elif (PlayerMethod=='PAPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_PAPLAYER 
        else: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    except: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    return PlayerMeth 
    return True 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
		
'''
def resolve(url): 
    play=xbmc.Player()
    import urlresolver
    try: play.play(url)
    except: pass
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
'''

def resolve(url):
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None
trailer=None
fav_mode=None
choice=None

try:
    choice=int(params["choice"])
except:
    pass

try:
    fav_mode=int(params["fav_mode"])
except:
    pass

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        trailer=urllib.unquote_plus(params["trailer"])
except:
        pass

        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
print "Trailer: "+str(trailer)

#####################################################END PROCESSES##############################################################		
		
if mode == None: Main_Menu()
elif mode == 1 : Main_Loop(url)
elif mode == 2 : Source_Movie()
elif mode == 11 : Source_Series()
elif mode == 12 : Source_Music()
elif mode == 14 : Source_Ro()
elif mode == 3 : Write_Favourite(name,url,choice,fav_mode)
elif mode == 4 : Read_Favourite(name,url,choice,fav_mode)
elif mode == 5 : Favourites_menu()
#elif mode == 6 : Search()
elif mode == 7 : Movies()
elif mode == 8 : Tv_Series()
elif mode == 9 : Music()
elif mode == 13 : Ro()
elif mode == 15 : Online()
elif mode == 10: resolve(url)

		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
