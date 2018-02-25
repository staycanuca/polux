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

YOUTUBE_CHANNEL_ID_1 = "UChZqLqw7JC-84hHPKOHVEiQ"
YOUTUBE_CHANNEL_ID_2 = "UCa3Ooij_nma-1B0w0K1jskQ"
YOUTUBE_CHANNEL_ID_3 = "UC0iiFx68RgAgcL8-0BgitXg"
YOUTUBE_CHANNEL_ID_4 = "UCD_zsThn-7SzgaxEFNaVdSQ"
YOUTUBE_CHANNEL_ID_5 = "PLf18bmmC4QchHmqaaHb8zA6dySWTbxByp"
YOUTUBE_CHANNEL_ID_6 = "PLkBtg9viSaKGpTQCISQoWnYMFq4uuUFL1"
YOUTUBE_CHANNEL_ID_7 = "PLom4W-SVgZOlxEGlO3Jmv3n8Zwh_keUTY"
YOUTUBE_CHANNEL_ID_8 = "PLP5Y0vr09hnwyPVe0L0iwOVlE4GLrTHpl"
YOUTUBE_CHANNEL_ID_9 = "PLqENHzByu2YXnLuI9HfiiA_8PWDzor70d"
YOUTUBE_CHANNEL_ID_10 = "PLCP1ojrqiXJafTWNRkfPwQIasXNtPrqpU"
YOUTUBE_CHANNEL_ID_11 = "UCZWIb2nQIfSHRTv8-TQe2ig"
YOUTUBE_CHANNEL_ID_12 = "UCwed4UuxvfcGcxJrUNgALQA"


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
        title="[COLOR skyblue]Documentare Romana - documentare in limba romana[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-LLVvptQAtiY/AAAAAAAAAAI/AAAAAAAAAAA/85mf46PG4X8/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-ygAiIrb-Vcs/VNHxLpYwiCI/AAAAAAAAADg/c4wo11bh9qo/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/2048.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]WikiBay - materiale educationale si documentare[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-deBQ2oICvmI/AAAAAAAAAAI/AAAAAAAAAAA/_s4Ny4Y3Kvs/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-97UzdpWknZo/VLJbOaRtn0I/AAAAAAAAACY/5fx2CsUMNek/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/channels4_banner.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare online subtitrate[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-HGAqVBRRxjw/AAAAAAAAAAI/AAAAAAAAAAA/CjRnkY_iEeg/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-6IqBuNQuH7s/VMqNtjSRJQI/AAAAAAAAADk/wp3tdVWvEm4/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/channels4_banner.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare Romanesti[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-QgB_aVD4Z-A/AAAAAAAAAAI/AAAAAAAAAAA/vJGQmYwH9HU/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://s.ytimg.com/yts/img/channels/c4/default_banner-vfl7DRgTn.png",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare istorice si stiintifice romanesti[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-7Yrl3biQumc/AAAAAAAAAAI/AAAAAAAAAAA/jjArkDil6NQ/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-yk39mVDCklE/Vo2pOSolnDI/AAAAAAAAAAU/JiGj0oC4KzY/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/Music%2BNEW%2B2016%2B.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]FILME DOCUMENTARE,PARANORMALE,CIUDATE[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/--8NyeOSWNrw/AAAAAAAAAAI/AAAAAAAAAAA/5z75iFKazEM/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-M0LYBuT2UVk/Vx6a2GJCqOI/AAAAAAAAAAQ/DSVLDCPt2uI_HN1ViU3mjdgKt-rvEbvCACL8B/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/documentareee.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Al doilea razboi mondial[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-_Qge5kcbw1U/AAAAAAAAAAI/AAAAAAAAAAA/fD4eqIsxuPA/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-czeVDjuh3PQ/VjS_rpHEj7I/AAAAAAAAADY/xULOhPlLuvQ/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/egypt-pyramids-giza-wallpapers-pictures-egyptian-wallpaper-high-resolution-for-house-border-walls-murals-wallpapers-hd-free-uk-tumblr-home.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Documentare romanesti[/COLOR]",
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
        title="[COLOR skyblue]Documentare[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_10+"/",
        thumbnail="https://yt3.ggpht.com/-LWZqBI81vkk/AAAAAAAAAAI/AAAAAAAAAAA/yAQNrjxUVC8/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-ohPiVef7NAQ/V4yGyq6JZeI/AAAAAAAAAEg/4C57bHDSdP0jktHwKKNTJifXjLgPVAusQCL8B/w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/oie_1893057gZ5b8WaK%2B%25281%2529.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Wildlife Documentaries[/COLOR]",
        url="plugin://plugin.video.youtube/playlist/"+YOUTUBE_CHANNEL_ID_11+"/",
        thumbnail="https://yt3.ggpht.com/-88EuD4De3KA/AAAAAAAAAAI/AAAAAAAAAAA/6tO2Hqp2eqE/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/veO8jpDyawnM21pgy_4MEmRe4mOqkp9XU6ovD_T2dbKBd-IMGJn8mHKKxDucEm2csq7_LIeP=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
        folder=True )
		
    plugintools.add_item( 
        #action="", 
        title="[COLOR skyblue]Tv Romania[/COLOR]",
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

		
run()
