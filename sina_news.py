#!/usr/bin/python3
#-*- coding:UTF-8 -*-


import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

#获取http://news.sina.com.cn/china下的新闻列表
def getNewsList(url):
    list = []
    res = requests.get(url) #requests.get抓取URL的Doc
    res.encoding='UTF-8' #设置编码
    soup = BeautifulSoup(res.text,'html.parser') 
    for news in soup.select('.news-item'):
        if len(news.select('h2'))>0:
            h2 = news.select('h2')[0].text
            time = news.select('.time')[0].text
            a = news.select('a')[0]['href']
            r = (time,h2,a)
            list.append(r)
    return list

#getNewsList('http://news.sina.com.cn/china/')

#根据内容页URL获取详细内容
def getNewsDetail(newsUrl):
    result={}
    res = requests.get(newsUrl)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text #标题
    result['newssource'] = soup.select('.time-source span a')[0].text #来源
    timesouce = soup.select('.time-source')[0].contents[0].strip() #时间
    dt = datetime.strptime(timesouce,'%Y年%m月%d日%H:%M')#字符串转时间格式
    result['dt'] = dt
    result['content'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]]) #文章内容
    result['editor'] = soup.select('.article-editor')[0].text.lstrip('责任编辑：').strip() #责任编辑
    result['comments_count'] = getCommentsCount(newsUrl)
    return result

#根据newsurl获取文章评论数
def getCommentsCount(newsUrl):
    m = re.search('doc-i(.+).shtml',newsUrl) #正则匹配url中的newsId
    newsId = m.group(1) #取到newsId
    commentsUrl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'
    url = commentsUrl.format(newsId)
    comments = requests.get(url)
    #print( url)
    jd = json.loads(comments.text.strip('var data='))
    return jd['result']['count']['total']


#count = getCommentsCount('http://news.sina.com.cn/c/nd/2017-03-06/doc-ifycaafm5323199.shtml');
#count


#c = getNewsDetail('http://news.sina.com.cn/c/nd/2017-03-06/doc-ifycaafm5323199.shtml')
#c