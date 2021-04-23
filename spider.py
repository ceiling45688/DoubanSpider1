#-*- coding = utf-8 -*- 
#@TIme: 2021/4/20 17:16
#@Author: Celine
#@File: spider.py
#@Software: PyCharm
#intro：第一次爬虫练习项目

import re
from bs4 import BeautifulSoup #网页解析，获取数据
import urllib.request, urllib.error #定制url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行sqlite数据库操作

findlink = re.compile(r'<a href="(.*?)">') # 全局变量，创建正则表达式对象 (.*?)表示任意多字符的非贪婪模式匹配,链接都放在一组()
findImgSrc = re.compile(r'<img.*src="(.*?)".*>', re.S) # .S匹配包括换行符
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findQuote = re.compile(r'<span class="inq">(.*)</span>', re.S)
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


#爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i*25) # 网页地址递增，str()字符串转换后才能拼接
        html = askURL(url)

        #每次获取到网页信息后需逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"): #查找属性class=item的div, 返回列表
            # print(item) #测试：查看电影item全部信息
            data = []
            item = str(item)
            #正则表达式返回匹配的链接（列表形式）,[0]返回第一个文本内容
            link = re.findall(findlink, item)[0] #影片详情链接
            # print(link) #测试
            data.append(link)

            imgSrc = re.findall(findImgSrc, item)[0] # 图片
            data.append(imgSrc)

            titles = re.findall(findTitle, item) # 标题， 注意title可能有多个名字
            if len(titles) == 2:
                ctitle = titles[0] #添加中文名
                data.append(ctitle)
                otitle = titles[1].replace('/','') #添加外文名
                data.append(otitle)
            else: #只有一个title
                data.append(titles[0])
                data.append(' ') # 注意：第二个外文名即使没有也需要留空！

            rating = re.findall(findRating, item)[0] # 评分
            data.append(rating)

            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            quote = re.findall(findQuote, item)
            if len(quote) != 0:
                quote = quote[0].replace('。', '')
                data.append(quote)
            else:
                data.append(' ')

            bd = re.findall(findBd, item)[0] # 人员
            bd = re.sub('<br(\s+)?/>(\s+)?', '', str(bd))#替换正则中的换行， \s匹配空白和tab
            data.append(bd.strip()) #去掉前后空格

            datalist.append(data) #处理好的一部电影信息放入datalist
    print(datalist) #测试
    return datalist

#得到制定一个url网页内容
def askURL(url):
    #headers伪装成浏览器访问豆瓣服务器， 用户代理：本质是告诉浏览器我们可以接受什么水平的文件内容
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77"}
    req = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(req) #返回的response对象包含整个网页信息
        html = response.read().decode("utf-8") #读取信息
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"): #获取错误原因
            print(e.reason)
    return html


#保存数据
def saveDate(savePath):
    pass

if __name__ == '__main__':
    #1.爬取网页
    #2.逐一解析数据
    #3.保存数据

    getData("https://movie.douban.com/top250?start=")
