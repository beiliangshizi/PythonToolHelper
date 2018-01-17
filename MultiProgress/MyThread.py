#coding:utf-8
#author: beilianghsizi
#file: MyThread.py
#time: 2018/1/10 13:37
#desc: ""

import threading
import time
import os

def booth(tid):
    global i
    global lock
    while True:
        lock.acquire()
        if i!=0:
            i=i-1
            print "window:",tid,",tickets left :",i
            time.sleep(1)
        else:
            print "Thread_id",tid,"No more tickets"
            os._exit(0)
        lock.release()
        time.sleep(1)

i = 100
lock=threading.Lock()

for k in range(10):
    new_thread = threading.Thread(target=booth,args=(k,))
    new_thread.start()