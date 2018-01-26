#coding:utf-8
#author: beilianghsizi
#file: command_timeout.py
#time: 2018/1/9 10:31
#desc: ""


import time
import subprocess
from threading import Timer

class TimeoutError(Exception):
    pass


def command(cmd, timeout=60):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    """
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            p.terminate()
            raise TimeoutError(cmd, timeout)
        time.sleep(0.1)
    return p.stdout.read()




def call(args, timeout):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    timer = Timer(timeout, lambda process: process.kill(), [p])

    try:
        timer.start()
        stdout, stderr = p.communicate()
        return_code = p.returncode
        return (stdout, stderr, return_code)
    finally:
        timer.cancel()

if __name__ == "__main__":
    # print command(cmd='ping www.baidu.com', timeout=10)
    print call(['hostname'], 2)
    print call(['ping', 'www.baidu.com'], 2)