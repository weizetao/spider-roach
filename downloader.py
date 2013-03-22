#!/usr/bin/env python
#-*- coding: utf-8 -*-
#------------------------------------------------------
#file:downloader.py
#desc:download the web page
#author:weizetao@pica.com
#date:2012-08-30
#------------------------------------------------------
import urllib2
import time
import StringIO
import string
import gzip

#---------get---html--------------
def get_source2(source):
    if source.find('p://') > 0:
        try:
            req = urllib2.Request(source)
            req.add_header('Accept-Encoding','gzip')
        except:
            return None

        try:
            retval = urllib2.urlopen(req)
        except:
            return None
        try:
            if retval.headers.has_key('content-encoding'):
                fileobj = StringIO.StringIO()
                fileobj.write(retval.read())
                fileobj.seek(0)
                gzip_file = gzip.GzipFile(fileobj=fileobj)
                context = gzip_file.read()
            else:
                context = retval.read()
        except:
            return None

        return context
    return None

def get_source(source):
    time.sleep(5)
    if source.find('p://') > 0:
        try:
            req = urllib2.Request(source)
            req.add_header('Accept-Encoding','gzip')
        except:
            return None

        try:
            retval = urllib2.urlopen(req)
        except:
            return None
        try:
            if retval.headers.has_key('content-encoding'):
                fileobj = StringIO.StringIO()
                fileobj.write(retval.read())
                fileobj.seek(0)
                gzip_file = gzip.GzipFile(fileobj=fileobj)
                context = gzip_file.read()
            else:
                context = retval.read()
        except:
            return None

        return context
    return None

