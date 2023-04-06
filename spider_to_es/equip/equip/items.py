# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from .es_orm import equipsType


class EquipItem1(scrapy.Item):
    # 需要提取的字段
    post_author = scrapy.Field()  # 发布作者
    author_link = scrapy.Field()  # 
    post_date = scrapy.Field()  # 发布时间
    title = scrapy.Field()  # 标题
    title_link = scrapy.Field()  # 标题链接
    item_summary = scrapy.Field()  # 摘要

    def save_to_es(self):
        print("--------------- 开始存入数据库 1 ---------------")
        equipObj = equipsType()  # 实例化elasticsearch(搜索引擎对象)
        equipObj.title = self['title']  # 字段名称=值
        equipObj.description = self['item_summary']
        equipObj.url = self['title_link']
        equipObj.riqi = self['post_date']
        equipObj.site = '船海装备网'
        equipObj.save()  # 将数据写入elasticsearch(搜索引擎对象)
        return

class Company(scrapy.Item):
    cname = scrapy.Field()
    link = scrapy.Field()
    brand = scrapy.Field()
    model = scrapy.Field()
    diameter = scrapy.Field()
    rotate = scrapy.Field()
    power = scrapy.Field()
    more = scrapy.Field()
    riqi = scrapy.Field()

    def save_to_es(self):
        print("--------------- 开始存入数据库 2 ---------------")
        equipObj = equipsType()  # 实例化elasticsearch(搜索引擎对象)
        equipObj.title = self['cname']  # 字段名称=值
        equipObj.description = self['model']
        equipObj.url = self['link']  # 字段名称=值
        equipObj.riqi = self['riqi']
        equipObj.site = '国际船舶网'
        equipObj.save()  # 将数据写入elasticsearch(搜索引擎对象)
        return
# class EquipItem2(scrapy.Item):
#     # 需要提取的字段
#     title = scrapy.Field()  # 标题
#     title_link = scrapy.Field()  # 标题链接
#     machine = scrapy.Field()

#     def save_to_es(self):
#         print("--------------- 开始存入数据库 222222222222222222 ---------------")
#         equipObj = equipsType()  # 实例化elasticsearch(搜索引擎对象)
#         equipObj.title = self['title']  # 字段名称=值
#         equipObj.url = self['title_link']
#         equipObj.machine = self['machine']
#         equipObj.save()  # 将数据写入elasticsearch(搜索引擎对象)
#         return