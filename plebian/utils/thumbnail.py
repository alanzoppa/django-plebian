from PIL import Image
from django.conf import settings
import os
import json
import random
import hashlib
import datetime
from django.contrib.sites.models import Site
from hmac import HMAC

def create_thumbnail(image, x, y):
    size = x,y

    path = image.path.split('/')[0:-1]
    url_root = image.url.split('/')[0:-1]
    filename = image.path.split('/')[-1]
    new_filename = str(x) + '-' + str(y) + '-' + filename
    new_path = '/'.join(path) + '/' + settings.THUMBNAIL_SUBDIR + '/' + new_filename
    new_url = '/'.join(url_root) + '/' + settings.THUMBNAIL_SUBDIR + '/' + new_filename

    try:
        test = Image.open(new_path)
    except IOError:
        im = Image.open(image.path)
        im.thumbnail(size, Image.ANTIALIAS)
        im.convert('RGB').save(new_path, "JPEG")

    return new_url

def destructive_thumbnail(image, x, y, new_filename=None):
    size = x,y
    output_path = image.split('.')[0] + '.jpg'
    try:
        im = Image.open(image)
    except IOError:
        return False
    im.thumbnail(size, Image.ANTIALIAS)
    im.convert('RGB').save(output_path, "JPEG")
    if image != output_path:
        os.remove(image)

    if new_filename:
        segments = output_path.split('/')[0:-1]
        path = '/'.join(segments) + '/'
        try:
            os.rename(output_path, path + new_filename)
        except:
            pass
        return new_filename
        
    return output_path.split('/')[-1]


def create_autocropped_thumbnail(image, x):
    size = x,x

    path = image.path.split('/')[0:-1]
    url_root = image.url.split('/')[0:-1]
    filename = image.path.split('/')[-1]
    new_filename = str(x) + '-' + str(x) + '-crop-' + filename
    new_path = '/'.join(path) + '/' + settings.THUMBNAIL_SUBDIR + '/' + new_filename
    new_url = '/'.join(url_root) + '/' + settings.THUMBNAIL_SUBDIR + '/' + new_filename

    try:
        test = Image.open(new_path)
    except IOError:
        im = Image.open(image.path)

        width, height = im.size

        if width > height:
           delta = width - height
           left = int(delta/2)
           upper = 0
           right = height + left
           lower = height
        else:
           delta = height - width
           left = 0
           upper = int(delta/2)
           right = width
           lower = width + upper

        im = im.crop((left, upper, right, lower))
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(new_path, "JPEG")

    return new_url

def destructive_autocrop(image, x):
    size = x,x
    im = Image.open(image)
    width, height = im.size

    if width > height:
       delta = width - height
       left = int(delta/2)
       upper = 0
       right = height + left
       lower = height
    else:
       delta = height - width
       left = 0
       upper = int(delta/2)
       right = width
       lower = width + upper

    im = im.crop((left, upper, right, lower))
    im.thumbnail(size, Image.ANTIALIAS)
    im.convert('RGB').save(image, "JPEG")

    return image
