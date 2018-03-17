# -*- coding:utf8 -*-

from os import path
import matplotlib.pyplot as plt
from news import models
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import jieba
from collections import Counter

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#去掉分词后的停用词，声明为全局变量
stopwords = {}
d = path.dirname(__file__)

def create_tag_cloud():
    get_government_tag()
    get_english_tag()
    get_MBA_tag()
    get_collegetest_tag()
    get_abroad_tag()
    get_hightest_tag()
    get_immigrant_tag()
    get_school_tag()

'''生成校园AND中考新闻的标签词云图'''
def get_school_tag():
    c_name_list = ['中考','中小学']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='school.png')

'''生成高考新闻的标签词云图'''
def get_hightest_tag():
    c_name_list = ['高考']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='high_test.png')


'''生成考研新闻的标签词云图'''
def get_collegetest_tag():
    c_name_list = ['考研']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='college_test.png')

'''生成公务员新闻的标签词云图'''
def get_government_tag():
    c_name_list = ['公务员']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='government.png')

'''生成英语新闻的标签词云图'''
def get_english_tag():
    c_name_list = ['外语', '少儿英语', '四六级']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='english.png')


'''生成留学AND国际学校新闻的标签词云图'''
def get_abroad_tag():
    c_name_list = ['出国留学', '国际学校','留学']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='abroad.png')

'''生成商学院新闻的标签词云图'''
def get_MBA_tag():
    c_name_list = ['商学院']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='MBA.png')

'''生成移民新闻的标签词云图'''
def get_immigrant_tag():
    c_name_list = ['移民']
    data = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:40].values_list('title', 'news_tag')
    processChinese(data)
    data = count_frequencies()
    tag_wordcloud(data, filename='immigrant.png')


#从文件中读取停用词，存入字典中，以便分词后清洗数据
def importStopword(filename=''):

    global stopwords
    f = open(filename, 'r')
    line = f.readline().rstrip()
    '''readline读取文件中的一行，rstrip：rstrip() 删除 string 字符串末尾的指定字符（默认为空格）
    返回删除 string 字符串末尾的指定字符后生成的新字符串'''

    while line:
        stopwords.setdefault(line, 0)
        stopwords[line] = 1
        line = f.readline().rstrip()
        '''读入的一行数据作为字典的key ，value设为1，重新读入一行'''
       # print stopwords

    f.close()


'''通过调用jieba分词库实现对数据的分词，同时实现对数据的清洗，最后把数据存入文件中'''
def processChinese(data):
    # d = path.dirname(__file__)
    '''调用函数importStopword（），读取停用词./static\txt\stopwords.txt'''
    #importStopword(filename='/static/txt/stopwords.txt')

    importStopword(filename=( path.join(d , "./static/txt/stopwords.txt")))
    '''打开文件存入分词并清洗后的数据'''
    # wf = open('../static/txt/clean_title.txt', 'w+')
    wf = open((path.join(d, './static/txt/clean_title.txt')), 'w+')
    for data_line in data:
        for line in data_line:
            '''调用jieba分词库的cut（）方法进行分词，该方法有两个参数， 1) 第一个参数为需要分词的字符串
            2）cut_all参数用来控制是否采用全模式（待分词的字符串可以是gbk字符串、utf-8字符串或者unicode）
            返回的结构都是一个可迭代的generator，可以使用for循环来获得分词后得到的每一个词语(unicode)，
            也可以用list(jieba.cut(...))转化为list'''
            word = jieba.cut(line, cut_all=False)
            for tag in word:
                tag = tag.encode('gbk')
                if tag not in stopwords:
                    if tag != ' ':
                        tag = tag + '\n'
                        # print tag
                        wf.write(tag)
    wf.close()

'''计算词频 使用python collections库的Counter类 '''
def count_frequencies():
    '''list存放从文本中读取的词语'''
    list1 = []

    # with open('./static/txt/clean_title.txt', 'r') as fr:
    with open((path.join(d, './static/txt/clean_title.txt')), 'r') as fr:
        line = fr.readline().rstrip().decode('gbk')
        #for word in fr.read():
            #list1.append(word.split(',')) # 使用逗号进行切分
        while line:
            list1.append(line)
            line = fr.readline().rstrip().decode('gbk')

        '''Counter类：为hashable对象计数。返回值以字典的键值对形式存储，其中元素作为key，其计数作为value'''
        data = Counter(list1)

        '''返回一个TopN列表。如果n没有被指定，则返回所有元素。当多个元素计数值相同时，排列是无确定顺序的。'''
        data = dict(data.most_common(70))
        #print data
    return data

'''生成词云图。接收两个参数，一个参数接收统计词频后的字典对象，以及将要保存的文件名称'''
def tag_wordcloud(text , filename ):
    #d = path.dirname(__file__)
    # 设置背景图片
    #back_coloring = plt.imread("./static/img/color.jpg")
    back_coloring = plt.imread(path.join(d,"./static/img/color.jpg" ))

    wc = WordCloud(font_path=(path.join(d, './static/font/msyh.ttf')),
                   # font_path='./static/font/msyh.ttf',  # 设置字体
                   background_color="black",  # 背景颜色
                   max_words=45,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   max_font_size=200,  # 字体最大值
                   #random_state=3,
                   )
    # 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
    #wc.generate(text)
    wc.generate_from_frequencies(text)
    # txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(back_coloring)

    plt.figure()
    # 以下代码显示图片
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    #plt.show()
    #显示绘制好的图片
    # 绘制词云
    #filename = "./static/img/ %s" % filename
    # 保存图片
    #wc.to_file("./static/img/%s" % filename)
    wc.to_file(path.join(d, "./static/img/%s" %filename))


