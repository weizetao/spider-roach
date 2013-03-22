#!/usr/bin/env python
#-*-coding:utf-8-*-
import redis
import sys
import MySQLdb

#配置redis
def getRedis(db=0):
    return redis.StrictRedis(host='localhost', port=6379, db=db)

def getMysql():
    return MySQLdb.connect(host='192.168.9.241',\
            user='test',passwd='123456',db="spider_db",port=9300,charset="utf8")

#加载映射表
def get_Maps():
    map_file = open("./maps.cfg", "r")
    str = map_file.read()
    map_file.close()
    try:
        d = eval(str)
    except:
        print 'The Maps config is error! Please check it.'
        sys.exit()
    return d

