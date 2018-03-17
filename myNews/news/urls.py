from django.conf.urls import url
from . import views
from . import search_view

urlpatterns = [
    url(r'^about/$', views.New_top_list, name='about'),
    url(r'^hit_top/$', views.hit_top_list, name='hit'),
    url(r'^contact/$', views.contact, name ='contact'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<news_id>[0-9]+)/$', views.news_page, name='news_page'),
    url(r'^school/$', views.school_news_list, name='school'),
    url(r'^middle_test/$', views.middle_test_list, name='middle_test'),
    url(r'^high_test/$', views.high_text_list, name='high_test'),
    url(r'^college_test/$', views.college_text_list, name='college_test'),
    url(r'^government/$', views.government_news_list, name='government'),
    url(r'^english/$', views.english_news_list, name='english'),
    url(r'^abroad/$', views.abroad_news_list, name='abroad'),
    url(r'^international/$', views.international_news_list, name='international'),
    url(r'^MBA/$', views.MBA_news_list, name='MBA'),
    url(r'^immigrant/$', views.immigrant_news_list, name='immigrant'),
    url(r'^(?P<news_id>[0-9]+)pre/$', views.previous_page, name='previous_page'),
    url(r'^(?P<news_id>[0-9]+)next/$', views.next_page, name='next_page'),
    url(r'^email/$', views.send_email, name='email'),
    url(r'^thanks/$', views.school_label, name='thanks'),

]
