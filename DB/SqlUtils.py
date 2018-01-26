#coding:utf-8
#author: beilianghsizi
#file: SqlUtils.py
#time: 2017/12/25 9:42
#desc: "上传文件到七牛云存储，图片上传至imgs空间，文件上传至files空间
# 安装qiniu
# pip install qiniu
# 在同目录下创建Config.py文件，在文件中写入所需配置项
# qiniu_ak = "xxxx"
# qiniu_sk = "xxxx"
# qiniu_base_url_img = "xxxx"
# qiniu_base_url_file = "xxxx"
# qiniu_bucket_name_img = "imgs"
# qiniu_bucket_name_file = "files"
# 在七牛申请ak，sk
# 获取自己的外链前缀和空间名
# 默认配置 python3 qiniu_upload.py
# 1.把需要上传的图片放在up_file文件夹里
# 2.执行qiniu_update.py
# 上传单文件
# python3 qiniu_update.py -f /Users/zhe/Pictures/a.png
# 上传文件夹里所有文件
# python3 qiniu_update.py -d /Users/zhe/Pictures"

import MySQLdb
import sys
import tempfile
import urllib2
import urllib
import json
import threading
from datetime import datetime
from springpython.database.core import *
from springpython.database.factory import *
from springpython.database.transaction import *

global LOG


def initlog():
    import logging
    logger = logging.getLogger()
    hdlr = logging.StreamHandler()
    flr = logging.FileHandler("pylog")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    flr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.addHandler(flr)
    logger.setLevel(logging.NOTSET)
    return (logger, flr)


class ImproveMySQLConnectionFactory(MySQLConnectionFactory):
    def __init__(self, user=None, passwd=None, host=None, port=None, db=None, charset="utf8"):
        MySQLConnectionFactory.__init__(self, username=user, password=passwd, hostname=host, db=db)
        self.charset = charset
        self.port = port

    def connect(self):
        """The import statement is delayed so the library is loaded ONLY if this factory is really used."""
        import MySQLdb
        return MySQLdb.connect(host=self.hostname, port=self.port, user=self.username, passwd=self.password, db=self.db,
                               charset=self.charset)

    def in_transaction(self):
        return True

    def count_type(self):
        return types.LongType


class DistributedDbHandler:
    def __init__(self, user, passwd, db, charset):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.connectionFactory = {}
        self.dt = {}
        # self.conn = {}
        # self.cur = {}

    def __del__(self):
        # for cur in self.cur.values():
        #     cur.close()
        #
        # for conn in self.conn.values():
        #     conn.close()
        #
        # print "closed"
        pass

    # 获取分库的序号
    def getDistributedIndex(self, key):
        return 0

    # 有可能按host或者port分库，按情况来
    def getHostAndPort(self, index):
        pass

    def execute(self, func, key, *args):
        try:
            index = self.getDistributedIndex(key)
            if self.dt.get(index) is None:
                self.connect(index)
            (sql, resultType, rowMapper) = func(args)
            if types.ListType == resultType:
                return self.queryForList(sql=sql, index=index)
            elif types.NoneType == resultType:
                return self.query(sql=sql, index=index, rowMapper=rowMapper)
            else:
                return self.queryForObject(sql=sql, index=index, resultType=resultType)
        except Exception, e:
            LOG.error('Error %d: %s' % (e.args[0], e.args[1]))

    def connect(self, index):
        (host, port) = self.getHostAndPort(index)
        connFac = ImproveMySQLConnectionFactory(user=self.user, passwd=self.passwd, host=host, db=self.db, port=port)
        self.connectionFactory[index] = connFac
        self.dt[index] = DatabaseTemplate(connFac)

    def query(self, sql, index=0, rowMapper=None):
        try:
            return self.dt.get(index).query(sql, rowhandler=rowMapper)
        except Exception, e:
            LOG.error('Error %d with sql: %s' % (e.args[0], sql))
            if e.args[0] == 2006:
                try:
                    LOG.info("reconnecting...")
                    self.connect(index)
                    return self.dt.get(index).query(sql, rowhandler=rowMapper)
                except Exception, e:
                    LOG.error('Error %d with sql: %s' % (e.args[0], sql))

    def queryForObject(self, sql, index=0, resultType=types.ObjectType):
        try:
            return self.dt.get(index).query_for_object(sql, required_type=resultType)
        except Exception, e:
            LOG.error('Error %d with sql: %s' % (e.args[0], sql))
            if e.args[0] == 2006:
                try:
                    LOG.info("reconnecting...")
                    self.connect(index)
                    return self.dt.get(index).query_for_object(sql, required_type=resultType)
                except Exception, e:
                    LOG.error('Error %d with sql: %s' % (e.args[0], sql))

    def queryForList(self, sql, index=0):
        try:
            return self.dt.get(index).query_for_list(sql)
        except Exception, e:
            LOG.error('Error %d with sql: %s' % (e.args[0], sql))
            if e.args[0] == 2006:
                try:
                    LOG.info("reconnecting...")
                    self.connect(index)
                    return self.dt.get(index).query_for_list(sql)
                except Exception, e:
                    LOG.error('Error %d with sql: %s' % (e.args[0], sql))


class MyDBHandler(DistributedDbHandler):
    def __init__(self, user, passwd, db, charset):
        DistributedDbHandler.__init__(self, user, passwd, db, charset)

    # 获取分库的序号,key为ucid
    def getDistributedIndex(self, key):
        return (key / 256 * 8 + key % 6) % 16

    # 有可能按host或者port分库，按情况来
    def getHostAndPort(self, index):
        host = "192.168.0.6"
        port = 6300 + index
        return (host, port)

class AdMapper(RowMapper):
    """This will handle one row of database. It can be reused for many queries if they
       are returning the same columns."""

    def map_row(self, row, metadata=None):
        return Ad(id=row[0], name=row[1], aderId=row[2])


class Ad:
    def __init__(self, id, name, aderId):
        self.id = id
        self.name = name
        self.aderId = aderId

# 对象封装列表
def getAdAbstract(args):
    return "SELECT ad.id,ad.name,ad.ader_id from brand_start_ad ad where ad.id=%s" % (
    str(args[0])), types.NoneType, AdMapper()

# 字典的列表
def getAdAbstract1(args):
    return "SELECT ad.id,ad.name,ad.ader_id from brand_start_ad ad where ad.id=%s" % (
    str(args[0])), types.NoneType, DictionaryRowMapper()

# 返回一个row[]的列表
def getAdAbstract2(args):
    return "SELECT ad.id,ad.name,ad.ader_id from brand_start_ad ad where ad.id=%s" % (
    str(args[0])), types.ListType, None


def getAdAderId(args):
    return "SELECT ad.ader_id from brand_start_ad ad where ad.id=%s" % (str(args[0])), types.LongType, None


def generateInSql(len):
    return "(" + "%s," * (len - 1) + "%s)"


def main():
    dbhandler = MyDBHandler("name", "pass", "db", "utf8")

    # 返回一个字典的列表
    resultList = dbhandler.execute(getAdAbstract1, None, 571715)
    # 对象封装列表
    resultList = dbhandler.execute(getAdAbstract, None, 571715)
    # 返回一个row[]的列表
    resultList = dbhandler.execute(getAdAbstract2, None, 571715)
    # 返回一个结果
    result = dbhandler.execute(getAdAderId, None, 571715)


if __name__ == "__main__":
    (LOG, FLR) = initlog()
    main()
    FLR.flush()