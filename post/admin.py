from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin,TabbedDjangoJqueryTranslationAdmin

# Register your models here.

class ImagePostAdmin(admin.TabularInline):
    model = ImagePost


class PostAdmin(TabbedTranslationAdmin):
    inlines = [ImagePostAdmin, ]
    pass

class ImageInfoAdmin(admin.TabularInline):
    model = ImageInfo

class InfoAdmin(TabbedTranslationAdmin):
    inlines = [ImageInfoAdmin, ]
    pass

class NewsAdmin(TabbedTranslationAdmin):
    search_fields = ['name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows': '50', 'columns': '50'})},
    }
    pass

admin.site.register(Info, InfoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(News, NewsAdmin)