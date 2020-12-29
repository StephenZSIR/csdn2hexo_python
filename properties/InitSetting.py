#-*- coding: utf-8 -*-
import os
import re

from properties import Properties
from paser import CorePaser
class InitSetting:
    # 读取文件
    props = Properties.Properties()
    paserCore = CorePaser.CorePaser()
    def __init__(self):
        print('InitSetting初始化')
        is_first = True
        is_first_view = self.props.get('is_first')
        if is_first_view=='False':
            is_first==False
        if is_first:
            self.settingInit()
            self.welcomeUI()
        else:
            self.welcomeUI()
    def welcomeUI(self):
        while True:
            message = '''
            ======================================================
            欢迎使用CSDN博客转HEXO博客工具:
            本工具可将线上CSDN中的html格式博客
            转换为HEXO博客所使用的MarkDown语言博客
            并可将线上图片转储到本地，现在开始使用吧
                输入 1 进入配置向导
                输入 2 按现有配置开始转换
                输入 3 快速开始
                输入 0 退出
            ======================================================
            '''
            print(message)
            num = input('>>')
            if num == '1':
                self.settingInit()
            elif num == '2':
                self.paserCore.paserCore()
            elif num == '3':
                self.fast_start()
            elif num == '0':
                num = input('点击回车键退出工具')
                break
            else:
                print('输入有误，请重新输入（输入0-3数字）')
    def fast_start(self):
        while True:
            message = '''
            ======================================================
            欢迎使用快速开始:
                步骤 1 输入爬取方式
                步骤 2 输入爬取地址
            ======================================================
            '''
            print(message)
            print('1 输入爬取方式')
            num = self.setting_property('url_way', '爬取方式', '1,2,3,4', 'value')
            print('2 输入爬取地址')
            if num == '1':
                self.setting_property('url_way_1', '方式1地址（全量分页爬取）', 'String', 'url')
            elif num == '2':
                self.setting_property('url_way_2', '方式2地址（分类专栏爬取）', 'String', 'url')
            elif num == '3':
                self.setting_property('url_way_3', '方式3地址（单篇博客爬取）', 'String', 'url')
            elif num == '4':
                self.setting_property('url_way_4', '方式4地址（单页模式爬取）', 'String', 'url')
            self.paserCore.paserCore()
            break
    def settingInit(self):
        while True:
            message = '''
            ======================================================
            欢迎使用配置向导:
                输入 1 设置MD文件head信息
                输入 2 设置存储路径信息
                输入 3 设置爬取博客信息
                输入 4 设置转换信息
                输入 5 查看说明
                输入 0 设置完成
            ======================================================
            '''
            print(message)
            num = input('>>')

            if num == '1':
                self.setting_one()
            elif num == '2':
                self.setting_two()
            elif num == '3':
                self.setting_three()
            elif num == '4':
                self.setting_four()
            elif num == '5':
                introduce = '''
                ======================================================
                设置MD文件head信息:
                    配置项      说明                       取值
                    head       是否渲染hexo头部            False,True
                    set_head   是否手动为每篇文章设置head    False,True
                    author     默认author                 String
                    tags       默认tags(多个用,隔开)        String
                    categories 默认categories(多个用,隔开)  String
                    title_type title类型                  date,title
                ======================================================
                设置存储路径信息:
                    配置项           说明                     取值
                    file_Path       保存根目录(博客source目录) String
                    html_path       原html保存目录名称        String
                    image_path      转储图片保存目录名称        String
                    md_path         MD文件保存目录名称         String
                ======================================================
                设置爬取博客信息:
                    配置项      说明                       取值
                    url_way    爬取方式                    1,2,3,4
                    url_way_1  方式1地址（全量分页爬取）      String
                    url_way_2  方式2地址（分类专栏爬取）      String
                    url_way_3  方式3地址（单篇博客爬取）      String
                    url_way_4  方式4地址（单页模式爬取）      String
                ======================================================
                设置转换信息:
                    配置项           说明                   取值
                    img_flag        是否转储图片            False,True
                    source_view     是否包含转载地址         False,True
                    web_image_path  转储图片线上地址前缀      String
                ======================================================
                '''
                print(introduce)
            elif num == '0':
                print('配置完成')
                self.props.put('is_first', 'False')
                break
            else:
                print('输入有误，请重新输入（输入0-5数字）')


    def is_valid_domain(self, value):
        if re.match(r'^https?:/{2}\w.+$', value):
            return True
        else:
            return False

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
            if type=='value':
                if value.count(str)>0 and str.count(',')==0:
                    self.props.put(field,str)
                    self.props = Properties.Properties()
                    print('%s的配置已修改为%s'%(field,str))
                    break
                else:
                    print('%s的取值必须为%s中的一个' % (field, value))
            elif type=='url':
                if self.is_valid_domain(str):
                    self.props.put(field, str)
                    self.props = Properties.Properties()
                    print('%s的配置已修改为%s' % (field, str))
                    break
                else:
                    print('%s的取值必须为网址' % (field))
            elif type=='path':
                if os.path.isdir(str):
                    self.props.put(field, str)
                    self.props = Properties.Properties()
                    print('%s的配置已修改为%s' % (field, str))
                    break
                else:
                    print('%s的取值必须为路径' % (field))
            elif type=='spilt':
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
    def setting_four(self):
        while True:
            message = '''
            ======================================================
            设置转换信息:
                输入 1 设置img_flag
                输入 2 设置source_view
                输入 3 设置web_image_path
                输入 4 查看说明
                输入 0 设置完成
            ======================================================
            '''
            print(message)
            num = input('>>')

            if num == '1':
                self.setting_property('img_flag','是否转储图片','False,True','value')
            elif num == '2':
                self.setting_property('source_view','是否包含转载地址','False,True','value')
            elif num == '3':
                self.setting_property('web_image_path','转储图片线上地址前缀','String','url')
            elif num == '4':
                introduce = '''
                ======================================================
                设置转换信息:
                    配置项           说明                   取值
                    img_flag        是否转储图片            False,True
                    source_view     是否包含转载地址         False,True
                    web_image_path  转储图片线上地址前缀      String
                ======================================================
                '''
                print(introduce)
            elif num == '0':
                print('设置完成')
                break
            else:
                print('输入有误，请重新输入（输入0-4数字）')


    def setting_three(self):
        while True:
            message = '''
            ======================================================
            设置爬取博客信息:
                输入 1 设置url_way
                输入 2 设置url_way_1
                输入 3 设置url_way_2
                输入 4 设置url_way_3
                输入 5 设置url_way_4
                输入 6 查看说明
                输入 0 设置完成
            ======================================================
            '''
            print(message)
            num = input('>>')

            if num == '1':
                self.setting_property('url_way','爬取方式','1,2,3,4','value')
            elif num == '2':
                self.setting_property('url_way_1','方式1地址（全量分页爬取）','String','url')
            elif num == '3':
                self.setting_property('url_way_2','方式2地址（分类专栏爬取）','String','url')
            elif num == '4':
                self.setting_property('url_way_3','方式3地址（单篇博客爬取）','String','url')
            elif num == '5':
                self.setting_property('url_way_4','方式4地址（单页模式爬取）','String','url')
            elif num == '6':
                introduce = '''
                ======================================================
                设置爬取博客信息:
                    配置项      说明                       取值
                    url_way    爬取方式                    1,2,3,4
                    url_way_1  方式1地址（全量分页爬取）      String
                    url_way_2  方式2地址（分类专栏爬取）      String
                    url_way_3  方式3地址（单篇博客爬取）      String
                    url_way_4  方式4地址（单页模式爬取）      String
                ======================================================
                '''
                print(introduce)
            elif num == '0':
                print('设置完成')
                break
            else:
                print('输入有误，请重新输入（输入0-6数字）')

    def setting_two(self):
        while True:
            message = '''
            ======================================================
            设置存储路径信息:
                输入 1 设置file_Path
                输入 2 设置html_path
                输入 3 设置image_path
                输入 4 设置md_path
                输入 5 查看说明
                输入 0 设置完成
            ======================================================
            '''
            print(message)
            num = input('>>')

            if num == '1':
                self.setting_property('file_Path','保存根目录(博客source目录)','String','path')
            elif num == '2':
                self.setting_property('html_path','原html保存文件夹名称','String','String')
            elif num == '3':
                self.setting_property('image_path','转储图片保存文件夹名称','String','String')
            elif num == '4':
                self.setting_property('md_path','MD文件保存文件夹名称','String','String')
            elif num == '5':
                introduce = '''
                ======================================================
                设置存储路径信息:
                    配置项           说明                     取值
                    file_Path       保存根目录(博客source目录)  String
                    html_path       原html保存文件夹名称       String
                    image_path      转储图片保存文件夹名称       String
                    md_path         MD文件保存文件夹名称        String
                ======================================================
                '''
                print(introduce)
            elif num == '0':
                print('设置完成')

                break
            else:
                print('输入有误，请重新输入（输入0-5数字）')

    def setting_one(self):
        while True:
            message = '''
            ======================================================
            设置MD文件head信息:
                输入 1 设置head
                输入 2 设置set_head
                输入 3 设置author
                输入 4 设置tags
                输入 5 设置categories
                输入 6 设置title_type
                输入 7 查看说明
                输入 0 设置完成
            ======================================================
            '''
            print(message)
            num = input('>>')

            if num == '1':
                self.setting_property('head','是否渲染hexo头部','False,True','value')
            elif num == '2':
                self.setting_property('set_head','是否手动为每篇文章设置head','False,True','value')
            elif num == '3':
                self.setting_property('author','默认author','String','String')
            elif num == '4':
                self.setting_property('tags','默认tags(多个用,隔开)','String','spilt')
            elif num == '5':
                self.setting_property('categories','默认categories(多个用,隔开)','String','spilt')
            elif num == '6':
                self.setting_property('title_type','title类型','date,title','value')
            elif num == '7':
                introduce = '''
                ======================================================
                设置MD文件head信息:
                    配置项      说明                       取值
                    head       是否渲染hexo头部            False,True
                    set_head   是否手动为每篇文章设置head    False,True
                    author     默认author                 String
                    tags       默认tags(多个用,隔开)        String
                    categories 默认categories(多个用,隔开)  String
                    title_type title类型                  date,title
                ======================================================
                '''
                print(introduce)
            elif num == '0':
                print('设置完成')
                break
            else:
                print('输入有误，请重新输入（输入0-7数字）')