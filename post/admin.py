from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin,TabbedDjangoJqueryTranslationAdmin


# Register your models here.

class PostForm(forms.ModelForm):
    research = forms.ModelChoiceField(queryset=Research.objects.filter(status = 2), label = "Исследования", required=False)

class ImagePostAdmin(admin.TabularInline):
    model = ImagePost


class PostAdmin(TabbedTranslationAdmin):
    form = PostForm
    inlines = [ImagePostAdmin, ]
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
    }
    pass


class ImageInfoAdmin(admin.TabularInline):
    model = ImageInfo


class InfoAdmin(TabbedTranslationAdmin):
    inlines = [ImageInfoAdmin, ]
    pass


class NewsAdmin(TabbedTranslationAdmin):
    search_fields = ['name']
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
    }
    pass


admin.site.register(Info, InfoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(News, NewsAdmin)
