# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''针对新浪新闻的Item'''
class XinlangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    '''大类的标题 和 url '''
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    '''小类的标题(即分类的标题） 和 url'''
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    # 小类目录存储路径
    #subFilename = scrapy.Field()

    '''小类下的子链接,即新闻列表的链接'''
    sonUrls = scrapy.Field()

    '''子链接中的链接,从新闻列表中获取到的链接'''
    ssonUrls = scrapy.Field()

    '''news_head文章标题;content新闻内容;news_time新闻的发布时间;
    news_source新闻来源；news_tag：新闻的标签'''
    news_head = scrapy.Field()
    content = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    news_tag = scrapy.Field()


'''针对网易新闻的Item'''
class EDU163Item(scrapy.Item):
    '''分类的标题和url'''
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()

    '''分类中的url即新闻url'''
    ssonUrls = scrapy.Field()

    '''news_head文章标题;content新闻内容;news_time新闻的发布时间;
    news_source新闻来源；news_tag：新闻的标签'''
    news_head = scrapy.Field()
    content = scrapy.Field()
    news_time = scrapy.Field()
    news_source = scrapy.Field()
    news_tag = scrapy.Field()