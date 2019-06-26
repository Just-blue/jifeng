# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JifengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    article_url = scrapy.Field()
    spider_type = scrapy.Field()
    scrawl_time = scrapy.Field()
    source = scrapy.Field()
    type = scrapy.Field()
