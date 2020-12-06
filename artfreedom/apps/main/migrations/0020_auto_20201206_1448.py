# Generated by Django 3.1.1 on 2020-12-06 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20201130_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge_article',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 6, 14, 48, 58, 631688), verbose_name='дата начала'),
        ),
        migrations.AlterField(
            model_name='challenge_to_user',
            name='role',
            field=models.CharField(choices=[('creator', 'creator'), ('participant', 'participant'), ('banned', 'banned')], max_length=50),
        ),
    ]