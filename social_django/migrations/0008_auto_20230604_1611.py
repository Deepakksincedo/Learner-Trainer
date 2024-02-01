# Generated by Django 3.2.19 on 2023-06-04 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_django', '0007_auto_20230604_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 4, 16, 11, 14, 548275)),
        ),
        migrations.AlterField(
            model_name='partial',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 6, 4, 16, 11, 14, 548275)),
        ),
        migrations.AlterField(
            model_name='usersocialauth',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 4, 16, 11, 14, 548275)),
        ),
    ]