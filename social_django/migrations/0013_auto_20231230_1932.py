# Generated by Django 3.2.23 on 2023-12-30 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0012_auto_20230622_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 30, 19, 32, 54, 441587)),
        ),
        migrations.AlterField(
            model_name='partial',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 30, 19, 32, 54, 441587)),
        ),
        migrations.AlterField(
            model_name='usersocialauth',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 30, 19, 32, 54, 441587)),
        ),
    ]
