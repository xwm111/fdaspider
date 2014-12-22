#!/usr/bin/python
#coding=utf-8
"""
根据id数量，开启5个线程进行同时下载
"""
__author__ = 'xuweiming'

import httplib
import threading
import os
import ConfigParser
import codecs
import sys

contentType = sys.argv[1]
#contentType = '国产药品商品名'
URL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=%s&tableName=TABLE%s&Id=%s"
cfgFile="%s_Ids.ini" % contentType
config = ConfigParser.ConfigParser()
config.readfp(open(cfgFile, "r"))
section = "%sIds" % contentType
ids = config.get(section, "ids")
tableId = config.get(section, "tableId")
tableIdArr = ids.split(',')
idLength = len(tableIdArr)
threadSize = 4
perThreadSize = idLength/threadSize

if not os.path.isdir(contentType):
        os.makedirs(contentType)

if perThreadSize*threadSize < idLength:
    remainArr = tableIdArr[perThreadSize*threadSize:]
    conn = httplib.HTTPConnection("app1.sfda.gov.cn")
    for i in remainArr:
        conn.request("GET", URL % (tableId, tableId, i))
        r1 = conn.getresponse()
        f = open("%s/%s.html" % (contentType, i), 'w')
        f.write(r1.read())
        f.close()
        print "remain file %s.html saved" % i
    conn.close()





class myThread(threading.Thread):
    def __init__(self, threadID, folderName, idarr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.folderName = folderName
        self.idarr = idarr

    def run(self):
        conn = httplib.HTTPConnection("app1.sfda.gov.cn")
        for i in self.idarr:
            conn.request("GET", URL % (tableId, tableId, i))
            r1 = conn.getresponse()
            f = open("%s/%s.html" % (self.folderName, i), 'w')
            f.write(r1.read())
            f.close()
            print "threadID:-%s file %s.html saved" % (self.threadID, i)
        conn.close()

threads = []


for i in range(0, threadSize):
    threads.append(myThread("%d" % i, contentType, tableIdArr[i*perThreadSize:((i+1)*perThreadSize)]))

for i in threads:
    i.start()

for t in threads:
    t.join()
print "Exiting Main Thread"