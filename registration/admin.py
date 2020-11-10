from django.contrib import admin
from .models import *
from itertools import chain
from research.models import Research
from django.contrib.auth.models import Group

from orders.models import Orders
# Register your models here.


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        try:
            data[f.name] = [i.email for i in f.value_from_object(instance)]
        except AttributeError:
            data[f.name] = [i.id for i in f.value_from_object(instance)]

    return data


class ResearchInline(admin.TabularInline):
    model = Research
    fk_name = "author"
    extra = 1


class QAdminsAdmin(admin.ModelAdmin):
    list_display = ['admin_status']
    inlines = [ResearchInline]
    search_fields = ['admin_status__email', 'admin_status__name']

    class Meta:
        model = QAdmins

    def get_queryset(self, request):
        if request.user.is_superuser == 0:
            only_me = QAdmins.objects.filter(id=request.user.id)
            return only_me
        else:
            everybody = QAdmins.objects.all()
            return everybody


class ClientsAdmin(admin.ModelAdmin):
    list_display = ['client_status']
    search_fields = ['client_status__email', 'client_status__name']

    class Meta:
        model = Clients


class OrdersInline(admin.TabularInline):
    model = Orders
    fk_name = "customer"
    extra = 0


class UsersAdmin(admin.ModelAdmin):
    list_display = ['email', 'primary_reference', 'initial_reference']
    inlines = [OrdersInline]
    search_fields = ['email', 'name']

    def photo_show(self, obj):
        return mark_safe('<img src="{url}"/>'.format(
            url=obj.photo.url,
            # width=obj.photo.width,
            # height=obj.headshot.height,
        )
        )
    photo_show.allow_tags = True

    class Meta:
        model = Users


admin.site.register(Users, UsersAdmin)
admin.site.register(QAdmins, QAdminsAdmin)
admin.site.register(Clients, ClientsAdmin)

admin.site.register(UsersConsentQliento)
admin.site.unregister(Group)
