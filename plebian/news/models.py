import datetime
from django.db import models
from plebian.core.models import Publishable, Ownable
from django.contrib.auth.models import User


sections = (
        ('news','News and Events'),
        ('press','Press Releases'),
        )

class NewsItem(Publishable, Ownable):
    slug = models.SlugField(max_length=50)
    section = models.CharField(max_length=160, default=sections[0][0], choices=sections)
    creator = models.ForeignKey(User, related_name="created_news_item_set", editable=False) 
    modifier = models.ForeignKey(User, related_name="modified_news_item_set", editable=False)
    body = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-live',)
        verbose_name = "News Entry"
        verbose_name_plural = "News, Events, and Press Releases"
        unique_together = (("slug", "section"),)

    def get_absolute_url(self):
        return "/%s/%s/" % ( self.section, self.slug )

    def humanized_section(self):
        for i in sections:
            if i[0] == self.section:
                result = i[1]
                return result
    humanized_section.short_description = 'Section'
