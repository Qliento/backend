# Generated by Django 2.2.8 on 2020-10-05 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('research', '0016_research_tags'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.PositiveIntegerField(blank=True, max_length=4, null=True)),
                ('total', models.IntegerField()),
                ('ordered_researches', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='researches', to='research.Research')),
            ],
        ),
        migrations.CreateModel(
            name='OrderForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='ФИО', max_length=120, verbose_name='ФИО')),
                ('logo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Название организации')),
                ('email', models.EmailField(max_length=120, unique=True, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(default=0, max_length=20, verbose_name='Номер телефона')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.Cart')),
                ('who_buys', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
