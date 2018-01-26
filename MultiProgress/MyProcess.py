#coding:utf-8
#author: beilianghsizi
#file: MyProcess.py
#time: 2018/1/10 16:03
#desc: ""

import multiprocessing
import time

class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        n = 5
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1

if __name__ == '__main__':
    p = ClockProcess(1)
    # p.daemon = True  #将子进程设置为守护进程，则主进程结束，子进程随着被停止；
    p.start()

    print p.name,p.pid
    print multiprocessing.cpu_count()