from django.db import models

# Create your models here.

class Info(models.Model):
	header = models.CharField(max_length = 255)
	description = models.CharField(max_length = 1000)

	def __str__(self):
		return self.header
	class Meta:
		verbose_name_plural = "Info"


class Post(models.Model):
	header = models.CharField(max_length = 255)
	description = models.CharField(max_length = 1000)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.header


class ImagePost(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	post = models.ForeignKey(Post, on_delete = models.CASCADE)

class ImageInfo(models.Model):
	url = models.ImageField(null = True, blank = True, upload_to='images')
	info = models.ForeignKey(Info, on_delete = models.CASCADE)
	


class News(models.Model):
	header = models.CharField(max_length = 255)
	image = models.ImageField(null = True, blank = True)
	description = models.CharField(max_length = 2000)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.header
	class Meta:
		verbose_name_plural = "News"




