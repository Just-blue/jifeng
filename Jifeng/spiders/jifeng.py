# -*- coding: utf-8 -*-
from datetime import datetime

import requests
import scrapy
from scrapy import Request
from scrapy.http import TextResponse

from Jifeng.items import JifengItem


class JifengSpider(scrapy.Spider):
    name = 'jifeng'
    # allowed_domains = ['http://bbs.gfan.com/']

    replydic = dict()
    start_urls = ['http://bbs.gfan.com']

    def parse(self, response):
        lines = response.css('#ct > div > div > div.fl.bm > div.bm.bmw.flg.cl')

        for item in lines:
            url = item.css('div.bm_h.cl h1 ::attr(href)').extract_first()
            yield Request(url, callback=self.prase_section)

    def prase_section(self, response):
        lines = response.css('tr.fl_row')
        for item in lines:
            url = item.css('td h2 a::attr(href)').extract_first()
            yield Request(url, callback=self.acquice_forum)

    def acquice_forum(self, response):

        article_list = response.css('th.new a.ast')
        for article in article_list:
            article_url = article.css('::attr(href)').extract_first()

            item = JifengItem()
            item['type'] = response.css('h1.xs2 a::text').extract_first()
            item['source'] = '机锋网'
            item['scrawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['spider_type'] = '论坛'
            item['article_url'] = article_url
            item['title'] = article.css('::text').extract_first()
            item['content'] = list()
            yield Request(article_url, callback=self.parse_detail, meta={'item': item})

        nextpage = response.css('a.nxt::attr(href)').extract_first()

        if nextpage:
            yield Request(nextpage, callback=self.acquice_forum)

    def parse_detail(self, response):
        """
        解析详情页，若有下一页，递归执行
        :param response:
        :return:
        """
        item = response.meta('item')
        postlist = response.css('div#postlist>div')
        for post in postlist:
            info = dict()
            info['user_name'] = post.css('div.authi > a.xw1::text').extract_first()
            info['publish_time'] = post.css('div.authi em::text').extract_first()

            floorname = ''.join(post.css('td.plc > div.pi > strong > a ::text').extract())
            idurl = post.css('td.plc > div.pi > strong > a::attr(href)').extract_first()  # 楼层链接
            self.replydic[idurl] = floorname  # 楼层链接与楼层id映射
            info['id'] = floorname

            # 判断有无回复楼层，无则设置为0
            replyurl = post.css('div.quote > blockquote ::attr(href)').extract_first()
            if replyurl:
                replyid = self.replydic.get(replyurl)
            else:
                replyid = 0
            info['reply_id'] = replyid

            item['content'].append(info)

        nexturl = response.css('a.nxt::attr(href)').extract_first()
        if nexturl:
            yield Request(nexturl, callback=self.parse_detail,meta={'item': item})
        else:
            self.replydic.clear()
            yield item