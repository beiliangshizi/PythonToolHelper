#coding:utf-8
#author: beilianghsizi
#file: subprocess.py
#time: 2018/1/5 17:37
#desc: ""Python目前已经废弃了os.system，os.spawn*，os.popen*，popen2.*，commands.*来执行其他语言的命令，subprocesss是被推荐的方法；
# subprocess允许你能创建很多子进程，创建的时候能指定子进程和子进程的输入、输出、错误输出管道，执行后能获取输出结果和执行状态。
# 在python中执行SHELL有时候也是很必须的，比如使用Python的线程机制启动不同的shell进程，目前subprocess是Python官方推荐的方法，
# 其支持的功能也是最多的，推荐大家使用。

import shlex
import datetime
import subprocess
import time


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # 没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)

    # subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)

    return str(sub.returncode)


if __name__ == "__main__":
    print execute_command("ls")