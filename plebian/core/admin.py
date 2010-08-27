from django.contrib import admin


class PublishableAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        url = request.META['HTTP_REFERER']
        method = url.split('/')[-2]
        add = False
        if method == 'add':
            add = True
        obj.modifier= request.user
        if add:
            obj.creator = request.user
        if not obj.contributor:
            obj.contributor = request.user
        obj.save()
