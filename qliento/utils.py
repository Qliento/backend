from django.utils.deprecation import MiddlewareMixin
from django.utils import translation
from django.conf import settings
class ActivateTranslationMiddleware(MiddlewareMixin):
	def process_ewquest(self, request):
		language = request.META.get('HTTP_ACCEPT_LANGUAGE', None)
		if str(language).lower() == 'ky':
			language = 'ky'
		elif str(language).lower() == 'en':
			language = 'en'
		else:
			language = 'ru'
		translation.activate(language)
class AdminLocaleURLMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG
class corsMiddleware(object):
    def process_response(self, req, resp):
        resp["Access-Control-Allow-Origin"] = "*"
        return resp