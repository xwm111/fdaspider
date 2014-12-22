#!/usr/bin/python
# coding=utf-8
"""
获取单个页面的ID,并存入各自的ini文件
"""
from bs4 import BeautifulSoup
import httplib
import ConfigParser
import sys

filename = sys.argv[1]

config = ConfigParser.ConfigParser()
config.readfp(open("config.ini"))
tableId = config.get("%s" % filename, "tableId")
page = config.get("%s" % filename, "page")

ids = []
for current in range(1, (int(page)+1)):
    url = 'http://app1.sfda.gov.cn/datasearch/face3/search.jsp?tableId=%s&curstart=%s' % (tableId, current)
    print url
    conn = httplib.HTTPConnection("app1.sfda.gov.cn")
    conn.request("GET", url)
    r1 = conn.getresponse()
    strings = r1.read()
    soup = BeautifulSoup(strings)

    for link in soup.find_all('a'):
        temp = link.get('href')
        temp = temp.partition("&Id=")
        drugId = temp[2].partition("'")
        ids.append(drugId[0])
    print 'page %s finish ' % current
print ids

savedids = ','.join(ids)
config = ConfigParser.ConfigParser()
config.optionxform = str
configFile = open('%s_Ids.ini' % filename, 'wb')
config.add_section("%sIds" % filename)
config.set("%sIds" % filename, "tableId", tableId)
config.set("%sIds" % filename, "ids", savedids)

config.write(configFile)
configFile.close()


