from django.db import models
from registration.models import Users
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, m2m_changed
from registration.utils import Util
from django.db.models import Sum
from django.core.mail import EmailMessage
from research.models import Research
from django.conf import settings


class Cart(models.Model):
    ordered_item = models.ManyToManyField(Research, related_name='ordered_items', default=1, null=True, blank=True, verbose_name="Исследования")
    total_of_all = models.IntegerField(blank=True, null=True, verbose_name="Общая стоимость")
    buyer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="buyer", verbose_name="Покупатель")
    added = models.BooleanField(null=True, blank=True, default=False)

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.ordered_item)

    class Meta:
        verbose_name = _("Корзина покупателя")
        verbose_name_plural = _('Корзины покупателей')


def add_cart_items(sender, action, **kwargs):
    details = kwargs['pk_set']
    its_id = kwargs['instance']

    if action == 'post_add':
        empty_researches = []
        aggregated_np = Research.objects.filter(ordered_items=its_id.id).aggregate(Sum('new_price'))
        aggregated_op = Research.objects.filter(ordered_items=its_id.id).aggregate(Sum('old_price'))

        for research_details in details:
            data_of_research = Research.objects.filter(id=research_details)
            empty_researches = list(data_of_research.values())

        for one in empty_researches:
            each_cart = Cart.objects.filter(id=its_id.id, added=False)
            try:
                np = one.get('new_price')
                op = one.get('old_price')

                if np is None and aggregated_np.get('new_price__sum') is None:
                    each_cart.update(total_of_all=aggregated_op.get('old_price__sum'))
                elif np or aggregated_np.get('new_price__sum'):
                    each_cart.update(total_of_all=aggregated_np.get('new_price__sum'))
                else:
                    each_cart.update(total_of_all=aggregated_op.get('old_price__sum'))

            except:
                raise ValueError


m2m_changed.connect(add_cart_items, sender=Cart.ordered_item.through)


class ItemsInCart(models.Model):
    items_in_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items_for_sell')


class Orders(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    items_ordered = models.ManyToManyField(Cart, related_name="items_to_pay")

    class Meta:
        verbose_name = _("Пред-покупки клиентов")
        verbose_name_plural = _('Пред-покупки клиентов')

    @property
    def get_total_from_cart(self):
        price = Cart.objects.filter(items_to_pay=self.pk).aggregate(Sum('total_of_all'))
        return price.get('total_of_all__sum')

    def save(self, *args, **kwargs):
        return super(Orders, self).save(*args, **kwargs)


def create_check_info(sender, action, **kwargs):
    details = kwargs['instance']

    if action == 'post_add':

        id_of_cart_objects = details.items_ordered.filter(items_to_pay=details.id)
        get_the_buyer = Cart.objects.get(id=list(kwargs['pk_set'])[0]).buyer

        c = Check.objects.create(total_price=details.get_total_from_cart,
                                 date=details.date_added,
                                 client_bought=get_the_buyer)

        b = Research.objects.filter(ordered_items=list(kwargs['pk_set'])[0])
        for each_research in b:
            c.ordered_researches.add(each_research.id)


m2m_changed.connect(create_check_info, sender=Orders.items_ordered.through)


class Check(models.Model):
    ordered_researches = models.ManyToManyField(Research, verbose_name="Исследования")
    total_price = models.IntegerField(verbose_name="Общая стоимость")
    date = models.DateTimeField(verbose_name="Время покупки")
    client_bought = models.CharField(max_length=100, verbose_name="Почта покупателя")

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


class Instructions(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Краткие инструкции")
        verbose_name_plural = _('Краткие инструкции')

    def __str__(self):
        return self.name


class ShortDescriptions(models.Model):
    picture1 = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    text1 = models.TextField(blank=True, null=True, verbose_name='Текст')
    data_needed = models.ForeignKey(Instructions, on_delete=models.CASCADE, verbose_name="Инструкции", related_name='data_for_instructions')

    class Meta:
        verbose_name = _("Данные для краткого описания")
        verbose_name_plural = _('Данные для краткого описания')


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
