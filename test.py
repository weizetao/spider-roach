#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
from lxml import etree
import re
import StringIO
import string
import urllib2
import time
import gzip
import urlparse
import json
from Logger import Logger
reload(sys)
sys.setdefaultencoding('utf-8')

import redis

#---------get---html--------------
def get_source(source):
    if source.find('p://') > 0:
        req = urllib2.Request(source)
        # req.add_header('Accept-Encoding','gzip')
        retval = urllib2.urlopen(req)
        if retval.headers.has_key('content-encoding'):
            fileobj = StringIO.StringIO()
            fileobj.write(retval.read())
            fileobj.seek(0)
            gzip_file = gzip.GzipFile(fileobj=fileobj)
            context = gzip_file.read()
        else:
            context = retval.read()
        return context


if __name__ == "__main__":

    # str = 'date:\n{"state":"100","data":[{"url":"/HotelInfo-222.html","hotalName":"香港九龙香格里拉酒店","price":"2300"}]}'
    # result = re.search('\"price\":\"(.*)\"', str)
    # print result.group(1)
    # file = open("./maps.cfg","r")
    # str = file.read()
    # print str
    # js = json.dumps(str)
    # js2 = json.loads(js)

    # for k,v in js2.items():
        # print k,v
    # print eval(str)

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    url = 'http://www.17u.cn/HotelInfo-%d.html'
    for i in range(1,70000):
        tmp = url % (i)
        r.rpush('url_list', tmp)

    # r.hset('kaixin.com','pxpath','{"name":"//div[@class=\'info\']/div/text()",}')
    # tmp = r.hgetall('kaixin.com')
    # print tmp
    # r = redis.Redis(host='localhost', port=6379, db=0)
    # print r.set('foo','baga')
    # r.rpush('url_list','http://www.baidu.com')
    # print r.lpop('url_list')
    # print r.llen('url_list') == 0
    # print r.get('foo')
    # tmp = r.zadd('pagerank', 2.2, 'google.com')
    # print r.zscore('pagerank', 'sss.com')

    # pipe = r.pipeline()

    # pipe.set('alia','soga')
    # pipe.set('zoulong','mina')

    # pipe.get('alia')
    # pipe.get('zoulong')
    # pipe.get('foo')
    # print pipe.execute()



