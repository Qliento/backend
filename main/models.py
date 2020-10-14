from django.db import models
from django.db.models import Count
# Create your models here.

class ContactInfo(models.Model):

	def __str__(self):
		return "Контактная информация"
	class Meta:
		verbose_name = 'Контактная информация'
		verbose_name_plural = 'Контактная информация'

class Contact(models.Model):
	info = models.CharField(max_length=255, verbose_name = 'Данные')

	contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name = 'contacts')


	class Meta:
		verbose_name = 'Контактные данные'
		verbose_name_plural = 'Контактные данные'

class MobApp(models.Model):
	description = models.CharField(max_length = 1000, verbose_name = 'Описание')
	image = models.ImageField(null = True, blank = True, upload_to='images', verbose_name = 'Изображение')
	url = models.URLField(max_length=250, verbose_name = 'Ссылка')
	def __str__(self):
		return "Информация о мобильном прижении"
	class Meta:
		verbose_name = 'Раздел о моб. приложении'
		verbose_name_plural = 'Раздел о моб. приложении'

class MainPage(models.Model):
	mob_app = models.ForeignKey(MobApp, on_delete = models.CASCADE, verbose_name = 'Информация о мобильном приложении') 
	сontacts = models.ForeignKey(ContactInfo, on_delete = models.CASCADE, verbose_name = 'Контакты') 

	def __str__(self):
		return "Информация на главной странице"
	class Meta:
		verbose_name = 'Главная страница'
		verbose_name_plural = 'Главная страница'


