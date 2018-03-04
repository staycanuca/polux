# -*- coding: utf-8 -*-

''' Copyright (c) 2017 Mario Bălănică
    
    This file contains all the functions for the 'Channels lists' folder.
    
    Functions:
    lists_menu() -> Shows the lists.
    addlist() -> Add a new list. It'll ask for local or remote and processes the given input.
    remove_list(name) -> Remove a list.
    list_type(url) -> Detects the type of the file in order to parse it correctly.
    parse_m3u(url) -> Parse a M3U playlist.
    parse_tvlist(url) -> Parse a TVL playlist.
    SopXML_get_groups(url) -> Display categories of a SopCast XML list.
    SopXML_get_channels(name,url) -> Display channels of a SopCast XML list based on the selected category.
    get_list_informations(url) -> Display informations about a TVList file.
    selection_dialog(name,url) -> Display a selection dialog (replaces the context menu) with 'remove_list(name)' and 'get_list_informations(url)' functions.
    
'''

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,datetime,os,xbmcvfs,sys
from utils.pluginxbmc import *
from utils.webutils import *
from utils.directoryhandle import *
from utils.iofile import *

def lists_menu():
    try:
        if os.path.exists(os.path.join(addonprofile,'Lists')):
            dirs, files = xbmcvfs.listdir(os.path.join(addonprofile,'Lists'))
            for file in files:
                f = open(os.path.join(addonprofile,'Lists',file), 'r')
                string = f.read()
                if xbmcvfs.exists(os.path.join(addonprofile,'Lists-fanart',file.replace('.txt','.jpg'))):
                    addDir('[B][COLOR orange]' + file.replace('.txt','') + '[/B][/COLOR]',string,101,os.path.join(addonpath,art,channelslists_menu_itemPNG),2,True,fan_art=os.path.join(addonprofile,'Lists-fanart',
                            file.replace('.txt','.jpg')))
                else: addDir('[B][COLOR orange]' + file.replace('.txt','') + '[/B][/COLOR]',string,101,os.path.join(addonpath,art,channelslists_menu_itemPNG),2,True)
    except: pass
    addDir('[B][COLOR=green]'+translate(30171)+'[/COLOR][/B]',MainURL,103,os.path.join(addonpath,art,plus_menuPNG),2,False)

def addlist():
    YNDialog = xbmcgui.Dialog().yesno(translate(30000), translate(30172),'','',translate(30173),translate(30174))
    if YNDialog:
        dialog = xbmcgui.Dialog()
        lista_xml = dialog.browse(1, translate(30175), 'files','.tvl|.m3u|.xml')
        xbmcKey = xbmc.Keyboard('', translate(30176))
        xbmcKey.doModal()
        if (xbmcKey.isConfirmed()):
            searchname = xbmcKey.getText()
            if searchname=='': sys.exit(0)
            encode=urllib.quote(searchname)
            if xbmcvfs.exists(os.path.join(addonprofile,'Lists')): pass
            else: xbmcvfs.mkdir(os.path.join(addonprofile,'Lists'))
            txt_name = searchname + '.txt'
            save(os.path.join(addonprofile,'Lists',txt_name),lista_xml)
            messageok(translate(30000),translate(30177))
            xbmc.executebuiltin('XBMC.Container.Refresh')
    else:
        keyb = xbmc.Keyboard('', translate(30178))
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            if 'dropbox' in search and not '?dl=1' in search: search = search + '?dl=1'
            if 'tvl' not in search.split('.')[-1] and 'xml' not in search.split('.')[-1] and 'm3u' not in search.split('.')[-1]:
                messageok(translate(30000),translate(30011)); sys.exit(0)
            else:
                try:
                    code = get_page_source(search)
                except:
                    messageok(translate(30000),translate(30011))
                    sys.exit(0)
            xbmcKey = xbmc.Keyboard('', translate(30176))
            xbmcKey.doModal()
            if (xbmcKey.isConfirmed()):
                searchname = xbmcKey.getText()
                if searchname=='': sys.exit(0)
                encode=urllib.quote(searchname)
                if os.path.exists(os.path.join(addonprofile,'Lists')): pass
                else: xbmcvfs.mkdir(os.path.join(addonprofile,'Lists'))
                txt_name = searchname + '.txt'
                save(os.path.join(addonprofile,'Lists',txt_name),search)
                messageok(translate(30000),translate(30177))
                xbmc.executebuiltin('XBMC.Container.Refresh')

