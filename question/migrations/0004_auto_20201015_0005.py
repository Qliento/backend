# Generated by Django 2.2.8 on 2020-10-14 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_havequestion_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnershipInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Информация о партнерстве',
                'verbose_name_plural': 'Информация о партнерстве',
            },
        ),
        migrations.AddField(
            model_name='partnership',
            name='partnership',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, related_name='partnership', to='question.PartnershipInfo'),
            preserve_default=False,
        ),
    ]
