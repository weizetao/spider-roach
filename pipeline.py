#!/usr/bin/env python
#-*- coding: utf-8 -*-
#------------------------------------------------------
#file:pipelines.py
#desc:Parse the html , extract the link and pageinfo
#author:we.agathe@gmail.com
#------------------------------------------------------
import sys
import urlparse
import re
from lxml import etree
from base import BaseParse
from base import BaseDb


class Parse_url(BaseParse):
    def __init__(self,list):
        self.parser = etree.HTMLParser(encoding = 'utf-8')
        self.db = BaseDb()
        self.db.connectdb()
        self.url_list = list['url']
        self.url_set = list['url_set']

    def parse(self, url, page,threadName):
        #Match extraction rules
        rule = self.findrules(url)
        if not rule:
            print 'Not found xpath:' + url 
            self.db.exception(url, 1)#No matched
            return False

        #extraction information with regular 
        if 'page_re' in rule:
            self.extract_re(rule, url, page)
            return True

        #Make DOM of html page
        try:
            self.html = etree.HTML(page, self.parser)
        except:
            print sys.exc_info()[0],url
            return False

        self.crawled = 'crawled_set'
        if 'crawled' in rule:
            self.crawled = rule['crawled']

        #extraction information with xpath
        if 'link_xpath' in rule:
            self.extract_link(rule)

        if 'page_xpath' in rule:
            if not self.extract_page_xpath(rule, url):
                return True

        if 'extra' in rule:
            self.doextra(rule, url)

        self.url_set.crawled(url, self.crawled)
        return True

    def doextra(self, rule, url):
        try:
            tmp = eval(rule['extra'])
            tmp += '&table=%s&url=%s' % (rule['table'], url)
            self.url_list.lpush(tmp)
        except:
            return None

    def geturlparam(self, url, param):
        result = urlparse.urlparse(url)
        return urlparse.parse_qs(result.query, True)[param][0] 
    
    def extract_link(self, rule):
        pre_url = ''
        if 'pre_url' in rule: pre_url = rule['pre_url']
        for lx in rule['link_xpath']:
            urls = self.html.xpath(lx)
            for i in urls:
                #save the url to the queue of linkbase
                if i[0] == '/': 
                    tmp = pre_url + i
                elif i.find('http://') == 0:
                    tmp = i
                else:
                    tmp = pre_url + '/' + i
                if not self.url_set.exist(tmp, self.crawled):
                    print 'push into url_list:' + tmp
                    self.url_list.push(tmp)
                    self.url_set.insert(tmp, self.crawled)

    def extract_page_xpath(self, rule, url):
        self.item.clear()
        self.item['url'] = url
        try:
            for k,v in rule['page_xpath'].items():
                self.add_xpath2(k, v)

            if self.item['name'] == '0':
                if 'page_xpath2' in rule:
                    self.item.clear()
                    self.item['url'] = url
                    for k,v in rule['page_xpath2'].items():
                        self.add_xpath2(k, v)
                    if self.item['name'] == '0':
                        self.db.exception(url, 2)
                        return False
                else:
                    self.db.exception(url, 2) 
                    return False
        except:
            info=sys.exc_info()
            print info[0],":---",info[1]
            self.db.exception(url, 2) 
            return False

            
        #save the information into mysql
        if self.url_set.isnewpage(url, self.crawled):#insert
            sql = self.db.sql_insert(rule['table'], self.item)
            if self.db.execsql(sql):
                return True
            else:
                self.db.exception(url, 3)
                return False

        else:#update
            sql = self.db.sql_update(rule['table'], self.item)
            if self.db.execsql(sql):
                return True
            else:
                self.db.exception(url, 4)
                return False
        

    def extract_re(self, rule, url, page):
        self.item.clear()
        try:
            self.item['url'] = self.geturlparam(url,'url')
            table = self.geturlparam(url, 'table')
        except:
            self.db.exception(url, 5)
            return False

        for k,v in rule['page_re'].items():
            self.item[k] = self.search(v, page)

        sql = self.db.sql_update(table, self.item)
        if not self.db.execsql(sql):
            self.db.exception(url, 5)

    def search(self, pe, str):
        result = re.search(pe, str)
        if result:
            return result.group(1)
        else:
            return None


