# Generated by Django 3.0.3 on 2020-02-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Просмотры'),
        ),
    ]
