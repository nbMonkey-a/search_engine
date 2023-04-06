# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from cursor import cursor
import pymysql


class EquipPipeline:
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(
            host='localhost', 
            port=3306, 
            user='root', 
            passwd='123456',
            db='database', 
            charset='utf8')
        # 建立游标对象
        self.cursor = self.conn.cursor()
        self.cursor.execute('truncate table data')
        self.conn.commit()

    def process_item(self, item, spider):
        print("- 进入管道- item：", item)
        try:
            self.cursor.execute("insert into data (post_author,author_link,post_date,title,title_link,item_summary) \
            VALUES (%s,%s,%s,%s,%s,%s)", (item['post_author'], item['author_link'], item['post_date'],
                                          item['title'], item['title_link'], item['item_summary']))
            self.conn.commit()
        except pymysql.Error:
            print("Error%s,%s,%s,%s,%s,%s" % (item['post_author'], item['author_link'], item['post_date'],
                                              item['title'], item['title_link'], item['item_summary']))
        item.save_to_es()
        return item


class EquipPipeline2:
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                    db='database', charset='utf8')
        # 建立游标对象
        self.cursor = self.conn.cursor()
        self.cursor.execute('truncate table mainEngine')
        self.conn.commit()

    def process_item(self, item, spider):
        print("- 进入管道- item：", item)
        try:
            self.cursor.execute("insert into mainEngine (cname,link,brand,model,diameter,rotate,power,more,riqi) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (item['cname'], item['link'], item['brand'],
                                                   item['model'], item['diameter'], item['rotate'],
                                                   item['power'], item['more'], item['riqi']))
            self.conn.commit()
        except pymysql.Error:
            print("Error%s,%s,%s,%s,%s,%s,%s,%s,%s" % (item['cname'], item['link'], item['brand'],
                                                       item['model'], item['diameter'], item['rotate'],
                                                       item['power'], item['more'], item['riqi']))
        item.save_to_es()
        return item
