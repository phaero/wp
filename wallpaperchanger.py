#!/usr/bin/python
#
# wallpaperchanger.py
#
# A script to change your gnome wallpaper to a random background image
#
# (c) 2004, Davyd Madeley <davyd@madeley.id.au>
# edited 8/2006 by Horst JENS <Horst.Jens@gmx.at>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


import gconf
import os
import sys
import random
import mimetypes

if os.name != 'posix':
    raise SystemExit, "no-linux Operations System detected. Yuk !"
sys.path.append(os.environ["HOME"])
sys.path.append(os.path.join(os.environ["HOME"], '.wallpaperchanger'))
configdir = os.path.join(os.environ["HOME"], '.wallpaperchanger')
inifiletext = """#config file for wallpaperchanger
#must be located in ~/.wallpaperchanger
#and must be named wallpaperchangerconfig.py
#all text behind a # is a comment
#you can edit this file as you like
#all directorys listed here will be searched recursive (INCLUDING their sub-directorys). Example:
# picturedirs = ["/home", "/media/win_c/pictures", "/media/win_d/personal/mycat/"]
picturedirs = ["/home", "/usr/share/pixmaps/backgrounds"]
#all keywords listed here will make the wallpaper tiled if keyword is found in pathname or filename.
keywords_tiled = ["tiled", "pattern"]
#all keywords listed here will make the wallpaper centered if keyword is found in pathname or filename.
keywords_centered = ["centered"]
#all keywords listed here will make the wallpaper zoomed if keyword is found in pathname or filename.
keywords_zoomed = ["zoomed"]
#all keywords listed here will make the wallpaper streched if keyword is found in pathname or filename.
keywords_stretched = ["stretched"]
# per default, all wallpapers will be "scaled" if no other keyword is found.
#if any of the keywords listed here is found in  filename or pathname, file will NOT be used as wallpaper..
keywords_exclude = ["privat", "secret", "bad", "ugly", "temp", "thumb"] 
"""
try:
    from wallpaperchangerconfig import * # try to import config file 
    #print "config file imported."
except:
    print 'could not import configfile, so fresh configfile will be created in ~/.wallpaperchanger'
    os.chdir(os.environ["HOME"])
    try:
        os.mkdir('.wallpaperchanger')
    except:
        pass # if you can not create a directory, it may already exist...
    os.chdir('.wallpaperchanger')
    try:
        c = file('wallpaperchangerconfig.py','w')
        c.wirte(inifiletext)
        c.close()
    except:
        raise SystemExit, "could not write configfile to ~/.wallpaperchanger . Please check write permissions."
    from wallpaperchangerconfig import * # try to import config file 
    print "config file written to ~/.wallpaperchanger and imported."


class GConfClient:
        def __init__(self):
                self.__client__ = gconf.client_get_default ()
        def get_background(self):
                return self.__client__.get_string("/desktop/gnome/background/picture_filename")
        def set_background(self, background):
                self.__client__.set_string("/desktop/gnome/background/picture_filename", background)
        def set_option (self, option):
                self.__client__.set_string("/desktop/gnome/background/picture_options", option)
client = GConfClient()


imageitems = []
for picturedir in picturedirs:
    for rootdir, dirlist, filelist in os.walk(picturedir): # recursive scan for filenames
        for file in filelist:
            mimetype = mimetypes.guess_type(file)[0]
            if mimetype and mimetype.split('/')[0] == "image":
                clean = True
                for keyword in keywords_exclude:
                    if keyword in rootdir or keyword in file:
                        clean = False
                if clean == True:
                    imageitems.append(os.path.join(rootdir,file))
if len(imageitems) < 1:
    raise SystemExit, "no pictures found"
item = random.randint(0, len (imageitems) - 1)
current_bg = client.get_background()

while (imageitems[item] == current_bg):
        item = random.randint(0, len(imageitems) - 1)
client.set_background(imageitems[item])

option = "scaled"  # default 
for option_name, keywordlist in (('wallpaper', keywords_tiled),
                                                    ('centered', keywords_centered),
                                                    ('zoom', keywords_zoomed),
                                                    ('stretched', keywords_stretched)):
    for keyword in keywordlist:
        #print option_name, keywordlist, keyword
        if keyword in imageitems[item]:
            option = option_name
            break 

client.set_option(option)
#print "setting wallpaper" , imageitems[item], "with the option", option
#options = ["scaled","wallpaper", "zoom", "centered", "streched"]

