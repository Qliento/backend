# Generated by Django 3.1.1 on 2020-09-28 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0006_auto_20200928_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='research',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='research.category'),
        ),
    ]
