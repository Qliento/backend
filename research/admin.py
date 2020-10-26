from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin
# Register your models here.
from django.http import HttpResponseRedirect
from orders.serializers import to_dict
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings
from mptt.admin import DraggableMPTTAdmin


class CategoryAdmin(DraggableMPTTAdmin, TranslationAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_researches_count', 'related_researches_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Research,
                'category',
                'researches_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Research,
                 'category',
                 'researches_count',
                 cumulative=False)
        return qs

    def related_researches_count(self, instance):
        return instance.researches_count
    related_researches_count.short_description = 'Related researches (for this specific category)'

    def related_researches_cumulative_count(self, instance):
        return instance.researches_cumulative_count
    related_researches_cumulative_count.short_description = 'Related researches (in tree)'
    search_fields = ['name']


class ResearchAdmin(TabbedDjangoJqueryTranslationAdmin):

        change_form_template = "admin/acceptordeny.html"

        def response_change(self, request, obj):
            if "_approve" in request.POST:
                mail = EmailMessage(' Ваше исследование было одобрено',
                                    'Доброго времени суток, {}. \n'
                                    'Поздравляем! По вашему запросу, ваше исследование, детали которого описаны ниже, было одобрено.\n'
                                    'Название: "{}" \n'
                                    'Идентификатор: {} \n'
                                    '\n'
                                    'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id),
                                    settings.EMAIL_HOST_USER,
                                    [obj.author.admin_status.email])

                mail.send()

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


class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']


class CountryAdmin(TranslationAdmin):
    search_fields = ['name']


admin.site.register(Status)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)