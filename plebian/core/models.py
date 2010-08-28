import datetime
from django.db import models
from django.contrib.auth.models import User

class PublishedArticleManager(models.Manager):
    def get_query_set(self):
        return super(PublishedArticleManager, self).get_query_set().filter(published=True, live__lte=datetime.datetime.now(),)



class Publishable(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    live = models.DateTimeField(help_text="Date this entry should go live. This is the only public-facing date.", default=datetime.datetime.now())
    published = models.BooleanField(default=True)
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=320)


    objects = models.Manager()
    published_objects = PublishedArticleManager()

    class Meta:
        ordering = ('-live',)
        abstract = True


class Ownable(models.Model):
    contributor = models.ForeignKey(User, related_name="contributed_article_set", blank=True, null=True,) 

    class Meta:
        abstract = True
