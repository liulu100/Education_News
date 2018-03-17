# -*- coding:utf8 -*-
from haystack.views import SearchView
from news import models
from views import get_time1


class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        name = ['教育', '最新', '热门']
        start = get_time1()
        Newses1 = models.News.objects.order_by('-news_time')[:8]
        Newses2 = models.News.objects.filter(news_time__gt=start).order_by('-num_click')[:8]
        Newses3 = self.get_Newese()
        context['name'] = name
        context['Newses1'] = Newses1
        context['Newses2'] = Newses2
        context['Newses3'] = Newses3
        return context

        # 获取数据库中最新的两条数据

    def get_Newese(self):
        Newses3 = models.News.objects.order_by('-news_time')[:2]
        return Newses3