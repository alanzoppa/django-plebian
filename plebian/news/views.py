import datetime
import time
import re
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.cache import cache_page
from django.conf import settings
from plebian.news.models import *


def newsentry(request, slug, section):
    newsentry = get_object_or_404(NewsItem, slug=slug, section=section, published=True, live__lte=datetime.datetime.now(),)
    recententries = NewsItem.objects.filter(published=True, section=section, live__lte=datetime.datetime.now())[:10]
    return render_to_response('news/entry.html', {'newsentry': newsentry, 'recententries': recententries, }, context_instance=RequestContext(request)) 

def index(request, section):
    newsentries = NewsItem.objects.filter(published=True, section=section, live__lte=datetime.datetime.now())
    paginator = Paginator(newsentries, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    return render_to_response('news/index.html', {'newsentries': page.object_list, 'page': page, }, context_instance=RequestContext(request)) 
