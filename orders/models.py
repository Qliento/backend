from django.db import models
from research.models import Research
from registration.models import Users
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from registration.utils import Util
from django.db.models import Avg, Count, Min, Sum
from random import randint
from django.db.models import F
# Create your models here.


class Cart(models.Model):
    ordered_item = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='ordered_items', default=1)
    amount_of_items = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    total_of_all = models.IntegerField(blank=True, null=True)
    buyer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="buyer")

    @property
    def count_items(self):
        return Research.objects.filter(ordered_items=self.pk).count()

    @property
    def get_cost_of_1(self):
        return self.ordered_item.new_price

    @property
    def get_discount(self):
        return self.ordered_item.old_price - self.ordered_item.new_price

    @property
    def get_general_sum(self):
        return Research.objects.filter(ordered_items=self.pk).aggregate(Sum('new_price'))

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)


class ItemsInCart(models.Model):
    items_in_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items_for_sell')


class Orders(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    items_ordered = models.ForeignKey(ItemsInCart, on_delete=models.CASCADE, related_name="items_to_pay")

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return '{}{}'.format('ID', self.pk)


class OrderForm(models.Model):
    name = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name="Имя")
    surname = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name="Фамилия")
    logo = models.CharField(blank=True, null=True, verbose_name="Название организации", max_length=100)
    email = models.EmailField(max_length=120, verbose_name="Электронная почта")
    phone_number = models.CharField(default=0000, verbose_name='Номер телефона', max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = _("Форма заказа")
        verbose_name_plural = _('Формы заказов')


def send_to_admin(sender, **kwargs):
    details = kwargs['instance']
    data = {'email_body': 'Клиент {}, {} \n'
                          'Контакты: \n''Почта {} \nТелефон {}. \n'
                          '\nЗапрос на новый заказ исследования и его описание: \n'
                          '"{}". '
                          .format(details.name,
                                  details.logo,
                                  details.email,
                                  details.phone_number,
                                  details.description),
            'to_email': 'qlientoinfo@gmail.com',
            'email_subject': 'Новый заказ'}
    Util.send_email(data)


post_save.connect(send_to_admin, sender=OrderForm)

