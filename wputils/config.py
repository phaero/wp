# -*- coding: utf-8 -*-
import os
from ConfigParser import SafeConfigParser
from datetime import datetime

from xdg import BaseDirectory as basedir

_config_file = os.path.join( basedir.xdg_config_home, 'wputil.conf' )

def load_config():
	config = SafeConfigParser()
	
	_setup_defaults( config )
	config.read( _config_file )
	
	# Add an easy method to get out datetime objects from the 
	# config file
	def get_datetime( self, section, key ):
		return parse_iso8601_date( self.get( section, key ) )
	
	SafeConfigParser.get_datetime = get_datetime
	
	return config

def _setup_defaults( config ):
	config.add_section( 'wp' )
	config.set( 'wp', 'wp_dir', os.path.expanduser( '~/.wallpapers/' ) )
	config.set( 'wp', 'wpdb_uri', 
			'sqlite:%s' % os.path.join( basedir.xdg_data_home, 'wp.db' ) )
	config.set( 'wp', 'wpdb_last_updated', datetime.now().replace( 
		microsecond = 0 ).isoformat() )

def parse_iso8601_date(s):
	""" Parse date in iso8601 format e.g. 2003-09-15T10:34:54 and
	returns a datetime object.
	"""
	y=m=d=hh=mm=ss=0
	if len(s) not in [10,19,20]:
		raise ValueError('Invalid timestamp length - "%s"' % s)
	if s[4] != '-' or s[7] != '-':
		raise ValueError('Invalid separators - "%s"' % s)
	if len(s) > 10 and (s[13] != ':' or s[16] != ':'):
		raise ValueError('Invalid separators - "%s"' % s)
	try:
		y = int(s[0:4])
		m = int(s[5:7])
		d = int(s[8:10])
		if len(s) >= 19:
			hh = int(s[11:13])
			mm = int(s[14:16])
			ss = int(s[17:19])
	except Exception, e:
		raise ValueError('Invalid timestamp - "%s": %s' % (s, str(e)))
	return datetime(y,m,d,hh,mm,ss)
