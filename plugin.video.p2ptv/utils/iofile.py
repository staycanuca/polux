# -*- coding: utf-8 -*-

""" Copyright (c) 2017 Mario Bălănică
    
    This file contains the functions for file handling.
    
    Functions:
    readfile(filename) -> Function to read text files.
    savefile(filename, contents) -> Function to write/save text files.
    save(filename,contents) -> Function to write/save text files.
    
"""

import os

def readfile(filename):
    f = open(filename, "r")
    string = f.read()
    return string

def savefile(filename, contents):
    try:
        destination = os.path.join(addonprofile, filename)
        fh = open(destination, 'wb')
        fh.write(contents)
        fh.close()
        return
    except:
        print("Could not write to: %s" % filename)
        return

def save(filename,contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()
    return
