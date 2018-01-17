#coding:utf-8
#author: beilianghsizi
#file: WebCommon.py
#time: 2017/12/25 10:11
#desc: ""

import urllib2
import urllib
import cookielib
import poster
class WebTool:
    Opener=None
    FileOpener=None
    Cookie=None
    #浏览器参数
    UserAgent="Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11D201 UCBrowser/10.7.5.650 Mobile"
    Referer=None
    Host=None


    def __init__(self):
        self.Cookie = cookielib.CookieJar()
        self.Opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.Cookie))
        self.Opener.addheaders = [("User-Agent",self.UserAgent)]
        #print "WebTool 初始化成功"
    def reload_haders(self):
        del self.Opener.addheaders

        self.Opener.addheaders = [('User-agent',self.UserAgent),("Referer",self.Referer),("Host",self.Host),("Accept","	*/*")]

    def set_host(self,url):
        proto, rest = urllib.splittype(url)
        res, rest = urllib.splithost(rest)
        self.Host=res
        self.reload_haders()

    def getdata(self,url,trytime=5):

        self.set_host(url)
        #获取网页并设置refer
        Flg=trytime
        op=""
        while Flg:
            try:
                op=self.Opener.open(url,timeout=20)
                #print op.info()
                op=op.read()
                Flg=0
            except:
                Flg-=1
        self.Referer=url
        return op
    def down(self,url,trytime=5):

        self.set_host(url)
        #获取网页并设置refer
        op=None
        Flg=trytime
        while Flg:
            try:
                op=self.Opener.open(url,timeout=120)
                #print op.info()
                Flg=0
            except:
                Flg-=1
        self.Referer=url
        return op


    def postdata(self,url,pdata):
        self.set_host(url)
        data = urllib.urlencode(pdata)
        op=self.Opener.open(url,data)
        self.Referer=url
        return op.read()

    def postfile(self,url,name,path,hader=[]):
       self.FileOpener = poster.streaminghttp.register_openers()
       self.FileOpener.add_handler(urllib2.HTTPCookieProcessor(self.Cookie))
       params = {name: open(path,"rb")}
       datagen, headers = poster.encode.multipart_encode(params)
       request = urllib2.Request(url, datagen, headers)
       for i in hader:
            request.add_header(i[0],i[1])


       result = urllib2.urlopen(request)
       return result.read()

    def postfileform(self,url,params,hader=[]):
       self.FileOpener = poster.streaminghttp.register_openers()
       self.FileOpener.add_handler(urllib2.HTTPCookieProcessor(self.Cookie))

       datagen, headers = poster.encode.multipart_encode(params)
       request = urllib2.Request(url, datagen, headers)
       for i in hader:
            request.add_header(i[0],i[1])
       result = urllib2.urlopen(request)
       return result.read()