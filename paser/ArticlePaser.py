#-*- coding: utf-8 -*-
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from model import Article
from properties import Properties


class ArticlePaser:
    article = Article.Article()
    props = Properties.Properties()  # 读取文件
    def __init__(self):
        print('ArticlePaser初始化')

    def paserArticle(self,url):
        self.props = Properties.Properties()  # 读取文件
        text = self.GetCSDNArticle(url)
        soup = BeautifulSoup(text,'lxml')
        url_arr = url.split('/')
        articleId = url_arr[len(url_arr)-1]
        articleTitle = soup.select(".article-title-box>h1")[0].string.strip()
        articleContent = soup.select("#article_content")[0]
        set_head = False
        set_head_view = self.props.get('set_head')
        if set_head_view =='True':
            set_head=True


        self.article.setId(int(articleId))
        self.article.setTitle(articleTitle)
        self.article.setContent(articleContent)

        self.article.setUrl(url)
        try:
            element = soup.select(".bar-content>.time")[0].string;
            self.article.setDate(element)
        except:
            print("应该是被反爬虫了,换个wifi或者网络试试~~~~~~~~~~~~~~~~~~~~~~~")
        if set_head:
            while True:
                message = '''
                ======================================================
                您已开启自定义header配置，需要进行以下操作:
                    1 输入author
                    2 输入tags
                    3 输入categories
                ======================================================
                '''
                print(message)
                print('1 输入author')
                author = self.setting_property('author','author名称','String','String')
                print('2 输入tags')
                tags = self.setting_property('tags','tags名称(多个用,隔开)','String','spilt').split(',')
                print('3 输入categories')
                categories = self.setting_property('categories','categories名称(多个用,隔开)','String','spilt').split(',')
                self.article.setAuthor(author)
                self.article.setCatagory(categories)
                self.article.setTags(tags)
                break
        else:
            tags = self.props.get('tags').split(',')
            categories = self.props.get('categories').split(',')
            author = self.props.get('author')
            self.article.setAuthor(author)
            self.article.setCatagory(categories)
            self.article.setTags(tags)
        return self.article
    def setting_property(self,field,descrip,value,type):
        value_now = self.props.get(field)
        str = ''
        while True:
            message = '''
            ======================================================
            配置项%s
                名称: %s
                说明: %s
                取值: %s
                现值: %s
            说明:输入为空回车将保持现值不变
            ======================================================
            '''%(field,field,descrip,value,value_now)
            print(message)
            str = input('请输入%s的值>>'%(field))
            if str=='':
                print('%s的配置将保持为现值%s' % (field, value_now))
                break
            if type=='spilt':
                if str != '':
                    self.props.put(field, str)
                    self.props = Properties.Properties()
                    print('%s的配置已修改为%s' % (field, str))
                    break
            elif type=='String':
                if str !='':
                    self.props.put(field, str)
                    self.props = Properties.Properties()
                    print('%s的配置已修改为%s' % (field, str))
                    break
        return str
    def GetHeaders(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'referer': url,
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        return headers

    def GetCSDNArticle(self, url):
        session = requests.Session()
        rst = session.get(url, headers=self.GetHeaders(url))
        rst = rst.text
        return rst

    def parseCata(self,page):
        elements = page.xpath(".tags-box>a")
        for element in elements:
            url=element.attr("href")
            if not url and len(url) != 0:
                if url.lastIndexOf("category") != -1:
                    return element.select(".tag-link").text().trim()
        return ''

    def parseArticleId(self,url):
        return re.match(r'.*/(\\d*)', url).group()

    def parseTags(self,page):
        list = [];
        elements = page.xpath(".artic-tag-box>a")
        for element in elements:
            text=element.xpath(".tag-link").text().trim()
            list.append(text)
        return list
