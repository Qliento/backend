# Generated by Django 2.2.8 on 2020-10-15 06:20

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0021_auto_20201014_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ky',
            field=models.CharField(max_length=200, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_en',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='research.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_ky',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='research.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_ru',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='research.Category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='country',
            name='name_en',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='country',
            name='name_ky',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='country',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='name_en',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Ключевое слово'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='name_ky',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Ключевое слово'),
        ),
        migrations.AddField(
            model_name='hashtag',
            name='name_ru',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Ключевое слово'),
        ),
        migrations.AddField(
            model_name='research',
            name='description_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='research',
            name='description_ky',
            field=models.CharField(max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='research',
            name='description_ru',
            field=models.CharField(max_length=1000, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='research',
            name='name_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='research',
            name='name_ky',
            field=models.CharField(max_length=1000, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='research',
            name='name_ru',
            field=models.CharField(max_length=1000, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='status',
            name='name_en',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='name_ky',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='name_ru',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
