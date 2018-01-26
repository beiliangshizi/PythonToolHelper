#coding:utf-8
#author: beilianghsizi
#file: ThreadsPool.py
#time: 2018/1/17 18:36
#desc: ""

import threading
import time
import contextlib
from Queue import Queue

workerStop = object()


class ThreadPool(object):
    workerCount = 0  # 当前没有关闭的线程数

    def __init__(self, max):
        self.queue = Queue(0)
        self.max = max  # 线程池最大线程数
        self.working = []  # 正在'工作'的线程
        self.waiters = []  # 正在'等待'的线程

    def callInTread(self, func, *args, **kwargs):
        self.callInThreadWithCallback(None, func, *args, **kwargs)

    def callInThreadWithCallback(self, onResult, func, *args, **kwargs):
        o = (func, args, kwargs, onResult)
        self.queue.put(o)

    def start(self):
        # '尽最大努力'创建线程去执行任务
        while self.workerCount < min(self.max, self.queue.qsize()):
            self.startWorker()

    def startWorker(self):
        self.workerCount += 1
        t = threading.Thread(target=self._worker)
        t.start()

    def _worker(self):
        '''最关键的函数'''
        o = self.queue.get()

        # 存在任务
        while o is not workerStop:
            thread = threading.currentThread()

            with self._workerState(self.working, thread):
                func, args, kwargs, onResult = o
                func(*args)  # 真正去执行函数

            with self._workerState(self.waiters, thread):
                o = self.queue.get()

    @contextlib.contextmanager
    def _workerState(self, threadList, thread):
        '''关键点之二:存放工作线程和等待线程'''
        threadList.append(thread)
        try:
            yield
        except Exception as e:
            raise
        else:
            threadList.remove(thread)

    def stop(self):
        '''关闭线程'''
        while self.workerCount:
            self.queue.put(workerStop)
            self.workerCount -= 1


def show(i):
    print i
    time.sleep(5)


pool = ThreadPool(5)
for i in xrange(50):
    pool.callInTread(show, i)  # 创建50个任务,存放到队列中

pool.start()  # 开启
pool.stop()  # 关闭