import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import pandas as pd
import re


class FidiboSearch(scrapy.Spider):
    name='virgool_content'
    def start_requests(self):
        urls = []
        for i in range(8):
            urls.append('https://virgool.io/topic/%D8%B1%D9%88%D8%A7%D9%86%D8%B4%D9%86%D8%A7%D8%B3%DB%8C?page='+str(i+1))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_front)


    def parse_front(self,response):
        articlelinks = response.xpath('//div[@class="post-content"][1]/a/@href').extract()
       
        for articlelink in articlelinks:
            yield response.follow(url =articlelink, callback=self.parse_page)

    def parse_page(self,response):

        title = response.xpath('/html/body/section/main/section/section[1]/section/article/div[1]/h1/text()').extract_first().strip()

        content = ' '.join(response.xpath('//p/text()').extract()).strip()

        yield {'title':title,'content':content}
    