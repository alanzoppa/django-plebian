from django.contrib import admin
from plebian.news.models import *
from plebian.news.forms import NewsItemForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage


class NewsItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = NewsItemForm

    search_fields = ['title', 'description',]
    list_display = ('__unicode__', 'humanized_section', 'published', 'live', 'created', 'updated', )    
    list_filter = ['published', 'section', ]
    fieldsets = (
        (None, {
            'fields': ('published', 'section', 'title', 'slug', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('live', )
        }),
        (None, {
            'fields': ('body',)
        }),
    )

    def save_model(self, request, obj, form, change):
        url = request.META['HTTP_REFERER']
        method = url.split('/')[-2]
        add = False
        if method == 'add':
            add = True
        obj.modifier= request.user
        if add:
            obj.creator = request.user
        obj.save()



admin.site.register(NewsItem, NewsItemAdmin) 
