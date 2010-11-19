from ajax_filtered_fields.forms import AjaxManyToManyField#, AjaxForeignKeyField
from django.utils.encoding import smart_unicode
from django.forms import ModelChoiceField


class AjaxUserField(AjaxManyToManyField):

    def _get_queryset(self):
        return self._queryset.order_by('last_name')

    def label_from_instance(self, obj):
        if obj.first_name and obj.last_name:
            return "%s, %s" % (obj.last_name, obj.first_name)
        return smart_unicode(obj)



class UserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.first_name and obj.last_name:
            return "%s, %s" % (obj.last_name, obj.first_name)
        return smart_unicode(obj)

