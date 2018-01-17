#coding:utf-8
#author: beilianghsizi
#file: DecorateSummary.py
#time: 2017/12/25 9:54
#desc: ""
import time
import requests
from datetime import datetime
from random import randint, uniform
from functools import wraps


def log(func):
    def wrapper(*args, **kwargs):
        now_time = str(time.strftime('%Y-%m-%d %X', time.localtime()))
        print '------------------------------------------------'
        print '%s %s called' % (now_time, func.__name__)
        print 'Document:%s' % func.__doc__
        print '%s returns:' % func.__name__
        re = func(*args, **kwargs)
        print re
        return re
    return wrapper


def slumber(func):  # 无参装饰器
    @wraps(func)
    def wrapper(*args, **kwargs):
        wait = randint(2, 4)
        print '----Sleep%s----' % str(wait)
        print '%s called.' % func.__name__
        back = func(*args, **kwargs)
        print '%s end.' % func.__name__
        time.sleep(wait)
        # return back
    return wrapper


def slumber_params(start, end):
    def _outer(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            try:
                assert isinstance(start, int) and isinstance(end, int)
            except Exception as err:
                print 'start and end time require both int type!'
            if start <= end:
                print datetime.now()
                wait = randint(start, end)
                time.sleep(wait)
                print datetime.now()
                print '----random sleep from %s to %s'  % (start, end)
                return func(*args, **kwargs)
            else:
                print 'start time must less or equal to end time!'
        return _inner
    return _outer


def cache(func):
    saved = {}

    @wraps(func)
    def wrapper(url):
        if url in saved:
            return saved[url]
        else:
            page = func(url)
            saved[url] = page
            return page
    return wrapper


@cache
def web_lookup(url):
    """如果该url曾经被爬过就直接从缓存中获取，否则爬下来之后加入到缓存，防止后续重复爬取"""
    return requests.get(url).content


@slumber_params(2, 4)
def test():
    url = 'https://movie.douban.com/top250'
    r = requests.get(url)
    r.encoding = 'utf-8'


@slumber
def test():
    url = 'https://movie.douban.com/top250'
    r = requests.get(url)
    r.encoding = 'utf-8'


if __name__ == '__main__':
    test()