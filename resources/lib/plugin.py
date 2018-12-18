# -*- coding: utf-8 -*-
import routing
import logging
import requests
import re
import xbmcaddon
import xbmcgui
import xbmc
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory


# monday work
# https://danvatterott.com/blog/2017/03/11/my-first-kodi-addon-pbs-newshour/
import urllib2
import zlib
UTF8 = 'utf-8'
USERAGENT = """Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36"""
httpHeaders = {'User-Agent': USERAGENT,
               'Accept': "application/json, text/javascript, text/html,*/*",
               'Accept-Encoding': 'gzip,deflate,sdch',
               'Accept-Language': 'en-US,en;q=0.8'
               }

# Get HTML content
# https://danvatterott.com/blog/2017/03/11/my-first-kodi-addon-pbs-newshour/
def getRequest(url, udata=None, headers=httpHeaders):
    req = urllib2.Request(url.encode(UTF8), udata, headers)
    try:
        response = urllib2.urlopen(req)
        page = response.read()
        if response.info().getheader('Content-Encoding') == 'gzip':
            page = zlib.decompress(page, zlib.MAX_WBITS + 16)
        response.close()
    except Exception:
        page = ""
        xbmc.log(msg='REQUEST ERROR', level=xbmc.LOGDEBUG)
    return(page)
# end of monday work!

""" next
    a. git !
    0. systématiser l'utilisation de la fonction getRequest
    1. ordonner la liste par horaire
    2. capturer le vs et le V
    3. présenter les tags ds acestreamns sur la gauche
    4. gérer les exceptions
 """

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
# config(): get the logger/handler & set leve to DEBUG - https://github.com/xbmc/generator-kodi-addon/blob/master/generators/app/templates/resources/lib/kodilogging.py
kodilogging.config()
# Routing addon - https://github.com/tamland/kodi-plugin-routing
plugin = routing.Plugin()
# Acestream launch link (Plexus)
AS_LAUNCH_LINK = 'XBMC.RunPlugin(plugin://program.plexus/?mode=1&url={url}&name={name})'

# Get reddit soccser streams
#_response = requests.get('https://www.reddit.com/r/soccerstreams/', headers = {'User-agent': 'myplugin'})
_response = getRequest("https://www.reddit.com/r/soccerstreams/")
_content = _response
_pattern = re.compile(r'\[[0-9].*vs.*<\/h2', re.UNICODE)
_urlLinkPattern = re.compile(r'[\w]*\/[0-9]([a-z0-9A-Z%_])*_vs_[\w]*', re.UNICODE)
_streamLinkPattern = re.compile(r'(\[[a-zA-Z0-9_\[\] ]*\] )?acestream:\/\/\w+ *(\[[a-zA-Z0-9_\[\] ]*\])?', re.UNICODE)
_acePattern = re.compile(r'acestream:\/\/\w+', re.UNICODE)
_tagsPattern = re.compile(r'\[[a-zA-Z0-9_\[\] ]*\]', re.UNICODE)

@plugin.route('/')
def index():
    # Initial matches parsing
    for m in _pattern.finditer(_content):
        _title = m.group()[:-4]
        _segment = _content[m.end() - 250:m.end()-4]
        _link = _urlLinkPattern.search(_segment).group(0).replace("/", "-")    
        addDirectoryItem(plugin.handle, plugin.url_for(show_category, _link), ListItem(_title), True)
    
    endOfDirectory(plugin.handle)
 
@plugin.route('/category/<category_id>')
def show_category(category_id):
    # Constructs URL   
    _matchURL = "https://www.reddit.com/r/soccerstreams/comments/" + category_id + "/"
    _matchURLDecoded = _matchURL.replace("-", "/")
    # Gather stream links    
    #_responseDetails = requests.get(_test, headers = {'User-agent': 'your bot 0.2'})
    _responseDetails = getRequest(_matchURLDecoded)
    _contentDetails = _responseDetails
    _iterator = _streamLinkPattern.finditer(_contentDetails)
    _list = []

    for j in _iterator:
        _list.append(j.group())
        print("link: " + j.group())

    _streamList = list(set(_list))

    for _sl in _streamList:
        print("stream link: " + str(_sl))
        _tags = _tagsPattern.search(_sl)
        _tag = _tags.group(0)
        # Last paramter 'isFolder' to False
        addDirectoryItem(plugin.handle, plugin.url_for(show_categoryDetails, ""+_sl.replace("/", "-")), ListItem("" + _tag), False)
        
    endOfDirectory(plugin.handle)
"""         for u in _tags:
            print("tags: " + str(u)) """

@plugin.route('/categoryDetails/<categoryDetails_id>')
def show_categoryDetails(categoryDetails_id):
    # Launch the stream    
    _stream = categoryDetails_id.replace("-", "/")
    print(_stream)
    #_acepattern = re.compile(r'acestream:\/\/\w+', re.UNICODE)
    _stream = _acePattern.search(_stream).group(0)
    try:
        xbmc.executebuiltin(AS_LAUNCH_LINK.format(url=_stream, name='spiv'))
    except Exception:        
        xbmc.log(msg='PLESUS ERROR', level=xbmc.LOGDEBUG)     

    endOfDirectory(plugin.handle)

def run():
    plugin.run()