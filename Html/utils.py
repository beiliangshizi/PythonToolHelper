#coding:utf-8
#author: beilianghsizi
#file: utils.py
#time: 2017/12/25 9:22
#desc: ""

import re
from urllib.parse import parse_qs, urlparse
from selenium import webdriver

def get_url_query_dict(url):
    return parse_qs(urlparse(url).query)


def match_one(src, regex):
    if not regex:
        return src
    match = re.compile(regex).search(src)
    return match.group(min(1, len(match.groups()))) if match else ''


def match_all(src, regex):
    if not regex:
        return [src]
    matches = re.compile(regex).findall(src)
    return matches

def get_driver(driver_name, driver_path, log_path='debug.log'):
    # 动态导入相应的包
    __import__('selenium.webdriver.%s.webdriver' % driver_name.lower())
    os.environ['webdriver.%s.driver' % driver_name] = driver_path
    driver = getattr(webdriver, driver_name)(driver_path, service_log_path=log_path)
    return driver

def strip_control_characters(s):
    """去除控制字符"""
    return ''.join(i for i in s if 31 < ord(i) < 127)