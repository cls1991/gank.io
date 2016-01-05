# coding: utf8

import os
import datetime
import pycurl
from StringIO import StringIO
from bs4 import BeautifulSoup

# 伪装成iPad客户端
user_agent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10' \
             ' (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# 伪造来源地址
refer_path = "http://gank.io"


def get_dlinks(source_url):
    """
    根据网页url图片的下载链接
    :param source_url: 原地址
    :return 返回图片的真实下载链接
    """
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_path)

    result = []
    counter = 1
    latest_timer = get_record_timer()
    # 是否是最新记录
    dt = datetime.datetime.now().strftime("/%Y/%m/%d")
    if latest_timer and cmp(latest_timer, dt) == 0:
        return result

    href = ""
    ll = ""
    print 'start'
    # 使用探测法拿到所有的图片资源
    while 1:
        print 'crawler the %d picture' % counter
        # 获取str类型的数据
        buffers = StringIO()
        target_url = source_url + href
        curl.setopt(pycurl.URL, target_url)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()

        body = buffers.getvalue()
        soup = BeautifulSoup(body)

        # 拿到目标div
        content = soup.find('div', {'class': 'container content'})
        soup.decompose()

        # 拿到图片链接
        img_div = content.find('div', {'class': 'outlink'})
        _img = img_div.find('img')
        if _img['src'].endswith('.jpg') or _img['src'].endswith('.png'):
            result.append(_img['src'])

        # 获取下一页地址
        a_div = content.find('div', {'style': 'text-align:right', 'class': 'six columns'})
        _a = a_div.find('a')
        buffers.close()
        if not _a:
            print 'done'
            break

        href = _a['href']
        if counter == 1:
            ll = href
        if latest_timer and cmp(href, latest_timer) <= 0:
            break

        counter += 1

    # 记录最新时间点
    buffers = StringIO()
    target_url = source_url + ll
    curl.setopt(pycurl.URL, target_url)
    curl.setopt(pycurl.WRITEDATA, buffers)
    curl.perform()

    body = buffers.getvalue()
    soup = BeautifulSoup(body)

    # 拿到目标div
    content = soup.find('div', {'class': 'container content'})
    soup.decompose()

    # 获取前向地址
    pre_div = content.find('div', {'class': 'six columns'})
    pre_href = pre_div.find('a')['href']
    # 更新时间点
    set_record_timer(pre_href)
    buffers.close()
    curl.close()

    return result


def save_to_file(d_links, file_name):
    """
    将图片链接存入文件
    :param d_links: 图片真实下载链接
    :param :file_name: 文件名
    :return
    """
    try:
        if not d_links:
            return
        base_dir = 'out/'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        file_object = open(base_dir + file_name, 'a')

        for item in d_links:
            file_object.write(item)
            file_object.write('\n')
        file_object.close()
    except IOError:
        print 'file not exist!'
        exit()


def get_record_timer():
    """
    从本地文件拿到最近一次的记录时间点
    :return
    """
    try:
        record_file = "timer.txt"
        if not os.path.exists(record_file):
            return None
        file_object = open(record_file, "r")
        line = file_object.readline()
        file_object.close()
        if not line:
            return None

        return line
    except IOError:
        print 'file io error!'
        exit()


def set_record_timer(record_timer):
    """
    记录最近一次记录时间点
    :param record_timer: 记录时间点
    :return
    """
    try:
        record_file = "timer.txt"
        file_object = open(record_file, "w")
        file_object.write(record_timer)
        file_object.close()
    except IOError:
        print 'file io error!'
        exit()
