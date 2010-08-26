import datetime
from haystack.indexes import *
from haystack import site
from plebian.news.models import NewsItem

class NewsItemIndex(SearchIndex):
    text = CharField(document=True, use_template=True, model_attr='body')
    title = CharField(model_attr='title')
    live = DateTimeField(model_attr='live')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return NewsItem.objects.filter(live__lte=datetime.datetime.now(), published=True)

site.register(NewsItem, NewsItemIndex)
