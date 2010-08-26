import datetime
import reversion
from django.db import models

sections = (
        ('news','News and Events'),
        ('press','Press Releases'),
        )

class NewsItem(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=320)
    body = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    live = models.DateTimeField(help_text="Date this entry should go live. This is the only public-facing date.", default=datetime.datetime.now())
    section = models.CharField(max_length=160, default=sections[0][0], choices=sections)

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
