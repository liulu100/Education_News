# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy import log
from hashlib import md5
from items import XinlangItem, EDU163Item
import bsddb
import os
import time

#爬取到的数据以json的形式存储
class XinlangPipeline(object):

        #初始化函数
        def __init__(self):

            self.file = codecs.open('edu163_education.json', 'w', encoding='utf-8')  # 保存为json文件

        #pipeline的默认调用
        def process_item(self, item, spider):
            if spider.name == 'news_163':
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"  ##转为json的格式
                self.file.write(line)  # 写入文件中

            elif spider.name == 'news':
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"  ##转为json的格式
                self.file.write(line)  # 写入文件中

            return item
        def spider_closed(self, spider):#爬虫结束时关闭文件
            self.file.close()


#数据存入数据库中
class MySqlPipeline(object):
    #__init__会得到数据库的连接池
    def __init__(self,dbpool):
        self.dbpool = dbpool

    #定义一个类方法from_settings，得到settings中的Mysql数据库配置信息，得到数据库连接池dbpool
    @classmethod
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    #pipeline默认调用
    def process_item(self, item, spider):
        if spider.name =='news_163':
            '''调用插入方法'''
            d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
            #调用异常处理方法
            d.addErrback(self._handle_error)
        elif spider.name =='news':
            '''调用插入方法'''
            d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
            # 调用异常处理方法
            d.addErrback(self._handle_error)
        return item

    #数据写入数据库中
    def _do_upinsert(self,conn,item,spider):
        #获取url的md5编码,避免重复采集
        urlmd5id = self._get_urlmd5id(item)
        #把新闻的标签列表换成字符串
        news_tag = ""
        for tag_one in item['news_tag']:
            news_tag = news_tag +tag_one + "   "

        #插入新闻到数据库
        sql_insert_news = "insert into news(c_name,news_time,news_url,title,source,content,news_tag) values(%s,%s,%s,%s,%s,%s,%s)"
        #params = (item['subTitle'], item['news_time'],item['news_head'],item['news_source'],item['content'])
        conn.execute(sql_insert_news, (item["subTitle"], item["news_time"], urlmd5id, item["news_head"], item["news_source"],item["content"],news_tag))

        #sql_insert_label = "insert into label(news_url,tag_time,tag_name) values(%s,%s,%s)"

        #插入标签到数据库
        #for tag_one in item['news_tag']:
            #conn.execute(sql_insert_label, (urlmd5id, self.getDaytime(), tag_one))

    def getDaytime(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))


    # 获取url的md5编码
    def _get_urlmd5id(self, item):
        return md5(item['ssonUrls']).hexdigest()


    #异常处理
    def _handle_error(self, e,):
        log.err(e)



