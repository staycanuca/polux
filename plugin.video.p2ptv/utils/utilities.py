# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains common utilities.
    
    Functions:
    handle_wait(time_to_wait,title,text,seconds='') -> Timer with dialog progress capabilities.
    getDirectorySize(directory) -> Returns a directory size recursively.
    recursive_overwrite(src, dest, ignore=None) -> Copy and replace an entire directory recursively.
   	
"""

import xbmc,xbmcplugin,xbmcgui,xbmcaddon,re,os,shutil
from pluginxbmc import *

def handle_wait(time_to_wait,title,text,seconds=''):
        ret = messagepg.create(' '+title)
        secs=0
        percent=0
        increment = int(100 / time_to_wait)
        cancelled = False
        while secs < time_to_wait:
                secs = secs + 1
                percent = increment*secs
                secs_left = str((time_to_wait - secs))
                if seconds=='': remaining_display = translate(30070) + str(secs_left) + translate(30071)
                else: remaining_display=seconds
                messagepg.update(percent,text,remaining_display)
                xbmc.sleep(1000)
                if (messagepg.iscanceled()):
                        cancelled = True
                        break
        if cancelled == True:
                return False
        else:
                messagepg.close()
                return False

def getDirectorySize(directory):
	dir_size = 0
	for (path, dirs, files) in os.walk(directory):
		for file in files:
			filename = os.path.join(path, file)
			dir_size += os.path.getsize(filename)
	return dir_size
	
def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)
    return
