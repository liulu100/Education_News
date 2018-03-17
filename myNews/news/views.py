# -*- coding:utf8 -*-
from django.shortcuts import render
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import models

from datetime import datetime, timedelta
from django.core.mail import send_mail

# Create your views here.
def school_label(request):
    #get_school_tag()
    #create_tag_cloud()
    #processChinese(label)
    #data = count_frequencies()
    #tag_wordcloud(data, filename='school.png')
    Newses3 = get_Newese()
    #label = models.News.objects.filter(c_name='中小学').order_by('-news_time')[:50].values_list('title', 'news_tag')
    return render(request, 'news/thanks.html', {'Newses3': Newses3})

#发送邮件模块
def send_email(request):
    errors = []
    Newses3 = get_Newese()
    if request.method == 'POST':
        if not request.POST.get('name', ''):
            errors.append('请输入您的名字！.')
        if not request.POST.get('message', ''):
            errors.append('请输入您的消息内容！')
        if not request.POST.get('email', ''):
            errors.append('请输入您的邮箱！')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('不合法的邮箱格式！')
        if not errors:
            subject = request.POST['name']+'\t' +request.POST['email']
            message = '来自:' + request.POST['email']+'\n' +'内容:' + request.POST['message']
            send_mail(
                subject,
                message,
                #request.POST.get('email', ),
                '18380122769@163.com',
                ['18380122769@163.com'],
            )
            return render(request, 'news/thanks.html', {'Newses3': Newses3})

    return render(request, 'news/contact.html', {'errors': errors, 'Newses3': Newses3})

"""主页面显示"""
def index(request):
    start = get_time1()
    name = ['教育', '最新', '热门']
    Newses1 = models.News.objects.order_by('-news_time')[:8]
    Newses2 = models.News.objects.filter(news_time__gt=start).order_by('-num_click')[:8]
    Newses3 = get_Newese()
    return render(request, 'news/index.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

#实现上一篇新闻页面跳转，获取到请求的id，查找该id下的前一条，把数据传传给前端
def previous_page(request,news_id):
    start = get_time1()
    news1 = models.News.objects.get(pk=news_id)
    mark = 0
    try:
        news2 = models.News.objects.filter(c_name=news1.c_name).order_by('news_time')
        news1 = news2.filter(news_time__gt=news1.news_time).order_by('news_time')[:1]
        #news[0].num_click = news[0].num_click + 1
        #news[0].save()
        news = models.News.objects.get(pk=news1[0].news_id)
        news.num_click = news.num_click + 1
        news.save()
        news = models.News.objects.get(pk=news1[0].news_id)
    except:
        news = models.News.objects.get(pk=news_id)
        news.num_click = news.num_click + 1
        news.save()
        news = models.News.objects.get(pk=news_id)
        mark = 1
    name = get_c_name(news.c_name)
    Newses1 = models.News.objects.filter(c_name=news.c_name).order_by('-news_time')[:8]
    Newses2 = models.News.objects.filter(c_name=news.c_name).filter(news_time__gt=start).order_by('-num_click')[:8]
    Newses3 = get_Newese()
    # label= news.label_set.all(),'Labels': label
    return render(request, 'news/single.html', {'News': news,
                                                'Newses1': Newses1,
                                                'Newses2': Newses2,
                                                'Newses3': Newses3,
                                                'name': name,
                                                'mark': mark})


#实现下一篇新闻页面跳转，获取到请求的id，查找该id下的后一条，把数据传传给前端
def next_page(request, news_id):
    start = get_time1()
    news1 = models.News.objects.get(pk=news_id)
    mark = 0
    try:
        news2 = models.News.objects.filter(c_name=news1.c_name).order_by('-news_time')
        news1 = news2.filter(news_time__lt=news1.news_time).order_by('-news_time')[:1]
        #news[0].num_click = news[0].num_click + 1
        #news[0].save()
        news = models.News.objects.get(pk=news1[0].news_id)
        news.num_click = news.num_click + 1
        news.save()
        news = models.News.objects.get(pk=news1[0].news_id)
    except:
        news = models.News.objects.get(pk=news_id)
        news.num_click = news.num_click + 1
        news.save()
        news = models.News.objects.get(pk=news_id)
        mark = 2
    name = get_c_name(news.c_name)
    Newses1 = models.News.objects.filter(c_name=news.c_name).order_by('-news_time')[:8]
    Newses2 = models.News.objects.filter(c_name=news.c_name).filter(news_time__gt=start).order_by('-num_click')[:8]
    Newses3 = get_Newese()
    # label= news.label_set.all(),'Labels': label
    return render(request, 'news/single.html', {'News': news,
                                                'Newses1': Newses1,
                                                'Newses2': Newses2,
                                                'Newses3': Newses3,
                                                'name': name,
                                                'mark': mark})

#实现对象分页功能，第一个参数伟请求内容，第二个为对象列表
#返回分页后的对象,每页显示10个
def page_split1(request,News_list):
    paginator = Paginator(News_list, 11)  # Show num contacts per page
    page = request.GET.get('page1')
    try:
        News = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        News = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        News = paginator.page(paginator.num_pages)
    return News

#实现对象分页功能，第一个参数伟请求内容，第二个为对象列表
#返回分页后的对象，每页显示7个
def page_split2(request,News_list):
    paginator = Paginator(News_list, 6)  # Show num contacts per page
    page = request.GET.get('page2')
    try:
        News = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        News = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        News = paginator.page(paginator.num_pages)
    return News

'''新闻点击量排行榜'''
def hit_top_list(request):
    start = get_time()
    name = ['教育', '热门', '最新']
    Newses1 = models.News.objects.order_by('-num_click').filter(news_time__gt=start)[:50]
    Newses2 = models.News.objects.order_by('-news_time')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''最新新闻排行榜'''
def New_top_list(request):
    start = get_time()
    name = ['教育', '最新', '热门']
    Newses1 = models.News.objects.order_by('-news_time')[:50]
    Newses2 = models.News.objects.order_by('-num_click').filter(news_time__gt=start)[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''校园新闻列表页面'''
def school_news_list(request):
    start = get_time()
    name = ['校园', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='中小学').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='中小学').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''中考新闻列表页面'''
def middle_test_list(request):
    start = get_time()
    name = ['中考', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='中考').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='中考').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''高考新闻列表页面'''
