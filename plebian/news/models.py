import datetime
import reversion
from django.db import models
from django.contrib.auth.models import User

class PublishedArticleManager(models.Manager):
    def get_query_set(self):
        return super(PublishedArticleManager, self).get_query_set().filter(published=True, live__lte=datetime.datetime.now(),)




sections = (
        ('news','News and Events'),
        ('press','Press Releases'),
        )

class NewsItem(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=50)
    published = models.BooleanField(default=True)
    contributor = models.ForeignKey(User, related_name="contributed_article_set", blank=True, null=True,) 
    creator = models.ForeignKey(User, related_name="created_news_item_set", editable=False) 
    modifier = models.ForeignKey(User, related_name="modified_news_item_set", editable=False)
    description = models.CharField(max_length=320)
    body = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    live = models.DateTimeField(help_text="Date this entry should go live. This is the only public-facing date.", default=datetime.datetime.now())
    section = models.CharField(max_length=160, default=sections[0][0], choices=sections)

    objects = models.Manager()
    published_objects = PublishedArticleManager()


    class Meta:
        ordering = ('-live',)
        verbose_name = "News Entry"
        verbose_name_plural = "News, Events, and Press Releases"
        unique_together = (("slug", "section"),)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % ( self.section, self.slug )

    def humanized_section(self):
        for i in sections:
            if i[0] == self.section:
                result = i[1]
                return result
    humanized_section.short_description = 'Section'
