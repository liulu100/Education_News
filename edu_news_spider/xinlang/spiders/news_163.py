# -*- coding: utf-8 -*-
import scrapy
from xinlang.items import EDU163Item
import time
import json
import jieba.analyse

class News163Spider(scrapy.Spider):
    name = "news_163"
    allowed_domains = ["edu.163.com"]
    start_urls = ['http://edu.163.com/']


    def parse(self, response):
        items = []
        '''获取导航栏的分类名和链接url'''
        subUrls = response.xpath('//div[@class=\"nav_bottom\"]/div[@class=\"area\"]/span/a/@href').extract()
        subTitle = response.xpath('//div[@class=\"nav_bottom\"]/div[@class=\"area\"]/span/a/text()').extract()

        for i in range(0, len(subTitle)):
            item = EDU163Item()

            '''如果分类名不等于首页，把它存入items'''
            '''由于分类的列表页是ajax动态获取的，如果直接请求无法获取到新闻链接，分析页面后，发现数据请求的网址为
            请求的js网址：
            移民：http://edu.163.com/special/0029881L/datalist_yimin.js?callback=data_callback
            留学：http://edu.163.com/special/0029881L/datalist_liuxue.js?callback=data_callback
            商学院：http://edu.163.com/special/0029881L/datalist_bschool.js?callback=data_callback
            校园：http://edu.163.com/special/0029881L/datalist_campus.js?callback=data_callback
            高考：http://edu.163.com/special/0029881L/datalist_gaokao.js?callback=data_callback
            外语：http://edu.163.com/special/0029881L/datalist_en.js?callback=data_callback
            请求该网址获取一个data_callback（）的json数据，将其处理解析后便可以得到新闻的网址'''

            if subTitle[i]!= '首页':
                item['subTitle'] = subTitle[i]
                #item['subUrls'] = subUrls[i]
                if subTitle[i] == '移民':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_yimin.js?callback=data_callback'

                if subTitle[i] == '留学':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_liuxue.js?callback=data_callback'

                if subTitle[i] == '商学院':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_bschool.js?callback=data_callback'

                if subTitle[i] == '校园':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_campus.js?callback=data_callback'

                if subTitle[i] == '高考':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_gaokao.js?callback=data_callback'

                if subTitle[i] == '外语':
                    item['subUrls'] = 'http://edu.163.com/special/0029881L/datalist_en.js?callback=data_callback'
                items.append(item)

        '''发送每个分类url的Request请求，得到Response连同包含meta数据 一同交给回调函数 second_parse 方法处理'''
        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1': item}, callback=self.second_parse)

    '''处理返回的每个分类url，分析出新闻的url进行再次请求'''
    def second_parse(self, response):

        ''' 提取每次Response的meta数据'''
        meta_1 = response.meta['meta_1']

        '''获取每个分类下的链接，即新闻的url newsdata_list'''
        ssonUrls = []
        # ssonUrls = response.xpath('//div[@class=\"news_title\"]/h3/a[contains(@href,\"%s\")]/@href'% self.getDaytime()).extract()
        html = response.body
        html = str(html).lstrip('data_callback(')
        html = str(html).rstrip(')').decode('gbk')
        #print html
        urls = json.loads(html)
        for url in urls:
            ssonUrls.append(url['docurl'])
        items = []

        for i in range(0, len(ssonUrls)):
            '''检查链接是否以edu.163.com 开头，是否以.html结尾，并且包含/17/0409的日期
            形如http://edu.163.com/17/0409/14/CHJ99EFR00297VGM.html'''
            if_belong = ssonUrls[i].endswith('.html') and ssonUrls[i].startswith('http://edu.163.com') and ssonUrls[i].find('/17/0509')>=0
            '''if_belong = ssonUrls[i].endswith('.html') and \
                        ssonUrls[i].startswith('http://edu.163.com') and\
                        ssonUrls[i].find('%s' % self.getDaytime()) >= 0'''
            #if_belong = ssonUrls[i].endswith('.html')

            if (if_belong):
                item = EDU163Item()

                item['subTitle'] = meta_1['subTitle']
                item['subUrls'] = meta_1['subUrls']
                #item['news_tag'] = news_tag
                item['ssonUrls'] = ssonUrls[i]
                items.append(item)

        ''' 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理'''
        for item in items:
            yield scrapy.Request(url=item['ssonUrls'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        ''' 提取每次Response的meta数据'''
        item = response.meta['meta_2']
        news_head = response.xpath('//div[@id=\"epContentLeft\"]/h1/text()').extract()
        news_time = response.xpath('//div[@class=\"post_time_source\"]/text()').extract()
        news_source = response.xpath('//div[@class=\"ep-source cDGray\"]/span[@class=\"left\"]/text()').extract()
        news_content = response.xpath('//div[@id=\"endText\"]/p/text()').extract()


        content = self.get_content(news_content)
        news_head = self.list_to_str(news_head)
        news_time = self.list_to_str(news_time)
        news_source = self.list_to_str(news_source)
        news_time = self.format_time(news_time)
        news_tag = self.get_news_tag(content)

        item['news_head'] = news_head
        item['content'] = content
        item['news_time'] = news_time
        item['news_source'] = news_source
        item['news_tag'] = news_tag

        yield item

    def get_content(self,news_content):
        content = ''
        for content_one in news_content:
            content = content +content_one + '\n'
        return content

    '''通过结巴分词库获取文档的关键词'''
    def get_news_tag(self, content):
        tags = jieba.analyse.extract_tags(content, topK=5)
        return tags

    def format_time(self,str):
        str = str.strip()
        str1 = str[:4]
        str2 = str[5:7]
        str3 = str[8:10]
        str4 = str[11:16]
        str = str1 + '年' + str2 + '月' + str3 + '日 ' + str4
        return str

    def list_to_str(self, list):
        addsum = ''
        for list_one in list:
            addsum = addsum + list_one
        return addsum

    def getDaytime(self):
        return time.strftime('%y/%m%d', time.localtime(time.time()))
