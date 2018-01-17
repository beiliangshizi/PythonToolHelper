#coding:utf-8
#author: beilianghsizi
#file: Schedule.py
#time: 2017/12/25 9:59
#desc: ""

import os
from glob import glob
import subprocess


def traverse_and_run():
    for path in glob('exp/*/'):
        for file_name in os.listdir(path):
            if file_name.endswith('.py'):
                p = subprocess.Popen(['python', file_name], cwd='%s' % path)
                p.wait()


if __name__ == '__main__':
    traverse_and_run()