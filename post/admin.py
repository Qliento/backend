from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin



# Register your models here.

class ImagePostAdmin(admin.TabularInline):
	model = ImagePost

class PostAdmin(TranslationAdmin):
    inlines = [ImagePostAdmin, ]

class ImageInfoAdmin(admin.TabularInline):
	model = ImageInfo

class InfoAdmin(TranslationAdmin):
	inlines = [ImageInfoAdmin, ]

class NewsAdmin(TranslationAdmin):
    search_fields = ['name']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'rows': '50', 'columns': '50'})},
    }
class InfoAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass
class PostAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass
class NewsAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(Info, InfoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(News, NewsAdmin)