from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _
from registration.models import QAdmins


# Create your models here.
class Category(MPTTModel):
	name = models.CharField(max_length=200, verbose_name = _('Название'))
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name = _('Категория'))

	def __str__(self):
		return self.name

	def get_parent(self):
		return self.parent

	class MPTTMeta:

		order_insertion_by = ['name']

	class Meta:
		verbose_name = _('Категория')
		verbose_name_plural = _('Категории')

	def get_recursive_product_count(self):

		return Research.objects.filter(category__in=self.get_descendants(include_self=True)).count()

	def get_categories(self):
		return self.get_descendants(include_self=True)


class Status(models.Model):

	name = models.CharField(max_length = 1000, verbose_name = _("Статус"))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Статус')
		verbose_name_plural = _('Статусы')


class Hashtag(models.Model):
	name = models.CharField(max_length = 255, unique=True, verbose_name = _('Ключевое слово'))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Ключевое слово')
		verbose_name_plural = _('Ключевые слова')


class Country(models.Model):
	name = models.CharField(max_length = 255, unique=True, verbose_name = _('Страна'))

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Страна')
		verbose_name_plural = _('Страны')


class Research(models.Model):
	name = models.CharField(max_length = 1000, verbose_name = _('Название'))
	image = models.FileField(null = True, blank = True, upload_to='images', verbose_name = _('Изображение'))
	date = models.DateField(auto_now_add = True, verbose_name = _('Дата публикации'))
	pages = models.IntegerField(verbose_name = _('Количество страниц'))
	old_price = models.IntegerField(verbose_name = _('Старая цена'))
	new_price = models.IntegerField(verbose_name = _('Новая цена'))
	description = models.TextField(verbose_name = _('Описание'))
	content = models.TextField( verbose_name = _('Содержание'))
	hashtag = models.ManyToManyField(Hashtag, verbose_name = _('Ключевые слова'))
	category = models.ForeignKey('Category', null=True, blank=True, on_delete = models.CASCADE, verbose_name = _('Категория'))
	demo = models.FileField(null = True, blank = True, upload_to='demos', verbose_name = _('Демоверсия'))
	country = models.ManyToManyField(Country, verbose_name = _('Страна'), null = True)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, default='1', verbose_name = _('Статус'))
	research = models.FileField(null = True, blank = True, verbose_name = _('Исследование'))
	similars = models.ManyToManyField('self', verbose_name = _('Похожие исследования'), null = True, blank = True)

	author = models.ForeignKey(QAdmins, on_delete=models.CASCADE, related_name='creator', null=True, blank=True)

	def similar_researches(self):
		return type(self).objects.prefetch_related('hashtag').filter(status=2).exclude(id=self.id)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('Исследование')
		verbose_name_plural = _('Исследования')
	

