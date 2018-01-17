#coding:utf-8
#author: beilianghsizi
#file: TinyPNG.py
#time: 2017/12/25 9:47
# #desc: "使用tinypng压缩png图片
# 每个key每月可压缩500张图片，key在 https://tinypng.com/developers 申请
# 先安装tinify和click
# pip3 install --upgrade tinify
# pip3 install click
# 在同目录下创建Config.py文件，在文件中写入key
# eg: pinypng_key = "xxxx"
# 默认配置 python3 tinypng.py
# 1.将需要压缩的图片放在uncompressed文件夹下
# 2.执行tinypng.py
# 3.压缩后的图片会在compressed文件夹下
# 处理单张图片 python3 tinypng.py -f 图片路径/xx.jpg
# 处理后文件名前添加_
# eg: python3 tinypng.py -f /Users/zhe/Pictures/a.png 生成_a.png
# 处理文件夹中的图片 python3 tinypng.py -d 文件夹路径
# 在文件夹下生成_tinypng文件夹放处理后的文件
# eg: python3 tinypng.py -d /Users/zhe/Pictures 在Pictures下生成_tinypng文件夹存放处理好的图片"

import os
import tinify
import click
import Config

tinify.key = Config.pinypng_key


# 判断是不是图片
def isPic(name):
    # 获取文件名和文件类型
    filename, filetype = os.path.splitext(name)
    if (filetype == ".png" or filetype == ".jpg" or filetype == ".jpeg"):
        return "true"
    else:
        print(name + "不是图片")


# 压缩图片
def compressed(inFile, outFile):
    source = tinify.from_file(inFile)
    source.to_file(outFile)


# 遍历文件夹，压缩图片
def walkFolder(inFolder, outFilder):
    for root, dirs, files in os.walk(inFolder):
        size = files.__len__()
        count = 1
        for name in files:
            if (not isPic(name)):
                size -= 1
                continue
            print("正在处理 %d/%d  %s " % (count, size, name))
            compressed(inFolder + "/" + name, outFilder + "/" + name)
            count += 1
        print("处理完成")
        break


# 没有任何参数，默认对预定文件夹操作
def default():
    sourceDir = "/Users/zhe/Documents/_tinypng_file/uncompressed"
    saveDir = "/Users/zhe/Documents/_tinypng_file/compressed"
    walkFolder(sourceDir, saveDir)


# 压缩单文件
def compressedFile(inFile):
    if (not os.path.isfile(inFile)):
        print("这不是文件")
        return
    # 文件路径
    dirname = os.path.dirname(inFile)
    # 文件名
    basename = os.path.basename(inFile)
    if (not isPic(basename)):
        return
    print("开始处理" + basename)
    compressed(inFile, dirname + "/_" + basename)
    print("处理完成")


# 压缩文件夹下所有文件
def compressedFolder(dir):
    if (not os.path.isdir(dir)):
        print("这不是文件夹")
        return
    saveDir = dir + "/_tinypng"
    if (not os.path.isdir(saveDir)):
        os.mkdir(saveDir)
    walkFolder(dir, saveDir)


@click.command()
@click.option("-f", "--file", default=None, help="处理单文件")
@click.option("-d", "--dir", default=None, help="处理文件夹里所有文件")
def run(file, dir):
    if (file is not None):
        compressedFile(file)
        pass
    elif (dir is not None):
        compressedFolder(dir)
        pass
    else:
        default()
        pass


# 程序入口
if __name__ == "__main__":
    run()