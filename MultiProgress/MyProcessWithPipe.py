#coding:utf-8
#author: beilianghsizi
#file: MyProcessWithPipe.py
#time: 2018/1/10 16:30
#desc: "Pipe方法返回(conn1, conn2)代表一个管道的两个端。Pipe方法有duplex参数，如果duplex参数为True(默认值)，
    # 那么这个管道是全双工模式，也就是说conn1和conn2均可收发。duplex为False，conn1只负责接受消息，conn2只负责发送消息。
    # send和recv方法分别是发送和接受消息的方法。例如，在全双工模式下，可以调用conn1.send发送消息，conn1.recv接收消息。
    # 如果没有消息可接收，recv方法会一直阻塞。如果管道已经被关闭，那么recv方法会抛出EOFError。"

import multiprocessing
import time

def proc1(pipe):
    while True:
        for i in xrange(10000):
            print "send: %s" %(i)
            pipe.send(i)
            time.sleep(1)

def proc2(pipe):
    while True:
        print "proc2 rev:", pipe.recv()
        time.sleep(1)

def proc3(pipe):
    while True:
        print "PROC3 rev:", pipe.recv()
        time.sleep(1)

if __name__ == "__main__":
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
    p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
    #p3 = multiprocessing.Process(target=proc3, args=(pipe[1],))

    p1.start()
    p2.start()
    #p3.start()

    p1.join()
    p2.join()
    #p3.join()