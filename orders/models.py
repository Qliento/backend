from django.db import models
from research.models import Research
from registration.models import Users
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Orders(models.Model):
    ordered_researches = models.ForeignKey(Research, on_delete=models.CASCADE, default=1, related_name='researches')
    date_added = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    customer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='buyer')
    total = models.IntegerField(blank=True, null=True)

    @property
    def get_total(self):
        return self.ordered_researches.new_price
    # def get_total(self):
    #     final = []
    #     for total in self.ordered_researches.new_price:
    #     self.total = sum(final)
    #     return sum(final)

    # def save(self, *args, **kwargs):
    #     self.total = self.get_total()
    #     super(Orders).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _('Заказы')


class OrderForm(models.Model):
    name = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name="ФИО")
    logo = models.CharField(blank=True, null=True, verbose_name="Название организации", max_length=100)
    email = models.EmailField(max_length=120, unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(default=0000, verbose_name='Номер телефона', max_length=20)
    description = models.TextField()

    class Meta:
        verbose_name = _("Форма заказа")
        verbose_name_plural = _('Формы заказов')