def remove_list(name):
    xbmcvfs.delete(name)
    notifi(translate(30000),translate(30179))
    xbmc.executebuiltin('Container.Refresh')

def list_type(url):
    ltype = url.split('.')[-1]
    if 'tvl' in ltype: parse_tvlist(url)
    elif 'm3u' in ltype: parse_m3u(url)
    elif 'xml' in ltype: SopXML_get_groups(url)
    else: pass

def parse_m3u(url):
    try:
        if url.startswith('http://') or url.startswith('https://'): content = get_page_source(url)
        else: content = readfile(url)
        match = re.compile('#EXTINF:.+?,(.*?)\n(.*?)(?:\r|\n)').findall(content)
        for channel_name,stream_url in match:
            if 'plugin://' in stream_url:
                stream_url = 'XBMC.RunPlugin('+stream_url+')'
                addDir(channel_name,stream_url,104,'',1,False)
            elif 'sop://' in stream_url:
                addDir(channel_name,stream_url,2,'',1,False)
            elif ('acestream://' in stream_url) or ('.acelive' in stream_url) or ('.torrent' in stream_url):
                addDir(channel_name,stream_url,1,'',1,False)
            elif ('http://' in stream_url) or ('https://' in stream_url) or ('rtmp://' in stream_url) or ('rtsp://' in stream_url) or ('mmsh://' in stream_url):
                addDir(channel_name,stream_url,15,'',1,False)
            else: addLink(channel_name,stream_url,'')
    except:
        notifi(translate(30000),translate(30181))
        lists_menu()

def parse_tvlist(url):
    try:
        from xml.etree import ElementTree
        if url.startswith('http://') or url.startswith('https://'):
            source = get_page_source(url)
        else:
            source = readfile(url)
        save(os.path.join(addonprofile,'temp_chlist.tvl'),source)
        chlist_tree = ElementTree.parse(os.path.join(addonprofile,'temp_chlist.tvl'))
        channels = ElementTree.parse(os.path.join(addonprofile,'temp_chlist.tvl')).findall('.//channel')
        for channel in channels:
            channels = channel.findall('.//channel')
            try:
                title = channel.find('.//name').text
                channelurl = channel.find('.//url').text
            except:
                messageok(translate(30000), translate(30193))
            try: thumbnail = channel.find('.//thumbnail').text
            except: pass
            if channelurl:
                try: addDir_livestreams_common('[B][COLOR orange]' + title + ' [/B][/COLOR]',channelurl,15,thumbnail,False)
                except:
                    messageok(translate(30000), translate(30193))
                    pass
    except:
        notifi(translate(30000),translate(30181))
        lists_menu()

def get_list_informations(url):
    from xml.etree import ElementTree
    try:
        if url.startswith('http://') or url.startswith('https://'):
            request = urllib2.Request(url, headers={'Accept' : 'application/xml'})
            addr = urllib2.urlopen(request)
            tree = ElementTree.parse(addr)
        else:
            tree = ElementTree.parse(url)
        root = tree.getroot()
        ltype = url.split('.')[-1]
        if 'tvl' in ltype: list_type = 'TVList'
        infos = ['[COLOR blue]' + translate(30188) + '[/COLOR]' + root.attrib['name'],
                    '[COLOR blue]' + translate(30189) + '[/COLOR]' + root.attrib['author'],
                      '[COLOR blue]' + translate(30190) + '[/COLOR]' + root.attrib['language'],
                        '[COLOR blue]' + translate(30192) + '[/COLOR]' + list_type,
                            '[COLOR blue]' + translate(30191) + '[/COLOR]' + root.attrib['version']]
        dialogInfo = xbmcgui.Dialog().select(translate(30000), infos)
        if dialogInfo == 0 or dialogInfo == 1 or dialogInfo == 2 or dialogInfo == 3 or dialogInfo == 4:
            get_list_informations(url)
    except:
        messageok(translate(30000), translate(30187))

