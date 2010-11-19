from ajax_filtered_fields.forms import AjaxManyToManyField
from django.utils.encoding import smart_unicode


class AjaxUserField(AjaxManyToManyField):
    def label_from_instance(self, obj):
        if obj.first_name and obj.last_name:
            return "%s, %s" % (obj.last_name, obj.first_name)
        return smart_unicode(obj)
 
