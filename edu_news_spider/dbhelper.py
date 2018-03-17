# -*- coding: utf-8 -*-
#调试数据库
import MySQLdb

conn = MySQLdb.Connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123456',
                       db='education_news',
                       charset='utf8')
cursor = conn.cursor()
sql_insert = "insert into news(c_name,news_time,title,source,content) values(%s,%s,%s,%s,%s)"
cursor.execute(sql_insert, ("考研","2017年03月02日 09:59","北京大学2017年硕士研究生招生复试基本分数线","",""))
conn.commit()

cursor.close()
conn.close()
