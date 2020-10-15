from django.db import models
from research.models import Research
# Create your models here.
from django.utils.translation import ugettext_lazy as _
class Info(models.Model):
	header = models.CharField(max_length = 255, verbose_name = _("Заголовок"))
	description = models.CharField(max_length = 1000)

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = _('О нас')
		verbose_name_plural = _('О нас')



class Post(models.Model):
	header = models.CharField(max_length = 255, verbose_name = _('Заголовок'))
	description = models.CharField(max_length = 1000, verbose_name = _('Описание'))
	date = models.DateField(auto_now_add=True, verbose_name = _('Дата публикации'))
	research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name = _('Исследование'))

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = _('Аналитика')
		verbose_name_plural = _('Аналитика')

class ImagePost(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='images')

	class Meta:
		verbose_name = _('Изображение для окна аналитики')
		verbose_name_plural = _('Изображения для окна аналитики')


class ImageInfo(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	info = models.ForeignKey(Info, on_delete = models.CASCADE, related_name = 'images')
	class Meta:
		verbose_name = _('Изображение для окна о нас')
		verbose_name_plural = _('Изображения для окна о нас')
	


class News(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _('Заголовок'))
	image = models.ImageField(null = True, blank = True, verbose_name = _('Изображение'))
	description = models.CharField(max_length = 2000, verbose_name = _('Описание'))
	date = models.DateField(auto_now_add=True, verbose_name = _('Дата публикации'))
	source = models.CharField(max_length=200, verbose_name = _('Источник'))

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = _('Новость')
		verbose_name_plural = _('Новости')




