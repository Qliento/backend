from django.db import models
from registration.models import Users
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, m2m_changed
from registration.utils import Util
from django.db.models import Sum
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings


class Orders(models.Model):
    completed = models.BooleanField(null=True, blank=True, default=False)
    buyer = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name="buyer", verbose_name="Покупатель")
    total_sum = models.IntegerField(blank=True, null=True, verbose_name="Общая сумма")

    class Meta:
        verbose_name = _("Корзина клиента")
        verbose_name_plural = _('Корзины клиентов')

    @property
    def get_total_from_cart(self):
        try:
            price = Cart.objects.filter(user_cart=self.pk).aggregate(Sum('total_of_all'))
            self.total_sum = price.get('total_of_all__sum')
            return self.total_sum
        except:
            raise ValueError

    def save(self, *args, **kwargs):
        return super(Orders, self).save(*args, **kwargs)


class Cart(models.Model):
    ordered_item = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='ordered_items', default=1, null=True, blank=True, verbose_name="Исследования")
    total_of_all = models.IntegerField(blank=True, null=True, verbose_name="Цена")
    added = models.BooleanField(null=True, blank=True, default=False, verbose_name="Куплено")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    user_cart = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='user_cart', default=1, blank=True, null=True, verbose_name="Корзина")

    def __str__(self):
        return '{}'.format(self.ordered_item)

    @property
    def calculate_total_price(self):
        research_objects = Research.objects.filter(ordered_items=self.pk)
        for i in research_objects:
            initial_price = i.new_price
            if initial_price:
                self.total_of_all = initial_price
                return self.total_of_all
            elif i.old_price:
                self.total_of_all = i.old_price
                return self.total_of_all
            else:
                pass

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Товар в корзине покупателя")
        verbose_name_plural = _('Товары в корзинах покупателей')


class Check(models.Model):
    ordered_researches = models.ManyToManyField(Research, verbose_name="Исследования")
    total_price = models.IntegerField(verbose_name="Общая стоимость")
    date = models.DateTimeField(verbose_name="Время покупки")
    client_bought = models.CharField(max_length=100, verbose_name="Почта покупателя")
    order_id = models.CharField(max_length=500, verbose_name="Номер заказа", null=True, blank=True)

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
    description = models.TextField(verbose_name='Описание')

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
    desired_research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name='Исследование', related_name='wanted_research')

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

        return super(DemoVersionForm, self).save(*args, **kwargs)


class ShortDescriptions(models.Model):
    title = models.CharField(max_length=120, default='Название', null=True, blank=True, verbose_name="Заголовок")
    picture1 = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    text1 = models.TextField(blank=True, null=True, verbose_name=_('Текст'))

    class Meta:
        verbose_name = _("Заказать исследование")
        verbose_name_plural = _('Заказать исследования')


class StatisticsDemo(models.Model):
    count_demo = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.count_demo)


class StatisticsWatches(models.Model):
    count_watches = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class StatisticsBought(models.Model):
    count_purchases = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Statistics(models.Model):
    research_to_collect = models.ForeignKey(Research, on_delete=models.CASCADE, related_name='research_of_admin', verbose_name="Исследование", default=1)
    demo_downloaded = models.ForeignKey(StatisticsDemo, null=True, blank=True, on_delete=models.CASCADE, related_name='demos_downloaded', verbose_name="Количество скачанных демо-версий")
    watches = models.ForeignKey(StatisticsWatches, null=True, blank=True, on_delete=models.CASCADE, related_name='watches_counted', verbose_name="Количество просмотров")
    bought = models.ForeignKey(StatisticsBought, null=True, blank=True, on_delete=models.CASCADE, related_name='bought_researches', verbose_name="Количество скачиваний")

    class Meta:
        verbose_name = _("Статистика")
        verbose_name_plural = _('Статистика')

    @property
    def get_name_partner(self):
        return '{}'.format(self.research_to_collect.author)

    @property
    def get_demo_downloaded(self):
        count_demos = Research.objects.filter(research_of_admin=self.pk).aggregate(demo_total=Sum('research_of_admin__demo_downloaded'))
        return count_demos.get('demo_total')

    @property
    def get_total_watches(self):
        count_watched_researches = Research.objects.filter(research_of_admin=self.pk).aggregate(watches_total=Sum('research_of_admin__watches'))
        return count_watched_researches.get('watches_total')


def create_stat_for_qadmin(sender, **kwargs):
    details_for_stat = kwargs['instance']
    Statistics.objects.create(research_to_collect=details_for_stat)


post_save.connect(create_stat_for_qadmin, sender=Research)
