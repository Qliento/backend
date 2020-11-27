from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Status)
class StatusTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Hashtag)
class HashtagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Research)
class ResearchShotsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
