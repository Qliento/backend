from django.contrib import admin
from .models import *
from django import forms
from modeltranslation.admin import TranslationStackedInline
from jet.admin import CompactInline
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
from django.forms import TextInput, Textarea
from orders.models import Statistics
from registration.models import Users
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from registration.utils import Util


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), label = "Категория",required=False)


class StatusesListFilter(admin.SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'
    default_value = None

    def lookups(self, request, model_admin):
        list_of_statuses = []
        queryset = Status.objects.all()
        for status in queryset:
            list_of_statuses.append(
                (str(status.id), status.name)
            )
        return sorted(list_of_statuses, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status_id=self.value())
        return queryset


class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
    }


class ResearchFileAdmin(admin.TabularInline):
    model = ResearchFiles


class ResearchContentInline(TranslationStackedInline):
    model = ResearchContent

class ResearchForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None), label = "Категория", required=False)

class ResearchAdmin(TabbedDjangoJqueryTranslationAdmin):
    form = ResearchForm
    inlines = [ResearchFileAdmin, ResearchContentInline]
    change_form_template = "admin/acceptordeny.html"
    autocomplete_fields = ['hashtag', 'country']
    list_display = ('name', 'status', 'id')
    list_filter = (StatusesListFilter, )

    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
    }

    def _response_post_save(self, request, obj):

        try:
            super_user_email = obj.author
            get_user_detail = Users.objects.filter(email=super_user_email.admin_status.email)

            for one_su in get_user_detail:
                if one_su.is_superuser:
                    r = Statistics.objects.create(research_to_collect=obj)
                else:
                    pass
        except:
            pass

        return super()._response_post_save(request, obj)

    def response_change(self, request, obj):

        if "_approve" in request.POST:
            get_some_status_2 = Status.objects.get(id=2)
            obj.status = get_some_status_2
            obj.save()

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

        if "_discount" in request.POST:
            get_some_status_4 = Status.objects.get(id=4)
            obj.status = get_some_status_4
            obj.save()
            email_body = 'Доброго времени суток, {}. \n' + \
                         'Мы рассмотрели вашу заявку и рады сообщить, что осталось совсем немного!\n' + \
                         'Осталось добавить скидочную цену в личном кабинете, после чего мы его рассмотрим его и обновим статус вашего исследования. \n' + \
                         'Название: "{}" \n' + \
                         'Идентификатор: {} \n' + \
                         '\n' + \
                         '{}\n' + \
                         'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id, obj.comment)

            data = {'email_body': email_body, 'to_email': str(obj.author.admin_status.email), 'email_subject': 'Время добавить скидочную цену!'}
            Util.send_email(data)

        if '_change_discount' in request.POST:
            get_some_status_4 = Status.objects.get(id=4)
            obj.status = get_some_status_4
            obj.save()

            email_body = 'Доброго времени суток, {}. \n' + \
                         'К сожалению, ваша скидочная цена {} - не одобрена.\n' + \
                         'Вы можете отправить повторный запрос на установление скидочной цены исследования в личном кабинете. \n' + \
                         'Название: "{}" \n' + \
                         'Идентификатор: {} \n' + \
                         '\n' + \
                         '{}\n' + \
                         'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id, obj.comment)

            data = {'email_body': email_body, 'to_email': str(obj.author.admin_status.email), 'email_subject': 'Поправка скидочной цены'}
            Util.send_email(data)

            return HttpResponseRedirect(".")

        if '_refuse' in request.POST:
            get_some_status_3 = Status.objects.get(id=3)
            obj.status = get_some_status_3
            obj.save()

            email_body = ' Ваше исследование было отклонено' + \
                         'Доброго времени суток, {}. \n' + \
                         'К сожалению, ваше исследование, детали которого описаны ниже, было отклонено.\n' + \
                         'Название: "{}" \n' + \
                         'Идентификатор: {} \n' + \
                         '{}\n' + \
                         'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id, obj.comment)

            data = {'email_body': email_body, 'to_email': str(obj.author.admin_status.email), 'email_subject': 'Поправка скидочной цены'}
            Util.send_email(data)

        return super().response_change(request, obj)

    def delete_model(self, request, obj):

        email_body = ' Ваше исследование было удалено' + \
                     'Доброго времени суток, {}. \n' + \
                     'К сожалению, ваше исследование, детали которого описаны ниже, было удалено.\n' + \
                     'Название: "{}" \n' + \
                     'Идентификатор: {} \n' + \
                     '\n' + \
                     'С уважением, команда Qliento'.format(obj.author, obj.name, obj.id)

        data = {'email_body': email_body, 'to_email': str(obj.author.admin_status.email), 'email_subject': 'Поправка скидочной цены'}
        Util.send_email(data)

        return super().delete_model(request, obj)


class CountryAdmin(TranslationAdmin):
    search_fields = ['name']


class CategoryAdmin(DraggableMPTTAdmin, TranslationAdmin):
    
    form = CategoryForm

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
    related_researches_count.short_description = 'Исследования в данной категории'  

    def related_researches_cumulative_count(self, instance):    
        return instance.researches_cumulative_count 
    related_researches_cumulative_count.short_description = 'Исследования в ветке'  
    search_fields = ['name']


class StatusAdmin(TabbedDjangoJqueryTranslationAdmin):
    list_display = ['id']
    pass


class ResearchContentAdmin(admin.ModelAdmin):
    fields = ['page', 'content', 'content_data']
    readonly_fields = ['page', 'content', 'content_data']


admin.site.register(ResearchFiles)
admin.site.register(Status, StatusAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)
# admin.site.register(ResearchContent, ResearchContentAdmin)
