from django.conf.urls.defaults import *

urlpatterns = patterns('plebian.news.views',

    (r'^$', 'index',),
    (r'^(?P<slug>[\w-]+)/$', 'newsentry',),
)
