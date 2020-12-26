from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from django.forms import TextInput, Textarea
from django import forms

# Register your models here.

class MainPageForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(parent=None), label = "Категория", required=False)

class ContactAdmin(admin.TabularInline):

    model = Contact


class ContactInfoAdmin(admin.ModelAdmin):

    inlines = [ContactAdmin, ]


class MobAppAdmin(TabbedTranslationAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
                           }
    pass

class MainPageAdmin(admin.ModelAdmin):
	form = MainPageForm

admin.site.register(MainPage, MainPageAdmin)
admin.site.register(MobApp, MobAppAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(SocialNetworks)
