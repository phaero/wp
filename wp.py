#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir, getcwd, rename
from os.path import basename, splitext, realpath, isdir, join, exists
from optparse import OptionParser
import Image
import logging

log = logging.getLogger( 'wp' )

def create_option_parser():
	parser = OptionParser( usage = '%prog [options] [directory(s)]' )
	
	parser.add_option( '-d', '--debug', action = 'store_true', default = False, 
			dest = 'debug', help = 'Print debug messages.' )
	
	parser.add_option( "-i", "--info", action = "store_true", default = False, 
			dest = "info", help = "Print info messages." )
	
	parser.add_option( "-r", "--recursive", action = "store_true", 
			default = False, dest = "recursive", 
			help = "Check directory(s) recursively." )
	
	parser.add_option( "--not-valid", action = "store_false", 
			default = True, dest = "show_valid_sizes", 
			help = "Print those pictures that doesn't match any of the valid wallpaper sizes." )
	
	parser.add_option( "-s", "--sizes", dest = "sizes", 
			help = "Set valid sizes" )
	
	parser.add_option( "-l", "--list", action="store_true", default = False, 
			dest = "show_sizes", help = "List all the images sizes." )
	
	parser.add_option( "-D", "--dir", default = None, dest = "move_to", 
			help = "Move files to dir." )
	
	parser.add_option( "-f", "--force", default = False, 
			action = "store_true", dest = "force", 
			help = "Overwrite files if a filename already exists." )
	
	parser.add_option( "-t", "--tag", dest = "tag", 
			help = "If 'dir' is set, move file to 'tag' subdir." )
	
	parser.add_option( "-S", "--subsize", default = False, 
			action = "store_true", dest = "move_to_size_subdir", 
			help = "If 'dir' is set, move file to 'WxH' subdir ( if tag is used then the size subdir should be in the 'tag' directory." )

	return parser

def main():
	parser = create_option_parser()
	options, args = parser.parse_args()
	
	if options.debug:
		logging.basicConfig( level = logging.DEBUG )
	elif options.info:
		logging.basicConfig( level = logging.INFO )
	
	include_ext = [ ".png", ".jpg", ".jpeg" ]
	valid_sizes = ( ( 1280, 1024 ), ( 1600, 1200 ), ( 1680, 1050 ), 
			( 1152, 864 ), ( 1920, 1200 ), ( 1280, 800 ), ( 1600, 1000 ) )
	
	logging.debug( "Options: %s", options )
	
	if len( args ) == 0:
		working_directory = getcwd()
	else:
		pass
	
	if options.sizes:
		valid_sizes = [ map( int, size.split('x') ) for size in 
				options.sizes.split(',') ]
	
	if options.move_to and not isdir( options.move_to ):
		logging.error( "'%s' is not a valid directory", options.move_to )
		parser.error( "'%s' is not a valid directory!" % options.move_to )
	
	# loop through all files in 'working_directory'
	for fname in listdir( working_directory ):
		logging.debug( "Checking %s", fname )
		# Check if it has a valid file extension
		if splitext( fname )[1].lower() in include_ext:
			logging.debug( "%s has a valid extension ( on of these %s )", 
					fname, include_ext )
			# Run 'identify to se if it is a valid image file and get 
			# its dimension at the same time if it is.
			try:
				img = Image.open( realpath( fname ) )
				logging.debug( "%s is %dx%d", fname, img.size[0], img.size[1] )
				
				if options.show_sizes:
					print "%dx%d %s" % ( img.size[0], img.size[1], fname )
				elif options.show_valid_sizes:
					if img.size in valid_sizes:
						logging.debug( "%s has a valid size.", fname )
						image_match( fname, img.size, options )
				else:
					if img.size not in valid_sizes:
						logging.debug( "%s has not valid size.", fname )
						image_match( fname, img.size, options )
			except IOError, ex:
				logging.error( "Could not open %s ( Exception: %s )", fname, ex )

def image_match( fname, size, options ):
	"""Moves a file to a specified directory or prints the filename 
	on stdout."""
	if options.move_to:
		path = realpath( options.move_to )
		
		if options.tag:
			path = join( path, options.tag )
		
		if options.move_to_size_subdir:
			path = join( path, "%dx%d" % size )
		
		path = join( path, basename( fname ) )
	
		if options.info:
			logging.info( "Renaming %s to %s", fname, path )
		elif not exists( path ) or ( exists( path ) and options.force ):
			logging.info( "Renaming %s to %s", fname, path )
			rename( realpath( fname ), path )
		else:
			logging.error( "%s already exists ( to overwrite this file use the '-f' option )", path )
	else:
		print '"%s"' % realpath( fname )

if __name__ == "__main__":
	main()
