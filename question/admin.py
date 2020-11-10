from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin


# Register your models here.

class PartnershipAdmin(admin.TabularInline):
	model = Partnership
class PartnershipInfoAdmin(admin.ModelAdmin):
    inlines = [PartnershipAdmin, ]

class PartnershipAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass

class QuestionAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(PartnershipInfo, PartnershipInfoAdmin)
admin.site.register(HaveQuestion)
admin.site.register(Feedback)