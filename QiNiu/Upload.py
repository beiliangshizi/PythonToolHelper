#coding:utf-8
#author: beilianghsizi
#file: Upload.py
#time: 2017/12/25 9:47
#desc: ""

import os
import click
from qiniu import Auth, put_file, etag
import Config

# ak sk
access_key = Config.qiniu_ak
secret_key = Config.qiniu_sk

# 构建鉴权对象
q = Auth(access_key, secret_key)

# 外链前缀
base_url_img = Config.qiniu_base_url_img
base_url_file = Config.qiniu_base_url_file

# 要上传的空间名
bucket_name_img = Config.qiniu_bucket_name_img
bucket_name_file = Config.qiniu_bucket_name_file

# 上传
def upload(name, sourceFile):
    filename, filetype = os.path.splitext(name)
    if (filetype == ".png" or filetype == ".jpg" or filetype == ".jpeg"):
        bucket_name = bucket_name_img
        base_url = base_url_img
    else:
        bucket_name = bucket_name_file
        base_url = base_url_file
    token = q.upload_token(bucket_name, name, 3600)
    ret, info = put_file(token, name, sourceFile)
    if (info.status_code == 200):
        assert ret['key'] == name
        assert ret['hash'] == etag(sourceFile)
        print("上传完成，外链url为--  %s" % (base_url + name))
    else:
        print("上传失败")


# 遍历文件夹
def walkFolder(rootDir):
    for root, dirs, files in os.walk(rootDir):
        size = files.__len__()
        count = 1
        for name in files:
            if (name.startswith(".")):
                size -= 1
                continue
            sourceFile = rootDir + "/" + name
            print("正在上传%s  %d/%d" % (name, count, size))
            upload(name, sourceFile)


# 上传单文件
def uploadFile(file):
    if (not os.path.isfile(file)):
        print("这不是文件")
        return
    basename = os.path.basename(file)
    print("正在上传")
    upload(basename, file)


# 上传文件夹里所有文件
def uploadFolder(dir):
    if (not os.path.isdir(dir)):
        print("这不是文件夹")
        return
    walkFolder(dir)


# 没有任何参数，默认对预定文件夹操作
def default():
    rootDir = "/Users/zhe/Documents/_qiniu_upfile"
    walkFolder(rootDir)


@click.command()
@click.option("-f", "--file", default=None, help="上传单文件")
@click.option("-d", "--dir", default=None, help="上传文件夹里所有文件")
def run(file, dir):
    if (file is not None):
        uploadFile(file)
        pass
    elif (dir is not None):
        uploadFolder(dir)
        pass
    else:
        default()
        pass


# 程序入口
if (__name__ == "__main__"):
    run()