# -*- coding: utf-8 -*-
#$pyFunction
       def GetLSProData(page_data,Cookie_Jar,m,url='http://gslh.co.uk:8080/live/owen/owen/82594.ts'):
       import urllib
       u = url
       if '.ts' in url:
        u = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=' + urllib.quote_plus(url)
       return u
       