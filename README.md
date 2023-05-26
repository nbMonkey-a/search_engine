### 简介
MES是一款基于ElasticSearch实现的船用设备信息检索引擎。

### 主要技术栈
+ Scrapy
+ ElasticSearch
+ Elasticsearch-dsl
+ Django

### 功能
+ 检索使用elasticsearch
  + 倒排索引
  + 关键词高亮
+ 页面分页显示
+ 数据报表导出

### 环境安装
pip install -i http://pypi.douban.com/simple -r requirements.txt
  
国内镜像：
清华：https://pypi.tuna.tsinghua.edu.cn/simple

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

豆瓣：http://pypi.douban.com/simple/

+ kibana-6.4.3 ( 便于操作管理数据信息 )
+ 以上的安装版本要相符合

### 项目启动
1.
启动elasticsearch-6.4.3/bin/elasticsearch.bat
浏览器输入localhost:9200查看是否正常启动（即返回一个json）

2.
命令行输入
cd spider_to_es/equip
运行es_orm.py    
main.py
开始爬虫

3.
Ctrl+C/V 暂停爬虫
cd django_search_engine 
进入 MarineEquipmentSearch\django_search_engine 目录
输入命令
python manage.py runserver
浏览器打开http://127.0.0.1:8000/
即可使用搜索引擎
   
