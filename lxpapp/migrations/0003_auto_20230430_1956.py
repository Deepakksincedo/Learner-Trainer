# Generated by Django 3.0.14 on 2023-04-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lxpapp', '0002_auto_20230428_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='urlvalue',
            field=models.CharField(max_length=2000),
        ),
    ]