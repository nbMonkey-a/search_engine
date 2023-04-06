# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrapy.selector import Selector
# from scrapy.http import Request
# from scrapy.item import Item, Field
# import csv
# import MySQLdb


# class Company(Item):
#     name = Field()
#     link = Field()
#     brand = Field()
#     model = Field()
#     diameter = Field()
#     rotate = Field()
#     power = Field()
#     more = Field()

# # class CompanyDetails(Item):
# #     name = Field()
# #     address = Field()
# #     phone = Field()
# #     email = Field()


# class EworldshipSpider(scrapy.Spider):
#     name = "eworldship"
#     allowed_domains = ["eworldship.com"]
#     start_urls = ["http://www.eworldship.com/app/engine"]

#     def parse(self, response):
#         sel = Selector(response)
#         companies = sel.xpath(
#             '//div[@class="left"]/div[@class="box_s1"]/div[@class="item"]')
#         for company in companies:
#             item = Company()
#             item['name'] = company.xpath(
#                 ".//div[@class='bs1_summary']/h3/a/text()").extract_first()
#             item['link'] = company.xpath(
#                 ".//div[@class='bs1_summary']/h3/a/@href").extract_first()
#             item["link"] = response.urljoin(item["link"])
#             yield scrapy.Request(url=item["link"], callback=self.parse_company_details, meta={"item": item})
#             # yield item

#         next_page = response.xpath("//div[@class='pages']/a[last()]/@href").extract_first()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

#     def parse_company_details(self, response):
#         item = response.meta['item']
#         sel = Selector(response)
#         # item = CompanyDetails()
#         # #爬取表格内容一定要注意tbody标签，很多都是浏览器衍生的虚标签，实际不存在啊！！！我被害惨了！！！
#         item['brand'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[1]/text()").extract_first()
#         item['model'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[2]/text()").extract_first()
#         item['diameter'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[3]/text()").extract_first()
#         item['rotate'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[4]/text()").extract_first()
#         item['power'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[5]/text()").extract_first()
#         item['more'] = sel.xpath(
#             "/html/body/div[1]/div[5]/div[2]/table/tr[1]/td[6]/a/@href").extract_first()
#         yield item


# # class MySQLPipeline(object):
# #     def __init__(self):
# #         self.conn = MySQLdb.connect(user='root', passwd='123456', db='database',
# #                                     host='localhost', port='3306', charset="utf8", use_unicode=True)
# #         self.cursor = self.conn.cursor()

# #     def process_item(self, item, spider):
# #         if isinstance(item, Company):
# #             try:
# #                 self.cursor.execute(
# #                     """INSERT INTO companies (name, link) VALUES (%s, %s)""", (item['name'], item['link']))
# #                 self.conn.commit()
# #             except MySQLdb.Error as e:
# #                 self.conn.rollback()
# #                 spider.logger.error("Error %s" % e)
# #         elif isinstance(item, CompanyDetails):
# #             try:
# #                 self.cursor.execute("""UPDATE companies SET address=%s, phone=%s, email=%s WHERE name=%s""", (
# #                     item['address'], item['phone'], item['email'], item['name']))
# #                 self.conn.commit()
# #             except MySQLdb.Error as e:
# #                 self.conn.rollback()
# #                 spider.logger.error("Error %s" % e)
# #         return item


# process = CrawlerProcess(get_project_settings())
# process.crawl(EworldshipSpider)
# process.start()
