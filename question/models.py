from django.db import models

# Create your models here.

class PartnershipInfo(models.Model):

	def __str__(self):
		return "Партнерство"
	class Meta:
		verbose_name = 'Информация о партнерстве'
		verbose_name_plural = 'Информация о партнерстве'

class Partnership(models.Model):
	header = models.CharField(max_length = 1000, verbose_name = 'Заголовок')
	description = models.CharField(max_length = 1000, verbose_name = 'Информация о партнерстве')
	partnership = models.ForeignKey(PartnershipInfo, on_delete=models.CASCADE, related_name='partnership')

	def __str__(self):
		return "Партнерство"
	class Meta:
		verbose_name = 'Партнерство'
		verbose_name_plural = 'Партнерство'

class Question(models.Model):
	question = models.CharField(max_length = 255, verbose_name = 'Вопрос')
	answer = models.CharField(max_length = 300, verbose_name = 'Ответ')
	def __str__(self):
		return self.question
	class Meta:
		verbose_name = 'ЧАВО'
		verbose_name_plural = 'ЧАВО'

class Feedback(models.Model):
	name = models.CharField(max_length = 255, verbose_name = 'ФИО')
	name_of_organization = models.CharField(max_length = 255, null = True, blank = True, verbose_name = 'Название организации')
	position = models.CharField(max_length = 255, null = True, blank = True, verbose_name = 'Должность')
	email = models.CharField(max_length = 255, verbose_name = 'Почта')
	phone = models.CharField(max_length = 255, verbose_name = 'Номер телефона')
	extra = models.CharField(max_length = 255, verbose_name = 'Дополнительно')

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Обратная связь(партнерство)'
		verbose_name_plural = 'Обратная связь(партнерство)' 

class HaveQuestion(models.Model):
	name = models.CharField(max_length = 255, verbose_name = 'ФИО')
	name_of_organization = models.CharField(max_length = 255, null = True, blank = True, verbose_name = 'Название организации')
	email = models.CharField(max_length = 255, verbose_name = 'Почта')
	phone = models.CharField(max_length = 255, verbose_name = 'Номер телефона')
	extra = models.CharField(max_length = 255, verbose_name = 'Ваш вопрос')

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Обратная связь(вопросы)'
		verbose_name_plural = 'Обратная связь(вопросы)'
