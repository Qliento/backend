from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin
from django.forms import TextInput, Textarea

# Register your models here.


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


admin.site.register(MainPage)
admin.site.register(MobApp, MobAppAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(SocialNetworks)
