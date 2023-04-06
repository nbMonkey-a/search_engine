import scrapy
import csv
from elasticsearch_dsl import Date
from ..items import EquipItem1
from ..items import Company
from scrapy.selector import Selector
from scrapy.http import Request


class Equip_Spider(scrapy.Spider):
    name = 'equip'
    # 可以爬取的域名范围
    allowed_domains = ['shipoe.com']
    # 起始地址
    start_urls = ['https://www.shipoe.com/sell/list-1-.html',
                #   'https://www.shipoe.com/sell/list-4-.html',
                #   'https://www.shipoe.com/sell/list-19-.html',
                #   'https://www.shipoe.com/sell/list-28-.html',
                #   'https://www.shipoe.com/sell/list-44-.html',
                #   'https://www.shipoe.com/sell/list-56-.html',
                ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'equip.pipelines.EquipPipeline': 300,
        }
    }

    def parse(self, response):
        if 'shipoe' in response.url:
            # formLst = response.xpath('//form[@method="post"]/div[@class="list"]')
            for div in response.xpath('//form[@method="post"]/div[@class="list"]')[:2]:
                item = EquipItem1()
                item["post_author"] = div.xpath(
                    ".//ul/li[position()=4]/a/text()").extract_first()
                item["author_link"] = div.xpath(
                    ".//ul/li[position()=4]/a/@href").extract_first()
                item["post_date"] = div.xpath(
                    ".//span[@class='f_r']/text()").extract_first()
                item["title"] = div.xpath(
                    ".//ul/li[position()=1]/a/strong/text()").extract_first()
                item["title_link"] = div.xpath(
                    ".//ul/li[position()=1]/a/@href").extract_first()
                item["item_summary"] = div.xpath(
                    ".//li[@class='f_gray']/text()").extract()
                yield item
            # 取下页url
            # nexturl = response.xpath(
            #     "//div[@class='pages']/a[last()]/@href").extract_first()
            # print(nexturl)
            # if nexturl is not None:
            #     yield scrapy.Request(nexturl, callback=self.parse)

                # def parse_detail(self,response):
                #     item=response.meta['item']
                #     item['product_detail']=response.xpath('./div[@class="content c_b"]//text()').extract()

    # def closed(self,response):
    #     with open('datas.csv', 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.DictWriter(f, fieldnames=['title', 'title_link', 'item_summary', 'post_date'])
    #         writer.writeheader()
    #         for data in self.datas:
    #             writer.writerow(data)
            # 取下页url
            # nexturl = response.xpath(
            #     "//div[@class='pages']/a[last()]/@href").extract_first()
            # print(nexturl)
            # if nexturl is not None:
            #     yield scrapy.Request(nexturl, callback=self.parse)

    #     elif 'eworldship' in response.url:
    #         for div in response.xpath('//div[@class="left"]/div[@class="box_s1"]/div[@class="item"]'):
    #             item = EquipItem2()
    #             item["title"] = div.xpath(
    #                 ".//div[@class='bs1_summary']/h3/a/text()").extract_first()
    #             item["title_link"] = div.xpath(
    #                 ".//div[@class='bs1_summary']/h3/a/@href").extract_first()
    #             item["title_link"] = response.urljoin(item["title_link"])
                
    #             yield response.follow(item['title_link'],self.parse_div,meta={'item':item})
    #             # yield response.follow(url=item['title_link'],meta={'item':item},callback=self.parse_div)

    #         # 取下页url
            # next_page = response.xpath("//div[@class='pages']/a[last()]/@href").extract_first()
            # if next_page:
            #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    #         nexturl = response.xpath(
    #             "//div[@class='pages']/a[last()]/@href").extract_first()
    #         nexturl = response.urljoin(item['title_link'])
    #         print(nexturl)
    #         if nexturl:
    #             yield response.follow(nexturl,self.parse)

    # def parse_div(self,response):
    #         item = response.meta['item']
            
    #         item['machine'] = response.xpath('//table[@class='tablesorter']/tbody/tr/td[0]/text()')
    #         yield item

class EworldshipSpider(scrapy.Spider):
    name = "eworldship"
    allowed_domains = ["eworldship.com"]
    start_urls = ["http://www.eworldship.com/app/engine"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'equip.pipelines.EquipPipeline2': 300,
        }
    }

    # 解析函数，用于解析网页内容
    def parse(self, response):
        sel = Selector(response)
        companies = sel.xpath(
            '//div[@class="left"]/div[@class="box_s1"]/div[@class="item"]')
        for company in companies[:1]:
            item = Company()
            item['cname'] = company.xpath(
                ".//div[@class='bs1_summary']/h3/a/text()").extract_first()
            item['link'] = company.xpath(
                ".//div[@class='bs1_summary']/h3/a/@href").extract_first()
            item["link"] = response.urljoin(item["link"])
            yield scrapy.Request(url=item["link"], callback=self.parse_company_details, meta={"item": item})
        # 翻页爬取
        # next_page = response.xpath("//div[@class='pages']/a[last()]/@href").extract_first()
        # if next_page:
        #     yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
    # 进一步详情解析页面内容
    def parse_company_details(self, response):
        item = response.meta['item']
        #爬取页面内容时一定要注意 tbody 标签，很多都是浏览器衍生的虚标签，实际不存在！！！我被害惨了！！！
        #爬取table时，选中所有的 tr 需要使用 table//tr 双斜杠选取
        for row in response.xpath("/html/body/div[1]/div[5]/div[2]/table//tr"):
            item['brand'] = row.xpath(
                ".//td[1]/text()").extract_first()
            item['model'] = row.xpath(
                ".//td[2]/text()").extract_first()
            item['diameter'] = row.xpath(
                ".//td[3]/text()").extract_first()
            item['rotate'] = row.xpath(
                ".//td[4]/text()").extract_first()
            item['power'] = row.xpath(
                ".//td[5]/text()").extract_first()
            item['more'] = row.xpath(
                ".//td[6]/a/@href").extract_first()
            item['riqi'] = "2023-06-01"
            yield item
        # next_page ="http://www.eworldship.com" + response.xpath("/html/body/div[1]/div[5]/div[2]/div[2]/a[2]/@href").extract_first()
        # if next_page:
        #     yield scrapy.Request(next_page, callback=self.parse_company_details)