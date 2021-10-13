from bs4 import BeautifulSoup
import requests
import urllib.request
import os
import time
import random


class PageInsect:
    url = ""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.jj20.com',
        'If-Modified-Since': 'Fri, 21 Dec 2018 03:58:29 GMT',
        'If-None-Match': '"cf51d66ee198d41:0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/68.0.3440.15 Safari/537.36',
    }
    UserAgent = 'Mozilla/5.0(windows NT 6.1; WOW64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 ' \
                'Safari/537.36 '

    def __init__(self, url):
        print("爬虫开始")
        self.url = url

    def insect(self):
        url = requests.get(self.url)
        html = url.text
        # 解析页面
        soup = BeautifulSoup(html, 'html.parser')
        # 查找该页面所有的img元素
        movie = soup.find_all('img')
        print(movie)
        for item in movie:
            imgSrc = item.get('src')
            print(imgSrc)
            # 图片是http开头的才下载
            if not imgSrc.startswith("http"):
                imgSrc = "http:" + imgSrc
            fileName = self.mkdirs("my_img_file", imgSrc)
            if not fileName:
                continue
            # 防止网站限制爬虫模拟头部
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', self.UserAgent),
                ('Referer', imgSrc)
            ]
            urllib.request.install_opener(opener)
            print(fileName)
            print(imgSrc)
            urllib.request.urlretrieve(imgSrc, fileName)
        print("图片下载完成")
        print("爬虫正在关闭")

    # 创建目录
    @staticmethod
    def mkdirs(dirName, imgSrc):
        # 当前目录
        cwd = os.getcwd()
        # 当前日期
        times = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 拼接目录
        dirs = cwd + "/" + dirName
        timeDir = dirs + "/" + times
        if os.path.exists(dirs):
            # 如果上级目录存在并且下级目录不存在创建下级目录
            if not os.path.exists(timeDir):
                os.mkdir(timeDir)
        else:
            # 如果上级目录没创建 则将他的下级目录也一起创建
            os.mkdir(dirs)
            os.mkdir(timeDir)
        if os.path.exists(timeDir):
            ran = random.randint(100, 999)
            ti = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            suffix = str(imgSrc).rsplit(".", 1)
            fileName = (str(str(ti) + str(ran))) + "." + suffix[1]
            urlFile = timeDir + "/" + fileName
        else:
            urlFile = ""

        # 单一出口原则
        return urlFile


# 路径需要加上http或者https
# page = PageInsect("https://wallhaven.cc/")
# page = PageInsect("http://www.netbian.com/")
# page = PageInsect("https://www.ivsky.com/")

urls = input("请输入携带http或者https的网址：")
if not urls:
    print("未输入地址")
else:
    page = PageInsect(urls)
    page.insect()
