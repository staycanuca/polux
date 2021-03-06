# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains all necessary functions to work with SopCast engine.
    
    Main functions:
    sopstreams(name,iconimage,sop) -> This function processes the id/sop url received as argument and then calls the SopCast engine for Windows.
                                        If the OS is not Windows, sopstreams_builtin will be called with the received arguments.
    sopstreams_builtin(name,iconimage,sop) -> This function processes the url received from sopstreams and then calls the SopCast engine for all *nix based OS's.
    
    Classes:
    SopWindowsPlayer -> Inheritance of XBMC Player class used only for Windows.
    streamplayer -> Inheritance of XBMC Player class used for Linux/OSX/Android.
    
    Sopcast utils:
    sop_sleep(time , spsc_pid) -> sopcast_binary pid sleep function. For all supported OS's except Windows.
    handle_wait_socket(time_to_wait,title,text,seconds='') -> Timer to check if sopcast local server has started (attempt to connect on sopcast local server port).
                                                                This function is used only for Windows.
    break_sopcast() -> Intentionally break the sopcast player in windows to avoid double sound created by the running sopcastp2p service.
    osx_sopcast_downloader() -> Sopcast downloader thread to avoid curl bugs in OSX.
    
"""

import xbmc,xbmcgui,xbmcplugin,urllib2,os,sys,subprocess,xbmcvfs,socket,re,requests,shutil
from thread import start_new_thread
from utils.pluginxbmc import *
from utils.utilities import handle_wait
from pages.history import add_to_history

""" Sopcast Dependent variables are listed below"""

SPSC_BINARY = "sp-sc-auth"
LOCAL_PORT = settings.getSetting('local_port')
VIDEO_PORT = settings.getSetting('video_port')
BUFER_SIZE = int(settings.getSetting('buffer_size'))
if(settings.getSetting('auto_ip')=='true'):
    LOCAL_IP=xbmc.getIPAddress()
else: LOCAL_IP=settings.getSetting('localhost')
VIDEO_STREAM = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"

""" Sopcast Main functions"""

def sopstreams(name,iconimage,sop):
    if not iconimage: iconimage = os.path.join(addonpath,'resources','art','sopcast_logo.png')
    if "sop://" not in sop: sop = "sop://broker.sopcast.com:3912/" + sop
    else: pass
    print("Starting Player Sop URL: " + str(sop))
    labelname=name
    if settings.getSetting('addon_history') == "true":
        try: add_to_history(labelname, str(sop),2, iconimage)
        except: pass
    if not xbmc.getCondVisibility('system.platform.windows'):
        if xbmc.getCondVisibility('System.Platform.Android'):
            if  settings.getSetting('external-sopcast') == "1":
                xbmc.executebuiltin('XBMC.StartAndroidActivity("org.sopcast.android","android.intent.action.VIEW","",'+sop+')')
            else: sopstreams_builtin(name,iconimage,sop)
        else: sopstreams_builtin(name,iconimage,sop)
    else:
        cmd = ['sc','sdshow','sopcastp2p']
        import subprocess
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        config = True
        for line in proc.stdout:
            if " 1060:" in line.rstrip():
                config = False
                print("Sopcast configuration is not done!")
        if config == False: messageok(translate(30000),translate(30027),translate(30028), translate(30029))
        else:
            import _winreg
            aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)

            #Dirty hack to break sopcast h264 codec so double sound can be avoided.

            try:
                aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                name, value, type = _winreg.EnumValue(aKey, 0)
                codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx')
                _winreg.CloseKey(aKey)
                if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old'))
            except:pass
            aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
            aKey = _winreg.OpenKey(aReg, r'SYSTEM\CurrentControlSet\Services\sopcastp2p\Parameters', 3, _winreg.KEY_WRITE)
            _winreg.SetValueEx(aKey,"AppParameters",0, _winreg.REG_SZ, sop)
            _winreg.CloseKey(aKey)
            cmd = ['sc','start','sopcastp2p']
            import subprocess
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            servicecreator = False
            for line in proc.stdout:
                print("result line: " + line.rstrip())
            res = handle_wait_socket(int(settings.getSetting('socket_time')),translate(30000),translate(30030))

            if res == True:
                print("Server created - waiting x seconds for confirmation")
                try: sock.close()
                except: pass
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                handle_wait(int(settings.getSetting('stream_time')),translate(30000),translate(30031),seconds='')
                try:
                    result = sock.connect(('127.0.0.1',8902))
                    connected = True
                except: connected = False
                if connected == True:
                    playlist = xbmc.PlayList(1)
                    playlist.clear()
                    listitem = xbmcgui.ListItem(labelname, iconImage=iconimage, thumbnailImage=iconimage)
                    listitem.setLabel(labelname)
                    listitem.setInfo("Video", {"Title":labelname})
                    listitem.setProperty('mimetype', 'video/x-msvideo')
                    listitem.setProperty('IsPlayable', 'true')
                    windows_sop_url = "http://127.0.0.1:8902/tv.asf"
                    listitem.setPath(path=windows_sop_url)
                    playlist.add(windows_sop_url, listitem)
                    xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
                    player = SopWindowsPlayer()
                    if int(sys.argv[1]) < 0:
                        player.play(playlist)
                    while player._playbackLock:
                        xbmc.sleep(5000)
                else: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30032), 1,os.path.join(addonpath,"icon.png")))
            else: xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30032), 1,os.path.join(addonpath,"icon.png")))
            print("Player reached the end")
            cmd = ['sc','stop','sopcastp2p']
            import subprocess
            proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
            servicecreator = False
            for line in proc.stdout:
                print("result line" + line.rstrip())
                 #break SopCast x264 codec - renaming the file later
            import _winreg
            aReg = _winreg.ConnectRegistry(None,_winreg.HKEY_LOCAL_MACHINE)
            try:
                aKey = _winreg.OpenKey(aReg, r'SOFTWARE\SopCast\Player\InstallPath',0, _winreg.KEY_READ)
                name, value, type = _winreg.EnumValue(aKey, 0)
                codec_file = os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx.old')
                _winreg.CloseKey(aKey)
                if xbmcvfs.exists(codec_file): xbmcvfs.rename(codec_file,os.path.join(os.path.join(value.replace("SopCast.exe","")),'codec','sop.ocx'))
            except:pass


def sopstreams_builtin(name,iconimage,sop):
    try:
        global spsc
        if xbmc.getCondVisibility('System.Platform.Linux') and not xbmc.getCondVisibility('System.Platform.Android'):

            if os.uname()[4] == "armv6l" or os.uname()[4] == "armv7l" or settings.getSetting('openelecx86_64') == "true":
                if settings.getSetting('jynxbox_arm7') == "true":
                    cmd = [os.path.join(addonprofile,'sopcast','ld-linux.so.3'),'--library-path',os.path.join(addonprofile,'sopcast','libqemu'),os.path.join(addonprofile,'sopcast','qemu-i386'),os.path.join(addonprofile,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(addonprofile,'sopcast',"lib"),os.path.join(addonprofile,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
                else:
                    cmd = [os.path.join(addonprofile,'sopcast','qemu-i386'),os.path.join(addonprofile,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(addonprofile,'sopcast',"lib"),os.path.join(addonprofile,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
            elif settings.getSetting('openeleci386') == "true":
                cmd = [os.path.join(addonprofile,'sopcast','lib/ld-linux.so.2'),"--library-path",os.path.join(addonprofile,'sopcast',"lib"),os.path.join(addonprofile,'sopcast','sp-sc-auth'),sop,str(LOCAL_PORT),str(VIDEO_PORT)]
            else:
                cmd = [os.path.join(addonprofile,'sopcast','ld-linux.so.2'),'--library-path',os.path.join(addonprofile,'sopcast','lib'),os.path.join(addonprofile,'sopcast',SPSC_BINARY), sop, str(LOCAL_PORT), str(VIDEO_PORT)]

        elif xbmc.getCondVisibility('System.Platform.OSX'):
            cmd = [os.path.join(addonprofile,'sopcast','sp-sc-auth'), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]

        elif xbmc.getCondVisibility('System.Platform.Android'):
            cmd = [str(settings.getSetting('android_sopclient')), str(sop), str(LOCAL_PORT), str(VIDEO_PORT)]

        print(cmd)

        #Check if another instance of the sopcast executable might still be running on the same port. Attempt to connect to server and video ports giving the user the choice before creating a new subprocess
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOCAL_IP, int(LOCAL_PORT)))
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((LOCAL_IP, int(VIDEO_PORT)))
            sock.close()
            existing_instance = True
        except: existing_instance = False
        if existing_instance == True:
            option = xbmcgui.Dialog().yesno(translate(30000), translate(30033),translate(30034))
            if not option:
                if xbmc.getCondVisibility('System.Platform.Android') == "true":
                    xbmc_user = os.getlogin()
                    procshut = subprocess.Popen(['ps','|','grep','sopclient'],shell=False,stdout=subprocess.PIPE)
                    for line in procshut.stdout:
                        match = re.findall(r'\S+', line.rstrip())
                        if match:
                            if 'sopclient' in match[-1] and len(match)>2:
                                if xbmc_user == match[0]:
                                    os.system("kill " + match[1])
                                    xbmc.sleep(200)
                                else:
                                    os.system("su -c kill " + match[1])
                                    xbmc.sleep(200)
                elif xbmc.getCondVisibility('System.Platform.Linux'):
                    os.system("kill $(ps aux | grep '[s]p-sc-auth' | awk '{print $1}')") #openelec
                    os.system("kill $(ps aux | grep '[s]p-sc-auth' | awk '{print $2}')")
                elif xbmc.getCondVisibility('System.Platform.OSX'):
                    os.system("kill $(ps aux | grep '[s]p-sc-auth')")
            else: pass
        else: pass

        #opening the subprocess
        if settings.getSetting('debug_mode') == "false":
            spsc = subprocess.Popen(cmd, shell=False, bufsize=BUFER_SIZE,stdin=None, stdout=None, stderr=None)
        else:
            spsc = subprocess.Popen(cmd, shell=False, bufsize=BUFER_SIZE,stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        listitem.setLabel(name)
        listitem.setInfo('video', {'Title': name})
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(int(settings.getSetting('wait_time')))
        res=False
        #counter=50
        counter = int(int(settings.getSetting("loading_time"))*2+10)
        ret = messagepg.create(translate(30000),"SopCast",translate(30035) % (str(20)))
        messagepg.update(0)
        warning = 0
        while counter > 0 and spsc.pid:
            if messagepg.iscanceled():
                messagepg.close()
                break
            xbmc.sleep(400)
            counter -= 1
            messagepg.update(int((1-(counter/50.0))*100),"SopCast",translate(30035) % str(int(int(settings.getSetting("loading_time")) * (1-((1-(counter/50.0)))))))
            try:
                urllib2.urlopen(url)
                counter=0
                res=sop_sleep(200 , spsc.pid)
                break
            except:
                if warning == 0:
                    print("Other instance of sopcast is still running")
                    warning += 1
                else: pass

        if res:
            messagepg.update(100)
            if not xbmc.getCondVisibility('System.Platform.OSX'):
                listitem.setPath(path=url)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
                player = streamplayer(spsc_pid=spsc.pid , listitem=listitem)
                if int(sys.argv[1]) < 0:
                    player.play(url, listitem)
                while player._playbackLock:
                    xbmc.sleep(500)
            else:
                xbmc.sleep(200)
                video_file = os.path.join(addonprofile,'sopcast.avi')
                start_new_thread(osx_sopcast_downloader,())
                handle_wait(int(settings.getSetting('stream_time_osx')),translate(30000),translate(30031),seconds='')
                listitem.setPath(path=video_file)
                xbmcplugin.setResolvedUrl(int(sys.argv[1]),True,listitem)
                player = streamplayer(spsc_pid=spsc.pid , listitem=listitem)
                player.play(video_file, listitem)
                while player._playbackLock:
                    xbmc.sleep(500)
        else:
            xbmc.sleep(200)
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(30000), translate(30032), 1,os.path.join(addonpath,"icon.png")))

    except: pass
    if settings.getSetting('debug_mode') == "true":
        try:
            stdout, stderr = spsc.communicate()
            print(stdout,stderr)
        except: pass
    try: os.kill(spsc.pid,9)
    except: pass
    xbmc.sleep(100)
    try:os.system("killall -9 "+SPSC_BINARY)
    except:pass
    xbmc.sleep(100)
    try:spsc.kill()
    except:pass
    xbmc.sleep(100)
    try:spsc.wait()
    except:pass
    xbmc.sleep(100)
    try: os.kill(spsc.pid,9)
    except: pass
    messagepg.close()
    print("Player ended at last")


""" Sopcast Player classes """


class SopWindowsPlayer(xbmc.Player):
    def __init__(self):
        self._playbackLock = True
        if settings.getSetting('force_dvplayer') == 'true': xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        print("Player created")

    def onPlayBackStarted(self):
        print("Player has started")

    def onPlayBackStopped(self):
        print("Player stoped")
        self._playbackLock = False
        import subprocess
        cmd = ['sc','stop','sopcastp2p']
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        for line in proc.stdout:
            print(line.rstrip())


    def onPlayBackEnded(self):
        self.onPlayBackStopped()
        print("Player ended")



class streamplayer(xbmc.Player):
    def __init__( self , *args, **kwargs):
        self.spsc_pid=kwargs.get('spsc_pid')
        self.listitem=kwargs.get('listitem')
        self._playbackLock = True

    def onPlayBackStarted(self):
        messagepg.close()
        if xbmc.Player().getPlayingFile() != "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/" and 'sopcast' not in xbmc.Player().getPlayingFile():
            try: os.kill(self.spsc_pid,9)
            except: pass
        else: pass

    def onPlayBackEnded(self):
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player().isPlaying():
                player = streamplayer(spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)
        try:
            xbmcvfs.delete(os.path.join(addonprofile,'sopcast.avi'))
        except:
            pass

    def onPlayBackStopped(self):
        self._playbackLock = False
        url = "http://"+LOCAL_IP+":"+str(VIDEO_PORT)+"/"
        xbmc.sleep(300)
        if os.path.exists("/proc/"+str(self.spsc_pid)) and xbmc.getCondVisibility("Window.IsActive(epg.xml)") and settings.getSetting('safe_stop')=="true":
            if not xbmc.Player().isPlaying():
                player = streamplayer(spsc_pid=self.spsc_pid , listitem=self.listitem)
                player.play(url, self.listitem)
        else:
            try: os.kill(self.spsc_pid,9)
            except: pass
        try:
            xbmcvfs.delete(os.path.join(addonprofile,'sopcast.avi'))
        except:
            pass

""" Sopcast Utils"""

def handle_wait_socket(time_to_wait,title,text,seconds=''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    ret = messagepg.create(' '+title)
    secs=0
    percent=0
    increment = int(100 / time_to_wait)
    cancelled = False
    while secs < time_to_wait:
        try:
            result = sock.connect(('127.0.0.1',8902))
            connected = True
            print("Connected to port 8902, server is working")
            break
            sock.close()
        except:
            print("Stil trying to connect")
        secs = secs + 1
        percent = increment*secs
        secs_left = str((time_to_wait - secs))
        if seconds=='': remaining_display = translate(30036) + " " + str(percent) + " %"
        else: remaining_display=seconds
        messagepg.update(percent,text,remaining_display)
        xbmc.sleep(1000)
        if (messagepg.iscanceled()):
            cancelled = True
            break
    if cancelled == True:
        return False
    elif connected == True:
        messagepg.close()
        return True
    else:
        messagepg.close()
        return False

def sop_sleep(time , spsc_pid):
    counter=0
    increment=200
    path="/proc/%s" % str(spsc_pid)
    try:
        while counter < time and spsc_pid>0 and not xbmc.abortRequested:
            counter += increment
            xbmc.sleep(increment)
    except: return True

    if counter < time: return False
    else: return True

#dirty hack to break sopcast.exe player codec to avoid double sound.
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

def osx_sopcast_downloader():
    print VIDEO_STREAM
    print "started osx downloader thread"
    response = requests.get(VIDEO_STREAM, stream=True)
    print response.headers
    video_file = os.path.join(addonprofile,'sopcast.avi')
    with open(video_file, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    print "ended thread"
