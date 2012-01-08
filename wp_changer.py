#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
wp_changer.py

Created by Johan Segolsson on 2009-12-26.
Copyright (c) 2009 Johan Segolsson. All rights reserved.
"""

import os
import sys
import random
import mimetypes

_WPCONFIG_DIR = os.path.expanduser( '~/.wallpaperchanger' )
_WPCONFIG_FNAME = '%s/wallpaperchangerconfig.py' % _WPCONFIG_DIR
_WPCONFIG = """#config file for wallpaperchanger
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

def _create_config():
	print 'could not import configfile, so fresh configfile will be created in ~/.wallpaperchanger'
	if not os.path.exists( _WPCONFIG_DIR ):
		try:
			os.mkdir( _WPCONFIG_DIR )
		except:
			pass

	os.chdir( _WPCONFIG_DIR )

	try:
		c = open( _WPCONFIG_FNAME,'w' )
		c.write( _WPCONFIG )
		c.close()
	except:
		raise SystemExit, 'could not write configfile to %s. Please check write permissions.' % _WPCONFIG_FNAME

def _get_valid_images():
	"""
	Return all valid images in all picture directories ( recursively ).
	"""
	for picturedir in picturedirs:
		for rootdir, dirlist, filelist in os.walk(picturedir): # recursive scan for filenames
			for _file in filelist:
				if _valid_image( rootdir, _file ):
					yield os.path.join( rootdir, _file )

def _valid_image( rootdir, _file):
	"""
	Change if the file is and image, if it contains any keywords that should be
	excluded.
	"""
	clean = True
	mimetype = mimetypes.guess_type(_file)[0]

	if mimetype and mimetype.split('/')[0] == "image":
		for keyword in keywords_exclude:
			if keyword in rootdir or keyword in _file:
				clean = False

		if clean == True:
			return True
	
	return False

def _change_background( fname ):
	"""
	Change desktop background.
	"""
	os.system( 'feh --bg-scale "%(fname)s"' % locals() )

def main( args ):
	images = [ i for i in _get_valid_images() ]

	if len(images) < 1:
		raise SystemExit, "no pictures found"

	_change_background( images[ random.randint(0, len (images) - 1) ] )

	return 0

# Add _WPCONFIG_DIR on the path and try to import it
sys.path.append( os.environ["HOME"] )
sys.path.append( _WPCONFIG_DIR )
try:
	from wallpaperchangerconfig import * # try to import config file 
	#print "config file imported."
except:
	_create_config()
	from wallpaperchangerconfig import * # try to import config file 
	print "config file written to ~/.wallpaperchanger and imported."

if __name__ == '__main__':
	sys.exit( main( sys.argv[1:] ) )
