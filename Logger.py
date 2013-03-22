#!/usr/bin/env python
#-*- coding: utf-8 -*-
#------------------------------------------------------
#file:logger.py
#desc: Record log information
#author:we.agathe@gmail.com
#------------------------------------------------------
import sys
import traceback
import time
import os
'''
类名:         Logger
功能描述:    打印输出到日志中
调用模块:    sys模块
作 者:未知
'''

try:
    class Logger(object):
        ft = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))
        day =time.strftime("%Y%m%d", time.localtime(time.time()))# 记录当天日志到子目录
        path = './logs'
        if not os.path.exists(path):
            #os.makedirs(path.decode('utf8','ignore').encode(sys.getfilesystemencoding()))
            os.makedirs(path)
        fn = os.path.join(path,'log-%s.txt') % ft
        _file = None

        def checktime(self, mytime):
            today = time.strftime("%Y%m%d", mytime)# 
            if today != self.day:
                ft = time.strftime("%Y%m%d-%H%M%S", mytime)
                self.fn = os.path.join(path,'log-%s.txt') % ft
                self.day = today
                self._file.close()
                self._file = None

        def write(self, s):
            curent_time = time.localtime(time.time())
            self.checktime(curent_time)
            if self._file is None:
                try:
                    self._file= open(Logger.fn,'a')
                except:
                    traceback.print_exc()
            if self._file is not None:
                t = '['+ time.strftime("%Y-%m-%d %H:%M:%S", curent_time) +']'
                txt = s.replace('\n','')
                txt = txt.replace('\r','')
                c=t + s + '\n'
                try: 
                    self._file.write(c.decode('utf8'))
                    self._file.flush()
                except: 
                    self._file.write(c)
                    self._file.flush()

        def flush(self):
            if self._file is not None:
                self._file.flush()

    mylogger = Logger()
    # sys.stdout = mylogger
    # sys.stderr = mylogger

except:
    traceback.print_exc()
