# Generated by Django 3.0.3 on 2020-02-11 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_auto_20200208_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_filled',
            field=models.BooleanField(default=False),
        ),
    ]
