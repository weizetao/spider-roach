#!/usr/bin/env python
#-*- coding: utf-8 -*-
#------------------------------------------------------
#file:Base.py
#desc:base class of Parse
#author:we.agathe@gmail.com
#------------------------------------------------------
import time
import sys
import re
import MySQLdb
import threading
from settings import getMysql
from downloader import get_source

global url_maps
url_maps = {}


class BaseDb():
    db = None
    def connectdb(self):
        try:
            self.db = getMysql()
            print 'connect to the dbserver !'
        except:
            print ":failed connected to db!"
        return self.db

    def execsql(self,sql):
        """execute the sql"""
        cursor=self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            info=sys.exc_info()
            print info[0],":---",info[1]
            self.connectdb()
            return False
    
        cursor.close()
        return True

    def __del__(self):
        self.db.close()

    def escapeString(self, s):
        if s is None:
            return 'NULL'
        elif isinstance(s, basestring):
            return '"%s"' % (s.replace('\\','\\\\').replace('"','\\"'))
        else:
            return str(s)

    def sql_insert(self, table, d):
        #construct INSERT SQL
        ks = ",".join(d.keys())
        vs = ",".join([self.escapeString(v) for v in d.values()])
        sql = 'insert into %s (%s) values (%s)' % (table,ks,vs)
        return sql

    def sql_update(self, table, d, key_name='url', renew=2):
        # construct UPDATE SQL
        key_value = d.pop(key_name)
        tmp = ''
        for k,v in d.items():
            tmp += ' `%s`=%s,' % (k, self.escapeString(v))
        sql = 'update %s set %s renew=%d where `%s`="%s"' % (table,tmp,renew,key_name,key_value)
        return sql

    def exception(self, url, type):
        #type: 0-fail to get the page
        #  1-No matching rules
        #  2-infomation extraction failure
        #  3-insert into db failure
        #  4-update db failure
        #  5-json infomation extraction failure
        #  6-failed to write file
        #  7-Error pages
        #  8-Error code of http response(http's 403、404)
        sql = "insert into spider_exception (url,time,type) values ('%s', now(), %s)" % (url, type)
        print "[exception]type=%s,url=%s" % (type,url)
        self.execsql(sql)

    def query(self, sql, record_callback):
        cur = self.db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        numrows = int(cur.rowcount)
        for i in range(numrows):
            fields = cur.fetchone()
            record_callback(fields)

class BaseParse():
    html = None
    item = {}
    
    def findrules(self,url):
        """Return the corresponding selection rules"""
        for k,v in url_maps.items():
            if re.match(k, url):
                return v
        return None

    def add_xpath2(self, name, xpath, split='|'):
        self.item[name] = '0'
        tmp = self.html.xpath(xpath)
        if not tmp:
            return False
        str = ''
        rlen = len(tmp)
        for i in range(0,rlen-1):
            temp = tmp[i].rstrip().lstrip()
            if not temp: continue
            str += temp + split
        str += tmp[rlen-1].rstrip().lstrip()
        self.item[name] = str
        return True

    def add_xpath(self, name, xpath):
        self.item[name] = ' '
        tmp = self.html.xpath(xpath)
        if tmp:
            self.item[name] = tmp[0].rstrip().lstrip()
        else:
            return False
        return True

    def get_id(self, url, str):
        pos = url.find(str) + len(str) 
        url_len = len(url)
        pos_end = pos
        while pos_end < url_len:
            if url[pos_end].isdigit():
                pos_end += 1
                continue
            else:
                break
        if pos > 0 and pos_end > pos:
            return url[pos:pos_end]
        else:
            return '0'


class spider_thread(threading.Thread):
    def __init__(self, threadName, list, pipename):
        threading.Thread.__init__(self, name = threadName)
        self.url_list = list['url']
        m = __import__('pipeline')
        c = getattr(m, pipename)
        self.pipeline = c(list)
    def run(self):
        while True:
            if self.url_list.empty():
                time.sleep(3)
                continue

            url = self.url_list.pop()
            if not url:
                continue

            print '['+self.getName()+']'+'[pop]'+str(self.url_list.len())+ "[get]"+url
            page = get_source(url)
            if page == None:
                self.url_list.push(url)
                print '['+self.getName()+']'+'[push]'+str(self.url_list.len())+ "[get source error:]"+url
                continue

            if not self.pipeline.parse(url, page, self.getName()):
                print '['+self.getName()+']'+'[push]'+str(self.url_list.len())+ "[parse error:]"+url
                self.url_list.push(url)

class BaseSpider():
    rules = [ ] 
    def __init__(self):
        self.Rules()
    def __Rules(self):
        pass
    def AddRules(self, list, pipe, name='Unkonwn', threadsize=1):
        """Add extraction rules"""
        self.rules += [{'name':name,'list':list,'pipe':pipe, 'threadsize':threadsize},]

    def scheduling(self):
        pass

    def start(self):
        for ru in self.rules:
            threadList = []
            for i in xrange(ru['threadsize']):
                threads = spider_thread(ru['name']+str(i), ru['list'], ru['pipe'])
                threadList.append(threads)
            for i in threadList:
                i.setDaemon(True)
                i.start()
        try:
            self.scheduling()
        except:
            print 'quit.'

