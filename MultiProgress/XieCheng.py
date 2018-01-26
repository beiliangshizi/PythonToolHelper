#coding:utf-8
#author: beilianghsizi
#file: XieCheng.py
#time: 2018/1/10 14:03
#desc: ""

import time
import sys
# 生产者
def produce(l):
    i=0
    while 1:
        if i < 10:
            l.append(i)
            yield i
            i=i+1
            time.sleep(1)
        else:
            return
# 消费者
def consume(l):
    p = produce(l)
    while 1:
        try:
            p.next()
            while len(l) > 0:
                print l.pop()
        except StopIteration:
            sys.exit(0)
if __name__ == "__main__":
    l = []
    consume(l)