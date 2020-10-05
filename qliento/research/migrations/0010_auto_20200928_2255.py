# Generated by Django 3.1.1 on 2020-09-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0009_auto_20200928_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='research',
            name='hashtag',
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('research', models.ManyToManyField(to='research.Research')),
            ],
        ),
    ]
