# -*- coding: utf-8 -*-

import sqlite3

def create_db( config ):
	conn = sqlite3.connect( config.get( 'wp', 'db_uri' ) )

	c = conn.cursor()
	c.execute( '''create table wallpapers ( fname text, tags text, height integer, width integer )''' )
	conn.commit()

	c.close()

def insert_wp( config, wp_fname, tags, height, width ):
	pass

def get_random_wp( config ):
	pass
