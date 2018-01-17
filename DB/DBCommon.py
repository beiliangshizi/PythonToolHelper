#coding:utf-8
#author: beilianghsizi
#file: DBCommon.py
#time: 2017/12/25 9:37
#desc: "数据库通用工具类"

import MySQLdb

class Column:
    # 数据库表的字段对应类
    name = ""    # 字段名称
    name_first_char_up = "" # 字段名称（首字符大写）
    type = ""   # 字段类型
    key = ""     # 键情况（'PRI':主键）
    annotation = ""   # 字段注释

    def __init__(self):
        pass

    def set_name(self, name):
        self.name = name
        if self.name != "":
            first_char = self.name[0: 1]
            first_char = first_char.upper()
            self.name_first_char_up = first_char+self.name[1: len(self.name)]

class MySqlTool:
    # MySQL工具类
    # 查询表结构的sql语句
    query_table_structure_sql = '''
    select
        t.COLUMN_NAME,
        t.DATA_TYPE,
        t.COLUMN_KEY,
        t.COLUMN_COMMENT
    from information_schema.columns t
        where t.table_name='%s'
    '''

    host = ""   # 数据库主机地址
    port = ""   # 接口号
    user_name = ""  # 登录名称
    password = ""   # 登录密码
    data_base_name = "" # 数据库名
    charset = ""    # 数据库编码
    db_connect = ""

    def __init__(self, host, port, user_name, password, data_base_name, charset):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.data_base_name = data_base_name
        self.charset = charset
        self.db_connect = MySQLdb.connect(host, user_name, password, data_base_name, charset=charset)

    def select_one(self, query_sql):
        # 单条数据查询（返回符合条件的第一条数据）
        cursor = self.db_connect.cursor()
        cursor.execute(query_sql)
        results = cursor.fetchone()
        return results

    def select_list(self, query_sql):
        # 列表查询
        cursor = self.db_connect.cursor()
        cursor.execute(query_sql)
        results = cursor.fetchall()
        return results

    def insert(self, insert_sql):
        # 插入操作
        cursor = self.db_connect.cursor()
        cursor.execute(insert_sql)
        self.db_connect.commit()

    def query_table_structure(self, table_name):
        # 查询数据表结构（返回column对象列表）
        cursor = self.db_connect.cursor()
        cursor.execute(self.query_table_structure_sql % table_name)
        results = cursor.fetchall()
        column_list = []
        for result in results:
            column = Column()
            column.set_name(result[0])
            column.type = result[1]
            column.key = result[2]
            column.annotation = result[3]
            column_list.append(column)
        return column_list


if __name__ == "__main__":
    mysql_tool = MySqlTool("127.0.0.1", "3306", "toyflivver", "toyflivver", "myfirst", "utf8")

    # 查询单个数据
    # print mysql_tool.select_one("select * from t_user t where t.id = 6")

    # 查询数据列表
    # results = mysql_tool.select_list("select * from t_user t")
    # for result in results:
    #     print result

    # 插入数据
    # mysql_tool.insert("insert into t_user values(null, 'd', 'd', '155')");

    # 查询表结构
    # column_list = mysql_tool.query_table_structure("t_user")
    # for column in column_list:
    #     print "%s, %s, %s, %s " % (column.name, column.type, column.key, column.annotation)