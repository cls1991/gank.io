# coding: utf8

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

import lib.crawler as cl


if __name__ == '__main__':
    # 测试用例
    s_url = "http://gank.io"
    file_name = "gank.txt"
    dlinks= cl.get_dlinks(s_url)
    cl.save_to_file(dlinks, file_name)


