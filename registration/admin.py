from django.contrib import admin
from .models import *
from itertools import chain
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


class QAdminsAdmin(admin.ModelAdmin):
    list_display = ['admin_status']

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

    class Meta:
        model = Clients


class UsersAdmin(admin.ModelAdmin):
    list_display = ['email', 'primary_reference', 'initial_reference']

    class Meta:
        model = Users


admin.site.register(Users, UsersAdmin)
admin.site.register(QAdmins, QAdminsAdmin)
admin.site.register(Clients, ClientsAdmin)
