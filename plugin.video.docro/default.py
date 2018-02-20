# -*- coding: utf-8 -*-
#------------------------------------------------------------
#polux Kodi Addon
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.docro'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

canal1 = xbmcaddon.Addon().getSetting('canal1')
canal1n = xbmcaddon.Addon().getSetting('canal1n')
canal2 = xbmcaddon.Addon().getSetting('canal2')
canal2n = xbmcaddon.Addon().getSetting('canal2n')
canal3 = xbmcaddon.Addon().getSetting('canal3')
canal3n = xbmcaddon.Addon().getSetting('canal3n')
canal4 = xbmcaddon.Addon().getSetting('canal4')
canal4n = xbmcaddon.Addon().getSetting('canal4n')
canal5 = xbmcaddon.Addon().getSetting('canal5')
canal5n = xbmcaddon.Addon().getSetting('canal5n')

YOUTUBE_CHANNEL_ID_1 = "UCXNoBhd_1lgssLhWjrwPDzg"
YOUTUBE_CHANNEL_ID_2 = "UCLQx5-plGoj2mX7ev9ZbTLQ"
YOUTUBE_CHANNEL_ID_3 = "UCsz0g_dBsQ9M69ict8wbh4Q"
YOUTUBE_CHANNEL_ID_4 = "UCSNYHHL74C5igK0p8hZCoGA"
YOUTUBE_CHANNEL_ID_5 = "UCTTLVwLT64nw59NTZIVExOQ"
YOUTUBE_CHANNEL_ID_6 = "UCkGgtLpqrMqjgy281lzz1IA"
YOUTUBE_CHANNEL_ID_7 = "UC0iiFx68RgAgcL8-0BgitXg"
YOUTUBE_CHANNEL_ID_8 = "PLqENHzByu2YXnLuI9HfiiA_8PWDzor70d"
YOUTUBE_CHANNEL_ID_9 = "PLP5Y0vr09hnzvpUPYEYrBI_9lMJrp-GE2"
YOUTUBE_CHANNEL_ID_10 = "UCZWIb2nQIfSHRTv8-TQe2ig"
YOUTUBE_CHANNEL_ID_11 = "PLy42lMquA-kAVu4j5gGLb3zk8yb7ZIP2n"
YOUTUBE_CHANNEL_ID_12 = "PL14caO0qJZW9A-Ylg6f5EEjgSgfXG6Sf1"


# Entry point
def run():
    plugintools.log("docu.run")
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare HD TV[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-LLVvptQAtiY/AAAAAAAAAAI/AAAAAAAAAAA/85mf46PG4X8/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-ygAiIrb-Vcs/VNHxLpYwiCI/AAAAAAAAADg/c4wo11bh9qo/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/2048.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare Online[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-deBQ2oICvmI/AAAAAAAAAAI/AAAAAAAAAAA/_s4Ny4Y3Kvs/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-97UzdpWknZo/VLJbOaRtn0I/AAAAAAAAACY/5fx2CsUMNek/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/channels4_banner.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Filme Documentare[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-HGAqVBRRxjw/AAAAAAAAAAI/AAAAAAAAAAA/CjRnkY_iEeg/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-6IqBuNQuH7s/VMqNtjSRJQI/AAAAAAAAADk/wp3tdVWvEm4/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/channels4_banner.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]DOCUMENTARE-RO[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-QgB_aVD4Z-A/AAAAAAAAAAI/AAAAAAAAAAA/vJGQmYwH9HU/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://s.ytimg.com/yts/img/channels/c4/default_banner-vfl7DRgTn.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentary 2016[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-7Yrl3biQumc/AAAAAAAAAAI/AAAAAAAAAAA/jjArkDil6NQ/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-yk39mVDCklE/Vo2pOSolnDI/AAAAAAAAAAU/JiGj0oC4KzY/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/Music%2BNEW%2B2016%2B.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Filme Documentare Traduse[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/--8NyeOSWNrw/AAAAAAAAAAI/AAAAAAAAAAA/5z75iFKazEM/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-M0LYBuT2UVk/Vx6a2GJCqOI/AAAAAAAAAAQ/DSVLDCPt2uI_HN1ViU3mjdgKt-rvEbvCACL8B/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/documentareee.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare Online Subtitrate[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-_Qge5kcbw1U/AAAAAAAAAAI/AAAAAAAAAAA/fD4eqIsxuPA/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-czeVDjuh3PQ/VjS_rpHEj7I/AAAAAAAAADY/xULOhPlLuvQ/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/egypt-pyramids-giza-wallpapers-pictures-egyptian-wallpaper-high-resolution-for-house-border-walls-murals-wallpapers-hd-free-uk-tumblr-home.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]DOCUMENTARE SUBTITRATE[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_8+"/",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]DOCUMENTARE SUBTITRATE[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_9+"/",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Wildlife Documentaries[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-LWZqBI81vkk/AAAAAAAAAAI/AAAAAAAAAAA/yAQNrjxUVC8/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-ohPiVef7NAQ/V4yGyq6JZeI/AAAAAAAAAEg/4C57bHDSdP0jktHwKKNTJifXjLgPVAusQCL8B/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/oie_1893057gZ5b8WaK%2B%25281%2529.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Strange Events[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]DOCUMENTARE SUBTITRATE[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_12+"/",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]DOCUMENTARE ROMANESTI SUBTITRATE[/COLOR]",
        url="plugin://plugin.video.youtube/search/?q=Documentare romanesti subtitrate",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="%s"%canal1n,
        url="plugin://plugin.video.youtube/channel/%s/"%canal1,
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="%s"%canal2n,
        url="plugin://plugin.video.youtube/channel/%s/"%canal2,
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="%s"%canal3n,
        url="plugin://plugin.video.youtube/channel/%s/"%canal3,
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="%s"%canal4n,
        url="plugin://plugin.video.youtube/channel/%s/"%canal4,
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="%s"%canal5n,
        url="plugin://plugin.video.youtube/channel/%s/"%canal5,
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
run()
