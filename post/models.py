from django.db import models
from research.models import Research
# Create your models here.
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
class Info(models.Model):
	header = models.CharField(max_length = 255, verbose_name = _("Заголовок"))
	description = models.TextField(verbose_name = _('Описание'))
	def __str__(self):
		return self.header
	class Meta:
		verbose_name = _('О нас')
		verbose_name_plural = _('О нас')

class Post(models.Model):
	header = models.CharField(max_length = 255, verbose_name = _('Заголовок'))
	description = models.TextField(verbose_name = _('Описание'))
	date = models.DateField(auto_now_add=True, verbose_name = _('Дата публикации'))
	research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name = _('Исследование'))

	def __str__(self):
		return self.header
	class Meta:
		verbose_name = _('Блог')
		verbose_name_plural = _('Блог')

class ImagePost(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='images')

	class Meta:
		verbose_name = _('Изображение для окна блога')
		verbose_name_plural = _('Изображения для окна блога')


class ImageInfo(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	info = models.ForeignKey(Info, on_delete = models.CASCADE, related_name = 'images')
	class Meta:
		verbose_name = _('Изображение для окна о нас')
		verbose_name_plural = _('Изображения для окна о нас')

	


class News(models.Model):
	name = models.CharField(max_length = 255, verbose_name = _('Заголовок'))
	image = models.ImageField(null = True, blank = True, verbose_name = _('Изображение'))
	description = models.TextField(verbose_name = _('Описание'))
	date = models.DateField(auto_now_add=True, verbose_name = _('Дата публикации'))
	source = models.CharField(max_length=200, verbose_name = _('Источник'), null = True, blank = True,)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.image = self.compressImage(self.image)
		super(News, self).save(*args, **kwargs)

	def compressImage(self,image):
		imageTemproary = Image.open(image)
		outputIoStream = BytesIO()
		imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
		imageTemproary.save(outputIoStream , format='JPEG', quality=70)
		outputIoStream.seek(0)
		image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
		return image

	class Meta:
		verbose_name = _('Новость')
		verbose_name_plural = _('Новости')





