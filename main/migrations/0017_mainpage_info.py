# Generated by Django 2.2.8 on 2020-10-27 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20201026_0047'),
        ('main', '0016_auto_20201026_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpage',
            name='info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.Info'),
            preserve_default=False,
        ),
    ]
