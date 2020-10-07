from django.contrib import admin
from .models import *
from research.models import Category
from post.models import News
from post.admin import NewsAdmin
# Register your models here.
class MainPageAdmin(admin.ModelAdmin):
    autocomplete_fields  = ['news', 'categories']





admin.site.register(MainPage, MainPageAdmin)
admin.site.register(MobApp)
admin.site.register(ContactInfo)
