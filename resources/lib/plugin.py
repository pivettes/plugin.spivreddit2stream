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
_content = _response._content
_pattern = re.compile(r'\[[0-9].*vs.*<\/h2', re.UNICODE)
_patternLink = re.compile(r'[\w]*\/[0-9]([a-z0-9A-Z%_])*_vs_[\w]*', re.UNICODE)
_list = _pattern.findall(_content.decode('utf8'))
_listLink = _patternLink.findall(_content.decode('utf8'))

""" _content[m.end() - 250:m.end()-4] """

""" for m in _pattern.finditer(_content):
    _title = m.group()[:-4]
    print("title: " + _title)
    _int1 = _content[m.end() - 250:m.end()-4]
    print("int1: " + _int1)
    _link = _patternLink.search(_int1).group(0).replace("/", "-")    
    print("link: " + _link)
    print(m.start())
    print(m.span())
    print(m.group())
    print(_content[m.end() - 250:m.end()-4]) """

"""     _link = _patternLink.search().group(0)
    print(_link) """



@plugin.route('/')
def index():

    for m in _pattern.finditer(_content):
        _title = m.group()[:-4]
        print("title: " + _title)
        _int1 = _content[m.end() - 250:m.end()-4]
        print("int1: " + _int1)
        _link = _patternLink.search(_int1).group(0).replace("/", "-")    
        print("link: " + _link)
        print(m.start())
        print(m.span())
        print(m.group())
        print(_content[m.end() - 250:m.end()-4])

        addDirectoryItem(plugin.handle, plugin.url_for(show_category, _link), ListItem(_title), True)
    
    print("end of for")
    endOfDirectory(plugin.handle)

"""     i = 0
    while i < len(_list):
        addDirectoryItem(plugin.handle, plugin.url_for(show_category, ""+_listLink[i].replace("/", "-")), ListItem(""+_list[i][:-4]), True)
        logger.debug("" + str(i) + " - "+_listLink[i].replace("/", "-"))
        logger.debug("" + str(i) + " - "+_list[i][:-4])
        i += 1 """
    
    


@plugin.route('/category/<category_id>')
def show_category(category_id):
    dialog = xbmcgui.Dialog()
    _pat = "https://www.reddit.com/r/soccerstreams/comments/" + category_id + "/"
    _test = _pat.replace("-", "/")
    print("URLM: " + _test)

    _responseDetails = requests.get(_test, headers = {'User-agent': 'your bot 0.2'})
    _contentDetails = _responseDetails.content
    #_listDetails = re.findall(r'\[[a-zA-Z0-9_\[\] ]*\] acestream:\/\/\w+', _contentDetails)
    #_finallist = list(set(_listDetails))

    #if len(_finallist) > 0:
    #    for x in _finallist:
    #        addDirectoryItem(plugin.handle, plugin.url_for(show_categoryDetails, ""+x.replace("/", "-")), ListItem(""+x), True)    

    #_acepattern = re.compile(r'acestream:\/\/\w+', re.UNICODE)
    #_matchObj = _heeuuu.search("[hfghfghf] acestream://ea3a0915d8530e49de0b8e5c3fb60f7acd66c923")
    #dialog = xbmcgui.Dialog()
    #if _matchObj:
    #    _ok = dialog.ok("heu", _acepattern.search("[hfghfghf] acestream://ea3a0915d8530e49de0b8e5c3fb60f7acd66c923").group(0))
    #else:
    #    _ok = dialog.ok("heu", "no match!")

    _patternLink2 = re.compile(r'acestream:\/\/\w+ *(\[[a-zA-Z0-9_\[\] ]*\])?', re.UNICODE)
    for nm in _patternLink2.finditer(_contentDetails):
        print("_listDetails: " + nm.group())
        addDirectoryItem(plugin.handle, plugin.url_for(show_categoryDetails, ""+nm.group().replace("/", "-")), ListItem(""+nm.group()), False)
    endOfDirectory(plugin.handle)
"""     _listDetails = re.findall(r'acestream:\/\/\w+ (\[[a-zA-Z0-9_\[\] ]*\])?', _contentDetails)
    print("_contentDetails: " + _contentDetails)
    for n in _listDetails:
        print("_listDetails: " + n)

    _finallist = list(set(_listDetails))

    if len(_finallist) > 0:
        for x in _finallist:
            addDirectoryItem(plugin.handle, plugin.url_for(show_categoryDetails, ""+x.replace("/", "-")), ListItem(""+x), True)
            print("finallist: " + x)
 """


    

@plugin.route('/categoryDetails/<categoryDetails_id>')
def show_categoryDetails(categoryDetails_id):
    
    #dialog = xbmcgui.Dialog()
    #_ok = dialog.ok("heu", categoryDetails_id.replace("-", "/"))

    _stream = categoryDetails_id.replace("-", "/")
    _acepattern = re.compile(r'acestream:\/\/\w+', re.UNICODE)
    _stream = _acepattern.search(_stream).group(0)

    try:
        xbmc.executebuiltin(AS_LAUNCH_LINK.format(url=_stream, name='spiv'))
    except Exception as inst:
        #log(inst)   
        res = "no"        

    endOfDirectory(plugin.handle)

def run():
    plugin.run()
