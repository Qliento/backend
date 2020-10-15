# Generated by Django 2.2.8 on 2020-10-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnership',
            name='description_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='Информация о партнерстве'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='description_ky',
            field=models.CharField(max_length=1000, null=True, verbose_name='Информация о партнерстве'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='description_ru',
            field=models.CharField(max_length=1000, null=True, verbose_name='Информация о партнерстве'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='header_en',
            field=models.CharField(max_length=1000, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='header_ky',
            field=models.CharField(max_length=1000, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='partnership',
            name='header_ru',
            field=models.CharField(max_length=1000, null=True, verbose_name='Заголовок'),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_en',
            field=models.CharField(max_length=300, null=True, verbose_name='Ответ'),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_ky',
            field=models.CharField(max_length=300, null=True, verbose_name='Ответ'),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_ru',
            field=models.CharField(max_length=300, null=True, verbose_name='Ответ'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Вопрос'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Вопрос'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Вопрос'),
        ),
    ]
