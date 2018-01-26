#coding:utf-8
#author: beilianghsizi
#file: MyProcessWithPool.py
#time: 2018/1/10 16:31
#desc: ""在利用Python进行系统管理的时候，特别是同时操作多个文件目录，或者远程控制多台主机，并行操作可以节约大量的时间。
    # 当被操作对象数目不大时，可以直接利用multiprocessing中的Process动态成生多个进程，十几个还好，但如果是上百个，上千个目标，
    # 手动的去限制进程数量却又太过繁琐，此时可以发挥进程池的功效。
    # Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；
    # 但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来它。

#****************************************************************************************************************************
# 1.使用进程池（非阻塞）
# 2.使用进程池（阻塞）
# 3.使用进程池，并关注结果
# 4.使用多个进程池
#****************************************************************************************************************************

#1 *****************************************************************************************************************************
import multiprocessing
import time

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in xrange(4):
        msg = "hello %d" %(i)
        pool.apply_async(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print "Sub-process(es) done."

#     函数解释：
# apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞，apply(func[, args[, kwds]])是阻塞的（理解区别，看例1例2结果区别）
# close()    关闭pool，使其不在接受新的任务。
# terminate()    结束工作进程，不在处理未完成的任务。
# join()    主进程阻塞，等待子进程的退出， join方法要在close或terminate之后使用。
# 执行说明：创建一个进程池pool，并设定进程的数量为3，xrange(4)会相继产生四个对象[0, 1, 2, 4]，四个对象被提交到pool中，
#       因pool指定进程数为3，所以0、1、2会直接送到进程中执行，当其中一个执行完事后才空出一个进程处理对象3，
#       所以会出现输出“msg: hello 3”出现在"end"后。因为为非阻塞，主函数会自己执行自个的，不搭理进程的执行，
#       所以运行完for循环后直接输出“mMsg: hark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~”，主程序在pool.join（）处等待各个进程的结束。

# 2 *****************************************************************************************************************************
#coding: utf-8
import multiprocessing
import time

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in xrange(4):
        msg = "hello %d" %(i)
        pool.apply(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print "Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~"
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print "Sub-process(es) done."
# 3 *****************************************************************************************************************************

import multiprocessing
import time

def func(msg):
    print "msg:", msg
    time.sleep(3)
    print "end"
    return "done" + msg

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in xrange(3):
        msg = "hello %d" %(i)
        result.append(pool.apply_async(func, (msg, )))
    pool.close()
    pool.join()
    for res in result:
        print ":::", res.get()
    print "Sub-process(es) done."

# 4 *****************************************************************************************************************************
import multiprocessing
import os, time, random


def Lee():
    print "\nRun task Lee-%s" % (os.getpid())  # os.getpid()获取当前的进程的ID
    start = time.time()
    time.sleep(random.random() * 10)  # random.random()随机生成0-1之间的小数
    end = time.time()
    print 'Task Lee, runs %0.2f seconds.' % (end - start)


def Marlon():
    print "\nRun task Marlon-%s" % (os.getpid())
    start = time.time()
    time.sleep(random.random() * 40)
    end = time.time()
    print 'Task Marlon runs %0.2f seconds.' % (end - start)


def Allen():
    print "\nRun task Allen-%s" % (os.getpid())
    start = time.time()
    time.sleep(random.random() * 30)
    end = time.time()
    print 'Task Allen runs %0.2f seconds.' % (end - start)


def Frank():
    print "\nRun task Frank-%s" % (os.getpid())
    start = time.time()
    time.sleep(random.random() * 20)
    end = time.time()
    print 'Task Frank runs %0.2f seconds.' % (end - start)


if __name__ == '__main__':
    function_list = [Lee, Marlon, Allen, Frank]
    print "parent process %s" % (os.getpid())

    pool = multiprocessing.Pool(4)
    for func in function_list:
        pool.apply_async(func)  # Pool执行函数，apply执行函数,当有一个进程执行完毕后，会添加一个新的进程到pool中

    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()  # 调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print 'All subprocesses done.'

