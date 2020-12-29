#-*- coding: utf-8 -*-
import platform

from properties import Properties
class HexoMdUtil:
    # 读取文件
    props = Properties.Properties()
    def __init__(self):
        print('HexoMdUtil初始化')
    # 适配hexo头部
    # ---
    # title: hexo deploy时重复输入用户名密码的问题
    # date: 2017-12-12 19:17:34
    # tags: hexo
    # ---
    def getHeader(self, article):
        separator = '\n'
        if platform.system()=='Windows':
            separator = '\r\n'

        article_title = article.getTitle()
        article_tags = article.getTags()
        hexo_tags = separator
        article_catagory = article.getCatagory()
        hexo_categories = separator
        for tag in article_tags:
            hexo_tags = hexo_tags+'- '+tag+separator
            
        for category in article_catagory:
            hexo_categories = hexo_categories+'- '+category+separator
        title = self.props.get("title")
        if (title !='' and not title):
            article_title = title
        sb=''
        sb = sb+"---\n"+("title: %s\n"%(article_title))+("author: %s\n"%(article.getAuthor()))+"tags: "+hexo_categories+"\n"+"category: "+hexo_tags+"\n"+("date: %s\n"%(article.getDate()))+"---\n"
        source_view_type = self.props.get("source_view")
        source_view = False
        if source_view_type == 'True':
            source_view = True
        if source_view:
            sb=sb+'本文转自['+article.getUrl()+']('+article.getUrl()+')\n'
        return sb

    def array2String(self, array):
        str=''
        for temp in array:
            str=str+temp
        return str

