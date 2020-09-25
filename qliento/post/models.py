from django.db import models

# Create your models here.

class Info(models.Model):
	header = models.CharField(max_length = 255)
	description = models.CharField(max_length = 1000)
	image = models.ImageField(null = True, blank = True)

	def __str__(self):
		return self.header

class Post(models.Model):
	header = models.CharField(max_length = 255)
	description = models.CharField(max_length = 1000)
	date = models.DateField(auto_now_add=True)
	image = models.ImageField(null = True, blank = True)

	def __str__(self):
		return self.header

class News(models.Model):
	image = models.ImageField(null = True, blank = True)
	description = models.CharField(max_length = 2000)
	date = models.DateField(auto_now_add=True)




