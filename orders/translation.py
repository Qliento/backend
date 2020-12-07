from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(ShortDescriptions)
class MobAppTranslationOptions(TranslationOptions):
    fields = ('text1',)


@register(Instructions)
class MobAppTranslationOptions(TranslationOptions):
    fields = ('name', )
