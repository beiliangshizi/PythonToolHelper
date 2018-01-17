#coding:utf-8
#author: beilianghsizi
#file: excel2csv.py
#time: 2017/12/25 9:52
#desc: ""

"""将excel文件转换成csv,再从csv中提取出urls，并最后保存成txt文件，方便爬虫去爬取"""
import os
import csv
import json
import subprocess


def convert_to_csv():
    for xlsxFilename in os.listdir('.'):
        if not xlsxFilename.endswith('.xlsx'):
            continue
        subprocess.call("python xlsx2csv.py %s %s.csv" % (xlsxFilename, xlsxFilename.split('.')[0]))


def extract_urls():
    for csvFilename in os.listdir('.'):
        if not csvFilename.endswith('.csv'):
            continue
        with open(csvFilename) as f:
            reader = csv.reader(f)
            result = []
            urls = []
            for row in reader:
                if reader.line_num == 1:  # 跳过csv第一行
                    continue
                result.append(row)
            for l in result:
                urls.append(l[-1])
        save_format = json.dumps(urls, sort_keys=True, indent=4).decode('unicode-escape').encode('utf8')
        with open('res/%s.txt' % csvFilename.split('.')[0], 'w') as f:
            f.write(save_format)


if __name__ == '__main__':
    convert_to_csv()
    extract_urls()