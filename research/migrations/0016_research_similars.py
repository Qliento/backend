# Generated by Django 3.1.1 on 2020-10-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0015_auto_20201002_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='similars',
            field=models.ManyToManyField(blank=True, null=True, related_name='_research_similars_+', to='research.Research', verbose_name='Похожие исследования'),
        ),
    ]
