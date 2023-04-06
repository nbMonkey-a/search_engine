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
cd ./django_search_engine 
进入 SimpleSearchEngine-main\django_search_engine>
输入命令
python manage.py runserver
浏览器输入http://127.0.0.1:8000/
即可使用搜索引擎
