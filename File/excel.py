#coding:utf-8
#author: beilianghsizi
#file: excel.py
#time: 2018/1/8 10:22
#desc: ""

import xlrd
data = xlrd.open_workbook('files/2018-01-05.xlsx')
table = data.sheets()[0]
nrows = table.nrows
for i in range(nrows):
    if i == 0:
        continue
    else:
        # print table.row_values(i)[:13]
        print i,"ip: %s   manufacturer: %s   sn: %s"%(table.row_values(i)[2],table.row_values(i)[3],table.row_values(i)[0])