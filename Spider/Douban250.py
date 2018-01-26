#coding:utf-8
#author: beilianghsizi
#file: Douban250.py
#time: 2017/12/25 9:55
#desc: ""

import time
import requests
from random import choice, uniform, randint
from pyquery import PyQuery as Pq
from functools import wraps
# from dialogue.dumblog import dlog

# logger = dlog(__file__, console='debug')


class Crawler(object):
    def __init__(self, url):
        user_agent = ['Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                      'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1;'
                      ' Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
                      'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
                      'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X)'
                      ' AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25']
        self.headers = {'User-Agent': choice(user_agent)}
        self.url = url
        self._page = None  # 任何单下划线(_)开头的名字应该总是被认为只属于内部实现

    @property
    def page(self):  # 方法变成属性调用
        if not self._page:
            r = requests.get(self.url, headers=self.headers)
            # logger.info(self.url)
            time.sleep(uniform(2, 4))
            r.encoding = 'utf-8'
            self._page = Pq(r.content).make_links_absolute(base_url=self.url)
        return self._page

    @page.setter
    def page(self, url):
        r = requests.get(url, headers=self.headers)
        # logger.info(url)
        time.sleep(uniform(2, 4))
        r.encoding = 'utf-8'
        self._page = Pq(r.content).make_links_absolute(base_url=url)

    def movie_urls(self):
        page_one_movie_urls = [{i('.info .title:eq(0)').text(): i('.pic a').attr('href')} for i in self.page('.grid_view .item').items()]
        rest_urls = [i.attr('href') for i in self.page('.paginator').remove('.next').find('a').items()]
        return page_one_movie_urls, rest_urls

    def movie_parser(self):
        sum_movie_urls = []  # 所有电影页的列表
        page_one_movie_urls, rest_urls = self.movie_urls()
        sum_movie_urls.extend(page_one_movie_urls)  # 将第一页的电影页加进去
        for rest_url in rest_urls:
            self.page = rest_url
            current_movie_urls = [{i('.info .title:eq(0)').text(): i('.pic a').attr('href')} for i in self.page('.grid_view .item').items()]
            sum_movie_urls.extend(current_movie_urls)
        return sum_movie_urls

    def detail_parser(self):
        res = []
        sum_movie_urls = self.movie_parser()
        for item in sum_movie_urls:
            self.page = item.values()[0]
            movie_brief = self.page('.all.hidden').text()
            item.setdefault('brief', movie_brief)
            res.append(item)
        return res



if __name__ == '__main__':
    # crawler = Crawler('https://movie.douban.com/top250')
    # res = crawler.movie_parser()
    # print res
    # print len(res)
    pass
