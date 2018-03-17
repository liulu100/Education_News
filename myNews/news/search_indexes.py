# -*- coding:utf8 -*-
from news.models import News
from haystack import indexes

'''每个索引里面必须有且只能有一个字段为document=True，这代表haystack 和搜索引擎
   将使用此字段的内容作为索引进行检索(primary field)。其他的字段只是附属的属性，
   方便调用，并不作为检索数据。'''
'''haystack提供了use_template=True在text字段，这样就允许我们使用数据模板去建立搜索引擎索引的文件
数据模板的路径为yourapp/templates/search/indexes/yourapp/note_text.txt
文件名必须为要索引的类名_text.txt'''
class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
    #确定在建立索引时有些记录被索引，这里我们简单地返回所有记录