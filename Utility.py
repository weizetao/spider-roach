#!/usr/bin/env python
#-*- coding:UTF-8 -*-

from collections import deque
#import threading
import time

class DQueue:
    def __init__(self, redis, list):
        self.lb = redis
        self.list = list
        # self.mutex = threading.Lock()

    def push(self, item):
        # self.mutex.acquire()
        # self.queue.push(item)
        self.lb.rpush(self.list,item)
        # self.mutex.release()
    def lpush(self, item):
        self.lb.lpush(self.list,item)

    def pop(self):
        # self.mutex.acquire()
        # tmp = self.queue.popleft()
        return self.lb.lpop(self.list)
        # self.mutex.release()

    def empty(self):
        len = self.lb.llen(self.list)
        return len == 0

    def len(self):
        return self.lb.llen(self.list)


class Record:
    def __init__(self,redis,key):
        self.lb = redis
        self.key = key

    def insert(self, item, key):
        return self.lb.zadd(key, 1, item)

    def isnewpage(self, item, key):
        tmp = self.lb.zscore(key, item)
        if not tmp or tmp == 1:
            return True
        else:
            return False

    def crawled(self, item, key):
        score = time.time()
        self.lb.zadd(key, score, item)
    
    def delete(self, item, key):
        return self.lb.zrem(key, item)

    def exist(self, item, key):
        return self.lb.zscore(key, item)

    # def counts(self):
        # return self.count
