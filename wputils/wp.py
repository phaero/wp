# -*- coding: utf-8 -*-
import sys
import logging
from optparse import OptionParser
from config import load_config

def init_wp( config, args ):
	print 'wallpaper directory: ', config.get( 'wp', 'wp_dir' )
	print 'Database uri: ', config.get( 'wp', 'wpdb_uri' )
	print 'Database last updated (str): ', config.get( 
			'wp', 'wpdb_last_updated' )
	print 'Database last updated (tuple): ', config.get_datetime( 
			'wp', 'wpdb_last_updated' )

def import_wp( config, args ):
	print 'import'

def update_wp( config, args ):
	print 'update'

def help_wp( config, args ):
	print "Usage: wp action [option(s)]"
	print
	print "Available options:"

	for action in actions:
		print '    %s' % action

actions = {
		'help' : help_wp,
		'init' : init_wp,
		'import' : import_wp,
		'update-wp' : update_wp,
	}

def main( args ):
	if not len( args ) > 0:
		help_wp( None, args )
		sys.exit(1)
	
	action = args.pop()
	
	# First check that the action is a valid one.
	if not action in actions.keys():
		print '"%s" is not a valid action!' % action
		sys.exit(1)
	
	action_function = actions[ action ]
	action_function( load_config(), args )
