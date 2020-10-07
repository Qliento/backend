from django.contrib import admin
from .models import *
# Register your models here.

class ImagePostAdmin(admin.TabularInline):
	model = ImagePost

class PostAdmin(admin.ModelAdmin):
    inlines = [ImagePostAdmin, ]

class ImageInfoAdmin(admin.TabularInline):
	model = ImageInfo

class InfoAdmin(admin.ModelAdmin):
	inlines = [ImageInfoAdmin, ]

class NewsAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Info, InfoAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(News, NewsAdmin)