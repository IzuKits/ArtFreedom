# Generated by Django 3.1.1 on 2020-09-19 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200919_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge_article',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 19, 22, 27, 5, 111199), verbose_name='дата начала'),
        ),
        migrations.AlterField(
            model_name='image',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание к картинке'),
        ),
    ]
