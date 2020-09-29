# Generated by Django 3.1.1 on 2020-09-27 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.category')),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('pages', models.IntegerField()),
                ('old_price', models.IntegerField()),
                ('new_price', models.IntegerField()),
                ('hashtag', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('demo', models.FileField(blank=True, null=True, upload_to='')),
                ('status', models.BooleanField(default=False)),
                ('research', models.FileField(blank=True, null=True, upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.category')),
                ('subCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='research.subcategory')),
            ],
        ),
    ]
