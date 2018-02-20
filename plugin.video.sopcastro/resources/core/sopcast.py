# -*- coding: utf-8 -*-

""" sopcastro  (c)  2014 enen92 fightnight

	Addon functions related to sopcast

	Main functions:
	sopstreams(name,iconimage,sop) -> Wrapper to Plexus sopstreams(name, iconimage, sop)

"""

import xbmc,urllib,xbmcvfs,os
from utils.pluginxbmc import settings
from history import add_to_history

def sopstreams(name, iconimage, sop):
	print("Call sopstreams with name: " + str(name)  + " sop = " + str(sop))

	if settings.getSetting('addon_history') == "true":
		try: add_to_history(name, sop, iconimage)
		except: pass

	plexusURI = 'plugin://program.plexus/?url={CHID}&mode=2&name={CHNAME}'.format(
				CHID   = urllib.quote(sop,  safe = ''),
				CHNAME = urllib.quote(name, safe = ''))

	if iconimage is not None:
		plexusURI += "&iconimage={CHICON}".format(CHICON = urllib.quote(iconimage, safe=''))

	print('Executing: PlayMedia("{0}")'.format(plexusURI))

	xbmc.executebuiltin('PlayMedia("{0}")'.format(plexusURI))

#dirty hack to break sopcast.exe player codec to avoid double sound
def break_sopcast():
	if xbmc.getCondVisibility('system.platform.windows'):
		import _winreg
		aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
		try:
			aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
			name, value, type = _winreg.EnumValue(aKey, 0)
			codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
			_winreg.CloseKey(aKey)
			if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
		except:pass