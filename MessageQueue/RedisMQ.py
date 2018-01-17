#coding:utf-8
#author: beilianghsizi
#file: RedisMQ.py
#time: 2018/1/11 10:20
#desc: "使用redis实现消息队列"
    # Python内置了一个好用的队列结构。我们也可以是用redis实现类似的操作。并做一个简单的异步任务。
    # Redis提供了两种方式来作消息队列。一个是使用生产者消费模式模式，另外一个方法就是发布订阅者模式。
    # 前者会让一个或者多个客户端监听消息队列，一旦消息到达，消费者马上消费，谁先抢到算谁的，如果队列里没有消息，则消费者继续监听。
    # 后者也是一个或多个客户端订阅消息频道，只要发布者发布消息，所有订阅者都能收到消息，订阅者都是ping的。



import redis


class Task(object):
    def __init__(self):
        self.rcon = redis.StrictRedis(host='localhost', db=5)
        self.queue = 'task:prodcons:queue'

    def listen_task(self):
        while True:
            test = self.rcon.blpop(self.queue, 1)
            task = test[1]
            print "Task get", task


if __name__ == '__main__':
    print 'listen task queue'
    Task().listen_task()