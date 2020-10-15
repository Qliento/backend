from modeltranslation.translator import register, TranslationOptions
from .models import *



@register(MobApp)
class MobAppTranslationOptions(TranslationOptions):
    fields = ('description', )

