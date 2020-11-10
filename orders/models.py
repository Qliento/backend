from django.db import models
from research.models import Research
from registration.models import Users
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from registration.utils import Util
from random import randint
from django.db.models import F
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

    def save(self, *args, **kwargs):

        super(Orders, self).save(*args, **kwargs)

        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.ordered_item)

    class Meta:
        verbose_name = _("Корзина покупателя")
        verbose_name_plural = _('Корзины покупателей')


class ItemsInCart(models.Model):
    items_in_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items_for_sell')


class Orders(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    items_ordered = models.ManyToManyField(Cart, related_name="items_to_pay")


    class Meta:
        verbose_name = _("Покупки клиентов")
        verbose_name_plural = _('Покупки клиентов')

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
        verbose_name = _("Заявка на исследование")
        verbose_name_plural = _('Заявки на исследования')


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


class DemoVersionForm(models.Model):
    name = models.CharField(max_length=120, default='ФИО', null=False, blank=False, verbose_name="ФИО")
    email = models.EmailField(max_length=120, verbose_name="Электронная почта")
    phone_number = models.CharField(default=0000, verbose_name='Номер телефона', max_length=20)
    desired_research = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='wanted_research')

    class Meta:
        verbose_name = _("Заявка на демоверсию")
        verbose_name_plural = _('Заявки демоверсий')

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        research_demo = self.desired_research.id
        email_of_recipient = self.email

        get_pdf_demo = Research.objects.filter(id=research_demo).values()
        normalized_data = list(get_pdf_demo)[0]
        name_of_file = normalized_data.get('demo')
        title_of_file = normalized_data.get('name')
        id_of_file = normalized_data.get('id')

        mail = EmailMessage(' Демо-версия',
                            'Доброго времени суток, пользователь. '
                            'По вашему запросу, вам была отправлена демоверсия исследования в формате PDF. \n'
                            'Название: "{}" \n'
                            'Идентификатор: {} \n'
                            '\n'
                            'С уважением, команда Qliento'.format(title_of_file, id_of_file),
                            settings.EMAIL_HOST_USER,
                            [email_of_recipient])

        mail.attach_file('static/files/{}'.format(name_of_file))
        mail.send()

        Statistics.objects.filter(partner_admin=normalized_data.get('author_id')).update(demo_downloaded=F('demo_downloaded') + 1)
        return super(DemoVersionForm, self).save(*args, **kwargs)


class Instructions(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Краткие инструкции")
        verbose_name_plural = _('Краткие инструкции')

    def __str__(self):
        return self.name


class ShortDescriptions(models.Model):
    picture1 = models.ImageField(blank=True, null=True)
    text1 = models.TextField(blank=True, null=True)
    data_needed = models.ForeignKey(Instructions, on_delete=models.CASCADE, related_name='data_for_instructions')

    class Meta:
        verbose_name = _("Данные для краткого описания")
        verbose_name_plural = _('Данные для краткого описания')


class Statistics(models.Model):
    partner_admin = models.ForeignKey(QAdmins, on_delete=models.CASCADE, related_name='partner_admin')
    demo_downloaded = models.IntegerField()
    watches = models.IntegerField()
    bought = models.IntegerField()

    class Meta:
        verbose_name = _("Статистика")
        verbose_name_plural = _('Статистика')


def create_stat_for_qadmin(sender, **kwargs):
    details_for_stat = kwargs['instance']
    Statistics.objects.create(partner_admin=details_for_stat, demo_downloaded=0, watches=0, bought=0)


post_save.connect(create_stat_for_qadmin, sender=QAdmins)
