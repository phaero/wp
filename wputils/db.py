# -*- coding: utf-8 -*-
import sqlobject

class Wallpaper( sqlobject.SQLObject ):
	fname = sqlobject.UnicodeCol()
	height = sqlobject.IntCol()
	width = sqlobject.IntCol()
