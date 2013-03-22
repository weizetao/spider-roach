#!/usr/bin/env python
#-*- coding: utf-8 -*-
#------------------------------------------------------
#file:scheduler.py
#desc:the scheduler of spider
#author:we.agathe@gmail.com
#------------------------------------------------------
from Utility import DQueue,Record
from base import BaseSpider,url_maps
from pipeline import *
import time
import signal
import base
from settings import getRedis,get_Maps

class test_spider(BaseSpider):
    def Rules(self): 
        print 'test ok!'

class roach(BaseSpider):

    def Rules(self):
        #linkbase
        linkbase = getRedis()

        url_list = DQueue(linkbase,'url_list')
        url_set = Record(linkbase, 'crawled_set')

        base.url_maps = get_Maps()
        signal.signal(60, self.reload_handler)

        list = {
            'url':url_list,
            'url_set':url_set,
        }

        self.AddRules(list, 'Parse_url', 'url', 10)

    def scheduling(self):
        """调度策略"""
        while 1:
            time.sleep(5)
            # url_list.push(start_url)

    def reload_handler(self,signum,frame):
        tmp = get_Maps()
        if tmp:
            base.url_maps = tmp
            print 'reload the maps config file ok ...'
            print base.url_maps
        else:
            print 'reload the maps config file failed ...'

