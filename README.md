s
### 简介
<未命名搜索引擎>是一款基于ElasticSearch实现的搜索引擎。


### 功能
+ 检索使用elasticsearch
  + 倒排索引
  + 关键词高亮
+ 页面分页显示



### 主要技术栈
+ Scrapy
+ ElasticSearch    6.8.0
+ elasticsearch-dsl    6.4.0
+ Django


### 环境安装
+ elasticsearch-6.4.3<br>启动地址 http://127.0.0.1:9200/

+ elasticsearch-head ( 用于方便查看数据信息 )<br>启动地址 http://localhost:9100/
+ kibana-6.4.3 ( 用于方便对数据信息操作 )
+ 以上的安装版本要相符合

### 使用说明

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
cd ../../ 回到SimpleSearchEngine-main\ 目录下输入命令 
cd django_search_engine 
进入 SimpleSearchEngine-main\django_search_engine>
输入命令
python manage.py runserver
浏览器输入http://127.0.0.1:8000/
即可使用搜索引擎
   
