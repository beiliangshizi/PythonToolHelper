#coding:utf-8
#author: beilianghsizi
#file: commands.py
#time: 2018/1/5 17:33
#desc: "commands对Python的os.popen()进行了封装，使用SHELL命令字符串作为其参数，返回命令的结果数据以及命令执行的状态；
# 该命令目前已经废弃，被subprocess所替代；"
# (status,result) = getstatusoutput(cmd_String)   如果执行成功则status等于为0


import commands
import pprint


def cmd_exe(cmd_String):
    print "will exe cmd,cmd:" + cmd_String
    return commands.getstatusoutput(cmd_String)


if __name__ == "__main__":
    pprint.pprint(cmd_exe("ls -la"))