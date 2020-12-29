实现参考了csdn2hexo[地址](https://github.com/LeesinDong/csdn2hexo)
将原本的java语言改成用python实现，并调整了一些逻辑

环境python3.6+PyCharm

用PyCharm打开项目
执行main.py启动



```bash
# 是否第一次使用。第一次使用会强制修改配置文件
is_first=True
# 是否渲染hexo头部
head=False
# 是否手动为每篇文章设置head（如果为True，每篇文章都将会要求输入信息）
set_head=False
# md文章头部配置
# 分类和标签逗号隔开
author=
tags=a,b,c
categories=a,b,c
# 文件命名规则  
# 可选值:date title ，date根据日期命名，title根据文章名命名（若上面头部title已设置则头部配置优先）
title_type=title
# 以下文件夹若已存在均不会删除原文件
# 文件保存的绝对路径，即img html post这三个文件夹的父文件夹(最好为hexo博客的source目录)
file_Path=G:\\Blog\\StephenZSIR\\source
# 设置保存原html的文件路径（将会新建在file_Path下）
html_path=html
# 设置转储图片的文件路径（将会新建在file_Path下）
image_path=upload_images
# 转储图片的线上地址前缀(转储时会在后面加图片名称)
web_image_path=https://stephenzsir.github.io/upload_images/
# 设置保存转换好的md的文件路径（将会新建在file_Path下）
md_path=_posts
# 是否转储博客线上图片
img_flag=True
# 设置爬取的方式，默认是从第一页往后不断的下载的
# 可选的方式：
#       1 默认轮询从第一页开始往后
#       2 分类专栏方式
#       3 指定某篇文章
#       4 指定页数
url_way=3
# 具体的四种抓取方法的地址填写（视自己情况而定）
url_way_1=https://elasticstack.blog.csdn.net/article/list/
url_way_2=https://elasticstack.blog.csdn.net/ubuntutouch/category_10053541.html
url_way_3=https://elasticstack.blog.csdn.net/article/details/102728604
url_way_4=https://elasticstack.blog.csdn.net/article/list/2
# 是否在转换后md中显示原文地址 
source_view=True
```



