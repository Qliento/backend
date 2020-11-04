from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin
# Register your models here.
from django.http import HttpResponseRedirect
from .models import Status
from orders.serializers import to_dict
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin

    
# class ResearchAdmin(TranslationAdmin):
#     autocomplete_fields  = ['hashtag', 'country']


class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']


class ResearchFileAdmin(admin.TabularInline):
    model = ResearchFiles


class ResearchAdmin(TabbedDjangoJqueryTranslationAdmin):
    inlines = [ResearchFileAdmin, ]
    change_form_template = "admin/acceptordeny.html"
    autocomplete_fields = ['hashtag', 'country']

    def response_change(self, request, obj):
        if "_approve" in request.POST:
            get_some_status_2 = Status.objects.get(id=2)
            obj.status = get_some_status_2

            mail = EmailMessage(' Ваше исследование было одобрено',
                                'Доброго времени суток, {}. \n'
                                'Поздравляем! По вашему запросу, ваше исследование, детали которого описаны ниже, было одобрено.\n'
                                'Название: "{}" \n'
                                'Идентификатор: {} \n'
                                '\n'
                                'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id),
                                settings.EMAIL_HOST_USER,
                                [obj.author.admin_status.email])

            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    def delete_model(self, request, obj):

        mail = EmailMessage(' Ваше исследование было отклонено',
                            'Доброго времени суток, {}. \n'
                            'К сожалению, ваше исследование, детали которого описаны ниже, было отклонено.\n'
                            'Название: "{}" \n'
                            'Идентификатор: {} \n'
                            '\n'
                            'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id),
                            settings.EMAIL_HOST_USER,
                            [obj.author.admin_status.email])

        mail.send()

        return super().delete_model(request, obj)


class CountryAdmin(TranslationAdmin):
    search_fields = ['name']


class CategoryAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


class StatusAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(ResearchFiles)
admin.site.register(Status, StatusAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)
