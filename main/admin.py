from django.contrib import admin
from .models import *

from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

# Register your models here.


class ContactAdmin(admin.TabularInline):
	model = Contact
class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [ContactAdmin, ]
class MobAppAdmin(TabbedTranslationAdmin):
    pass



admin.site.register(MainPage)
admin.site.register(MobApp, MobAppAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(SocialNetworks)
