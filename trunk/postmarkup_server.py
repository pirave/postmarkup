"""This is a WSGI server that runs a very simple application to test Postmarkup

You can find it on http://postmarkup.willmcgugan.com

"""

import postmarkup
import os
try:
    from fs.osfs import OSFS
except ImportError:
    print "Get PyFilesystem from http://code.google.com/p/pyfilesystem/"
    raise


def application(environ, start_response):
    fs = OSFS('./')
    path = environ["PATH_INFO"]    
    if path in ("", "/"):        
        path = "index.htm"
    if path == "/getbbcode":
        bbcode = unicode(environ["wsgi.input"].read(), 'utf-8')
        html = postmarkup.render_bbcode(bbcode, clean=True)
        start_response("200 OK", [])
        return [html]
    if not fs.isfile(path):
        start_response("404 NOT FOUND", [])
        return ["Nobody here but us chickens"]
    start_response("200 OK", [])    
    return [fs.getcontents(path)]
    
        
if __name__ == "__main__":
    from paste import httpserver
    httpserver.serve(application)
