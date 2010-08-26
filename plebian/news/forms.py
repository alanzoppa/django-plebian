from django import forms
from django.forms.models import ModelForm
from plebian.news.models import *
from tinymce.widgets import TinyMCE
from django.conf import settings

class NewsItemForm(ModelForm):
    body = forms.CharField(widget=TinyMCE())

    class Meta:
        model = NewsItem 
