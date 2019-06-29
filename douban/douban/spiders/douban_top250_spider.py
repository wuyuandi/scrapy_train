# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanTop250SpiderSpider(scrapy.Spider):
    name = 'douban_top250_spider'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()

            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduction'] = content_s

            douban_item['star'] = i.xpath(".//div//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i.xpath(".//div//p[@class='quote']//span[@class='inq']/text()").extract_first()
            yield douban_item

        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse, dont_filter=True)
