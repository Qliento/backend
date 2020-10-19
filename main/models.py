from django.db import models
from research.models import Category
from post.models import Post
# Create your models here.
from django.utils.translation import ugettext_lazy as _


class ContactInfo(models.Model):

	def __str__(self):
		return "Контактная информация"
	class Meta:
		verbose_name = _('Контактная информация')
		verbose_name_plural = _('Контактная информация')

class Contact(models.Model):
	info = models.CharField(max_length=255, verbose_name = _('Данные'))

	contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name = 'contacts')


	class Meta:
		verbose_name = _('Контактные данные')
		verbose_name_plural = _('Контактные данные')

class MobApp(models.Model):
	description = models.TextField(verbose_name = _('Описание'))
	image = models.ImageField(null = True, blank = True, upload_to='images', verbose_name = _('Изображение'))
	url = models.URLField(max_length=250, verbose_name = _('Ссылка'))
	def __str__(self):
		return "Информация о мобильном прижении"
	class Meta:
		verbose_name = _('Раздел о моб. приложении')
		verbose_name_plural = _('Раздел о моб. приложении')

class MainPage(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ManyToManyField(Category, verbose_name="Категории")
	mob_app = models.ForeignKey(MobApp, on_delete = models.CASCADE, verbose_name = _('Информация о мобильном приложении')) 
	сontacts = models.ForeignKey(ContactInfo, on_delete = models.CASCADE, verbose_name = _('Контакты')) 

	def __str__(self):
		return "Информация на главной странице"
	class Meta:
		verbose_name = _('Главная страница')
		verbose_name_plural = _('Главная страница')


