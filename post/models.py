from django.db import models
from research.models import Research
# Create your models here.

class Info(models.Model):
	header = models.CharField(max_length = 255, verbose_name = "Заголовок")
	description = models.CharField(max_length = 1000)

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = 'О нас'
		verbose_name_plural = 'О нас'



class Post(models.Model):
	header = models.CharField(max_length = 255, verbose_name = 'Заголовок')
	description = models.CharField(max_length = 1000, verbose_name = 'Описание')
	date = models.DateField(auto_now_add=True, verbose_name = 'Дата публикации')
	research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name = 'Исследование')

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = 'Аналитика'
		verbose_name_plural = 'Аналитика'

class ImagePost(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='images')

	class Meta:
		verbose_name = 'Изображение для окна аналитики'
		verbose_name_plural = 'Изображения для окна аналитики'


class ImageInfo(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	info = models.ForeignKey(Info, on_delete = models.CASCADE, related_name = 'images')
	class Meta:
		verbose_name = 'Изображение для окна о нас'
		verbose_name_plural = 'Изображения для окна о нас'
	


class News(models.Model):
	header = models.CharField(max_length = 255, verbose_name = 'Заголовок')
	image = models.ImageField(null = True, blank = True, verbose_name = 'Изображение')
	description = models.CharField(max_length = 2000, verbose_name = 'Описание')
	date = models.DateField(auto_now_add=True, verbose_name = 'Дата публикации')
	source = models.CharField(max_length=200, verbose_name = 'Источник')

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'




