import datetime
from django.db import models
from plebian.utils.thumbnail import create_autocropped_thumbnail
from django.conf import settings
from django.contrib.auth.models import User

class PublishedObjectManager(models.Manager):
    def get_query_set(self):
        return super(PublishedObjectManager, self).get_query_set().filter(published=True, live__lte=datetime.datetime.now(),)


class Publishable(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    creator = models.ForeignKey(User, related_name="created_%(class)s_set", editable=False) 
    modifier = models.ForeignKey(User, related_name="modified_%(class)s_set", editable=False)
    live = models.DateTimeField(help_text="Date this entry should go live. This is the only public-facing date.", default=datetime.datetime.now())
    published = models.BooleanField(default=True)
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=320)
    slug = models.SlugField(max_length=50, unique=True)

    objects = models.Manager()
    published_objects = PublishedObjectManager()

    class Meta:
        ordering = ('-live',)
        abstract = True

    def _implemented_fields(self):
        return [i for i in self._meta._name_map.iterkeys()]

    def _get_image_set(self):
        try:
            return eval('self.%simage_set' % self._meta.module_name)
        except AttributeError:
            return False

    @models.permalink
    def get_absolute_url(self):
        return ('single_%s' % self._meta.module_name, (), {'slug': self.slug})

    def primary_thumb(self):
        try:
            image = self._get_image_set().filter(primary=True)[0]
        except IndexError:
            try:
                image = self._get_image_set().all()[0]
            except IndexError:
                return False
        except AttributeError:
            ''' This probably means that there is no associated image model. '''
            return False
        return image.thumbnail_dict()

    def as_simpledict(self):
        obj = {
           'id': self.id,
           'title': self.title,
           'description': self.description,
            }

        if 'contributor' in self._implemented_fields():
            obj['contributor'] = self.contributor.username

        if 'category' in self._implemented_fields() and self.category:
            obj['category'] = self.category.title

        if self.primary_thumb():
            obj['thumbnail'] = self.primary_thumb()

        if self.get_absolute_url():
            obj['get_absolute_url'] = self.get_absolute_url()

        return obj

    def __unicode__(self):
        return self.title


class RelatedImage(models.Model):
    published = models.BooleanField(default=True,)
    primary = models.BooleanField(default=False)
    title = models.CharField(max_length=160,)
    image = models.ImageField(upload_to="related_images/images", max_length=200,)
    caption = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ('-primary',)
        abstract = True

    def __unicode__(self):
        return self.title

    def thumbnail(self, size):
        return create_autocropped_thumbnail(self.image, size)

    def thumbnail_dict(self):
        return_dict = {}
        for key,value in settings.THUMBNAIL_SIZES.iteritems():
            return_dict[key] = self.thumbnail(value)
        return return_dict

    def as_dict(self):
        obj = {
            'primary': self.primary,
            'thumbnail': self.thumbnail_dict(),
            }

        if self.title:
            obj['title'] = self.title
        if self.caption:
            obj['caption'] = self.caption
        return obj