def high_text_list(request):
    start = get_time()
    name = ['高考', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='高考').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='高考').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''考研新闻列表页面'''
def college_text_list(request):
    start = get_time()
    name = ['考研', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='考研').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='考研').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''公务员新闻列表页面'''
def government_news_list(request):
    start = get_time()
    name = ['公务员', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='公务员').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='公务员').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''英语新闻列表页面'''
def english_news_list(request):
    start = get_time()
    name = ['英语', '最新', '热门']
    c_name_list = ['外语', '少儿英语', '四六级']
    Newses1 = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name__in=c_name_list).filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''出国留学新闻列表页面'''
def abroad_news_list(request):
    start = get_time()
    c_name_list = ['出国留学','留学']
    name = ['留学', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name__in=c_name_list).order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name__in=c_name_list).filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''国际学校新闻列表页面'''
def international_news_list(request):
    start = get_time()
    name = ['国际学校', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='国际学校').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='国际学校').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''商学院新闻列表页面'''
def MBA_news_list(request):
    start = get_time()
    name = ['商学院', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='商学院').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='商学院').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''移民新闻列表页面'''
def immigrant_news_list(request):
    start = get_time()
    name = ['移民', '最新', '热门']
    Newses1 = models.News.objects.filter(c_name='移民').order_by('-news_time')[:50]
    Newses2 = models.News.objects.filter(c_name='移民').filter(news_time__gt=start).order_by('-num_click')[:35]
    Newses3 = get_Newese()
    Newses1 = page_split1(request, Newses1)
    Newses2 = page_split2(request, Newses2)
    return render(request, 'news/about.html', {'Newses1': Newses1, 'Newses2': Newses2, 'name': name, 'Newses3': Newses3})

'''联系开发者页面'''
def contact(request):
    Newses3 = get_Newese()
    return render(request, 'news/contact.html',{'Newses3': Newses3})

'''新闻内容页面显示'''
def news_page(request, news_id):
    start = get_time1()
    #点击量功能的实现：当用户每请求一次页面，及请求一次News对象，就把该对象的点击量增加1
    news = models.News.objects.get(pk=news_id)
    news.num_click = news.num_click +1
    news.save()

    news = models.News.objects.get(pk=news_id)
    name = get_c_name(news.c_name)
    Newses1 = models.News.objects.filter(c_name=news.c_name).order_by('-news_time')[:8]
    Newses2 = models.News.objects.filter(c_name=news.c_name).filter(news_time__gt=start).order_by('-num_click')[:8]
    Newses3 = get_Newese()
    #label= news.label_set.all(),'Labels': label
    return render(request, 'news/single.html', {'News': news,
                                                'Newses1': Newses1,
                                                'Newses2': Newses2,
                                                'Newses3': Newses3,
                                                'name':name})

'''获取系统时间减去五天的时间，并把它转换为2017年04月08日 10:08 的形式
用于过滤点击量排行榜，保证是在一段时间内的热门'''
def get_time():
    now = datetime.now()
    start = now - timedelta(days=365)
    time = start.strftime("%Y年%m月%d日 %H:%M")
    return time

'''获取系统时间减去五天的时间，并把它转换为2017年04月08日 10:08 的形式
用于过滤点击量排行榜，保证是在一段时间内的热门'''
def get_time1():
    now = datetime.now()
    start = now - timedelta(days=365)
    time = start.strftime("%Y年%m月%d日 %H:%M")
    return time

#获取数据库中最新的三条数据
def get_Newese():
    Newses3 = models.News.objects.order_by('-news_time')[:2]
    return Newses3

#判断新闻所属类别，返回类别的名字
def get_c_name(name):
    #cmp(x,y) 函数用于比较2个对象，如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1
    #比较字符串可直接用==
    if (name == '中小学'):
        name = '校园'
    elif(name == '出国留学'):
        name = '留学'
    elif (name=='少儿英语' or name=='外语' or name=='四六级'):
        name = '英语'
    else:
        name = name
    return name


