from django.contrib import admin

# Register your models here.
from news import models
class newsAdmin(admin.ModelAdmin):
    list_display = ('c_name', 'title','news_time','num_click','news_id')
class tagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_time', 'news_url', 'tag_id')

admin.site.register(models.News, newsAdmin)
admin.site.register(models.Label, tagsAdmin)
