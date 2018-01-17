#coding:utf-8
#author: beilianghsizi
#file: csv2mysql.py
#time: 2017/12/22 14:23
#desc: "从csv中读取数据写入到mysql数据库中"

import mysql.connector
import csv,time

variable = {
    'discuz_uid' : 20,
    'discuz_user' : 'bjxuekun',
    'fid' : 78,
    'typeid' : 0,
    'subject' :'直接发帖测试标题',
    'message' :'直接发帖测试内容-------------。[img]图片[/img]',
    'timestamp' : 'timestamp',
    'onlineip' : 'clientip',
    'ismobile' : 4
}
config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'',
    'port':3306 ,
    'database':'discuz',
    'charset':'utf8'
}
try:
    cnn=mysql.connector.connect(**config)
    if cnn:
        print '数据库连接成功!'
except mysql.connector.Error as e:
    print('数据库连接失败!{}'.format(e))
cursor=cnn.cursor()
read = csv.reader(open('items.csv'))
count = 0
datas = []
#根据当前时间生成时间戳
timeArray = time.strftime(time.ctime(),"%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeArray))



for useid,idtem,behavior,ugeohash,cate,time in read:
    sql_insert="insert into tian_yi_user(user_id,item_id,behavior_type,user_geohash,item_category,time) values (%(user_id)s,%(item_id)s,%(behavior_type)s,%(user_geohash)s,%(item_category)s,%(time)s)"
    sql_update = "UPDATE pre_forum_forum SET lastpost='{}', threads=threads+1, posts=posts+1, todayposts=todayposts+1 WHERE fid='$fid'", 'UNBUFFERED'
    data = {'user_id':useid,'item_id':idtem,'behavior_type':behavior,'user_geohash':ugeohash,'item_category':cate,'time':time}
    datas.append(data)
    count+=1
    if count/200000==1:
        cursor.executemany(sql_insert,datas)
        cnn.commit()
        count=0
        datas=[]
cursor.executemany(sql_insert,datas)
cnn.commit()
cursor.close()
cnn.close()

#读取商品csv的文件

read = csv.reader(open('tianchi_mobile_recommend_train_item.csv'))
for idtem,geohash,category in read:
    sql_insert="insert into tian_yi_item(item_id,item_geohash,item_category) values (%(item_id)s,%(item_geohash)s,%(item_category)s)"
    data = {'item_id':idtem,'item_geohash':geohash,'item_category':category}
    cursor.execute(sql_insert,data)
cnn.commit()
cursor.close()

cnn.close()