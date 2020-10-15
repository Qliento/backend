from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Partnership)
class PartnershipTranslationOptions(TranslationOptions):
    fields = ('header', 'description', )


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question', 'answer', )



