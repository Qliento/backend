from django.contrib import admin
from .models import *
from django import forms

# Register your models here.

from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin


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


class ResearchAdmin(TranslationAdmin):
    autocomplete_fields  = ['hashtag', 'country']
    list_display = ('name', 'status', )
    list_filter = (StatusesListFilter, )

class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']

class CountryAdmin(TranslationAdmin):
    search_fields = ['name']

class CategoryAdmin(TranslationAdmin):
    form = CategoryForm
    list_display = ('name', 'parent', )



class StatusAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Status, StatusAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)