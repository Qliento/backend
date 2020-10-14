from django.contrib import admin
from .models import *
# Register your models here.

class PartnershipAdmin(admin.TabularInline):
	model = Partnership
class PartnershipInfoAdmin(admin.ModelAdmin):
    inlines = [PartnershipAdmin, ]

admin.site.register(Question)
admin.site.register(PartnershipInfo, PartnershipInfoAdmin)
admin.site.register(HaveQuestion)