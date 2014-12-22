#!/usr/bin/python
# coding=utf-8
"""
在dir页面查询各类别的页面数量
"""

from bs4 import BeautifulSoup
import httplib
import math
import ConfigParser
import string

print '开始更新记录数'
url = 'http://app1.sfda.gov.cn/datasearch/face3/dir.html'
conn = httplib.HTTPConnection("app1.sfda.gov.cn")
conn.request("GET", url)
r1 = conn.getresponse()
strings = r1.read()
soup = BeautifulSoup(strings)
soup.prettify()

config = ConfigParser.ConfigParser()
config.optionxform = str
configFile = open('config.ini', 'wb')

pagesize = 15
for link in soup.find_all('a'):
    name = link.contents[0]
    if name == '国产药品'.decode('utf-8'):
        tableString = link['href'].partition('tableId=')
        tableId = tableString[2].partition('&tableName=')[0]
        page = link.contents[1].contents[0]
        page = page.replace('(', '').replace(')', '')
        config.add_section("国产药品")
        config.set("国产药品", "tableId", tableId)
        config.set("国产药品", "page", int(math.ceil(string.atof(page) / pagesize)))
    if name == '国产药品商品名'.decode('utf-8'):
        tableString = link['href'].partition('tableId=')
        tableId = tableString[2].partition('&tableName=')[0]
        page = link.contents[1].contents[0]
        page = page.replace('(', '').replace(')', '')
        config.add_section("国产药品商品名")
        config.set("国产药品商品名", "tableId", tableId)
        config.set("国产药品商品名", "page", int(math.ceil(string.atof(page) / pagesize)))
    if name == '进口药品商品名'.decode('utf-8'):
        tableString = link['href'].partition('tableId=')
        tableId = tableString[2].partition('&tableName=')[0]
        page = link.contents[1].contents[0]
        page = page.replace('(', '').replace(')', '')
        config.add_section("进口药品商品名")
        config.set("进口药品商品名", "tableId", tableId)
        config.set("进口药品商品名", "page", int(math.ceil(string.atof(page) / pagesize)))
    if name == '进口药品'.decode('utf-8'):
        tableString = link['href'].partition('tableId=')
        tableId = tableString[2].partition('&tableName=')[0]
        page = link.contents[1].contents[0]
        page = page.replace('(', '').replace(')', '')
        config.add_section("进口药品")
        config.set("进口药品", "tableId", tableId)
        config.set("进口药品", "page", int(math.ceil(string.atof(page) / pagesize)))
config.write(configFile)
configFile.close()

print '更新记录数完毕'