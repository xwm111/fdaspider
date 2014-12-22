#!/usr/bin/python
# coding=utf-8
__author__ = 'xuweiming'

import httplib
import threading
import os
import sys


urltype = sys.argv[1]

#药品地址
URL = ""

#国产药品地址
gcypURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=25&tableName=TABLE25&tableView=%%B9%%FA%%B2%%FA%%D2%%A9%%C6%%B7&Id=%d"

#国产药品商品名地址
gcypspmURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=32&tableName=TABLE32&tableView=%%B9%%FA%%B2%%FA%%D2%%A9%%C6%%B7%%C9%%CC%%C6%%B7%%C3%%FB&Id=%d"

#进口药品地址
jkypURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=36&tableName=TABLE36&tableView=%%BD%%F8%%BF%%DA%%D2%%A9%%C6%%B7&Id=%d"

#进口药品商品名地址
jkypspmURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=60&tableName=TABLE60&tableView=%%BD%%F8%%BF%%DA%%D2%%A9%%C6%%B7%%C9%%CC%%C6%%B7%%C3%%FB&Id=%d"

#药品生产企业
ypscqyURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=34&tableName=TABLE34&tableView=%%D2%%A9%%C6%%B7%%C9%%FA%%B2%%FA%%C6%%F3%%D2%%B5&Id=%d"

#药品经营企业
ypjyqyURL = "http://app1.sfda.gov.cn/datasearch/face3/content.jsp?tableId=41&tableName=TABLE41&tableView=%%D2%%A9%%C6%%B7%%BE%%AD%%D3%%AA%%C6%%F3%%D2%%B5&Id=%d"



class myThread(threading.Thread):
    def __init__(self, threadID,folderName,URL, startID, endID):
        if not os.path.isdir(folderName):
            os.makedirs(folderName)
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.folderName = folderName
        self.URL = URL
        self.startID = startID
        self.endID = endID

    def run(self):
        conn = httplib.HTTPConnection("app1.sfda.gov.cn")
        for i in range(self.startID, self.endID):
            conn.request("GET",self.URL % (i))
            r1 = conn.getresponse()
            f = open("%s/%d.html" % (self.folderName, i), 'w')
            f.write(r1.read())
            f.close()
            print "threadID:-%s file %d saved" % (self.threadID,i)
        conn.close()


threads = []

if urltype == "1":
    for i in range (1,10):
        threads.append(myThread("%d" % i,"国产药品",gcypURL, (i-1)*2000, i*2000))
if urltype == "2":
    for i in range (1,20):
        threads.append(myThread("%d" % i,"国产药品商品名",gcypspmURL, (i-1)*2000, i*2000))
if urltype == "3":
    for i in range (100,101):
        threads.append(myThread("%d" % i,"进口药品",jkypURL, (i-1)*2000, i*2000))
if urltype == "4":
    for i in range (100,101):
        threads.append(myThread("%d" % i,"进口药品商品名",jkypspmURL, (i-1)*2000, i*2000))
if urltype == "5":
    for i in range (100,101):
        threads.append(myThread("%d" % i,"药品生产企业",ypscqyURL, (i-1)*2000, i*2000))
if urltype == "6":
    for i in range (100,101):
        threads.append(myThread("%d" % i,"药品经营企业",ypjyqyURL, (i-1)*2000, i*2000))

for i in threads:
    i.start()

for t in threads:
    t.join()
print "Exiting Main Thread"








