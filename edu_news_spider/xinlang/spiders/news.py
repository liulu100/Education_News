# -*- coding: utf-8 -*-


import scrapy
import os
from xinlang.items import XinlangItem
import time
import bsddb
from hashlib import md5
class NewsSpider(scrapy.Spider):
    #def __init__(self):
        #self.dbenv = bsddb.db.DBEnv()
        #self.dbenv.open("word_freq_db", bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
        #self.db = bsddb.db.DB(self.dbenv)
        #self.db.open("word_freq.db", bsddb.db.DB_HASH, bsddb.db.DB_CREATE, 0666)

    name = "news"
    allowed_domains = ["sina.com.cn"]
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        # 教育类的url 和 标题<div class="clearfix" data-sudaclick="edunav">
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div[@data-sudaclick=\"edunav\"]/h3/a/@href').extract()
        parentTitle = response.xpath("//div[@id=\"tab01\"]/div[@data-sudaclick=\"edunav\"]/h3/a/text()").extract()

        # 所有小类的ur 和 标题
        subUrls = response.xpath('//div[@id=\"tab01\"]/div[@data-sudaclick=\"edunav\"]/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div[@data-sudaclick=\"edunav\"]/ul/li/a/text()').extract()

        # 爬取所有大类
        for i in range(0, len(parentTitle)):
            # 指定大类目录的路径和目录名
            # parentFilename = "./Data/" + parentTitle[i]

            # 如果目录不存在，则创建目录
            # if (not os.path.exists(parentFilename)):
                # os.makedirs(parentFilename)

            # 爬取所有小类
            for j in range(0, len(subUrls)):
                item = XinlangItem()
                # 保存大类的title和urls
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]
                # 检查小类的url是否以同类别大类url开头，如果是返回True (sports.sina.com.cn 和 sports.sina.com.cn/nba)
                if_belong = subUrls[j].startswith(item['parentUrls'])

                # 如果属于本大类，将存储目录放在本大类目录下
                if ( if_belong ):
                    # subFilename = parentFilename + '/' + subTitle[j]
                    # 如果目录不存在，则创建目录
                    # if (not os.path.exists(subFilename)):
                        # os.makedirs(subFilename)

                    # 存储 小类url、title和filename字段数据
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    # item['subFilename'] = subFilename

                    items.append(item)
        # 发送每个小类url的Request请求，得到Response连同包含meta数据 一同交给回调函数 second_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1': item}, callback=self.second_parse)

    # 对于返回的小类的url，再进行递归请求
    def second_parse(self, response):
        # 提取每次Response的meta数据
        meta_1 = response.meta['meta_1']

        # 取出小类里所有子链接<ul class="list01 l14 fblk">

        sonUrls = response.xpath('//a/@href').extract()

        items = []

        for i in range(0, len(sonUrls)):
            # 检查每个链接是否以大类url开头、以.shtml结尾，如果是返回True<a href="http://roll.edu.sina.com.cn/more/ky3/kyzx/hsky/kaoshi/index.shtml" target="_blank">话说考研</a>
            if_belong = sonUrls[i].endswith('index.shtml')

            # 如果属于本大类，获取字段值放在同一个item下便于传输
            if (if_belong):
                item = XinlangItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                # item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        # 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2': item}, callback=self.urls_parse)


    def urls_parse(self, response):
        # 提取每次Response的meta数据
        meta_2 = response.meta['meta_2']

        # 取出小类里所有子链接<ul class="list01 l14 fblk">
        ssonUrls = response.xpath('//a[contains(@href,"2017-05-09")]/@href').extract()
        #ssonUrls = response.xpath('//a[contains(@href,\"%s\")]/@href' % self.getDaytime()).extract()

        items = []
       # for i in range(0, len(ssonUrls)):
            # 检查每个链接是否以大类url开头、以.shtml结尾，如果是返回True
            # if_belong = ssonUrls[i].endswith('.shtml') and ssonUrls[i].startswith(meta_2['parentUrls'])

            #如果属于本大类，把链接存入数据库
            #urlMD5=self._get_urlmd5id(ssonUrls[i])
            #if(if_belong):
                #self.db.put(urlMD5, "url")

        for i in range(0, len(ssonUrls)):
            #urlMD5 = self._get_urlmd5id(ssonUrls[i])
            #value = self.read_from_db(urlMD5)
            if_belong = ssonUrls[i].endswith('.shtml') and ssonUrls[i].startswith(meta_2['parentUrls'])
            if (if_belong):
                item = XinlangItem()
                item['parentTitle'] = meta_2['parentTitle']
                item['parentUrls'] = meta_2['parentUrls']
                item['subUrls'] = meta_2['subUrls']
                item['subTitle'] = meta_2['subTitle']
                # item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = meta_2["sonUrls"]
                item['ssonUrls'] = ssonUrls[i]
                items.append(item)

        # 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['ssonUrls'], meta={'meta_3': item}, callback=self.detail_parse)


    # 数据解析方法，获取文章标题和内容
    def detail_parse(self, response):
        # 提取每次Response的meta数据
        item = response.meta['meta_3']

        content = ''

        head_list = response.xpath('//h1[@id=\"main_title\"]/text()').extract()
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()
        #content = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()
        time_list= response.xpath('//span[@class=\"titer\"]/text()').extract()
        news_source1 = response.xpath('//span[@class=\"source\"]/a/text()').extract()
        news_source2 = response.xpath('//span[@class=\"source\"]/text()').extract()
        news_source3 = response.xpath('//span[@id=\"media_name\"]/text()').extract()
        news_source4 = response.xpath('//span[@id=\"media_name\"]/a/text()').extract()
        news_tag = response.xpath('//p[@class=\"art_keywords\"]/a/text()').extract()

        for content_one in content_list:
            content = content +content_one + '\n'

        news_head = self.list_sum(head_list)
        news_time = self.list_sum(time_list)

        news_source1 = self.list_sum(news_source1)
        news_source2 = self.list_sum(news_source2)
        news_source3 = self.list_sum(news_source3)
        news_source4 = self.list_sum(news_source4)
        if (news_source1):
            news_source = news_source1
        elif (news_source2):
            news_source = news_source2
        elif (news_source3):
            news_source = news_source3
        elif (news_source4):
            news_source = news_source4
        else:
            news_source = '新浪教育'

        item['news_head'] = news_head
        item['content'] = content
        item['news_time'] = news_time
        item['news_source'] = news_source
        item['news_tag'] = news_tag

        yield item

    def list_sum(self,list):
        addsum = ''
        for list_one in list:
            addsum = addsum + list_one
        return addsum
    def getDaytime(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 获取key
    def read_from_db(self, key):
        return self.db.get(key)

    # 获取url的md5编码
    def _get_urlmd5id(self, url):
        return md5(url).hexdigest()

   # def spider_closed(self, spider):  # 爬虫结束时关闭文件
        #self.db.close()
        #self.dbenv.close()


