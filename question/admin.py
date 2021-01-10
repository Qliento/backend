from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedDjangoJqueryTranslationAdmin
from django.forms import TextInput, Textarea
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin, TranslationTabularInline


# Register your models here.


class PartnershipAdmin(TranslationTabularInline):
    model = Partnership


class PartnershipInfoAdmin(admin.ModelAdmin):
    inlines = [PartnershipAdmin, ]
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})},
                           }


class QuestionAdmin(TabbedDjangoJqueryTranslationAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 50,
                                  'style': 'height: 5em;'})
                           },
                           }
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(PartnershipInfo, PartnershipInfoAdmin)
admin.site.register(HaveQuestion)
admin.site.register(Feedback)
