# Generated by Django 2.2.16 on 2020-10-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnership',
            name='description',
            field=models.TextField(verbose_name='Информация о партнерстве'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Информация о партнерстве'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='description_ky',
            field=models.TextField(null=True, verbose_name='Информация о партнерстве'),
        ),
        migrations.AlterField(
            model_name='partnership',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Информация о партнерстве'),
        ),
    ]
