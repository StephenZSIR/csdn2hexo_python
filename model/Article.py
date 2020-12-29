#-*- coding: utf-8 -*-
#文章类
class Article(object):
    def __init__(self, id, title, content, author, tags, catagory, date, url):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.tags = tags
        self.catagory = catagory
        self.date = date
        self.url = url
        print('Article实体化')
    def toList(self):
        list = []
        list.append(self.id)
        list.append(self.title)
        list.append(self.content)
        list.append(self.author)
        list.append(self.tags)
        list.append(self.catagory)
        list.append(self.date)
        list.append(self.url)
        return list
    def __init__(self):
        print('Article实体化')
    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def getAuthor(self):
        return self.author

    def setAuthor(self, author):
        self.author = author

    def getTags(self):
        return self.tags

    def setTags(self, tags):
        self.tags = tags

    def getCatagory(self):
        return self.catagory

    def setCatagory(self, catagory):
        self.catagory = catagory

    def getDate(self):
        return self.date

    def setDate(self, date):
        self.date = date

    def getUrl(self):
        return self.url

    def setUrl(self, url):
        self.url = url