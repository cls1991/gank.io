# coding: utf8

import os
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

    href = ""
    result = []
    counter = 1

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
        result.append(_img['src'])

        # 获取下载链接
        a_div = content.find('div', {'style': 'text-align:right', 'class': 'six columns'})
        _a = a_div.find('a')
        if not _a:
            print 'done'
            break

        else:
            href = _a['href']
        buffers.close()
        counter += 1

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
        base_dir = 'out/'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        file_object = open(base_dir + file_name, 'w')

        for item in d_links:
            file_object.write(item)
            file_object.write('\n')
        file_object.close()
    except IOError:
        print 'file not exist!'
        exit()


