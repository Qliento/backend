from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Info)
class InfoTranslationOptions(TranslationOptions):
    fields = ('header', 'description')


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('header', 'description')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


