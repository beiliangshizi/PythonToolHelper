#coding:utf-8
#author: beilianghsizi
#file: TextCommon.py
#time: 2017/12/22 10:40
#desc: "处理各种文本相关的"

import re



class TextCommonHelper:
    def __init__(self,str):
        self.str = str
    def findallmatch(self,pattern):  #按照正则表达式来匹配文本中全部匹配字段
        pt = r"{}".format(pattern)
        matches = re.findall(pt,self.str)
        return matches
    def replaceallmatch(self,pattern,replacestr):  #将所有匹配字段替换为指定内容
        return re.sub(pattern,replacestr,self.str)

if __name__ == "__main__":
    tch = TextCommonHelper("adasa f sas")
    matches = tch.findallmatch("d(.*?)f")
    print tch.replaceallmatch("d(.*?)f","oo")

    # print tch.str.replace("a","12")
