from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class PartnershipInfo(models.Model):

	def __str__(self):
		return "Партнерство"
	class Meta:
		verbose_name = _('Информация о партнерстве')
		verbose_name_plural = _('Информация о партнерстве')

class Partnership(models.Model):
	header = models.CharField(max_length = 1000, verbose_name = _('Заголовок'))
	description = models.TextField( verbose_name = _('Информация о партнерстве'))
	partnership = models.ForeignKey(PartnershipInfo, on_delete=models.CASCADE, related_name='partnership')

	def __str__(self):
		return "Партнерство"
	class Meta:
		verbose_name = _('Партнерство')
		verbose_name_plural = _('Партнерство')

class Question(models.Model):
	question = models.CharField(max_length = 255, verbose_name = _('Вопрос'))
	answer = models.CharField(max_length = 300, verbose_name = _('Ответ'))
	def __str__(self):
		return self.question
	class Meta:
		verbose_name = _('ЧАВО')
		verbose_name_plural = _('ЧАВО')

class Feedback(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _('ФИО'))
	name_of_organization = models.CharField(max_length = 255, null = True, blank = True, verbose_name = _('Название организации'))
	position = models.CharField(max_length = 255, null = True, blank = True, verbose_name = _('Должность'))
	email = models.CharField(max_length = 255, verbose_name = _('Почта'))
	phone = models.CharField(max_length = 255, verbose_name = _('Номер телефона'))
	extra = models.CharField(max_length = 255, verbose_name = _('Дополнительно'))

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = _('Обратная связь(партнерство)')
		verbose_name_plural = _('Обратная связь(партнерство)' )

class HaveQuestion(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _('ФИО'))
	name_of_organization = models.CharField(max_length = 255, null = True, blank = True, verbose_name = _('Название организации'))
	email = models.CharField(max_length = 255, verbose_name = _('Почта'))
	phone = models.CharField(max_length = 255, verbose_name = _('Номер телефона'))
	extra = models.CharField(max_length = 255, verbose_name = _('Ваш вопрос'))

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = _('Обратная связь(вопросы)')
		verbose_name_plural = _('Обратная связь(вопросы)')
