# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\Users\\spivette\\AppData\\Local\\Programs\\Python\\Python37\\python.exe")
sys.path.append("C:\\Users\\pivet\\AppData\\Local\\Programs\\Python\\Python37\\python.exe")

from resources.lib import kodilogging
from resources.lib import plugin

import logging
import xbmcaddon



# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
kodilogging.config()

plugin.run()


