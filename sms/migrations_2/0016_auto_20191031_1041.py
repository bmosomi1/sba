# Generated by Django 2.2.4 on 2019-10-31 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0015_auto_20191030_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoing1',
            name='sent_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 10, 31, 10, 41, 1, 831783)),
        ),
    ]