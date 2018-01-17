#coding:utf-8
#author: beilianghsizi
#file: FileCommon.py
#time: 2017/12/25 9:41
#desc: ""

import os


class File:
    # 文件工具类
    file_path_name = ""
    file_path = ""
    file_name = ""

    new_file = None

    def __init__(self, file_path_name):
        self.file_path_name = file_path_name
        last_separator_index = file_path_name.rfind("\\")
        if last_separator_index > 0:
            self.file_path = file_path_name[0:last_separator_index]
        else:
            self.file_path = ""
        self.file_name = file_path_name[file_path_name.rfind("\\")+1:len(file_path_name)]

    def create_if_not_exist(self):
        # 创建文件，如果文件已存在，则保留原文件，不再创建
        if self.file_path != "":
            if self.exists():
                pass
            else:
                os.makedirs(self.file_path)

        self.new_file = open(self.file_path_name, "a+")
        self.new_file.close()

    def open(self):
        # 打开文件
        self.new_file = open(self.file_path_name, "a+")

    def close(self):
        # 关闭文件
        self.new_file.close()

    def exists(self):
        # 检查文件是否存在（存在返回True）
        return os.path.exists(self.file_path)

    def clear_content(self):
        # 清空文件内容
        self.close()
        self.remove()
        self.create_if_not_exist()
        self.open()
        self.append("")

    def append(self, text):
        # 向文件末尾添加内容
        self.new_file.write(text)

    def append_line(self, text_line):
        # 向文件末尾添加一行内容
        self.new_file.write(text_line)
        self.new_file.write("\n")

    def read_all(self):
        # 读取文件的全部内容
        self.open()
        content = self.new_file.read()
        self.close()
        return content

    def replace_all(self, old_str, new_str):
        # 替换文件内容，类似字符串替换功能
        content = self.read_all()
        content = content.replace(old_str, new_str)
        self.remove()
        self.create_if_not_exist()
        self.open()
        self.append(content)
        self.close()

    def remove(self):
        # 删除文件
        self.close()
        os.remove(self.file_path_name)


if __name__ == "__main__":
    # 测试代码
    my_file = File("C:\\text\\text.txt")
    # 创建文件
    my_file.create_if_not_exist()
    my_file.open()
    my_file.clear_content()
    # 向文件中添加内容
    my_file.append("号 #{replace}")
    my_file.append_line("content #{replace}")
    # 获取文件内容
    file_content = my_file.read_all()
    # 创建新文件
    my_file_copy = File("C:\\text\\textNew.txt")
    my_file_copy.create_if_not_exist()
    my_file_copy.open()
    my_file_copy.clear_content()
    # 将文件内容写入新文件
    my_file_copy.append(file_content)
    # 替换文件内容的指定内容
    my_file_copy.replace_all("#{replace}", "QBF")
    my_file.close()
    my_file_copy.close()
    my_file.remove()
