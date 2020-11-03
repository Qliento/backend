from django.contrib import admin
from .models import *

# Register your models here.

from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin


    
class ResearchAdmin(TranslationAdmin):
    autocomplete_fields  = ['hashtag', 'country']

class ResearchAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

class HashtagAdmin(TranslationAdmin):
    search_fields = ['name']

class CountryAdmin(TranslationAdmin):
    search_fields = ['name']

class CategoryAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

class HashtagAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

class CountryAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

class StatusAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Status, StatusAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Category)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Country, CountryAdmin)