def SopXML_get_groups(url):
    from xml.etree import ElementTree
    try:
        if url.startswith('http://') or url.startswith('https://'):
            source = get_page_source(url)
            save(os.path.join(addonprofile,'temp_sop.xml'),source)
            workingxml = os.path.join(addonprofile,'temp_sop.xml')
        else:
            workingxml = url
        groups = ElementTree.parse(workingxml).findall('.//group')
        unname_group_index = 1
        LANGUAGE = 'en'
        for group in groups:
            if group.attrib[LANGUAGE] == '':
                group.attrib[LANGUAGE] = str(unname_group_index)
                unname_group_index = unname_group_index + 1
                if re.sub('c','e',LANGUAGE) == LANGUAGE:
                    OTHER_LANG = re.sub('e','c',LANGUAGE)
                else:
                    OTHER_LANG = re.sub('c','e',LANGUAGE)
                if LANGUAGE == 'cn':
                    try:
                        if len(group.attrib[OTHER_LANG]) > 0:
                            group.attrib[LANGUAGE] = group.attrib[OTHER_LANG]
                            unname_group_index = unname_group_index - 1
                    except:
                        pass
            if (group.find('.//channel')==None): continue
            group_name=group.attrib[LANGUAGE]
            try:
                addDir_livestreams_common(group_name,url,107,os.path.join(addonpath,art,sopcast_menu_itemPNG),True)
            except: pass
    except:
        notifi(translate(30000),translate(30181))
        lists_menu()

def SopXML_get_channels(name,url):
    from xml.etree import ElementTree
    if url.startswith('http://') or url.startswith('https://'):
        source = get_page_source(url)
    else:
        source = readfile(url)
    save(os.path.join(addonprofile,'temp_sop.xml'),source)
    chlist_tree = ElementTree.parse(os.path.join(addonprofile,'temp_sop.xml'))
    LANGUAGE = 'en'
    groups = ElementTree.parse(os.path.join(addonprofile,'temp_sop.xml')).findall('.//group')
    for group in groups:
        if group.attrib[LANGUAGE].encode('utf-8') == name:
            channels = group.findall('.//channel')
            for channel in channels:
                try:
                    try:
                        title = channel.find('.//name').attrib['en'].encode('utf-8')
                    except: title = ''
                    if not title: 
                        try: title = channel.find('.//name').attrib['cn'].encode('utf-8')
                        except: title = ''
                    if not title:
                        try: title = channel.find('.//name').text
                        except: title = ''
                    ch_type = channel.find('.//stream_type').text
                    sop_address = channel.find('.//item').text
                    if not ch_type: ch_type = 'N/A'
                    if not title: title = 'N/A'
                    thumbnail = ''
                    try:
                        thumbnail = channel.find('.//thumbnail').text
                    except: pass
                    if sop_address:
                        if thumbnail == "": thumbnail = os.path.join(addonpath,art,sopcast_menu_itemPNG)
                        try: addDir_livestreams_common('[B][COLOR orange]' + title + ' [/B][/COLOR](' + ch_type +')',sop_address,2,thumbnail,False)
                        except:pass
                    else: pass
                except: pass
        else: pass

def selection_dialog(name,url):
    modeselect = ['[COLOR blue]' + translate(30186) + '[/COLOR]', '[COLOR red]' + translate(30025) + '[/COLOR]']
    dialogSelection = xbmcgui.Dialog()
    selection = dialogSelection.select(translate(30185), modeselect)
    if selection == 0:
        get_list_informations(url)
    elif selection == 1:
        remove_list(name)
