#coding:utf-8
#author: beilianghsizi
#file: Urllib2.py
#time: 2017/12/26 15:15
#desc: "urllib2的测试脚本"

import urllib2,re
from lxml import etree


def translate_by_re(str):
    tags = re.findall(r'\"/home/[a-zA-z]+/',str)
    for i in tags:
        print i

response = urllib2.urlopen('http://www.talkwithtrend.com/Article/178081')
html = response.read()
ht = etree.HTML(html)
httext = ht.xpath("//div[@class='articleM_body markdown-body editormd-html-preview']")[0]
hto = etree.tostring(httext)
# print re.sub(r'\"/home/[a-zA-z]+/',)
hto.replace("r'\"/home/[a-zA-z]+/'","")
print hto.encode("utf-8")