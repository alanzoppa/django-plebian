import random
import json
from django.test.client import Client
from django.test import TestCase
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from plebian.news.models import *

class SimpleTest(TestCase):
    def test_validity_of_urls(self):
        c = Client()
        for i in NewsItem.objects.filter(published=True):
            print 'testing:', i.get_absolute_url()
            page = c.get(i.get_absolute_url())
            if not page.status_code == 200: assert False
