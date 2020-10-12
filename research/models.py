from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=200, verbose_name = 'Название')
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name = 'Категория')
	def __str__(self):
		return self.name
	class MPTTMeta:
		order_insertion_by = ['name']
	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
	def get_recursive_product_count(self):
		return Research.objects.filter(category__in=self.get_descendants(include_self=True)).count()
	
class Status(models.Model):
	name = models.CharField(max_length = 1000)
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Статус'
		verbose_name_plural = 'Статусы'

class Hashtag(models.Model):
	name = models.CharField(max_length = 255, unique=True, verbose_name = 'Ключевое слово')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Ключевое слово'
		verbose_name_plural = 'Ключевые слова'

class Country(models.Model):
	name = models.CharField(max_length = 255, unique=True, verbose_name = 'Страна')
	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Страна'
		verbose_name_plural = 'Страны'
		
class Research(models.Model):
	name = models.CharField(max_length = 1000, verbose_name = 'Название')
	image = models.FileField(null = True, blank = True, upload_to='images', verbose_name = 'Изображение')
	date = models.DateField(auto_now_add = True, verbose_name = 'Дата публикации')
	pages = models.IntegerField(verbose_name = 'Количество страниц')
	old_price = models.IntegerField(verbose_name = 'Старая цена')
	new_price = models.IntegerField(verbose_name = 'Новая цена')
	description = models.CharField(max_length = 1000, verbose_name = 'Описание')
	hashtag = models.ManyToManyField(Hashtag, verbose_name = 'Ключевые слова')
	category = models.ForeignKey('Category', null=True, blank=True, on_delete = models.CASCADE, verbose_name = 'Категория')
	demo = models.FileField(null = True, blank = True, upload_to='demos', verbose_name = 'Демоверсия')
	country = models.ManyToManyField(Country, verbose_name = 'Страна', null = True)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, default='1', verbose_name = 'Статус')
	research = models.FileField(null = True, blank = True, verbose_name = 'Исследование')
	similars = models.ManyToManyField('self', verbose_name = 'Похожие исследования', null = True, blank = True)

	def similar_researches(self):
		return type(self).objects.prefetch_related('hashtag').filter(status=2).exclude(id=self.id)

	def __str__(self):
		return self.name
	class Meta:
		verbose_name = 'Исследование'
		verbose_name_plural = 'Исследования'

