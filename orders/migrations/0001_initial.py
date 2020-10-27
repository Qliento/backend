# Generated by Django 2.2.8 on 2020-10-16 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('research', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='ФИО', max_length=120, verbose_name='Имя')),
                ('surname', models.CharField(default='ФИО', max_length=120, verbose_name='Фамилия')),
                ('logo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название организации')),
                ('email', models.EmailField(max_length=120, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(default=0, max_length=20, verbose_name='Номер телефона')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Форма заказа',
                'verbose_name_plural': 'Формы заказов',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('ordered_researches', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='researches', to='research.Research')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]