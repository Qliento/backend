from django.contrib import admin
from .models import *



# Register your models here.


class ContactAdmin(admin.TabularInline):
	model = Contact
class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [ContactAdmin, ]




admin.site.register(MainPage)
admin.site.register(MobApp)
admin.site.register(ContactInfo, ContactInfoAdmin)
