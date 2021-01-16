from modeltranslation.translator import register, TranslationOptions
from .models import *
from registration.models import UsersConsentQliento


@register(Partnership)
class PartnershipTranslationOptions(TranslationOptions):
    fields = ('header', 'description', )


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'answer', )


@register(UsersConsentQliento)
class UserConsentQlientoTranslation(TranslationOptions):
    fields = ('text',)
