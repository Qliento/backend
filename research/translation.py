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
    fields = ()


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ()


@register(Research)
class ResearchShotsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'demo', )


@register(ResearchContent)
class ResearchContentTranslationOption(TranslationOptions):
    fields = ['content', 'page']
