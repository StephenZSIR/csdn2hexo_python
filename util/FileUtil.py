#-*- coding: utf-8 -*-
import datetime
import os
import platform
import re
import time
import uuid
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import html2text as ht
from properties import Properties
from util import HexoMdUtil
class FileUtil:
    props = Properties.Properties()  # 读取文件
    hexomUtil = HexoMdUtil.HexoMdUtil()
    dir = ''
    htmlDir = ''
    mdDir = ''
    imgDir = ''
    imgflag = False
    def __init__(self):
        print('FileUtil初始化')
        self.dir = self.props.get("file_Path")
        if self.dir == '':
            print('根目录不能为空')
            return
        imgSwitch = self.props.get("img_flag")
        html_path = self.props.get("html_path")
        image_path = self.props.get("image_path")
        md_path = self.props.get("md_path")
        sys_name = platform.system()
        if sys_name == 'Windows':
            self.htmlDir = self.dir + "\\" + html_path + "\\"
            self.mdDir = self.dir + "\\" + md_path + "\\"
            self.imgDir = self.dir + "\\" + image_path + "\\"
        else:
            self.htmlDir = self.dir + "/" + html_path + "/"
            self.mdDir = self.dir + "/" + md_path + "/"
            self.imgDir = self.dir + "/" + image_path + "/"
        if imgSwitch=='True':
            self.imgflag = True
        else:
            self.imgflag = False
        self.judeDirExists(self.dir, self.htmlDir, self.mdDir, self.imgDir)


    def save(self,content, filePath):
        try:
            with open(filePath, 'wb') as f:
                f.write(content.encode())
        except Exception as e:
            print('文件%s写入失败'%(filePath))
            raise e


    def saveHtml(self,article):
        fileName = article.getTitle()
        if fileName == '':
            fileName = article.getDate().replace(' ','').replace('-','').replace(':','')+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        else:
            fileName = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",fileName.strip())
        filePath = self.htmlDir + fileName + '.html'
        self.save(article.getContent(), filePath)


    def saveHexomd(self, article):
        mdhead = ''
        filePath = ''
        head = self.props.get('head')
        if (head=='True'):
            mdhead = self.hexomUtil.getHeader(article)
        try :
            fileName = article.getTitle()
            if fileName == '':
                fileName = article.getDate().replace(' ','').replace('-','').replace(':','')+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            else:
                fileName = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",fileName.strip())
            text_maker = ht.HTML2Text()
            # 读取html格式文件
            with open(self.htmlDir + fileName+ '.html', 'r', encoding='UTF-8') as f:
                htmlpage = f.read()
            # 处理html格式文件中的内容
            # 图片转储处理
            if self.imgflag:
                web_image_path = self.props.get('web_image_path')
                soup = BeautifulSoup(htmlpage, 'lxml')
                imgs_list = soup.select('img')
                for img_model in imgs_list:
                    old_url = img_model['src']
                    fix = self.getPicture(old_url)
                    if fix!='':
                        new_url = web_image_path+self.getPicture(old_url)
                        img_model['src'] = new_url

            mdContent = text_maker.handle(str(soup))

            realContent = mdhead + mdContent

            title_type = self.props.get("title_type")
            if (title_type=='date') :
                MdFileName = article.getDate().replace(' ','').replace('-','').replace(':','')+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            else:
                MdFileName = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",article.getTitle().strip())
            filePath = self.mdDir + MdFileName + ".md"
            self.save(realContent, filePath)
        except Exception as e:
            print('文件%s写入失败'%(filePath))
            raise e


    def html2HexoMd(self,article):
        self.saveHtml(article)
        self.saveHexomd(article)
    def getPicture(self,url) :
        fix = ''
        if (self.imgflag and url and url!=''):
            try:
                fix = str(uuid.uuid3(uuid.NAMESPACE_DNS,url))
                response = requests.get(url, headers=self.GetHeaders(url))
                image = Image.open(BytesIO(response.content))
                fix = fix + '.' +image.format
                image.save(self.imgDir+fix.replace(' ','').replace('-',''))
            except:
                print('下载图片%s失败'%(url))
                return ''
        return fix.replace(' ','').replace('-','')

    def GetHeaders(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'referer': url,
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        return headers

    #判断文件夹是否存在
    def judeDirExists(self,dirRoot, htmlDirPath, mdDirPath, imgDirPath):
        try:
            sys_name = platform.system()
            if sys_name == 'Windows':
                dir_arr = dirRoot.split('\\')
                baseUrl = ''
                for dir in dir_arr:
                    if dir.count(':') > 0:
                        baseUrl=dir
                    if dir.count(':')<=0 and dir != '':
                        baseUrl = baseUrl+'\\'+dir
                        if(os.path.isdir(baseUrl)):
                            print("根目录%s已存在！"%(baseUrl))
                        else:
                            os.mkdir(baseUrl)
                            print("根目录%s已创建！"%(baseUrl))
            else:
                dir_arr = dirRoot.split('/')
                baseUrl = ''
                for dir in dir_arr:
                    if dir != '':
                        baseUrl = baseUrl + '/' + dir
                        if (os.path.isdir(baseUrl)):
                            print("根目录%s已存在！" % (baseUrl))
                        else:
                            os.mkdir(baseUrl)
                            print("根目录%s已创建！" % (baseUrl))

            if (os.path.isdir(htmlDirPath)):
                print("原网页保存目录%s已存在！"%(htmlDirPath))
            else:
                os.mkdir(htmlDirPath)
                print("原网页保存目录%s已创建！" % (htmlDirPath))
            if (os.path.isdir(mdDirPath)):
                print("转换后md文件保存目录%s已存在！" % (mdDirPath))
            else:
                os.mkdir(mdDirPath)
                print("转换后md文件保存目录%s已创建！" % (mdDirPath))
            if (os.path.isdir(imgDirPath)):
                print("转储图片保存目录%s已存在！" % (imgDirPath))
            else:
                os.mkdir(imgDirPath)
                print("转储图片保存目录%s已创建！" % (imgDirPath))
        except Exception as e:
            raise e
