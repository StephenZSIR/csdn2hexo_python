#-*- coding: utf-8 -*-
from properties import Properties
from util import FileUtil
from paser import ArticlePaser
from bs4 import BeautifulSoup
class CorePaser:
	articlePaser = ArticlePaser.ArticlePaser()
	fileutil = FileUtil.FileUtil()

	def __init__(self):
		print("CorePaser初始化")
	# 解析博客的入口函数
	def paserCore(self):
		props = Properties.Properties()  # 读取文件
		recordCount = 1
		pageCount = 1
		uris = []

		# print("正在爬取第%d页"%(pageCount))
		print("正在爬取")
		try :
			url_way = int(props.get("url_way"))
			if url_way == 1:
				print("方式一:全量轮询模式")
				url_url_way_1 = props.get("url_way_1")
				count = 0
				while True:
					print("正在爬取第%d页" % (pageCount))
					sub_url = self.parseArticleURIs(url_url_way_1 + str(pageCount))
					uris.extend(sub_url)
					if count==0:
						count = len(sub_url)
					else:
						if count != len(sub_url):
							count = len(sub_url)
							print("第%d页共%d篇博客" % (pageCount, count))
							print("爬取结束，共爬取%d页%d条博客" % (pageCount, len(uris)))
							break
					pageCount = pageCount + 1
					print("第%d页共%d篇博客" % (pageCount,count))
			elif url_way == 2:
				print("方式二:专栏分类模式")
				print("正在爬取第%d页" % (pageCount))
				url_url_way_2 = props.get("url_way_2")
				uris = self.parseArticleURIsOfZhuanLan(url_url_way_2)
				print("第%d页共%d篇博客" % (pageCount, len(uris)))
				print("爬取结束，共爬取%d页%d条博客" % (pageCount, len(uris)))
			elif url_way == 3:
				print("方式三:单篇博客模式")
				print("正在爬取单篇博客")
				url_url_way_3 = props.get("url_way_3")
				uris.append(url_url_way_3)
				print("爬取结束，共爬取1篇博客")
			elif url_way == 4:
				print("方式四:单页博客模式")
				print("正在爬取第%d页" % (pageCount))
				url_url_way_4 = props.get("url_way_4")
				uris = self.parseArticleURIs(url_url_way_4)
				print("第%d页共%d篇博客" % (pageCount, len(uris)))
				print("爬取结束，共爬取%d页%d条博客" % (pageCount, len(uris)))
			else:
				return
			# 获得当前页所有文章的URI
			if (len(uris) == 0):
				return
			print("博客转换开始")
			for uri in uris:
				if (uri.count('http') <= 0):
					print("博客网址%s格式不正确"%(uri))
					continue
				# 核心
				article = self.articlePaser.paserArticle(uri)
				print("第%d篇  =>%s  %s"%(recordCount,article.getId(),article.getTitle()))
				# 核心
				self.fileutil.html2HexoMd(article)
				recordCount=recordCount+1
			print("博客转换完成")
		except Exception as e:
			print("解析博客失败")
			raise e

	def parseArticleURIs(self, url):
		ids = []
		text = self.articlePaser.GetCSDNArticle(url)
		soup = BeautifulSoup(text,'lxml')
		elements = soup.select(".article-item-box>h4>a")
		for element in elements:
			ids.append(element["href"])
		return ids

	def parseArticleURIsOfZhuanLan(self, url):
		ids = []
		text = self.articlePaser.GetCSDNArticle(url)
		soup = BeautifulSoup(text, 'lxml')
		elements = soup.select(".column_article_list>li>a")
		for element in elements:
			ids.append(element["href"])
		return ids







