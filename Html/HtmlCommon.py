#coding:utf-8
#author: beilianghsizi
#file: HtmlCommon.py
#time: 2017/12/22 16:34
#desc: "将html中的指定字段替换为其他字段"

import HTMLParser
import re

if __name__ == '__main__':
    html = open("index.htm","rb")
    text = html.read()
    # output = re.sub(r'tppabs=\"[a-zA-z]+://[^\s]*\"',"",text)
    output = re.sub('�[^\s]+\?',"",text)
    # output = re.sub(r"慕轲","小毛球",text)
    html.close()
    html = open("index.htm","wb")
    html.write(output)
    html.close()

