from plebian.core.admin import PublishableAdmin
from plebian.news.models import *
from plebian.news.forms import NewsItemForm
from django.contrib import admin



class NewsItemAdmin(PublishableAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = NewsItemForm

    search_fields = ['title', 'description',]
    list_display = ('__unicode__', 'humanized_section', 'contributor', 'published', 'live', 'created', 'modified', 'creator', 'modifier',)
    list_filter = ['published', 'section', ]
    fieldsets = (
        (None, {
            'fields': ( 'section', 'title', 'description', 'contributor',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('slug','published','live',)
        }),
        (None, {
            'fields': ('body',)
        }),
    )

admin.site.register(NewsItem, NewsItemAdmin) 
