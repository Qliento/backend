from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin
# Register your models here.

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
    pass


class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']


class CountryAdmin(TranslationAdmin):
    search_fields = ['name']


admin.site.register(Status)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)